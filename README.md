# 📄 LaTeX Site — GitHub Pages

Sistema para publicar documentos LaTeX como páginas web, com opção de download em PDF.  
**Escreva `.tex` → faça push → o site atualiza automaticamente.**

---

## 🚀 Configuração Inicial (5 minutos)

### 1. Crie o repositório no GitHub

```bash
# Clone ou faça upload desta pasta para um repositório no GitHub
git init
git add .
git commit -m "feat: initial latex site setup"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
git push -u origin main
```

### 2. Ative o GitHub Pages

1. Vá em **Settings → Pages** no seu repositório
2. Em **Source**, selecione **GitHub Actions**
3. Salve

### 3. Pronto! 🎉

Na próxima vez que fizer push na branch `main`, o site será compilado e publicado em:
```
https://SEU-USUARIO.github.io/SEU-REPO/
```

---

## 📁 Estrutura do Projeto

```
.
├── content/
│   ├── articles/     ← Artigos científicos e textos
│   ├── cv/           ← Currículo / CV
│   ├── slides/       ← Apresentações Beamer
│   └── math/         ← Notas matemáticas
├── templates/
│   └── page.html     ← Template HTML das páginas
├── scripts/
│   ├── build.sh      ← Script de compilação principal
│   └── generate_index.py ← Gera a página inicial
└── .github/
    └── workflows/
        └── build.yml ← Automação GitHub Actions
```

---

## ✍️ Como adicionar documentos

1. Crie um arquivo `.tex` na pasta correta:
   ```
   content/articles/meu-artigo.tex
   content/cv/meu-cv.tex
   content/slides/minha-apresentacao.tex
   content/math/minhas-notas.tex
   ```

2. Inclua `\title{Título do Documento}` no arquivo `.tex`

3. Faça push:
   ```bash
   git add content/articles/meu-artigo.tex
   git commit -m "add: artigo sobre X"
   git push
   ```

4. Aguarde ~3 minutos para o Actions compilar e publicar.

---

## 🔧 Tecnologias

| Ferramenta | Função |
|---|---|
| **GitHub Actions** | Automação: compila ao fazer push |
| **TeX Live** | Compilação `.tex` → PDF |
| **Pandoc** | Conversão `.tex` → HTML |
| **MathJax** | Renderização de fórmulas no browser |
| **GitHub Pages** | Hospedagem gratuita |

---

## 📐 Fórmulas matemáticas

As fórmulas são renderizadas pelo MathJax diretamente no browser:

- **Inline:** `$E = mc^2$`
- **Display:** `$$\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}$$`

Não é necessária nenhuma configuração extra — funciona automaticamente.

---

## 💡 Dicas

- Use `\title{}`, `\author{}` e `\date{}` nos seus documentos para que apareçam nas páginas
- PDFs são gerados automaticamente e ficam disponíveis para download em cada página
- O índice (`index.html`) é gerado automaticamente listando todos os documentos
- Documentos com erros de compilação ainda geram HTML via Pandoc (best-effort)

---

## 🛠 Desenvolvimento local

Para testar localmente antes de fazer push:

```bash
# Instalar dependências (Ubuntu/Debian)
sudo apt-get install texlive-full pandoc python3

# Compilar
bash scripts/build.sh

# Ver resultado
open site/index.html
```
