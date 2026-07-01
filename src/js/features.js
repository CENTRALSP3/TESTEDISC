// ===== FEATURES: Dark mode, Share, PDF, PWA =====

function initDarkMode() {
  const saved = localStorage.getItem('disc-theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
  }
}

function toggleDarkMode() {
  document.documentElement.classList.toggle('dark');
  localStorage.setItem('disc-theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
}

async function salvarResultadoAnonimo(dual, perfil) {
  if (!API_BASE) return;
  try {
    await fetch(`${API_BASE}/responses`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.sessionId,
        instrument_version: INSTRUMENT_VERSION,
        natural: dual.natural,
        adapted: dual.adapted,
        blend: perfil.blend,
      }),
    });
  } catch (_) { /* offline ok */ }
}

async function inferirViaAPI(dual) {
  if (!API_BASE) return null;
  try {
    const resp = await fetch(`${API_BASE}/infer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ natural: dual.natural, adapted: dual.adapted, share: true }),
    });
    if (!resp.ok) return null;
    return await resp.json();
  } catch (_) { return null; }
}

function gerarLinkCompartilhamento(hash) {
  if (!hash) return '';
  const url = `${window.location.origin}${window.location.pathname}?r=${hash}`;
  return url;
}

async function copiarLink(hash) {
  const url = gerarLinkCompartilhamento(hash);
  if (!url) { alert('Link não disponível (modo offline).'); return; }
  try {
    await navigator.clipboard.writeText(url);
    alert('Link copiado para a área de transferência!');
  } catch (_) {
    prompt('Copie o link:', url);
  }
}

function exportarPDF() {
  window.print();
}

async function carregarResultadoCompartilhado() {
  const params = new URLSearchParams(window.location.search);
  const hash = params.get('r');
  if (!hash || !API_BASE) return false;
  try {
    const resp = await fetch(`${API_BASE}/result/${hash}`);
    if (!resp.ok) return false;
    const data = await resp.json();
    const dual = { natural: data.natural, adapted: data.adapted,
      discrepancy: {}, pressure: {} };
    FACTORES.forEach(f => {
      dual.discrepancy[f] = Math.round((data.adapted[f] - data.natural[f]) * 10) / 10;
      dual.pressure[f] = dual.discrepancy[f];
    });
    document.getElementById('home').style.display = 'none';
    calcularERenderizar(data.name || 'Resultado Compartilhado', dual, data);
    return true;
  } catch (_) { return false; }
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  carregarResultadoCompartilhado();
});