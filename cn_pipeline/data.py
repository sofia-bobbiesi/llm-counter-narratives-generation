"""Carga y preparación del dataset ASOHMO."""

from __future__ import annotations

import random
from typing import List

from load_dataset import load_asohmo


def resolve_extra_info(use_extra_info: str, cn_strategy: str) -> str:
    """Traduce la estrategia de tipo de contra-narrativa al flag interno.

    `load_dataset.parse_dataset` espera valores especiales (`cn_a`, `cn_a_no_info`,
    etc.) para filtrar por tipo de contra-narrativa. Esta función centraliza esa
    conversión.
    """
    if cn_strategy == "a":
        return "cn_a" if use_extra_info == "premises" else "cn_a_no_info"
    if cn_strategy == "b":
        return "cn_b" if use_extra_info == "collective" else "cn_b_no_info"
    if cn_strategy == "c":
        return "cn_c" if use_extra_info == "premises" else "cn_c_no_info"
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


def sample_counter_narrative(train: List[dict], val: List[dict], seed: int):
    """Muestrea una única contra-narrativa de train+val (para one-shot/CARE)."""
    pool = train + val
    if not pool:
        return ""
    example = random.Random(seed).choice(pool)
    cn = example["counterSpeech"]
    if isinstance(cn, list):
        return cn[0] if cn else ""
    return cn
