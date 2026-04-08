#!/usr/bin/env python3
"""
generate_index.py — Gera o index.html listando todos os PDFs compilados.

Uso:
    python3 generate_index.py \
        --output site/index.html \
        --template templates/page.html \
        --docs '{"articles": [{"title": "...", "file": "....pdf"}], ...}'
"""

import argparse
import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Labels e ícones por categoria
# ---------------------------------------------------------------------------
CATEGORY_META = {
    "articles": {"label": "Artigos",    "icon": "📄", "anchor": "articles"},
    "cv":       {"label": "Currículo",  "icon": "👤", "anchor": "cv"},
    "slides":   {"label": "Slides",     "icon": "🖥️",  "anchor": "slides"},
    "math":     {"label": "Matemática", "icon": "∑",  "anchor": "math"},
}

CATEGORIES_ORDER = ["articles", "cv", "slides", "math"]

# ---------------------------------------------------------------------------
# HTML inline (usado quando não há template externo)
# ---------------------------------------------------------------------------
DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LaTeX Site</title>
  <style>
    :root {{
      --bg: #0d1117;
      --surface: #161b22;
      --border: #30363d;
      --accent: #58a6ff;
      --text: #c9d1d9;
      --muted: #8b949e;
      --green: #3fb950;
      --red: #f85149;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }}
    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 1.25rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    header h1 {{ font-size: 1.4rem; color: var(--accent); }}
    header p  {{ font-size: 0.85rem; color: var(--muted); margin-top: .25rem; }}
    nav {{ display: flex; gap: .75rem; flex-wrap: wrap; }}
    nav a {{
      color: var(--muted);
      text-decoration: none;
      font-size: .875rem;
      padding: .3rem .75rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      transition: color .15s, border-color .15s;
    }}
    nav a:hover {{ color: var(--accent); border-color: var(--accent); }}
    main {{ max-width: 860px; margin: 0 auto; padding: 2rem 1.5rem; }}
    .section {{ margin-bottom: 3rem; }}
    .section-header {{
      display: flex;
      align-items: center;
      gap: .6rem;
      margin-bottom: 1rem;
      padding-bottom: .5rem;
      border-bottom: 1px solid var(--border);
    }}
    .section-header h2 {{ font-size: 1.1rem; }}
    .section-icon {{ font-size: 1.2rem; }}
    .doc-list {{ list-style: none; display: flex; flex-direction: column; gap: .5rem; }}
    .doc-item {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: .75rem 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      transition: border-color .15s;
    }}
    .doc-item:hover {{ border-color: var(--accent); }}
    .doc-title {{ font-size: .95rem; }}
    .doc-link {{
      font-size: .8rem;
      color: var(--accent);
      text-decoration: none;
      padding: .25rem .6rem;
      border: 1px solid var(--accent);
      border-radius: 5px;
      white-space: nowrap;
      transition: background .15s;
    }}
    .doc-link:hover {{ background: rgba(88,166,255,.1); }}
    .empty {{
      color: var(--muted);
      font-size: .9rem;
      padding: 1rem 0;
      font-style: italic;
    }}
    footer {{
      text-align: center;
      padding: 2rem;
      color: var(--muted);
      font-size: .8rem;
      border-top: 1px solid var(--border);
    }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>LaTeX Site</h1>
      <p>Documentos compilados automaticamente via GitHub Actions</p>
    </div>
    <nav>
      {nav_links}
    </nav>
  </header>
  <main>
    {sections}
  </main>
  <footer>
    Gerado em {date} &middot; LaTeX + GitHub Actions + GitHub Pages
  </footer>
</body>
</html>
"""


def build_nav(docs: dict) -> str:
    links = []
    for cat in CATEGORIES_ORDER:
        meta = CATEGORY_META[cat]
        links.append(
            f'<a href="#{meta["anchor"]}">{meta["icon"]} {meta["label"]}</a>'
        )
    return "\n      ".join(links)


def build_sections(docs: dict) -> str:
    html = ""
    for cat in CATEGORIES_ORDER:
        meta = CATEGORY_META[cat]
        items = docs.get(cat, [])

        if items:
            lis = "\n".join(
                f'        <li class="doc-item">'
                f'<span class="doc-title">{item["title"]}</span>'
                f'<a class="doc-link" href="{cat}/{item["file"]}" '
                f'target="_blank" rel="noopener">📥 PDF</a>'
                f'</li>'
                for item in items
            )
            list_html = f'<ul class="doc-list">\n{lis}\n      </ul>'
        else:
            list_html = (
                '<p class="empty">Nenhum documento publicado ainda. '
                'Adicione arquivos <code>.tex</code> em '
                f'<code>content/{cat}/</code> e faça um push.</p>'
            )

        html += f"""
    <section class="section" id="{meta['anchor']}">
      <div class="section-header">
        <span class="section-icon">{meta['icon']}</span>
        <h2>{meta['label']}</h2>
      </div>
      {list_html}
    </section>
"""
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",   required=True, help="Caminho do index.html gerado")
    parser.add_argument("--template", required=False, help="Template HTML externo (opcional)")
    parser.add_argument("--docs",     required=True, help="JSON com os documentos compilados")
    args = parser.parse_args()

    docs = json.loads(args.docs)

    # Remove entradas vazias geradas por linhas em branco no bash
    for cat in docs:
        docs[cat] = [d for d in docs[cat] if d.get("title") and d.get("file")]

    # Carrega template externo ou usa o padrão embutido
    if args.template and os.path.isfile(args.template):
        with open(args.template, encoding="utf-8") as f:
            template = f.read()
    else:
        template = DEFAULT_TEMPLATE

    nav_links = build_nav(docs)
    sections  = build_sections(docs)
    date      = datetime.now().strftime("%d/%m/%Y %H:%M")

    output = (
        template
        .replace("{nav_links}", nav_links)
        .replace("{sections}",  sections)
        .replace("{date}",      date)
    )

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"index.html gerado em: {args.output}")


if __name__ == "__main__":
    main()