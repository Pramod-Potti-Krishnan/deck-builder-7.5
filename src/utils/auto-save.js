/**
 * Auto-Save System for Presentation Editor
 *
 * Provides debounced auto-save functionality that tracks changes
 * and saves them automatically after a period of inactivity.
 *
 * Features:
 * - Debounced save (2500ms of inactivity)
 * - Per-slide change tracking
 * - Visual status indicator (Unsaved/Saving/Saved/Error)
 * - Retry logic for failed saves
 * - Manual save trigger option
 */

(function() {
  'use strict';

  // Configuration
  const DEBOUNCE_DELAY = 2500; // 2.5 seconds of inactivity
  const RETRY_ATTEMPTS = 3;
  const RETRY_DELAY = 1000; // 1 second between retries

  // State
  let saveTimeout = null;
  let pendingChanges = new Map(); // slide index -> { fields, timestamp }
  let isSaving = false;
  let lastSaveTime = null;
  let statusIndicator = null;
  let isInitialized = false;

  // Status states
  const STATUS = {
    SAVED: 'saved',
    UNSAVED: 'unsaved',
    SAVING: 'saving',
    ERROR: 'error'
  };

  /**
   * Initialize the auto-save system
   */
  function initAutoSave() {
    if (isInitialized) return;

    statusIndicator = document.getElementById('auto-save-indicator');
    if (!statusIndicator) {
      console.warn('Auto-save indicator element not found');
    }

    // Set initial status
    updateStatus(STATUS.SAVED);

    isInitialized = true;
    console.log('Auto-save system initialized');
  }

  /**
   * Mark content as changed and schedule save
   * @param {number} slideIndex - Index of the slide that changed (optional)
   * @param {string} field - The field that changed (optional)
   */
  function markContentChanged(slideIndex = null, field = null) {
    // Only track in edit mode
    if (document.body.getAttribute('data-mode') !== 'edit') return;

    // Track the change
    if (slideIndex !== null) {
      if (!pendingChanges.has(slideIndex)) {
        pendingChanges.set(slideIndex, { fields: new Set(), timestamp: Date.now() });
      }
      if (field) {
        pendingChanges.get(slideIndex).fields.add(field);
      }
    } else {
      // Mark current slide as changed
      const currentSlideIndex = getCurrentSlideIndex();
      if (!pendingChanges.has(currentSlideIndex)) {
        pendingChanges.set(currentSlideIndex, { fields: new Set(), timestamp: Date.now() });
      }
    }

    // Update status to unsaved
    updateStatus(STATUS.UNSAVED);

    // Clear existing timeout and set new one
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }

    saveTimeout = setTimeout(() => {
      triggerSave();
    }, DEBOUNCE_DELAY);
  }

  /**
   * Get the current slide index from Reveal.js
   */
  function getCurrentSlideIndex() {
    if (typeof Reveal !== 'undefined' && Reveal.isReady()) {
      const indices = Reveal.getIndices();
      return indices.h || 0;
    }
    return 0;
  }

  /**
   * Trigger the save operation
   */
  async function triggerSave() {
    if (isSaving) {
      // Already saving, reschedule
      saveTimeout = setTimeout(() => triggerSave(), 500);
      return;
    }

    if (pendingChanges.size === 0) {
      updateStatus(STATUS.SAVED);
      return;
    }

    isSaving = true;
    updateStatus(STATUS.SAVING);

    try {
      await saveAllChanges();
      lastSaveTime = Date.now();
      pendingChanges.clear();
      updateStatus(STATUS.SAVED);
    } catch (error) {
      console.error('Auto-save failed:', error);
      updateStatus(STATUS.ERROR, error.message);
    } finally {
      isSaving = false;
    }
  }

  /**
   * Save all pending changes to the server
   */
  async function saveAllChanges() {
    const presentationId = getPresentationId();
    if (!presentationId) {
      throw new Error('No presentation ID found');
    }

    // Collect all slide content
    const slides = document.querySelectorAll('.reveal .slides > section');
    const slideUpdates = [];

    slides.forEach((slide, index) => {
      const update = collectSlideContent(slide, index);
      if (update) {
        slideUpdates.push(update);
      }
    });

    // Make batch update API call with retry
    let lastError = null;
    for (let attempt = 0; attempt < RETRY_ATTEMPTS; attempt++) {
      try {
        const response = await fetch(`/api/presentations/${presentationId}/slides`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            slides: slideUpdates,
            updated_by: 'user',
            change_summary: 'Auto-save from editor'
          })
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `HTTP ${response.status}`);
        }

        console.log('Auto-save successful');
        return; // Success!
      } catch (error) {
        lastError = error;
        console.warn(`Save attempt ${attempt + 1} failed:`, error);
        if (attempt < RETRY_ATTEMPTS - 1) {
          await sleep(RETRY_DELAY);
        }
      }
    }

    throw lastError;
  }

  /**
   * Collect content from a slide element
   */
  function collectSlideContent(slideElement, index) {
    const update = {};

    // Get layout type
    const layout = slideElement.getAttribute('data-layout') || 'L25';

    // Collect content based on layout
    if (layout === 'L29') {
      // Hero layout - full content
      const heroContent = slideElement.querySelector('.hero-content, [data-section="hero"]');
      if (heroContent) {
        update.hero_content = heroContent.innerHTML;
      }
    } else {
      // Standard layouts with title, subtitle, content
      const titleEl = slideElement.querySelector('.slide-title, [data-section="title"]');
      const subtitleEl = slideElement.querySelector('.slide-subtitle, [data-section="subtitle"]');
      const contentEl = slideElement.querySelector('.rich-content, [data-section="content"], [data-section="body"]');

      if (titleEl) {
        update.slide_title = titleEl.textContent.trim();
      }
      if (subtitleEl) {
        update.subtitle = subtitleEl.textContent.trim();
      }
      if (contentEl) {
        update.rich_content = contentEl.innerHTML;
      }

      // Handle additional layout-specific elements
      for (let i = 1; i <= 5; i++) {
        const el = slideElement.querySelector(`[data-section="element-${i}"]`);
        if (el) {
          update[`element_${i}`] = el.innerHTML;
        }
      }
    }

    // Collect background if present
    const bgColor = slideElement.getAttribute('data-background-color');
    const bgImage = slideElement.getAttribute('data-background-image');
    if (bgColor) update.background_color = bgColor;
    if (bgImage) update.background_image = bgImage;

    // Collect text boxes from this slide
    const textBoxes = collectTextBoxes(slideElement, index);
    if (textBoxes.length > 0) {
      update.text_boxes = textBoxes;
    }

    return update;
  }

  /**
   * Collect text boxes from a slide
   */
  function collectTextBoxes(slideElement, slideIndex) {
    const textBoxes = [];

    // Find all text box elements in this slide
    const textBoxElements = slideElement.querySelectorAll('.inserted-textbox');

    textBoxElements.forEach(el => {
      const textBox = {
        id: el.id,
        position: {
          grid_row: el.style.gridRow || '5/10',
          grid_column: el.style.gridColumn || '3/15'
        },
        z_index: parseInt(el.style.zIndex) || 1000,
        content: '',
        style: {},
        locked: el.classList.contains('textbox-locked'),
        visible: !el.classList.contains('textbox-hidden')
      };

      // Get content from contentEditable area
      const contentEl = el.querySelector('.textbox-content');
      if (contentEl) {
        textBox.content = contentEl.innerHTML;
      }

      // Extract container styles (background, border, etc.)
      textBox.style = {
        background_color: el.style.backgroundColor || 'transparent',
        border_color: el.style.borderColor || 'transparent',
        border_width: parseInt(el.style.borderWidth) || 0,
        border_radius: parseInt(el.style.borderRadius) || 0,
        padding: parseInt(el.style.padding) || 16,
        opacity: parseFloat(el.style.opacity) || 1.0,
        box_shadow: el.style.boxShadow || null
      };

      // Extract text formatting styles from content element
      // These are set by postMessage commands (setTextBoxColor, setTextBoxFont, etc.)
      if (contentEl) {
        textBox.text_style = {
          color: contentEl.style.color || null,
          font_family: contentEl.style.fontFamily || null,
          font_size: contentEl.style.fontSize || null,
          font_weight: contentEl.style.fontWeight || null,
          font_style: contentEl.style.fontStyle || null,
          text_align: contentEl.style.textAlign || null,
          line_height: contentEl.style.lineHeight || null,
          letter_spacing: contentEl.style.letterSpacing || null,
          text_decoration: contentEl.style.textDecoration || null
        };
        // Remove null values to keep payload clean
        Object.keys(textBox.text_style).forEach(key => {
          if (!textBox.text_style[key]) delete textBox.text_style[key];
        });
        // Only include text_style if it has values
        if (Object.keys(textBox.text_style).length === 0) {
          delete textBox.text_style;
        }
      }

      textBoxes.push(textBox);
    });

    return textBoxes;
  }

  /**
   * Get presentation ID from URL or data attribute
   */
  function getPresentationId() {
    // Try URL first (matches /p/{presentation_id} pattern)
    const urlMatch = window.location.pathname.match(/\/p\/([^\/]+)/);
    if (urlMatch) {
      return urlMatch[1];
    }

    // Try data attribute
    const container = document.querySelector('[data-presentation-id]');
    if (container) {
      return container.getAttribute('data-presentation-id');
    }

    // Try global variable
    if (typeof window.presentationId !== 'undefined') {
      return window.presentationId;
    }

    return null;
  }

  /**
   * Update the status indicator
   */
  function updateStatus(status, message = null) {
    if (!statusIndicator) return;

    // Remove all status classes
    statusIndicator.classList.remove('status-saved', 'status-unsaved', 'status-saving', 'status-error');

    // Add new status class
    statusIndicator.classList.add(`status-${status}`);

    // Update text content
    const textEl = statusIndicator.querySelector('.status-text');
    if (textEl) {
      switch (status) {
        case STATUS.SAVED:
          textEl.textContent = lastSaveTime
            ? `Saved ${formatTimeAgo(lastSaveTime)}`
            : 'All changes saved';
          break;
        case STATUS.UNSAVED:
          textEl.textContent = 'Unsaved changes';
          break;
        case STATUS.SAVING:
          textEl.textContent = 'Saving...';
          break;
        case STATUS.ERROR:
          textEl.textContent = message || 'Save failed';
          break;
      }
    }

    // Show/hide indicator based on edit mode
    const isEditMode = document.body.getAttribute('data-mode') === 'edit';
    statusIndicator.style.display = isEditMode ? 'flex' : 'none';
  }

  /**
   * Format time ago string
   */
  function formatTimeAgo(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);

    if (seconds < 5) return 'just now';
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    return `${Math.floor(seconds / 3600)}h ago`;
  }

  /**
   * Sleep helper
   */
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Force an immediate save
   */
  function forceSave() {
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
    return triggerSave();
  }

  /**
   * Check if there are pending changes
   */
  function hasPendingChanges() {
    return pendingChanges.size > 0;
  }

  /**
   * Get pending changes info
   */
  function getPendingChangesInfo() {
    return {
      hasPending: pendingChanges.size > 0,
      slideCount: pendingChanges.size,
      slides: Array.from(pendingChanges.keys()),
      lastSaveTime: lastSaveTime
    };
  }

  /**
   * Clear all pending changes (e.g., after page reload)
   */
  function clearPendingChanges() {
    pendingChanges.clear();
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
    updateStatus(STATUS.SAVED);
  }

  // Expose functions globally
  window.initAutoSave = initAutoSave;
  window.markContentChanged = markContentChanged;
  window.forceSave = forceSave;
  window.hasPendingChanges = hasPendingChanges;
  window.getPendingChangesInfo = getPendingChangesInfo;
  window.clearPendingChanges = clearPendingChanges;

  // Handle beforeunload to warn about unsaved changes
  window.addEventListener('beforeunload', (e) => {
    if (hasPendingChanges()) {
      e.preventDefault();
      e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
      return e.returnValue;
    }
  });

  // Auto-initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    console.log('Auto-save module loaded');
  });

})();
