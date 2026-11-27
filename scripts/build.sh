#!/usr/bin/env bash
set -euo pipefail

# build.sh — compila os documentos LaTeX (PDF e HTML) e gera o site e os READMEs.

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

HAS_PANDOC=0
if command -v pandoc >/dev/null; then
  HAS_PANDOC=1
else
  echo "Aviso: pandoc não encontrado; as versões HTML serão ignoradas."
fi

# Gera a versão HTML (com LaTeX) de um documento. É opcional: se falhar, o PDF continua valendo.
gerar_html() {
  local cat="$1" texfile="$2" filename="$3" tema
  [[ "$HAS_PANDOC" == 1 ]] || return 0
  if grep -qiE '^%[[:space:]]*html:[[:space:]]*off' "$texfile"; then
    echo "     HTML desativado neste documento"
    return 0
  fi
  tema="$(python3 "$PYTHON_DIR/site_data.py" tema "$texfile")"
  mkdir -p "$SITE_DIR/$cat/html"
  if pandoc "$texfile" \
      --from latex --to html5 --standalone --mathjax \
      --template "$REPO_ROOT/templates/page.html" \
      --metadata "basename=$filename" \
      --metadata "category=$cat" \
      --metadata "tema=$tema" \
      --output "$SITE_DIR/$cat/html/$filename.html" </dev/null >/dev/null 2>&1; then
    echo "     OK: html/$filename.html (tema: $tema)"
  else
    rm -f "$SITE_DIR/$cat/html/$filename.html"
    echo "     AVISO: HTML não gerado para $cat/$filename.tex"
  fi
}

# Documentos que usam fontspec/\babelfont precisam de LuaLaTeX; os demais usam pdflatex.
escolher_motor() {
  if grep -qE '\\usepackage(\[[^]]*\])?\{fontspec\}|\\babelfont' "$1"; then
    echo lualatex
  else
    echo pdflatex
  fi
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
done

echo "==> Compilando documentos..."
for cat in $CATEGORIES; do
  SRC_DIR="$SOURCE_DIR/$cat"
  OUT_DIR="$SITE_DIR/$cat"
  [[ -d "$SRC_DIR" ]] || continue

  while IFS= read -r -d '' texfile; do
    filename="$(basename "$texfile" .tex)"
    engine="$(escolher_motor "$texfile")"
    echo "  -> $cat/$filename.tex ($engine)"

    if "$engine" \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" >/dev/null 2>&1 &&
       "$engine" \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" >/dev/null 2>&1; then

      gerar_html "$cat" "$texfile" "$filename"

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

echo "==> Gerando cores dos temas..."
python3 "$PYTHON_DIR/generate_theme_css.py" --site "$SITE_DIR"

echo "==> Gerando visualizadores..."
python3 "$PYTHON_DIR/generate_viewers.py" \
  --site "$SITE_DIR" \
  --template "$REPO_ROOT/templates/viewer.html"

echo "==> Gerando index.html..."
python3 "$PYTHON_DIR/generate_index.py" \
  --site "$SITE_DIR" \
  --output "$SITE_DIR/index.html" \
  --template "$REPO_ROOT/templates/index.html"

if [[ "$COMPILE_FAILURES" -gt 0 ]]; then
  echo "==> Build concluído com $COMPILE_FAILURES erro(s)."
  exit 1
fi

echo "==> Build concluído! Arquivos em: $SITE_DIR"