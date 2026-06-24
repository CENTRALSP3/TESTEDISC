// ===== PERGUNTAS DO QUIZ DISC =====
const perguntasDISC = [
    { id: 'd1', fator: 'D', texto: 'Eu gosto de assumir a liderança em situações desafiadoras.' },
    { id: 'd2', fator: 'D', texto: 'Tenho facilidade para tomar decisões rápidas e assumir riscos.' },
    { id: 'd3', fator: 'D', texto: 'Sou competitivo(a) e gosto de superar obstáculos.' },
    { id: 'd4', fator: 'D', texto: 'Prefiro definir metas ambiciosas e buscar resultados expressivos.' },
    { id: 'd5', fator: 'D', texto: 'Sinto-me confortável em confrontar ideias divergentes diretamente.' },
    { id: 'i1', fator: 'I', texto: 'Sou uma pessoa comunicativa e gosto de interagir com diferentes pessoas.' },
    { id: 'i2', fator: 'I', texto: 'Tenho facilidade para motivar e entusiasmar os outros.' },
    { id: 'i3', fator: 'I', texto: 'Sinto-me energizado(a) ao trabalhar em grupo e compartilhar ideias.' },
    { id: 'i4', fator: 'I', texto: 'Gosto de ser o centro das atenções em eventos sociais.' },
    { id: 'i5', fator: 'I', texto: 'Sou persuasivo(a) e consigo engajar pessoas em torno de uma visão.' },
    { id: 's1', fator: 'S', texto: 'Valoro ambientes estáveis e previsíveis no trabalho.' },
    { id: 's2', fator: 'S', texto: 'Sou paciente e consistente na execução das minhas tarefas.' },
    { id: 's3', fator: 'S', texto: 'Prefiro rotinas bem estabelecidas a mudanças constantes.' },
    { id: 's4', fator: 'S', texto: 'Sou leal à equipe e busco manter harmonia no grupo.' },
    { id: 's5', fator: 'S', texto: 'Costumo ouvir atentamente antes de expressar minha opinião.' },
    { id: 'c1', fator: 'C', texto: 'Sou detalhista e gosto de seguir procedimentos estabelecidos.' },
    { id: 'c2', fator: 'C', texto: 'Prefiro tomar decisões baseadas em dados e evidências concretas.' },
    { id: 'c3', fator: 'C', texto: 'Tenho alta exigência com qualidade e padrões de excelência.' },
    { id: 'c4', fator: 'C', texto: 'Sou criterioso(a) e analiso cuidadosamente antes de agir.' },
    { id: 'c5', fator: 'C', texto: 'Valorizo regras claras e prefiro evitar erros por descuido.' }
];

const labelsLikert = [
    'Discordo Totalmente', 'Discordo Parcialmente',
    'Neutro', 'Concordo Parcialmente', 'Concordo Totalmente'
];

const state = {
    respostas: {},
    passo: 0,
    resultado: null,
    perfilPrimario: null,
    perfilSecundario: null,
    perfisData: null
};

// ===== INICIAR =====
function iniciarQuiz() {
    document.getElementById('home').style.display = 'none';
    const quiz = document.getElementById('quiz-section');
    quiz.style.display = 'block';
    state.passo = 0;
    state.respostas = {};
    state.resultado = null;
    mostrarPergunta();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== PERGUNTA =====
function mostrarPergunta() {
    const total = perguntasDISC.length;
    const idx = state.passo;
    if (idx >= total) { finalizarQuiz(); return; }

    const p = perguntasDISC[idx];
    document.getElementById('quiz-progresso').textContent = `${idx + 1} de ${total}`;
    document.getElementById('progress-bar').style.width = `${(idx / total) * 100}%`;

    const container = document.getElementById('quiz-container');

    // Botões navegação
    const navHtml = `
        <div class="quiz-nav">
            ${idx > 0 ? '<button class="btn btn-secondary" onclick="voltarPergunta()">Voltar</button>' : ''}
            <button class="btn btn-primary" id="btn-proximo" onclick="avancarPergunta()">
                ${idx < total - 1 ? 'Próxima' : 'Ver Meu Resultado'}
            </button>
        </div>`;

    container.innerHTML = `
        <div class="quiz-card" data-id="${p.id}">
            <div class="quiz-fator" style="color:${CORES[p.fator]}">Fator ${p.fator}</div>
            <p class="quiz-pergunta">${p.texto}</p>
            <div class="quiz-opcoes">
                ${labelsLikert.map((label, i) => {
                    const v = i + 1;
                    const sel = state.respostas[p.id] === v;
                    return `<label class="quiz-opcao ${sel ? 'selected' : ''}">
                        <input type="radio" name="q-${p.id}" value="${v}" ${sel ? 'checked' : ''}>
                        <span class="quiz-num">${v}</span>
                        <span class="quiz-label">${label}</span>
                    </label>`;
                }).join('')}
            </div>
        </div>
        ${navHtml}`;

    // Eventos de seleção
    container.querySelectorAll('.quiz-opcao input').forEach(input => {
        input.addEventListener('change', function () {
            const lbl = this.closest('.quiz-opcao');
            lbl.parentElement.querySelectorAll('.quiz-opcao').forEach(el => el.classList.remove('selected'));
            lbl.classList.add('selected');
            state.respostas[p.id] = parseInt(this.value);
        });
    });
}

function avancarPergunta() {
    const p = perguntasDISC[state.passo];
    if (!state.respostas[p.id]) {
        alert('Selecione uma opção para continuar.');
        return;
    }
    state.passo++;
    mostrarPergunta();
}

function voltarPergunta() {
    if (state.passo > 0) { state.passo--; mostrarPergunta(); }
}

// ===== CÁLCULO =====
function calcularPerfil() {
    const somas = { D: 0, I: 0, S: 0, C: 0 };
    const contagens = { D: 0, I: 0, S: 0, C: 0 };
    perguntasDISC.forEach(p => {
        const v = state.respostas[p.id];
        if (v) { somas[p.fator] += v; contagens[p.fator]++; }
    });
    const r = {};
    factorOrder.forEach(f => { r[f] = contagens[f] > 0 ? Math.round((somas[f] / (contagens[f] * 5)) * 100) : 0; });
    const sorted = factorOrder.slice().sort((a, b) => r[b] - r[a]);
    state.perfilPrimario = sorted[0];
    state.perfilSecundario = sorted[1];
    state.resultado = r;
}

// ===== FINALIZAR =====
function finalizarQuiz() {
    document.getElementById('progress-bar').style.width = '100%';
    fetch('perfis.json').then(r => r.json()).then(d => {
        state.perfisData = d;
        renderizarResultado();
    });
}

// ===== RENDERIZAR RESULTADO =====
function renderizarResultado() {
    calcularPerfil();
    document.getElementById('quiz-section').style.display = 'none';
    const section = document.getElementById('resultado-section');
    section.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });

    const r = state.resultado;
    const p1 = state.perfilPrimario;
    const p2 = state.perfilSecundario;
    const pd = state.perfisData;
    const pAtual = pd[p1] || pd[p1 + p2] || pd[p1.toLowerCase()];
    const pNome = pAtual ? pAtual.titulo : p1;
    const pDesc = pAtual ? pAtual.desc : '';

    const zonaAtiva = {};
    factorOrder.forEach(f => { zonaAtiva[f] = r[f] >= 75 ? 'alta' : r[f] <= 25 ? 'baixa' : 'normal'; });
    const temZona = Object.values(zonaAtiva).filter(v => v !== 'normal').length > 0;

    document.getElementById('resultado-container').innerHTML = `
        <div id="resultado-print">

            <div class="resultado-header">
                <h2>Seu Perfil Comportamental</h2>
                <div class="resultado-nome-area">
                    <label for="participante-nome">Nome:</label>
                    <input type="text" id="participante-nome" placeholder="Digite seu nome" autocomplete="name">
                </div>
            </div>

            <!-- GRÁFICO -->
            <div class="grafico-section">
                <h3>Geral dos Fatores</h3>
                <div class="grafico-container">
                    ${factorOrder.map(f => `
                        <div class="grafico-bar-row">
                            <div class="grafico-label" style="color:${CORES[f]}">${f}</div>
                            <div class="grafico-bar-wrapper">
                                <div class="grafico-bar" style="width:${r[f]}%;background:${CORES[f]}">
                                    <span class="grafico-valor">${r[f]}%</span>
                                </div>
                            </div>
                        </div>`).join('')}
                    <div class="grafico-mediana"></div>
                </div>
                <div class="grafico-legenda"><span class="legenda-mediana">— Linha mediana (50%)</span></div>
            </div>

            <!-- PERFIL PESSOAL -->
            <div class="devolutiva-section">
                <h3>Perfil Pessoal</h3>
                <div class="devolutiva-card" style="border-left-color:${CORES[p1]}">
                    <span class="devolutiva-sigla" style="background:${CORES[p1]}">${p1}</span>
                    <h4>${pNome}</h4>
                    <p>${pDesc}</p>
                    ${pAtual?.forcas ? '<p><strong>Forças:</strong> ' + pAtual.forcas + '</p>' : ''}
                    ${pAtual?.comunicacao ? '<p><strong>Comunicação:</strong> ' + pAtual.comunicacao + '</p>' : ''}
                    ${pAtual?.melhorias ? '<p><strong>Pontos de Atenção:</strong> ' + pAtual.melhorias + '</p>' : ''}
                    ${pAtual?.dicas ? '<p><strong>Recomendação:</strong> ' + pAtual.dicas + '</p>' : ''}
                </div>
                ${p2 ? `
                <div class="devolutiva-card secundario" style="border-left-color:${CORES[p2]}">
                    <span class="devolutiva-sigla" style="background:${CORES[p2]}">${p2}</span>
                    <h4>Perfil Secundário: ${pd[p2]?.titulo || p2}</h4>
                    <p>${pd[p2]?.desc || ''}</p>
                </div>` : ''}
            </div>

            <!-- COMO OS OUTROS VEEM -->
            <div class="devolutiva-section">
                <h3>Como os Outros Veem Você</h3>
                <div class="devolutiva-card" style="border-left-color:${CORES[p1]}">
                    <p>${textoPercepcao(p1)}</p>
                </div>
            </div>

            <!-- SOB PRESSÃO -->
            <div class="devolutiva-section">
                <h3>Comportamento sob Pressão</h3>
                <div class="devolutiva-card" style="border-left-color:${CORES[p1]}">
                    <p>${textoPressao(p1)}</p>
                </div>
            </div>

            ${temZona ? `
            <div class="devolutiva-section">
                <h3>Zona Cinzenta</h3>
                ${Object.entries(zonaAtiva).filter(([,v]) => v !== 'normal').map(([f, v]) => `
                    <div class="devolutiva-card" style="border-left-color:${CORES[f]}">
                        <p><strong style="color:${CORES[f]}">Fator ${f} (${r[f]}%) — ${v === 'alta' ? 'Muito elevado' : 'Muito baixo'}:</strong><br>
                        ${v === 'alta'
                            ? 'Sua intensidade neste fator está acima da média. Pode ser uma vantagem em contextos específicos, mas requer atenção para evitar excessos.'
                            : 'Sua intensidade neste fator está abaixo da média. Considere desenvolvê-lo para situações que exijam esta característica.'}</p>
                    </div>`).join('')}
            </div>` : ''}

            <!-- BOTÃO PDF -->
            <div class="resultado-actions">
                <button class="btn btn-primary" onclick="gerarPDF()">📄 Baixar PDF</button>
                <button class="btn btn-secondary" onclick="gerarImagem()">🖼️ Baixar Imagem</button>
                <button class="btn btn-secondary" onclick="refazer()">Refazer Teste</button>
            </div>
        </div>`;

    setTimeout(posicionarMediana, 150);
}

function posicionarMediana() {
    const c = document.querySelector('.grafico-container');
    const m = c?.querySelector('.grafico-mediana');
    const w = c?.querySelector('.grafico-bar-wrapper');
    if (c && m && w) m.style.left = (36 + w.offsetWidth * 0.5) + 'px';
}

// ===== TEXTOS =====
function textoPercepcao(p) {
    const t = {
        D: 'Você projeta uma imagem de confiança, determinação e objetividade. Os outros provavelmente o veem como alguém direto, que vai ao ponto e não perde tempo com rodeios. Sua postura transmite capacidade de liderança e tomada de decisão, mas em alguns contextos pode ser percebido como autoritário ou impaciente.',
        I: 'Você é percebido como uma pessoa carismática, entusiasta e comunicativa. Os outros provavelmente o veem como alguém que traz energia positiva aos grupos, que sabe se expressar bem e engajar as pessoas. Sua expressividade transmite confiança, mas em excesso pode ser visto como disperso ou superficial.',
        S: 'Você transmite calma, confiabilidade e consistência. Os outros provavelmente o veem como uma pessoa paciente, leal e que traz estabilidade ao ambiente. Sua postura acolhedora gera confiança, mas pode ser interpretada como resistência a mudanças ou falta de iniciativa.',
        C: 'Você é percebido como uma pessoa criteriosa, precisa e analítica. Os outros provavelmente o veem como alguém que valoriza qualidade, segue padrões e não abre mão do rigor técnico. Sua postura transmite competência, mas pode ser interpretada como excessivamente crítica ou lenta.'
    };
    return t[p] || t.D;
}

function textoPressao(p) {
    const t = {
        D: 'Sob pressão, você tende a se tornar ainda mais direto e orientado a resultados. Sua reação natural é assumir o controle e buscar soluções rápidas. Pode ficar impaciente com hesitações e tender a atropelar processos ou pessoas. O risco é agir por impulso sem considerar todas as variáveis. Em situações de crise, é importante fazer pausas deliberadas para ouvir o grupo antes de decidir.',
        I: 'Sob pressão, você busca apoio social e validação externa. Sua reação natural é comunicar-se mais intensamente e tentar engajar os outros para resolver o problema juntos. Pode ficar disperso ou ansioso se sentir que está isolado. O risco é evitar o enfrentamento direto dos problemas. Em momentos de estresse, busque estruturar suas ideias por escrito antes de compartilhá-las.',
        S: 'Sob pressão, você tende a se retrair e buscar estabilidade. Sua reação natural é manter a rotina e evitar mudanças abruptas. Pode ficar hesitante em tomar decisões rápidas e precisar de mais tempo para processar. O risco é resistir a mudanças necessárias por medo do desconhecido. Em crises, busque apoio em pessoas de confiança e foque em um passo de cada vez.',
        C: 'Sob pressão, você se aprofunda ainda mais na análise. Sua reação natural é buscar mais dados e informações antes de agir. Pode ficar sobrecarregado com a necessidade de decisões rápidas sem informações suficientes. O risco é a paralisia por análise. Em momentos de estresse, estabeleça prazos para decidir e aceite que informações parciais são suficientes para começar.'
    };
    return t[p] || t.D;
}

function refazer() {
    document.getElementById('resultado-section').style.display = 'none';
    document.getElementById('home').style.display = 'block';
    state.respostas = {};
    state.passo = 0;
    state.resultado = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ===== PDF / IMAGEM =====
function gerarPDF() {
    const nome = document.getElementById('participante-nome')?.value || 'Participante';
    const el = document.getElementById('resultado-print');
    const btn = event?.target;
    if (btn) btn.disabled = true;

    const inp = document.getElementById('participante-nome');
    if (inp && !inp.value) inp.value = nome;

    html2canvas(el, { scale: 2, backgroundColor: '#ffffff', useCORS: true }).then(canvas => {
        const img = canvas.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pw = 210, ph = (canvas.height * pw) / canvas.width;
        let left = ph, pos = 0;
        pdf.addImage(img, 'PNG', 0, pos, pw, ph);
        left -= 297;
        while (left > 0) { pos = left - ph; pdf.addPage(); pdf.addImage(img, 'PNG', 0, pos, pw, ph); left -= 297; }
        pdf.save(`Perfil_DISC_${nome.replace(/\s+/g, '_')}.pdf`);
        if (btn) btn.disabled = false;
    }).catch(() => { if (btn) btn.disabled = false; });
}

function gerarImagem() {
    const nome = document.getElementById('participante-nome')?.value || 'Participante';
    const el = document.getElementById('resultado-print');
    const inp = document.getElementById('participante-nome');
    if (inp && !inp.value) inp.value = nome;

    html2canvas(el, { scale: 2, backgroundColor: '#ffffff', useCORS: true }).then(canvas => {
        const link = document.createElement('a');
        link.download = `Perfil_DISC_${nome.replace(/\s+/g, '_')}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}
