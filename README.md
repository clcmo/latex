<!-- Generated from content/pt-br.md; edit the source file. -->

🇧🇷 Português | [English](README.en.md)

# LaTeX Site — Publicação de documentos

Site para compilar e publicar documentos LaTeX como PDF e como HTML no GitHub Pages, organizados por tema.

## Como funciona

Os documentos `.tex` ficam em `src/`, organizados por tipo. A cada push na `main`, o GitHub Actions compila cada documento, gera a versão HTML (com a matemática renderizada) e publica:

- um índice por tema;
- uma página de visualização com o PDF e o HTML lado a lado;
- uma apresentação do projeto.

## Pedir a publicação de um documento

Qualquer pessoa pode pedir para publicar, corrigir ou atualizar um documento abrindo uma issue, sem precisar mexer no código.

1. Abra uma [nova issue](https://github.com/clcmo/latex/issues/new/choose) e escolha o modelo **Documento (Português)**.
2. Marque a categoria, o tema e o tipo de pedido.
3. Informe o PDF (nome ou link) e a fonte, se já existirem.
4. Para um documento novo, anexe o arquivo `.tex` na issue.
5. A pessoa mantenedora revisa, adiciona o arquivo em `src/` e o site é atualizado no build seguinte.

O GitHub não costuma aceitar `.tex` como anexo. Envie o arquivo compactado em `.zip` (inclua imagens e bibliografia, se houver), renomeie-o para `.txt` ou, se for curto, cole o conteúdo em um bloco de código.

Enviar o arquivo não garante a publicação: o documento precisa compilar e passa por revisão.

## Adicionar um documento

Para quem mantém o repositório:

1. Crie um `.tex` em `src/articles/`, `src/cv/`, `src/math/` ou `src/slides/`.
2. Se possível, declare `\title{Título do documento}` para exibir o título no índice.
3. Execute `bash scripts/build.sh` e confira o resultado em `site/`.

O build requer Python 3 e `pdflatex` (TeX Live). O `pandoc` é opcional: sem ele, o site só tem os PDFs. Documentos que usam `fontspec` são compilados com `lualatex`; os demais, com `pdflatex`.

## Temas

A pasta em `src/` define o **tipo** do documento (artigo, currículo, slides, notas). O **tema** define em qual seção do site ele aparece e qual cor de destaque usa.

1. Para escolher o tema, escreva no topo do `.tex`: `% tema: fisica`.
2. Sem essa linha, o tema padrão vem do tipo (veja `padrao_por_tipo` em `content/temas.json`).
3. Para criar ou editar um tema, altere `content/temas.json` (nome, descrição e cor `#rrggbb`).
4. Para não gerar a versão HTML de um documento, escreva `% html: off` no topo do `.tex`.

A versão HTML é gerada pelo `pandoc` e é uma conversão aproximada: documentos com muitos pacotes (TikZ, caixas coloridas) podem perder formatação. O PDF continua sendo a versão de referência.

## Estrutura

```text
.github/
  ISSUE_TEMPLATE/      Modelos de issue (português e inglês)
  workflows/           CI, Pages, READMEs e release
assets/
  css/                 Estilos do site
  js/                  Comportamentos do site
  python/              Geradores do índice, dos visualizadores, das cores dos temas e dos READMEs
content/
  en.md                Fonte do README em inglês
  pt-br.md             Fonte deste README
  temas.json           Temas (nome, descrição, cor) e slides da apresentação
src/
  articles/            Artigos e textos
  cv/                  Currículos
  math/                Notas matemáticas
  slides/              Apresentações Beamer
templates/             Templates HTML do site
scripts/build.sh       Build local e de CI
```

## Publicar no GitHub Pages

Configure **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Pushes e pull requests para `main` compilam os documentos; pushes para `main`
publicam o site.

## Atualizar os READMEs

Edite `content/pt-br.md` e `content/en.md`. O build gera `README.md` e
`README.en.md` a partir desses arquivos.
