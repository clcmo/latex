#!/usr/bin/env python3
"""Gera themes.css: a cor de destaque de cada tema, a partir de content/temas.json."""

import argparse
import re
from pathlib import Path

from site_data import carregar_temas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, help="Pasta do site gerado")
    args = parser.parse_args()

    regras = []
    for slug, tema in carregar_temas()["temas"].items():
        cor = tema["cor"]
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", cor):
            raise SystemExit(f"Cor inválida no tema '{slug}': {cor}")
        regras.append(f'[data-tema="{slug}"] {{ --tema: {cor}; --gold: {cor}; --link: {cor}; }}')

    saida = Path(args.site) / "assets" / "css" / "themes.css"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text("/* Gerado de content/temas.json */\n" + "\n".join(regras) + "\n", encoding="utf-8")
    print(f"themes.css gerado em: {saida}")


if __name__ == "__main__":
    main()
