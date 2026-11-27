(() => {
  const deck = document.getElementById("deck");
  const dados = document.getElementById("slides-data");
  if (!deck || !dados) return;

  const slides = JSON.parse(dados.textContent);
  const corpo = deck.querySelector(".slide");
  const contagem = deck.querySelector(".contagem");
  const anterior = deck.querySelector("[data-ant]");
  const proximo = deck.querySelector("[data-prox]");
  let atual = 0;
  let origem = null;

  function mostrar() {
    const slide = slides[atual];
    const titulo = document.createElement("h2");
    titulo.textContent = slide.titulo;
    corpo.replaceChildren(titulo);
    if (slide.texto) {
      const texto = document.createElement("p");
      texto.textContent = slide.texto;
      corpo.appendChild(texto);
    }
    if (slide.itens) {
      const lista = document.createElement("ul");
      slide.itens.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        lista.appendChild(li);
      });
      corpo.appendChild(lista);
    }
    contagem.textContent = `${atual + 1} de ${slides.length}`;
    anterior.disabled = atual === 0;
    proximo.textContent =
      atual === slides.length - 1 ? "Ver documentos" : "Próximo";
  }

  function abrir() {
    origem = document.activeElement;
    atual = 0;
    mostrar();
    deck.hidden = false;
    proximo.focus();
  }

  function fechar() {
    deck.hidden = true;
    if (origem) origem.focus();
  }

  function avancar() {
    if (atual === slides.length - 1) return fechar();
    atual += 1;
    mostrar();
  }

  function voltar() {
    if (atual === 0) return;
    atual -= 1;
    mostrar();
  }

  document
    .querySelectorAll("[data-apresentar]")
    .forEach((botao) => botao.addEventListener("click", abrir));
  deck.querySelector("[data-fechar]").addEventListener("click", fechar);
  proximo.addEventListener("click", avancar);
  anterior.addEventListener("click", voltar);
  document.addEventListener("keydown", (evento) => {
    if (deck.hidden) return;
    if (evento.key === "ArrowRight") avancar();
    if (evento.key === "ArrowLeft") voltar();
    if (evento.key === "Escape") fechar();
  });
})();
