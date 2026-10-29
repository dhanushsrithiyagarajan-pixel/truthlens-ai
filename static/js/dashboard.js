/**
 * TruthLens AI - Dashboard & Metrics Visualizer (Module A)
 */

let verdictChartInstance = null;
let categoryChartInstance = null;

async function loadDashboardMetrics() {
  try {
    const res = await fetch('/api/metrics');
    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    const m = json.data;

    // Update Counter Badges
    document.getElementById('metric-total-reports').textContent = m.total_reports;
    document.getElementById('metric-user-reports').textContent = `${m.user_reports} Live Submissions`;
    document.getElementById('metric-demo-reports').textContent = `${m.demo_reports} Seeded Samples`;
    document.getElementById('metric-avg-confidence').textContent = `${m.avg_confidence}%`;
    document.getElementById('metric-total-checklists').textContent = m.total_checklists;
    document.getElementById('metric-quiz-attempts').textContent = m.total_quizzes;
    document.getElementById('metric-avg-quiz').textContent = `${m.avg_quiz_score}% Avg Score`;

    // Render Charts
    renderVerdictChart(m.verdict_counts);
    renderCategoryChart(m.category_counts);

    // Render Recent Table
    renderRecentReports(m.recent_reports);
  } catch (err) {
    console.error('Failed to load metrics:', err);
    window.showToast('Could not load live metrics: ' + err.message, 'error');
  }
}

function renderVerdictChart(counts) {
  const ctx = document.getElementById('chart-verdicts');
  if (!ctx || typeof Chart === 'undefined') return;

  const labels = Object.keys(counts);
  const data = Object.values(counts);

  const colors = labels.map(l => {
    if (l.includes('Supported')) return '#10b981';
    if (l.includes('Contradicted')) return '#ef4444';
    if (l.includes('Misleading')) return '#f59e0b';
    if (l.includes('Suspicious')) return '#dc2626';
    return '#0284c7';
  });

  if (verdictChartInstance) verdictChartInstance.destroy();

  verdictChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderColor: '#0d1527',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#94a3b8', font: { size: 11 } }
        }
      }
    }
  });
}

function renderCategoryChart(counts) {
  const ctx = document.getElementById('chart-categories');
  if (!ctx || typeof Chart === 'undefined') return;

  const labels = Object.keys(counts).map(c => c.charAt(0).toUpperCase() + c.slice(1));
  const data = Object.values(counts);

  if (categoryChartInstance) categoryChartInstance.destroy();

  categoryChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Reports',
        data: data,
        backgroundColor: 'rgba(0, 242, 254, 0.65)',
        borderColor: '#00f2fe',
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        },
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, color: '#94a3b8' },
          grid: { color: 'rgba(255, 255, 255, 0.05)' }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderRecentReports(recent) {
  const tbody = document.getElementById('recent-reports-body');
  if (!tbody) return;

  if (!recent || recent.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:#64748b; padding:1.5rem;">No verification records found yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = recent.map(r => `
    <tr>
      <td>
        <strong>#${r.id}</strong>
        ${r.is_demo ? '<span style="font-size:0.68rem; color:#8b5cf6; margin-left:4px;">[DEMO]</span>' : '<span style="font-size:0.68rem; color:#10b981; margin-left:4px;">[LIVE]</span>'}
      </td>
      <td style="max-width:320px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;" title="${escapeHtml(r.claim)}">
        ${escapeHtml(r.claim)}
      </td>
      <td><span style="text-transform:capitalize;">${r.category}</span></td>
      <td>
        <span class="badge-verdict ${getVerdictClass(r.verdict)}">${r.verdict}</span>
      </td>
      <td>
        <button class="btn-secondary" style="padding:0.25rem 0.65rem; font-size:0.75rem;" onclick="viewReportDetails(${r.id})">
          Inspect
        </button>
      </td>
    </tr>
  `).join('');
}

function getVerdictClass(v) {
  if (v.includes('Supported')) return 'verdict-supported';
  if (v.includes('Contradicted')) return 'verdict-contradicted';
  if (v.includes('Misleading')) return 'verdict-misleading';
  if (v.includes('Suspicious')) return 'verdict-suspicious';
  return 'verdict-unverified';
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

window.loadDashboardMetrics = loadDashboardMetrics;
window.getVerdictClass = getVerdictClass;
window.escapeHtml = escapeHtml;
