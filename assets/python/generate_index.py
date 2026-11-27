#!/usr/bin/env python3
"""Gera o índice do site, agrupado por tema, a partir do template HTML."""

import argparse
import html
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

from site_data import carregar_temas, coletar_docs


def agrupar(docs: list, temas: dict) -> dict:
    grupos = {slug: [] for slug in temas["ordem"]}
    for doc in docs:
        grupos[doc["tema"]].append(doc)
    return {slug: itens for slug, itens in grupos.items() if itens}


def build_nav(grupos: dict, temas: dict) -> str:
    return "\n      ".join(
        f'<a href="#{slug}" data-tema="{slug}">{html.escape(temas["temas"][slug]["nome"])}</a>'
        for slug in grupos
    )


def build_item(doc: dict, tipos: dict) -> str:
    nome = quote(doc["nome"], safe="")
    tipo = doc["tipo"]
    links = [f'<a class="doc-link primary" href="{tipo}/ver/{nome}.html">Abrir</a>']
    links.append(f'<a class="doc-link" href="{tipo}/{nome}.pdf" target="_blank" rel="noopener">PDF</a>')
    if doc["tem_html"]:
        links.append(f'<a class="doc-link" href="{tipo}/html/{nome}.html">HTML</a>')
    return (
        f'<li class="doc-item"><div><span class="doc-title">{html.escape(doc["titulo"])}</span>'
        f'<span class="doc-tipo">{html.escape(tipos.get(tipo, tipo))}</span></div>'
        f'<span class="doc-links">{"".join(links)}</span></li>'
    )


def build_sections(grupos: dict, temas: dict) -> str:
    if not grupos:
        return (
            '<p class="empty">Nenhum documento publicado. Adicione arquivos '
            "<code>.tex</code> em <code>src/</code>.</p>"
        )
    secoes = []
    for slug, itens in grupos.items():
        tema = temas["temas"][slug]
        lista = "\n".join(build_item(doc, temas["tipos"]) for doc in itens)
        secoes.append(
            f'<section class="index-section" id="{slug}" data-tema="{slug}">'
            f'<h2>{html.escape(tema["nome"])}</h2>'
            f'<p class="tema-desc">{html.escape(tema["descricao"])}</p>\n'
            f'<ul class="doc-list">\n{lista}\n</ul>\n</section>'
        )
    return "\n".join(secoes)


def build_slides(grupos: dict, temas: dict) -> str:
    slides = []
    for slide in temas["apresentacao"]:
        if slide.get("especial") == "temas":
            itens = [
                f'{temas["temas"][slug]["nome"]}: {temas["temas"][slug]["descricao"]} ({len(docs)})'
                for slug, docs in grupos.items()
            ]
            slide = {"titulo": slide["titulo"], "itens": itens}
        slides.append(slide)
    return json.dumps(slides, ensure_ascii=False).replace("</", "<\\/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, help="Pasta do site gerado")
    parser.add_argument("--output", required=True, help="Caminho do index.html")
    parser.add_argument("--template", required=True, help="Template index.html")
    args = parser.parse_args()

    temas = carregar_temas()
    grupos = agrupar(coletar_docs(Path(args.site)), temas)
    modelo = Path(args.template).read_text(encoding="utf-8")

    saida = (
        modelo.replace("{descricao}", html.escape(temas["projeto"]["descricao"]))
        .replace("{nav_links}", build_nav(grupos, temas))
        .replace("{sections}", build_sections(grupos, temas))
        .replace("{slides_json}", build_slides(grupos, temas))
        .replace("{date}", datetime.now().strftime("%d/%m/%Y %H:%M"))
    )
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    Path(args.output).write_text(saida, encoding="utf-8")
    print(f"index.html gerado em: {args.output}")


if __name__ == "__main__":
    main()
