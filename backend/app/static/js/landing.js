(() => {
  const api = "";
  const el = (id) => document.getElementById(id);

  // Footer year
  el("year").textContent = new Date().getFullYear();

  async function probe(path, target) {
    try {
      const r = await fetch(`${api}${path}`, { headers: { "cache-control": "no-cache" } });
      const txt = await r.text();
      el(target).textContent = txt.length > 400 ? txt.slice(0, 400) + " …" : txt;
    } catch (e) {
      el(target).textContent = `error: ${e.message}`;
    }
  }

  probe("/health", "health");
  probe("/info", "info");
})();
