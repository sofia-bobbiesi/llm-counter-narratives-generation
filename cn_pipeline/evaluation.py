"""Evaluación automática con BLEU, ROUGE y BERTScore.

Cada tweet del corpus puede tener más de una contra-narrativa de referencia
(los tres tipos A/B/C). Para no privilegiar arbitrariamente una de ellas, cada
métrica se calcula contra todas las referencias disponibles de cada fila y se
reporta el máximo: una generación que se aproxime a cualquiera de las
respuestas humanas válidas obtiene crédito.

En las corridas con tipo de contra-narrativa (a/b/c) la referencia es única
(la de ese tipo), por lo que el máximo equivale a la métrica directa.

Toma una lista de filas (una por <tweet, técnica>) y produce:
    - un DataFrame detallado con las métricas por fila;
    - un DataFrame resumen con el promedio de cada métrica por técnica.
"""

from __future__ import annotations

import ast

import evaluate
import pandas as pd

DEFAULT_BERT_MODEL = "dccuchile/bert-base-spanish-wwm-cased"

# Columnas de la tabla detallada que no son métricas (no se promedian).
NON_METRIC_COLUMNS = {
    "hate_speech",
    "true_cn",
    "generated_cn",
    "prompt_type",
}


def get_references(reference) -> list:
    """Devuelve la lista de contra-narrativas de referencia limpias.

    Acepta una lista de contra-narrativas (corridas genéricas), una única
    contra-narrativa (corridas con tipo) o su representación como string
    (p. ej. al releer un CSV guardado).
    """
    if reference is None:
        return []
    if isinstance(reference, str):
        text = reference.strip()
        if text.startswith("["):
            try:
                reference = ast.literal_eval(text)
            except (ValueError, SyntaxError):
                pass
    items = reference if isinstance(reference, list) else [reference]
    refs = [str(item).strip() for item in items]
    return [r for r in refs if r]


def evaluate_predictions(
    rows,
    metrics=None,
    bert_model: str = DEFAULT_BERT_MODEL,
):
    """Evalúa una lista de filas (dicts) y devuelve (detallado, resumen).

    Cada fila debe tener las claves: `hate_speech`, `true_cn`, `prompt_type` y
    `generated_cn`, además de las columnas `judge_*` que agrega el evaluador
    LLM-as-judge (se incluyen en el resumen por ser numéricas).

    Por cada fila se calcula cada métrica contra cada referencia disponible y
    se conserva el máximo.
    """
    metrics = metrics or ["bleu", "rouge", "bertscore"]
    detailed = pd.DataFrame(rows)

    predictions = detailed["generated_cn"].astype(str).tolist()
    references = detailed["true_cn"].apply(get_references).tolist()
    # Guarda contra filas sin referencias (no debería ocurrir en el corpus).
    references = [refs or [""] for refs in references]

    if "bleu" in metrics:
        bleu = evaluate.load("bleu")
        detailed["BLEU"] = [
            max(bleu.compute(predictions=[p], references=[[r]])["bleu"] for r in refs)
            for p, refs in zip(predictions, references)
        ]

    if "rouge" in metrics:
        rouge = evaluate.load("rouge")
        r1, r2, rl = [], [], []
        for p, refs in zip(predictions, references):
            scores = [rouge.compute(predictions=[p], references=[r]) for r in refs]
            r1.append(max(s["rouge1"] for s in scores))
            r2.append(max(s["rouge2"] for s in scores))
            rl.append(max(s["rougeL"] for s in scores))
        detailed["ROUGE-1"] = r1
        detailed["ROUGE-2"] = r2
        detailed["ROUGE-L"] = rl

    if "bertscore" in metrics:
        # Se usa la librería `bert_score` directamente: el wrapper de `evaluate`
        # solo acepta modelos predefinidos (lanza KeyError con `dccuchile/...`).
        from bert_score import score as bert_score_score

        # Se expande cada fila por sus referencias y se conserva el máximo F1.
        flat_predictions, flat_references, owner = [], [], []
        for i, (p, refs) in enumerate(zip(predictions, references)):
            for r in refs:
                flat_predictions.append(p)
                flat_references.append(r)
                owner.append(i)
        _, _, f1 = bert_score_score(
            flat_predictions,
            flat_references,
            lang="es",
            model_type=bert_model,
            num_layers=12,
            verbose=False,
        )
        best = [-1.0] * len(predictions)
        for i, value in zip(owner, f1.tolist()):
            best[i] = max(best[i], value)
        detailed["BERT-F1"] = best

    # Presentación legible en el CSV: referencias y generaciones en una sola línea.
    detailed["true_cn"] = [" || ".join(refs) for refs in references]
    detailed["generated_cn"] = [p.replace("\n", " ").strip() for p in predictions]

    summary = summarize(detailed)
    return detailed, summary


def summarize(detailed: pd.DataFrame) -> pd.DataFrame:
    """Promedia las métricas (columnas numéricas) por tipo de prompt."""
    metric_cols = [
        c
        for c in detailed.columns
        if c not in NON_METRIC_COLUMNS and pd.api.types.is_numeric_dtype(detailed[c])
    ]
    if not metric_cols:
        return pd.DataFrame(columns=["prompt_type"])
    return detailed.groupby("prompt_type")[metric_cols].mean().reset_index()
