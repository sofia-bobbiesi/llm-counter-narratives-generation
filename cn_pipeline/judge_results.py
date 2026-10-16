"""Aplica el LLM-as-judge sobre resultados ya generados (juez en dos fases).

Permite separar la generación (GPU, posiblemente en un nodo sin salida a
internet) del juicio (que requiere acceso al endpoint del juez). Se lee un
`results.csv` ya generado, se puntúan las filas con el LLM-as-judge y se
reescriben `results.csv` (agregando las columnas `judge_*`) y `summary.csv`.

Los aspectos y escalas son los de la rúbrica de `cn_pipeline.llm_judge`
(alineados con la anotación humana del grupo); `judge_promedio` se calcula en
código como media normalizada (0-1) de los cuatro aspectos, igual que en el
juez in-pipeline.

Uso:
    python -m cn_pipeline.judge_results --config configs/config_gemma.json \\
        --run_dir outputs/<exp_id> [--resume]

`--resume` saltea las filas que ya tienen `judge_promedio` numérico y reintenta
solo las fallidas/faltantes. No recomputa BLEU/ROUGE/BERTScore: esas métricas ya
vienen calculadas en `results.csv`.
"""

from __future__ import annotations

import argparse
import os

import pandas as pd

from .config import add_judge_args, apply_judge_overrides, load_config
from .evaluation import summarize
from .llm_judge import JUDGE_ASPECTS, build_judge, judge_promedio, judge_with_retry

REQUIRED_COLUMNS = ("hate_speech", "generated_cn")


def _print_summary(summary: pd.DataFrame) -> None:
    """Imprime el resumen (usa `tabulate` si está; si no, texto plano)."""
    try:
        print(summary.to_markdown(index=False))
    except ImportError:
        print(summary.to_string(index=False))


def judge_results_dir(
    cfg,
    run_dir: str,
    resume: bool = False,
    max_retries: int = 5,
    base_delay: float = 2.0,
) -> pd.DataFrame:
    """Juzga las filas de `run_dir/results.csv` y reescribe results/summary.

    Devuelve el DataFrame resumen (`summary.csv`).
    """
    results_path = os.path.join(run_dir, "results.csv")
    summary_path = os.path.join(run_dir, "summary.csv")
    if not os.path.isfile(results_path):
        raise FileNotFoundError(f"No se encontró {results_path}")

    df = pd.read_csv(results_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(
            f"A {results_path} le faltan columnas requeridas: {missing}"
        )

    judge = build_judge(cfg.llm_judge)
    print(
        f"[judge] modelo={cfg.llm_judge.model} endpoint={cfg.llm_judge.base_url} "
        f"timeout={cfg.llm_judge.timeout}s"
    )

    # Filas a juzgar: con `--resume` se saltean las que ya tienen promedio.
    if resume and "judge_promedio" in df.columns:
        to_judge = df["judge_promedio"].isna()
    else:
        to_judge = pd.Series(True, index=df.index)
        stale = [c for c in df.columns if c.startswith("judge_")]
        if stale:
            df = df.drop(columns=stale)

    indices = df.index[to_judge].tolist()
    print(f"[judge] {len(indices)}/{len(df)} filas a juzgar (resume={resume})")
    if not indices:
        summary = summarize(df)
        df.to_csv(results_path, index=False)
        summary.to_csv(summary_path, index=False)
        _print_summary(summary)
        return summary

    # Juzgar con reintentos; los fallos definitivos se registran como NaN.
    scores_by_index = {}
    for i, idx in enumerate(indices, start=1):
        row = df.loc[idx]
        try:
            scores = judge_with_retry(
                judge,
                str(row["hate_speech"]),
                str(row["generated_cn"]),
                retries=max_retries,
                base_delay=base_delay,
            )
        except Exception as exc:  # no interrumpir el resto por un fallo puntual
            scores = {"error": str(exc)}
        row_scores = {f"judge_{k}": v for k, v in scores.items() if k in JUDGE_ASPECTS}
        # Garantizar las cuatro columnas de aspectos (NaN si el juez las omitió)
        for aspect in JUDGE_ASPECTS:
            row_scores.setdefault(f"judge_{aspect}", float("nan"))
        # El promedio se calcula en código: media normalizada (0-1) de los
        # cuatro aspectos, igual que el juez in-pipeline (`judge_rows`).
        row_scores["judge_promedio"] = judge_promedio(row_scores)
        if "error" in scores:
            row_scores["judge_error"] = scores["error"]
        scores_by_index[idx] = row_scores
        print(f"[judge] {i}/{len(indices)} -> promedio={row_scores['judge_promedio']}")

    # Limpiar errores previos de las filas rejuzgadas y mergear los puntajes.
    judged = list(scores_by_index.keys())
    if "judge_error" in df.columns:
        df.loc[judged, "judge_error"] = pd.NA
    scores_df = pd.DataFrame.from_dict(scores_by_index, orient="index")
    for col in scores_df.columns:
        if col not in df.columns:
            df[col] = pd.NA
        df.loc[scores_df.index, col] = scores_df[col].to_numpy()
    # Asegurar dtype numérico en las métricas del juez (para que `summarize` las promedie).
    for col in df.columns:
        if col.startswith("judge_") and col != "judge_error":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Reordenar: columnas `judge_*` justo después de `generated_cn`.
    judge_cols = [c for c in df.columns if c.startswith("judge_")]
    rest = [c for c in df.columns if not c.startswith("judge_")]
    if "generated_cn" in rest:
        pos = rest.index("generated_cn") + 1
        df = df[rest[:pos] + judge_cols + rest[pos:]]
    else:
        df = df[rest + judge_cols]

    df.to_csv(results_path, index=False)
    summary = summarize(df)
    summary.to_csv(summary_path, index=False)
    print(f"[judge] resultados actualizados en {run_dir}/")
    _print_summary(summary)
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Parser de CLI del juez en dos fases."""
    parser = argparse.ArgumentParser(
        description=(
            "Aplica el LLM-as-judge sobre un results.csv ya generado y "
            "recomputa el summary.csv."
        )
    )
    parser.add_argument("--config", type=str, required=True,
                        help="Ruta al JSON de configuración del experimento.")
    parser.add_argument("--run_dir", type=str, required=True,
                        help="Directorio con results.csv (p. ej. outputs/<exp_id>).")
    parser.add_argument("--resume", action="store_true", default=False,
                        help="Saltear filas ya puntuadas (judge_promedio no nulo).")
    parser.add_argument("--max_retries", type=int, default=5,
                        help="Reintentos por fila ante errores transitorios.")
    parser.add_argument("--base_delay", type=float, default=2.0,
                        help="Delay base (s) del backoff exponencial.")
    add_judge_args(parser)
    return parser


def main(argv=None) -> None:
    """Punto de entrada CLI: `python -m cn_pipeline.judge_results ...`."""
    args = build_parser().parse_args(argv)
    cfg = load_config(args.config)
    apply_judge_overrides(cfg.llm_judge, args)
    judge_results_dir(
        cfg,
        args.run_dir,
        resume=args.resume,
        max_retries=args.max_retries,
        base_delay=args.base_delay,
    )


if __name__ == "__main__":
    main()
