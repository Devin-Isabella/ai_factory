(function () {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  const statsEl = document.getElementById('hero-stats');
  if (!statsEl) return;

  async function safeJson(url) {
    try {
      const r = await fetch(url, { headers: { 'accept': 'application/json' } });
      if (!r.ok) throw new Error(r.statusText);
      return await r.json();
    } catch { return null; }
  }

  Promise.all([
    safeJson('/monitor/stats'),
    safeJson('/monitor/db'),
    safeJson('/health'),
  ]).then(([stats, db, health]) => {
    const items = [
      { label: 'API', value: health?.status ?? 'unknown' },
      { label: 'Database', value: db?.db ?? db?.driver ?? 'unknown' },
      { label: 'Requests (1h)', value: stats?.requests_last_hour ?? '—' },
    ];
    statsEl.innerHTML = items.map(i =>
      `<div class="stat"><div class="k">${i.value}</div><div class="v">${i.label}</div></div>`
    ).join('');
  });
})();
