/**
 * TruthLens AI - Deepfake Awareness & Image Forensics Lab (Module C)
 */

document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('image-dropzone');
  const fileInput = document.getElementById('image-file-input');

  if (dropzone && fileInput) {
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
      dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        fileInput.files = e.dataTransfer.files;
        handleImageSelection(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleImageSelection(e.target.files[0]);
      }
    });
  }

  const runAnalysisBtn = document.getElementById('run-image-analysis-btn');
  if (runAnalysisBtn) {
    runAnalysisBtn.addEventListener('click', executeImageAnalysis);
  }
});

let selectedImageFile = null;

function handleImageSelection(file) {
  // Validate format and size
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    window.showToast('Please upload a valid JPG, PNG, or WEBP image.', 'error');
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    window.showToast('Image exceeds 5MB size limit.', 'error');
    return;
  }

  selectedImageFile = file;

  // Safe client-side preview
  const reader = new FileReader();
  reader.onload = (e) => {
    document.getElementById('preview-original').src = e.target.result;
    document.getElementById('image-lab-results').style.display = 'block';
    document.getElementById('dropzone-filename').textContent = `Loaded: ${file.name} (${Math.round(file.size / 1024)} KB)`;
    window.showToast(`Loaded ${file.name}. Review visual checks and click 'Run Forensic Analysis'.`, 'info');
  };
  reader.readAsDataURL(file);
}

async function executeImageAnalysis() {
  if (!selectedImageFile) {
    window.showToast('Please select or drop an image first.', 'warning');
    return;
  }

  const btn = document.getElementById('run-image-analysis-btn');
  const origText = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = `<span>⏳ Extracting EXIF & Generating ELA...</span>`;

  // Collect visual check selections
  const visualChecks = {};
  document.querySelectorAll('.visual-check-box').forEach(cb => {
    visualChecks[cb.dataset.checkKey] = cb.checked;
  });

  const formData = new FormData();
  formData.append('image', selectedImageFile);
  formData.append('visual_checks', JSON.stringify(visualChecks));

  try {
    const res = await fetch('/api/image-lab/analyze', {
      method: 'POST',
      body: formData
    });

    const json = await res.json();
    if (json.status !== 'success') throw new Error(json.message);

    renderImageLabResults(json);
    window.showToast('Forensic analysis completed!', 'success');
  } catch (err) {
    console.error('Image lab error:', err);
    window.showToast('Forensics failed: ' + err.message, 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = origText;
  }
}

function renderImageLabResults(data) {
  // Update ELA preview
  const elaImg = document.getElementById('preview-ela');
  if (data.ela_url) {
    elaImg.src = data.ela_url;
    elaImg.style.display = 'block';
    document.getElementById('ela-container').style.display = 'block';
  } else {
    document.getElementById('ela-container').style.display = 'none';
  }

  // Update Metadata Table
  const meta = data.metadata || {};
  document.getElementById('meta-dimensions').textContent = meta.dimensions || 'Unknown';
  document.getElementById('meta-camera').textContent = `${meta.camera_make} / ${meta.camera_model}`;
  document.getElementById('meta-software').textContent = meta.software || 'None detected';
  document.getElementById('meta-datetime').textContent = meta.date_time_original || 'Not recorded';

  // Render Clues / Indicators
  const cluesList = document.getElementById('image-indicators-list');
  const indicators = data.assessment.indicators || [];
  if (indicators.length > 0) {
    cluesList.innerHTML = indicators.map(i => `<li>${window.escapeHtml(i)}</li>`).join('');
  } else {
    cluesList.innerHTML = `<li>No specific visual or metadata anomalies recorded.</li>`;
  }

  // Verdict & Summary
  document.getElementById('image-assessment-verdict').textContent = data.assessment.verdict;
  document.getElementById('image-assessment-summary').textContent = data.assessment.summary;

  // Reverse Search Buttons
  const toolsContainer = document.getElementById('reverse-search-tools-container');
  if (toolsContainer && data.reverse_search_tools) {
    toolsContainer.innerHTML = data.reverse_search_tools.map(t => `
      <a href="${t.url}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="font-size:0.8rem; padding:0.4rem 0.8rem;">
        🔍 ${t.name}
      </a>
    `).join('');
  }
}

window.handleImageSelection = handleImageSelection;
window.executeImageAnalysis = executeImageAnalysis;
