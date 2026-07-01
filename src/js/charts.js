// ===== GRÁFICO =====
function gerarGrafico(nome, scores, perfil) {
  return `
    <div class="bg-white rounded-2xl shadow-sm p-5 sm:p-8 mb-6 fade-in">
      <h3 class="text-lg font-bold mb-4 text-center">Gráfico de Perfil DISC</h3>
      <div class="relative" style="height:320px">
        <canvas id="chartDISC"></canvas>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-center">
        ${FACTORES.map(f => `
          <div>
            <div class="font-bold text-lg" style="color:${CORES[f]}">${f}</div>
            <div class="text-2xl font-bold">${scores[f] > 0 ? '+' : ''}${scores[f]}</div>
            <div class="text-xs text-gray-400">${classificarScore(scores[f])}</div>
          </div>
        `).join('')}
      </div>
    </div>`;
}

function initGrafico(scores) {
  const ctx = document.getElementById('chartDISC');
  if (!ctx) return;
  if (window._chart) window._chart.destroy();

  window._chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: FACTORES,
      datasets: [{
        label: 'Score DISC',
        data: FACTORES.map(f => scores[f]),
        backgroundColor: FACTORES.map(f => CORES[f] + 'CC'),
        borderColor: FACTORES.map(f => CORES[f]),
        borderWidth: 2,
        borderRadius: 6,
        barPercentage: 0.6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: c => `Score: ${c.parsed.y > 0 ? '+' : ''}${c.parsed.y}`,
            afterLabel: c => {
              const f = FACTORES[c.dataIndex];
              return classificarScore(scores[f]) + (Math.abs(scores[f]) > 8 ? '\n⚠️ Zona Cinzenta' : '');
            }
          }
        }
      },
      scales: {
        y: {
          min: -11, max: 11,
          ticks: {
            stepSize: 2,
            callback: v => v === -10 ? '-10 (↓ Baixo)' : v === 0 ? '0 (Neutro)' : v === 10 ? '10 (↑ Alto)' : v
          },
          grid: {
            color: c => c.tick.value === 0 ? '#333' : c.tick.value % 4 === 0 ? '#ddd' : '#eee'
          }
        }
      }
    },
    plugins: [{
      id: 'zoneLines',
      afterDraw(chart) {
        const yScale = chart.scales.y;
        const c = chart.ctx;
        [-8, 8].forEach(val => {
          const y = yScale.getPixelForValue(val);
          c.save();
          c.setLineDash([5, 5]);
          c.strokeStyle = val > 0 ? '#E74C3C' : '#2980B9';
          c.lineWidth = 1.5;
          c.beginPath();
          c.moveTo(chart.chartArea.left, y);
          c.lineTo(chart.chartArea.right, y);
          c.stroke();
          c.restore();
        });
      }
    }]
  });
}