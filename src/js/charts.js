// ===== GRÁFICOS I / II / III =====

function gerarGraficosTriplos(dual) {
  return `
    <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in card">
      <h3 class="text-lg font-bold mb-6 text-center">Gráficos DISC — Natural · Pressão · Adaptado</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <p class="text-xs font-bold text-center mb-2 text-green-700">III — Autoimagem (Natural)</p>
          <div style="height:220px"><canvas id="chartNatural"></canvas></div>
        </div>
        <div>
          <p class="text-xs font-bold text-center mb-2 text-purple-700">II — Pressão (Diferença)</p>
          <div style="height:220px"><canvas id="chartPressure"></canvas></div>
        </div>
        <div>
          <p class="text-xs font-bold text-center mb-2 text-blue-700">I — Adaptado (Trabalho)</p>
          <div style="height:220px"><canvas id="chartAdapted"></canvas></div>
        </div>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 text-center">
        ${FACTORES.map(f => `
          <div class="p-2 rounded-lg bg-gray-50 dark:bg-gray-800">
            <div class="font-bold" style="color:${CORES[f]}">${f}</div>
            <div class="text-xs text-gray-500">Nat: ${dual.natural[f] > 0 ? '+' : ''}${dual.natural[f]}</div>
            <div class="text-xs text-gray-500">Adp: ${dual.adapted[f] > 0 ? '+' : ''}${dual.adapted[f]}</div>
            <div class="text-xs ${Math.abs(dual.discrepancy[f]) >= DISCREPANCY_THRESHOLD ? 'text-red-500 font-bold' : 'text-gray-400'}">Δ ${dual.discrepancy[f] > 0 ? '+' : ''}${dual.discrepancy[f]}</div>
          </div>`).join('')}
      </div>
    </div>`;
}

function makeChart(canvasId, data, windowKey, label) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return;
  if (window[windowKey]) window[windowKey].destroy();
  window[windowKey] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: FACTORES,
      datasets: [{
        label,
        data: FACTORES.map(f => data[f]),
        backgroundColor: FACTORES.map(f => CORES[f] + 'CC'),
        borderColor: FACTORES.map(f => CORES[f]),
        borderWidth: 2, borderRadius: 4, barPercentage: 0.65
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { min: -11, max: 11, ticks: { stepSize: 5 },
          grid: { color: c => c.tick.value === 0 ? '#333' : '#eee' } }
      }
    }
  });
}

function initGraficosTriplos(dual) {
  makeChart('chartNatural', dual.natural, '_chartNat', 'Natural');
  makeChart('chartAdapted', dual.adapted, '_chartAdp', 'Adaptado');
  makeChart('chartPressure', dual.discrepancy, '_chartPress', 'Pressão');
}