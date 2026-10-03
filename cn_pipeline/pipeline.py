"""Orquestación de un experimento completo.

Un experimento consiste en: cargar datos -> cargar modelo -> generar
contra-narrativas con las técnicas de prompt seleccionadas -> evaluar con
métricas automáticas (y LLM-as-judge si está configurado) -> guardar resultados.

Puede ejecutarse desde la notebook (`run_experiment`) o desde la línea de
comandos (`python -m cn_pipeline.pipeline --config configs/config_gemma.json ...`).
"""

from __future__ import annotations

import os
import random
from dataclasses import asdict
from typing import Optional

import numpy as np
import torch

from .config import (
    Config,
    QUANTIZATION_MODES,
    build_parser,
    load_config,
    apply_overrides,
    resolve_device,
    save_config,
)
from .data import CN_STRATEGIES, load_data, sample_examples, sample_counter_narrative
from .evaluation import evaluate_predictions, get_references
from .generation import Generator, add_arg_info, build_prompt
from .llm_judge import build_judge, judge_rows
from .prompts import PROMPTS, CN_TYPE_INSTRUCTIONS


def set_seed(seed: int) -> None:
    """Fija las semillas para reproducibilidad."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def experiment_id(cfg: Config) -> str:
    """Identificador legible del experimento, usado para el directorio de salida."""
    model = cfg.model_name.split("/")[-1]
    extra = cfg.use_extra_info or "no-info"
    cn = cfg.cn_strategy or "no-strategy"
    return f"{model}_{cfg.language}_{extra}_{cn}_seed{cfg.seed}"


def run_experiment(cfg: Config):
    """Ejecuta el experimento descrito por `cfg`.

    Devuelve (detallado, resumen, directorio de salida).
    """
    set_seed(cfg.seed)
    device = resolve_device(cfg.device)
    print(f"[pipeline] device={device}, dtype={cfg.torch_dtype}")

    # 0. Juez (obligatorio): valida modelo y clave, y falla temprano si faltan.
    judge = build_judge(cfg.llm_judge)
    print(f"[pipeline] LLM-as-judge: {cfg.llm_judge.model}")

    # 1. Datos.
    test, train, val = load_data(cfg.use_extra_info, cfg.cn_strategy)
    print(f"[pipeline] test={len(test)}, train={len(train)}, val={len(val)}")

    # 2. Subconjunto de test (si max_samples está definido).
    if cfg.max_samples is not None and len(test) > cfg.max_samples:
        rng = np.random.RandomState(cfg.seed)
        indices = rng.choice(len(test), size=cfg.max_samples, replace=False)
        test = [test[i] for i in indices]

    # 3. Ejemplos para few-shot / one-shot / CARE.
    needs_examples = any(PROMPTS[p].get("requiere_ejemplos") for p in cfg.prompt_types)
    needs_counter = any(
        "{contra_ejemplo}" in PROMPTS[p]["plantilla"] for p in cfg.prompt_types
    )
    examples: Optional[list] = None
    if needs_examples:
        examples = sample_examples(train, val, cfg.fewshot_examples, cfg.seed)
    counter_example: Optional[str] = None
    if needs_counter:
        counter_example = sample_counter_narrative(train, val, cfg.seed)

    # 4. Modelo.
    generator = Generator(
        cfg.model_name,
        device,
        asdict(cfg.generation),
        torch_dtype=cfg.torch_dtype,
        quantization=cfg.quantization,
    )

    # 5. Generación.
    tipo_instruccion = CN_TYPE_INSTRUCTIONS.get(cfg.cn_strategy, "")
    rows = []
    for sample in test:
        tweet = sample["hateSpeech"]
        tweet_input = add_arg_info(sample.get("extra_info", {}), tweet)
        for prompt_type in cfg.prompt_types:
            prompt = build_prompt(
                prompt_type,
                tweet_input,
                examples=examples,
                counter_example=counter_example,
                tipo_instruccion=tipo_instruccion,
            )
            generated = generator.generate(prompt)
            rows.append(
                {
                    "hate_speech": tweet,
                    "true_cn": sample["counterSpeech"],
                    "prompt_type": prompt_type,
                    "generated_cn": generated,
                }
            )
    print(f"[pipeline] generadas {len(rows)} contra-narrativas")

    # 6. Evaluación (métricas automáticas + LLM-as-judge).
    print("[pipeline] evaluando con LLM-as-judge...")
    rows = judge_rows(judge, rows)

    detailed, summary = evaluate_predictions(rows, metrics=cfg.metrics)

    # 7. Guardar resultados.
    exp_id = experiment_id(cfg)
    out_dir = os.path.join(cfg.output_dir, exp_id)
    os.makedirs(out_dir, exist_ok=True)

    detailed_path = os.path.join(out_dir, "results.csv")
    summary_path = os.path.join(out_dir, "summary.csv")
    config_path = os.path.join(out_dir, "config.json")
    anecdotal_path = os.path.join(out_dir, "anecdotal.txt")

    detailed.to_csv(detailed_path, index=False)
    summary.to_csv(summary_path, index=False)
    save_config(cfg, config_path)
    _save_anecdotal(rows, anecdotal_path)

    print(f"[pipeline] resultados en {out_dir}/")
    print(summary.to_markdown(index=False))
    return detailed, summary, out_dir


def _save_anecdotal(rows, path: str) -> None:
    """Guarda un volcado legible para revisión anecdótica (a ojo)."""
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write("=" * 72 + "\n")
            f.write(f"[{row['prompt_type']}] odio: {row['hate_speech']}\n")
            for ref in get_references(row["true_cn"]):
                f.write(f"referencia: {ref}\n")
            f.write(f"generado:   {row['generated_cn']}\n")


def main(argv=None) -> None:
    """Punto de entrada CLI: `python -m cn_pipeline.pipeline ...`."""
    parser = build_parser()
    args = parser.parse_args(argv)

    cfg = load_config(args.config) if args.config else Config()
    cfg = apply_overrides(cfg, args)

    # Validación de técnicas solicitadas.
    unknown = [p for p in cfg.prompt_types if p not in PROMPTS]
    if unknown:
        raise ValueError(
            f"Técnicas de prompt desconocidas: {unknown}. Disponibles: {list(PROMPTS)}"
        )

    # Validación de la estrategia de tipo de contra-narrativa.
    if cfg.cn_strategy not in CN_STRATEGIES:
        raise ValueError(
            f"cn_strategy desconocida: {cfg.cn_strategy!r}. "
            f"Disponibles: {list(CN_STRATEGIES)}"
        )

    # Validación del modo de cuantización.
    if cfg.quantization not in QUANTIZATION_MODES:
        raise ValueError(
            f"quantization desconocida: {cfg.quantization!r}. "
            f"Disponibles: {list(QUANTIZATION_MODES)}"
        )

    run_experiment(cfg)


if __name__ == "__main__":
    main()
