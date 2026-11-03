"""Resumen de experimentos del protocolo (materia prima del análisis).

Lee los directorios de resultados bajo `outputs/` (uno por corrida, cada uno con
`summary.csv`, `results.csv` y `config.json`) y produce un resumen compacto en
Markdown con dos partes independientes:

    1. Jueces: puntaje de calidad (juez 1) y tasa de preferencia (juez 2), por
       separado (no se combinan con las métricas automáticas ni entre sí).
    2. Métricas automáticas: ROUGE-1, ROUGE-2, ROUGE-L y BERT-F1 (BLEU se
       excluye; ver nota en `build_summary`).

En ambos casos se cruza técnica (tipo de prompt) × experimento, se indica la
mejor técnica por experimento y el mejor experimento por técnica, y se evalúa
el efecto de inyectar la información del tipo de contra-narrativa (pares que
comparten tweets, con test de signos).

Uso:

    python analysis/compare_experiments.py                     # resumen a stdout
    python analysis/compare_experiments.py --save summary.md   # además, guardarlo
    python analysis/compare_experiments.py --outputs outputs   # otro directorio de resultados
    python analysis/compare_experiments.py --strict            # falla (exit 2) si falta el juez
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import pandas as pd

# Parte I = jueces (por separado); Parte II = automáticas. BLEU se excluye.
SUMMARY_JUDGE_METRICS = ["judge_promedio", "judge2_gen_rate"]
SUMMARY_AUTO_METRICS = ["ROUGE-1", "ROUGE-2", "ROUGE-L", "BERT-F1"]
GENERIC_ORDER = ["all", "collective", "premises", "no-info"]
TYPED_ORDER = ["a", "a_no_info", "b", "b_no_info", "c", "c_no_info"]
INFO_PAIRS = [("a", "a_no_info"), ("b", "b_no_info"), ("c", "c_no_info")]

# Etiqueta de reporte para cada métrica (la columna de los CSV no cambia).
METRIC_LABELS = {
    "judge_promedio": "Puntaje de calidad (juez 1)",
    "judge2_gen_rate": "Tasa de preferencia (juez 2)",
}


def metric_label(metric: str) -> str:
    """Nombre de la métrica tal como se reporta (los CSV conservan su columna)."""
    return METRIC_LABELS.get(metric, metric)


def model_label(exp_dir: Path) -> str:
    """Etiqueta del modelo para una corrida (desde su config.json guardado)."""
    config_path = exp_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                model_name = json.load(f).get("model_name", "")
            if model_name:
                return model_name.split("/")[-1]
        except (json.JSONDecodeError, OSError):
            pass
    return exp_dir.name


def run_config_label(exp_dir: Path) -> str:
    """Etiqueta corta de una corrida según su config.json (info/tipo de CN).

    Devuelve el tipo de estrategia (`cn_strategy`) si la corrida es tipeada, o
    el eje de información (`use_extra_info`) si es genérica; p. ej. `all`,
    `collective`, `premises`, `no-info`, `a`, `b`, `c`, `a_no_info`...
    """
    config_path = exp_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                config = json.load(f)
            return config.get("cn_strategy") or config.get("use_extra_info") or "no-info"
        except (json.JSONDecodeError, OSError):
            pass
    return exp_dir.name


def run_labels(runs) -> list:
    """Etiqueta corta por corrida; desambigua si un modelo tiene varias corridas.

    Si las etiquetas cortas (config) se repiten, se prefija el modelo
    (`modelo/config`); si aun así hay colisiones, se usa el nombre del
    directorio para no mezclar resultados.
    """
    config_labels = [run_config_label(d) for d, _, _ in runs]
    if len(set(config_labels)) == len(config_labels):
        return config_labels
    composite = [f"{model_label(d)}/{c}" for (d, _, _), c in zip(runs, config_labels)]
    if len(set(composite)) == len(composite):
        return composite
    return [d.name for d, _, _ in runs]


def run_is_typed(exp_dir: Path) -> bool:
    """True si la corrida es tipeada (`cn_strategy` presente); False si genérica."""
    config_path = exp_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                return bool(json.load(f).get("cn_strategy"))
        except (json.JSONDecodeError, OSError):
            pass
    return False


def run_fewshot_examples(exp_dir: Path):
    """Nº de ejemplos del prompt `few_shot` (`fewshot_examples` del config.json)."""
    config_path = exp_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, encoding="utf-8") as f:
                return json.load(f).get("fewshot_examples")
        except (json.JSONDecodeError, OSError):
            pass
    return None


def load_runs(outputs_dir: str):
    """Devuelve la lista de corridas encontradas: [(directorio, summary, results)].

    El glob es recursivo (`**/summary.csv`) porque las corridas viven anidadas
    bajo la carpeta de su modelo (`outputs/<modelo>/<run_id>/`); también
    encuentra corridas al ras, si las hubiera.
    """
    runs = []
    for summary_path in sorted(Path(outputs_dir).glob("**/summary.csv")):
        exp_dir = summary_path.parent
        results_path = exp_dir / "results.csv"
        summary = pd.read_csv(summary_path)
        results = pd.read_csv(results_path) if results_path.exists() else None
        runs.append((exp_dir, summary, results))
    return runs


def judge_warnings(runs) -> list:
    """Advierte sobre corridas sin juzgar o con filas del juez faltantes.

    El LLM-as-judge es obligatorio: un `results.csv` sin columnas `judge_*`
    proviene de una corrida con `--skip_judge` cuya fase 2 (`cn_pipeline.judge_results`)
    quedó pendiente, y no debe analizarse como si estuviera completa.
    """
    warnings = []
    for exp_dir, summary, results in runs:
        df = results if results is not None and not results.empty else summary
        judge_cols = [c for c in df.columns if c.startswith("judge_")]
        if not judge_cols:
            warnings.append(
                f"- {exp_dir.name}: SIN juez (faltan columnas `judge_*`). "
                f"Completar con `python -m cn_pipeline.judge_results --config <cfg> "
                f"--run_dir {exp_dir}`."
            )
            continue
        if "judge_promedio" in df.columns:
            missing = int(df["judge_promedio"].isna().sum())
            if missing:
                warnings.append(
                    f"- {exp_dir.name}: {missing}/{len(df)} filas sin `judge_promedio` "
                    "(fallos del juez o fase 2 incompleta); reintentar con `--resume`."
                )
    return warnings


def sign_test_pvalue(wins: int, losses: int) -> float:
    """P-valor bilateral exacto del test de signos (descarta empates)."""
    n = wins + losses
    if n == 0:
        return float("nan")
    tail = sum(math.comb(n, k) for k in range(0, min(wins, losses) + 1))
    return min(1.0, 2 * tail / (2**n))


def _order_labels(labels: list, preferred: list) -> list:
    rank = {label: i for i, label in enumerate(preferred)}
    return sorted(labels, key=lambda label: (rank.get(label, len(rank)), label))


def _summary_data(runs, fewshot_label: str = "few_shot") -> list:
    """Prepara corridas para el resumen: {label, group, indexed, results}.

    Si `fewshot_label` cambia (p. ej. "few_shot (n=3)"), se renombra la técnica
    `few_shot` en el índice y en `results` para que la anotación se propague a
    todas las tablas del resumen.
    """
    labels = run_labels(runs)
    data = []
    for (exp_dir, summary, results), label in zip(runs, labels):
        indexed = summary.set_index("prompt_type")
        if fewshot_label != "few_shot":
            indexed = indexed.rename(index={"few_shot": fewshot_label})
            if results is not None and "prompt_type" in results.columns:
                results = results.copy()
                results["prompt_type"] = results["prompt_type"].replace(
                    "few_shot", fewshot_label
                )
        data.append(
            {
                "label": label,
                "group": "tipeada" if run_is_typed(exp_dir) else "generica",
                "indexed": indexed,
                "results": results,
            }
        )
    return data


def _md_table(df: pd.DataFrame, index_name: str = "") -> str:
    """Renderiza un DataFrame de celdas ya formateadas como tabla Markdown."""
    if index_name:
        df = df.rename_axis(index_name)
    cols = list(df.columns)
    lines = [
        "| " + " | ".join([index_name] + [str(c) for c in cols]) + " |",
        "|" + "|".join([" --- "] * (len(cols) + 1)) + "|",
    ]
    for idx, row in df.iterrows():
        lines.append("| " + " | ".join([str(idx)] + [str(v) for v in row]) + " |")
    return "\n".join(lines)


def _cross_table(data, group: str, metric: str, labels_order: list) -> pd.DataFrame:
    """Matriz técnica × experimento; `★` mejor de columna, `▲` mejor de fila."""
    group_data = [d for d in data if d["group"] == group]
    labels = _order_labels([d["label"] for d in group_data], labels_order)
    by_label = {d["label"]: d["indexed"] for d in group_data}
    techniques = sorted({t for d in group_data for t in d["indexed"].index})

    values = pd.DataFrame(index=techniques, columns=labels, dtype=float)
    for label in labels:
        indexed = by_label[label]
        for technique in techniques:
            if technique in indexed.index and metric in indexed.columns:
                values.at[technique, label] = indexed.at[technique, metric]

    col_best = values.max(axis=0)
    row_best = values.max(axis=1)
    disp = pd.DataFrame(index=techniques, columns=labels, dtype=object)
    for technique in techniques:
        for label in labels:
            value = values.at[technique, label]
            if pd.isna(value):
                disp.at[technique, label] = ""
                continue
            mark = ("★" if value == col_best[label] else "") + (
                "▲" if value == row_best[technique] else ""
            )
            disp.at[technique, label] = f"{value:.4f}{mark}"
    return disp


def _best(indexed: pd.DataFrame, metric: str):
    """Técnica con mayor valor de `metric` en una corrida (y su valor)."""
    if metric not in indexed.columns:
        return None, float("nan")
    series = indexed[metric].dropna()
    if series.empty:
        return None, float("nan")
    return series.idxmax(), float(series.max())


def _best_experiment_table(data, group: str, metrics: list, labels_order: list) -> pd.DataFrame:
    """Por técnica (filas), el mejor experimento de cada métrica como `label (valor)`."""
    group_data = [d for d in data if d["group"] == group]
    labels = _order_labels([d["label"] for d in group_data], labels_order)
    by_label = {d["label"]: d["indexed"] for d in group_data}
    techniques = sorted({t for d in group_data for t in d["indexed"].index})

    columns = {}
    for metric in metrics:
        cells = {}
        for technique in techniques:
            candidates = []
            for label in labels:
                indexed = by_label[label]
                if technique in indexed.index and metric in indexed.columns:
                    value = indexed.at[technique, metric]
                    if not pd.isna(value):
                        candidates.append((label, value))
            if candidates:
                label, value = max(candidates, key=lambda item: item[1])
                cells[technique] = f"{label} ({value:.4f})"
        columns[metric] = pd.Series(cells)
    return pd.DataFrame(columns).reindex(techniques).rename(columns=metric_label)


def _global_best(data, group: str, metrics: list, labels_order: list) -> pd.Series:
    """Mejor celda (experimento / técnica) de cada métrica dentro de un grupo."""
    group_data = [d for d in data if d["group"] == group]
    labels = _order_labels([d["label"] for d in group_data], labels_order)
    by_label = {d["label"]: d["indexed"] for d in group_data}

    cells = {}
    for metric in metrics:
        best = None
        for label in labels:
            indexed = by_label[label]
            if metric in indexed.columns:
                series = indexed[metric].dropna()
                if not series.empty:
                    candidate = (label, series.idxmax(), float(series.max()))
                    if best is None or candidate[2] > best[2]:
                        best = candidate
        cells[metric] = f"{best[0]} / {best[1]} ({best[2]:.4f})" if best else ""
    return pd.Series(cells)


def _info_effect(data, metrics: list) -> list:
    """Efecto de inyectar la información: pares con-with/without sobre los mismos tweets.

    Cada par (p. ej. `a` vs `a_no_info`) comparte el set de tweets, así que la
    comparación es emparejada tweet a tweet; se aplica el test de signos.
    """
    by_label = {d["label"]: d for d in data}
    rows = []
    for with_label, without_label in INFO_PAIRS:
        if with_label not in by_label or without_label not in by_label:
            continue
        with_results = by_label[with_label]["results"]
        without_results = by_label[without_label]["results"]
        if with_results is None or without_results is None:
            continue
        techniques = sorted(
            set(with_results["prompt_type"]) & set(without_results["prompt_type"])
        )
        for technique in techniques:
            for metric in metrics:
                if metric not in with_results.columns or metric not in without_results.columns:
                    continue
                con = with_results[with_results["prompt_type"] == technique].set_index(
                    "hate_speech"
                )[metric]
                sin = without_results[without_results["prompt_type"] == technique].set_index(
                    "hate_speech"
                )[metric]
                joined = pd.concat([con.rename("con"), sin.rename("sin")], axis=1).dropna()
                diffs = joined["con"] - joined["sin"]
                wins = int((diffs > 0).sum())
                losses = int((diffs < 0).sum())
                rows.append(
                    {
                        "par": f"{with_label} vs {without_label}",
                        "tecnica": technique,
                        "metrica": metric,
                        "mean_diff": float(diffs.mean()) if len(diffs) else float("nan"),
                        "con": wins,
                        "sin": losses,
                        "p": sign_test_pvalue(wins, losses),
                    }
                )
    return rows


def _format_info_effect(rows: list, metrics: list) -> str:
    lines = []
    for metric in metrics:
        subset = [r for r in rows if r["metrica"] == metric]
        if not subset:
            continue
        lines.append(f"#### {metric_label(metric)}\n")
        lines.append(
            "| Par | Técnica | Δ media (con − sin) | gana con info | gana sin info | p (signos) |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for row in subset:
            lines.append(
                f"| {row['par']} | {row['tecnica']} | {row['mean_diff']:+.4f} "
                f"| {row['con']} | {row['sin']} | {row['p']:.4f} |"
            )
        lines.append("")
    return "\n".join(lines)


def build_summary(runs, warnings: list | None = None) -> str:
    """Resumen compacto: Parte I (jueces) y Parte II (automáticas), por separado."""
    n_values = {run_fewshot_examples(exp_dir) for exp_dir, _, _ in runs} - {None}
    if len(n_values) == 1:
        n = next(iter(n_values))
        fewshot_label = f"few_shot (n={n})"
        note = (
            f"- `few_shot`: n = {n} ejemplos "
            "(campo `fewshot_examples` de `config.json`).\n"
        )
    elif len(n_values) > 1:
        fewshot_label = "few_shot"
        note = (
            "- `few_shot`: n ∈ {"
            + ", ".join(str(v) for v in sorted(n_values))
            + "} ejemplos (varía por corrida; campo `fewshot_examples` de `config.json`).\n"
        )
    else:
        fewshot_label = "few_shot"
        note = (
            "- `few_shot`: nº de ejemplos no disponible "
            "(falta `fewshot_examples` en los `config.json`).\n"
        )

    data = _summary_data(runs, fewshot_label)
    models = {model_label(exp_dir) for exp_dir, _, _ in runs}
    title = models.pop() if len(models) == 1 else "múltiples modelos"

    lines = [f"# Resumen ({title})\n"]
    lines.append(
        "Éxito evaluado **por métrica, sin combinar**. `★` = mejor de la columna, "
        "`▲` = mejor de la fila. Agrupación: genéricas (mismos 27 tweets) y "
        "tipeadas (a/b/c comparten tweets solo dentro de su par).\n"
    )
    lines.append(note)
    if warnings:
        lines.append("## Advertencias de juez (LLM-as-judge)\n")
        lines.append("\n".join(warnings))
        lines.append("")

    lines.append("## PARTE I — Jueces\n")
    lines.append(
        "El puntaje de calidad (juez 1) y la tasa de preferencia (juez 2) se analizan "
        "por separado; ⚠ marca cuando el ganador difiere entre ambos.\n"
    )

    lines.append("### 1.1 Cruce genéricas (técnica × experimento)\n")
    for metric in SUMMARY_JUDGE_METRICS:
        lines.append(f"#### {metric_label(metric)}\n")
        lines.append(_md_table(_cross_table(data, "generica", metric, GENERIC_ORDER), "técnica"))
        lines.append("")

    lines.append("### 1.2 Cruce tipeadas (técnica × experimento)\n")
    for metric in SUMMARY_JUDGE_METRICS:
        lines.append(f"#### {metric_label(metric)}\n")
        lines.append(_md_table(_cross_table(data, "tipeada", metric, TYPED_ORDER), "técnica"))
        lines.append("")

    lines.append("### 1.3 Mejor técnica por experimento\n")
    lines.append(
        "| Experimento | Mejor (juez 1) | Puntaje de calidad (juez 1) | Mejor (juez 2) "
        "| Tasa de preferencia (juez 2) | ¿coinciden? |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- |")
    by_label = {d["label"]: d for d in data}
    for label in _order_labels(list(by_label), GENERIC_ORDER + TYPED_ORDER):
        indexed = by_label[label]["indexed"]
        tech1, val1 = _best(indexed, "judge_promedio")
        tech2, val2 = _best(indexed, "judge2_gen_rate")
        same = "★" if tech1 == tech2 else "⚠ no"
        lines.append(
            f"| {label} | {tech1} | {val1:.4f} | {tech2} | {val2:.4f} | {same} |"
        )
    lines.append("")

    for i, (group, order, name) in enumerate(
        [
            ("generica", GENERIC_ORDER, "genéricas"),
            ("tipeada", TYPED_ORDER, "tipeadas"),
        ]
    ):
        base = 4 + 2 * i
        lines.append(f"### 1.{base} Mejor experimento por técnica — {name}\n")
        lines.append(
            _md_table(
                _best_experiment_table(data, group, SUMMARY_JUDGE_METRICS, order), "técnica"
            )
        )
        lines.append("")
        lines.append(f"### 1.{base + 1} Mejor global — {name}\n")
        global_best = _global_best(data, group, SUMMARY_JUDGE_METRICS, order)
        lines.append("| Métrica | Mejor (experimento / técnica) |")
        lines.append("| --- | --- |")
        for metric, value in global_best.items():
            lines.append(f"| {metric_label(metric)} | {value} |")
        lines.append("")

    lines.append("### 1.8 Efecto de la información (pares con tweets compartidos)\n")
    lines.append(
        "Cada par difiere solo en si se inyecta la información del tipo "
        "(`a`→con info, `a_no_info`→sin info). Positivo = conviene inyectarla.\n"
    )
    lines.append(_format_info_effect(_info_effect(data, SUMMARY_JUDGE_METRICS), SUMMARY_JUDGE_METRICS))

    lines.append("## PARTE II — Métricas automáticas\n")
    lines.append("Métricas: ROUGE-1, ROUGE-2, ROUGE-L, BERT-F1 (por separado).\n")

    lines.append("### 2.1 Cruce genéricas (técnica × experimento)\n")
    for metric in SUMMARY_AUTO_METRICS:
        lines.append(f"#### {metric_label(metric)}\n")
        lines.append(_md_table(_cross_table(data, "generica", metric, GENERIC_ORDER), "técnica"))
        lines.append("")

    lines.append("### 2.2 Cruce tipeadas (técnica × experimento)\n")
    for metric in SUMMARY_AUTO_METRICS:
        lines.append(f"#### {metric_label(metric)}\n")
        lines.append(_md_table(_cross_table(data, "tipeada", metric, TYPED_ORDER), "técnica"))
        lines.append("")

    lines.append("### 2.3 Mejor técnica por experimento\n")
    lines.append("| Experimento | " + " | ".join(SUMMARY_AUTO_METRICS) + " |")
    lines.append("| --- |" + " --- |" * len(SUMMARY_AUTO_METRICS))
    for label in _order_labels(list(by_label), GENERIC_ORDER + TYPED_ORDER):
        indexed = by_label[label]["indexed"]
        cells = []
        for metric in SUMMARY_AUTO_METRICS:
            technique, _ = _best(indexed, metric)
            cells.append(str(technique))
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines.append("")

    for i, (group, order, name) in enumerate(
        [
            ("generica", GENERIC_ORDER, "genéricas"),
            ("tipeada", TYPED_ORDER, "tipeadas"),
        ]
    ):
        base = 4 + 2 * i
        lines.append(f"### 2.{base} Mejor experimento por técnica — {name}\n")
        lines.append(
            _md_table(
                _best_experiment_table(data, group, SUMMARY_AUTO_METRICS, order), "técnica"
            )
        )
        lines.append("")
        lines.append(f"### 2.{base + 1} Mejor global — {name}\n")
        global_best = _global_best(data, group, SUMMARY_AUTO_METRICS, order)
        lines.append("| Métrica | Mejor (experimento / técnica) |")
        lines.append("| --- | --- |")
        for metric, value in global_best.items():
            lines.append(f"| {metric_label(metric)} | {value} |")
        lines.append("")

    lines.append("### 2.8 Efecto de la información (pares con tweets compartidos)\n")
    lines.append(_format_info_effect(_info_effect(data, SUMMARY_AUTO_METRICS), SUMMARY_AUTO_METRICS))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resumen de corridas del protocolo bajo outputs/."
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

    warnings = judge_warnings(runs)
    if warnings:
        print(
            "ADVERTENCIA (el LLM-as-judge es obligatorio):\n" + "\n".join(warnings),
            file=sys.stderr,
        )
        if args.strict:
            raise SystemExit(2)

    text = build_summary(runs, warnings)
    print(text)
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"resumen guardado en {args.save}")


if __name__ == "__main__":
    main()
