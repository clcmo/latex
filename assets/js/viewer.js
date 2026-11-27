(() => {
  const viewer = document.getElementById("viewer");
  if (!viewer) return;

  const botoes = document.querySelectorAll(".modos button");
  const temHtml = viewer.dataset.html === "1";
  const validos = temHtml ? ["pdf", "html", "split"] : ["pdf"];
  const chave = "latex-modo";

  function guardado() {
    try {
      return localStorage.getItem(chave);
    } catch (erro) {
      return null;
    }
  }

  function aplicar(modo, salvar) {
    if (!validos.includes(modo)) modo = validos[0];
    viewer.dataset.modo = modo;
    botoes.forEach((botao) =>
      botao.setAttribute("aria-pressed", String(botao.dataset.modo === modo)),
    );
    history.replaceState(null, "", `#${modo}`);
    if (!salvar) return;
    try {
      localStorage.setItem(chave, modo);
    } catch (erro) {
      /* armazenamento indisponível: a escolha vale só nesta página */
    }
  }

  botoes.forEach((botao) => {
    if (!validos.includes(botao.dataset.modo)) botao.hidden = true;
    botao.addEventListener("click", () => aplicar(botao.dataset.modo, true));
  });

  const estreita = window.matchMedia("(max-width: 860px)").matches;
  const inicial =
    location.hash.slice(1) || guardado() || (estreita ? "html" : "split");
  aplicar(estreita && inicial === "split" ? "html" : inicial, false);
})();
