"""Carga y preparación del dataset ASOHMO."""

from __future__ import annotations

import random
from glob import glob
from typing import List

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


# Flags internos de `resolve_extra_info` que sí inyectan información argumentativa.
INFO_FLAGS = ("collective", "premises", "all", "cn_a", "cn_b", "cn_c")


def injects_info(use_extra_info: str, cn_strategy: str) -> bool:
    """Indica si la configuración inyecta información argumentativa en el tweet."""
    return resolve_extra_info(use_extra_info, cn_strategy) in INFO_FLAGS


def parse_dataset(filenames, use_extra_info=""):
    """Parsea los `.conll` (argumentación) y `.cn` (contra-narrativas).

    Devuelve `(cns_by_tweet, nonargs, cn_length, cn_type_not_present)`.
    """
    cns_by_tweet = {}
    nonargs = 0
    cn_length = 0
    cn_type_not_present = 0
    for filename in glob(filenames):
        tweet_list = []
        is_arg = True
        type_just = ""
        type_conc = ""
        need_collective = (
            use_extra_info == "collective"
            or use_extra_info == "all"
            or use_extra_info == "cn_a"
            or use_extra_info == "cn_b"
        )
        need_premises = (
            use_extra_info == "premises"
            or use_extra_info == "all"
            or use_extra_info == "cn_c"
            or use_extra_info == "cn_a"
        )
        if need_collective:
            collective = []
            consecutive_collective = False
            property = []
            consecutive_property = False
        if need_premises:
            justification = []
            consecutive_just = False
            conclusion = []
            consecutive_conc = False
            pivot = []
            consecutive_pivot = False
        prev_line = ["", "", "", "", "", "", "", "", ""]
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                splitted_line = line.split("\t")
                if splitted_line[1].startswith("NoArgumentative"):
                    is_arg = False
                    break
                if splitted_line[4].startswith("Collective") and need_collective:
                    if not prev_line[4].startswith("Collective") and consecutive_collective:
                        collective.append(" - ")
                    collective.append(splitted_line[0])
                    consecutive_collective = True
                if splitted_line[5].startswith("Property") and need_collective:
                    if not prev_line[5].startswith("Property") and consecutive_property:
                        property.append(" - ")
                    property.append(splitted_line[0])
                    consecutive_property = True
                if splitted_line[2].startswith("Premise2Justification") and need_premises:
                    if not prev_line[2].startswith("Premise2Justification") and consecutive_just:
                        justification.append(" - ")
                    justification.append(splitted_line[0])
                    consecutive_just = True
                if splitted_line[3].startswith("Premise1Conclusion") and need_premises:
                    if not prev_line[3].startswith("Premise1Conclusion") and consecutive_conc:
                        conclusion.append(" - ")
                    conclusion.append(splitted_line[0])
                    consecutive_conc = True
                if splitted_line[6].startswith("pivot") and need_premises:
                    if not prev_line[6].startswith("pivot") and consecutive_pivot:
                        pivot.append(" - ")
                    pivot.append(splitted_line[0])
                    consecutive_pivot = True
                if (not splitted_line[7].startswith("O")) and need_premises:
                    type_just = splitted_line[7].strip()
                if (not splitted_line[8].startswith("O")) and need_premises:
                    type_conc = splitted_line[8].strip()

                tweet_list.append(splitted_line[0])
                prev_line = splitted_line
        if not is_arg:
            nonargs += 1
            continue
        tweet = " ".join(tweet_list)
        number = filename.split("_")[-1].replace(".conll", "")
        extra_info = {"number": number}
        if need_collective:
            extra_info["collective"] = " ".join(collective)
            extra_info["property"] = " ".join(property)
        if need_premises:
            extra_info["justification"] = " ".join(justification) + " (" + type_just + ") "
            extra_info["conclusion"] = " ".join(conclusion) + " (" + type_conc + ") "
            extra_info["pivot"] = " ".join(pivot)

        counternarratives = []
        cn_not_present = False
        with open(filename.replace("conll", "cn"), "r", encoding="utf-8") as cn:
            if use_extra_info.startswith("cn_"):
                cn_not_present = False
            for idx, line in enumerate(cn):
                if use_extra_info in ("cn_a", "cn_a_no_info"):
                    if idx == 0:
                        if line.replace("\n", "").strip() != "":
                            counternarratives.append(line)
                        else:
                            cn_not_present = True
                elif use_extra_info in ("cn_b", "cn_b_no_info"):
                    if idx == 1:
                        if line.replace("\n", "").strip() != "":
                            counternarratives.append(line)
                        else:
                            cn_not_present = True
                elif use_extra_info in ("cn_c", "cn_c_no_info"):
                    if idx == 2:
                        if line.replace("\n", "").strip() != "":
                            counternarratives.append(line)
                        else:
                            cn_not_present = True
                else:
                    if line.replace("\n", "").strip() != "":
                        counternarratives.append(line)
        if tweet in cns_by_tweet:
            cns_by_tweet[tweet]["cns"] += counternarratives
        else:
            if use_extra_info.startswith("cn_") and cn_not_present:
                cn_type_not_present += 1
            else:
                cns_by_tweet[tweet] = {
                    "cns": counternarratives,
                    "lang": "spanish",
                    "extra_info": extra_info,
                }
        cn_length += len(counternarratives)
        if use_extra_info.startswith("cn_") and len(counternarratives) > 1:
            raise ValueError(
                f"Error parsing the data: Expected at most one counternarrative for {use_extra_info}, "
                f"but found {len(counternarratives)}. Check the file {filename} for inconsistencies."
            )
    return cns_by_tweet, nonargs, cn_length, cn_type_not_present


def load_asohmo(use_extra_info="", finetuning=False):
    """Carga las particiones test/train/dev y devuelve `[test, train, val]`."""
    test_cns, _, _, _ = parse_dataset(
        "dataset/ASOHMO/spanish/test/*.conll", use_extra_info=use_extra_info
    )
    train_cns, _, _, _ = parse_dataset(
        "dataset/ASOHMO/spanish/train/*.conll", use_extra_info=use_extra_info
    )
    val_cns, _, _, _ = parse_dataset(
        "dataset/ASOHMO/spanish/dev/*.conll", use_extra_info=use_extra_info
    )

    test_dataset = []
    train_dataset = []
    val_dataset = []
    keys = sorted(test_cns.keys())
    random.seed(42)
    random.shuffle(keys)
    for key in keys:
        # Con fine-tuning se genera un ejemplo por contra-narrativa; si no, todas
        # las contra-narrativas del tweet quedan juntas en una lista.
        if finetuning:
            for cn in test_cns[key]["cns"]:
                test_dataset.append(
                    {
                        "hateSpeech": key,
                        "extra_info": test_cns[key]["extra_info"],
                        "counterSpeech": cn,
                        "language": test_cns[key]["lang"],
                    }
                )
        else:
            test_dataset.append(
                {
                    "hateSpeech": key,
                    "extra_info": test_cns[key]["extra_info"],
                    "counterSpeech": test_cns[key]["cns"],
                    "language": test_cns[key]["lang"],
                }
            )

    for key in train_cns:
        for cn in train_cns[key]["cns"]:
            train_dataset.append(
                {
                    "hateSpeech": key,
                    "extra_info": train_cns[key]["extra_info"],
                    "counterSpeech": cn,
                    "language": train_cns[key]["lang"],
                }
            )
    for key in val_cns:
        for cn in val_cns[key]["cns"]:
            val_dataset.append(
                {
                    "hateSpeech": key,
                    "extra_info": val_cns[key]["extra_info"],
                    "counterSpeech": cn,
                    "language": val_cns[key]["lang"],
                }
            )
    return [test_dataset, train_dataset, val_dataset]


def load_data(use_extra_info: str = "", cn_strategy: str = ""):
    """Carga las particiones test/train/dev de ASOHMO.

    Devuelve una tupla `(test, train, val)` de listas de diccionarios con claves
    `hateSpeech`, `counterSpeech`, `extra_info` y `language`.
    """
    extra_info = resolve_extra_info(use_extra_info, cn_strategy)
    test, train, val = load_asohmo(use_extra_info=extra_info, finetuning=False)
    return test, train, val


def sample_examples(train: List[dict], val: List[dict], n: int, seed: int,
                    nested: bool = False) -> List[dict]:
    """Muestrea `n` ejemplos (tweet + contra-narrativa) de train+val para few-shot.

    Con `nested=True` se mezcla todo el pool una vez (seed fija) y se toman los
    primeros `n`, de modo que los conjuntos son anidados (n=1 ⊂ n=3 ⊂ n=5 ...).
    Es el modo usado por las curvas de few-shot para aislar el efecto de la
    cantidad de ejemplos.
    """
    pool = train + val
    rng = random.Random(seed)
    if nested:
        return rng.sample(pool, len(pool))[:n]
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
