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
    'body': 'textbox',

    // Image-based slots -> Image Element Type
    'logo': 'image',
    'background': 'image'
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
    'body': 1016
  };

  /**
   * CSS class to DOM selector mapping for finding slot elements
   */
  const SLOT_CLASS_SELECTORS = {
    'H1-structured': {
      'title': '.title-hero',
      'subtitle': '.subtitle-hero',
      'footer': '.footer-hero',
      'logo': '.logo-hero',
      'background': '.background-hero'
    },
    'H2-section': {
      'section_number': '.section-number',
      'title': '.title-hero',
      'background': '.background-hero'
    },
    'H3-closing': {
      'title': '.title-hero',
      'subtitle': '.subtitle-hero',
      'contact_info': '.contact-info',
      'logo': '.logo-hero',
      'background': '.background-hero'
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
      const existingId = `slide-${slideIndex}-slot-${slotName}-element`;
      if (document.getElementById(existingId)) {
        console.log(`[SlotConverter] Element ${existingId} already exists (restored)`);
        slotElement.classList.add('converted');
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
   * @returns {string} Element type: 'textbox' or 'image'
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

    if (elementType === 'textbox') {
      convertToTextBox(slotElement, slotDef, slotName, slideIndex);
    } else if (elementType === 'image') {
      convertToImage(slotElement, slotDef, slotName, slideIndex);
    } else {
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

      // Mark original slot as converted and hide it
      slotElement.classList.add('converted');

      // Add class to identify this as a converted slot element
      const newElement = document.getElementById(result.elementId);
      if (newElement) {
        newElement.classList.add('converted-slot', `slot-${slotName}`);
        newElement.dataset.originalSlot = slotName;
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
    const textStyle = {
      color: slotStyle.color || computedStyle.color || '#ffffff',
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

      // Mark original slot as converted and hide it
      slotElement.classList.add('converted');

      // Add class to identify this as a converted slot element
      const newElement = document.getElementById(result.elementId);
      if (newElement) {
        newElement.classList.add('converted-slot', `slot-${slotName}`);
        newElement.dataset.originalSlot = slotName;

        // Special handling for background
        if (slotName === 'background') {
          newElement.classList.add('slot-background');
          // Ensure background is behind everything
          newElement.style.zIndex = '1';
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
