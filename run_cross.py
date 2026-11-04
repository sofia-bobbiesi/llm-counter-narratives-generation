"""Cross completo de la fase 1 (generación, sin juez) por modelo.

Recorre, para cada modelo elegido, las 10 configuraciones de info/tipo de
contra-narrativa (4 genéricas + 6 con tipo), cada una con las técnicas de
prompt del config base. Carga el modelo **una sola vez por modelo** y es
**resumible**: saltea las corridas que ya tienen `summary.csv`.

El juez (fase 2) se corre aparte con `cn_pipeline.judge_results`.

Uso:
    python run_cross.py                      # los tres modelos, todas las configs
    python run_cross.py --models gemma       # solo Gemma
    python run_cross.py --models gemma --force
    # smoke test rápido:
    python run_cross.py --models gemma --prompt_types zero_shot --max_samples 2
"""

from __future__ import annotations

import argparse
import copy
import os
import traceback

from cn_pipeline.config import load_config, resolve_device
from cn_pipeline.pipeline import (
    build_generator,
    experiment_id,
    finalize_experiment,
    generate_rows,
    prepare_experiment,
)

# Dimensión "info/tipo": (use_extra_info, cn_strategy).
# En las corridas con tipo, use_extra_info se ignora (lo sobreescribe data.resolve_extra_info).
GENERIC = [("", ""), ("collective", ""), ("premises", ""), ("all", "")]
TYPED = [("", cs) for cs in ("a", "b", "c", "a_no_info", "b_no_info", "c_no_info")]
CROSS = GENERIC + TYPED

DEFAULT_MODELS = ("gemma", "llama", "mistral")


def run_model(model_key: str, args) -> dict:
    """Corre las 10 configuraciones de un modelo. Devuelve conteos ok/skip/fail."""
    base = load_config(f"configs/config_{model_key}.json")
    base.seed = args.seed
    base.output_dir = os.path.join(args.outputs, base.model_name.split("/")[-1])
    if args.max_samples is not None:
        base.max_samples = args.max_samples
    if args.prompt_types:
        base.prompt_types = [s.strip() for s in args.prompt_types.split(",") if s.strip()]

    device = resolve_device(base.device)
    generator = None
    counts = {"ok": 0, "skip": 0, "fail": 0}

    for use_extra_info, cn_strategy in CROSS:
        cfg = copy.deepcopy(base)
        cfg.use_extra_info = use_extra_info
        cfg.cn_strategy = cn_strategy
        exp_id = experiment_id(cfg)
        summary_path = os.path.join(cfg.output_dir, exp_id, "summary.csv")
        tag = f"{model_key} cn_strategy={cn_strategy or '-'} use_extra_info={use_extra_info or '-'}"

        if not args.force and os.path.isfile(summary_path):
            print(f"[cross] skip {tag} -> {exp_id}")
            counts["skip"] += 1
            continue

        if generator is None:
            print(f"[cross] cargando modelo {base.model_name} ...")
            generator = build_generator(base, device)

        print(f"[cross] run  {tag} -> {exp_id}")
        try:
            _, test, examples, counter_example = prepare_experiment(cfg, device)
            rows = generate_rows(cfg, test, examples, counter_example, generator)
            finalize_experiment(cfg, rows)  # fase 1: sin juez
            counts["ok"] += 1
        except Exception:
            print(f"[cross] FALLO {tag}")
            traceback.print_exc()
            counts["fail"] += 1

    return counts


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Cross completo de la fase 1 (generación, sin juez)."
    )
    parser.add_argument(
        "--models", type=str, default=",".join(DEFAULT_MODELS),
        help="Modelos a correr, separados por coma (gemma,llama,mistral).",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_samples", type=int, default=None,
                        help="Acota tweets de test (smoke test).")
    parser.add_argument("--prompt_types", type=str, default=None,
                        help="Técnicas a correr, separadas por coma (smoke test).")
    parser.add_argument("--outputs", type=str, default="outputs")
    parser.add_argument("--force", action="store_true",
                        help="Re-corre aunque ya exista summary.csv.")
    args = parser.parse_args(argv)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    total = {"ok": 0, "skip": 0, "fail": 0}
    for model_key in models:
        print(f"\n[cross] === modelo {model_key} ===")
        counts = run_model(model_key, args)
        for key in total:
            total[key] += counts[key]

    print(f"\n[cross] fin: ok={total['ok']} skip={total['skip']} fail={total['fail']}")


if __name__ == "__main__":
    main()
