#!/usr/bin/env python3
"""Generate the index.html listing all published documents."""

import os, sys, json
from pathlib import Path
from datetime import datetime

CATEGORY_META = {
    "articles": {"label": "Artigos",       "icon": "✦", "color": "#c8a96e"},
    "cv":        {"label": "Currículo",     "icon": "◈", "color": "#7eb8c8"},
    "slides":    {"label": "Apresentações", "icon": "◉", "color": "#c87eb8"},
    "math":      {"label": "Matemática",    "icon": "∑", "color": "#7ec87e"},
}

def scan_documents(site_dir: Path):
    docs = {}
    for category in ["articles", "cv", "slides", "math"]:
        cat_dir = site_dir / category
        if not cat_dir.exists():
            continue
        docs[category] = []
        for html_file in sorted(cat_dir.glob("*.html")):
            base = html_file.stem
            has_pdf = (site_dir / "pdf" / f"{base}.pdf").exists()
            # Try to extract title from HTML
            content = html_file.read_text(errors="ignore")
            title = base
            for line in content.splitlines():
                if "<title>" in line:
                    t = line.replace("<title>","").replace("</title>","").strip()
                    if t: title = t
                    break
            docs[category].append({
                "base": base,
                "title": title,
                "html": f"{category}/{base}.html",
                "pdf": f"pdf/{base}.pdf" if has_pdf else None,
            })
    return docs

def render_card(doc, meta):
    pdf_btn = ""
    if doc["pdf"]:
        pdf_btn = f'<a class="btn-pdf" href="{doc["pdf"]}" download>↓ PDF</a>'
    return f"""
    <article class="doc-card">
      <div class="card-icon">{meta['icon']}</div>
      <h3><a href="{doc['html']}">{doc['title']}</a></h3>
      <div class="card-actions">
        <a class="btn-view" href="{doc['html']}">Ver →</a>
        {pdf_btn}
      </div>
    </article>"""

def generate(site_dir_str):
    site_dir = Path(site_dir_str)
    docs = scan_documents(site_dir)
    sections = ""
    for cat, meta in CATEGORY_META.items():
        items = docs.get(cat, [])
        if not items:
            continue
        cards = "\n".join(render_card(d, meta) for d in items)
        sections += f"""
      <section class="category" id="{cat}">
        <h2 class="cat-title" style="--accent:{meta['color']}">
          <span class="cat-icon">{meta['icon']}</span> {meta['label']}
        </h2>
        <div class="card-grid">{cards}</div>
      </section>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>LaTeX Site</title>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
  <style>
    :root {{
      --bg: #0d0d0f;
      --surface: #141416;
      --border: #2a2a2e;
      --text: #e8e4dc;
      --muted: #888;
      --gold: #c8a96e;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'EB Garamond', Georgia, serif;
      min-height: 100vh;
    }}
    /* ── Header ── */
    header {{
      border-bottom: 1px solid var(--border);
      padding: 3rem 2rem 2rem;
      text-align: center;
      position: relative;
      overflow: hidden;
    }}
    header::before {{
      content: '';
      position: absolute; inset: 0;
      background: radial-gradient(ellipse at 50% 0%, rgba(200,169,110,.08) 0%, transparent 70%);
      pointer-events: none;
    }}
    .site-title {{
      font-size: clamp(2.4rem, 6vw, 4rem);
      font-weight: 600;
      letter-spacing: -.02em;
      color: var(--gold);
    }}
    .site-sub {{
      margin-top: .5rem;
      color: var(--muted);
      font-style: italic;
      font-size: 1.1rem;
    }}
    nav {{
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      margin-top: 2rem;
      flex-wrap: wrap;
    }}
    nav a {{
      color: var(--muted);
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-size: .8rem;
      letter-spacing: .08em;
      text-transform: uppercase;
      padding: .3rem .6rem;
      border: 1px solid transparent;
      border-radius: 3px;
      transition: all .2s;
    }}
    nav a:hover {{ color: var(--text); border-color: var(--border); }}
    /* ── Main ── */
    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 4rem 2rem;
    }}
    .category {{ margin-bottom: 4rem; }}
    .cat-title {{
      font-size: 1.6rem;
      font-weight: 600;
      margin-bottom: 1.5rem;
      padding-bottom: .75rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      gap: .6rem;
      color: var(--accent);
    }}
    .cat-icon {{ font-size: 1.2rem; opacity: .8; }}
    .card-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1rem;
    }}
    .doc-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: .75rem;
      transition: border-color .2s, transform .2s;
    }}
    .doc-card:hover {{ border-color: #444; transform: translateY(-2px); }}
    .card-icon {{ font-size: 1.4rem; opacity: .5; }}
    .doc-card h3 {{ font-size: 1.05rem; font-weight: 600; line-height: 1.4; }}
    .doc-card h3 a {{ color: var(--text); text-decoration: none; }}
    .doc-card h3 a:hover {{ color: var(--gold); }}
    .card-actions {{ display: flex; gap: .5rem; margin-top: auto; }}
    .btn-view, .btn-pdf {{
      font-family: 'JetBrains Mono', monospace;
      font-size: .75rem;
      padding: .35rem .75rem;
      border-radius: 3px;
      text-decoration: none;
      transition: all .15s;
    }}
    .btn-view {{
      background: rgba(200,169,110,.12);
      color: var(--gold);
      border: 1px solid rgba(200,169,110,.3);
    }}
    .btn-view:hover {{ background: rgba(200,169,110,.22); }}
    .btn-pdf {{
      background: rgba(255,255,255,.05);
      color: var(--muted);
      border: 1px solid var(--border);
    }}
    .btn-pdf:hover {{ color: var(--text); border-color: #555; }}
    /* ── Empty state ── */
    .empty {{
      text-align: center;
      padding: 6rem 2rem;
      color: var(--muted);
    }}
    .empty code {{
      font-family: 'JetBrains Mono', monospace;
      background: var(--surface);
      padding: .2rem .5rem;
      border-radius: 3px;
      font-size: .9rem;
    }}
    footer {{
      border-top: 1px solid var(--border);
      text-align: center;
      padding: 2rem;
      color: var(--muted);
      font-size: .85rem;
      font-family: 'JetBrains Mono', monospace;
    }}
  </style>
</head>
<body>
  <header>
    <h1 class="site-title">LaTeX Site</h1>
    <p class="site-sub">Documentos compilados automaticamente via GitHub Actions</p>
    <nav>
      <a href="#articles">Artigos</a>
      <a href="#cv">Currículo</a>
      <a href="#slides">Slides</a>
      <a href="#math">Matemática</a>
    </nav>
  </header>
  <main>
    {sections if sections else '<div class="empty"><p>Nenhum documento publicado ainda.</p><p>Adicione arquivos <code>.tex</code> em <code>content/</code> e faça um push.</p></div>'}
  </main>
  <footer>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} · LaTeX + GitHub Actions + GitHub Pages</footer>
</body>
</html>"""

    (site_dir / "index.html").write_text(html)
    print(f"  📑 index.html gerado com {sum(len(v) for v in docs.values())} documentos")

if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv) > 1 else "site")
