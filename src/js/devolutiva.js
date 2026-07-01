// ===== TEXTOS DEVOLUTIVA =====
const TEXTOS = {
  descricao: {
    D: { alto: 'Pessoas com D alto são diretas, orientadas a resultados, gostam de desafios e tomam decisões rápidas. Têm alta energia para superar obstáculos.', baixo: 'D baixo sugere perfil mais cooperativo, que prefere evitar confrontos e valoriza consenso em vez de competição direta.' },
    I: { alto: 'Pessoas com I alto são comunicativas, entusiasmadas, gostam de interagir e influenciar pessoas. Trazem energia positiva aos grupos.', baixo: 'I baixo sugere perfil mais reservado, que prefere profundidade nas relações em vez de amplitude social.' },
    S: { alto: 'Pessoas com S alto são estáveis, consistentes, leais e valorizam harmonia. Trazem segurança e confiabilidade às equipes.', baixo: 'S baixo sugere preferência por dinamismo, mudanças e variedade em vez de rotinas previsíveis.' },
    C: { alto: 'Pessoas com C alto são analíticas, precisas, criteriosas e valorizam qualidade. Seguem padrões e buscam excelência técnica.', baixo: 'C baixo sugere perfil mais flexível com regras, que prefere autonomia e não se prende a procedimentos rígidos.' }
  },
  forcas: {
    D: ['Capacidade de tomar decisões rápidas', 'Orientação a resultados e metas', 'Iniciativa e proatividade', 'Enfrenta desafios com determinação'],
    I: ['Comunicação persuasiva e envolvente', 'Capacidade de motivar equipes', 'Criatividade e otimismo', 'Facilidade para networking'],
    S: ['Confiabilidade e consistência', 'Paciência e capacidade de ouvir', 'Lealdade à equipe', 'Estabilidade em momentos de crise'],
    C: ['Precisão e atenção aos detalhes', 'Pensamento analítico e crítico', 'Compromisso com qualidade', 'Seguimento de padrões e processos']
  },
  atencao: {
    D: ['Pode ser visto como autoritário ou impaciente', 'Risco de atropelar processos e pessoas', 'Dificuldade com burocracia e detalhes', 'Pode se frustrar com ritmos mais lentos'],
    I: ['Pode ser visto como disperso ou superficial', 'Dificuldade com follow-through e prazos', 'Evita confrontos necessários', 'Pode ser excessivamente otimista'],
    S: ['Resistência a mudanças necessárias', 'Dificuldade com decisões rápidas', 'Pode evitar conflitos importantes', 'Dificuldade em se posicionar'],
    C: ['Paralisia por análise', 'Pode ser visto como crítico ou frio', 'Dificuldade com ambiguidade', 'Perfeccionismo pode atrasar entregas']
  },
  comunicacao: {
    D: 'Comunicação direta, objetiva e focada em resultados. Prefere mensagens claras sem rodeios.',
    I: 'Comunicação expressiva, entusiasta e persuasiva. Valoriza troca de ideias e reconhecimento.',
    S: 'Comunicação calma, acolhedora e consistente. Prefere diálogos harmoniosos e sem pressa.',
    C: 'Comunicação técnica, precisa e fundamentada em dados. Valoriza argumentos lógicos e específicos.'
  },
  pressao: {
    D: 'Sob pressão, tende a assumir o controle e buscar soluções rápidas. Risco de impaciência e decisões impulsivas.',
    I: 'Sob pressão, busca apoio social e validação. Risco de dispersão se isolado ou sem reconhecimento.',
    S: 'Sob pressão, tende a se retrair e buscar estabilidade. Risco de hesitação em decisões urgentes.',
    C: 'Sob pressão, se aprofunda na análise. Risco de paralisia por excesso de informação.'
  },
  percepcao: {
    D: 'Projeta confiança, determinação e objetividade. Pode ser percebido como assertivo ou, em excesso, autoritário.',
    I: 'Percebido como carismático, entusiasta e comunicativo. Pode ser visto como energizador ou, em excesso, superficial.',
    S: 'Transmite calma, confiabilidade e consistência. Pode ser visto como estável ou, em excesso, resistente a mudanças.',
    C: 'Percebido como criterioso, preciso e analítico. Pode ser visto como competente ou, em excesso, excessivamente crítico.'
  },
  recomendacoes: {
    D: ['Pratique escuta ativa antes de decidir', 'Valorize contribuições de perfis mais analíticos', 'Faça pausas para reflexão', 'Delegue mais e confie na equipe'],
    I: ['Equilibre entusiasmo com disciplina de prazos', 'Documente acordos e decisões', 'Desenvolva resiliência a críticas', 'Aprofunde temas antes de compartilhar'],
    S: ['Comunique-se abertamente sobre mudanças', 'Pratique sair da zona de conforto gradualmente', 'Desenvolva assertividade', 'Compartilhe suas opiniões mais cedo'],
    C: ['Equilibre análise com ação', 'Aceite que informação parcial é ok para começar', 'Pratique decisões com prazos curtos', 'Compartilhe conhecimento com a equipe']
  },
  equipe: {
    D: ['Direcionamento e foco em resultados', 'Capacidade de tomar decisões difíceis', 'Energia para superar obstáculos', 'Visão estratégica e ambição'],
    I: ['Energia positiva e motivação', 'Criatividade e geração de ideias', 'Conexão e networking', 'Comunicação e engajamento'],
    S: ['Estabilidade e confiabilidade', 'Apoio e suporte à equipe', 'Memória institucional e consistência', 'Harmonia e cooperação'],
    C: ['Análise crítica e qualidade', 'Precisão e atenção a detalhes', 'Padrões elevados de excelência', 'Rigor técnico e metodologia']
  }
};

const blendDescriptions = {
  D: 'Foco em resultados e ação direta',
  I: 'Foco em pessoas e comunicação',
  S: 'Foco em estabilidade e harmonia',
  C: 'Foco em qualidade e análise',
  DI: 'Ação combinada com influência — orientado a resultados através de pessoas',
  ID: 'Influência combinada com ação — comunicação direcionada a metas',
  DS: 'Determinação equilibrada com estabilidade',
  SD: 'Estabilidade com capacidade de ação',
  DC: 'Ação com critério — resultados com qualidade',
  CD: 'Critério com ação — qualidade orientada a resultados',
  IS: 'Influência com estabilidade — comunicação acolhedora',
  SI: 'Estabilidade com influência — conexão consistente',
  SC: 'Estabilidade com critério — análise consistente',
  CS: 'Critério com estabilidade — qualidade consistente',
  IC: 'Influência com critério — comunicação analítica',
  CI: 'Critério com influência — análise comunicativa'
};

function getTextoPorScore(f, score) {
  return score > 0 ? TEXTOS.descricao[f].alto : TEXTOS.descricao[f].baixo;
}

function capitalizar(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Seleciona palavras descritivas por fator e intensidade (corrigido) */
function palavrasPorFator(f, score) {
  const pdf = (PALAVRAS_PDF && PALAVRAS_PDF[f]) || [];
  const fb = PALAVRAS_FALLBACK[f];
  const intensidade = score > 5 ? 'alto' : score > 0 ? 'medio' : 'baixo';
  const qtd = score > 5 ? 4 : score > 0 ? 3 : 2;
  const fromPdf = pdf
    .filter(w => !w.startsWith('não ') && w.length > 2)
    .slice(0, qtd)
    .map(capitalizar);
  const fromFb = (fb[intensidade] || []).slice(0, qtd);
  return [...new Set([...fromPdf, ...fromFb])].slice(0, qtd);
}

function gerarDescritivo(scores, sorted) {
  const palavras = [];
  sorted.forEach(f => {
    palavras.push(...palavrasPorFator(f, scores[f]));
  });
  const unicas = [...new Set(palavras)].slice(0, 12);
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4">🏷️ Palavras Descritivas</h3>
      <p class="text-xs text-gray-400 mb-3">Baseado em padrões identificados em 66 perfis profissionais DISC</p>
      <div class="flex flex-wrap gap-2">
        ${unicas.map(p => `<span class="px-3 py-1.5 bg-gray-100 rounded-full text-sm font-medium">${p}</span>`).join('')}
      </div>
    </div>`;
}

function gerarSecaoMultiFator(titulo, scores, fonteTextos) {
  const fatores = getFatoresPonderados(scores);
  const blocos = fatores.map(f => `
    <div class="mb-3 ${fatores.length > 1 ? 'pl-3 border-l-4' : ''}" style="${fatores.length > 1 ? 'border-color:' + CORES[f] : ''}">
      ${fatores.length > 1 ? `<span class="text-xs font-bold uppercase" style="color:${CORES[f]}">Fator ${f}</span>` : ''}
      <p class="text-gray-600 leading-relaxed ${fatores.length > 1 ? 'mt-1' : ''}">${fonteTextos[f]}</p>
    </div>`).join('');
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4">${titulo}</h3>
      ${blocos}
    </div>`;
}

function gerarSecaoPerfil(perfil, scores) {
  const { primario, secundario, blend } = perfil;
  const desc = TEXTOS.descricao[primario];
  const descTexto = scores[primario] > 0 ? desc.alto : desc.baixo;
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4">📋 Visão Geral do Perfil</h3>
      <div class="flex items-center gap-3 mb-4 flex-wrap">
        <span class="px-4 py-1.5 rounded-full text-white font-bold text-sm" style="background:${CORES[primario]}">${blend}</span>
        <span class="text-gray-600">${blendDescriptions[blend] || 'Perfil combinado'}</span>
      </div>
      <p class="text-gray-600 leading-relaxed">${descTexto}</p>
      ${secundario && scores[secundario] > 0 ? `
        <div class="mt-4 p-4 bg-gray-50 rounded-xl">
          <p class="text-sm"><strong>Influência secundária de ${secundario}:</strong> ${getTextoPorScore(secundario, scores[secundario])}</p>
        </div>` : ''}
    </div>`;
}

function gerarListaSecao(titulo, scores, fonte) {
  const itens = [];
  getFatoresAtivos(scores, 0).forEach(f => {
    if (fonte[f]) itens.push(...fonte[f]);
  });
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4">${titulo}</h3>
      <ul class="space-y-2">
        ${itens.slice(0, 8).map(i => `<li class="flex items-start gap-2"><span class="text-green-500 mt-1">✓</span><span class="text-gray-600 text-sm">${i}</span></li>`).join('')}
      </ul>
    </div>`;
}

function gerarSecaoZona(scores) {
  const naZona = FACTORES.filter(f => Math.abs(scores[f]) > 8);
  if (!naZona.length) return '';
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 border-2 border-red-200 fade-in">
      <h3 class="text-lg font-bold mb-4">⚠️ Zona Cinzenta — Linha de Ênfase</h3>
      <p class="text-gray-600 text-sm mb-4">Fatores com |score| > 8 estão na zona cinzenta. São traços muito pronunciados — grandes forças que podem exigir moderação para evitar excessos.</p>
      ${naZona.map(f => `
        <div class="p-4 rounded-xl mb-3" style="background:${CORES[f]}15;border-left:4px solid ${CORES[f]}">
          <strong style="color:${CORES[f]}">Fator ${f} (${scores[f] > 0 ? '+' : ''}${scores[f]}):</strong>
          <p class="text-sm text-gray-600 mt-1">${scores[f] > 0 ? 'Intensidade muito elevada. Grande força que pede atenção para não se tornar excesso.' : 'Intensidade muito baixa. Pode indicar área que requer desenvolvimento consciente.'}</p>
        </div>`).join('')}
    </div>`;
}

function gerarSecaoSI(scores) {
  const sScore = scores.S;
  const iScore = scores.I;
  const outrosMedio = FACTORES.filter(f => f !== 'S' && f !== 'I')
    .reduce((acc, f) => acc + Math.abs(scores[f]), 0) / 2;

  let interpretacao = '';
  if (Math.abs(sScore) < 2 && outrosMedio > 4) {
    interpretacao += '⚠️ Seu fator S (Estabilidade) está próximo do neutro enquanto outros fatores têm intensidade maior. Isso pode indicar desconforto com falta de estabilidade ou ritmo inadequado.<br><br>';
  }
  if (Math.abs(iScore) < 2 && outrosMedio > 4) {
    interpretacao += '⚠️ Seu fator I (Influência) está próximo do neutro enquanto outros fatores têm intensidade maior. Isso pode indicar frustração na expressão social ou dificuldade em exercer influência.<br><br>';
  }
  if (Math.abs(sScore) >= 5) {
    interpretacao += `✓ Fator S (${sScore > 0 ? '+' : ''}${sScore}): ${sScore > 0 ? 'forte necessidade de estabilidade e consistência' : 'preferência por dinamismo e variedade'}.`;
  }
  if (Math.abs(iScore) >= 5) {
    interpretacao += `<br>✓ Fator I (${iScore > 0 ? '+' : ''}${iScore}): ${iScore > 0 ? 'forte orientação social e comunicativa' : 'preferência por interações mais reservadas'}.`;
  }
  if (!interpretacao) {
    interpretacao = 'Seus fatores S e I estão alinhados com os demais, sem indicadores significativos de frustração ou desconforto.';
  }

  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4">📊 Análise Comparativa — Fatores S e I</h3>
      <p class="text-gray-600 text-sm leading-relaxed">${interpretacao}</p>
    </div>`;
}

function gerarDisclaimer() {
  return `
    <div class="text-center text-xs text-gray-400 mt-8 pt-4 border-t space-y-2">
      <p><strong>Instrumento de autoconhecimento comportamental</strong> inspirado no modelo DISC (Dominância, Influência, Estabilidade, Conformidade).</p>
      <p>Este teste <strong>não substitui</strong> avaliação psicológica, psicométrica ou de RH conduzida por profissional habilitado. Resultados são indicativos, contextuais e baseados em autorrelato.</p>
      <p>Não possui normas populacionais validadas. Versão do instrumento: ${INSTRUMENT_VERSION}</p>
    </div>`;
}

// ===== RENDERIZAR RESULTADO =====
function calcularERenderizar(nome) {
  const scores = calcularScoresFromState();
  const perfil = determinarPerfil(scores);
  const hoje = new Date().toLocaleDateString('pt-BR');

  document.getElementById('resultadoContainer').innerHTML = `
    <div id="printArea">
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold">Perfil Comportamental DISC</h2>
        <p class="text-gray-500 mt-1">${nome} · ${hoje}</p>
        <div class="inline-block bg-[#1a1a2e] text-white px-5 py-2 rounded-full text-sm font-bold mt-3">Perfil Principal: ${perfil.blend}</div>
      </div>

      ${gerarGrafico(nome, scores, perfil)}
      ${gerarSecaoPerfil(perfil, scores)}
      ${gerarDescritivo(scores, perfil.sorted)}
      ${gerarListaSecao('Forças / Pontos Fortes', scores, TEXTOS.forcas)}
      ${gerarSecaoMultiFator('💬 Estilo de Comunicação', scores, TEXTOS.comunicacao)}
      ${gerarListaSecao('Pontos de Atenção / Áreas de Desenvolvimento', scores, TEXTOS.atencao)}
      ${gerarListaSecao('Recomendações Práticas', scores, TEXTOS.recomendacoes)}
      ${gerarSecaoMultiFator('🔥 Comportamento sob Pressão', scores, TEXTOS.pressao)}
      ${gerarSecaoMultiFator('👀 Como os Outros Veem Você', scores, TEXTOS.percepcao)}
      ${gerarListaSecao('O que você traz para a equipe', scores, TEXTOS.equipe)}
      ${gerarSecaoZona(scores)}
      ${gerarSecaoSI(scores)}
      ${gerarDisclaimer()}

      <div class="flex flex-wrap justify-center gap-3 mt-8 no-print">
        <button onclick="window.print()" class="bg-[#1a1a2e] text-white px-6 py-2.5 rounded-full font-semibold shadow hover:shadow-lg transition-all btn-scale">🖨️ Imprimir / Salvar PDF</button>
        <button onclick="refazer()" class="bg-gray-200 text-gray-700 px-6 py-2.5 rounded-full font-semibold hover:bg-gray-300 transition-all btn-scale">Refazer Teste</button>
      </div>
    </div>`;

  document.getElementById('resultado').style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => initGrafico(scores), 100);
}