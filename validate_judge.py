"""Segundo juez: comparación por pares (CN generada vs conjunto de CNs humanas).

Instrumento de validación independiente del juez de producción. Para cada fila
de un `results.csv` ya generado, compara la contra-narrativa generada contra las
referencias humanas del mismo tweet (presentadas juntas en un lado, la generada
en el otro, con el lado asignado por seed) y pregunta cuál funciona mejor como
contra-narrativa. Permite empates.

Una llamada por fila. En las corridas con tipo hay una sola referencia, así que
coincide con el 1-vs-1. En un 20% de las filas se corre también el orden
invertido (control de sesgo de posición).

Los resultados se escriben **en el `results.csv` y `summary.csv` de la corrida**
(igual que el juez 1), con las columnas `judge2_*`; no genera archivos aparte.
El juez de producción (qwen3.8, rúbrica de 4 aspectos) no se toca.

Uso:
    export LLM_JUDGE_API_KEY=<token>
    python validate_judge.py paircompare \\
        --run_dir outputs/gemma-4-12B-it/gemma-4-12B-it_spanish_all_no-strategy_seed42

Smoke con pocas llamadas: --limit 3.  Sin API: --dry_run.
Resumible: las filas ya puntuadas en `results.csv` se saltean.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import time

import pandas as pd
import requests

from cn_pipeline.evaluation import summarize
from cn_pipeline.llm_judge import ASPECT_CRITERIA

# Columnas que agrega el juez 2 (orden canónico en el CSV).
JUDGE2_COLUMNS = ["judge2_verdict", "judge2_n_refs", "judge2_reason",
                  "judge2_swapped_verdict"]

# ---------------------------------------------------------------------------
# Prompt (construcción por concatenación: los textos pueden tener llaves)
# ---------------------------------------------------------------------------
_PAIR_HEADER = (
    "Dado el siguiente mensaje de odio y dos propuestas de respuesta (A y B), "
    "decidí cuál funciona mejor como contra-narrativa, considerando los mismos "
    "criterios que un evaluador de contra-narrativas:\n\n"
    + ASPECT_CRITERIA
    + "\n"
    "Gana la propuesta que, en balance, cumpla mejor esos criterios. Una de las "
    "propuestas puede reunir varias respuestas: juzgá la propuesta según su mejor "
    "respuesta. No prefieras por extensión ni formalidad. Permité empates si son "
    "equivalentes.\n\n"
)

_PAIR_TAIL = (
    'Respondé SOLO con un objeto JSON con esta forma:\n'
    '{"prefer": "A" o "B" o "tie", "razon": "una frase breve"}\n\n'
    'Aquí está el mensaje de odio y las dos propuestas de respuesta:\n\n'
)

_MAX_REASON_CHARS = 200


def format_references_block(references) -> str:
    """Formatea un conjunto de referencias humanas como lista numerada."""
    if len(references) == 1:
        return references[0]
    return "\n".join(f"{i}. {ref}" for i, ref in enumerate(references, 1))


def build_pair_prompt(tweet: str, a_text: str, b_text: str) -> str:
    """Arma el prompt ciego del juez 2 (sin `.format` sobre los datos)."""
    return (
        _PAIR_HEADER
        + "Mensaje de odio:\n"
        + tweet
        + "\n\nRespuesta A:\n"
        + a_text
        + "\n\nRespuesta B:\n"
        + b_text
        + "\n\n"
        + _PAIR_TAIL
    )


def parse_pair_json(content: str) -> dict | None:
    """Extrae `{"prefer": "A"|"B"|"tie", ...}` de la salida del juez.

    Devuelve None si no se puede parsear o si `prefer` no es A/B/tie (señal de
    reintento en el backend).
    """
    text = (content or "").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        data = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    prefer_map = {"a": "A", "b": "B", "tie": "tie"}
    prefer = str(data.get("prefer", "")).strip().lower()
    if prefer not in prefer_map:
        return None
    return {"prefer": prefer_map[prefer],
            "razon": str(data.get("razon", "")).strip()[:_MAX_REASON_CHARS]}


# ---------------------------------------------------------------------------
# Backend del juez 2 (inline: el pipeline de producción no se toca)
# ---------------------------------------------------------------------------
class PairJudge:
    """Cliente del endpoint compatible con OpenAI para el juez por pares."""

    def __init__(self, model: str, base_url: str, api_key_env: str = "LLM_JUDGE_API_KEY",
                 temperature: float = 0.0, max_tokens: int = 300, timeout: int = 120,
                 max_retries: int = 3, base_delay: float = 2.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.last_error = ""

    def ask(self, prompt: str) -> dict | None:
        """Consulta al juez 2: veredicto parseado o None en fallo."""
        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise SystemExit(
                f"Falta la clave del juez 2: exportá {self.api_key_env}=<token> antes de correr."
            )
        response = None
        for attempt in range(self.max_retries + 1):
            delay = self.base_delay * (2 ** attempt)
            retry_after = None
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": self.temperature,
                        "max_tokens": self.max_tokens,
                        "stream": False,
                    },
                    timeout=self.timeout,
                )
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                verdict = parse_pair_json(content)
                if verdict is not None:
                    return verdict
                self.last_error = "salida no parseable"
            except requests.exceptions.RequestException as exc:
                self.last_error = str(exc)
                response = getattr(exc, "response", None)
                status = getattr(response, "status_code", None)
                retryable = status is None or status == 429 or 500 <= status < 600
                if attempt >= self.max_retries or not retryable:
                    return None
                retry_after = getattr(response, "headers", {}).get("Retry-After")
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except (TypeError, ValueError):
                    pass
            time.sleep(delay)
        return None


# ---------------------------------------------------------------------------
# Planificación de comparaciones (una por fila; doble orden en una fracción)
# ---------------------------------------------------------------------------
def split_references(true_cn) -> list:
    """Divide la columna `true_cn` (unida con ' || ') en sus referencias."""
    if pd.isna(true_cn):
        return []
    return [r.strip() for r in str(true_cn).split(" || ") if r.strip()]


def plan_comparisons(df: pd.DataFrame, seed: int, swap_frac: float) -> list:
    """Planifica una comparación por fila (+ doble orden en un `swap_frac`).

    `gen_in` ("A"/"B") es el lado donde queda la CN generada, derivado
    determinísticamente de (seed, tweet, técnica) — idempotente entre corridas.
    """
    plan = []
    for row_idx, row in df.iterrows():
        tweet_raw = row.get("hate_speech")
        tweet = "" if pd.isna(tweet_raw) else str(tweet_raw).strip()
        technique = str(row.get("prompt_type", "") or "")
        candidate_raw = row.get("generated_cn")
        candidate = "" if pd.isna(candidate_raw) else str(candidate_raw).strip()
        references = split_references(row.get("true_cn"))
        refs_block = format_references_block(references)
        cmp_id = hashlib.sha1(f"{tweet}|{technique}".encode("utf-8")).hexdigest()[:12]
        gen_in = "A" if random.Random(f"{seed}:{cmp_id}:side").random() < 0.5 else "B"
        plan.append({
            "row_idx": row_idx, "technique": technique, "tweet": tweet,
            "candidate": candidate, "refs_block": refs_block,
            "n_refs": len(references), "gen_in": gen_in, "order": 0,
        })
        if random.Random(f"{seed}:{cmp_id}:swap").random() < swap_frac:
            plan.append({
                "row_idx": row_idx, "technique": technique, "tweet": tweet,
                "candidate": candidate, "refs_block": refs_block,
                "n_refs": len(references),
                "gen_in": "B" if gen_in == "A" else "A", "order": 1,
            })
    return plan


def resolve(prefer: str, gen_in: str) -> str:
    """Convierte (prefer, lado donde estaba la generada) en quien ganó."""
    if prefer == "tie":
        return "tie"
    if prefer in ("A", "B"):
        return "generated" if prefer == gen_in else "human"
    return "invalid"


def humanize_reason(reason: str, gen_in: str) -> str:
    """Reemplaza las referencias de lado ('A'/'B') por 'la respuesta generada/humana'.

    El juez 2 redacta el motivo con los lados "A"/"B" (prompt ciego); acá se
    traduce al lado real usando `gen_in`, sin guardar la columna del lado. Se
    normalizan las formas "la respuesta/opción/propuesta X", "la X" y "X" suelta
    a una única frase, para no duplicar artículos. Solo considera letras A/B
    mayúsculas sueltas (no rompe preposiciones ni palabras como "Aporta").
    """
    if not reason:
        return reason
    label = ({"A": "generada", "B": "humana"} if gen_in == "A"
             else {"A": "humana", "B": "generada"})

    def phrase(match):
        return f"la respuesta {label[match.group(1)]}"

    text = reason
    text = re.sub(r"[Ll]a\s+(?:respuesta|opci[oó]n|propuesta)\s+([AB])\b", phrase, text)
    text = re.sub(r"[Ll]a\s+([AB])\b", phrase, text)
    text = re.sub(r"\b([AB])\b", phrase, text)
    # Capitalizar si la referencia quedó al inicio de oración.
    text = re.sub(
        r"(^|[.!?]\s+)(la respuesta (?:generada|humana))",
        lambda m: m.group(1) + m.group(2)[0].upper() + m.group(2)[1:],
        text,
    )
    return text


# ---------------------------------------------------------------------------
# Escritura en el results.csv de la corrida
# ---------------------------------------------------------------------------
def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Crea las columnas `judge2_*` con dtype estable si no existen."""
    if "judge2_verdict" not in df.columns:
        df["judge2_verdict"] = pd.Series([None] * len(df), dtype=object, index=df.index)
    if "judge2_swapped_verdict" not in df.columns:
        df["judge2_swapped_verdict"] = pd.Series([None] * len(df), dtype=object, index=df.index)
    if "judge2_n_refs" not in df.columns:
        df["judge2_n_refs"] = pd.Series(pd.NA, index=df.index, dtype="Int64")
    if "judge2_reason" not in df.columns:
        df["judge2_reason"] = pd.Series([None] * len(df), dtype=object, index=df.index)
    return df


JUDGE2_RATE_COLUMNS = ["judge2_gen_rate", "judge2_human_rate", "judge2_tie_rate"]


def judge2_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Tasas de veredicto del juez 2 por técnica (generated/human/tie)."""
    empty = pd.DataFrame(columns=["prompt_type"] + JUDGE2_RATE_COLUMNS)
    if "judge2_verdict" not in df.columns:
        return empty
    valid = df[df["judge2_verdict"].isin(["generated", "human", "tie"])]
    if not len(valid):
        return empty
    tab = pd.crosstab(valid["prompt_type"], valid["judge2_verdict"], normalize="index")
    for c in ("generated", "human", "tie"):
        if c not in tab.columns:
            tab[c] = 0.0
    rates = tab[["generated", "human", "tie"]].rename(columns={
        "generated": "judge2_gen_rate", "human": "judge2_human_rate",
        "tie": "judge2_tie_rate"})
    return rates.round(4).reset_index()


def write_results(df: pd.DataFrame, run_dir: str) -> None:
    """Escribe results.csv (columnas `judge2_*` tras `judge_*`) y summary.csv."""
    # Limpiar columnas judge2_* fuera del esquema canónico (p. ej. `judge2_score`
    # de versiones previas).
    stale = [c for c in df.columns if c.startswith("judge2_") and c not in JUDGE2_COLUMNS]
    if stale:
        df = df.drop(columns=stale)
    judge_cols = [c for c in df.columns if c.startswith("judge_")]
    judge2_cols = [c for c in JUDGE2_COLUMNS if c in df.columns]
    base = [c for c in df.columns if c not in judge2_cols]
    if judge_cols:
        anchor = judge_cols[-1]
    elif "generated_cn" in base:
        anchor = "generated_cn"
    else:
        anchor = base[-1]
    pos = base.index(anchor) + 1
    ordered = base[:pos] + judge2_cols + base[pos:]
    df = df[ordered]

    summary = summarize(df)
    rates = judge2_rates(df)
    if len(rates) and "prompt_type" in summary.columns:
        summary = summary.merge(rates, on="prompt_type", how="left")
    # `judge2_n_refs` solo vive en results.csv (trazabilidad por fila); no aporta
    # al summary (es ~constante por técnica).
    summary = summary.drop(columns=["judge2_n_refs"], errors="ignore")
    # Orden del summary: prompt_type, judge_*, judge2_*, resto.
    cols = list(summary.columns)
    judge_cols_s = [c for c in cols if c.startswith("judge_")]
    judge2_cols_s = [c for c in cols if c.startswith("judge2_")]
    rest_s = [c for c in cols if c != "prompt_type" and c not in judge_cols_s
              and c not in judge2_cols_s]
    summary = summary[["prompt_type"] + judge_cols_s + judge2_cols_s + rest_s]

    results_path = os.path.join(run_dir, "results.csv")
    summary_path = os.path.join(run_dir, "summary.csv")
    df.to_csv(results_path, index=False)
    summary.to_csv(summary_path, index=False)


def print_position_bias(df: pd.DataFrame) -> None:
    """Imprime el sesgo de posición a partir de la columna swapped."""
    swapped = df[df["judge2_swapped_verdict"].notna()]
    if not len(swapped):
        return
    agree = int((swapped["judge2_verdict"] == swapped["judge2_swapped_verdict"]).sum())
    print(f"[pair2] sesgo de posición: {agree}/{len(swapped)} filas con veredicto "
          "idéntico en ambos órdenes")


def run_paircompare(args) -> None:
    run_dir = args.run_dir
    results_path = os.path.join(run_dir, "results.csv")
    if not os.path.isfile(results_path):
        raise SystemExit(f"No se encontró {results_path}")

    df = pd.read_csv(results_path)
    if args.limit_rows is not None:
        df = df.head(args.limit_rows)
    df = _ensure_columns(df)

    plan = plan_comparisons(df, seed=args.seed, swap_frac=args.swap_frac)
    base = [c for c in plan if c["order"] == 0]
    pending = []
    for c in plan:
        col = "judge2_verdict" if c["order"] == 0 else "judge2_swapped_verdict"
        if pd.isna(df.at[c["row_idx"], col]):
            pending.append(c)

    print(f"[pair2] run={os.path.basename(os.path.normpath(run_dir))} filas={len(df)} "
          f"comparaciones={len(plan)} (base={len(base)}, doble orden={len(plan) - len(base)}) "
          f"pendientes={len(pending)}")

    if args.dry_run:
        print("[pair2] dry-run: sin llamadas al juez.")
        return
    if not pending:
        write_results(df, run_dir)
        print_position_bias(df)
        print("[pair2] nada pendiente; results.csv/summary.csv regenerados.")
        return

    judge = PairJudge(args.j2_model, args.j2_base_url, args.api_key_env,
                      temperature=args.judge_temperature, max_tokens=args.max_tokens,
                      timeout=args.timeout, max_retries=args.max_retries)

    executed = 0
    for c in plan:
        col = "judge2_verdict" if c["order"] == 0 else "judge2_swapped_verdict"
        if pd.notna(df.at[c["row_idx"], col]):
            continue
        if args.limit is not None and executed >= args.limit:
            break
        if not c["candidate"] or not c["refs_block"]:
            resolved, reason = "invalid", "texto vacío"
        else:
            if c["gen_in"] == "A":
                a_text, b_text = c["candidate"], c["refs_block"]
            else:
                a_text, b_text = c["refs_block"], c["candidate"]
            verdict = judge.ask(build_pair_prompt(c["tweet"], a_text, b_text))
            prefer = (verdict or {}).get("prefer", "")
            resolved = resolve(prefer, c["gen_in"])
            # Una sola columna combina el motivo del juez y el error.
            reason = (verdict or {}).get("razon", "") if verdict is not None else judge.last_error
        df.at[c["row_idx"], col] = resolved
        if c["order"] == 0:
            df.at[c["row_idx"], "judge2_n_refs"] = c["n_refs"]
            df.at[c["row_idx"], "judge2_reason"] = humanize_reason(reason, c["gen_in"]) or None
        write_results(df, run_dir)  # persistir tras cada llamada (tolerante a cortes)
        executed += 1
        print(f"[pair2] {executed}/{len(pending)} {c['technique']} "
              f"({c['n_refs']} refs, gen en {c['gen_in']}) -> {resolved}")

    print_position_bias(df)
    counts = df["judge2_verdict"].value_counts(dropna=True).to_dict()
    print(f"[pair2] listo: {results_path} y summary.csv actualizados | {counts}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Juez 2: compara la CN generada de un run contra el conjunto de "
            "referencias humanas (1 llamada por fila) y escribe las columnas "
            "judge2_* en el results.csv de la corrida."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("paircompare",
                       help="Compara la CN generada contra el conjunto de referencias humanas.")
    p.add_argument("--run_dir", type=str, required=True,
                   help="Directorio del run con results.csv.")
    p.add_argument("--j2_model", type=str, default="vllm/ministral3-8b",
                   help="Modelo juez 2 (tag tal como aparece en el endpoint).")
    p.add_argument("--j2_base_url", type=str,
                   default="https://chat.ccad.unc.edu.ar/api",
                   help="Endpoint base compatible con OpenAI (sin /chat/completions).")
    p.add_argument("--api_key_env", type=str, default="LLM_JUDGE_API_KEY")
    p.add_argument("--judge_temperature", type=float, default=0.0)
    p.add_argument("--max_tokens", type=int, default=300)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--max_retries", type=int, default=3)
    p.add_argument("--swap_frac", type=float, default=0.2,
                   help="Fracción de filas con doble orden (sesgo de posición).")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--limit_rows", type=int, default=None,
                   help="Procesar solo las primeras N filas (pruebas).")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap de llamadas nuevas en esta sesión (smoke).")
    p.add_argument("--dry_run", action="store_true",
                   help="Enumera las comparaciones sin llamar al juez.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "paircompare":
        run_paircompare(args)
    else:
        parser.error(f"subcomando desconocido: {args.command}")


if __name__ == "__main__":
    main()
