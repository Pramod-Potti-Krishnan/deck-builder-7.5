/**
 * Review Mode for Section Selection
 * Enables visual selection of slide sections for AI regeneration
 *
 * Part of Phase 2: World-Class Editor with AI-Powered Regeneration
 */

let reviewModeActive = false;
const selectedSections = new Set();

/**
 * Initialize Review Mode - register keyboard shortcuts
 * Called automatically when DOM is ready
 */
function initReviewMode() {
  console.log('✅ Review mode initialized');

  // Register keyboard shortcuts
  document.addEventListener('keydown', handleKeyboardShortcut);
}

/**
 * Handle keyboard shortcuts for review mode
 */
function handleKeyboardShortcut(event) {
  // Ignore if user is typing in an input field
  if (event.target.matches('input, textarea, [contenteditable="true"]')) {
    return;
  }

  // R key - Toggle review mode
  if (event.key === 'r' || event.key === 'R') {
    event.preventDefault();
    toggleReviewMode();
  }

  // ESC key - Exit review mode and clear selection
  if (event.key === 'Escape' && reviewModeActive) {
    event.preventDefault();
    exitReviewMode();
  }

  // Delete/Backspace key - Clear selection (keep review mode active)
  if ((event.key === 'Delete' || event.key === 'Backspace') && reviewModeActive && selectedSections.size > 0) {
    event.preventDefault();
    clearSelection();
  }
}

/**
 * Attach event listeners to sections
 * Extracted as separate function with retry logic for DOM timing
 */
function attachSectionListeners() {
  const sections = document.querySelectorAll('[data-section-id]');
  console.log(`Found ${sections.length} selectable sections`);

  if (sections.length === 0) {
    console.warn('⚠️ No sections found yet, retrying in 500ms...');
    // Retry after delay if sections haven't rendered yet
    setTimeout(attachSectionListeners, 500);
    return;
  }

  // Make sections selectable
  sections.forEach(section => {
    section.classList.add('selectable');
    section.addEventListener('click', handleSectionClick);
  });

  console.log('✅ Section listeners attached');
}

/**
 * Enter Review Mode - makes sections selectable
 */
function enterReviewMode() {
  reviewModeActive = true;
  document.body.dataset.mode = 'review';

  console.log('📋 Entering Review Mode...');

  // Wait for Reveal.js to be ready before attaching listeners
  if (typeof Reveal !== 'undefined' && Reveal.isReady && Reveal.isReady()) {
    attachSectionListeners();
  } else {
    // Fallback: attach after delay if Reveal not ready
    console.log('Waiting for Reveal.js to be ready...');
    setTimeout(attachSectionListeners, 500);
  }

  // Show selection indicator
  showSelectionIndicator();

  if (typeof showNotification === 'function') {
    showNotification('📋 Review Mode Active (R) - Click sections to select', 'info');
  }
}

/**
 * Exit Review Mode - restore normal view
 */
function exitReviewMode() {
  reviewModeActive = false;
  document.body.dataset.mode = 'view';

  console.log('👁️ Exiting Review Mode...');

  // Remove selectable state
  const sections = document.querySelectorAll('[data-section-id]');
  sections.forEach(section => {
    section.classList.remove('selectable', 'selected');
    section.removeEventListener('click', handleSectionClick);
  });

  // Clear selection
  clearSelection();
  hideSelectionIndicator();

  if (typeof showNotification === 'function') {
    showNotification('Review Mode Exited', 'info');
  }
}

/**
 * Toggle Review Mode on/off
 */
function toggleReviewMode() {
  if (reviewModeActive) {
    exitReviewMode();
  } else {
    enterReviewMode();
  }
}

/**
 * Handle section click in review mode
 */
function handleSectionClick(event) {
  if (!reviewModeActive) return;

  event.stopPropagation();
  const sectionId = event.currentTarget.dataset.sectionId;

  if (event.ctrlKey || event.metaKey) {
    // Multi-select with Ctrl/Cmd
    toggleSectionSelection(sectionId);
  } else {
    // Single select - clear others first
    clearSelection();
    selectSection(sectionId);
  }
}

/**
 * Select a section
 */
function selectSection(sectionId) {
  selectedSections.add(sectionId);
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (element) {
    element.classList.add('selected');
  }
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log(`✅ Selected: ${sectionId}`);
}

/**
 * Deselect a section
 */
function deselectSection(sectionId) {
  selectedSections.delete(sectionId);
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (element) {
    element.classList.remove('selected');
  }
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log(`❌ Deselected: ${sectionId}`);
}

/**
 * Toggle section selection
 */
function toggleSectionSelection(sectionId) {
  if (selectedSections.has(sectionId)) {
    deselectSection(sectionId);
  } else {
    selectSection(sectionId);
  }
}

/**
 * Clear all selections
 */
function clearSelection() {
  selectedSections.forEach(sectionId => {
    const element = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (element) {
      element.classList.remove('selected');
    }
  });
  selectedSections.clear();
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log('🧹 Selection cleared');
}

/**
 * Get selected sections with metadata
 */
function getSelectedSections() {
  const sections = [];

  selectedSections.forEach(sectionId => {
    const element = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (element) {
      sections.push({
        sectionId: element.dataset.sectionId,
        sectionType: element.dataset.sectionType,
        slideIndex: parseInt(element.dataset.slideIndex),
        content: element.innerHTML,
        layout: element.closest('[data-layout]')?.dataset.layout || 'unknown'
      });
    }
  });

  return sections;
}

/**
 * Show selection indicator (floating badge)
 */
function showSelectionIndicator() {
  let indicator = document.getElementById('selection-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.id = 'selection-indicator';
    indicator.className = 'selection-indicator';
    document.body.appendChild(indicator);
  }
  updateSelectionIndicator();
}

/**
 * Update selection indicator count
 */
function updateSelectionIndicator() {
  const indicator = document.getElementById('selection-indicator');
  if (indicator) {
    const count = selectedSections.size;
    indicator.textContent = `${count} section${count !== 1 ? 's' : ''} selected`;
    indicator.style.display = count > 0 ? 'block' : 'none';
  }
}

/**
 * Hide selection indicator
 */
function hideSelectionIndicator() {
  const indicator = document.getElementById('selection-indicator');
  if (indicator) {
    indicator.style.display = 'none';
  }
}

/**
 * Show/hide regeneration panel based on selection
 */
function updateRegenerationPanel() {
  const panel = document.getElementById('regeneration-panel');
  if (panel) {
    panel.style.display = selectedSections.size > 0 ? 'block' : 'none';
  }
}

// Export functions for global access
if (typeof window !== 'undefined') {
  window.enterReviewMode = enterReviewMode;
  window.exitReviewMode = exitReviewMode;
  window.toggleReviewMode = toggleReviewMode;
  window.getSelectedSections = getSelectedSections;
  window.clearSelection = clearSelection;
  window.reviewModeActive = () => reviewModeActive;
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initReviewMode);
} else {
  // DOM already loaded, initialize immediately
  initReviewMode();
}

console.log('✅ Review Mode module loaded');
