// ===== STATE =====
const state = {
  passo: 0,
  most: {},
  least: {},
  shuffled: []
};

// ===== SHUFFLE =====
function shuffleArray(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shufflePerguntas() {
  state.shuffled = shuffleArray([...PERGUNTAS]);
  state.shuffled.forEach(q => {
    q._shuffled = shuffleArray([...q.opts]);
  });
}

// ===== INICIAR =====
function iniciar() {
  document.getElementById('home').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  state.passo = 0;
  state.most = {};
  state.least = {};
  shufflePerguntas();
  mostrarPergunta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== QUIZ UI =====
function mostrarPergunta() {
  const total = state.shuffled.length;
  const idx = state.passo;
  if (idx >= total) { mostrarFormNome(); return; }

  const q = state.shuffled[idx];
  document.getElementById('progressText').textContent = `${idx + 1} de ${total}`;
  document.getElementById('progressBar').style.width = `${(idx / total) * 100}%`;

  const container = document.getElementById('quizContainer');
  const optLetters = ['A', 'B', 'C', 'D'];
  const validacao = validarRespostaQuestao(q.id);
  const alertHtml = !validacao.ok && (state.most[q.id] !== undefined || state.least[q.id] !== undefined)
    ? `<div class="text-amber-600 text-sm mb-3 bg-amber-50 p-3 rounded-lg">${validacao.msg}</div>` : '';

  let optsHtml = q._shuffled.map((opt, oi) => {
    const isMost = state.most[q.id] === oi;
    const isLeast = state.least[q.id] === oi;
    return `<div class="opt-card bg-gray-50 rounded-xl p-3 sm:p-4 mb-2 ${isMost ? 'most' : ''} ${isLeast ? 'least' : ''}">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold flex-shrink-0">${optLetters[oi]}</span>
        <span class="text-sm text-gray-700">${opt.t}</span>
      </div>
      <div class="flex gap-2 mt-2 ml-10">
        <button class="btn-most text-xs font-semibold px-3 py-1 rounded-full ${isMost ? 'bg-[#1a1a2e] text-white' : 'bg-gray-200 text-gray-500'} transition-all" data-q="${q.id}" data-idx="${oi}">+ Mais</button>
        <button class="btn-least text-xs font-semibold px-3 py-1 rounded-full ${isLeast ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-500'} transition-all" data-q="${q.id}" data-idx="${oi}">- Menos</button>
      </div>
    </div>`;
  }).join('');

  container.innerHTML = `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 fade-in">
      <div class="flex items-center gap-2 mb-4">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">${q.tema}</span>
        <span class="text-gray-300">·</span>
        <span class="text-xs text-gray-400">Questão ${idx + 1} de ${total}</span>
      </div>
      <p class="text-base sm:text-lg font-semibold mb-5 leading-relaxed">Escolha uma opção para <strong>MAIS</strong> e uma para <strong>MENOS</strong> se parece com você:</p>
      ${alertHtml}
      ${optsHtml}
    </div>
    <div class="flex justify-center gap-3 mt-4">
      ${idx > 0 ? '<button onclick="voltar()" class="bg-gray-200 text-gray-700 px-6 py-2.5 rounded-full font-semibold hover:bg-gray-300 transition-all">Voltar</button>' : ''}
      <button onclick="avancar()" class="bg-[#1a1a2e] text-white px-8 py-2.5 rounded-full font-semibold shadow hover:shadow-lg transition-all" id="btnAvancar">
        ${idx < total - 1 ? 'Próxima →' : 'Ver Resultado →'}
      </button>
    </div>`;

  container.querySelectorAll('.btn-most').forEach(btn => {
    btn.onclick = function(e) {
      e.stopPropagation();
      const qid = this.dataset.q;
      const idx = parseInt(this.dataset.idx);
      if (state.least[qid] === idx) state.least[qid] = -1;
      state.most[qid] = state.most[qid] === idx ? -1 : idx;
      mostrarPergunta();
    };
  });
  container.querySelectorAll('.btn-least').forEach(btn => {
    btn.onclick = function(e) {
      e.stopPropagation();
      const qid = this.dataset.q;
      const idx = parseInt(this.dataset.idx);
      if (state.most[qid] === idx) state.most[qid] = -1;
      state.least[qid] = state.least[qid] === idx ? -1 : idx;
      mostrarPergunta();
    };
  });
}

function voltar() {
  if (state.passo > 0) { state.passo--; mostrarPergunta(); }
}

function avancar() {
  const q = state.shuffled[state.passo];
  const validacao = validarRespostaQuestao(q.id);
  if (!validacao.ok) {
    alert(validacao.msg);
    return;
  }
  state.passo++;
  mostrarPergunta();
}

// ===== FORM NOME =====
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

// ===== REFAZER =====
function refazer() {
  document.getElementById('resultado').style.display = 'none';
  document.getElementById('home').style.display = 'block';
  if (window._chart) { window._chart.destroy(); window._chart = null; }
  window.scrollTo({ top: 0, behavior: 'smooth' });
}