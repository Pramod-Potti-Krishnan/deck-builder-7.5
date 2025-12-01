/**
 * Format API for Layout Builder v7.5
 *
 * Provides programmatic text formatting via postMessage API.
 * Uses document.execCommand() for formatting operations.
 *
 * Exposed via window.FormatAPI for postMessage handler access.
 */

(function() {
  'use strict';

  // ===== FORMAT TEXT API =====

  /**
   * Apply text formatting to selection or section
   *
   * @param {Object} options - Formatting options
   * @param {string} [options.sectionId] - Target section by data-section-id
   * @param {boolean|'toggle'} [options.bold] - Bold formatting
   * @param {boolean|'toggle'} [options.italic] - Italic formatting
   * @param {boolean|'toggle'} [options.underline] - Underline formatting
   * @param {boolean|'toggle'} [options.strikethrough] - Strikethrough formatting
   * @param {string} [options.fontSize] - Font size (execCommand size 1-7 or CSS px)
   * @param {string} [options.fontFamily] - Font family
   * @param {string} [options.color] - Text color (hex)
   * @param {string} [options.backgroundColor] - Highlight color (hex)
   * @param {string} [options.alignment] - Text alignment: left|center|right|justify
   * @param {string} [options.listType] - List type: bullet|numbered|none
   * @returns {Object} Result with success and applied commands
   */
  function formatText(options = {}) {
    // Validate we're in edit mode
    if (document.body.getAttribute('data-mode') !== 'edit') {
      return {
        success: false,
        error: 'Not in edit mode. Enter edit mode first.'
      };
    }

    // If targeting a specific section, select its content
    if (options.sectionId) {
      const section = document.querySelector(`[data-section-id="${options.sectionId}"]`);
      if (!section) {
        return {
          success: false,
          error: `Section not found: ${options.sectionId}`
        };
      }

      // Check if section is editable
      if (!section.isContentEditable) {
        return {
          success: false,
          error: 'Section is not editable. Enter edit mode first.'
        };
      }

      // If applyToAll or no existing selection in this section, select all content
      if (options.applyToAll) {
        const range = document.createRange();
        range.selectNodeContents(section);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
      }
    }

    // Check for valid selection
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) {
      // If no selection and no sectionId, can't format
      if (!options.sectionId) {
        return {
          success: false,
          error: 'No text selected. Select text or provide sectionId with applyToAll.'
        };
      }
    }

    const applied = [];
    const errors = [];

    // Apply formatting commands
    try {
      // Bold
      if (options.bold !== undefined) {
        applyToggleCommand('bold', options.bold);
        applied.push('bold');
      }

      // Italic
      if (options.italic !== undefined) {
        applyToggleCommand('italic', options.italic);
        applied.push('italic');
      }

      // Underline
      if (options.underline !== undefined) {
        applyToggleCommand('underline', options.underline);
        applied.push('underline');
      }

      // Strikethrough
      if (options.strikethrough !== undefined) {
        applyToggleCommand('strikeThrough', options.strikethrough);
        applied.push('strikethrough');
      }

      // Font Size
      if (options.fontSize) {
        // execCommand fontSize accepts 1-7
        let size = options.fontSize;
        if (typeof size === 'string' && size.endsWith('px')) {
          size = pxToExecCommandSize(parseInt(size));
        }
        document.execCommand('fontSize', false, size);
        applied.push('fontSize');
      }

      // Font Family
      if (options.fontFamily) {
        document.execCommand('fontName', false, options.fontFamily);
        applied.push('fontFamily');
      }

      // Text Color
      if (options.color) {
        document.execCommand('foreColor', false, options.color);
        applied.push('color');
      }

      // Background/Highlight Color
      if (options.backgroundColor) {
        document.execCommand('hiliteColor', false, options.backgroundColor);
        applied.push('backgroundColor');
      }

      // Alignment
      if (options.alignment) {
        const alignCommands = {
          left: 'justifyLeft',
          center: 'justifyCenter',
          right: 'justifyRight',
          justify: 'justifyFull'
        };
        const cmd = alignCommands[options.alignment];
        if (cmd) {
          document.execCommand(cmd, false, null);
          applied.push('alignment');
        }
      }

      // List Type
      if (options.listType) {
        if (options.listType === 'bullet') {
          document.execCommand('insertUnorderedList', false, null);
          applied.push('bulletList');
        } else if (options.listType === 'numbered') {
          document.execCommand('insertOrderedList', false, null);
          applied.push('numberedList');
        } else if (options.listType === 'none') {
          // Remove list by toggling if currently in a list
          if (document.queryCommandState('insertUnorderedList')) {
            document.execCommand('insertUnorderedList', false, null);
            applied.push('removeBulletList');
          }
          if (document.queryCommandState('insertOrderedList')) {
            document.execCommand('insertOrderedList', false, null);
            applied.push('removeNumberedList');
          }
        }
      }

      // Trigger auto-save
      if (applied.length > 0 && typeof markContentChanged === 'function') {
        const slideIndex = getSlideIndexFromSelection();
        markContentChanged(slideIndex, 'content');
      }

      return {
        success: true,
        applied: applied,
        errors: errors.length > 0 ? errors : undefined
      };

    } catch (error) {
      return {
        success: false,
        error: `Formatting failed: ${error.message}`,
        applied: applied
      };
    }
  }

  /**
   * Apply a toggle command (bold, italic, underline, strikethrough)
   *
   * @param {string} command - execCommand name
   * @param {boolean|'toggle'} value - true, false, or 'toggle'
   */
  function applyToggleCommand(command, value) {
    if (value === 'toggle') {
      document.execCommand(command, false, null);
    } else if (value === true && !document.queryCommandState(command)) {
      document.execCommand(command, false, null);
    } else if (value === false && document.queryCommandState(command)) {
      document.execCommand(command, false, null);
    }
  }

  /**
   * Convert pixel font size to execCommand size (1-7)
   *
   * @param {number} px - Font size in pixels
   * @returns {string} execCommand size (1-7)
   */
  function pxToExecCommandSize(px) {
    // Approximate mapping: 10px=1, 13px=2, 16px=3, 18px=4, 24px=5, 32px=6, 48px=7
    if (px <= 10) return '1';
    if (px <= 13) return '2';
    if (px <= 16) return '3';
    if (px <= 18) return '4';
    if (px <= 24) return '5';
    if (px <= 32) return '6';
    return '7';
  }

  /**
   * Get slide index from current selection
   *
   * @returns {number} Slide index (0-based)
   */
  function getSlideIndexFromSelection() {
    const selection = window.getSelection();
    if (!selection || !selection.focusNode) {
      return getCurrentSlideIndexFallback();
    }

    const node = selection.focusNode.nodeType === Node.TEXT_NODE
      ? selection.focusNode.parentElement
      : selection.focusNode;

    const section = node.closest('[data-slide-index]');
    if (section) {
      return parseInt(section.dataset.slideIndex) || 0;
    }

    return getCurrentSlideIndexFallback();
  }

  /**
   * Fallback to get current slide index from Reveal.js
   *
   * @returns {number} Slide index
   */
  function getCurrentSlideIndexFallback() {
    if (typeof Reveal !== 'undefined' && Reveal.isReady()) {
      const indices = Reveal.getIndices();
      return indices.h || 0;
    }
    return 0;
  }

  // ===== GET FORMAT STATE API =====

  /**
   * Get current formatting state at selection
   *
   * @returns {Object} Current formatting state
   */
  function getFormatState() {
    return {
      bold: document.queryCommandState('bold'),
      italic: document.queryCommandState('italic'),
      underline: document.queryCommandState('underline'),
      strikethrough: document.queryCommandState('strikeThrough'),
      fontSize: document.queryCommandValue('fontSize'),
      fontFamily: document.queryCommandValue('fontName'),
      color: document.queryCommandValue('foreColor'),
      backgroundColor: document.queryCommandValue('hiliteColor'),
      alignment: {
        left: document.queryCommandState('justifyLeft'),
        center: document.queryCommandState('justifyCenter'),
        right: document.queryCommandState('justifyRight'),
        justify: document.queryCommandState('justifyFull')
      },
      bulletList: document.queryCommandState('insertUnorderedList'),
      numberedList: document.queryCommandState('insertOrderedList')
    };
  }

  // ===== FORMAT SECTION API =====

  /**
   * Apply formatting to an entire section
   *
   * @param {string} sectionId - data-section-id value
   * @param {Object} options - Formatting options (same as formatText)
   * @returns {Object} Result
   */
  function formatSection(sectionId, options = {}) {
    return formatText({
      ...options,
      sectionId: sectionId,
      applyToAll: true
    });
  }

  // ===== REMOVE FORMATTING API =====

  /**
   * Remove all formatting from selection or section
   *
   * @param {string} [sectionId] - Optional section to clear
   * @returns {Object} Result
   */
  function removeFormatting(sectionId) {
    if (sectionId) {
      const section = document.querySelector(`[data-section-id="${sectionId}"]`);
      if (!section) {
        return { success: false, error: `Section not found: ${sectionId}` };
      }

      const range = document.createRange();
      range.selectNodeContents(section);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }

    try {
      document.execCommand('removeFormat', false, null);

      if (typeof markContentChanged === 'function') {
        markContentChanged();
      }

      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ===== EXPOSE API =====

  window.FormatAPI = {
    formatText: formatText,
    getFormatState: getFormatState,
    formatSection: formatSection,
    removeFormatting: removeFormatting
  };

  console.log('FormatAPI initialized');

})();
