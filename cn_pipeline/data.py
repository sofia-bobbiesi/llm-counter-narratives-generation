"""Carga y preparación del dataset ASOHMO."""

from __future__ import annotations

import random
from typing import List

from load_dataset import load_asohmo

# Estrategias de tipo de contra-narrativa soportadas. Las variantes "a/b/c"
# inyectan la información argumentativa del tipo; las "*_no_info" solo filtran.
CN_STRATEGIES = ("", "a", "b", "c", "a_no_info", "b_no_info", "c_no_info")


def resolve_extra_info(use_extra_info: str, cn_strategy: str) -> str:
    """Traduce la estrategia de tipo de contra-narrativa al flag interno.

    Cuando `cn_strategy` selecciona un tipo, se inyecta la información
    argumentativa correspondiente a ese tipo (con independencia de
    `use_extra_info`):
        - "a" / "b" / "c" → con info:
            "a" -> justificación + conclusión (+ colectivo y propiedad)
            "b" -> colectivo + propiedad
            "c" -> justificación + conclusión
        - "a_no_info" / "b_no_info" / "c_no_info" → mismo filtro de tipo, pero
          SIN información argumentativa.

    `use_extra_info` solo se usa cuando `cn_strategy` es "" (sin tipo).
    """
    if cn_strategy in ("a", "b", "c"):
        return f"cn_{cn_strategy}"  # con info
    if cn_strategy in ("a_no_info", "b_no_info", "c_no_info"):
        return f"cn_{cn_strategy}"  # sin info
    return use_extra_info


def load_data(use_extra_info: str = "", cn_strategy: str = ""):
    """Carga las particiones test/train/dev de ASOHMO.

    Devuelve una tupla `(test, train, val)` de listas de diccionarios con claves
    `hateSpeech`, `counterSpeech`, `extra_info` y `language`.
    """
    extra_info = resolve_extra_info(use_extra_info, cn_strategy)
    test, train, val = load_asohmo(use_extra_info=extra_info, finetuning=False)
    return test, train, val


def sample_examples(train: List[dict], val: List[dict], n: int, seed: int) -> List[dict]:
    """Muestrea `n` ejemplos (tweet + contra-narrativa) de train+val para few-shot."""
    pool = train + val
    rng = random.Random(seed)
    return rng.sample(pool, min(n, len(pool)))


def sample_counter_narrative(train: List[dict], val: List[dict], seed: int) -> str:
    """Muestrea una única contra-narrativa de train+val (para one-shot/CARE)."""
    pool = train + val
    if not pool:
        return ""
    example = random.Random(seed).choice(pool)
    cn = example["counterSpeech"]
    if isinstance(cn, list):
        return cn[0] if cn else ""
    return cn
