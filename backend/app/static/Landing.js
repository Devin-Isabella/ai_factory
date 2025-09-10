async function j(method, url, body){
  const opt = { method, headers:{'Content-Type':'application/json'} };
  if(body) opt.body = JSON.stringify(body);
  const r = await fetch(url, opt);
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}

function setPill(ok){
  const pill = document.getElementById('health');
  pill.className = 'pill ' + (ok===true ? 'pill-green' : ok===false ? 'pill-red' : 'pill-amber');
  pill.textContent = ok===true ? 'healthy' : ok===false ? 'unhealthy' : 'checking…';
}

async function probe(){
  try{
    const h = await j('GET','/health');
    setPill(h.status==='ok');
    document.getElementById('sHealth').textContent = h.status || 'unknown';
  }catch{ setPill(false); document.getElementById('sHealth').textContent = 'error'; }

  try{
    const s = await j('GET','/store/search?page=1&size=1&sort=created_desc');
    const n = (s.items && s.items.length) ? `${s.items.length}+` : '0';
    document.getElementById('sStore').textContent = `OK (${n} visible)`;
  }catch{ document.getElementById('sStore').textContent = 'error'; }

  try{
    const m = await j('GET','/monitor/stats');
    const cpu = (m && typeof m.cpu === 'number') ? `${m.cpu}%` : 'n/a';
    document.getElementById('sStats').textContent = `OK (CPU ${cpu})`;
  }catch{ document.getElementById('sStats').textContent = 'error'; }
}

document.getElementById('loginForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const email = document.getElementById('email').value.trim();
  const name  = document.getElementById('name').value.trim() || 'Mobile User';
  const out   = document.getElementById('tokenBox');
  out.textContent = 'Requesting token…';
  try{
    const r = await j('POST','/auth/login',{email, name});
    out.textContent = JSON.stringify(r,null,2);
  }catch(err){
    out.textContent = 'Error: ' + err.message;
  }
});

probe();
setInterval(probe, 15000);
