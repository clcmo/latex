#!/usr/bin/env python3
"""Gera, para cada documento, a página que mostra o PDF e a aula em HTML."""

import argparse
import html
from pathlib import Path
from urllib.parse import quote

from site_data import carregar_temas, coletar_docs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, help="Pasta do site gerado")
    parser.add_argument("--template", required=True, help="Template viewer.html")
    args = parser.parse_args()

    site = Path(args.site)
    modelo = Path(args.template).read_text(encoding="utf-8")
    temas = carregar_temas()
    tipos = temas["tipos"]
    total = 0

    for doc in coletar_docs(site):
        nome = quote(doc["nome"], safe="")
        pagina = (
            modelo.replace("{titulo}", html.escape(doc["titulo"]))
            .replace("{tema}", doc["tema"])
            .replace("{tema_nome}", html.escape(temas["temas"][doc["tema"]]["nome"]))
            .replace("{tipo_nome}", html.escape(tipos.get(doc["tipo"], doc["tipo"])))
            .replace("{pdf}", f"../{nome}.pdf")
            .replace("{html}", f"../html/{nome}.html?embed" if doc["tem_html"] else "about:blank")
            .replace("{tex}", html.escape(doc["tex_url"]))
            .replace("{tem_html}", "1" if doc["tem_html"] else "0")
        )
        destino = site / doc["tipo"] / "ver" / f"{doc['nome']}.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")
        total += 1

    print(f"{total} visualizador(es) gerado(s) em: {site}")


if __name__ == "__main__":
    main()
