#!/usr/bin/env python3
"""Gera index.html self-contained a partir dos módulos em src/js/."""
from pathlib import Path

BASE = Path(__file__).resolve().parent
JS_DIR = BASE / "src" / "js"
OUTPUT = BASE / "index.html"

JS_ORDER = [
    "constants.js",
    "questions.js",
    "palavras-data.js",
    "devolutiva-templates.js",
    "scoring.js",
    "charts.js",
    "devolutiva.js",
    "features.js",
    "app.js",
]

HTML_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Perfil DISC V2 - Análise Comportamental</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#1a1a2e">
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config={darkMode:'class'}</script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{font-family:'Inter',system-ui,sans-serif;scroll-behavior:smooth}
.disc-d{color:#E74C3C}.disc-i{color:#F39C12}.disc-s{color:#27AE60}.disc-c{color:#2980B9}
.bg-d{background:#E74C3C}.bg-i{background:#F39C12}.bg-s{background:#27AE60}.bg-c{background:#2980B9}
.opt-card{cursor:pointer;border:2px solid transparent;transition:.15s}
.opt-card.most{border-color:#1a1a2e;background:#eef2f7}
.dark .opt-card.most{background:#2d3748}
.opt-card.least{border-color:#E74C3C;background:#fde8e8}
.dark .opt-card.least{background:#4a2020}
@keyframes fIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulseGlow{0%,100%{box-shadow:0 4px 18px rgba(26,26,46,.2)}50%{box-shadow:0 8px 28px rgba(243,156,18,.35)}}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}
.fade-in{animation:fIn .4s ease}
.home-card{animation:fIn .55s ease}
.btn-primary{animation:pulseGlow 2.8s ease-in-out infinite}
.progress-bar{transition:width .5s ease;background:linear-gradient(90deg,#f59e0b,#ef4444,#f59e0b);background-size:200% 100%;animation:shimmer 3s linear infinite}
.factor-badge{transition:transform .2s ease,box-shadow .2s ease}
.factor-badge:hover{transform:scale(1.06);box-shadow:0 4px 12px rgba(0,0,0,.12)}
.opt-card{transition:transform .15s ease,border-color .15s,background .15s,box-shadow .15s}
.opt-card:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,.06)}
html.dark body{background:#111827;color:#f3f4f6}
html.dark .card{background:#1f2937!important}
.nav-pill{transition:all .2s ease}
.nav-pill:hover{transform:translateY(-1px)}
@media print{.no-print{display:none!important}}
</style>
</head>
<body class="bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100 min-h-screen flex flex-col">

<header class="bg-gradient-to-r from-[#1a1a2e] to-[#16213e] text-white py-6 px-4 text-center relative">
  <nav class="absolute top-3 left-3 right-3 flex justify-between items-center no-print" aria-label="Navegação entre testes">
    <a href="https://centralsp3.github.io/central/" class="nav-pill text-xs text-white/50 hover:text-white/90">← Central</a>
    <a href="https://centralsp3.github.io/PERSONALIDADE/" class="nav-pill text-xs font-semibold px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/20 border border-purple-400/50 text-purple-200">Personalidade OCEAN →</a>
  </nav>
  <h1 class="text-xl font-bold tracking-wider mt-6">Perfil <span class="text-amber-400">DISC</span></h1>
  <p class="text-sm text-white/60 mt-1">Comportamento observável · Método DISC (forced-choice)</p>
  <p class="text-xs text-white/40 mt-1 max-w-md mx-auto">Mede <strong>D, I, S e C</strong> — distinto do teste de traços Big Five (Likert)</p>
</header>

<main class="flex-1" id="app">

<section id="home" class="py-12 px-4">
  <div class="max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8 text-center home-card card">
    <h2 class="text-2xl font-bold mb-3">Descubra seu Perfil Comportamental</h2>
    <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed mb-2">O método <strong>DISC</strong> mapeia quatro dimensões do <strong>comportamento observável</strong>: Dominância (D), Influência (I), Estabilidade (S) e Conformidade (C).</p>
    <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed mb-4">São <strong>56 afirmações</strong> em formato <strong>escolha forçada</strong> (mais/menos). Não é questionário de traços de personalidade — cada instrumento mede constructos diferentes.</p>
    <div class="grid grid-cols-4 gap-2 max-w-xs mx-auto mb-6">
      <div class="factor-badge bg-d text-white rounded-xl p-3 font-bold text-center text-sm">D<br><span class="font-normal text-xs">Dominância</span></div>
      <div class="factor-badge bg-i text-white rounded-xl p-3 font-bold text-center text-sm">I<br><span class="font-normal text-xs">Influência</span></div>
      <div class="factor-badge bg-s text-white rounded-xl p-3 font-bold text-center text-sm">S<br><span class="font-normal text-xs">Estabilidade</span></div>
      <div class="factor-badge bg-c text-white rounded-xl p-3 font-bold text-center text-sm">C<br><span class="font-normal text-xs">Conformidade</span></div>
    </div>
    <button onclick="iniciar()" class="btn-primary bg-[#1a1a2e] text-white px-12 py-3.5 rounded-full font-semibold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all">Iniciar Teste DISC</button>
    <div class="flex justify-center gap-3 mt-5 flex-wrap">
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500"><strong>56</strong> questões</span>
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500"><strong>~15</strong> min</span>
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500">v<strong>2.1</strong></span>
    </div>
    <button onclick="toggleDarkMode()" class="mt-4 text-xs text-gray-400 underline">Alternar modo escuro</button>
  </div>
</section>

<section id="quiz" class="py-8 px-4" style="display:none">
  <div class="max-w-2xl mx-auto">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-5 mb-5">
      <div class="flex justify-end items-center mb-3">
        <span id="progressText" class="text-sm font-semibold text-gray-400">1 de 56</span>
      </div>
      <div class="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
        <div id="progressBar" class="progress-bar h-full bg-gradient-to-r from-amber-400 to-red-500 rounded-full" style="width:0%"></div>
      </div>
    </div>
    <div id="quizContainer" class="min-h-[300px]"></div>
  </div>
</section>

<section id="pausaBloco" class="py-12 px-4" style="display:none">
  <div class="max-w-lg mx-auto bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-8 text-center fade-in card">
    <h2 class="text-xl font-bold mb-2">Metade do questionário!</h2>
    <p class="text-gray-500 dark:text-gray-400 text-sm mb-6">Você completou 28 de 56 afirmações. Faça uma pausa breve se precisar — suas respostas anteriores estão salvas.</p>
    <button onclick="continuarAposPausa()" class="bg-[#1a1a2e] text-white px-10 py-3 rounded-full font-semibold shadow-lg">Continuar →</button>
  </div>
</section>

<section id="nameForm" class="py-8 px-4" style="display:none">
  <div class="max-w-lg mx-auto bg-white rounded-2xl shadow-sm p-8 text-center fade-in">
    <h2 class="text-xl font-bold mb-2">Teste Concluído!</h2>
    <p class="text-gray-500 text-sm mb-6">Insira seu nome para gerar o relatório personalizado.</p>
    <input id="userName" type="text" placeholder="Seu nome" class="w-full border rounded-xl px-4 py-3 text-center text-lg font-medium outline-none focus:border-[#1a1a2e] transition-colors mb-4">
    <div id="nameError" class="text-red-500 text-sm mb-3 hidden">Por favor, digite seu nome.</div>
    <button onclick="gerarRelatorio()" class="bg-[#1a1a2e] text-white px-10 py-3 rounded-full font-semibold shadow-lg hover:shadow-xl transition-all">Gerar meu Relatório</button>
  </div>
</section>

<section id="resultado" class="py-8 px-4" style="display:none">
  <div class="max-w-3xl mx-auto" id="resultadoContainer"></div>
</section>

</main>

<footer class="bg-[#1a1a2e] text-white/60 text-center py-4 text-xs mt-auto">
  <p>Perfil Comportamental DISC — instrumento de autoconhecimento. Não substitui avaliação psicológica profissional.</p>
</footer>

<script>
"""

HTML_TAIL = """
</script>
</body>
</html>
"""


def build():
    parts = [HTML_HEAD]
    for fname in JS_ORDER:
        path = JS_DIR / fname
        if not path.exists():
            raise FileNotFoundError(f"Módulo ausente: {path}")
        parts.append(f"\n// --- {fname} ---\n")
        parts.append(path.read_text(encoding="utf-8"))
    parts.append(HTML_TAIL)

    content = "".join(parts)
    OUTPUT.write_text(content, encoding="utf-8")

    # GitHub Pages publica a pasta docs/
    docs_dir = BASE / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "index.html").write_text(content, encoding="utf-8")
    for asset in ("manifest.json", "sw.js"):
        src = BASE / asset
        if src.exists():
            (docs_dir / asset).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"✓ Gerado: {OUTPUT} ({len(content) // 1024} KB, {len(JS_ORDER)} módulos)")
    print(f"✓ Copiado para: {docs_dir / 'index.html'} (GitHub Pages)")


if __name__ == "__main__":
    build()