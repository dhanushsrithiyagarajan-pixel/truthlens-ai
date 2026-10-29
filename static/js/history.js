/**
 * TruthLens AI - Report History & Export Controller (Module H)
 */

document.addEventListener('DOMContentLoaded', () => {
  const filterCat = document.getElementById('history-filter-category');
  const filterVerdict = document.getElementById('history-filter-verdict');
  const searchInput = document.getElementById('history-search-input');

  if (filterCat) filterCat.addEventListener('change', loadReportsHistory);
  if (filterVerdict) filterVerdict.addEventListener('change', loadReportsHistory);
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(loadReportsHistory, 300);
    });
  }
});

async function loadReportsHistory() {
  const cat = document.getElementById('history-filter-category')?.value || 'all';
  const ver = document.getElementById('history-filter-verdict')?.value || 'all';
  const search = document.getElementById('history-search-input')?.value.trim() || '';

  const params = new URLSearchParams();
  if (cat !== 'all') params.append('category', cat);
  if (ver !== 'all') params.append('verdict', ver);
  if (search) params.append('search', search);

  try {
    const res = await fetch(`/api/reports?${params.toString()}`);
    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    renderHistoryTable(json.data);
  } catch (err) {
    console.error('History fetch failed:', err);
    window.showToast('Failed to load history: ' + err.message, 'error');
  }
}

function renderHistoryTable(reports) {
  const tbody = document.getElementById('history-table-body');
  if (!tbody) return;

  if (!reports || reports.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:#64748b; padding:2rem;">No matching verification dossiers found.</td></tr>`;
    return;
  }

  tbody.innerHTML = reports.map(r => `
    <tr>
      <td>
        <strong>#${r.id}</strong>
        ${r.is_demo ? '<span style="font-size:0.68rem; color:#8b5cf6; margin-left:4px;">[DEMO]</span>' : '<span style="font-size:0.68rem; color:#10b981; margin-left:4px;">[LIVE]</span>'}
      </td>
      <td style="max-width:280px; text-overflow:ellipsis; overflow:hidden; white-space:nowrap;" title="${window.escapeHtml(r.claim)}">
        ${window.escapeHtml(r.claim)}
      </td>
      <td><span style="text-transform:capitalize;">${r.category}</span></td>
      <td>
        <span class="badge-verdict ${window.getVerdictClass ? window.getVerdictClass(r.verdict) : ''}">
          ${r.verdict}
        </span>
      </td>
      <td><strong>${r.confidence}%</strong></td>
      <td style="font-size:0.78rem; color:#94a3b8;">${r.created_at || 'Recent'}</td>
      <td>
        <div style="display:flex; align-items:center; gap:0.35rem;">
          <button class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="viewReportDetails(${r.id})">
            👁 View
          </button>
          <button class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="window.open('/api/export/report/${r.id}?format=markdown', '_blank')" title="Export Markdown">
            📄 MD
          </button>
          <button class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="window.open('/api/export/report/${r.id}?format=json', '_blank')" title="Export JSON">
            💾 JSON
          </button>
          ${!r.is_demo ? `
            <button class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem; color:#ef4444; border-color:rgba(239,68,68,0.3);" onclick="confirmDeleteReport(${r.id})">
              🗑
            </button>
          ` : ''}
        </div>
      </td>
    </tr>
  `).join('');
}

async function viewReportDetails(reportId) {
  try {
    const res = await fetch(`/api/reports/${reportId}`);
    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    const r = json.data;
    document.getElementById('modal-report-id').textContent = `#${r.id}`;
    document.getElementById('modal-report-type').textContent = r.is_demo ? 'Demonstration Sample' : 'Live User Submission';
    document.getElementById('modal-claim-text').textContent = r.claim;
    document.getElementById('modal-source-info').textContent = `${r.source_name} (${r.source_url || 'No URL cited'})`;
    document.getElementById('modal-verdict-badge').textContent = r.verdict;
    document.getElementById('modal-verdict-badge').className = `badge-verdict ${window.getVerdictClass ? window.getVerdictClass(r.verdict) : ''}`;
    document.getElementById('modal-confidence').textContent = `${r.confidence}%`;
    document.getElementById('modal-main-claim').textContent = r.main_claim;
    document.getElementById('modal-evidence').textContent = r.evidence_summary;

    const modalFacts = document.getElementById('modal-facts-list');
    modalFacts.innerHTML = (r.factual_statements && r.factual_statements.length > 0)
      ? r.factual_statements.map(s => `<li>${window.escapeHtml(s)}</li>`).join('')
      : '<li>No explicit empirical statements separated.</li>';

    const modalIndicators = document.getElementById('modal-indicators-list');
    modalIndicators.innerHTML = (r.suspicious_indicators && r.suspicious_indicators.length > 0)
      ? r.suspicious_indicators.map(i => `<li>${window.escapeHtml(i)}</li>`).join('')
      : '<li>No suspicious indicators detected.</li>';

    const modalRecs = document.getElementById('modal-recs-list');
    modalRecs.innerHTML = (r.recommendations && r.recommendations.length > 0)
      ? r.recommendations.map(re => `<li>${window.escapeHtml(re)}</li>`).join('')
      : '<li>Conduct independent multi-source verification.</li>';

    // Export links in modal
    document.getElementById('modal-export-md').onclick = () => window.open(`/api/export/report/${r.id}?format=markdown`, '_blank');
    document.getElementById('modal-export-json').onclick = () => window.open(`/api/export/report/${r.id}?format=json`, '_blank');

    window.openModal('report-detail-modal');
  } catch (err) {
    console.error('Failed to load report detail:', err);
    window.showToast('Could not load report details: ' + err.message, 'error');
  }
}

async function confirmDeleteReport(reportId) {
  if (!confirm(`Are you sure you want to delete report #${reportId}? This action cannot be undone.`)) {
    return;
  }

  try {
    const res = await fetch(`/api/reports/${reportId}`, { method: 'DELETE' });
    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    window.showToast(`Report #${reportId} deleted successfully.`, 'success');
    loadReportsHistory();
    if (window.loadDashboardMetrics) window.loadDashboardMetrics();
  } catch (err) {
    console.error('Delete failed:', err);
    window.showToast('Delete failed: ' + err.message, 'error');
  }
}

window.loadReportsHistory = loadReportsHistory;
window.viewReportDetails = viewReportDetails;
window.confirmDeleteReport = confirmDeleteReport;
