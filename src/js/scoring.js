// ===== SCORING =====

function calcularScores(respostas) {
  const raw = { D: 0, I: 0, S: 0, C: 0 };
  respostas.forEach(q => {
    if (q.mostIdx !== undefined && q.mostIdx !== -1) {
      raw[q.mostFactor] += 1;
    }
    if (q.leastIdx !== undefined && q.leastIdx !== -1) {
      raw[q.leastFactor] -= 1;
    }
  });
  const scores = {};
  FACTORES.forEach(f => {
    scores[f] = Math.max(-10, Math.min(10, Math.round(raw[f] / 4 * 10) / 10));
  });
  return { raw, scores };
}

function calcularScoresFromState() {
  const respostas = state.shuffled.map(q => ({
    mostIdx: state.most[q.id],
    leastIdx: state.least[q.id],
    mostFactor: state.most[q.id] !== undefined && state.most[q.id] !== -1
      ? q._shuffled[state.most[q.id]].f : null,
    leastFactor: state.least[q.id] !== undefined && state.least[q.id] !== -1
      ? q._shuffled[state.least[q.id]].f : null,
  }));
  return calcularScores(respostas).scores;
}

/** Lógica canônica de blend — única fonte de verdade */
function determinarPerfil(scores) {
  const sorted = FACTORES.slice().sort((a, b) => scores[b] - scores[a]);
  const primario = sorted[0];
  const secundario = scores[sorted[1]] > 0 ? sorted[1] : null;
  const terciario = (
    secundario &&
    scores[sorted[2]] > 0 &&
    Math.abs(scores[sorted[2]] - scores[sorted[1]]) < 2
  ) ? sorted[2] : null;

  let blend = primario;
  if (secundario) blend += secundario;
  if (terciario) blend += terciario;

  return { primario, secundario, terciario, blend, sorted };
}

function classificarScore(valor) {
  if (Math.abs(valor) > 8) return 'Zona Cinzenta';
  if (valor > 5) return 'Alto';
  if (valor > 2) return 'Médio-Alto';
  if (valor > -2) return 'Médio';
  if (valor > -5) return 'Médio-Baixo';
  if (valor > -8) return 'Baixo';
  return 'Zona Cinzenta';
}

/** Fatores com influência significativa, ordenados por score */
function getFatoresAtivos(scores, minScore = 0) {
  return FACTORES
    .filter(f => scores[f] > minScore)
    .sort((a, b) => scores[b] - scores[a]);
}

/** Fatores ponderados para devolutiva multi-fator */
function getFatoresPonderados(scores, maxFatores = 2) {
  const ativos = getFatoresAtivos(scores, 1);
  if (!ativos.length) {
    const sorted = FACTORES.slice().sort((a, b) => scores[b] - scores[a]);
    return [sorted[0]];
  }
  const result = [ativos[0]];
  if (ativos.length > 1 && scores[ativos[1]] >= scores[ativos[0]] - 3) {
    result.push(ativos[1]);
  }
  return result.slice(0, maxFatores);
}

function validarRespostaQuestao(qid) {
  const most = state.most[qid];
  const least = state.least[qid];
  if (most === undefined || most === -1) return { ok: false, msg: 'Selecione a opção que MAIS se parece com você.' };
  if (least === undefined || least === -1) return { ok: false, msg: 'Selecione a opção que MENOS se parece com você.' };
  if (most === least) return { ok: false, msg: 'A opção MAIS e MENOS devem ser diferentes.' };
  return { ok: true };
}