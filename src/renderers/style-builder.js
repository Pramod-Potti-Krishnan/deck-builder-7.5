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

// ==================== THEMING SUPPORT ====================

/**
 * SLOT_STYLE_DEFAULTS - Base typography defaults by profile (standard vs hero)
 *
 * These are the foundation of the style cascade and provide consistent
 * defaults across all templates when theming is enabled.
 */
const SLOT_STYLE_DEFAULTS = {
  standard: {
    title: {
      fontSize: '42px',
      fontWeight: 'bold',
      color: 'var(--theme-text-primary)',
      lineHeight: '1.2',
      fontFamily: 'var(--theme-font-family)'
    },
    subtitle: {
      fontSize: '24px',
      fontWeight: 'normal',
      color: 'var(--theme-text-secondary)',
      lineHeight: '1.4',
      fontFamily: 'var(--theme-font-family)'
    },
    body: {
      fontSize: '20px',
      color: 'var(--theme-text-body)',
      lineHeight: '1.6',
      fontFamily: 'var(--theme-font-family)'
    },
    content: {
      fontSize: '20px',
      color: 'var(--theme-text-body)',
      lineHeight: '1.6',
      fontFamily: 'var(--theme-font-family)'
    },
    footer: {
      fontSize: '18px',
      fontWeight: '500',
      color: 'var(--theme-footer-text)',
      fontFamily: 'var(--theme-font-family)'
    }
  },
  hero: {
    title: {
      fontSize: '72px',
      fontWeight: 'bold',
      color: 'var(--theme-hero-text-primary)',
      textShadow: '0 2px 4px rgba(0,0,0,0.3)',
      lineHeight: '1.2',
      fontFamily: 'var(--theme-font-family)'
    },
    subtitle: {
      fontSize: '32px',
      fontWeight: 'normal',
      color: 'var(--theme-hero-text-secondary)',
      lineHeight: '1.4',
      fontFamily: 'var(--theme-font-family)'
    },
    footer: {
      fontSize: '18px',
      color: 'var(--theme-hero-text-secondary)',
      fontFamily: 'var(--theme-font-family)'
    }
  }
};

/**
 * Check if a template is a hero template
 *
 * @param {string} templateId - Template identifier
 * @returns {boolean} True if hero template (H1, H2, H3 series)
 */
function isHeroTemplate(templateId) {
  return /^H[123]/.test(templateId);
}

/**
 * Get the style profile for a template
 *
 * @param {string} templateId - Template identifier
 * @returns {string} 'hero' or 'standard'
 */
function getStyleProfile(templateId) {
  return isHeroTemplate(templateId) ? 'hero' : 'standard';
}

/**
 * Compute final slot style with full cascade (theming support)
 *
 * Style cascade priority (lowest to highest):
 * 1. SLOT_STYLE_DEFAULTS (profile: standard/hero)
 * 2. Theme typography settings (from THEME_REGISTRY)
 * 3. Template-specific overrides (from TEMPLATE_REGISTRY)
 * 4. Presentation color overrides (from theme_config.color_overrides)
 * 5. Inline element overrides (passed as additionalStyles)
 *
 * @param {string} templateId - The template ID (e.g., 'H1-structured', 'C1-text')
 * @param {string} slotName - The slot name (e.g., 'title', 'subtitle', 'body')
 * @param {Object} options - Theming options
 * @param {string} options.themeId - Theme identifier (default: 'corporate-blue')
 * @param {Object} options.themeOverrides - Color overrides from presentation
 * @param {Object} options.inlineOverrides - Inline style overrides
 * @returns {Object} Computed style object
 */
function getComputedSlotStyle(templateId, slotName, options = {}) {
  const {
    themeId = 'corporate-blue',
    themeOverrides = {},
    inlineOverrides = {}
  } = options;

  // 1. Determine profile (standard or hero)
  const profile = getStyleProfile(templateId);

  // 2. Base defaults from SLOT_STYLE_DEFAULTS
  const baseDefaults = SLOT_STYLE_DEFAULTS[profile]?.[slotName] || {};

  // 3. Theme-specific styles (if THEME_REGISTRY available)
  let themeSlotStyle = {};
  if (typeof THEME_REGISTRY !== 'undefined') {
    const theme = THEME_REGISTRY[themeId] || THEME_REGISTRY['corporate-blue'];
    if (theme?.typography?.[profile]?.[slotName]) {
      themeSlotStyle = { ...theme.typography[profile][slotName] };
    }
  }

  // 4. Template-specific overrides (from TEMPLATE_REGISTRY)
  let templateSlotStyle = {};
  if (typeof TEMPLATE_REGISTRY !== 'undefined') {
    const template = TEMPLATE_REGISTRY[templateId];
    if (template?.slots?.[slotName]?.style) {
      templateSlotStyle = { ...template.slots[slotName].style };
    }
  }

  // 5. Apply color overrides - convert to CSS variables where applicable
  // Theme overrides are already applied via CSS variables by ThemeManager,
  // but we can also apply inline overrides here

  // Merge in priority order
  const computedStyle = {
    ...baseDefaults,
    ...themeSlotStyle,
    ...templateSlotStyle,
    ...inlineOverrides
  };

  return computedStyle;
}

/**
 * Build themed slot style string
 *
 * Similar to buildSlotStyle but uses the full style cascade with theming.
 * Only used when theming is enabled for a template.
 *
 * @param {string} templateId - The template ID
 * @param {string} slotName - The slot name
 * @param {Object} options - Theming and style options
 * @returns {string} CSS inline style string
 */
function buildThemedSlotStyle(templateId, slotName, options = {}) {
  const { additionalStyles = {}, ...themingOptions } = options;

  // Check if TEMPLATE_REGISTRY is available
  if (typeof TEMPLATE_REGISTRY === 'undefined') {
    console.warn('TEMPLATE_REGISTRY not found. Ensure template-registry.js is loaded first.');
    return '';
  }

  const template = TEMPLATE_REGISTRY[templateId];

  // Check if theming is enabled for this template
  const themingEnabled = template?.themingEnabled === true;

  if (!themingEnabled) {
    // Fall back to standard buildSlotStyle
    return buildSlotStyle(templateId, slotName, additionalStyles);
  }

  // Get grid positioning from template
  const slot = template?.slots?.[slotName];
  const styles = {};

  if (slot) {
    // Grid positioning
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
  }

  // Get computed theme style
  const computedStyle = getComputedSlotStyle(templateId, slotName, {
    ...themingOptions,
    inlineOverrides: additionalStyles
  });

  // Apply computed styles
  Object.entries(computedStyle).forEach(([key, value]) => {
    const cssKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();
    styles[cssKey] = value;
  });

  // Convert to inline style string
  return Object.entries(styles)
    .map(([k, v]) => `${k}: ${v}`)
    .join('; ');
}

// Export for browser
if (typeof window !== 'undefined') {
  window.buildSlotStyle = buildSlotStyle;
  window.buildBackgroundStyle = buildBackgroundStyle;
  window.getTemplateDefaultBackground = getTemplateDefaultBackground;
  window.buildSlotAttributes = buildSlotAttributes;
  // Theming exports
  window.SLOT_STYLE_DEFAULTS = SLOT_STYLE_DEFAULTS;
  window.isHeroTemplate = isHeroTemplate;
  window.getStyleProfile = getStyleProfile;
  window.getComputedSlotStyle = getComputedSlotStyle;
  window.buildThemedSlotStyle = buildThemedSlotStyle;
}
