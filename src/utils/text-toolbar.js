/**
 * Text Toolbar - Rich Text Formatting for Presentation Editor
 *
 * Provides a floating toolbar for inline text formatting using
 * native browser execCommand API.
 *
 * Features:
 * - Bold, italic, underline, strikethrough
 * - Font size and family selection
 * - Text and highlight colors
 * - Text alignment
 * - Bullet and numbered lists
 * - Keyboard shortcuts (Ctrl+B, Ctrl+I, Ctrl+U)
 */

(function() {
  'use strict';

  // Toolbar element reference
  let toolbar = null;
  let isToolbarInitialized = false;

  /**
   * Initialize the text toolbar
   */
  function initTextToolbar() {
    if (isToolbarInitialized) return;

    toolbar = document.getElementById('text-toolbar');
    if (!toolbar) {
      console.warn('Text toolbar element not found');
      return;
    }

    // Set up button click handlers
    setupButtonHandlers();

    // Set up select handlers
    setupSelectHandlers();

    // Set up color picker handlers
    setupColorHandlers();

    // Set up keyboard shortcuts
    setupKeyboardShortcuts();

    // Set up selection change handler
    setupSelectionHandler();

    isToolbarInitialized = true;
    console.log('Text toolbar initialized');
  }

  /**
   * Set up click handlers for formatting buttons
   */
  function setupButtonHandlers() {
    const buttons = toolbar.querySelectorAll('button[data-command]');

    buttons.forEach(button => {
      button.addEventListener('mousedown', (e) => {
        e.preventDefault(); // Prevent losing selection
      });

      button.addEventListener('click', (e) => {
        e.preventDefault();
        const command = button.getAttribute('data-command');
        executeCommand(command);
        updateButtonStates();
        triggerAutoSave();
      });
    });
  }

  /**
   * Set up handlers for font size and family selects
   */
  function setupSelectHandlers() {
    const fontSizeSelect = document.getElementById('font-size-select');
    const fontFamilySelect = document.getElementById('font-family-select');

    if (fontSizeSelect) {
      fontSizeSelect.addEventListener('mousedown', (e) => {
        e.stopPropagation(); // Prevent toolbar from hiding
      });

      fontSizeSelect.addEventListener('change', (e) => {
        const value = e.target.value;
        if (value) {
          executeCommand('fontSize', value);
          triggerAutoSave();
        }
        e.target.value = ''; // Reset to placeholder
      });
    }

    if (fontFamilySelect) {
      fontFamilySelect.addEventListener('mousedown', (e) => {
        e.stopPropagation();
      });

      fontFamilySelect.addEventListener('change', (e) => {
        const value = e.target.value;
        if (value) {
          executeCommand('fontName', value);
          triggerAutoSave();
        }
        e.target.value = '';
      });
    }
  }

  /**
   * Set up handlers for color pickers
   */
  function setupColorHandlers() {
    const textColorInput = document.getElementById('text-color');
    const highlightColorInput = document.getElementById('highlight-color');

    if (textColorInput) {
      textColorInput.addEventListener('input', (e) => {
        executeCommand('foreColor', e.target.value);
        triggerAutoSave();
      });
    }

    if (highlightColorInput) {
      highlightColorInput.addEventListener('input', (e) => {
        executeCommand('hiliteColor', e.target.value);
        triggerAutoSave();
      });
    }
  }

  /**
   * Set up keyboard shortcuts
   */
  function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Only handle when in edit mode
      if (document.body.getAttribute('data-mode') !== 'edit') return;

      // Check for modifier key (Ctrl on Windows/Linux, Cmd on Mac)
      const isMod = e.ctrlKey || e.metaKey;

      if (isMod) {
        switch (e.key.toLowerCase()) {
          case 'b':
            e.preventDefault();
            executeCommand('bold');
            updateButtonStates();
            triggerAutoSave();
            break;
          case 'i':
            e.preventDefault();
            executeCommand('italic');
            updateButtonStates();
            triggerAutoSave();
            break;
          case 'u':
            e.preventDefault();
            executeCommand('underline');
            updateButtonStates();
            triggerAutoSave();
            break;
        }
      }
    });
  }

  /**
   * Set up selection change handler to show/hide toolbar
   */
  function setupSelectionHandler() {
    document.addEventListener('selectionchange', () => {
      // Only show when in edit mode
      if (document.body.getAttribute('data-mode') !== 'edit') {
        hideToolbar();
        return;
      }

      const selection = window.getSelection();

      if (selection.rangeCount === 0 || selection.isCollapsed) {
        hideToolbar();
        return;
      }

      // Check if selection is within an editable element
      const anchorNode = selection.anchorNode;
      const editableParent = anchorNode?.parentElement?.closest('[contenteditable="true"]');

      if (!editableParent) {
        hideToolbar();
        return;
      }

      // Show toolbar near selection
      showToolbar(selection);
      updateButtonStates();
    });

    // Hide toolbar on click outside
    document.addEventListener('mousedown', (e) => {
      if (toolbar && !toolbar.contains(e.target)) {
        // Check if clicking on an editable element
        const clickedEditable = e.target.closest('[contenteditable="true"]');
        if (!clickedEditable) {
          hideToolbar();
        }
      }
    });
  }

  /**
   * Execute a formatting command
   */
  function executeCommand(command, value = null) {
    document.execCommand(command, false, value);
  }

  /**
   * Show the toolbar near the current selection
   */
  function showToolbar(selection) {
    if (!toolbar) return;

    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();

    // Position above the selection
    const toolbarHeight = toolbar.offsetHeight || 40;
    const toolbarWidth = toolbar.offsetWidth || 400;

    let top = rect.top - toolbarHeight - 10;
    let left = rect.left + (rect.width / 2) - (toolbarWidth / 2);

    // Keep within viewport
    if (top < 10) {
      top = rect.bottom + 10; // Show below if not enough space above
    }
    if (left < 10) left = 10;
    if (left + toolbarWidth > window.innerWidth - 10) {
      left = window.innerWidth - toolbarWidth - 10;
    }

    toolbar.style.top = `${top}px`;
    toolbar.style.left = `${left}px`;
    toolbar.classList.remove('hidden');
  }

  /**
   * Hide the toolbar
   */
  function hideToolbar() {
    if (toolbar) {
      toolbar.classList.add('hidden');
    }
  }

  /**
   * Update button active states based on current formatting
   */
  function updateButtonStates() {
    if (!toolbar) return;

    const commands = ['bold', 'italic', 'underline', 'strikeThrough', 'justifyLeft', 'justifyCenter', 'justifyRight', 'insertUnorderedList', 'insertOrderedList'];

    commands.forEach(command => {
      const button = toolbar.querySelector(`button[data-command="${command}"]`);
      if (button) {
        if (document.queryCommandState(command)) {
          button.classList.add('active');
        } else {
          button.classList.remove('active');
        }
      }
    });
  }

  /**
   * Trigger auto-save after formatting change
   */
  function triggerAutoSave() {
    if (typeof markContentChanged === 'function') {
      markContentChanged();
    }
  }

  // Expose functions globally
  window.initTextToolbar = initTextToolbar;
  window.hideToolbar = hideToolbar;
  window.showToolbar = showToolbar;

  // Auto-initialize when edit mode is activated
  document.addEventListener('DOMContentLoaded', () => {
    // Toolbar will be initialized when edit mode starts
    console.log('Text toolbar module loaded');
  });

})();
