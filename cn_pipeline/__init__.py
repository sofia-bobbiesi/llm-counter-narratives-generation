"""Paquete `cn_pipeline`: pipeline de generación de contra-narrativas contra el
discurso de odio mediante técnicas de prompt-engineering.

Módulos:
    config      -- configuración de experimentos (dataclass, loader, CLI).
    prompts     -- biblioteca de prompts (basada en la guía Legal Prompts).
    data        -- carga y preparación del dataset ASOHMO.
    generation  -- carga de modelos, armado de prompts y generación.
    evaluation  -- métricas automáticas (BLEU/ROUGE/BERTScore).
    llm_judge   -- evaluación LLM-as-judge (métrica obligatoria).
    pipeline    -- orquestación de un experimento completo.
"""

__version__ = "0.1.0"
