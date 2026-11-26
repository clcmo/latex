(() => {
  const toc = document.getElementById("toc");
  if (!toc) return;

  const headings = document.querySelectorAll("article h2, article h3");
  headings.forEach((heading, index) => {
    if (!heading.id) heading.id = `heading-${index}`;

    const item = document.createElement("li");
    item.className = heading.tagName === "H3" ? "toc-h3" : "";

    const link = document.createElement("a");
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    item.appendChild(link);
    toc.appendChild(item);
  });

  if (!("IntersectionObserver" in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const link = toc.querySelector(`a[href="#${entry.target.id}"]`);
      if (link) link.classList.toggle("active", entry.isIntersecting);
    });
  }, { rootMargin: "-60px 0px -80% 0px" });

  headings.forEach((heading) => observer.observe(heading));
})();
