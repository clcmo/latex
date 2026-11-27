#!/usr/bin/env python3
"""Funções compartilhadas pelos geradores do site."""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TIPOS = ("articles", "cv", "slides", "math")
REPOSITORIO = os.environ.get("GITHUB_REPOSITORY", "clcmo/latex")


def carregar_temas() -> dict:
    return json.loads((ROOT / "content" / "temas.json").read_text(encoding="utf-8"))


def _limpar(bruto: str) -> str:
    texto = bruto.replace("\\\\", " ")
    texto = re.sub(r"\\[A-Za-z]+\*?", "", texto)
    texto = texto.replace("{", "").replace("}", "")
    return " ".join(texto.split())


def _comando(texto: str, nome: str) -> str:
    """Primeiro \\nome{...} que cabe em uma linha e não está comentado."""
    for linha in texto.splitlines():
        if linha.lstrip().startswith("%"):
            continue
        achou = re.search(r"\\" + nome + r"\{(.*)\}", linha)
        if achou:
            return _limpar(achou.group(1))
    return ""


def ler_metadados(tex: Path, tipo: str, temas: dict) -> dict:
    texto = tex.read_text(encoding="utf-8", errors="replace")
    marca = re.search(r"^%\s*tema:\s*([\w-]+)", texto, re.M | re.I)
    tema = marca.group(1).lower() if marca else None
    if tema not in temas["temas"]:
        if tema:
            print(f"Aviso: tema '{tema}' desconhecido em {tex.name}", file=sys.stderr)
        tema = temas["padrao_por_tipo"].get(tipo, temas["ordem"][-1])
    return {
        "titulo": _comando(texto, "title") or tex.stem,
        "autor": _comando(texto, "author"),
        "tema": tema,
    }


def coletar_docs(site: Path) -> list:
    """Documentos de src/ que já têm PDF compilado em site/."""
    temas = carregar_temas()
    docs = []
    for tipo in TIPOS:
        for tex in sorted((ROOT / "src" / tipo).glob("*.tex")):
            if not (site / tipo / f"{tex.stem}.pdf").exists():
                continue
            doc = ler_metadados(tex, tipo, temas)
            doc.update(
                tipo=tipo,
                nome=tex.stem,
                tem_html=(site / tipo / "html" / f"{tex.stem}.html").exists(),
                tex_url=f"https://github.com/{REPOSITORIO}/blob/main/src/{tipo}/{tex.name}",
            )
            docs.append(doc)
    return docs


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "tema":
        arquivo = Path(sys.argv[2])
        print(ler_metadados(arquivo, arquivo.parent.name, carregar_temas())["tema"])
    else:
        sys.exit("uso: site_data.py tema ARQUIVO.tex")
