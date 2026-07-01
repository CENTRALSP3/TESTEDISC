// ===== DEVOLUTIVA V2 — 12 SEÇÕES =====

const ONTOLOGY_UI = {
  D: { motivacao: 'Desafios, autonomia, resultados tangíveis e oportunidades de liderar.',
       enfase: 'Posições com metas claras, decisões rápidas e autonomia para agir.',
       comunicar_fazer: 'Seja direto, objetivo e focado em resultados.',
       comunicar_evitar: 'Evite rodeios, burocracia excessiva e reuniões longas sem decisão.',
       medo: 'Perder controle ou ser explorado por outros.' },
  I: { motivacao: 'Reconhecimento, interação social, variedade e ambiente positivo.',
       enfase: 'Funções com contato humano, criatividade e espaço para se expressar.',
       comunicar_fazer: 'Seja aberto, entusiasta e reconheça contribuições.',
       comunicar_evitar: 'Evite isolamento, críticas públicas e ambientes frios.',
       medo: 'Rejeição social ou perda de influência.' },
  S: { motivacao: 'Segurança, estabilidade, reconhecimento sincero e rotina previsível.',
       enfase: 'Funções com processos claros, equipe estável e mudanças graduais.',
       comunicar_fazer: 'Seja paciente, ofereça segurança e explique mudanças com antecedência.',
       comunicar_evitar: 'Evite pressa, mudanças abruptas e tom agressivo.',
       medo: 'Mudanças inesperadas e instabilidade.' },
  C: { motivacao: 'Precisão, qualidade, expertise técnica e padrões bem definidos.',
       enfase: 'Funções analíticas com tempo para análise e critérios objetivos.',
       comunicar_fazer: 'Traga dados, seja específico e respeite padrões.',
       comunicar_evitar: 'Evite generalizações, improviso e pressão por decisões sem dados.',
       medo: 'Críticas à qualidade do trabalho ou erros públicos.' },
};

const TEXTOS = {
  descricao: {
    D: { alto: 'Perfil direto, orientado a resultados, com energia para superar obstáculos e tomar decisões rápidas.',
         baixo: 'Perfil cooperativo que valoriza consenso e evita confrontos desnecessários.' },
    I: { alto: 'Perfil comunicativo e entusiasmado, que energiza grupos e constrói conexões.',
         baixo: 'Perfil mais reservado, com preferência por relações profundas em vez de amplitude social.' },
    S: { alto: 'Perfil estável, leal e consistente, que traz segurança e harmonia às equipes.',
         baixo: 'Perfil dinâmico que prefere variedade e mudanças a rotinas rígidas.' },
    C: { alto: 'Perfil analítico e criterioso, orientado a qualidade, precisão e padrões elevados.',
         baixo: 'Perfil flexível com regras, que prefere autonomia a procedimentos rígidos.' },
  },
  forcas: {
    D: ['Decisões rápidas', 'Orientação a resultados', 'Iniciativa', 'Determinação'],
    I: ['Comunicação persuasiva', 'Motivação de equipes', 'Criatividade', 'Networking'],
    S: ['Confiabilidade', 'Paciência', 'Lealdade', 'Estabilidade em crises'],
    C: ['Precisão analítica', 'Atenção a detalhes', 'Qualidade', 'Rigor técnico'],
  },
  atencao: {
    D: ['Pode parecer impaciente', 'Risco de atropelar processos', 'Dificuldade com detalhes', 'Frustração com ritmos lentos'],
    I: ['Pode parecer disperso', 'Dificuldade com prazos', 'Evita confrontos', 'Otimismo excessivo'],
    S: ['Resistência a mudanças', 'Hesitação em decisões rápidas', 'Evita conflitos', 'Dificuldade em se posicionar'],
    C: ['Paralisia por análise', 'Pode parecer crítico', 'Dificuldade com ambiguidade', 'Perfeccionismo'],
  },
  comunicacao: {
    D: 'Comunicação direta e orientada a resultados.',
    I: 'Comunicação expressiva, entusiasta e persuasiva.',
    S: 'Comunicação calma, acolhedora e consistente.',
    C: 'Comunicação técnica, precisa e fundamentada em dados.',
  },
  pressao: {
    D: 'Assume controle e busca soluções rápidas. Risco de impulsividade.',
    I: 'Busca apoio social. Risco de dispersão se isolado.',
    S: 'Busca estabilidade. Risco de hesitação em urgências.',
    C: 'Aprofunda análise. Risco de paralisia por excesso de informação.',
  },
  percepcao: {
    D: 'Projeta confiança e objetividade. Pode ser visto como assertivo ou autoritário.',
    I: 'Percebido como carismático e comunicativo. Pode parecer superficial em excesso.',
    S: 'Transmite calma e confiabilidade. Pode parecer resistente a mudanças.',
    C: 'Percebido como criterioso e competente. Pode parecer excessivamente crítico.',
  },
  recomendacoes: {
    D: ['Pratique escuta ativa', 'Valorize perfis analíticos', 'Faça pausas antes de decidir', 'Delegue mais'],
    I: ['Equilibre entusiasmo com prazos', 'Documente acordos', 'Desenvolva resiliência a críticas', 'Aprofunde antes de compartilhar'],
    S: ['Comunique mudanças abertamente', 'Saia da zona de conforto gradualmente', 'Desenvolva assertividade', 'Posicione-se mais cedo'],
    C: ['Equilibre análise com ação', 'Aceite informação parcial', 'Pratique decisões com prazo', 'Compartilhe conhecimento'],
  },
  equipe: {
    D: ['Direcionamento e resultados', 'Decisões difíceis', 'Energia para obstáculos', 'Visão estratégica'],
    I: ['Motivação e energia', 'Ideias criativas', 'Networking', 'Engajamento'],
    S: ['Estabilidade', 'Suporte à equipe', 'Consistência', 'Harmonia'],
    C: ['Análise crítica', 'Qualidade', 'Padrões elevados', 'Rigor técnico'],
  },
};

const blendDescriptions = {
  D: 'Foco em resultados e ação', I: 'Foco em pessoas e comunicação',
  S: 'Foco em estabilidade e harmonia', C: 'Foco em qualidade e análise',
  DI: 'Resultados através de influência', ID: 'Comunicação direcionada a metas',
  DS: 'Determinação com estabilidade', SD: 'Estabilidade com ação',
  DC: 'Resultados com critério', CD: 'Qualidade orientada a resultados',
  IS: 'Influência acolhedora', SI: 'Conexão consistente',
  SC: 'Análise consistente', CS: 'Qualidade estável',
  IC: 'Comunicação analítica', CI: 'Análise comunicativa',
};

function getTextoPorScore(f, score) {
  return score > 0 ? TEXTOS.descricao[f].alto : TEXTOS.descricao[f].baixo;
}

function capitalizar(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

function palavrasPorFator(f, score) {
  const pdf = (PALAVRAS_PDF && PALAVRAS_PDF[f]) || [];
  const fb = PALAVRAS_FALLBACK[f];
  const intensidade = score > 5 ? 'alto' : score > 0 ? 'medio' : 'baixo';
  const qtd = score > 5 ? 4 : score > 0 ? 3 : 2;
  const fromPdf = pdf.filter(w => !w.startsWith('não ')).slice(0, qtd).map(capitalizar);
  const fromFb = (fb[intensidade] || []).slice(0, qtd);
  return [...new Set([...fromPdf, ...fromFb])].slice(0, qtd);
}

function gerarDescritivo(scores, sorted) {
  const palavras = [];
  sorted.forEach(f => palavras.push(...palavrasPorFator(f, scores[f])));
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">4. Palavras Descritivas</h3>
    <div class="flex flex-wrap gap-2">${[...new Set(palavras)].slice(0, 12).map(p =>
      `<span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-full text-sm font-medium">${p}</span>`).join('')}</div>
  </div>`;
}

function gerarSecaoMultiFator(titulo, num, scores, fonte) {
  const fatores = getFatoresPonderados(scores);
  const blocos = fatores.map(f => `
    <div class="mb-3 ${fatores.length > 1 ? 'pl-3 border-l-4' : ''}" style="${fatores.length > 1 ? 'border-color:'+CORES[f] : ''}">
      ${fatores.length > 1 ? `<span class="text-xs font-bold" style="color:${CORES[f]}">${f}</span>` : ''}
      <p class="text-gray-600 dark:text-gray-300 text-sm mt-1">${fonte[f]}</p>
    </div>`).join('');
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">${num}. ${titulo}</h3>${blocos}</div>`;
}

function gerarMotivacao(perfil) {
  const f = perfil.primario;
  const o = ONTOLOGY_UI[f];
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">5. Auto Motivação</h3>
    <p class="text-gray-600 dark:text-gray-300">${o.motivacao}</p>
    <p class="text-sm text-gray-400 mt-2">Medo fundamental: ${o.medo}</p>
  </div>`;
}

function gerarEnfaseTrabalho(perfil) {
  const o = ONTOLOGY_UI[perfil.primario];
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">6. Ênfase no Trabalho</h3>
    <p class="text-gray-600 dark:text-gray-300">${o.enfase}</p>
  </div>`;
}

function gerarComunicacaoGuia(perfil) {
  const f = perfil.primario;
  const o = ONTOLOGY_UI[f];
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">9. Guia de Comunicação</h3>
    <p class="text-sm mb-2"><strong class="text-green-600">Faça:</strong> ${o.comunicar_fazer}</p>
    <p class="text-sm"><strong class="text-red-600">Evite:</strong> ${o.comunicar_evitar}</p>
  </div>`;
}

function gerarDiscrepancia(dual) {
  const alertas = analisarDiscrepancia(dual);
  if (!alertas.length) return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">10. Análise de Discrepância (Natural vs Adaptado)</h3>
    <p class="text-gray-600 text-sm">Seu comportamento natural e adaptado estão alinhados. O ambiente parece compatível com seu perfil.</p>
  </div>`;
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 border-2 border-amber-200 fade-in">
    <h3 class="text-lg font-bold mb-4">10. Análise de Discrepância (Natural vs Adaptado)</h3>
    ${alertas.map(a => `<div class="p-3 mb-2 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-sm">${a.texto}</div>`).join('')}
  </div>`;
}

function gerarInferenciaAPI(apiResult) {
  if (!apiResult) return '';
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 border-l-4 border-blue-500 fade-in">
    <h3 class="text-lg font-bold mb-4">12. Interpretação Avançada</h3>
    <p class="text-gray-700 dark:text-gray-200 font-medium">${apiResult.interpretation}</p>
    ${apiResult.matched_rules?.length ? `<p class="text-xs text-gray-400 mt-2">Regras: ${apiResult.matched_rules.join(', ')}</p>` : ''}
    ${apiResult.share_hash ? `<button onclick="copiarLink('${apiResult.share_hash}')" class="mt-3 text-sm text-blue-600 underline">Copiar link para compartilhar</button>` : ''}
  </div>`;
}

function gerarListaSecao(titulo, num, scores, fonte) {
  const itens = [];
  getFatoresAtivos(scores, 0).forEach(f => { if (fonte[f]) itens.push(...fonte[f]); });
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">${num}. ${titulo}</h3>
    <ul class="space-y-2">${itens.slice(0, 8).map(i =>
      `<li class="flex gap-2 text-sm text-gray-600 dark:text-gray-300"><span class="text-green-500">✓</span>${i}</li>`).join('')}</ul>
  </div>`;
}

function gerarSecaoPerfil(perfil, scores) {
  const desc = getTextoPorScore(perfil.primario, scores[perfil.primario]);
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
    <h3 class="text-lg font-bold mb-4">3. Visão Geral do Perfil</h3>
    <div class="flex items-center gap-3 mb-4 flex-wrap">
      <span class="px-4 py-1.5 rounded-full text-white font-bold text-sm" style="background:${CORES[perfil.primario]}">${perfil.blend}</span>
      <span class="text-gray-600 dark:text-gray-300">${blendDescriptions[perfil.blend] || 'Perfil combinado'}</span>
    </div>
    <p class="text-gray-600 dark:text-gray-300">${desc}</p>
  </div>`;
}

function gerarSecaoZona(scores) {
  const naZona = FACTORES.filter(f => Math.abs(scores[f]) > ZONA_CINZENTA);
  if (!naZona.length) return '';
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 border-2 border-red-200 fade-in">
    <h3 class="text-lg font-bold mb-4">11. Zona Cinzenta</h3>
    ${naZona.map(f => `<div class="p-3 mb-2 rounded-xl" style="background:${CORES[f]}15;border-left:4px solid ${CORES[f]}">
      <strong style="color:${CORES[f]}">${f} (${scores[f] > 0 ? '+' : ''}${scores[f]})</strong>
      <p class="text-sm text-gray-600 mt-1">${scores[f] > 0 ? 'Traço muito pronunciado — moderação recomendada.' : 'Traço muito baixo — área de desenvolvimento.'}</p>
    </div>`).join('')}
  </div>`;
}

function gerarDisclaimer() {
  return `<div class="text-center text-xs text-gray-400 mt-8 pt-4 border-t space-y-1">
    <p>Instrumento de autoconhecimento DISC v${INSTRUMENT_VERSION}. Não substitui avaliação psicológica profissional.</p>
    <p>Normas populacionais em coleta — resultados indicativos baseados em autorrelato.</p>
  </div>`;
}

async function calcularERenderizar(nome, dualPrecomputed, apiPrecomputed) {
  const dual = dualPrecomputed || calcularScoresDual();
  const perfilNat = determinarPerfil(dual.natural);
  const perfilAdp = determinarPerfil(dual.adapted);
  const hoje = new Date().toLocaleDateString('pt-BR');

  let apiResult = apiPrecomputed;
  if (!apiResult) {
    apiResult = await inferirViaAPI(dual);
    salvarResultadoAnonimo(dual, perfilNat);
  }

  document.getElementById('resultadoContainer').innerHTML = `
    <div id="printArea">
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold">Perfil Comportamental DISC</h2>
        <p class="text-gray-500 mt-1">${nome} · ${hoje}</p>
        <div class="flex flex-wrap justify-center gap-2 mt-3">
          <span class="bg-green-700 text-white px-4 py-1.5 rounded-full text-sm font-bold">Natural: ${perfilNat.blend}</span>
          <span class="bg-blue-700 text-white px-4 py-1.5 rounded-full text-sm font-bold">Adaptado: ${perfilAdp.blend}</span>
        </div>
      </div>
      ${gerarGraficosTriplos(dual)}
      ${gerarSecaoPerfil(perfilNat, dual.natural)}
      ${gerarDescritivo(dual.natural, perfilNat.sorted)}
      ${gerarMotivacao(perfilNat)}
      ${gerarEnfaseTrabalho(perfilNat)}
      ${gerarListaSecao('Forças / Pontos Fortes', 7, dual.natural, TEXTOS.forcas)}
      ${gerarListaSecao('Pontos de Atenção', 8, dual.natural, TEXTOS.atencao)}
      ${gerarComunicacaoGuia(perfilNat)}
      ${gerarSecaoMultiFator('Comportamento sob Pressão', 10, dual.adapted, TEXTOS.pressao)}
      ${gerarDiscrepancia(dual)}
      ${gerarSecaoZona(dual.natural)}
      ${gerarListaSecao('Recomendações Práticas', 11, dual.natural, TEXTOS.recomendacoes)}
      ${gerarInferenciaAPI(apiResult)}
      ${gerarDisclaimer()}
      <div class="flex flex-wrap justify-center gap-3 mt-8 no-print">
        <button onclick="exportarPDF()" class="bg-[#1a1a2e] text-white px-6 py-2.5 rounded-full font-semibold">PDF / Imprimir</button>
        <button onclick="toggleDarkMode()" class="bg-gray-200 px-6 py-2.5 rounded-full font-semibold">Modo Escuro</button>
        ${apiResult?.share_hash ? `<button onclick="copiarLink('${apiResult.share_hash}')" class="bg-blue-600 text-white px-6 py-2.5 rounded-full font-semibold">Compartilhar</button>` : ''}
        <button onclick="refazer()" class="bg-gray-200 px-6 py-2.5 rounded-full font-semibold">Refazer</button>
      </div>
    </div>`;

  document.getElementById('resultado').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => initGraficosTriplos(dual), 100);
}