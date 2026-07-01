// ===== STATE =====
const state = {
  passo: 0,
  most: {},
  least: {},
  shuffled: [],
  pausaVista: false,
  sessionId: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36),
};

const TOTAL_QUESTOES = TOTAL_POR_BLOCO * 2;
const PAUSA_EM = TOTAL_POR_BLOCO;

function shuffleArray(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function prepararQuestao(q, rotOffset) {
  const opts = [...q.opts];
  const n = opts.length;
  const rotated = [...opts.slice(rotOffset % n), ...opts.slice(0, rotOffset % n)];
  return { ...q, opts: [...q.opts], _shuffled: shuffleArray(rotated) };
}

function perguntasEmbaralhadas() {
  const natural = shuffleArray(PERGUNTAS_NATURAL.map((q, i) => prepararQuestao(q, i * 3 + 1)));
  const adaptado = shuffleArray(PERGUNTAS_ADAPTADO.map((q, i) => prepararQuestao(q, i * 5 + 2)));
  const slots = shuffleArray([...Array(TOTAL_QUESTOES).keys()]);
  const natSlots = slots.slice(0, TOTAL_POR_BLOCO).sort((a, b) => a - b);
  const adpSlots = slots.slice(TOTAL_POR_BLOCO).sort((a, b) => a - b);
  const merged = new Array(TOTAL_QUESTOES);
  natural.forEach((q, i) => { merged[natSlots[i]] = q; });
  adaptado.forEach((q, i) => { merged[adpSlots[i]] = q; });
  return merged;
}

function shufflePerguntas() {
  state.shuffled = perguntasEmbaralhadas();
}

function iniciar() {
  document.getElementById('home').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  state.passo = 0;
  state.most = {};
  state.least = {};
  state.pausaVista = false;
  shufflePerguntas();
  mostrarPergunta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function mostrarPergunta() {
  const idx = state.passo;
  if (idx >= TOTAL_QUESTOES) {
    mostrarFormNome();
    return;
  }

  const q = state.shuffled[idx];

  document.getElementById('progressText').textContent = `${idx + 1} de ${TOTAL_QUESTOES}`;
  document.getElementById('progressBar').style.width = `${((idx + 1) / TOTAL_QUESTOES) * 100}%`;

  const container = document.getElementById('quizContainer');
  const optLetters = ['A', 'B', 'C', 'D'];

  const optsHtml = q._shuffled.map((opt, oi) => {
    const isMost = state.most[q.id] === oi;
    const isLeast = state.least[q.id] === oi;
    return `<div class="opt-card bg-gray-50 dark:bg-gray-800 rounded-xl p-3 sm:p-4 mb-2 ${isMost ? 'most' : ''} ${isLeast ? 'least' : ''}">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-xs font-bold flex-shrink-0">${optLetters[oi]}</span>
        <span class="text-sm text-gray-700 dark:text-gray-200">${opt.t}</span>
      </div>
      <div class="flex gap-2 mt-2 ml-10">
        <button class="btn-most text-xs font-semibold px-3 py-1 rounded-full ${isMost ? 'bg-[#1a1a2e] text-white' : 'bg-gray-200 text-gray-500'} transition-all" data-q="${q.id}" data-idx="${oi}">+ Mais</button>
        <button class="btn-least text-xs font-semibold px-3 py-1 rounded-full ${isLeast ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-500'} transition-all" data-q="${q.id}" data-idx="${oi}">- Menos</button>
      </div>
    </div>`;
  }).join('');

  container.innerHTML = `
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 fade-in card">
      <p class="text-base sm:text-lg font-semibold mb-5 leading-relaxed">Leia as afirmações abaixo e indique quais são <strong>mais</strong> e <strong>menos</strong> parecidas com você.</p>
      <p class="text-sm text-gray-500 mb-4">Responda com sinceridade — não há respostas certas ou erradas.</p>
      ${optsHtml}
    </div>
    <div class="flex justify-center gap-3 mt-4">
      ${idx > 0 ? '<button onclick="voltar()" class="bg-gray-200 text-gray-700 px-6 py-2.5 rounded-full font-semibold hover:bg-gray-300 transition-all">Voltar</button>' : ''}
      <button onclick="avancar()" class="bg-[#1a1a2e] text-white px-8 py-2.5 rounded-full font-semibold shadow hover:shadow-lg transition-all">
        ${idx < TOTAL_QUESTOES - 1 ? 'Próxima →' : 'Concluir →'}
      </button>
    </div>`;

  container.querySelectorAll('.btn-most').forEach(btn => {
    btn.onclick = function(e) {
      e.stopPropagation();
      const qid = this.dataset.q;
      const i = parseInt(this.dataset.idx);
      if (state.least[qid] === i) state.least[qid] = -1;
      state.most[qid] = state.most[qid] === i ? -1 : i;
      mostrarPergunta();
    };
  });
  container.querySelectorAll('.btn-least').forEach(btn => {
    btn.onclick = function(e) {
      e.stopPropagation();
      const qid = this.dataset.q;
      const i = parseInt(this.dataset.idx);
      if (state.most[qid] === i) state.most[qid] = -1;
      state.least[qid] = state.least[qid] === i ? -1 : i;
      mostrarPergunta();
    };
  });
}

function mostrarPausaBloco() {
  document.getElementById('quiz').style.display = 'none';
  document.getElementById('pausaBloco').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function continuarAposPausa() {
  state.pausaVista = true;
  document.getElementById('pausaBloco').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  mostrarPergunta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function voltar() {
  if (state.passo > 0) {
    if (state.passo === PAUSA_EM && state.pausaVista) {
      state.pausaVista = false;
      document.getElementById('pausaBloco').style.display = 'none';
      document.getElementById('quiz').style.display = 'block';
    }
    state.passo--;
    mostrarPergunta();
  }
}

function avancar() {
  const q = state.shuffled[state.passo];
  const v = validarRespostaQuestao(q.id);
  if (!v.ok) { alert(v.msg); return; }
  state.passo++;
  if (state.passo === PAUSA_EM && !state.pausaVista) {
    mostrarPausaBloco();
    return;
  }
  mostrarPergunta();
}

function mostrarFormNome() {
  document.getElementById('progressBar').style.width = '100%';
  document.getElementById('quiz').style.display = 'none';
  document.getElementById('nameForm').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function gerarRelatorio() {
  const nome = document.getElementById('userName').value.trim();
  if (!nome) {
    document.getElementById('nameError').classList.remove('hidden');
    return;
  }
  document.getElementById('nameError').classList.add('hidden');
  document.getElementById('nameForm').style.display = 'none';
  calcularERenderizar(nome);
}

function refazer() {
  document.getElementById('resultado').style.display = 'none';
  document.getElementById('home').style.display = 'block';
  ['_chartNat', '_chartAdp', '_chartPress'].forEach(k => {
    if (window[k]) { window[k].destroy(); window[k] = null; }
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}