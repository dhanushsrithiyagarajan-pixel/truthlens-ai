/**
 * TruthLens AI - Main Application Controller (SPA Router & Utilities)
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initMobileMenu();

  // Load initial view: Dashboard
  switchView('dashboard');
});

// SPA View Switcher
function switchView(viewName) {
  // Update nav link active state
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.target === viewName);
  });

  // Hide all views, display targeted view
  document.querySelectorAll('.module-view').forEach(view => {
    view.classList.remove('active');
  });

  const targetView = document.getElementById(`view-${viewName}`);
  if (targetView) {
    targetView.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Trigger view-specific data refresh
  if (viewName === 'dashboard') {
    if (window.loadDashboardMetrics) window.loadDashboardMetrics();
  } else if (viewName === 'history') {
    if (window.loadReportsHistory) window.loadReportsHistory();
  } else if (viewName === 'quiz') {
    if (window.resetQuizState) window.resetQuizState();
  }
}

function initNavigation() {
  document.querySelectorAll('[data-target]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const target = trigger.dataset.target;
      switchView(target);

      // Close mobile menu if open
      const navLinks = document.getElementById('nav-links');
      if (navLinks && navLinks.classList.contains('mobile-open')) {
        navLinks.classList.remove('mobile-open');
      }
    });
  });
}

function initMobileMenu() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const navLinks = document.getElementById('nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
    });
  }
}

// Toast Notification Manager
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '❌';
  if (type === 'warning') icon = '⚠️';

  toast.innerHTML = `<span>${icon}</span> <div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Global modal helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove('active');
}

// Expose globally
window.switchView = switchView;
window.showToast = showToast;
window.openModal = openModal;
window.closeModal = closeModal;
