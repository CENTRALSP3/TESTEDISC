// ===== STATE =====
const state = {
  passo: 0,
  bloco: 'natural',
  most: {},
  least: {},
  shuffled: [],
  sessionId: crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36),
};

function shuffleArray(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function perguntasDoBloco(bloco) {
  const src = bloco === 'natural' ? PERGUNTAS_NATURAL : PERGUNTAS_ADAPTADO;
  return shuffleArray([...src]).map(q => {
    const copy = { ...q, opts: [...q.opts], _shuffled: shuffleArray([...q.opts]) };
    return copy;
  });
}

function shufflePerguntas() {
  state.shuffled = [...perguntasDoBloco('natural'), ...perguntasDoBloco('adaptado')];
}

function questoesAtivas() {
  return state.shuffled.filter(q => q.bloco === state.bloco);
}

function iniciar() {
  document.getElementById('home').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  state.passo = 0;
  state.bloco = 'natural';
  state.most = {};
  state.least = {};
  shufflePerguntas();
  mostrarPergunta();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function mostrarPergunta() {
  const ativas = questoesAtivas();
  const idx = state.passo;
  if (idx >= ativas.length) {
    if (state.bloco === 'natural') { mostrarPausaBloco(); return; }
    mostrarFormNome();
    return;
  }

  const q = ativas[idx];
  const blocoLabel = state.bloco === 'natural' ? 'Perfil Natural' : 'Perfil Adaptado (Trabalho)';
  const totalGeral = TOTAL_POR_BLOCO * 2;
  const offset = state.bloco === 'natural' ? 0 : TOTAL_POR_BLOCO;
  const globalIdx = offset + idx;

  document.getElementById('progressText').textContent = `${globalIdx + 1} de ${totalGeral}`;
  document.getElementById('progressBar').style.width = `${(globalIdx / totalGeral) * 100}%`;
  document.getElementById('blocoLabel').textContent = blocoLabel;

  const container = document.getElementById('quizContainer');
  const optLetters = ['A', 'B', 'C', 'D'];

  let optsHtml = q._shuffled.map((opt, oi) => {
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

  const instrucao = state.bloco === 'natural'
    ? 'Responda como você <strong>naturalmente é</strong> na maioria das situações:'
    : 'Responda como você <strong>age no seu ambiente de trabalho atual</strong>:';

  container.innerHTML = `
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 fade-in card">
      <div class="flex items-center gap-2 mb-4 flex-wrap">
        <span class="text-xs font-bold uppercase tracking-wider px-2 py-1 rounded-full ${state.bloco === 'natural' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}">${blocoLabel}</span>
        <span class="text-xs text-gray-400">${q.tema} · ${idx + 1}/${TOTAL_POR_BLOCO}</span>
      </div>
      <p class="text-base sm:text-lg font-semibold mb-5 leading-relaxed">${instrucao}</p>
      <p class="text-sm text-gray-500 mb-4">Escolha uma opção <strong>MAIS</strong> e uma <strong>MENOS</strong> parecida com você.</p>
      ${optsHtml}
    </div>
    <div class="flex justify-center gap-3 mt-4">
      ${idx > 0 ? '<button onclick="voltar()" class="bg-gray-200 text-gray-700 px-6 py-2.5 rounded-full font-semibold hover:bg-gray-300 transition-all">Voltar</button>' : ''}
      <button onclick="avancar()" class="bg-[#1a1a2e] text-white px-8 py-2.5 rounded-full font-semibold shadow hover:shadow-lg transition-all">
        ${idx < ativas.length - 1 ? 'Próxima →' : (state.bloco === 'natural' ? 'Continuar →' : 'Ver Resultado →')}
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

function iniciarBlocoAdaptado() {
  document.getElementById('pausaBloco').style.display = 'none';
  document.getElementById('quiz').style.display = 'block';
  state.bloco = 'adaptado';
  state.passo = 0;
  mostrarPergunta();
}

function voltar() {
  if (state.passo > 0) { state.passo--; mostrarPergunta(); }
}

function avancar() {
  const q = questoesAtivas()[state.passo];
  const v = validarRespostaQuestao(q.id);
  if (!v.ok) { alert(v.msg); return; }
  state.passo++;
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