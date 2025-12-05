/**
 * Slot Converter - Converts H1-structured template slots to Element Type instances
 *
 * This module provides the post-render conversion layer that transforms
 * static slot-based HTML elements into fully interactive Element Type instances
 * with drag handles, resize handles, and format panel support.
 *
 * Usage:
 *   convertHeroSlotsToElements(slideElement, slideIndex, 'H1-structured');
 *
 * Conversion is triggered after initial HTML rendering in presentation-viewer.html
 */

(function() {
  'use strict';

  // ===== CONFIGURATION =====

  /**
   * Feature flag to enable/disable slot conversion
   * Set to false to revert to static slot behavior
   */
  const ENABLE_SLOT_CONVERSION = true;

  /**
   * Mapping from slot tags to Element Types
   */
  const SLOT_TO_ELEMENT_MAP = {
    // Text-based slots -> TextBox Element Type
    'title': 'textbox',
    'subtitle': 'textbox',
    'footer': 'textbox',
    'section_number': 'textbox',
    'contact_info': 'textbox',
    'body': 'textbox',      // C1-text body content -> textbox

    // Visual content slots -> Their own Element Types
    // Each visual type has a dedicated insert function in element-manager.js
    'table': 'table',           // C2-table -> insertTable
    'chart': 'chart',           // C3-chart -> insertChart
    'infographic': 'infographic', // C4-infographic -> insertInfographic
    'diagram': 'diagram',       // C5-diagram -> insertDiagram
    'image': 'image',           // C6-image -> insertImage

    // Image-based slots -> Image Element Type
    'logo': 'image',
    'background': 'image',

    // Split template slots (S1-S4)
    'visual': 'image',          // S1/S3 visual areas -> image placeholder
    'header': 'textbox',        // S4 column headers
    'caption_left': 'textbox',  // S3 left caption
    'caption_right': 'textbox', // S3 right caption
    'header_left': 'textbox',   // S4 left header
    'header_right': 'textbox',  // S4 right header
    'content_left': 'textbox',  // S1/S3/S4 left content (body)
    'content_right': 'textbox', // S1/S3/S4 right content (body)

    // Blank template slot (B1)
    'canvas': 'textbox'         // B1 canvas -> textbox for freeform content
  };

  /**
   * Z-index assignments for slot types
   * Background is lowest, content elements above
   */
  const SLOT_Z_INDEX = {
    'background': 1,
    'title': 1010,
    'subtitle': 1011,
    'footer': 1012,
    'logo': 1013,
    'section_number': 1014,
    'contact_info': 1015,
    'body': 1016,
    // Visual content areas (same z-index as body)
    'table': 1016,
    'chart': 1016,
    'infographic': 1016,
    'diagram': 1016,
    'image': 1016,
    // Split template slots
    'visual': 1016,
    'header': 1014,
    'header_left': 1014,
    'header_right': 1014,
    'content_left': 1016,
    'content_right': 1016,
    'caption_left': 1017,
    'caption_right': 1017,
    // Blank template
    'canvas': 1016
  };

  /**
   * CSS class to DOM selector mapping for finding slot elements
   */
  const SLOT_CLASS_SELECTORS = {
    // ===== HERO TEMPLATES =====
    'H1-structured': {
      'title': '.title-hero',
      'subtitle': '.subtitle-hero',
      'footer': '.footer-hero',
      'logo': '.logo-hero',
      'background': '.background-hero'
    },
    'H2-section': {
      'section_number': '.section-number-hero',
      'title': '.title-hero',
      'background': '.background-hero'
    },
    'H3-closing': {
      'title': '.title-hero',
      'subtitle': '.subtitle-hero',
      'contact_info': '.contact-hero',
      'logo': '.logo-hero',
      'background': '.background-hero'
    },
    // ===== CONTENT TEMPLATES (C1-C6) =====
    // All use 'content' slot key from TEMPLATE_REGISTRY
    // Element type is determined by slotDef.tag (body, table, chart, infographic, diagram, image)
    'C1-text': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'C2-table': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'C3-chart': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'C4-infographic': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'C5-diagram': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'C6-image': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    // ===== SPLIT TEMPLATES (S1-S4) =====
    'S1-visual-text': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content_left': '.content-left',
      'content_right': '.content-right',
      'footer': '.footer',
      'logo': '.logo'
    },
    'S2-image-content': {
      'image': '.image-area',
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content': '.content-area',
      'footer': '.footer',
      'logo': '.logo'
    },
    'S3-two-visuals': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'content_left': '.content-left',
      'content_right': '.content-right',
      'caption_left': '.caption-left',
      'caption_right': '.caption-right',
      'footer': '.footer',
      'logo': '.logo'
    },
    'S4-comparison': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'header_left': '.header-left',
      'header_right': '.header-right',
      'content_left': '.content-left',
      'content_right': '.content-right',
      'footer': '.footer',
      'logo': '.logo'
    },
    // ===== BLANK TEMPLATE (B1) =====
    'B1-blank': {
      'title': '.slide-title',
      'subtitle': '.subtitle',
      'canvas': '.canvas',
      'footer': '.footer',
      'logo': '.logo'
    }
  };

  // ===== MAIN CONVERSION FUNCTIONS =====

  /**
   * Convert all slots in a Hero template slide to Element Type instances
   *
   * @param {HTMLElement} slideElement - The slide section element
   * @param {number} slideIndex - Slide index (0-based)
   * @param {string} templateId - Template ID (e.g., 'H1-structured')
   */
  function convertHeroSlotsToElements(slideElement, slideIndex, templateId) {
    if (!ENABLE_SLOT_CONVERSION) {
      console.log('[SlotConverter] Conversion disabled by feature flag');
      return;
    }

    if (!slideElement) {
      console.warn('[SlotConverter] No slide element provided');
      return;
    }

    // Check if TEMPLATE_REGISTRY is available
    if (typeof TEMPLATE_REGISTRY === 'undefined') {
      console.warn('[SlotConverter] TEMPLATE_REGISTRY not found');
      return;
    }

    const template = TEMPLATE_REGISTRY[templateId];
    if (!template || !template.slots) {
      console.warn(`[SlotConverter] Template ${templateId} not found or has no slots`);
      return;
    }

    // Check if ElementManager is available
    if (typeof window.ElementManager === 'undefined') {
      console.warn('[SlotConverter] ElementManager not available');
      return;
    }

    console.log(`[SlotConverter] Converting slots for ${templateId} on slide ${slideIndex}`);

    const selectors = SLOT_CLASS_SELECTORS[templateId] || {};

    // Convert each slot defined in the template
    Object.entries(template.slots).forEach(([slotName, slotDef]) => {
      const selector = selectors[slotName];
      if (!selector) {
        console.log(`[SlotConverter] No selector defined for slot: ${slotName}`);
        return;
      }

      const slotElement = slideElement.querySelector(selector);
      if (!slotElement) {
        console.log(`[SlotConverter] Slot element not found: ${selector}`);
        return;
      }

      // Skip if already converted
      if (slotElement.classList.contains('converted')) {
        console.log(`[SlotConverter] Slot ${slotName} already converted`);
        return;
      }

      // Check for existing converted element (restoration scenario)
      // Instead of skipping, UPDATE the element to match template positions
      const existingId = `slide-${slideIndex}-slot-${slotName}-element`;
      const existingElement = document.getElementById(existingId);
      if (existingElement) {
        console.log(`[SlotConverter] Updating restored element ${existingId} to match template`);
        // UPDATE position to match template (restored elements may have saved positions)
        existingElement.style.gridRow = slotDef.gridRow;
        existingElement.style.gridColumn = slotDef.gridColumn;
        // REMOVE original slot from DOM (not just hide)
        slotElement.remove();
        existingElement.classList.add('converted-slot', `slot-${slotName}`);
        existingElement.dataset.originalSlot = slotName;
        // Apply slot-specific styling for background
        if (slotName === 'background') {
          existingElement.classList.add('slot-background');
          existingElement.style.zIndex = '1';
          existingElement.style.borderRadius = '0';
        }
        // Apply slot-specific styling for logo
        if (slotName === 'logo') {
          existingElement.classList.add('slot-logo');
        }
        return;
      }

      // Determine element type and convert
      const elementType = getElementTypeForSlot(slotName, slotDef);
      convertSlotToElement(slotElement, slotDef, slotName, elementType, slideIndex);
    });
  }

  /**
   * Determine the Element Type for a given slot
   *
   * @param {string} slotName - Name of the slot (e.g., 'title')
   * @param {Object} slotDef - Slot definition from TEMPLATE_REGISTRY
   * @returns {string} Element type: 'textbox', 'image', 'chart', 'infographic', 'diagram', 'table'
   */
  function getElementTypeForSlot(slotName, slotDef) {
    // First check explicit mapping
    if (SLOT_TO_ELEMENT_MAP[slotName]) {
      return SLOT_TO_ELEMENT_MAP[slotName];
    }

    // Then check slot tag
    if (slotDef.tag && SLOT_TO_ELEMENT_MAP[slotDef.tag]) {
      return SLOT_TO_ELEMENT_MAP[slotDef.tag];
    }

    // Check accepts array for hints
    if (slotDef.accepts) {
      if (slotDef.accepts.includes('image') || slotDef.accepts.includes('color')) {
        return 'image';
      }
    }

    // Default to textbox
    return 'textbox';
  }

  /**
   * Convert a single slot element to an Element Type instance
   *
   * @param {HTMLElement} slotElement - The original slot DOM element
   * @param {Object} slotDef - Slot definition from TEMPLATE_REGISTRY
   * @param {string} slotName - Name of the slot
   * @param {string} elementType - Target element type
   * @param {number} slideIndex - Slide index
   */
  function convertSlotToElement(slotElement, slotDef, slotName, elementType, slideIndex) {
    console.log(`[SlotConverter] Converting slot '${slotName}' to ${elementType}`);

    switch (elementType) {
      case 'textbox':
        convertToTextBox(slotElement, slotDef, slotName, slideIndex);
        break;
      case 'image':
        convertToImage(slotElement, slotDef, slotName, slideIndex);
        break;
      case 'chart':
        convertToChart(slotElement, slotDef, slotName, slideIndex);
        break;
      case 'infographic':
        convertToInfographic(slotElement, slotDef, slotName, slideIndex);
        break;
      case 'diagram':
        convertToDiagram(slotElement, slotDef, slotName, slideIndex);
        break;
      case 'table':
        convertToTable(slotElement, slotDef, slotName, slideIndex);
        break;
      default:
        console.warn(`[SlotConverter] Unknown element type: ${elementType}`);
    }
  }

  // ===== TEXT BOX CONVERSION =====

  /**
   * Convert a slot element to a TextBox Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToTextBox(slotElement, slotDef, slotName, slideIndex) {
    // Extract current content - trim and use defaultText as fallback
    const rawContent = slotElement.innerHTML?.trim();
    const content = rawContent || slotDef.defaultText || '';

    // Extract styles from slot definition and computed styles
    const computedStyle = window.getComputedStyle(slotElement);
    const config = buildTextBoxConfigFromSlot(slotElement, slotDef, slotName, slideIndex, computedStyle);
    config.content = content;

    // Insert the TextBox element
    const result = window.ElementManager.insertTextBox(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created TextBox ${result.elementId} for slot '${slotName}'`);

      // REMOVE original slot element from DOM (not just hide)
      // This prevents ghost elements appearing when converted element is deleted
      slotElement.remove();

      // Add class to identify this as a converted slot element
      const newElement = document.getElementById(result.elementId);
      if (newElement) {
        newElement.classList.add('converted-slot', `slot-${slotName}`);
        newElement.dataset.originalSlot = slotName;

        // FORCE template-defined grid position (in case defaults were used)
        newElement.style.gridRow = slotDef.gridRow;
        newElement.style.gridColumn = slotDef.gridColumn;

        // FORCE flexbox alignment from template definition
        const slotStyle = slotDef.style || {};
        newElement.style.display = 'flex';
        newElement.style.flexDirection = 'column';
        newElement.style.justifyContent = slotStyle.justifyContent || 'flex-start';
        newElement.style.alignItems = slotStyle.alignItems || 'flex-start';

        // CRITICAL: Remove min-height from textbox-content so flexbox alignment works
        // The inline style min-height: 100% prevents justify-content from positioning content
        const contentDiv = newElement.querySelector('.textbox-content');
        if (contentDiv) {
          contentDiv.style.minHeight = 'auto';
          contentDiv.style.height = 'auto';

          // Force apply color and text-transform from template definition (belt and suspenders)
          if (slotStyle.color) {
            contentDiv.style.color = slotStyle.color;
          }
          if (slotStyle.textTransform) {
            contentDiv.style.textTransform = slotStyle.textTransform;
          }
        }
      }
    } else {
      console.error(`[SlotConverter] Failed to create TextBox for slot '${slotName}':`, result.error);
    }
  }

  /**
   * Build TextBox configuration from slot element and definition
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   * @param {CSSStyleDeclaration} computedStyle - Computed styles
   * @returns {Object} TextBox configuration object
   */
  function buildTextBoxConfigFromSlot(slotElement, slotDef, slotName, slideIndex, computedStyle) {
    // Build position from slot definition
    const position = {
      gridRow: slotDef.gridRow || '1/19',
      gridColumn: slotDef.gridColumn || '1/33'
    };

    // Build text style from slot definition with fallback to computed styles
    const slotStyle = slotDef.style || {};

    // Slot-specific default colors (for dark background visibility on hero slides)
    const slotColors = {
      'title': '#ffffff',         // White for title (prominent)
      'subtitle': '#94a3b8',      // Slate for subtitle (muted)
      'footer': '#ffffff',        // White for footer
      'section_number': '#ffffff', // White for section number (H2-section)
      'contact_info': '#ffffff'   // White for contact info (H3-closing)
    };

    // NOTE: Color priority is slotStyle.color > slotColors[slotName] > fallback
    // We intentionally skip computedStyle.color because the rendered slot element
    // may have inherited dark text color from parent CSS which overrides template settings
    const textStyle = {
      color: slotStyle.color || slotColors[slotName] || '#ffffff',
      font_family: slotStyle.fontFamily || computedStyle.fontFamily || 'Poppins, sans-serif',
      font_size: slotStyle.fontSize || computedStyle.fontSize || '32px',
      font_weight: slotStyle.fontWeight || computedStyle.fontWeight || 'normal',
      font_style: computedStyle.fontStyle || 'normal',
      text_align: slotStyle.textAlign || computedStyle.textAlign || 'left',
      line_height: computedStyle.lineHeight || '1.4',
      letter_spacing: computedStyle.letterSpacing || 'normal',
      text_decoration: computedStyle.textDecoration?.split(' ')[0] || 'none',
      text_transform: slotStyle.textTransform || computedStyle.textTransform || 'none'
    };

    // Build container style with flexbox alignment from slot definition
    // justifyContent controls vertical alignment when flexDirection is 'column'
    // alignItems controls horizontal alignment when flexDirection is 'column'
    const style = {
      backgroundColor: 'transparent',  // Slots typically have transparent background
      borderWidth: 0,
      borderRadius: 0,
      padding: 0,  // Slots handle their own padding via grid
      opacity: 1,
      // Flexbox alignment from slot definition
      display: 'flex',
      flexDirection: 'column',
      justifyContent: slotStyle.justifyContent || 'flex-start',  // Vertical: flex-end = bottom
      alignItems: slotStyle.alignItems || 'flex-start'           // Horizontal: flex-start = left
    };

    return {
      id: `slide-${slideIndex}-slot-${slotName}-element`,  // Predictable ID for persistence
      position: position,
      style: style,
      textStyle: textStyle,
      placeholder: slotDef.defaultText || `Enter ${slotName}...`,
      draggable: true,
      resizable: true,
      zIndex: SLOT_Z_INDEX[slotName] || 1010
    };
  }

  // ===== IMAGE CONVERSION =====

  /**
   * Convert a slot element to an Image Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToImage(slotElement, slotDef, slotName, slideIndex) {
    // Extract image URL if present
    const imgElement = slotElement.querySelector('img');
    const imageUrl = imgElement?.src || null;
    const alt = imgElement?.alt || slotName;

    // Build configuration
    const config = buildImageConfigFromSlot(slotElement, slotDef, slotName, slideIndex);
    config.imageUrl = imageUrl;
    config.alt = alt;

    // Insert the Image element
    const result = window.ElementManager.insertImage(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created Image ${result.elementId} for slot '${slotName}'`);

      // REMOVE original slot element from DOM (not just hide)
      // This prevents ghost elements appearing when converted element is deleted
      slotElement.remove();

      // Add class to identify this as a converted slot element
      const newElement = document.getElementById(result.elementId);
      if (newElement) {
        newElement.classList.add('converted-slot', `slot-${slotName}`);
        newElement.dataset.originalSlot = slotName;

        // FORCE template-defined grid position (in case insertImage used defaults)
        newElement.style.gridRow = slotDef.gridRow;
        newElement.style.gridColumn = slotDef.gridColumn;

        // Special handling for Background Image
        if (slotName === 'background') {
          newElement.classList.add('slot-background');
          // Ensure background is behind everything and full-bleed
          newElement.style.zIndex = '1';
          newElement.style.borderRadius = '0';  // No rounded corners for full-bleed
        }

        // Special handling for Logo Image
        if (slotName === 'logo') {
          newElement.classList.add('slot-logo');
        }
      }
    } else {
      console.error(`[SlotConverter] Failed to create Image for slot '${slotName}':`, result.error);
    }
  }

  /**
   * Slot-specific customization for Image placeholders
   * Defines custom placeholder text and colors for different slot types
   */
  const SLOT_IMAGE_CUSTOMIZATION = {
    'background': {
      placeholderText: 'Background Image',
      placeholderColor: 'rgba(30, 58, 95, 0.8)'  // Darker blue for background
    },
    'logo': {
      placeholderText: 'Logo',
      placeholderColor: 'rgba(100, 116, 139, 0.6)'  // Slate gray for logo
    }
  };

  /**
   * Build Image configuration from slot element and definition
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   * @returns {Object} Image configuration object
   */
  function buildImageConfigFromSlot(slotElement, slotDef, slotName, slideIndex) {
    // Build position from slot definition
    const position = {
      gridRow: slotDef.gridRow || '1/19',
      gridColumn: slotDef.gridColumn || '1/33'
    };

    // Determine object-fit based on slot type
    const objectFit = slotName === 'background' ? 'cover' : 'contain';

    // Get slot-specific customization
    const customization = SLOT_IMAGE_CUSTOMIZATION[slotName] || {};

    return {
      id: `slide-${slideIndex}-slot-${slotName}-element`,
      position: position,
      objectFit: objectFit,
      draggable: slotName !== 'background',  // Background typically not draggable
      resizable: true,
      zIndex: SLOT_Z_INDEX[slotName] || 1,
      // Slot-specific placeholder customization
      placeholderText: customization.placeholderText,
      placeholderColor: customization.placeholderColor
    };
  }

  // ===== CHART CONVERSION =====

  /**
   * Convert a slot element to a Chart Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToChart(slotElement, slotDef, slotName, slideIndex) {
    // Build configuration
    const config = buildVisualElementConfig(slotElement, slotDef, slotName, slideIndex, 'chart');

    // Insert the Chart element
    const result = window.ElementManager.insertChart(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created Chart ${result.elementId} for slot '${slotName}'`);
      finalizeConvertedElement(slotElement, slotDef, slotName, result.elementId);
    } else {
      console.error(`[SlotConverter] Failed to create Chart for slot '${slotName}':`, result.error);
    }
  }

  // ===== INFOGRAPHIC CONVERSION =====

  /**
   * Convert a slot element to an Infographic Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToInfographic(slotElement, slotDef, slotName, slideIndex) {
    // Build configuration
    const config = buildVisualElementConfig(slotElement, slotDef, slotName, slideIndex, 'infographic');

    // Insert the Infographic element
    const result = window.ElementManager.insertInfographic(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created Infographic ${result.elementId} for slot '${slotName}'`);
      finalizeConvertedElement(slotElement, slotDef, slotName, result.elementId);
    } else {
      console.error(`[SlotConverter] Failed to create Infographic for slot '${slotName}':`, result.error);
    }
  }

  // ===== DIAGRAM CONVERSION =====

  /**
   * Convert a slot element to a Diagram Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToDiagram(slotElement, slotDef, slotName, slideIndex) {
    // Build configuration
    const config = buildVisualElementConfig(slotElement, slotDef, slotName, slideIndex, 'diagram');

    // Insert the Diagram element
    const result = window.ElementManager.insertDiagram(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created Diagram ${result.elementId} for slot '${slotName}'`);
      finalizeConvertedElement(slotElement, slotDef, slotName, result.elementId);
    } else {
      console.error(`[SlotConverter] Failed to create Diagram for slot '${slotName}':`, result.error);
    }
  }

  // ===== TABLE CONVERSION =====

  /**
   * Convert a slot element to a Table Element Type
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   */
  function convertToTable(slotElement, slotDef, slotName, slideIndex) {
    // Build configuration
    const config = buildVisualElementConfig(slotElement, slotDef, slotName, slideIndex, 'table');

    // Insert the Table element
    const result = window.ElementManager.insertTable(slideIndex, config);

    if (result.success) {
      console.log(`[SlotConverter] Created Table ${result.elementId} for slot '${slotName}'`);
      finalizeConvertedElement(slotElement, slotDef, slotName, result.elementId);
    } else {
      console.error(`[SlotConverter] Failed to create Table for slot '${slotName}':`, result.error);
    }
  }

  // ===== VISUAL ELEMENT HELPERS =====

  /**
   * Build configuration for visual elements (chart, infographic, diagram, table)
   *
   * @param {HTMLElement} slotElement - Original slot element
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {number} slideIndex - Slide index
   * @param {string} elementType - Element type (chart, infographic, diagram, table)
   * @returns {Object} Configuration object
   */
  function buildVisualElementConfig(slotElement, slotDef, slotName, slideIndex, elementType) {
    // Build position from slot definition
    const position = {
      gridRow: slotDef.gridRow || '4/17',
      gridColumn: slotDef.gridColumn || '2/32'
    };

    return {
      id: `slide-${slideIndex}-slot-${slotName}-element`,
      position: position,
      draggable: true,
      resizable: true,
      zIndex: SLOT_Z_INDEX[slotName] || 1016
    };
  }

  /**
   * Finalize a converted element - remove original slot and apply classes
   *
   * @param {HTMLElement} slotElement - Original slot element to remove
   * @param {Object} slotDef - Slot definition
   * @param {string} slotName - Slot name
   * @param {string} elementId - New element's ID
   */
  function finalizeConvertedElement(slotElement, slotDef, slotName, elementId) {
    // REMOVE original slot element from DOM
    slotElement.remove();

    // Add class to identify this as a converted slot element
    const newElement = document.getElementById(elementId);
    if (newElement) {
      newElement.classList.add('converted-slot', `slot-${slotName}`);
      newElement.dataset.originalSlot = slotName;

      // FORCE template-defined grid position
      newElement.style.gridRow = slotDef.gridRow;
      newElement.style.gridColumn = slotDef.gridColumn;
    }
  }

  // ===== UTILITY FUNCTIONS =====

  /**
   * Check if a slide has already been converted
   *
   * @param {HTMLElement} slideElement - The slide element
   * @param {string} templateId - Template ID
   * @returns {boolean} True if already converted
   */
  function isSlideConverted(slideElement, templateId) {
    // Check if any converted-slot elements exist
    return slideElement.querySelectorAll('.converted-slot').length > 0;
  }

  /**
   * Revert converted elements back to slots (for debugging/testing)
   *
   * @param {HTMLElement} slideElement - The slide element
   * @param {number} slideIndex - Slide index
   */
  function revertConvertedElements(slideElement, slideIndex) {
    // Find all converted slot elements
    const convertedElements = slideElement.querySelectorAll('.converted-slot');

    convertedElements.forEach(element => {
      const slotName = element.dataset.originalSlot;
      if (slotName) {
        // Delete the element
        window.ElementManager.deleteElement(element.id);

        // Show original slot
        const originalSlot = slideElement.querySelector(`.slot-${slotName}.converted, [data-slot-type="${slotName}"].converted`);
        if (originalSlot) {
          originalSlot.classList.remove('converted');
        }
      }
    });

    console.log(`[SlotConverter] Reverted ${convertedElements.length} elements on slide ${slideIndex}`);
  }

  // ===== EXPOSE TO GLOBAL SCOPE =====

  window.convertHeroSlotsToElements = convertHeroSlotsToElements;
  window.getElementTypeForSlot = getElementTypeForSlot;
  window.revertConvertedElements = revertConvertedElements;
  window.isSlideConverted = isSlideConverted;

  // Feature flag control
  window.SlotConverter = {
    enable: function() {
      console.log('[SlotConverter] Conversion enabled');
      // Note: Can't change const, this is for documentation
    },
    isEnabled: function() {
      return ENABLE_SLOT_CONVERSION;
    }
  };

  console.log('[SlotConverter] Module loaded. Use convertHeroSlotsToElements() to convert slots.');

})();
