#!/usr/bin/env bash
set -e

SITE_DIR="site"
PDF_DIR="site/pdf"
CONTENT_DIR="content"
TEMPLATE="templates/page.html"

mkdir -p "$SITE_DIR" "$PDF_DIR"

echo "🔨 Building LaTeX site..."

# ─── Helper: convert one .tex file ───────────────────────────────────────────
build_document() {
  local tex_file="$1"
  local category="$2"           # articles | cv | slides | math
  local base
  base=$(basename "$tex_file" .tex)
  local out_dir="$SITE_DIR/$category"
  mkdir -p "$out_dir"

  echo "  📄 $tex_file → HTML + PDF"

  # Extract title from \title{...} or use filename
  local title
  title=$(grep -oP '(?<=\\title\{)[^}]+' "$tex_file" | head -1 || echo "$base")

  # ── Compile PDF ──────────────────────────────────────────────────────────────
  local tmp_dir
  tmp_dir=$(mktemp -d)
  cp "$tex_file" "$tmp_dir/"
  (cd "$tmp_dir" && pdflatex -interaction=nonstopmode "$(basename "$tex_file")" > /dev/null 2>&1 || true)
  (cd "$tmp_dir" && pdflatex -interaction=nonstopmode "$(basename "$tex_file")" > /dev/null 2>&1 || true)
  if [ -f "$tmp_dir/$base.pdf" ]; then
    cp "$tmp_dir/$base.pdf" "$PDF_DIR/$base.pdf"
  fi
  rm -rf "$tmp_dir"

  # ── Convert to HTML via Pandoc ───────────────────────────────────────────────
  pandoc "$tex_file" \
    --standalone \
    --template="$TEMPLATE" \
    --mathjax \
    --highlight-style=pygments \
    --metadata title="$title" \
    --metadata category="$category" \
    --metadata basename="$base" \
    -o "$out_dir/$base.html" 2>/dev/null || {
      echo "    ⚠️  Pandoc warning for $tex_file (continuing)"
    }
}

# ─── Build each category ─────────────────────────────────────────────────────
for category in articles cv slides math; do
  if [ -d "$CONTENT_DIR/$category" ]; then
    for tex in "$CONTENT_DIR/$category"/*.tex; do
      [ -f "$tex" ] && build_document "$tex" "$category"
    done
  fi
done

# ─── Generate index page ──────────────────────────────────────────────────────
python3 scripts/generate_index.py "$SITE_DIR"

echo "✅ Build complete! Site is in ./$SITE_DIR"
