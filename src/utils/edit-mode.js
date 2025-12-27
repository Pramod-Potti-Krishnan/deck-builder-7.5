/**
 * Edit Mode for v7.5-main Presentations
 *
 * Enables in-browser editing of slide content with:
 * - contentEditable for text fields
 * - Save/Cancel functionality
 * - Version history integration
 * - Visual editing indicators
 * - Rich text formatting toolbar
 * - Auto-save with debounce
 */

// State management
let isEditMode = false;
let originalContent = null;
let presentationId = null;
let inputListeners = []; // Track input listeners for cleanup

/**
 * Initialize edit mode system
 */
function initEditMode() {
  // Extract presentation ID from URL
  const urlParts = window.location.pathname.split('/');
  presentationId = urlParts[urlParts.length - 1];

  // Add keyboard shortcut (E key for Edit Mode)
  document.addEventListener('keydown', (e) => {
    // E key (not in input field)
    if (e.key === 'e' && !e.target.isContentEditable && e.target.tagName !== 'INPUT') {
      e.preventDefault();
      toggleEditMode();
    }

    // ESC key to exit edit mode
    if (e.key === 'Escape' && isEditMode) {
      cancelEdits();
    }

    // Ctrl+S / Cmd+S to save (when in edit mode)
    if ((e.ctrlKey || e.metaKey) && e.key === 's' && isEditMode) {
      e.preventDefault();
      saveAllChanges();
    }
  });

  // Auto-exit edit mode when entering fullscreen (Play mode)
  document.addEventListener('fullscreenchange', handleFullscreenChange);
  document.addEventListener('webkitfullscreenchange', handleFullscreenChange);  // Safari

  console.log('✅ Edit mode initialized');
}

/**
 * Handle fullscreen changes - exit edit mode when entering fullscreen
 */
function handleFullscreenChange() {
  const isFullscreen = document.fullscreenElement || document.webkitFullscreenElement;

  if (isFullscreen && isEditMode) {
    console.log('[EditMode] Exiting edit mode for fullscreen presentation');
    exitEditMode();
  }
}

/**
 * Toggle between View and Edit modes
 */
async function toggleEditMode() {
  if (isEditMode) {
    await exitEditMode();
  } else {
    enterEditMode();
  }
}

/**
 * Enter Edit Mode
 */
function enterEditMode() {
  isEditMode = true;
  document.body.dataset.mode = 'edit';

  // Capture current state for cancel functionality
  originalContent = captureCurrentState();

  // Make text fields editable
  enableContentEditing();

  // Initialize text toolbar
  if (typeof initTextToolbar === 'function') {
    initTextToolbar();
  }

  // Initialize auto-save
  if (typeof initAutoSave === 'function') {
    initAutoSave();
  }

  // Set up change tracking for auto-save
  setupChangeTracking();

  // Update UI
  updateEditModeUI();

  // Show notification
  showNotification('📝 Edit Mode Active - Click on text to edit', 'info');

  console.log('✅ Entered edit mode');
}

/**
 * Exit Edit Mode (without saving)
 */
async function exitEditMode() {
  if (!isEditMode) return;

  // Force save any pending changes before exiting
  if (typeof forceSave === 'function' && typeof hasPendingChanges === 'function') {
    if (hasPendingChanges()) {
      console.log('Saving pending changes before exiting edit mode...');
      await forceSave();
    }
  }

  isEditMode = false;
  document.body.dataset.mode = 'view';

  // Disable editing
  disableContentEditing();

  // Hide text toolbar
  if (typeof hideToolbar === 'function') {
    hideToolbar();
  }

  // Clear pending auto-save changes
  if (typeof clearPendingChanges === 'function') {
    clearPendingChanges();
  }

  // Remove change tracking listeners
  removeChangeTracking();

  // Update UI
  updateEditModeUI();

  // Clear original content
  originalContent = null;

  console.log('✅ Exited edit mode');
}

/**
 * Enable contentEditable on text fields
 */
function enableContentEditing() {
  // Get all slides
  const slides = document.querySelectorAll('.reveal .slides section');

  slides.forEach((slide, slideIndex) => {
    // Make title, subtitle, rich content, and text boxes editable
    const editableSelectors = [
      '.slide-title',
      '.subtitle',
      '.rich-content-area',
      '.hero-content-area',
      '.body-primary',
      '.body-secondary',
      '.textbox-content',  // Text boxes must be editable in edit mode
      // Infographic and Diagram HTML content (v7.5.3)
      '.inserted-infographic:not(.inserted-element-placeholder) .element-content',
      '.inserted-diagram:not(.inserted-element-placeholder) .element-content'
    ];

    editableSelectors.forEach(selector => {
      const elements = slide.querySelectorAll(selector);
      elements.forEach(el => {
        el.contentEditable = true;
        el.classList.add('editable');
        el.dataset.slideIndex = slideIndex;

        // Add placeholder for empty elements
        if (!el.textContent.trim()) {
          el.dataset.placeholder = 'Click to add content...';
        }
      });
    });
  });
}

/**
 * Disable contentEditable
 */
function disableContentEditing() {
  const editableElements = document.querySelectorAll('[contenteditable="true"]');

  editableElements.forEach(el => {
    el.contentEditable = false;
    el.classList.remove('editable');
    delete el.dataset.slideIndex;
    delete el.dataset.placeholder;
  });
}

/**
 * Set up change tracking for auto-save
 * Attaches input listeners to editable elements
 */
function setupChangeTracking() {
  const editableElements = document.querySelectorAll('[contenteditable="true"]');

  editableElements.forEach(el => {
    const listener = () => {
      // Get slide index from the element or its parent slide
      const slideIndex = el.dataset.slideIndex ||
        el.closest('section')?.dataset.slideIndex ||
        getCurrentSlideIndex();

      // Determine field type from element class or data attribute
      let field = 'content';
      if (el.classList.contains('slide-title')) field = 'slide_title';
      else if (el.classList.contains('subtitle')) field = 'subtitle';
      else if (el.classList.contains('rich-content-area')) field = 'rich_content';
      else if (el.classList.contains('hero-content-area')) field = 'hero_content';

      // Notify auto-save system of change
      if (typeof markContentChanged === 'function') {
        markContentChanged(parseInt(slideIndex) || 0, field);
      }
    };

    el.addEventListener('input', listener);
    inputListeners.push({ element: el, listener });
  });
}

/**
 * Remove change tracking listeners
 */
function removeChangeTracking() {
  inputListeners.forEach(({ element, listener }) => {
    element.removeEventListener('input', listener);
  });
  inputListeners = [];
}

/**
 * Get current slide index from Reveal.js
 */
function getCurrentSlideIndex() {
  if (typeof Reveal !== 'undefined' && Reveal.isReady()) {
    const indices = Reveal.getIndices();
    return indices.h || 0;
  }
  return 0;
}

/**
 * Update UI elements for edit mode
 */
function updateEditModeUI() {
  const toggleButton = document.getElementById('toggle-edit-mode');
  const editControls = document.getElementById('edit-controls');

  if (isEditMode) {
    toggleButton.innerHTML = '👁️ View Mode';
    toggleButton.classList.add('active');
    editControls.style.display = 'flex';
  } else {
    toggleButton.innerHTML = '✏️ Edit Mode';
    toggleButton.classList.remove('active');
    editControls.style.display = 'none';
  }
}

/**
 * Capture current state of all slides
 */
function captureCurrentState() {
  const slides = document.querySelectorAll('.reveal .slides section');
  const state = [];

  slides.forEach((slide, index) => {
    const slideContent = {
      index: index,
      slide_title: slide.querySelector('.slide-title')?.innerHTML || '',
      subtitle: slide.querySelector('.subtitle')?.innerHTML || '',
      rich_content: slide.querySelector('.rich-content-area')?.innerHTML || '',
      hero_content: slide.querySelector('.hero-content-area')?.innerHTML || ''
    };
    state.push(slideContent);
  });

  return state;
}

/**
 * Restore original content (for cancel)
 */
function restoreOriginalContent(state) {
  if (!state) return;

  const slides = document.querySelectorAll('.reveal .slides section');

  slides.forEach((slide, index) => {
    if (state[index]) {
      const content = state[index];

      const title = slide.querySelector('.slide-title');
      if (title && content.slide_title) title.innerHTML = content.slide_title;

      const subtitle = slide.querySelector('.subtitle');
      if (subtitle && content.subtitle) subtitle.innerHTML = content.subtitle;

      const richContent = slide.querySelector('.rich-content-area');
      if (richContent && content.rich_content) richContent.innerHTML = content.rich_content;

      const heroContent = slide.querySelector('.hero-content-area');
      if (heroContent && content.hero_content) heroContent.innerHTML = content.hero_content;
    }
  });
}

/**
 * Extract content from a single slide
 */
function extractSlideContent(slide) {
  const content = {};

  // Extract title
  const title = slide.querySelector('.slide-title');
  if (title) {
    content.slide_title = title.textContent.trim();
  }

  // Extract subtitle
  const subtitle = slide.querySelector('.subtitle');
  if (subtitle) {
    content.subtitle = subtitle.textContent.trim();
  }

  // Extract rich content (preserve HTML)
  const richContent = slide.querySelector('.rich-content-area');
  if (richContent) {
    content.rich_content = richContent.innerHTML;
  }

  // Extract hero content (preserve HTML)
  const heroContent = slide.querySelector('.hero-content-area');
  if (heroContent) {
    content.hero_content = heroContent.innerHTML;
  }

  return content;
}

/**
 * Save all changes to the server
 */
async function saveAllChanges() {
  if (!isEditMode) return;

  showNotification('💾 Saving changes...', 'info');

  try {
    const slides = document.querySelectorAll('.reveal .slides section');
    const updates = [];

    // Extract content from each slide
    slides.forEach((slide, index) => {
      const content = extractSlideContent(slide);
      updates.push({ slideIndex: index, content });
    });

    // Save each slide
    let successCount = 0;
    for (const update of updates) {
      const response = await fetch(
        `/api/presentations/${presentationId}/slides/${update.slideIndex}?created_by=user&change_summary=Manual edit via browser`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(update.content)
        }
      );

      if (response.ok) {
        successCount++;
      } else {
        const error = await response.json();
        console.error(`Failed to update slide ${update.slideIndex}:`, error);
      }
    }

    // Show success message
    if (successCount === updates.length) {
      showNotification(`✅ All changes saved! (${successCount} slides updated)`, 'success');

      // Update original content to new state
      originalContent = captureCurrentState();

      // Exit edit mode after successful save
      setTimeout(() => {
        exitEditMode();
      }, 1000);
    } else {
      showNotification(`⚠️ Partially saved: ${successCount}/${updates.length} slides updated`, 'warning');
    }

  } catch (error) {
    console.error('Error saving changes:', error);
    showNotification('❌ Error saving changes: ' + error.message, 'error');
  }
}

/**
 * Cancel all edits and restore original content
 */
function cancelEdits() {
  if (!isEditMode) return;

  // Restore original content
  if (originalContent) {
    restoreOriginalContent(originalContent);
  }

  // Exit edit mode
  exitEditMode();

  showNotification('❌ Changes discarded', 'info');
}

/**
 * Show notification to user
 */
function showNotification(message, type = 'info') {
  const notification = document.getElementById('edit-notification');
  if (!notification) return;

  // Set message and type
  notification.textContent = message;
  notification.className = `edit-notification ${type}`;

  // Show notification
  notification.classList.add('show');

  // Auto-hide after 3 seconds (except for errors)
  if (type !== 'error') {
    setTimeout(() => {
      notification.classList.remove('show');
    }, 3000);
  } else {
    // Errors stay visible until clicked
    notification.style.cursor = 'pointer';
    notification.onclick = () => {
      notification.classList.remove('show');
      notification.onclick = null;
    };
  }
}

/**
 * Show version history modal
 */
async function showVersionHistory() {
  showNotification('📜 Loading version history...', 'info');

  try {
    const response = await fetch(`/api/presentations/${presentationId}/versions`);

    if (!response.ok) {
      throw new Error('Failed to load version history');
    }

    const data = await response.json();

    if (data.versions.length === 0) {
      showNotification('ℹ️ No version history yet. Make some edits to create versions!', 'info');
      return;
    }

    // Build version history HTML
    let html = '<div class="version-history-modal">';
    html += '<div class="version-history-header">';
    html += '<h2>📜 Version History</h2>';
    html += '<button onclick="closeVersionHistory()">✕</button>';
    html += '</div>';
    html += '<div class="version-list">';

    data.versions.forEach((version, index) => {
      const date = new Date(version.created_at).toLocaleString();
      html += `
        <div class="version-item">
          <div class="version-info">
            <strong>Version ${data.versions.length - index}</strong>
            <span class="version-date">${date}</span>
            <span class="version-creator">by ${version.created_by}</span>
            <p class="version-summary">${version.change_summary || 'No description'}</p>
          </div>
          <button onclick="restoreVersionConfirm('${version.version_id}')" class="restore-btn">
            ↺ Restore
          </button>
        </div>
      `;
    });

    html += '</div></div>';

    // Show modal
    const overlay = document.createElement('div');
    overlay.id = 'version-history-overlay';
    overlay.innerHTML = html;
    document.body.appendChild(overlay);

  } catch (error) {
    console.error('Error loading version history:', error);
    showNotification('❌ Error loading version history', 'error');
  }
}

/**
 * Close version history modal
 */
function closeVersionHistory() {
  const overlay = document.getElementById('version-history-overlay');
  if (overlay) {
    overlay.remove();
  }
}

/**
 * Confirm and restore version
 */
function restoreVersionConfirm(versionId) {
  if (confirm('Restore this version? Current changes will be backed up.')) {
    restoreVersion(versionId);
  }
}

/**
 * Restore a specific version
 */
async function restoreVersion(versionId) {
  showNotification('⏳ Restoring version...', 'info');
  closeVersionHistory();

  try {
    const response = await fetch(
      `/api/presentations/${presentationId}/restore/${versionId}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ create_backup: true })
      }
    );

    if (!response.ok) {
      throw new Error('Failed to restore version');
    }

    showNotification('✅ Version restored! Reloading...', 'success');

    // Reload page after 1 second
    setTimeout(() => {
      window.location.reload();
    }, 1000);

  } catch (error) {
    console.error('Error restoring version:', error);
    showNotification('❌ Error restoring version', 'error');
  }
}

// Make functions globally available
if (typeof window !== 'undefined') {
  window.initEditMode = initEditMode;
  window.toggleEditMode = toggleEditMode;
  window.enterEditMode = enterEditMode;
  window.exitEditMode = exitEditMode;
  window.saveAllChanges = saveAllChanges;
  window.cancelEdits = cancelEdits;
  window.showVersionHistory = showVersionHistory;
  window.closeVersionHistory = closeVersionHistory;
  window.restoreVersionConfirm = restoreVersionConfirm;
  window.isInEditMode = () => isEditMode;
  window.getCurrentSlideIndex = getCurrentSlideIndex;
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initEditMode);
} else {
  initEditMode();
}
