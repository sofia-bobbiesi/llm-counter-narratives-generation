"""
Biblioteca de prompts para la generación de contra-narrativas contra el discurso
de odio, basada en la guía:

    "Legal Prompts: guía práctica de instrucciones para uso de IA generativa"
    Agostina Jara Rey — UBA IALAB, Agosto 2024.

El objetivo de este archivo es centralizar, de forma fácilmente editable, los
prompts que se usan para explorar las respuestas del modelo ante tweets de odio.

Estructura de cada entrada:
    - tecnica:            referencia a la sección de la guía.
    - descripcion:        qué hace el prompt y cuándo conviene usarlo.
    - requiere_ejemplos:  bool, si necesita ejemplos few-shot.
    - modo:               "chat" (usa mensaje de sistema) o "texto" (plano).
    - system:             mensaje de sistema opcional (solo modo "chat").
    - plantilla:          texto con placeholders.

Placeholders disponibles:
    {tweet}            -> el tweet de odio a responder.
    {contra_ejemplo}   -> contra-narrativa de ejemplo (one-shot).
    {ejemplos}         -> bloque de ejemplos "Tweet: ... Respuesta: ..." (few-shot).
    {colectivo}        -> colectivo atacado (info argumentativa).
    {propiedad}        -> propiedad asociada al colectivo.
    {conclusion}       -> conclusión del tweet (info argumentativa).
"""

SYSTEM_ROLE = (
    "Actuás como un operario de una ONG experto en generación de "
    "contra-narrativas y contra-discurso contra el discurso de odio. Hablás "
    "únicamente en español y no podés generar texto en otro idioma. Tu tarea es "
    "responder a tweets de odio con contra-narrativas respetuosas y "
    "argumentativas: no seas agresivo ni abusivo, no difundas odio, tratá de "
    "desescalar la conversación, respondé pensando en una audiencia más amplia "
    "que quien publicó el tweet y construí una narrativa. No incites al odio ni "
    "repliques el discurso agresivo. No aclares que sos un modelo de lenguaje ni "
    "te niegues a asumir el rol."
)

# Restricción de salida compartida por todas las técnicas: evita respuestas
# "meta" (varias opciones, títulos, markdown) y fuerza una única contra-narrativa.
OUTPUT_CONSTRAINTS = (
    "Respondé únicamente con la contra-narrativa: una o dos oraciones, sin títulos, "
    "listas, opciones alternativas, explicaciones ni comentarios, sin repetir el tweet "
    "y sin usar formato Markdown."
)

# Instrucción para usar la información argumentativa inyectada tras '|'.
ARG_INFO_NOTE = (
    "El tweet incluye, tras '|', información sobre su estructura argumentativa "
    "(colectivo, propiedad, justificación, conclusión, pivote); usala para elaborar "
    "la respuesta y no la reproduzcas literalmente."
)

PROMPTS = {
    "system_message": {
        "tecnica": "A. System message",
        "descripcion": (
            "Configura al modelo con un rol, idioma y límites para toda la "
            "interacción. No es un prompt de generación en sí, sino un mensaje "
            "de sistema que puede combinarse con el resto de las técnicas."
        ),
        "requiere_ejemplos": False,
        "modo": "chat",
        "system": SYSTEM_ROLE,
        "plantilla": "Generá una contra-narrativa en español para el siguiente tweet de odio: {tweet}",
    },
    "zero_shot": {
        "tecnica": "B. Zero shot prompting",
        "descripcion": (
            "Instrucción directa, sin ejemplos ni contexto previo. Ideal para "
            "respuestas rápidas y para dejar margen a respuestas creativas."
        ),
        "requiere_ejemplos": False,
        "modo": "texto",
        "system": None,
        "plantilla": (
            "Escribe una contra-narrativa en español, respetuosa y argumentativa, "
            "para responder al siguiente tweet de odio: {tweet}"
        ),
    },
    "one_shot": {
        "tecnica": "C. One shot prompting",
        "descripcion": (
            "Aporta un único ejemplo de contra-narrativa para guiar el estilo, "
            "tono y formato de la salida, sin dejarlo librado a la creatividad "
            "del modelo."
        ),
        "requiere_ejemplos": False,
        "modo": "texto",
        "system": None,
        "plantilla": (
            "A continuación se muestra un ejemplo de contra-narrativa frente a "
            "un tweet de odio:\n"
            "Contra-narrativa de ejemplo: {contra_ejemplo}\n\n"
            "Siguiendo ese estilo y tono, genera una contra-narrativa en español "
            "para el siguiente tweet de odio: {tweet}"
        ),
    },
    "few_shot": {
        "tecnica": "D. Few shot prompting",
        "descripcion": (
            "Proporciona varios ejemplos (2-4) para que el modelo detecte el "
            "patrón de respuesta y lo replique con coherencia y precisión."
        ),
        "requiere_ejemplos": True,
        "modo": "texto",
        "system": None,
        "plantilla": (
            "A continuación se muestran varios ejemplos de cómo responder a "
            "tweets de odio con contra-narrativas:\n"
            "{ejemplos}\n\n"
            "Basándote en el patrón de esos ejemplos, genera una contra-narrativa "
            "en español para el siguiente tweet de odio: {tweet}"
        ),
    },
    "super_prompt": {
        "tecnica": "I. Super-prompt",
        "descripcion": (
            "Combina roles de varios expertos que debaten en cascada, reflejan "
            "los argumentos en un cuadro, arriban a una conclusión consensuada y "
            "luego es puesta en crisis por otros expertos."
        ),
        "requiere_ejemplos": False,
        "modo": "chat",
        "system": SYSTEM_ROLE,
        "plantilla": (
            "Necesito que actúes como tres expertos: dos operarios de una ONG y "
            "un especialista en derechos humanos. Deberán debatir de manera "
            "iterada cuál es la mejor contra-narrativa para el siguiente tweet de "
            "odio: {tweet}. Reflejá los argumentos de cada uno en un cuadro. Luego "
            "arriben a una conclusión consensuada con una única contra-narrativa "
            "elegida y elaboren una matriz conceptual. Por último, que otros tres "
            "expertos pongan en crisis los argumentos y la conclusión de los "
            "anteriores y propongan una versión final. El límite máximo es de 100 "
            "palabras."
        ),
    },
    "tam": {
        "tecnica": "J. TAM (Tarea, Acción y Meta)",
        "descripcion": (
            "Estructura el prompt en Tarea, Acción y Meta para orientarlo a un "
            "objetivo concreto y con pasos específicos."
        ),
        "requiere_ejemplos": False,
        "modo": "texto",
        "system": None,
        "plantilla": (
            "TAREA: generar una contra-narrativa contra un tweet de odio.\n"
            "ACCIÓN: identificá el colectivo atacado y redactá una respuesta "
            "argumentativa en español, sin incitar al odio.\n"
            "META: una contra-narrativa respetuosa que desmonte el discurso de "
            "odio del siguiente tweet: {tweet}"
        ),
    },
    "care": {
        "tecnica": "L. CARE (Contexto, Acción, Resultado y Ejemplo)",
        "descripcion": (
            "Proporciona contexto, acción, resultado esperado y un ejemplo "
            "concreto como guía y referencia para alinear la respuesta."
        ),
        "requiere_ejemplos": False,
        "modo": "texto",
        "system": None,
        "plantilla": (
            "CONTEXTO: sos un operario de una ONG experto en contra-narrativas "
            "contra el discurso de odio.\n"
            "ACCIÓN: proponé una contra-narrativa argumentativa en español para "
            "el siguiente tweet de odio: {tweet}\n"
            "RESULTADO: una respuesta que desmonte el odio sin replicarlo ni "
            "incitar a la violencia.\n"
            "EJEMPLO: {contra_ejemplo}"
        ),
    },
}

# Instrucciones de estrategia por tipo de contra-narrativa (guía, sección 6).
# Se combinan con cualquier técnica de prompt: según `cn_strategy` se anexa la
# instrucción correspondiente a la plantilla elegida.
#
# Claves "a"/"b"/"c": tipo con información argumentativa (el tweet llega con los
# componentes tras "|"), por lo que la instrucción los referencia.
# Claves "a_no_info"/"b_no_info"/"c_no_info": mismo tipo y estrategia, pero sin
# información inyectada; el modelo debe identificar los componentes por sí mismo.
CN_TYPE_INSTRUCTIONS = {
    "a": (
        "La contra-narrativa debe negar la relación entre la justificación y la "
        "conclusión del tweet. Usá la justificación y la conclusión indicadas "
        "(tras '|') para construir tu respuesta, sin reproducirlas literalmente."
    ),
    "b": (
        "La contra-narrativa debe negar la relación entre el colectivo atacado y "
        "las propiedades o consecuencias que se le asocian. Usá el colectivo y la "
        "propiedad indicados (tras '|') para construir tu respuesta, sin "
        "reproducirlos literalmente."
    ),
    "c": (
        "La contra-narrativa debe refutar la justificación del tweet. Si la "
        "justificación es un hecho (fact), ponelo en duda o pedí fuentes; si es "
        "una opinión (value), destacá que es subjetiva y relativizala; si es una "
        "política (policy), proponé una política contraria. Usá la justificación "
        "indicada (tras '|') para construir tu respuesta, sin reproducirla "
        "literalmente."
    ),
    "a_no_info": (
        "La contra-narrativa debe negar la relación entre la justificación y la "
        "conclusión del tweet. Identificá la justificación y la conclusión "
        "directamente en el texto del tweet."
    ),
    "b_no_info": (
        "La contra-narrativa debe negar la relación entre el colectivo atacado y "
        "las propiedades o consecuencias que se le asocian. Identificá el "
        "colectivo y las propiedades directamente en el texto del tweet."
    ),
    "c_no_info": (
        "La contra-narrativa debe refutar la justificación del tweet. Si la "
        "justificación es un hecho (fact), ponelo en duda o pedí fuentes; si es "
        "una opinión (value), destacá que es subjetiva y relativizala; si es una "
        "política (policy), proponé una política contraria. Identificá la "
        "justificación y su tipo directamente en el texto del tweet."
    ),
    "": "",
}

# Técnicas de la guía que NO se incluyen como plantilla única y por qué.
OMITIDAS = {
    "E. Break the task down": (
        "No es una plantilla única sino un flujo de trabajo: se divide la tarea "
        "en varios prompts secuenciales (p. ej. 1) identificar el colectivo "
        "atacado, 2) generar la contra-narrativa). Requiere orquestar más de una "
        "llamada al modelo, por lo que no encaja en una única entrada de este "
        "diccionario."
    ),
    "F. Chain of thought (cadena de pensamientos)": (
        "Solicita al modelo que razone paso a paso. Para esta tarea corre el "
        "riesgo de que el 'razonamiento' intermedio se filtre en la salida en "
        "lugar de la contra-narrativa final. Puede habilitarse agregando 'pensá "
        "paso a paso' a alguna plantilla si se busca auditar la coherencia."
    ),
    "G. Prompt de conocimiento integrado": (
        "Consiste en aportar conocimiento externo al modelo. En este proyecto ya "
        "se cubre mediante la información argumentativa (colectivo, propiedad, "
        "conclusión) que inyecta `use_extra_info` en el pipeline, por lo que no "
        "se duplica como plantilla independiente."
    ),
    "H. Skeleton-of-thought": (
        "Implica dos pasos: primero pedir un esquema/eje del texto y luego "
        "completarlo. Como es un proceso en dos iteraciones, no es una plantilla "
        "única y queda fuera de este diccionario."
    ),
    "K. ADP (Antes, Después y Puente)": (
        "Está orientada a planificar la transición de una situación actual a una "
        "deseada (p. ej. modernización de un Poder Judicial), no a la generación "
        "de texto argumentativo, por lo que no resulta aplicable a esta tarea."
    ),
}

BUENAS_PRACTICAS = [
    "Verificar la respuesta: el contenido puede ser correcto o una alucinación.",
    "Anonimizar ejemplos con datos personales antes de usarlos en few-shot.",
    "Documentar y reutilizar los prompts que resulten efectivos.",
    "Ajustar el prompt de forma iterativa según los resultados obtenidos.",
]
