/**
 * TruthLens AI - Mandatory Automation: Suspicious Claim to Verification Checklist (Module I)
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('automation-form');
  if (form) {
    form.addEventListener('submit', handleAutomationSubmit);
  }
});

async function handleAutomationSubmit(e) {
  e.preventDefault();

  const claim = document.getElementById('auto-claim-input').value.trim();
  const category = document.getElementById('auto-category-select').value;
  const source_url = document.getElementById('auto-source-url').value.trim();

  if (!claim) {
    window.showToast('Please provide a claim to automate.', 'warning');
    return;
  }

  await triggerAutomationFromClaim(claim, category, source_url);
}

async function triggerAutomationFromClaim(claim, category = 'other', source_url = '') {
  const btn = document.getElementById('auto-run-btn');
  let origText = '';
  if (btn) {
    origText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<span>⏳ Synthesizing Verification Protocol...</span>`;
  }

  try {
    const res = await fetch('/api/automation/claim-to-checklist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ claim, category, source_url })
    });

    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    // Transition directly to the interactive checklist loaded with this custom protocol
    if (window.loadCustomChecklistData) {
      window.loadCustomChecklistData(json.data);
    }
  } catch (err) {
    console.error('Automation error:', err);
    window.showToast('Automation failed: ' + err.message, 'error');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = origText;
    }
  }
}

window.triggerAutomationFromClaim = triggerAutomationFromClaim;
