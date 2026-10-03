"""Configuración de experimentos.

Define la estructura de un experimento mediante dataclasses, funciones para
cargar/guardar la configuración desde/hacia JSON y un parser de línea de
comandos (argparse) que permite sobreescribir valores puntuales.

Uso típico:
    from cn_pipeline.config import load_config, build_parser, apply_overrides
    cfg = load_config("configs/config_gemma.json")
    args = build_parser().parse_args()
    cfg = apply_overrides(cfg, args)
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional

from .prompts import PROMPTS

# Modos de cuantización soportados (además de None, sin cuantizar).
QUANTIZATION_MODES = (None, "8bit", "4bit")


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
@dataclass
class GenerationParams:
    """Parámetros de generación pasados a `model.generate`."""

    max_new_tokens: int = 200
    do_sample: bool = True
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 0
    num_beams: int = 1
    no_repeat_ngram_size: int = 0


@dataclass
class LLMJudgeConfig:
    """Configuración del evaluador LLM-as-judge vía API (métrica obligatoria).

    El modelo (`model`) no tiene valor por defecto: debe configurarse. La clave
    se lee de la variable de entorno indicada en `api_key_env`.
    """

    model: Optional[str] = None  # sin default: debe configurarse
    base_url: Optional[str] = None  # endpoint base (obligatorio), sin '/chat/completions'
    api_key_env: str = "LLM_JUDGE_API_KEY"  # variable de entorno con la clave
    rubric: Optional[str] = None  # None -> rúbrica por defecto de llm_judge
    max_tokens: int = 300
    temperature: float = 0.0


@dataclass
class Config:
    """Descripción completa de un experimento."""

    model_name: str = "google/gemma-4-12B-it"
    use_extra_info: str = ""  # "" | "collective" | "premises" | "all"
    cn_strategy: str = ""  # "" | "a" | "b" | "c"
    language: str = "spanish"
    fewshot_examples: int = 3  # nº de ejemplos para el prompt few_shot
    prompt_types: List[str] = field(
        default_factory=lambda: list(PROMPTS.keys())
    )
    max_samples: Optional[int] = None  # nº de tweets a muestrear (None = todo el test)
    seed: int = 42
    device: str = "auto"  # "auto" | "cuda" | "cpu"
    torch_dtype: str = "auto"  # "auto" | "float16" | "bfloat16" | "float32"
    quantization: Optional[str] = None  # None | "8bit" | "4bit"
    generation: GenerationParams = field(default_factory=GenerationParams)
    metrics: List[str] = field(
        default_factory=lambda: ["bleu", "rouge", "bertscore"]
    )
    llm_judge: LLMJudgeConfig = field(default_factory=LLMJudgeConfig)
    output_dir: str = "outputs"


# ---------------------------------------------------------------------------
# (De)serialización
# ---------------------------------------------------------------------------
def config_from_dict(data: dict) -> Config:
    """Construye una `Config` a partir de un diccionario (JSON)."""
    data = dict(data)
    generation = GenerationParams(**(data.pop("generation", None) or {}))
    judge_data = data.pop("llm_judge", None)
    llm_judge = LLMJudgeConfig(**(judge_data or {}))
    return Config(generation=generation, llm_judge=llm_judge, **data)


def config_to_dict(cfg: Config) -> dict:
    """Convierte una `Config` a diccionario (serializable a JSON)."""
    return asdict(cfg)


def load_config(path: str) -> Config:
    """Carga una configuración desde un archivo JSON."""
    with open(path, encoding="utf-8") as f:
        return config_from_dict(json.load(f))


def save_config(cfg: Config, path: str) -> None:
    """Guarda una configuración como JSON (para reproducibilidad)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config_to_dict(cfg), f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
_SIMPLE_FIELDS = [
    "model_name",
    "use_extra_info",
    "cn_strategy",
    "language",
    "fewshot_examples",
    "max_samples",
    "seed",
    "device",
    "torch_dtype",
    "quantization",
    "output_dir",
]

_GENERATION_FIELDS = [
    "max_new_tokens",
    "do_sample",
    "temperature",
    "top_p",
    "top_k",
    "num_beams",
    "no_repeat_ngram_size",
]


def build_parser() -> argparse.ArgumentParser:
    """Parser de línea de comandos. Todos los argumentos son opcionales y
    sobreescriben la configuración cargada desde archivo."""
    parser = argparse.ArgumentParser(
        description="Genera contra-narrativas contra el discurso de odio y las evalúa."
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Ruta a un archivo JSON de configuración.",
    )
    for field_name in _SIMPLE_FIELDS:
        parser.add_argument(f"--{field_name}", type=str, default=None)
    parser.add_argument(
        "--prompt_types",
        type=str,
        default=None,
        help="Lista de técnicas separadas por comas, p. ej. zero_shot,few_shot.",
    )
    for field_name in _GENERATION_FIELDS:
        parser.add_argument(f"--{field_name}", type=str, default=None)
    return parser


def _coerce(value: str, target):
    """Convierte el string de CLI al tipo del campo correspondiente."""
    if isinstance(target, bool):
        return str(value).strip().lower() in ("1", "true", "yes", "on")
    if isinstance(target, int):
        return int(value)
    if isinstance(target, float):
        return float(value)
    return value


def apply_overrides(cfg: Config, args: argparse.Namespace) -> Config:
    """Aplica al `cfg` solo los argumentos de CLI provistos (no None)."""
    for field_name in _SIMPLE_FIELDS:
        value = getattr(args, field_name, None)
        if value is not None:
            setattr(cfg, field_name, _coerce(value, getattr(cfg, field_name)))

    if getattr(args, "prompt_types", None):
        cfg.prompt_types = [
            s.strip() for s in args.prompt_types.split(",") if s.strip()
        ]

    for field_name in _GENERATION_FIELDS:
        value = getattr(args, field_name, None)
        if value is not None:
            setattr(
                cfg.generation,
                field_name,
                _coerce(value, getattr(cfg.generation, field_name)),
            )
    return cfg


def resolve_device(device: str):
    """Devuelve un `torch.device` a partir del string de configuración."""
    import torch

    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(device)
