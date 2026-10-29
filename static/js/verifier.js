/**
 * TruthLens AI - Claim Verification Controller (Module B)
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('claim-verify-form');
  if (form) {
    form.addEventListener('submit', handleClaimVerification);
  }

  // Pre-load sample buttons
  document.querySelectorAll('[data-sample-claim]').forEach(btn => {
    btn.addEventListener('click', () => {
      document.getElementById('input-claim').value = btn.dataset.sampleClaim;
      document.getElementById('input-source-url').value = btn.dataset.sampleUrl || '';
      document.getElementById('input-source-name').value = btn.dataset.sampleSource || '';
      document.getElementById('select-category').value = btn.dataset.sampleCategory || 'other';
      window.showToast('Loaded sample benchmark claim.', 'info');
    });
  });
});

async function handleClaimVerification(e) {
  e.preventDefault();

  const claim = document.getElementById('input-claim').value.trim();
  const source_url = document.getElementById('input-source-url').value.trim();
  const source_name = document.getElementById('input-source-name').value.trim();
  const category = document.getElementById('select-category').value;
  const context = document.getElementById('input-context').value.trim();

  if (!claim) {
    window.showToast('Please enter a claim to verify.', 'warning');
    return;
  }

  const submitBtn = document.getElementById('verify-submit-btn');
  const originalText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<span>⏳ Analyzing with Evidence Engine...</span>`;

  try {
    const res = await fetch('/api/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ claim, source_url, source_name, category, context })
    });

    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    renderVerificationResult(json.data);
    window.showToast('Structured verification report generated!', 'success');
  } catch (err) {
    console.error('Verification error:', err);
    window.showToast('Verification failed: ' + err.message, 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  }
}

function renderVerificationResult(data) {
  const resultBox = document.getElementById('verification-result-box');
  if (!resultBox) return;

  resultBox.style.display = 'block';
  resultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Store active report for export
  window.currentVerificationReport = data;

  // Header Elements
  const badgeClass = window.getVerdictClass ? window.getVerdictClass(data.verdict) : 'verdict-unverified';
  document.getElementById('res-verdict-badge').className = `badge-verdict ${badgeClass}`;
  document.getElementById('res-verdict-badge').textContent = data.verdict;

  document.getElementById('res-confidence-num').textContent = `${data.confidence}%`;
  document.getElementById('res-confidence-bar').style.width = `${data.confidence}%`;

  document.getElementById('res-engine-mode').textContent = data.engine_mode || 'TruthLens Fact-Check Engine';

  // Section 1: Main Claim & Deconstruction
  document.getElementById('res-main-claim').textContent = data.main_claim;

  // Factual vs Opinion Statements
  const factsList = document.getElementById('res-facts-list');
  factsList.innerHTML = (data.factual_statements && data.factual_statements.length > 0)
    ? data.factual_statements.map(s => `<li>${window.escapeHtml(s)}</li>`).join('')
    : `<li>No explicit empirical statements separated.</li>`;

  const opinionsList = document.getElementById('res-opinions-list');
  opinionsList.innerHTML = (data.opinion_statements && data.opinion_statements.length > 0)
    ? data.opinion_statements.map(s => `<li>${window.escapeHtml(s)}</li>`).join('')
    : `<li>No overt emotional opinion markers detected.</li>`;

  // Section 2: Corroboration Needs
  const needsList = document.getElementById('res-needs-list');
  needsList.innerHTML = (data.corroboration_needs && data.corroboration_needs.length > 0)
    ? data.corroboration_needs.map(s => `<li>${window.escapeHtml(s)}</li>`).join('')
    : `<li>Independent primary documentation required.</li>`;

  // Section 3: Evidence Summary & Suspicious Indicators
  document.getElementById('res-evidence-summary').textContent = data.evidence_summary;

  const indicatorsBox = document.getElementById('res-indicators-container');
  const indicatorsList = document.getElementById('res-indicators-list');
  if (data.suspicious_indicators && data.suspicious_indicators.length > 0) {
    indicatorsBox.style.display = 'block';
    indicatorsList.innerHTML = data.suspicious_indicators.map(i => `<li>${window.escapeHtml(i)}</li>`).join('');
  } else {
    indicatorsBox.style.display = 'none';
  }

  // Section 4: Recommendations
  const recsList = document.getElementById('res-recommendations-list');
  recsList.innerHTML = (data.recommendations && data.recommendations.length > 0)
    ? data.recommendations.map(r => `<li>${window.escapeHtml(r)}</li>`).join('')
    : `<li>Verify claim against accredited public databases.</li>`;

  // Section 5: Limitations
  document.getElementById('res-limitations').textContent = data.limitations;
}

// Global hook to trigger automation from verification result
function convertCurrentClaimToChecklist() {
  if (!window.currentVerificationReport) {
    window.showToast('No active report available to convert.', 'warning');
    return;
  }
  const rep = window.currentVerificationReport;
  if (window.triggerAutomationFromClaim) {
    window.triggerAutomationFromClaim(rep.claim, rep.category, rep.source_url);
  }
}

function exportCurrentReport(format) {
  if (!window.currentVerificationReport || !window.currentVerificationReport.id) {
    window.showToast('Save or submit report first before exporting.', 'warning');
    return;
  }
  const id = window.currentVerificationReport.id;
  window.open(`/api/export/report/${id}?format=${format}`, '_blank');
}

window.convertCurrentClaimToChecklist = convertCurrentClaimToChecklist;
window.exportCurrentReport = exportCurrentReport;
window.renderVerificationResult = renderVerificationResult;
