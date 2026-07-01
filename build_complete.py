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
@keyframes fIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.fade-in{animation:fIn .35s ease}
.progress-bar{transition:width .5s ease}
html.dark body{background:#111827;color:#f3f4f6}
html.dark .card{background:#1f2937!important}
@media print{.no-print{display:none!important}}
</style>
</head>
<body class="bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100 min-h-screen flex flex-col">

<header class="bg-gradient-to-r from-[#1a1a2e] to-[#16213e] text-white py-6 px-4 text-center">
  <h1 class="text-xl font-bold tracking-wider">Perfil <span class="text-amber-400">DISC</span></h1>
  <p class="text-sm text-white/60 mt-1">Análise Comportamental | TeclaPonto</p>
</header>

<main class="flex-1" id="app">

<section id="home" class="py-12 px-4">
  <div class="max-w-2xl mx-auto bg-white rounded-2xl shadow-sm p-8 text-center">
    <h2 class="text-2xl font-bold mb-3">Descubra seu Perfil Comportamental</h2>
    <p class="text-gray-500 text-sm leading-relaxed mb-2">O método DISC mapeia quatro dimensões do comportamento: <strong>Dominância (D)</strong>, <strong>Influência (I)</strong>, <strong>Estabilidade (S)</strong> e <strong>Conformidade (C)</strong>.</p>
    <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed mb-4">São <strong>56 questões</strong> em dois blocos: <strong>Perfil Natural</strong> (como você é) e <strong>Perfil Adaptado</strong> (como age no trabalho). Em cada uma, escolha a opção <strong>mais</strong> e <strong>menos</strong> parecida com você.</p>
    <div class="grid grid-cols-4 gap-2 max-w-xs mx-auto mb-6">
      <div class="bg-d text-white rounded-xl p-3 font-bold text-center text-sm">D<br><span class="font-normal text-xs">Dominância</span></div>
      <div class="bg-i text-white rounded-xl p-3 font-bold text-center text-sm">I<br><span class="font-normal text-xs">Influência</span></div>
      <div class="bg-s text-white rounded-xl p-3 font-bold text-center text-sm">S<br><span class="font-normal text-xs">Estabilidade</span></div>
      <div class="bg-c text-white rounded-xl p-3 font-bold text-center text-sm">C<br><span class="font-normal text-xs">Conformidade</span></div>
    </div>
    <button onclick="iniciar()" class="bg-[#1a1a2e] text-white px-12 py-3.5 rounded-full font-semibold shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all">Iniciar Teste</button>
    <div class="flex justify-center gap-3 mt-5 flex-wrap">
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500"><strong>56</strong> questões</span>
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500"><strong>2</strong> blocos</span>
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500"><strong>~15</strong> min</span>
      <span class="bg-white dark:bg-gray-800 border rounded-full px-4 py-1.5 text-xs text-gray-500">v<strong>2.0</strong></span>
    </div>
    <button onclick="toggleDarkMode()" class="mt-4 text-xs text-gray-400 underline">Alternar modo escuro</button>
  </div>
</section>

<section id="quiz" class="py-8 px-4" style="display:none">
  <div class="max-w-2xl mx-auto">
    <div class="bg-white rounded-xl shadow-sm p-5 mb-5">
      <div class="flex justify-between items-center mb-3">
        <span id="blocoLabel" class="bg-[#1a1a2e] text-white text-xs font-bold px-3 py-1 rounded-full">Perfil Natural</span>
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
    <h2 class="text-xl font-bold mb-2">Bloco 1 Concluído!</h2>
    <p class="text-gray-500 dark:text-gray-400 text-sm mb-2">Você completou o <strong>Perfil Natural</strong> (como você é).</p>
    <p class="text-gray-500 dark:text-gray-400 text-sm mb-6">Agora responda o <strong>Perfil Adaptado</strong> — como você age no seu ambiente de trabalho atual.</p>
    <button onclick="iniciarBlocoAdaptado()" class="bg-[#1a1a2e] text-white px-10 py-3 rounded-full font-semibold shadow-lg">Iniciar Bloco 2 →</button>
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
  <p>TeclaPonto — Análise Comportamental DISC. Instrumento de autoconhecimento. Não substitui avaliação psicológica profissional.</p>
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