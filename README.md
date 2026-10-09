# llm-counter-narratives-generation

Generación de contra-narrativas contra el discurso de odio mediante técnicas de *prompt-engineering* con LLMs, sobre el corpus CONEAS/ASOHMO en español.

## Estructura del repo

```
cn_pipeline/            Paquete con el pipeline
run_cross.py            Cross completo de la fase 1 (10 configs × técnicas, por modelo)
compare_experiments.py  Comparación de corridas (matrices + tests emparejados)
dataset_stats.py        Estadísticas del corpus
load_dataset.py         Parser original de ASOHMO (.conll/.cn)
configs/                Un JSON por modelo (config_gemma, config_llama, config_mistral)
dataset/ASOHMO/spanish/{test,train,dev}   Corpus
outputs/                Resultados, un directorio por corrida
```

## Instalación

```bash
pip install -r requirements.txt
```

- Requiere **GPU**. En CPU corre, pero es muy lento.
- Modelos *gated* de HuggingFace (p. ej. Llama): aceptar la licencia en la web y
  `export HF_TOKEN=hf_...` (o `huggingface-cli login`).

## Correr

```bash
# Una corrida (con juez: export LLM_JUDGE_API_KEY=<token> antes; sin red: --skip_judge)
python -m cn_pipeline.pipeline --config configs/config_gemma.json

# Cross completo de fase 1: 10 configs de info/tipo × técnicas, por modelo.
# Resumible (saltea corridas con summary.csv), sin juez, continúa ante fallos.
python run_cross.py --models gemma
# Smoke test: --prompt_types zero_shot --max_samples 2   ·   --force para re-correr

# Fase 2: juez sobre corridas ya generadas (idempotente con --resume)
export LLM_JUDGE_API_KEY=<token>
python -m cn_pipeline.judge_results --config configs/config_gemma.json \
  --run_dir outputs/gemma-4-12B-it_spanish_all_no-strategy_seed42 --resume
```

- Con juez en la corrida 1: `LLM_JUDGE_API_KEY` seteada (aborta al inicio si
  falta). Sin juez (`--skip_judge`): completar con la fase 2 después.
- Detalle del flujo en dos fases: `docs/flujo_juez_dos_fases.md`.

## Configuración

Configs en `configs/*.json`, un JSON por modelo (`config_gemma`, `config_llama`,
`config_mistral`). Campos principales: `model_name`, `prompt_types` (técnicas,
ver `cn_pipeline/prompts.py`), `cn_strategy` (`""` | `a` | `b` | `c` |
`*_no_info`), `use_extra_info` (`""` | `collective` | `premises` | `all`),
`fewshot_examples`, `seed`, `max_samples`. Todos sobrescribibles por CLI:
`python -m cn_pipeline.pipeline --help`.

## Salidas

`outputs/<modelo>_<idioma>_<info>_<cn-strategy>_seed<seed>/` con:

- `results.csv`: una fila por `<tweet, técnica>` con la generación, las
  métricas (BLEU, ROUGE-1/2/L, BERT-F1) y las columnas `judge_*` si corrió el juez.
- `summary.csv`: promedios por técnica de prompt.
- `config.json`: configuración usada (reproducibilidad).
- `anecdotal.txt`: volcado legible (ignorado por git).

## Análisis

```bash
python compare_experiments.py            # matriz técnica (x modelo) por métrica
python compare_experiments.py --paired   # + tests emparejados por tweet
python compare_experiments.py --strict   # falla si falta el juez
python dataset_stats.py                  # estadísticas del corpus
```

## Notas

- El parser del corpus y la inyección de información argumentativa se adaptan de
  [DamiFur/counter-narratives-generation](https://github.com/DamiFur/counter-narratives-generation).
- En las corridas con tipo, el juez usa la config guardada en el run dir;
  `--config` solo aporta el bloque `llm_judge` si falta.
