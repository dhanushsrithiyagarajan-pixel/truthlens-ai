/**
 * TruthLens AI - Source Credibility Explorer (Module D)
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('source-inspect-form');
  if (form) {
    form.addEventListener('submit', handleSourceInspect);
  }
});

async function handleSourceInspect(e) {
  e.preventDefault();

  const url = document.getElementById('input-inspect-url').value.trim();
  if (!url) {
    window.showToast('Please enter a URL to inspect.', 'warning');
    return;
  }

  const btn = document.getElementById('source-inspect-btn');
  const origText = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `<span>⏳ Inspecting Anatomy...</span>`;

  try {
    const res = await fetch('/api/source/inspect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    renderSourceInspection(json.data);
    window.showToast('Domain anatomy inspected!', 'success');
  } catch (err) {
    console.error('Source inspection error:', err);
    window.showToast('Inspection failed: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

function renderSourceInspection(d) {
  const resultCard = document.getElementById('source-inspection-results');
  if (!resultCard) return;

  resultCard.style.display = 'block';
  resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  // Domain breakdown tags
  document.getElementById('inspect-domain-name').textContent = d.domain;
  document.getElementById('inspect-protocol').textContent = d.protocol.toUpperCase();
  document.getElementById('inspect-tld').textContent = d.tld || 'Standard';

  // Tier badge
  const badge = document.getElementById('inspect-tier-badge');
  badge.textContent = d.credibility_tier;
  badge.className = `badge-verdict ${d.badge_color === 'emerald' ? 'verdict-supported' : d.badge_color === 'red' ? 'verdict-suspicious' : 'verdict-misleading'}`;

  // Risk Score Meter
  document.getElementById('inspect-risk-score').textContent = `${d.risk_score} / 100 Risk`;
  document.getElementById('inspect-risk-bar').style.width = `${d.risk_score}%`;
  document.getElementById('inspect-risk-bar').style.backgroundColor = d.risk_score >= 60 ? '#ef4444' : d.risk_score >= 30 ? '#f59e0b' : '#10b981';

  // Positive & Caution indicators
  const posList = document.getElementById('inspect-positive-list');
  posList.innerHTML = (d.positive_indicators && d.positive_indicators.length > 0)
    ? d.positive_indicators.map(i => `<li>${window.escapeHtml(i)}</li>`).join('')
    : `<li>No specific positive structural endorsements noted.</li>`;

  const cautionList = document.getElementById('inspect-caution-list');
  cautionList.innerHTML = (d.caution_indicators && d.caution_indicators.length > 0)
    ? d.caution_indicators.map(i => `<li>${window.escapeHtml(i)}</li>`).join('')
    : `<li>No suspicious domain patterns detected.</li>`;

  // Educational Guidance
  const guideList = document.getElementById('inspect-guidance-list');
  guideList.innerHTML = d.educational_guidance.map(g => `<li>${window.escapeHtml(g)}</li>`).join('');
}

window.handleSourceInspect = handleSourceInspect;
