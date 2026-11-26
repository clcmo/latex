<!-- Generated from content/en.md; edit the source file. -->

🇺🇸 English | [Português](README.md)

# LaTeX Site — Document publishing

A site for compiling and publishing LaTeX documents as PDFs on GitHub Pages.

## How it works

LaTeX `.tex` documents live in `src/`, organized by category. GitHub Actions
compiles each document and publishes its PDF alongside a browsable index.

## Structure

```text
assets/
  css/                 Site styles
  js/                  Site behavior
  python/              Index and README generators
content/
  en.md                Source for this README
  pt-br.md             Source for the Portuguese README
src/
  articles/            Articles and papers
  cv/                  Resumes
  math/                Mathematics notes
  slides/              Beamer presentations
templates/             HTML site templates
scripts/build.sh       Local and CI build
```

## Add a document

1. Create a `.tex` file in `src/articles/`, `src/cv/`, `src/math/`, or
   `src/slides/`.
2. If possible, add `\title{Document title}` so the title appears in the index.
3. Run `bash scripts/build.sh` and inspect the generated files in `site/`.

The build requires Python 3 and `pdflatex` (TeX Live).

## Publish on GitHub Pages

Set **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Pushes and pull requests to `main` compile the documents; pushes to `main`
publish the site.

## Update the READMEs

Edit `content/pt-br.md` and `content/en.md`. The build generates `README.md`
and `README.en.md` from these source files.
