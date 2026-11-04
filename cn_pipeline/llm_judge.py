"""Evaluación LLM-as-judge (métrica obligatoria).

Puntúa contra-narrativas con un LLM como juez, consultado mediante una API
compatible con OpenAI. Se ejecuta en todos los experimentos: el modelo debe
configurarse en `llm_judge.model` y la clave se lee de la variable de entorno
indicada en `llm_judge.api_key_env` (por defecto `LLM_JUDGE_API_KEY`).

La rúbrica por defecto está alineada con la anotación humana del grupo sobre el
mismo corpus (Furman et al. 2023b; repo `DamiFur/CounterNarrativesEvaluation`):
usa sus aspectos y escalas — ofensividad (offensive, 1–3), stance frente al
mensaje (1–3), informatividad (informativeness, 0–3) y apropiación como
contra-narrativa (felicity, 1–3) — con anclas por punto redactadas de forma
operativa para el juez. La dirección de cada escala también es una definición
operativa propia (a validar contra el corpus etiquetado del grupo cuando se
corra la calibración). `judge_promedio` se calcula en código como media
normalizada (0–1) de los aspectos, nunca lo calcula el modelo. Si el juez falla
en una contra-narrativa puntual, esa fila se registra con `NaN` y no interrumpe
la corrida.
"""

from __future__ import annotations

import json
import math
import os
from abc import ABC, abstractmethod

# Aspectos y escalas del juez, alineados con el corpus etiquetado del grupo
# (repo DamiFur/CounterNarrativesEvaluation): aspecto -> (mínimo, máximo).
JUDGE_ASPECTS = {
    "offensive": (1, 3),
    "stance": (1, 3),
    "informativeness": (0, 3),
    "felicity": (1, 3),
}

# Dirección de cada escala (definiciones operativas propias; ver docstring y
# rúbrica): función que mapea el valor crudo a una calidad en [0, 1].
JUDGE_QUALITY = {
    "offensive": lambda v: (3.0 - v) / 2.0,   # 1 (nada ofensiva) -> 1 ; 3 -> 0
    "stance": lambda v: (v - 1.0) / 2.0,      # 1 (no refuta) -> 0 ; 3 (refuta) -> 1
    "informativeness": lambda v: v / 3.0,     # 0 (cliché) -> 0 ; 3 (específica) -> 1
    "felicity": lambda v: (v - 1.0) / 2.0,    # 1 (no funciona) -> 0 ; 3 -> 1
}

# Definición de los cuatro aspectos (con anclas). Fuente única compartida por el
# juez 1 (que puntúa) y el juez 2 (`validate_judge.py`, que compara por pares).
ASPECT_CRITERIA = (
    "offensive — ofensividad de la respuesta (1–3): 1 = nada ofensiva; 2 = "
    "levemente descalificadora o hiriente; 3 = claramente ofensiva hacia el "
    "colectivo atacado.\n"
    "stance — refutación del mensaje de odio (1–3): 1 = no refuta el mensaje (lo "
    "ignora, cambia de tema o llega a apoyarlo); 2 = refutación parcial o "
    "genérica; 3 = refuta directamente el mensaje o su argumento central.\n"
    "informativeness — contenido informativo que aporta (0–3): 0 = no aporta "
    "información (solo atribuye culpa o es un cliché); 1 = aporta algo de "
    "contenido; 2 = contenido relevante pero parcial; 3 = aporta información "
    "concreta y relevante (datos o refutación específica del argumento o del "
    "colectivo).\n"
    "felicity — apropiación como contra-narrativa en una intervención real "
    "(1–3): 1 = no funcionaría como respuesta al mensaje; 2 = funcionamiento "
    "dudoso (vaga, se pierde del tweet o no está dirigida a una audiencia "
    "amplia); 3 = muy apropiada: no es agresiva, ayuda a desescalar y a "
    "construir una contra-narrativa.\n"
)

DEFAULT_RUBRIC = (
    "Actuá como evaluador experto de contra-narrativas contra el discurso de odio. "
    "Dado un mensaje de odio y una contra-narrativa candidata, puntuá los cuatro "
    "aspectos siguientes con sus escalas (solo valores enteros dentro de la "
    "escala). Usá la escala completa: otorgá el valor máximo únicamente cuando el "
    "aspecto sea claramente notable, y penalizá las respuestas genéricas o de "
    "fórmula.\n\n"
    + ASPECT_CRITERIA
    + "\n"
    "Respondé SOLO con un objeto JSON con esta forma:\n"
    '{{"offensive": n, "stance": n, "informativeness": n, "felicity": n}}\n\n'
    "Mensaje de odio: {hate_tweet}\n"
    "Contra-narrativa: {counter_narrative}"
)


def render_rubric(rubric: str, hate_tweet: str, counter_narrative: str) -> str:
    """Sustituye los placeholders de la rúbrica."""
    try:
        return rubric.format(hate_tweet=hate_tweet, counter_narrative=counter_narrative)
    except (KeyError, IndexError, ValueError):
        return (
            rubric.replace("{hate_tweet}", hate_tweet)
            .replace("{counter_narrative}", counter_narrative)
        )


def parse_judge_json(content: str) -> dict:
    """Extrae un JSON de la salida del juez (tolera code fences y texto extra)."""
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.lower().startswith("json"):
            content = content[4:]
    start = content.find("{")
    end = content.rfind("}")
    if start != -1 and end != -1 and end > start:
        content = content[start : end + 1]
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        data = {}
    return {k: float(v) for k, v in data.items() if isinstance(v, (int, float))}


class JudgeBackend(ABC):
    """Interfaz común de los backends de LLM-as-judge."""

    @abstractmethod
    def judge(self, hate_tweet: str, counter_narrative: str) -> dict:
        """Devuelve un diccionario con los puntajes por aspecto."""


class APIBackend(JudgeBackend):
    """Backend que consulta un endpoint compatible con OpenAI."""

    def __init__(self, model: str, base_url=None, api_key_env: str = "LLM_JUDGE_API_KEY",
                 rubric=None, max_tokens: int = 300, temperature: float = 0.0,
                 timeout: int = 120):
        self.model = model
        self.base_url = base_url
        self.api_key_env = api_key_env
        self.rubric = rubric or DEFAULT_RUBRIC
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

    def judge(self, hate_tweet: str, counter_narrative: str) -> dict:
        import requests

        api_key = os.environ.get(self.api_key_env)
        if not api_key:
            raise RuntimeError(
                f"No se encontró la clave en la variable de entorno {self.api_key_env}. "
                "Configurala antes de usar LLM-as-judge."
            )
        messages = [
            {
                "role": "user",
                "content": render_rubric(self.rubric, hate_tweet, counter_narrative),
            }
        ]
        response = requests.post(
            f"{self.base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": False,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return parse_judge_json(content)


def judge_with_retry(judge: JudgeBackend, hate_tweet: str, counter_narrative: str,
                     retries: int = 3, base_delay: float = 2.0) -> dict:
    """Llama al juez reintentando ante errores transitorios (red/429/5xx).

    Usa backoff exponencial (`base_delay * 2**intento`) y respeta el encabezado
    `Retry-After` si está presente. Los errores de configuración (p. ej.
    `RuntimeError` por clave faltante) y los 4xx no reintentables se propagan.
    """
    import time

    import requests

    attempt = 0
    while True:
        try:
            return judge.judge(hate_tweet, counter_narrative)
        except RuntimeError:
            raise
        except requests.exceptions.RequestException as exc:
            response = getattr(exc, "response", None)
            status = getattr(response, "status_code", None)
            retryable = status is None or status == 429 or 500 <= status < 600
            if attempt >= retries or not retryable:
                raise
            delay = base_delay * (2 ** attempt)
            retry_after = getattr(response, "headers", {}).get("Retry-After")
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except (TypeError, ValueError):
                    pass
            time.sleep(delay)
            attempt += 1


def build_judge(judge_cfg):
    """Construye el backend API del juez, validando modelo y clave.

    El evaluador es obligatorio, por lo que aborta con un mensaje claro si no se
    configuró el modelo o si la variable de entorno con la clave no está seteada.
    """
    if judge_cfg is None or not judge_cfg.model:
        raise ValueError(
            "El evaluador LLM-as-judge es obligatorio: configurá 'llm_judge.model' "
            "en el archivo de configuración."
        )
    if not judge_cfg.base_url:
        raise ValueError(
            "Configurá 'llm_judge.base_url' con el endpoint del evaluador"
        )
    if not os.environ.get(judge_cfg.api_key_env):
        raise RuntimeError(
            "Falta la clave del evaluador LLM-as-judge: seteá la variable de "
            f"entorno '{judge_cfg.api_key_env}' antes de ejecutar el experimento."
        )
    return APIBackend(
        model=judge_cfg.model,
        base_url=judge_cfg.base_url,
        api_key_env=judge_cfg.api_key_env,
        rubric=judge_cfg.rubric,
        max_tokens=judge_cfg.max_tokens,
        temperature=judge_cfg.temperature,
        timeout=getattr(judge_cfg, "timeout", 120),
    )


def judge_promedio(scores: dict) -> float:
    """Media normalizada (0–1) de los aspectos del juez; NaN si falta alguno.

    `scores` admite claves del backend (`offensive`) o de fila
    (`judge_offensitive`... `judge_offensive`). Se calcula en código, nunca por
    el modelo, para que sea determinista y comparable.
    """
    values = []
    for aspect, quality in JUDGE_QUALITY.items():
        v = scores.get(aspect, scores.get(f"judge_{aspect}", float("nan")))
        try:
            v = float(v)
        except (TypeError, ValueError):
            return float("nan")
        if math.isnan(v):
            return float("nan")
        values.append(quality(v))
    return sum(values) / len(values)


def judge_rows(judge: JudgeBackend, rows, retries: int = 0, base_delay: float = 2.0) -> list:
    """Añade a cada fila los puntajes del juez (columnas `judge_*`).

    Cada aspecto se recorta a su escala (`JUDGE_ASPECTS`); un aspecto ausente
    queda como `NaN`. `judge_promedio` es la media normalizada (0–1) calculada
    en código con `judge_promedio()`: NaN si falta algún aspecto.
    """
    updated = []
    for row in rows:
        new_row = dict(row)
        try:
            scores = judge_with_retry(
                judge,
                row["hate_speech"],
                row["generated_cn"],
                retries=retries,
                base_delay=base_delay,
            )
        except Exception as exc:  # no interrumpir todo el experimento por un fallo
            scores = {"error": str(exc)}
        for aspect, (low, high) in JUDGE_ASPECTS.items():
            value = scores.get(aspect)
            if isinstance(value, (int, float)) and not math.isnan(value):
                new_row[f"judge_{aspect}"] = float(min(max(value, low), high))
            else:
                new_row[f"judge_{aspect}"] = float("nan")
        new_row["judge_promedio"] = judge_promedio(new_row)
        if "error" in scores:
            new_row["judge_error"] = scores["error"]
        updated.append(new_row)
    return updated
