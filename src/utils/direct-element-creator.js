/**
 * Direct Element Creator
 *
 * Simple approach: Instead of converting HTML slot elements to Element Types,
 * directly create elements using ElementManager with properties from template registry.
 *
 * Flow:
 * 1. Renderer outputs blank grid container
 * 2. This module creates elements directly using ElementManager
 * 3. No slot conversion, no race conditions
 *
 * Usage:
 *   createElementsForTemplate(slideElement, slideIndex, 'C6-image', content);
 */

(function() {
  'use strict';

  /**
   * Mapping from slot names/tags to Element Types
   */
  const SLOT_TO_ELEMENT_TYPE = {
    // Text slots -> TextBox
    'title': 'textbox',
    'subtitle': 'textbox',
    'footer': 'textbox',
    'body': 'textbox',

    // Visual content slots -> Their element types
    'image': 'image',
    'chart': 'chart',
    'infographic': 'infographic',
    'diagram': 'diagram',
    'table': 'table',

    // Image-based slots
    'logo': 'image',

    // Split template specific slots (S1-S4)
    'visual': 'image',        // S1/S3 visual slots - renders as image placeholder
    'header': 'textbox',      // S4 header slots
    'caption_left': 'textbox',  // S3 caption slots
    'caption_right': 'textbox',
    'header_left': 'textbox',   // S4 header slots
    'header_right': 'textbox',

    // NOTE: 'content', 'content_left', 'content_right' slots are NOT mapped here
    // They use slotDef.tag to determine type:
    // - S1: content_left.tag='visual', content_right.tag='body'
    // - S2: content.tag='body'
    // - S3: content_left/right.tag='visual'
    // - S4: content_left/right.tag='body'
  };

  /**
   * Create all elements for a template on a slide
   *
   * @param {HTMLElement} slideElement - The slide container element
   * @param {number} slideIndex - 0-based slide index
   * @param {string} templateId - Template ID (e.g., 'C6-image')
   * @param {Object} content - Content object from slide data
   */
  function createElementsForTemplate(slideElement, slideIndex, templateId, content) {
    // Check dependencies
    if (typeof TEMPLATE_REGISTRY === 'undefined') {
      console.error('[DirectElementCreator] TEMPLATE_REGISTRY not available');
      return;
    }

    if (typeof window.ElementManager === 'undefined') {
      console.error('[DirectElementCreator] ElementManager not available');
      return;
    }

    const template = TEMPLATE_REGISTRY[templateId];
    if (!template || !template.slots) {
      console.warn(`[DirectElementCreator] Template ${templateId} not found or has no slots`);
      return;
    }

    console.log(`[DirectElementCreator] Creating elements for ${templateId} on slide ${slideIndex}`);

    // Create each element from the template slots
    Object.entries(template.slots).forEach(([slotName, slotDef]) => {
      const elementType = getElementTypeForSlot(slotName, slotDef);

      console.log(`[DirectElementCreator] Creating ${elementType} for slot '${slotName}'`);

      switch (elementType) {
        case 'textbox':
          createTextBox(slideIndex, slotName, slotDef, content);
          break;
        case 'image':
          createImage(slideIndex, slotName, slotDef, content);
          break;
        case 'chart':
          createChart(slideIndex, slotName, slotDef, content);
          break;
        case 'infographic':
          createInfographic(slideIndex, slotName, slotDef, content);
          break;
        case 'diagram':
          createDiagram(slideIndex, slotName, slotDef, content);
          break;
        case 'table':
          createTable(slideIndex, slotName, slotDef, content);
          break;
        default:
          console.warn(`[DirectElementCreator] Unknown element type: ${elementType}`);
      }
    });

    console.log(`[DirectElementCreator] Finished creating elements for ${templateId}`);
  }

  /**
   * Determine element type for a slot
   */
  function getElementTypeForSlot(slotName, slotDef) {
    // First check by slot name
    if (SLOT_TO_ELEMENT_TYPE[slotName]) {
      return SLOT_TO_ELEMENT_TYPE[slotName];
    }

    // Then check by slot tag
    if (slotDef.tag && SLOT_TO_ELEMENT_TYPE[slotDef.tag]) {
      return SLOT_TO_ELEMENT_TYPE[slotDef.tag];
    }

    // Check accepts array
    if (slotDef.accepts) {
      if (slotDef.accepts.includes('image')) return 'image';
      if (slotDef.accepts.includes('text')) return 'textbox';
    }

    // Default to textbox
    return 'textbox';
  }

  /**
   * Create a TextBox element
   */
  function createTextBox(slideIndex, slotName, slotDef, content) {
    const slotStyle = slotDef.style || {};
    const textContent = getTextContent(slotName, content, slotDef.defaultText);

    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      content: textContent,
      style: {
        backgroundColor: 'transparent',
        borderWidth: 0,
        padding: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: slotStyle.justifyContent || 'flex-start',
        alignItems: slotStyle.alignItems || 'flex-start'
      },
      textStyle: {
        font_size: slotStyle.fontSize || '24px',
        font_family: slotStyle.fontFamily || 'Poppins, sans-serif',
        font_weight: slotStyle.fontWeight || 'normal',
        color: slotStyle.color || '#333333',
        text_align: slotStyle.textAlign || 'left',
        text_transform: slotStyle.textTransform || 'none'
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertTextBox(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created TextBox: ${result.elementId}`);

      // Apply additional styling to ensure flex alignment works
      const element = document.getElementById(result.elementId);
      if (element) {
        element.style.display = 'flex';
        element.style.flexDirection = 'column';
        element.style.justifyContent = slotStyle.justifyContent || 'flex-start';
        element.style.alignItems = slotStyle.alignItems || 'flex-start';

        // Fix inner content div for flex alignment
        const contentDiv = element.querySelector('.textbox-content');
        if (contentDiv) {
          contentDiv.style.minHeight = 'auto';
          contentDiv.style.height = 'auto';
          if (slotStyle.color) {
            contentDiv.style.color = slotStyle.color;
          }
        }
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create TextBox: ${result.error}`);
    }
  }

  /**
   * Create an Image element
   */
  function createImage(slideIndex, slotName, slotDef, content) {
    const imageUrl = getImageUrl(slotName, content);

    console.log(`[DirectElementCreator] createImage() called:`, {
      slideIndex,
      slotName,
      imageUrl,
      isPlaceholder: !imageUrl,
      contentImageUrl: content?.image_url,
      contentLogo: content?.company_logo
    });

    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      imageUrl: imageUrl,  // null = placeholder mode
      objectFit: 'contain',
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertImage(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Image: ${result.elementId} (placeholder: ${!imageUrl})`);
    } else {
      console.error(`[DirectElementCreator] Failed to create Image: ${result.error}`);
    }
  }

  /**
   * Create a Chart element (placeholder)
   */
  function createChart(slideIndex, slotName, slotDef, content) {
    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertChart(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Chart: ${result.elementId}`);
    } else {
      console.error(`[DirectElementCreator] Failed to create Chart: ${result.error}`);
    }
  }

  /**
   * Create an Infographic element (placeholder)
   */
  function createInfographic(slideIndex, slotName, slotDef, content) {
    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertInfographic(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Infographic: ${result.elementId}`);
    } else {
      console.error(`[DirectElementCreator] Failed to create Infographic: ${result.error}`);
    }
  }

  /**
   * Create a Diagram element (placeholder)
   */
  function createDiagram(slideIndex, slotName, slotDef, content) {
    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertDiagram(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Diagram: ${result.elementId}`);
    } else {
      console.error(`[DirectElementCreator] Failed to create Diagram: ${result.error}`);
    }
  }

  /**
   * Create a Table element (placeholder)
   */
  function createTable(slideIndex, slotName, slotDef, content) {
    const config = {
      id: `slide-${slideIndex}-${slotName}`,
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName)
    };

    const result = window.ElementManager.insertTable(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Table: ${result.elementId}`);
    } else {
      console.error(`[DirectElementCreator] Failed to create Table: ${result.error}`);
    }
  }

  /**
   * Get text content for a slot from the content object
   */
  function getTextContent(slotName, content, defaultText) {
    if (!content) return defaultText || '';

    const mapping = {
      // Standard content slots
      'title': content.slide_title || content.title,
      'subtitle': content.subtitle,
      'footer': content.footer_text || content.footer || content.presentation_name,
      'body': content.body || content.content_html,

      // Split template specific slots (S1-S4)
      'content_left': content.content_left || content.visual_content,
      'content_right': content.content_right || content.rich_content || content.body,
      'caption_left': content.caption_left,
      'caption_right': content.caption_right,
      'header_left': content.header_left || content.left_header,
      'header_right': content.header_right || content.right_header,

      // S2 uses 'content' for body text on right side
      'content': content.rich_content || content.body || content.content_html
    };

    return mapping[slotName] || defaultText || '';
  }

  /**
   * Get image URL for a slot from the content object
   * Returns null if no valid URL, which triggers placeholder mode
   */
  function getImageUrl(slotName, content) {
    if (!content) return null;

    // Helper to validate URL
    const isValidHttpUrl = (url) => url && typeof url === 'string' && url.startsWith('http');

    // Main content area - C6-image
    if (slotName === 'content') {
      const url = content.image_url;
      return isValidHttpUrl(url) ? url : null;
    }

    // Logo slot
    if (slotName === 'logo') {
      const url = content.company_logo;
      return isValidHttpUrl(url) ? url : null;
    }

    // S2-image-content: 'image' slot (full-height left image)
    if (slotName === 'image') {
      const url = content.image_url || content.image;
      return isValidHttpUrl(url) ? url : null;
    }

    // S1/S3 visual slots (content_left, content_right for visuals)
    // These are chart/diagram/infographic placeholders - return null for placeholder mode
    if (slotName === 'content_left' || slotName === 'content_right') {
      // Check if there's a valid image URL for this slot
      const urlMapping = {
        'content_left': content.visual_left_url || content.chart_url_1,
        'content_right': content.visual_right_url || content.chart_url_2
      };
      const url = urlMapping[slotName];
      return isValidHttpUrl(url) ? url : null;
    }

    return null;  // Default: placeholder mode
  }

  /**
   * Get z-index for a slot type
   */
  function getZIndexForSlot(slotName) {
    const zIndexMap = {
      // Standard slots
      'title': 1010,
      'subtitle': 1011,
      'footer': 1012,
      'logo': 1013,
      'content': 1016,
      'body': 1016,

      // Split template slots (S1-S4)
      'image': 1014,           // S2 full-height image
      'content_left': 1015,    // S1/S3/S4 left content
      'content_right': 1015,   // S1/S3/S4 right content
      'header_left': 1014,     // S4 headers
      'header_right': 1014,
      'caption_left': 1012,    // S3 captions
      'caption_right': 1012
    };
    return zIndexMap[slotName] || 1010;
  }

  // ===== EXPOSE TO GLOBAL SCOPE =====

  window.createElementsForTemplate = createElementsForTemplate;

  console.log('[DirectElementCreator] Module loaded. Use createElementsForTemplate() to create elements.');

})();
