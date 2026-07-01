// ===== SCORING V2 — Natural + Adaptado =====

function normalizeRaw(raw, itemCount) {
  const divisor = itemCount / 10; // 28 itens → divisor 2.8 → range -10/+10
  const scores = {};
  FACTORES.forEach(f => {
    scores[f] = Math.max(-10, Math.min(10, Math.round(raw[f] / divisor * 10) / 10));
  });
  return scores;
}

function calcularScores(respostas, itemCount = TOTAL_POR_BLOCO) {
  const raw = { D: 0, I: 0, S: 0, C: 0 };
  respostas.forEach(q => {
    if (q.mostFactor) raw[q.mostFactor] += 1;
    if (q.leastFactor) raw[q.leastFactor] -= 1;
  });
  return { raw, scores: normalizeRaw(raw, itemCount) };
}

function respostasDoBloco(bloco) {
  return state.shuffled
    .filter(q => q.bloco === bloco)
    .map(q => ({
      mostFactor: state.most[q.id] !== undefined && state.most[q.id] !== -1
        ? q._shuffled[state.most[q.id]].f : null,
      leastFactor: state.least[q.id] !== undefined && state.least[q.id] !== -1
        ? q._shuffled[state.least[q.id]].f : null,
    }));
}

function calcularScoresDual() {
  const natural = calcularScores(respostasDoBloco('natural'));
  const adapted = calcularScores(respostasDoBloco('adaptado'));
  const discrepancy = {};
  const pressure = {};
  FACTORES.forEach(f => {
    discrepancy[f] = Math.round((adapted.scores[f] - natural.scores[f]) * 10) / 10;
    pressure[f] = discrepancy[f];
  });
  return { natural: natural.scores, adapted: adapted.scores, discrepancy, pressure };
}

function determinarPerfil(scores) {
  const sorted = FACTORES.slice().sort((a, b) => scores[b] - scores[a]);
  const primario = sorted[0];
  const secundario = scores[sorted[1]] > 0 ? sorted[1] : null;
  const terciario = (
    secundario && scores[sorted[2]] > 0 &&
    Math.abs(scores[sorted[2]] - scores[sorted[1]]) < 2
  ) ? sorted[2] : null;
  let blend = primario;
  if (secundario) blend += secundario;
  if (terciario) blend += terciario;
  return { primario, secundario, terciario, blend, sorted };
}

function classificarScore(valor) {
  if (Math.abs(valor) > ZONA_CINZENTA) return 'Zona Cinzenta';
  if (valor > 5) return 'Alto';
  if (valor > 2) return 'Médio-Alto';
  if (valor > -2) return 'Médio';
  if (valor > -5) return 'Médio-Baixo';
  if (valor > -ZONA_CINZENTA) return 'Baixo';
  return 'Zona Cinzenta';
}

function getFatoresAtivos(scores, minScore = 0) {
  return FACTORES.filter(f => scores[f] > minScore).sort((a, b) => scores[b] - scores[a]);
}

function getFatoresPonderados(scores, maxFatores = 2) {
  const ativos = getFatoresAtivos(scores, 1);
  if (!ativos.length) return [FACTORES.slice().sort((a, b) => scores[b] - scores[a])[0]];
  const result = [ativos[0]];
  if (ativos.length > 1 && scores[ativos[1]] >= scores[ativos[0]] - 3) result.push(ativos[1]);
  return result.slice(0, maxFatores);
}

function analisarDiscrepancia(dual) {
  const alertas = [];
  FACTORES.forEach(f => {
    const d = dual.discrepancy[f];
    const nat = dual.natural[f];
    const adp = dual.adapted[f];
    if (d <= -DISCREPANCY_THRESHOLD && nat > 2) {
      alertas.push({ fator: f, tipo: 'supressao', delta: d,
        texto: `Fator ${f}: possível supressão no trabalho (natural +${nat} → adaptado +${adp}). Pode indicar ambiente que não permite expressar esse traço.` });
    } else if (d >= DISCREPANCY_THRESHOLD && nat < adp) {
      alertas.push({ fator: f, tipo: 'hiperadaptacao', delta: d,
        texto: `Fator ${f}: possível hiperadaptação (+${d}). Você pode estar forçando comportamentos além do seu perfil natural.` });
    }
  });
  return alertas;
}

function validarRespostaQuestao(qid) {
  const most = state.most[qid];
  const least = state.least[qid];
  if (most === undefined || most === -1) return { ok: false, msg: 'Selecione a opção que MAIS se parece com você.' };
  if (least === undefined || least === -1) return { ok: false, msg: 'Selecione a opção que MENOS se parece com você.' };
  if (most === least) return { ok: false, msg: 'A opção MAIS e MENOS devem ser diferentes.' };
  return { ok: true };
}