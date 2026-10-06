"""Carga de modelos, armado de prompts y generación de contra-narrativas.

Responsabilidades:
    - Detectar si un modelo es de tipo chat o multimodal.
    - Construir los prompts a partir de la biblioteca `cn_pipeline.prompts`.
    - Anexar la información argumentativa al tweet.
    - Cargar tokenizer + modelo y generar/limpiar la respuesta.
"""

from __future__ import annotations

import re
from typing import Optional

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from .prompts import PROMPTS, SYSTEM_ROLE, OUTPUT_CONSTRAINTS, ARG_INFO_NOTE

# Marcadores para detectar modelos que usan formato de chat (instruct).
CHAT_MODEL_MARKERS = ("llama", "mistral", "falcon", "zephyr", "gemma", "qwen", "mixtral")

# Textos para la información argumentativa. Se usan strings planos (corrigen el
# bug de `constants.py`, que los define como `set` y renderiza llaves en el prompt).
ARG_LABELS = {
    "collective": "Colectivo contra quien se dirige el odio",
    "property": "Propiedad asociada al colectivo",
    "justification": "Justificación",
    "conclusion": "Conclusión",
    "pivot": "Pivote",
}
ARG_ORDER = ["collective", "property", "justification", "conclusion", "pivot"]


def is_chat_model(model_name: str) -> bool:
    """Determina si el modelo usa formato de chat (plantilla de mensajes)."""
    return any(marker in model_name.lower() for marker in CHAT_MODEL_MARKERS)


def is_gemma4_model(model_name: str) -> bool:
    """Determina si es un Gemma 4 (multimodal/unified, carga con AutoProcessor)."""
    return "gemma-4" in model_name.lower()


def is_mistral3_model(model_name: str) -> bool:
    """Determina si es un Ministral/Mistral 3 (Mistral3ForConditionalGeneration)."""
    name = model_name.lower()
    return "ministral-3" in name or "mistral3" in name


def add_arg_info(extra_info: dict, tweet: str) -> str:
    """Anexa la información argumentativa disponible al tweet, separada por '|'."""
    parts = [tweet]
    for key in ARG_ORDER:
        if key in extra_info and str(extra_info[key]).strip() != "":
            parts.append(f"{ARG_LABELS[key]}: {extra_info[key]}")
    return " | ".join(parts)


def format_examples(examples) -> str:
    """Formatea una lista de ejemplos como bloques 'Tweet: ... Respuesta: ...'."""
    if not examples:
        return ""
    return "\n\n".join(
        f"Tweet: {ex['hateSpeech']}\nRespuesta: {ex['counterSpeech']}" for ex in examples
    )


def build_prompt(prompt_key: str, tweet: str, examples: Optional[list] = None,
                 counter_example: Optional[str] = None,
                 tipo_instruccion: Optional[str] = None,
                 usar_info: bool = False):
    """Construye el prompt para una técnica dada.

    `tipo_instruccion` (opcional) anexa la instrucción de estrategia de
    contra-narrativa (A/B/C, ver `CN_TYPE_INSTRUCTIONS`). `usar_info` anexa la
    nota para usar la información argumentativa inyectada tras '|'. Todas las
    técnicas reciben además `OUTPUT_CONSTRAINTS` (una única contra-narrativa,
    sin títulos, listas ni markdown).

    Devuelve:
        - una lista de mensajes `[{"role": ..., "content": ...}, ...]` si la
          técnica es de modo "chat";
        - un string si es de modo "texto".
    """
    spec = PROMPTS[prompt_key]
    kwargs = {
        "tweet": tweet,
        "contra_ejemplo": counter_example or "",
        "ejemplos": format_examples(examples),
    }
    text = spec["plantilla"].format(**kwargs)
    if tipo_instruccion:
        text = f"{text}\n\n{tipo_instruccion}"
    if usar_info:
        text = f"{text}\n\n{ARG_INFO_NOTE}"
    text = f"{text}\n\n{OUTPUT_CONSTRAINTS}"
    if spec.get("modo") == "chat":
        system = spec.get("system") or SYSTEM_ROLE
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ]
    return text


def clean_response(text: str) -> str:
    """Elimina tokens residuales de la salida decodificada."""
    for token in (
        "</s>", "<s>", "<pad>", "<|eot_id|>", "<|start_header_id|>",
        "<|end_header_id|>", "<|im_end|>", "[/INST]", "<|assistant|>",
    ):
        text = text.replace(token, "")
    return text.strip()


def clean_gemma4_response(text: str) -> str:
    """Limpia la salida cruda de Gemma 4.

    Gemma 4 cierra el turno con `<turn|>` (no con `<eos>`), así que si la
    generación no se detiene ahí continúa con un segundo turno
    (`<|channel>thought\\n<channel|>` + la respuesta repetida). Se corta en el
    primer fin de turno y se quitan los marcadores de canal/turno.
    """
    for tok in ("<turn|>", "<end_of_turn>"):
        if tok in text:
            text = text.split(tok)[0]
    text = re.sub(r"<\|channel>.*?<channel\|>", "", text, flags=re.DOTALL)
    for tok in ("<|channel>", "<channel|>", "<|turn>", "<turn|>", "<eos>", "<bos>", "<pad>"):
        text = text.replace(tok, "")
    return text.strip()


def _resolve_dtype(dtype: str, device: torch.device):
    """Resuelve el `torch.dtype` a usar según configuración y dispositivo."""
    if dtype == "auto":
        return torch.float16 if device.type == "cuda" else torch.float32
    return getattr(torch, dtype)


class Generator:
    """Envuelve un modelo de lenguaje para generar contra-narrativas."""

    def __init__(self, model_name: str, device, generation_params: dict = None,
                 torch_dtype: str = "auto", quantization: str = None):
        self.model_name = model_name
        self.device = device if isinstance(device, torch.device) else torch.device(device)
        self.generation_params = dict(generation_params or {})
        self.is_chat = is_chat_model(model_name)
        self.is_gemma4 = is_gemma4_model(model_name)
        self.is_mistral3 = is_mistral3_model(model_name)
        self.quantization = quantization
        self.processor = None
        self.dtype = _resolve_dtype(torch_dtype, self.device)
        self.tokenizer = self._load_tokenizer()
        self.model = self._load_model()

    def _load_tokenizer(self):
        if self.is_gemma4:
            from transformers import AutoProcessor

            self.processor = AutoProcessor.from_pretrained(self.model_name)
            tokenizer = self.processor.tokenizer
        elif self.is_mistral3:
            # Mistral 3 usa MistralCommonBackend (requiere `mistral-common`).
            from transformers import MistralCommonBackend

            tokenizer = MistralCommonBackend.from_pretrained(self.model_name)
        else:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if not self.is_mistral3 and not getattr(tokenizer, "pad_token", None):
            tokenizer.pad_token = tokenizer.eos_token
        return tokenizer

    def _quantization_config(self):
        """Devuelve una BitsAndBytesConfig según `self.quantization` (o None)."""
        if not self.quantization:
            return None
        from transformers import BitsAndBytesConfig

        if self.quantization == "8bit":
            return BitsAndBytesConfig(load_in_8bit=True)
        if self.quantization == "4bit":
            return BitsAndBytesConfig(load_in_4bit=True)
        raise ValueError(f"quantization desconocida: {self.quantization!r}")

    def _load_model(self):
        bnb = self._quantization_config()
        if self.is_gemma4:
            # Gemma 4 es multimodal/unified: se carga con AutoModelForMultimodalLM.
            # Se usa device_map="auto" y no se mueve con .to(device) (carga directa
            # en GPU, sin pasar por CPU).
            from transformers import AutoModelForMultimodalLM

            kwargs = {"device_map": "auto"}
            if bnb is not None:
                kwargs["quantization_config"] = bnb
            else:
                kwargs["dtype"] = self.dtype
            model = AutoModelForMultimodalLM.from_pretrained(self.model_name, **kwargs)
            model.eval()
            return model
        if self.is_mistral3:
            # Mistral 3 es multimodal (vision + texto); se usa en modo texto.
            from transformers import Mistral3ForConditionalGeneration

            kwargs = {"device_map": "auto"}
            if bnb is not None:
                kwargs["quantization_config"] = bnb
            model = Mistral3ForConditionalGeneration.from_pretrained(
                self.model_name, **kwargs
            )
            model.eval()
            return model
        if bnb is not None:
            # Cuantizado: bitsandbytes + device_map="auto" (no se mueve con .to()).
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name, quantization_config=bnb, device_map="auto"
            )
            model.eval()
            return model
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name, torch_dtype=self.dtype
        )
        model.to(self.device)
        model.eval()
        return model

    def _generation_kwargs(self) -> dict:
        kwargs = dict(self.generation_params)
        kwargs.setdefault("max_new_tokens", 200)
        kwargs.setdefault("pad_token_id", self.tokenizer.pad_token_id)
        kwargs.setdefault("eos_token_id", self.tokenizer.eos_token_id)
        return kwargs

    def generate(self, prompt) -> str:
        """Genera y devuelve la contra-narrativa (solo los tokens nuevos)."""
        gen_kwargs = self._generation_kwargs()

        # Las técnicas de modo "texto" devuelven un string; los modelos de chat
        # esperan una lista de mensajes. Se normaliza como un turno de usuario.
        if (self.is_gemma4 or self.is_chat) and isinstance(prompt, str):
            prompt = [{"role": "user", "content": prompt}]

        if self.is_gemma4:
            # Detener la generación en el fin de turno de Gemma (`<turn|>`), que
            # no es el `<eos>`; si no, sigue con un segundo turno repetido.
            turn_id = self.tokenizer.convert_tokens_to_ids("<turn|>")
            if turn_id is not None and turn_id != self.tokenizer.unk_token_id:
                gen_kwargs["eos_token_id"] = [self.tokenizer.eos_token_id, turn_id]
            inputs = self.processor.apply_chat_template(
                prompt,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
                add_generation_prompt=True,
                enable_thinking=False,
            ).to(self.device)
            outputs = self.model.generate(**inputs, **gen_kwargs)
            input_len = inputs["input_ids"].shape[-1]
            raw = self.tokenizer.decode(
                outputs[0][input_len:], skip_special_tokens=False
            )
            return clean_gemma4_response(raw)

        if self.is_mistral3:
            inputs = self.tokenizer.apply_chat_template(
                prompt, return_tensors="pt", return_dict=True
            )
            inputs = {
                k: (v.to(self.device) if hasattr(v, "to") else v)
                for k, v in inputs.items()
            }
            outputs = self.model.generate(**inputs, **gen_kwargs)
            input_len = inputs["input_ids"].shape[-1]
            return clean_response(
                self.tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
            )

        if self.is_chat:
            input_ids = self.tokenizer.apply_chat_template(
                prompt, add_generation_prompt=True, return_tensors="pt"
            ).to(self.device)
            attention_mask = torch.ones_like(input_ids)
            outputs = self.model.generate(
                input_ids=input_ids, attention_mask=attention_mask, **gen_kwargs
            )
            new_tokens = outputs[0][input_ids.shape[-1]:]
            return clean_response(
                self.tokenizer.decode(new_tokens, skip_special_tokens=True)
            )

        inputs = self.tokenizer(
            prompt, return_tensors="pt", padding=True, truncation=True
        ).to(self.device)
        outputs = self.model.generate(**inputs, **gen_kwargs)

        # Descartar la parte correspondiente al prompt.
        input_len = inputs["input_ids"].shape[-1]
        return clean_response(
            self.tokenizer.decode(outputs[0][input_len:], skip_special_tokens=True)
        )
