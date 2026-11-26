<!-- Generated from content/pt-br.md; edit the source file. -->

🇧🇷 Português | [English](README.en.md)

# LaTeX Site — Publicação de documentos

Site para compilar e publicar documentos LaTeX como PDFs no GitHub Pages.

## Como funciona

Os documentos `.tex` ficam em `src/`, organizados por categoria. O GitHub Actions
compila cada documento e publica os PDFs e um índice navegável.

## Estrutura

```text
assets/
  css/                 Estilos do site
  js/                  Comportamentos do site
  python/              Geradores do índice e dos READMEs
content/
  en.md                Fonte do README em inglês
  pt-br.md             Fonte deste README
src/
  articles/            Artigos e textos
  cv/                  Currículos
  math/                Notas matemáticas
  slides/              Apresentações Beamer
templates/             Templates HTML do site
scripts/build.sh       Build local e de CI
```

## Adicionar um documento

1. Crie um `.tex` em `src/articles/`, `src/cv/`, `src/math/` ou `src/slides/`.
2. Se possível, declare `\title{Título do documento}` para exibir o título no
   índice.
3. Execute `bash scripts/build.sh` e confira o resultado em `site/`.

O build requer Python 3 e `pdflatex` (TeX Live).

## Publicar no GitHub Pages

Configure **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Pushes e pull requests para `main` compilam os documentos; pushes para `main`
publicam o site.

## Atualizar os READMEs

Edite `content/pt-br.md` e `content/en.md`. O build gera `README.md` e
`README.en.md` a partir desses arquivos.
