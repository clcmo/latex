#!/usr/bin/env bash
set -euo pipefail

# build.sh — compila os documentos LaTeX e gera o site e os READMEs.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$REPO_ROOT/src"
SITE_DIR="$REPO_ROOT/site"
PYTHON_DIR="$REPO_ROOT/assets/python"
CATEGORIES="articles cv slides math"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
COMPILE_FAILURES=0

command -v pdflatex >/dev/null || {
  echo "Erro: pdflatex não encontrado."
  exit 1
}
command -v python3 >/dev/null || {
  echo "Erro: python3 não encontrado."
  exit 1
}

echo "==> Criando estrutura do site..."
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR/assets"
cp -R "$REPO_ROOT/assets/css" "$SITE_DIR/assets/"
cp -R "$REPO_ROOT/assets/js" "$SITE_DIR/assets/"

echo "==> Gerando READMEs..."
python3 "$PYTHON_DIR/build_readme.py"

for cat in $CATEGORIES; do
  mkdir -p "$SITE_DIR/$cat"
  : > "$TMP_DIR/$cat.tsv"
done

echo "==> Compilando documentos..."
for cat in $CATEGORIES; do
  SRC_DIR="$SOURCE_DIR/$cat"
  OUT_DIR="$SITE_DIR/$cat"
  [[ -d "$SRC_DIR" ]] || continue

  while IFS= read -r -d '' texfile; do
    filename="$(basename "$texfile" .tex)"
    echo "  -> $cat/$filename.tex"

    if pdflatex \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" >/dev/null 2>&1 &&
       pdflatex \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" >/dev/null 2>&1; then

      title="$({ grep -m1 '\\title{' "$texfile" || true; } |
        sed 's/.*\\title{\(.*\)}/\1/' |
        sed 's/\\\\/ /g' |
        tr -d '{}' |
        xargs)"
      [[ -n "$title" ]] || title="$filename"
      printf '%s\t%s\n' "$title" "$filename.pdf" >> "$TMP_DIR/$cat.tsv"

      rm -f "$OUT_DIR/$filename.aux" "$OUT_DIR/$filename.log" \
        "$OUT_DIR/$filename.out" "$OUT_DIR/$filename.toc" \
        "$OUT_DIR/$filename.lof" "$OUT_DIR/$filename.lot" \
        "$OUT_DIR/$filename.nav" "$OUT_DIR/$filename.snm" \
        "$OUT_DIR/$filename.vrb"
      echo "     OK: $filename.pdf"
    else
      echo "     ERRO: $cat/$filename.tex"
      COMPILE_FAILURES=$((COMPILE_FAILURES + 1))
      rm -f "$OUT_DIR/$filename.aux" "$OUT_DIR/$filename.log" \
        "$OUT_DIR/$filename.out" "$OUT_DIR/$filename.toc" \
        "$OUT_DIR/$filename.lof" "$OUT_DIR/$filename.lot" \
        "$OUT_DIR/$filename.nav" "$OUT_DIR/$filename.snm" \
        "$OUT_DIR/$filename.vrb"
    fi
  done < <(find "$SRC_DIR" -maxdepth 1 -name "*.tex" -print0 | sort -z)
done

echo "==> Gerando index.html..."
python3 - "$TMP_DIR" "$SITE_DIR/index.html" "$PYTHON_DIR/generate_index.py" \
  "$REPO_ROOT/templates/index.html" <<'PY'
import json
import pathlib
import subprocess
import sys

tmp_dir = pathlib.Path(sys.argv[1])
output = sys.argv[2]
generator = sys.argv[3]
template = sys.argv[4]

docs = {}
for category in ("articles", "cv", "slides", "math"):
    items = []
    for line in (tmp_dir / f"{category}.tsv").read_text(encoding="utf-8").splitlines():
        title, pdf_file = line.split("\t", 1)
        items.append({"title": title, "file": pdf_file})
    docs[category] = items

subprocess.run(
    [
        sys.executable,
        generator,
        "--output",
        output,
        "--template",
        template,
        "--docs",
        json.dumps(docs, ensure_ascii=False),
    ],
    check=True,
)
PY

if [[ "$COMPILE_FAILURES" -gt 0 ]]; then
  echo "==> Build concluído com $COMPILE_FAILURES erro(s)."
  exit 1
fi

echo "==> Build concluído! Arquivos em: $SITE_DIR"