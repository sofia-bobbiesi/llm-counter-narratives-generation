"""Curvas de few-shot (H1): desempeño vs número de ejemplos en contexto.

Corre, por modelo, la técnica `few_shot` con n ∈ {1, 3, 5, 10} ejemplos
(muestreo **anidado**), sobre la config del modelo, **sin juez** (solo métricas
automáticas). Cada punto se guarda en `outputs_curves/<modelo>/<run_id>_fs<N>/`
y, al terminar, se escribe una tabla `curve_summary.csv` por modelo.

Es una fase 1 (generación + métricas). El juez se puede correr después con
`cn_pipeline.judge_results` o `validate_judge.py`, por cada run dir.

Uso:
    python run_curves.py --models gemma
    python run_curves.py --models gemma --values 1,3,5,10 --force
    python run_curves.py --models gemma --dry_run          # enumera sin correr
"""

from __future__ import annotations

import argparse
import copy
import os
import traceback

import pandas as pd

from cn_pipeline.config import load_config, resolve_device
from cn_pipeline.pipeline import (
    build_generator,
    experiment_id,
    finalize_experiment,
    generate_rows,
    prepare_experiment,
)

DEFAULT_MODELS = ("gemma", "llama", "mistral")
DEFAULT_VALUES = "1,3,5,10"


def run_dir_for(cfg, n):
    """Directorio de salida para el punto `n` de la curva."""
    return os.path.join(cfg.output_dir, experiment_id(cfg, suffix=f"_fs{n}"))


def curve_table(entries) -> pd.DataFrame:
    """Tabla de la curva: una fila por n con las métricas de `few_shot`."""
    rows = []
    for n, run_dir in entries:
        summary_path = os.path.join(run_dir, "summary.csv")
        results_path = os.path.join(run_dir, "results.csv")
        if not os.path.isfile(summary_path):
            continue
        summary = pd.read_csv(summary_path)
        few = summary[summary["prompt_type"] == "few_shot"]
        if not len(few):
            continue
        metrics = {k: v for k, v in few.iloc[0].to_dict().items() if k != "prompt_type"}
        n_tweets = len(pd.read_csv(results_path)) if os.path.isfile(results_path) else None
        rows.append({"n": n, "run_id": os.path.basename(run_dir),
                     "n_tweets": n_tweets, **metrics})
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows).sort_values("n")
    first = ["n", "run_id", "n_tweets"]
    return df[first + [c for c in df.columns if c not in first]]


def run_model(model_key: str, values, args) -> dict:
    """Corre la curva de un modelo. Devuelve conteos ok/skip/fail."""
    base = load_config(f"configs/config_{model_key}.json")
    base.prompt_types = ["few_shot"]           # la curva es solo de few-shot
    base.seed = args.seed
    base.output_dir = os.path.join(args.outputs, base.model_name.split("/")[-1])
    if args.max_samples is not None:
        base.max_samples = args.max_samples
    device = resolve_device(base.device)

    generator = None
    entries = []
    counts = {"ok": 0, "skip": 0, "fail": 0}

    for n in values:
        cfg = copy.deepcopy(base)
        cfg.fewshot_examples = n
        out_dir = run_dir_for(cfg, n)
        entries.append((n, out_dir))
        tag = f"{model_key} n={n}"
        if args.dry_run:
            print(f"[curves] dry-run {tag} -> {out_dir}")
            continue
        if not args.force and os.path.isfile(os.path.join(out_dir, "summary.csv")):
            print(f"[curves] skip {tag} (ya existe)")
            counts["skip"] += 1
            continue
        if generator is None:
            print(f"[curves] cargando modelo {base.model_name} ...")
            generator = build_generator(base, device)
        print(f"[curves] run  {tag} -> {out_dir}")
        try:
            _, test, examples, counter_example = prepare_experiment(
                cfg, device, nested_examples=True)
            rows = generate_rows(cfg, test, examples, counter_example, generator)
            finalize_experiment(cfg, rows, dir_suffix=f"_fs{n}")
            counts["ok"] += 1
        except Exception:
            print(f"[curves] FALLO {tag}")
            traceback.print_exc()
            counts["fail"] += 1

    if not args.dry_run:
        table = curve_table(entries)
        if len(table):
            out_csv = os.path.join(base.output_dir, "curve_summary.csv")
            table.to_csv(out_csv, index=False)
            print(f"[curves] tabla de la curva en {out_csv}")
            print(table.to_string(index=False))
    return counts


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Curvas de few-shot (nº de ejemplos) por modelo, sin juez."
    )
    parser.add_argument("--models", type=str, default="gemma",
                        help="Modelos separados por coma (gemma,llama,mistral).")
    parser.add_argument("--values", type=str, default=DEFAULT_VALUES,
                        help="Valores de few-shot a recorrer.")
    parser.add_argument("--outputs", type=str, default="outputs_curves")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_samples", type=int, default=None,
                        help="Acota tweets de test (smoke test).")
    parser.add_argument("--force", action="store_true",
                        help="Re-corre aunque exista summary.csv.")
    parser.add_argument("--dry_run", action="store_true",
                        help="Enumera los puntos sin llamar al modelo.")
    args = parser.parse_args(argv)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    values = [int(v) for v in args.values.split(",") if v.strip()]
    total = {"ok": 0, "skip": 0, "fail": 0}
    for model_key in models:
        print(f"\n[curves] === modelo {model_key} (n={values}) ===")
        counts = run_model(model_key, values, args)
        for k in total:
            total[k] += counts[k]
    if not args.dry_run:
        print(f"\n[curves] fin: ok={total['ok']} skip={total['skip']} fail={total['fail']}")


if __name__ == "__main__":
    main()
