// ===== DEVOLUTIVA V2.1 — Estrutura Thomas (66 relatórios) =====

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

function hashScores(scores) {
  const s = FACTORES.map(f => scores[f]).join('');
  let h = 0;
  for (let i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

function pickFromList(list, seed, offset = 0) {
  if (!list || !list.length) return '';
  return list[(seed + offset) % list.length];
}

function pickFactorTemplate(fator, campo, seed, offset = 0) {
  const tpl = DEVOLUTIVA_TEMPLATES?.fatores?.[fator]?.[campo];
  if (!tpl || !tpl.length) return '';
  const item = tpl[(seed + offset) % tpl.length];
  if (typeof item === 'string') return item;
  if (Array.isArray(item)) return item;
  return item;
}

function formatParagrafos(texto) {
  if (!texto) return '';
  return texto.split(/\n\n+/).filter(p => p.trim().length > 20)
    .map(p => `<p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed mb-3">${p.trim()}</p>`)
    .join('');
}

function cardSecao(num, titulo, conteudo, extraClass = '') {
  return `<div class="card bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in ${extraClass}">
    <div class="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100 dark:border-gray-700">
      <span class="w-8 h-8 rounded-full bg-[#1a1a2e] text-white text-sm font-bold flex items-center justify-center flex-shrink-0">${num}</span>
      <h3 class="text-lg font-bold">${titulo}</h3>
    </div>
    ${conteudo}
  </div>`;
}

function gerarSumario(nome, hoje, perfilNat, perfilAdp, dual) {
  const blendDesc = DEVOLUTIVA_TEMPLATES?.blends?.[perfilNat.blend] || 'Perfil comportamental combinado';
  return `<div class="text-center mb-8 pb-6 border-b border-gray-200 dark:border-gray-700">
    <p class="text-xs uppercase tracking-widest text-gray-400 mb-2">Análise de Perfil Pessoal</p>
    <h2 class="text-2xl font-bold">Perfil Comportamental DISC</h2>
    <p class="text-gray-500 mt-1">${nome} · ${hoje}</p>
    <div class="flex flex-wrap justify-center gap-2 mt-4">
      <span class="px-4 py-1.5 rounded-full text-white text-sm font-bold" style="background:${CORES[perfilNat.primario]}">${perfilNat.blend}</span>
      <span class="text-sm text-gray-500 self-center">${blendDesc}</span>
    </div>
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-4 max-w-lg mx-auto text-xs">
      ${FACTORES.map(f => `<div class="p-2 rounded-lg bg-gray-50 dark:bg-gray-800">
        <span class="font-bold" style="color:${CORES[f]}">${f}</span>
        <span class="text-gray-500 ml-1">${dual.natural[f] > 0 ? '+' : ''}${dual.natural[f]}</span>
      </div>`).join('')}
    </div>
  </div>`;
}

function gerarAutoImagem(perfil, scores, seed) {
  const f = perfil.primario;
  const texto = pickFactorTemplate(f, 'auto_imagem', seed);
  const sec = perfil.secundario ? ` com traços de <strong style="color:${CORES[perfil.secundario]}">${perfil.secundario}</strong>` : '';
  const intro = texto
    ? formatParagrafos(texto)
    : `<p class="text-gray-600 dark:text-gray-300 text-sm">Perfil com predominância de <strong style="color:${CORES[f]}">${f}</strong>${sec}.</p>`;
  return cardSecao(1, 'Autoimagem — Gráfico III', `
    <p class="text-xs text-gray-400 mb-3 uppercase tracking-wide">Comportamento natural</p>
    ${intro}
    <div class="mt-4 flex flex-wrap gap-2">
      <span class="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-800">Primário: <strong style="color:${CORES[f]}">${f}</strong> (${scores[f] > 0 ? '+' : ''}${scores[f]})</span>
      ${perfil.secundario ? `<span class="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-800">Secundário: <strong style="color:${CORES[perfil.secundario]}">${perfil.secundario}</strong></span>` : ''}
    </div>`);
}

function gerarPalavrasDescritivas(perfil, scores, seed) {
  const palavras = [];
  perfil.sorted.forEach((f, i) => {
    const fromTpl = pickFactorTemplate(f, 'palavras', seed, i);
    if (Array.isArray(fromTpl)) palavras.push(...fromTpl);
    palavras.push(...palavrasPorFator(f, scores[f]));
  });
  const unicas = [...new Set(palavras)].slice(0, 16);
  return cardSecao(2, 'Palavras Descritivas', `
    <p class="text-xs text-gray-400 mb-3">Baseado em ${DEVOLUTIVA_TEMPLATES?.meta?.source_documents || 66} perfis de referência</p>
    <div class="flex flex-wrap gap-2">${unicas.map(p =>
      `<span class="px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-full text-sm font-medium">${p}</span>`).join('')}</div>`);
}

function gerarAutoMotivacao(perfil, seed) {
  const f = perfil.primario;
  const texto = pickFactorTemplate(f, 'auto_motivacao', seed);
  const motivadores = pickFactorTemplate(f, 'motivadores', seed, 1);
  return cardSecao(3, 'Auto Motivação', `
    ${texto ? formatParagrafos(texto) : `<p class="text-gray-600 text-sm">Motivação orientada pelo fator <strong style="color:${CORES[f]}">${f}</strong>.</p>`}
    ${motivadores ? `<div class="mt-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-sm text-gray-600 dark:text-gray-300">${typeof motivadores === 'string' ? motivadores : ''}</div>` : ''}`);
}

function gerarEnfaseTrabalho(perfil, seed) {
  const f = perfil.primario;
  const enfase = pickFactorTemplate(f, 'enfase_trabalho', seed);
  let html = '';
  if (enfase && typeof enfase === 'object' && enfase.titulo) {
    html = `<p class="font-semibold text-gray-800 dark:text-gray-200 mb-2">${enfase.titulo}</p>${formatParagrafos(enfase.corpo)}`;
  } else if (typeof enfase === 'string') {
    html = formatParagrafos(enfase);
  } else {
    html = `<p class="text-gray-600 text-sm">Ênfase profissional alinhada ao perfil <strong>${perfil.blend}</strong>.</p>`;
  }
  return cardSecao(4, 'Ênfase no Trabalho', html);
}

function gerarCaracteristicas(perfil, seed) {
  const bullets = [];
  [perfil.primario, perfil.secundario].filter(Boolean).forEach((f, i) => {
    const tpl = DEVOLUTIVA_TEMPLATES?.fatores?.[f]?.caracteristicas;
    if (!tpl?.length) return;
    const start = (seed + i * 3) % tpl.length;
    for (let j = 0; j < 5 && j < tpl.length; j++) bullets.push(tpl[(start + j) % tpl.length]);
  });
  const unicos = [...new Set(bullets)].slice(0, 10);
  if (!unicos.length) return '';
  return cardSecao(5, 'Características Gerais', `
    <ul class="space-y-2">${unicos.map(b =>
      `<li class="flex gap-2 text-sm text-gray-600 dark:text-gray-300"><span class="text-[#1a1a2e] dark:text-amber-400 font-bold">•</span><span>${b}</span></li>`).join('')}</ul>`);
}

function gerarPercepcaoAdaptada(perfilAdp, dual, seed) {
  const disc = analisarDiscrepancia(dual);
  let texto = '';
  if (!disc.length) {
    const alinhados = DEVOLUTIVA_TEMPLATES?.discrepancia?.alinhado || [];
    texto = pickFromList(alinhados, seed) || 'O comportamento no ambiente profissional está alinhado com a autoimagem natural, sugerindo compatibilidade com o papel desempenhado.';
  } else {
    texto = disc.map(d => d.texto).join(' ');
  }
  return cardSecao(6, 'Percepção no Ambiente Profissional — Gráfico I', `
    <p class="text-xs text-gray-400 mb-3">Perfil adaptado: <strong>${perfilAdp.blend}</strong></p>
    <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">${texto}</p>`);
}

function gerarSobPressao(perfil, seed) {
  const f = perfil.primario;
  const texto = pickFactorTemplate(f, 'sob_pressao', seed);
  return cardSecao(7, 'Comportamento sob Pressão — Gráfico II', `
    ${texto ? formatParagrafos(texto) : `<p class="text-gray-600 text-sm">Sob pressão, tende a reforçar características do fator <strong style="color:${CORES[f]}">${f}</strong>.</p>`}`);
}

function gerarEstimulos(perfil, seed) {
  const f = perfil.primario;
  const texto = pickFactorTemplate(f, 'estimulos', seed);
  if (!texto) return '';
  return cardSecao(8, 'Estímulos e Orientações ao Gestor', formatParagrafos(typeof texto === 'string' ? texto : ''));
}

function gerarValorOrganizacao(perfil, seed) {
  const f = perfil.primario;
  const texto = pickFactorTemplate(f, 'valor_organizacao', seed);
  if (!texto) return '';
  return cardSecao(9, 'Valor para a Organização', formatParagrafos(typeof texto === 'string' ? texto : ''));
}

function gerarDiscrepancia(dual, seed) {
  const alertas = analisarDiscrepancia(dual);
  if (!alertas.length) {
    const tpl = pickFromList(DEVOLUTIVA_TEMPLATES?.discrepancia?.alinhado, seed);
    return cardSecao(10, 'Análise de Discrepância (Natural vs Adaptado)', `
      <p class="text-gray-600 text-sm leading-relaxed">${tpl || 'Seu comportamento natural e adaptado estão alinhados. O ambiente parece compatível com seu perfil.'}</p>`);
  }
  return cardSecao(10, 'Análise de Discrepância (Natural vs Adaptado)', `
    ${alertas.map(a => `<div class="p-3 mb-2 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-sm text-gray-700 dark:text-gray-300 border-l-4 border-amber-400">${a.texto}</div>`).join('')}`,
    'border-2 border-amber-100');
}

function gerarSecaoZona(scores) {
  const naZona = FACTORES.filter(f => Math.abs(scores[f]) > ZONA_CINZENTA);
  if (!naZona.length) return '';
  return cardSecao(11, 'Indicadores de Zona Cinzenta', `
    <p class="text-xs text-gray-400 mb-3">Fatores com intensidade extrema — requerem atenção especial na interpretação</p>
    ${naZona.map(f => `<div class="p-3 mb-2 rounded-xl" style="background:${CORES[f]}12;border-left:4px solid ${CORES[f]}">
      <strong style="color:${CORES[f]}">${f} (${scores[f] > 0 ? '+' : ''}${scores[f]})</strong>
      <p class="text-sm text-gray-600 mt-1">${scores[f] > 0 ? 'Traço muito pronunciado — moderação e autoconsciência recomendadas.' : 'Traço muito baixo — área potencial de desenvolvimento.'}</p>
    </div>`).join('')}`, 'border-2 border-red-100');
}

function gerarInferenciaAPI(apiResult) {
  if (!apiResult) return '';
  return cardSecao(12, 'Interpretação Avançada', `
    <p class="text-gray-700 dark:text-gray-200 font-medium leading-relaxed">${apiResult.interpretation}</p>
    ${apiResult.matched_rules?.length ? `<p class="text-xs text-gray-400 mt-3">Regras aplicadas: ${apiResult.matched_rules.join(', ')}</p>` : ''}
    ${apiResult.share_hash ? `<button onclick="copiarLink('${apiResult.share_hash}')" class="mt-3 text-sm text-blue-600 underline">Copiar link para compartilhar</button>` : ''}`,
    'border-l-4 border-blue-500');
}

function gerarDisclaimer() {
  return `<div class="text-center text-xs text-gray-400 mt-8 pt-4 border-t space-y-1">
    <p>Instrumento de autoconhecimento DISC v${INSTRUMENT_VERSION}. Não substitui avaliação psicológica profissional.</p>
    <p>Devolutiva baseada em ${DEVOLUTIVA_TEMPLATES?.meta?.source_documents || 66} relatórios de referência. Resultados indicativos baseados em autorrelato.</p>
    <p class="italic">Este relatório deve servir como guia e ser complementado por entrevista e avaliação contextual.</p>
  </div>`;
}

async function calcularERenderizar(nome, dualPrecomputed, apiPrecomputed) {
  const dual = dualPrecomputed || calcularScoresDual();
  const perfilNat = determinarPerfil(dual.natural);
  const perfilAdp = determinarPerfil(dual.adapted);
  const hoje = new Date().toLocaleDateString('pt-BR');
  const seed = hashScores(dual.natural);

  let apiResult = apiPrecomputed;
  if (!apiResult) {
    apiResult = await inferirViaAPI(dual);
    salvarResultadoAnonimo(dual, perfilNat);
  }

  document.getElementById('resultadoContainer').innerHTML = `
    <div id="printArea">
      ${gerarSumario(nome, hoje, perfilNat, perfilAdp, dual)}
      ${gerarGraficosTriplos(dual)}
      ${gerarAutoImagem(perfilNat, dual.natural, seed)}
      ${gerarPalavrasDescritivas(perfilNat, dual.natural, seed)}
      ${gerarAutoMotivacao(perfilNat, seed)}
      ${gerarEnfaseTrabalho(perfilNat, seed)}
      ${gerarCaracteristicas(perfilNat, seed)}
      ${gerarPercepcaoAdaptada(perfilAdp, dual, seed)}
      ${gerarSobPressao(perfilNat, seed)}
      ${gerarEstimulos(perfilNat, seed)}
      ${gerarValorOrganizacao(perfilNat, seed)}
      ${gerarDiscrepancia(dual, seed)}
      ${gerarSecaoZona(dual.natural)}
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