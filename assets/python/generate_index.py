#!/usr/bin/env python3
"""Generate the document index from the HTML template and compiled PDFs."""

import argparse
import html
import json
import os
from datetime import datetime
from urllib.parse import quote

CATEGORY_META = {
    "articles": {"label": "Artigos", "icon": "📄", "anchor": "articles"},
    "cv": {"label": "Currículo", "icon": "👤", "anchor": "cv"},
    "slides": {"label": "Slides", "icon": "🖥️", "anchor": "slides"},
    "math": {"label": "Matemática", "icon": "∑", "anchor": "math"},
}
CATEGORIES_ORDER = ("articles", "cv", "slides", "math")


def build_nav() -> str:
    return "\n      ".join(
        f'<a href="#{CATEGORY_META[category]["anchor"]}">'
        f'{CATEGORY_META[category]["icon"]} {CATEGORY_META[category]["label"]}</a>'
        for category in CATEGORIES_ORDER
    )


def build_sections(docs: dict) -> str:
    sections = []
    for category in CATEGORIES_ORDER:
        meta = CATEGORY_META[category]
        items = docs.get(category, [])
        if items:
            rows = []
            for item in items:
                title = html.escape(item["title"])
                filename = quote(item["file"], safe="")
                rows.append(
                    f'<li class="doc-item"><span class="doc-title">{title}</span>'
                    f'<a class="doc-link" href="{category}/{filename}" '
                    f'target="_blank" rel="noopener">Baixar PDF</a></li>'
                )
            content = '<ul class="doc-list">\n' + "\n".join(rows) + "\n</ul>"
        else:
            content = (
                '<p class="empty">Nenhum documento publicado. Adicione arquivos '
                f'<code>.tex</code> em <code>src/{category}/</code>.</p>'
            )

        sections.append(
            f'<section class="index-section" id="{meta["anchor"]}">'
            f'<h2>{meta["icon"]} {meta["label"]}</h2>\n{content}\n</section>'
        )
    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Generated index HTML path")
    parser.add_argument("--template", required=True, help="HTML template path")
    parser.add_argument("--docs", required=True, help="JSON document metadata")
    args = parser.parse_args()

    docs = json.loads(args.docs)
    for category in docs:
        docs[category] = [
            item
            for item in docs[category]
            if item.get("title") and item.get("file")
        ]

    with open(args.template, encoding="utf-8") as template_file:
        template = template_file.read()

    output = (
        template.replace("{nav_links}", build_nav())
        .replace("{sections}", build_sections(docs))
        .replace("{date}", datetime.now().strftime("%d/%m/%Y %H:%M"))
    )
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as output_file:
        output_file.write(output)

    print(f"index.html gerado em: {args.output}")


if __name__ == "__main__":
    main()
