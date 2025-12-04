/**
 * Style Builder Utility for Frontend Template Renderers
 *
 * This utility reads slot definitions from TEMPLATE_REGISTRY and generates
 * correct inline CSS styles. This ensures renderers match the template
 * definitions exactly - same positioning, sizing, fonts, and alignment.
 *
 * Usage:
 *   const style = buildSlotStyle('H1-structured', 'title');
 *   // Returns: "grid-row-start: 7; grid-row-end: 10; grid-column-start: 3; grid-column-end: 31; font-size: 72px; font-weight: bold; color: #ffffff; text-align: center; text-shadow: 0 2px 4px rgba(0,0,0,0.3)"
 */

/**
 * Build inline styles from template registry slot definition
 *
 * @param {string} templateId - The template ID (e.g., 'H1-structured', 'C1-text')
 * @param {string} slotName - The slot name (e.g., 'title', 'subtitle', 'body')
 * @param {Object} additionalStyles - Additional styles to merge (optional)
 * @returns {string} CSS inline style string
 */
function buildSlotStyle(templateId, slotName, additionalStyles = {}) {
  // Check if TEMPLATE_REGISTRY is available
  if (typeof TEMPLATE_REGISTRY === 'undefined') {
    console.warn('TEMPLATE_REGISTRY not found. Ensure template-registry.js is loaded first.');
    return '';
  }

  const template = TEMPLATE_REGISTRY[templateId];
  if (!template || !template.slots || !template.slots[slotName]) {
    console.warn(`Slot not found: ${templateId}/${slotName}`);
    return Object.entries(additionalStyles)
      .map(([k, v]) => `${k}: ${v}`)
      .join('; ');
  }

  const slot = template.slots[slotName];
  const styles = {};

  // Grid positioning - convert "7/10" format to CSS properties
  if (slot.gridRow) {
    const [start, end] = slot.gridRow.split('/');
    styles['grid-row-start'] = start.trim();
    styles['grid-row-end'] = end.trim();
  }
  if (slot.gridColumn) {
    const [start, end] = slot.gridColumn.split('/');
    styles['grid-column-start'] = start.trim();
    styles['grid-column-end'] = end.trim();
  }

  // Apply all style properties from slot definition
  if (slot.style) {
    Object.entries(slot.style).forEach(([key, value]) => {
      // Convert camelCase to kebab-case (fontSize -> font-size)
      const cssKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      styles[cssKey] = value;
    });
  }

  // Merge additional styles (these override slot styles)
  Object.entries(additionalStyles).forEach(([key, value]) => {
    // Additional styles are already in kebab-case
    styles[key] = value;
  });

  // Convert to inline style string
  return Object.entries(styles)
    .map(([k, v]) => `${k}: ${v}`)
    .join('; ');
}

/**
 * Build background style string from slide/content data
 *
 * @param {Object} slide - The slide object
 * @param {Object} content - The content object
 * @param {string} defaultColor - Default background color
 * @returns {string} CSS background style string
 */
function buildBackgroundStyle(slide = {}, content = {}, defaultColor = '#1f2937') {
  const backgroundColor = slide?.background_color || content?.background_color || defaultColor;
  const backgroundImage = slide?.background_image || content?.background_image || '';

  if (backgroundImage) {
    let style = `background-image: url('${backgroundImage}'); background-size: cover; background-position: center; background-repeat: no-repeat;`;
    if (backgroundColor) {
      style += ` background-color: ${backgroundColor};`;
    }
    return style;
  } else if (backgroundColor) {
    return `background-color: ${backgroundColor};`;
  }
  return '';
}

/**
 * Get the default background color for a template
 *
 * @param {string} templateId - The template ID
 * @returns {string} Default background color
 */
function getTemplateDefaultBackground(templateId) {
  if (typeof TEMPLATE_REGISTRY === 'undefined') {
    return '#1f2937';
  }
  const template = TEMPLATE_REGISTRY[templateId];
  return template?.defaults?.background_color || '#1f2937';
}

/**
 * Helper to generate common slot attributes
 *
 * @param {string} slotType - The slot type (title, subtitle, body, etc.)
 * @param {number} slideIndex - The slide index
 * @returns {string} HTML attributes string
 */
function buildSlotAttributes(slotType, slideIndex) {
  return `data-slot-type="${slotType}" data-section-id="slide-${slideIndex}-section-${slotType}" data-section-type="${slotType}" data-slide-index="${slideIndex}" data-editable="true"`;
}

// Export for browser
if (typeof window !== 'undefined') {
  window.buildSlotStyle = buildSlotStyle;
  window.buildBackgroundStyle = buildBackgroundStyle;
  window.getTemplateDefaultBackground = getTemplateDefaultBackground;
  window.buildSlotAttributes = buildSlotAttributes;
}
