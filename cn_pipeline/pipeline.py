"""Orquestación de un experimento completo.

Un experimento consiste en: cargar datos -> cargar modelo -> generar
contra-narrativas con las técnicas de prompt seleccionadas -> evaluar con
métricas automáticas (y LLM-as-judge si está configurado) -> guardar resultados.

Se ejecuta desde la línea de comandos
(`python -m cn_pipeline.pipeline --config configs/config_gemma.json ...`) o
invocando `run_experiment` desde otro script. Para el barrido completo de
configuraciones, usar `run_cross.py` en la raíz del repo.
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
from .data import CN_STRATEGIES, injects_info, load_data, sample_examples, sample_counter_narrative
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


def build_generator(cfg: Config, device=None) -> Generator:
    """Carga el modelo/tokenizer de `cfg` (reutilizable entre corridas del mismo modelo)."""
    if device is None:
        device = resolve_device(cfg.device)
    return Generator(
        cfg.model_name,
        device,
        asdict(cfg.generation),
        torch_dtype=cfg.torch_dtype,
        quantization=cfg.quantization,
    )


def prepare_experiment(cfg: Config, device=None):
    """Fija la semilla y prepara datos, ejemplos few-shot/one-shot y contra-ejemplo.

    Devuelve `(device, test, examples, counter_example)`.
    """
    set_seed(cfg.seed)
    if device is None:
        device = resolve_device(cfg.device)

    test, train, val = load_data(cfg.use_extra_info, cfg.cn_strategy)
    print(f"[pipeline] test={len(test)}, train={len(train)}, val={len(val)}")

    if cfg.max_samples is not None and len(test) > cfg.max_samples:
        rng = np.random.RandomState(cfg.seed)
        indices = rng.choice(len(test), size=cfg.max_samples, replace=False)
        test = [test[i] for i in indices]

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

    return device, test, examples, counter_example


def generate_rows(cfg: Config, test, examples, counter_example, generator: Generator) -> list:
    """Genera las contra-narrativas para `test` con `cfg.prompt_types`."""
    tipo_instruccion = CN_TYPE_INSTRUCTIONS.get(cfg.cn_strategy, "")
    usar_info = injects_info(cfg.use_extra_info, cfg.cn_strategy)
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
                usar_info=usar_info,
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
    return rows


def finalize_experiment(cfg: Config, rows, run_judge: bool = False, judge=None):
    """Evalúa (juez opcional + métricas) y guarda los resultados de `cfg`."""
    if run_judge:
        print("[pipeline] evaluando con LLM-as-judge...")
        rows = judge_rows(judge, rows, retries=3)

    detailed, summary = evaluate_predictions(rows, metrics=cfg.metrics)

    exp_id = experiment_id(cfg)
    out_dir = os.path.join(cfg.output_dir, exp_id)
    os.makedirs(out_dir, exist_ok=True)

    detailed.to_csv(os.path.join(out_dir, "results.csv"), index=False)
    summary.to_csv(os.path.join(out_dir, "summary.csv"), index=False)
    save_config(cfg, os.path.join(out_dir, "config.json"))
    _save_anecdotal(rows, os.path.join(out_dir, "anecdotal.txt"))

    print(f"[pipeline] resultados en {out_dir}/")
    print(summary.to_markdown(index=False))
    return detailed, summary, out_dir


def run_experiment(cfg: Config, run_judge: bool = True):
    """Ejecuta el experimento descrito por `cfg`.

    Si `run_judge=False` (p. ej. en un nodo sin red) se omite el LLM-as-judge;
    las columnas `judge_*` quedan ausentes y pueden completarse luego con
    `cn_pipeline.judge_results`.

    Devuelve (detallado, resumen, directorio de salida).
    """
    device = resolve_device(cfg.device)
    print(f"[pipeline] device={device}, dtype={cfg.torch_dtype}")

    # Juez (obligatorio a nivel workflow): valida modelo y clave temprano.
    judge = None
    if run_judge:
        judge = build_judge(cfg.llm_judge)
        print(f"[pipeline] LLM-as-judge: {cfg.llm_judge.model}")
    else:
        print(
            "[pipeline] LLM-as-judge: omitido (--skip_judge). "
            "Completar luego con `python -m cn_pipeline.judge_results`."
        )

    _, test, examples, counter_example = prepare_experiment(cfg, device)
    generator = build_generator(cfg, device)
    rows = generate_rows(cfg, test, examples, counter_example, generator)
    return finalize_experiment(cfg, rows, run_judge=run_judge, judge=judge)


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

    run_experiment(cfg, run_judge=not args.skip_judge)


if __name__ == "__main__":
    main()
