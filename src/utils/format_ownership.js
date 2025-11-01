/**
 * Format Ownership Utility
 *
 * Handles format ownership detection and proper rendering based on
 * whether content is owned by "layout_builder" or "text_service".
 *
 * Rules:
 * - layout_builder: Receives plain text, applies HTML formatting
 * - text_service: Receives HTML, renders as-is (NO modifications)
 */

/**
 * Detect format owner from content object
 * @param {Object} content - Slide content object
 * @param {string} fieldName - Name of the field being rendered
 * @returns {string} - "layout_builder" or "text_service"
 */
function detectFormatOwner(content, fieldName) {
  // Check if content has explicit format_owner field
  if (content.format_owner) {
    return content.format_owner;
  }

  // Default ownership rules based on field type
  const layoutOwned = [
    'slide_title',
    'subtitle',
    'main_title',
    'section_title',
    'closing_message',
    'presenter_name',
    'organization',
    'date',
    'contact_email',
    'website',
    'social_media',
    'footer',
    'label',
    'header',
    'column_header',
    'quadrant_header',
    'caption',
    'attribution'
  ];

  const textServiceOwned = [
    'main_text_content',
    'text_content',
    'bullets',
    'numbered_items',
    'quote_text',
    'summary',
    'key_insights',
    'explanation_text',
    'supporting_text'
  ];

  if (layoutOwned.includes(fieldName)) {
    return 'layout_builder';
  }

  if (textServiceOwned.includes(fieldName)) {
    return 'text_service';
  }

  // Default to layout_builder for unknown fields
  return 'layout_builder';
}

/**
 * Render content based on format ownership
 * @param {string|Array} content - Content to render
 * @param {Object} contentObj - Full content object
 * @param {string} fieldName - Name of the field
 * @returns {string} - HTML string
 */
function renderWithOwnership(content, contentObj, fieldName) {
  const owner = detectFormatOwner(contentObj, fieldName);

  if (owner === 'text_service') {
    // Text service owns formatting - render HTML as-is
    if (Array.isArray(content)) {
      // If it's an array (like bullets), text service should have sent HTML
      // Check if first item looks like HTML
      if (content[0] && content[0].includes('<')) {
        // Already has HTML tags, render as-is
        return content.join('');
      } else {
        // Plain text array - text service didn't format, we add minimal structure
        return `<ul>${content.map(item => `<li>${item}</li>`).join('')}</ul>`;
      }
    }

    // For strings, render as-is (may contain HTML)
    return content || '';
  } else {
    // Layout builder owns formatting - apply HTML to plain text
    if (Array.isArray(content)) {
      // Create proper bullet list structure
      return `<ul>${content.map(item => `<li>${item}</li>`).join('')}</ul>`;
    }

    // For strings, escape any HTML and treat as plain text
    // (though in practice, layout_builder fields should be plain text)
    return content || '';
  }
}

/**
 * Check if content field is owned by text service
 * @param {Object} content - Slide content object
 * @param {string} fieldName - Name of the field
 * @returns {boolean}
 */
function isTextServiceOwned(content, fieldName) {
  return detectFormatOwner(content, fieldName) === 'text_service';
}

/**
 * Check if content field is owned by layout builder
 * @param {Object} content - Slide content object
 * @param {string} fieldName - Name of the field
 * @returns {boolean}
 */
function isLayoutBuilderOwned(content, fieldName) {
  return detectFormatOwner(content, fieldName) === 'layout_builder';
}

// Export for use in renderers
if (typeof window !== 'undefined') {
  window.FormatOwnership = {
    detectFormatOwner,
    renderWithOwnership,
    isTextServiceOwned,
    isLayoutBuilderOwned
  };
}
