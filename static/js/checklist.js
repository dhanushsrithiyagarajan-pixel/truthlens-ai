/**
 * TruthLens AI - Interactive Verification Checklist & Dossier (Module E & I)
 */

let activeChecklist = {
  id: null,
  claim_title: "General Verification Protocol",
  category: "other",
  completed_steps: 0,
  total_steps: 10,
  final_verdict: "In Progress — Verification Pending",
  final_notes: "",
  steps: []
};

// Default 10-step verification template
const DEFAULT_VERIFICATION_STEPS = [
  {
    step_id: 1,
    title: "Primary Source & Domain Check",
    category: "Source Verification",
    instruction: "Identify the primary publisher or origin account. Is it an authorized domain, or an impersonator?",
    target_action: "Examine domain URL and inspect WHOIS age or 'About Us' credentials.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 2,
    title: "Author Credential & Timestamp Audit",
    category: "Attribution",
    instruction: "Identify who authored the content and when it was originally published.",
    target_action: "Verify author byline on Google Scholar/LinkedIn; check original publication timestamp.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 3,
    title: "Reverse Image & Video Forensics",
    category: "Media Forensics",
    instruction: "Run any embedded imagery or video keyframes through reverse search engines.",
    target_action: "Use Google Lens, TinEye, or the TruthLens Deepfake Awareness Lab.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 4,
    title: "Original Context & Chronology Check",
    category: "Contextual Accuracy",
    instruction: "Determine if an authentic older photo or quote is being falsely repurposed for current events.",
    target_action: "Check date of earliest indexed appearance using search engine date filters.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 5,
    title: "Independent Reputable Source Comparison",
    category: "Corroboration",
    instruction: "Look for corroboration across at least 2 independent accredited news wires.",
    target_action: "Consult Reuters, AP News, PTI, BBC, or official regulatory registers.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 6,
    title: "Primary Evidence & Citation Review",
    category: "Citation Audit",
    instruction: "Check if laws, government notifications, court orders, or scientific studies actually exist.",
    target_action: "Review official government gazette (egazette.gov.in) or scientific repositories (PubMed).",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 7,
    title: "Visual Artifacts & Deepfake Indicators",
    category: "Synthesis Analysis",
    instruction: "Inspect facial edges, pupil reflections, teeth regularity, and background geometry for AI artifacts.",
    target_action: "Run Error Level Analysis (ELA) and zoom into high-contrast boundaries.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 8,
    title: "Emotional Manipulation & Panic Audit",
    category: "Psychological Heuristics",
    instruction: "Analyze tone: Does the content provoke extreme fear, greed, or demand immediate forwarding?",
    target_action: "Flag urgent deadlines, sensationalized superlatives, and outrage-farming phrasing.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 9,
    title: "Scam & Cyber Fraud Pattern Check",
    category: "Threat Assessment",
    instruction: "Check for financial fraud markers: requests for OTP, payment transfers, APK installs, or lottery winnings.",
    target_action: "Report suspected financial scams to 1930 / cybercrime.gov.in.",
    completed: false,
    user_notes: ""
  },
  {
    step_id: 10,
    title: "Final Decision, Documentation & Reporting",
    category: "Reporting Guidance",
    instruction: "Synthesize notes into a formal verdict. If false or harmful, do not share and warn contacts responsibly.",
    target_action: "Export completed TruthLens verification dossier.",
    completed: false,
    user_notes: ""
  }
];

document.addEventListener('DOMContentLoaded', () => {
  initDefaultChecklist();

  const saveBtn = document.getElementById('checklist-save-btn');
  if (saveBtn) saveBtn.addEventListener('click', saveChecklistToBackend);

  const printBtn = document.getElementById('checklist-print-btn');
  if (printBtn) printBtn.addEventListener('click', () => window.print());
});

function initDefaultChecklist() {
  activeChecklist.steps = JSON.parse(JSON.stringify(DEFAULT_VERIFICATION_STEPS));
  renderChecklistUI();
}

function renderChecklistUI() {
  document.getElementById('checklist-claim-display').textContent = activeChecklist.claim_title;
  document.getElementById('checklist-category-display').textContent = `Category: ${activeChecklist.category.toUpperCase()}`;

  const container = document.getElementById('checklist-steps-container');
  if (!container) return;

  container.innerHTML = activeChecklist.steps.map((s, idx) => `
    <div class="checklist-step-item ${s.completed ? 'completed' : ''}" id="step-box-${idx}">
      <div class="step-item-header">
        <div class="step-item-left">
          <input type="checkbox" id="check-step-${idx}" ${s.completed ? 'checked' : ''} onchange="toggleStep(${idx})">
          <div>
            <strong>Step ${s.step_id}: ${window.escapeHtml(s.title)}</strong>
            <span class="step-badge">${window.escapeHtml(s.category)}</span>
          </div>
        </div>
        <span style="font-size:0.75rem; color:${s.completed ? '#10b981' : '#64748b'};">
          ${s.completed ? '✓ Completed' : 'Pending Review'}
        </span>
      </div>
      <p style="font-size:0.86rem; color:#cbd5e1; margin-bottom:0.4rem;">${window.escapeHtml(s.instruction)}</p>
      <div style="font-size:0.78rem; color:#38bdf8; margin-bottom:0.6rem;">
        ⚡ <strong>Target Action:</strong> ${window.escapeHtml(s.target_action)}
      </div>
      <div>
        <label style="font-size:0.75rem; color:#94a3b8;">Your Investigation Notes & Evidence Findings:</label>
        <textarea 
          style="min-height:60px; font-size:0.85rem;" 
          placeholder="Record source URLs, discrepancy observations, or findings here..."
          onchange="updateStepNotes(${idx}, this.value)"
        >${window.escapeHtml(s.user_notes || '')}</textarea>
      </div>
    </div>
  `).join('');

  updateProgressSummary();
}

function toggleStep(idx) {
  activeChecklist.steps[idx].completed = !activeChecklist.steps[idx].completed;
  const box = document.getElementById(`step-box-${idx}`);
  if (box) box.classList.toggle('completed', activeChecklist.steps[idx].completed);
  updateProgressSummary();
}

function updateStepNotes(idx, notes) {
  activeChecklist.steps[idx].user_notes = notes;
}

function updateProgressSummary() {
  const completedCount = activeChecklist.steps.filter(s => s.completed).length;
  activeChecklist.completed_steps = completedCount;
  const pct = Math.round((completedCount / activeChecklist.total_steps) * 100);

  document.getElementById('checklist-progress-text').textContent = `${completedCount} of 10 Steps Completed (${pct}%)`;
  document.getElementById('checklist-progress-bar').style.width = `${pct}%`;
}

async function saveChecklistToBackend() {
  const finalVerdict = document.getElementById('checklist-final-verdict').value;
  const finalNotes = document.getElementById('checklist-final-notes').value;

  activeChecklist.final_verdict = finalVerdict;
  activeChecklist.final_notes = finalNotes;

  try {
    const res = await fetch('/api/checklists/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        id: activeChecklist.id,
        claim_title: activeChecklist.claim_title,
        category: activeChecklist.category,
        checklist_data: activeChecklist.steps,
        completed_steps: activeChecklist.completed_steps,
        total_steps: activeChecklist.total_steps,
        final_verdict: activeChecklist.final_verdict,
        final_notes: activeChecklist.final_notes
      })
    });

    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    activeChecklist.id = json.checklist_id;
    window.showToast('Checklist state saved to database!', 'success');
  } catch (err) {
    console.error('Failed to save checklist:', err);
    window.showToast('Error saving checklist: ' + err.message, 'error');
  }
}

// Function to load automated checklist returned by Module I
function loadCustomChecklistData(customData) {
  activeChecklist.id = customData.checklist_id || null;
  activeChecklist.claim_title = customData.claim_title;
  activeChecklist.category = customData.inferred_category || 'other';
  activeChecklist.steps = customData.steps;
  activeChecklist.completed_steps = 0;
  activeChecklist.total_steps = 10;
  activeChecklist.final_verdict = 'In Progress';
  activeChecklist.final_notes = `Checklist generated by TruthLens Automation for claim: "${customData.main_claim}"`;

  renderChecklistUI();
  window.switchView('checklist');
  window.showToast('Customized 10-step protocol loaded into checklist!', 'success');
}

window.toggleStep = toggleStep;
window.updateStepNotes = updateStepNotes;
window.loadCustomChecklistData = loadCustomChecklistData;
