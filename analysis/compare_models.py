"""Comparación por modelo entre los resúmenes de corridas.

Extiende el análisis de `compare_experiments.py` al caso de varios modelos
corriendo el mismo protocolo (mismos experimentos y técnicas). Lee los
directorios de resultados bajo `outputs/` y produce un resumen Markdown con
cuatro vistas independientes:

    1. Resumen compacto: por métrica, filas = experimento, columnas = modelos;
       celda = mejor técnica con su valor; ★ = mejor modelo del experimento.
    2. Detalle técnica × modelo: para cada experimento y métrica, la matriz
       completa (★ mejor modelo de fila, ▲ mejor técnica de columna).
    3. Test de signos entre modelos: pares de modelos comparados emparejados
       por tweet (cada experimento comparte los mismos 27 tweets).
    4. Ranking global: experimentos ganados, media de mejores y media global.

Uso:

    python analysis/compare_models.py                     # resumen a stdout
    python analysis/compare_models.py --save summary.md   # además, guardarlo
    python analysis/compare_models.py --strict            # falla (exit 2) si falta el juez
"""

from __future__ import annotations

import argparse
import itertools
import sys

import pandas as pd

from compare_experiments import (
    GENERIC_ORDER,
    SUMMARY_AUTO_METRICS,
    SUMMARY_JUDGE_METRICS,
    TYPED_ORDER,
    _best,
    _cross_table,
    _md_table,
    _order_labels,
    judge_warnings,
    load_runs,
    model_label,
    run_config_label,
    run_fewshot_examples,
    run_is_typed,
    sign_test_pvalue,
)

ALL_METRICS = SUMMARY_JUDGE_METRICS + SUMMARY_AUTO_METRICS
CONFIGS_ORDER = GENERIC_ORDER + TYPED_ORDER

# Etiqueta de reporte para cada métrica (la columna de los CSV no cambia).
METRIC_LABELS = {
    "judge_promedio": "Puntaje de calidad (juez 1)",
    "judge2_gen_rate": "Tasa de preferencia (juez 2)",
}


def metric_label(metric: str) -> str:
    """Nombre de la métrica tal como se reporta (los CSV conservan su columna)."""
    return METRIC_LABELS.get(metric, metric)


def load_by_config(runs) -> dict:
    """Agrupa las corridas: {config: {modelo: (exp_dir, summary, results)}}."""
    by_config = {}
    for exp_dir, summary, results in runs:
        cfg = run_config_label(exp_dir)
        model = model_label(exp_dir)
        by_config.setdefault(cfg, {})[model] = (exp_dir, summary, results)
    return by_config


def coverage_warnings(by_config: dict) -> list:
    """Advierte configs que algún modelo no tiene (comparación incompleta)."""
    models = {m for models in by_config.values() for m in models}
    warnings = []
    for cfg in _order_labels(sorted(by_config), CONFIGS_ORDER):
        missing = models - set(by_config[cfg])
        if missing:
            warnings.append(f"- {cfg}: sin corridas de {', '.join(sorted(missing))}")
    return warnings


def _indexed(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.set_index("prompt_type")


def _compact_table(by_config: dict, models: list, metric: str) -> pd.DataFrame:
    """Tabla compacta: filas = experimento, columnas = modelos.

    Celda = mejor técnica de esa corrida para la métrica, `valor (técnica)`;
    ★ = mejor modelo del experimento (empates marcados en todos).
    """
    cfgs = _order_labels(sorted(by_config), CONFIGS_ORDER)
    raw = pd.DataFrame(index=cfgs, columns=models, dtype=float)
    techs = pd.DataFrame(index=cfgs, columns=models, dtype=object)
    for cfg in cfgs:
        for m in models:
            run = by_config[cfg].get(m)
            if run is None:
                continue
            technique, val = _best(_indexed(run[1]), metric)
            if technique is not None:
                raw.at[cfg, m] = val
                techs.at[cfg, m] = technique
    disp = pd.DataFrame(index=cfgs, columns=models, dtype=object)
    row_best = raw.max(axis=1)
    for cfg in cfgs:
        for m in models:
            val = raw.at[cfg, m]
            if pd.isna(val):
                disp.at[cfg, m] = ""
                continue
            mark = "★" if val == row_best[cfg] else ""
            disp.at[cfg, m] = f"{val:.4f} ({techs.at[cfg, m]}){mark}"
    return disp


def _detail_tables(by_config: dict, models: list, cfg: str, metric: str):
    """Matriz técnica × modelo para un experimento y métrica (vía `_cross_table`)."""
    data = []
    for m in models:
        run = by_config[cfg].get(m)
        if run is None:
            continue
        exp_dir, summary, results = run
        data.append(
            {
                "label": m,
                "group": "tipeada" if run_is_typed(exp_dir) else "generica",
                "indexed": _indexed(summary),
                "results": results,
            }
        )
    if not data:
        return None
    group = data[0]["group"]
    return _cross_table(data, group, metric, CONFIGS_ORDER)


def _pairwise_sign_rows(by_config: dict, models: list, metrics: list) -> list:
    """Comparación emparejada por tweet entre pares de modelos.

    Para cada par de modelos, experimento y técnica, junta los resultados por
    `hate_speech` y aplica el test de signos a la diferencia de métricas.
    """
    rows = []
    for m1, m2 in itertools.combinations(models, 2):
        for cfg in sorted(by_config):
            run1, run2 = by_config[cfg].get(m1), by_config[cfg].get(m2)
            if run1 is None or run2 is None:
                continue
            r1, r2 = run1[2], run2[2]
            if r1 is None or r2 is None:
                continue
            for technique in sorted(set(r1["prompt_type"]) & set(r2["prompt_type"])):
                for metric in metrics:
                    if metric not in r1.columns or metric not in r2.columns:
                        continue
                    a = r1[r1["prompt_type"] == technique].set_index("hate_speech")[metric]
                    b = r2[r2["prompt_type"] == technique].set_index("hate_speech")[metric]
                    joined = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
                    diffs = joined["a"] - joined["b"]
                    wins = int((diffs > 0).sum())
                    losses = int((diffs < 0).sum())
                    rows.append(
                        {
                            "par": (m1, m2),
                            "config": cfg,
                            "tecnica": technique,
                            "metrica": metric,
                            "mean_diff": float(diffs.mean()) if len(diffs) else float("nan"),
                            "wins": wins,
                            "losses": losses,
                            "p": sign_test_pvalue(wins, losses),
                        }
                    )
    return rows


def _ranking_table(by_config: dict, models: list, metric: str) -> pd.DataFrame:
    """Ranking por modelo: experimentos ganados, media de mejores y media global.

    - Experimentos ganados: configs donde el modelo logra el mejor valor con su
      mejor técnica (empates cuentan para todos los empatados).
    - Media de mejores: promedio de los valores de la mejor técnica por config.
    - Media global: promedio de todas las técnicas en todos los experimentos.
    """
    cfgs = _order_labels(sorted(by_config), CONFIGS_ORDER)
    columns = {"Experimentos ganados": [], "Media de mejores": [], "Media global": []}
    for m in models:
        best_vals = []
        wins = 0
        global_vals = []
        for cfg in cfgs:
            run = by_config[cfg].get(m)
            if run is None:
                continue
            indexed = _indexed(run[1])
            technique, val = _best(indexed, metric)
            if technique is not None:
                best_vals.append(val)
                global_vals.extend(indexed[metric].dropna().tolist())
        raw = pd.Series(index=cfgs, dtype=float)
        for cfg in cfgs:
            run = by_config[cfg].get(m)
            if run is not None:
                technique, val = _best(_indexed(run[1]), metric)
                if technique is not None:
                    raw.at[cfg] = val
        for cfg in cfgs:
            row = pd.Series(
                {
                    m2: (
                        _best(_indexed(by_config[cfg][m2][1]), metric)[1]
                        if m2 in by_config[cfg]
                        else float("nan")
                    )
                    for m2 in models
                }
            )
            cell = raw.at[cfg]
            if not pd.isna(cell) and cell == row.max():
                wins += 1
        columns["Experimentos ganados"].append(f"{wins}/{len(cfgs)}")
        columns["Media de mejores"].append(
            f"{pd.Series(best_vals).mean():.4f}" if best_vals else ""
        )
        columns["Media global"].append(
            f"{pd.Series(global_vals).mean():.4f}" if global_vals else ""
        )
    return pd.DataFrame(columns, index=models)


def _fewshot_note(runs) -> str:
    """Nota sobre el n de `few_shot` (mismo formato que `compare_experiments`)."""
    n_values = {run_fewshot_examples(exp_dir) for exp_dir, _, _ in runs} - {None}
    if len(n_values) == 1:
        n = next(iter(n_values))
        return f"- `few_shot`: n = {n} ejemplos (campo `fewshot_examples` de `config.json`).\n"
    if len(n_values) > 1:
        return (
            "- `few_shot`: n ∈ {"
            + ", ".join(str(v) for v in sorted(n_values))
            + "} ejemplos (varía por corrida; campo `fewshot_examples` de `config.json`).\n"
        )
    return "- `few_shot`: nº de ejemplos no disponible (falta `fewshot_examples` en los `config.json`).\n"


def build_model_summary(runs, warnings: list | None = None) -> str:
    """Reporte de comparación por modelo en cuatro secciones."""
    models = sorted({model_label(exp_dir) for exp_dir, _, _ in runs})
    by_config = load_by_config(runs)
    lines = [f"# Comparación por modelo ({', '.join(models)})\n"]
    lines.append(
        "Mismos experimentos y técnicas para todos los modelos. `★` = mejor "
        "modelo del experimento (sección 1) o de la fila (sección 2); `▲` = "
        "mejor técnica de columna. Experimentos ordenados: genéricas primero "
        f"({', '.join(GENERIC_ORDER)}), luego tipeadas ({', '.join(TYPED_ORDER)}).\n"
    )
    lines.append(_fewshot_note(runs))
    if warnings:
        lines.append("## Advertencias\n")
        lines.append("\n".join(warnings))
        lines.append("")

    # 1. Resumen compacto
    for parte, metrics, name in [
        ("1.1", SUMMARY_JUDGE_METRICS, "Jueces"),
        ("1.2", SUMMARY_AUTO_METRICS, "Métricas automáticas"),
    ]:
        lines.append(f"## 1. Resumen compacto — {parte} {name}\n")
        lines.append("Filas = experimento; celda = mejor técnica con su valor.\n")
        for metric in metrics:
            lines.append(f"#### {metric_label(metric)}\n")
            lines.append(_md_table(_compact_table(by_config, models, metric), "experimento"))
            lines.append("")

    # 2. Detalle técnica × modelo
    lines.append("## 2. Detalle técnica × modelo\n")
    for cfg in _order_labels(sorted(by_config), CONFIGS_ORDER):
        lines.append(f"### {cfg}\n")
        for metric in ALL_METRICS:
            table = _detail_tables(by_config, models, cfg, metric)
            if table is None:
                continue
            lines.append(f"#### {metric_label(metric)}\n")
            lines.append(_md_table(table, "técnica"))
            lines.append("")

    # 3. Test de signos entre modelos
    lines.append("## 3. Test de signos entre modelos\n")
    lines.append(
        "Comparación emparejada por tweet (cada experimento comparte los mismos "
        "27 tweets). Solo se listan las diferencias significativas (p < 0.05, "
        "test de signos bilateral); Δ media = A − B.\n"
    )
    sign_rows = _pairwise_sign_rows(by_config, models, ALL_METRICS)
    for (m1, m2) in itertools.combinations(models, 2):
        pair_rows = [r for r in sign_rows if r["par"] == (m1, m2)]
        if not pair_rows:
            continue
        lines.append(f"### {m1} vs {m2}\n")
        for metric in ALL_METRICS:
            subset = [r for r in pair_rows if r["metrica"] == metric]
            if not subset:
                continue
            sig = [r for r in subset if r["p"] < 0.05]
            lines.append(f"#### {metric_label(metric)}\n")
            lines.append(
                f"{len(sig)} de {len(subset)} comparaciones significativas (p < 0.05).\n"
            )
            if sig:
                lines.append("| Experimento | Técnica | Δ media | gana " + m1 + " | gana " + m2 + " | p |")
                lines.append("| --- | --- | --- | --- | --- | --- |")
                for r in sig:
                    lines.append(
                        f"| {r['config']} | {r['tecnica']} | {r['mean_diff']:+.4f} "
                        f"| {r['wins']} | {r['losses']} | {r['p']:.4f} |"
                    )
                lines.append("")

    # 4. Ranking global
    lines.append("## 4. Ranking global\n")
    lines.append(
        "`Experimentos ganados` = configs donde el modelo logra el mejor valor "
        "con su mejor técnica (de la sección 1). `Media de mejores` = promedio "
        "de esos valores. `Media global` = promedio de todas las técnicas en "
        "todos los experimentos.\n"
    )
    for parte, metrics, name in [
        ("4.1", SUMMARY_JUDGE_METRICS, "Jueces"),
        ("4.2", SUMMARY_AUTO_METRICS, "Métricas automáticas"),
    ]:
        lines.append(f"### {parte} {name}\n")
        for metric in metrics:
            lines.append(f"#### {metric_label(metric)}\n")
            lines.append(_md_table(_ranking_table(by_config, models, metric), "modelo"))
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Comparación por modelo de los resúmenes bajo outputs/."
    )
    parser.add_argument(
        "--outputs", type=str, default="outputs", help="Directorio de resultados."
    )
    parser.add_argument(
        "--save", type=str, default=None, help="Ruta para guardar el resumen Markdown."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Falla (exit 2) si alguna corrida no está juzgada; por defecto solo "
            "advierte."
        ),
    )
    args = parser.parse_args()

    runs = load_runs(args.outputs)
    if not runs:
        raise SystemExit(f"No se encontraron corridas (summary.csv) bajo {args.outputs}/")

    warnings = judge_warnings(runs) + coverage_warnings(load_by_config(runs))
    if warnings:
        print("ADVERTENCIA:\n" + "\n".join(warnings), file=sys.stderr)
        if args.strict:
            raise SystemExit(2)

    text = build_model_summary(runs, warnings)
    print(text)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"resumen guardado en {args.save}")


if __name__ == "__main__":
    main()
