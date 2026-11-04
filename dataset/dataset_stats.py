"""Estadísticas del corpus ASOHMO/CONEAS.

Recorre las anotaciones (.conll) y las contra-narrativas (.cn) de cada
partición del corpus y reporta, por partición:

    - tweets totales (archivos anotados)
    - tweets no argumentativos (se descartan: no tienen contra-narrativas)
    - tweets argumentativos (los efectivamente usados por el pipeline)
    - tweets con contra-narrativa de cada tipo (A, B y C)
    - contra-narrativas totales
    - tweets con colectivo/propiedad anotados y con pivote anotado
    - longitud promedio (en palabras) de tweets y contra-narrativas

Formato de los .conll (columnas separadas por tabulador, una por token):

    0: token            1: etiqueta BIO   2: justificación (Premise2Justification)
    3: conclusión (Premise1Conclusion)      4: colectivo (Collective)
    5: propiedad (Property)                6: pivote (pivot)
    7: tipo de la justificación (fact/value/policy)
    8: tipo de la conclusión (fact/value/policy)

Un tweet es no argumentativo si alguna de sus líneas tiene "NoArgumentative"
en la columna 1 (criterio del parser original en `cn_pipeline/data.py`).

Formato de los .cn: una línea por tipo de contra-narrativa (línea 0 = tipo A,
línea 1 = tipo B, línea 2 = tipo C), vacía si no se escribió ese tipo.

Uso:

    python3 dataset_stats.py [--root ASOHMO/spanish]

El default de --root se resuelve relativo al directorio de este script.
"""

from __future__ import annotations

import argparse
from collections import Counter
from glob import glob
from pathlib import Path

PARTITIONS = ("train", "dev", "test")

# Columna de cada componente argumentativo en los .conll.
COMPONENT_COLS = {
    "justificación": 2,
    "conclusión": 3,
    "colectivo": 4,
    "propiedad": 5,
    "pivote": 6,
}

# Índice de línea de cada tipo de contra-narrativa en los .cn.
CN_TYPE_LINES = {"A": 0, "B": 1, "C": 2}


def read_rows(conll_path: Path) -> list:
    """Devuelve las filas (listas de columnas) de un archivo .conll."""
    with open(conll_path, encoding="utf-8") as f:
        return [line.rstrip("\n").split("\t") for line in f if line.strip()]


def is_argumentative(rows: list) -> bool:
    """Determina si un tweet es argumentativo (criterio del parser original)."""
    return not any(len(r) > 1 and r[1].startswith("NoArgumentative") for r in rows)


def has_component(rows: list, col: int) -> bool:
    """Determina si algún token del tweet está anotado con el componente."""
    return any(len(r) > col and not r[col].startswith("O") for r in rows)


def read_cn_lines(cn_path: Path) -> list:
    """Devuelve las líneas (vacías incluidas) de un archivo .cn."""
    with open(cn_path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]


def stats_for_split(split: str, root: str) -> dict:
    """Calcula las estadísticas de una partición."""
    conll_files = sorted(glob(f"{root}/{split}/*.conll"))
    cn_files = sorted(glob(f"{root}/{split}/*.cn"))

    n_total = len(conll_files)
    n_nonarg = 0
    components = Counter()
    tweet_lengths = []

    for path in conll_files:
        rows = read_rows(Path(path))
        if not is_argumentative(rows):
            n_nonarg += 1
            continue
        tweet_lengths.append(len(rows))
        for name, col in COMPONENT_COLS.items():
            if has_component(rows, col):
                components[name] += 1

    cn_by_type = Counter()
    cn_lengths = []
    for path in cn_files:
        lines = read_cn_lines(Path(path))
        for cn_type, idx in CN_TYPE_LINES.items():
            if idx < len(lines) and lines[idx].strip():
                cn_by_type[cn_type] += 1
                cn_lengths.append(len(lines[idx].split()))

    average = lambda xs: round(sum(xs) / len(xs), 1) if xs else 0.0

    return {
        "tweets_totales": n_total,
        "no_argumentativos": n_nonarg,
        "argumentativos": n_total - n_nonarg,
        "cn_totales": sum(cn_by_type.values()),
        "cn_tipo_A": cn_by_type["A"],
        "cn_tipo_B": cn_by_type["B"],
        "cn_tipo_C": cn_by_type["C"],
        "con_colectivo": components["colectivo"],
        "con_propiedad": components["propiedad"],
        "con_pivote": components["pivote"],
        "tweet_palabras_prom": average(tweet_lengths),
        "cn_palabras_prom": average(cn_lengths),
    }


def print_summary(split: str, stats: dict) -> None:
    print(f"[{split}]")
    print(
        f"    tweets={stats['tweets_totales']} "
        f"(no argumentativos: {stats['no_argumentativos']}, "
        f"argumentativos: {stats['argumentativos']})"
    )
    print(
        f"    contra-narrativas: total={stats['cn_totales']} "
        f"(A: {stats['cn_tipo_A']}, B: {stats['cn_tipo_B']}, C: {stats['cn_tipo_C']})"
    )
    print(
        f"    tweets con anotado: colectivo={stats['con_colectivo']}, "
        f"propiedad={stats['con_propiedad']}, pivote={stats['con_pivote']}"
    )
    print(
        f"    longitud promedio: tweet={stats['tweet_palabras_prom']} tokens, "
        f"contra-narrativa={stats['cn_palabras_prom']} palabras"
    )
    print()


def print_markdown_table(all_stats: dict) -> None:
    headers = [
        "Partición",
        "Tweets totales",
        "No argumentativos",
        "Argumentativos",
        "CNs totales",
        "Con CN tipo A",
        "Con CN tipo B",
        "Con CN tipo C",
        "Con colectivo",
        "Con pivote",
    ]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join([" --- "] * len(headers)) + "|")
    for split, s in all_stats.items():
        row = [
            split,
            s["tweets_totales"],
            s["no_argumentativos"],
            s["argumentativos"],
            s["cn_totales"],
            s["cn_tipo_A"],
            s["cn_tipo_B"],
            s["cn_tipo_C"],
            s["con_colectivo"],
            s["con_pivote"],
        ]
        print("| " + " | ".join(str(v) for v in row) + " |")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estadísticas del corpus ASOHMO/CONEAS."
    )
    parser.add_argument(
        "--root",
        type=str,
        default=str(Path(__file__).resolve().parent / "ASOHMO" / "spanish"),
        help="Ruta a la carpeta del corpus con las particiones train/dev/test.",
    )
    args = parser.parse_args()

    all_stats = {}
    for split in PARTITIONS:
        all_stats[split] = stats_for_split(split, args.root)
        print_summary(split, all_stats[split])

    print_markdown_table(all_stats)


if __name__ == "__main__":
    main()
