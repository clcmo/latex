#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# build.sh — Compila todos os .tex em content/ e monta o site em site/
# ---------------------------------------------------------------------------

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTENT_DIR="$REPO_ROOT/content"
SITE_DIR="$REPO_ROOT/site"
SCRIPTS_DIR="$REPO_ROOT/scripts"

CATEGORIES=("articles" "cv" "slides" "math")

echo "==> Criando estrutura do site..."
mkdir -p "$SITE_DIR"
for cat in "${CATEGORIES[@]}"; do
  mkdir -p "$SITE_DIR/$cat"
done

# ---------------------------------------------------------------------------
# Compila cada .tex encontrado
# ---------------------------------------------------------------------------
declare -A COMPILED_DOCS  # categoria -> lista de "titulo|arquivo.pdf"

for cat in "${CATEGORIES[@]}"; do
  SRC_DIR="$CONTENT_DIR/$cat"
  OUT_DIR="$SITE_DIR/$cat"

  [[ -d "$SRC_DIR" ]] || continue

  while IFS= read -r -d '' texfile; do
    filename="$(basename "$texfile" .tex)"
    echo "  -> Compilando: $cat/$filename.tex"

    # Compila duas vezes para resolver referências cruzadas
    if pdflatex \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" > /dev/null 2>&1 && \
       pdflatex \
        -interaction=nonstopmode \
        -halt-on-error \
        -output-directory="$OUT_DIR" \
        "$texfile" > /dev/null 2>&1; then

      # Extrai título do .tex (primeira ocorrência de \title{...})
      title=$(grep -m1 '\\title{' "$texfile" \
              | sed 's/.*\\title{\(.*\)}/\1/' \
              | sed 's/\\\\/ /g' \
              | tr -d '{}' \
              | xargs)
      [[ -z "$title" ]] && title="$filename"

      # Acumula para o index
      COMPILED_DOCS["$cat"]+="${title}|${filename}.pdf"$'\n'

      # Remove arquivos auxiliares, mantém só o PDF
      rm -f "$OUT_DIR/$filename".{aux,log,out,toc,lof,lot,nav,snm,vrb}

      echo "     OK: $filename.pdf"
    else
      echo "     ERRO ao compilar $cat/$filename.tex — pulando"
    fi
  done < <(find "$SRC_DIR" -maxdepth 1 -name "*.tex" -print0 | sort -z)
done

# ---------------------------------------------------------------------------
# Gera o index.html via script Python
# ---------------------------------------------------------------------------
echo "==> Gerando index.html..."

# Serializa os docs compilados como JSON para passar ao Python
DOCS_JSON="{"
for cat in "${CATEGORIES[@]}"; do
  DOCS_JSON+="\"$cat\": ["
  while IFS='|' read -r title pdffile; do
    [[ -z "$title" ]] && continue
    # Escapa aspas duplas
    title="${title//\"/\\\"}"
    DOCS_JSON+="{\"title\": \"$title\", \"file\": \"$pdffile\"},"
  done <<< "${COMPILED_DOCS[$cat]:-}"
  # Remove trailing comma e fecha array
  DOCS_JSON="${DOCS_JSON%,}],"
done
DOCS_JSON="${DOCS_JSON%,}}"

python3 "$SCRIPTS_DIR/generate_index.py" \
  --output "$SITE_DIR/index.html" \
  --template "$REPO_ROOT/templates/page.html" \
  --docs "$DOCS_JSON"

echo "==> Build concluído! Arquivos em: $SITE_DIR"