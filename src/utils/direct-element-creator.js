/**
 * Direct Element Creator - v7.5.2 Infographic/Diagram Content Support
 *
 * Simple approach: Instead of converting HTML slot elements to Element Types,
 * directly create elements using ElementManager with properties from template registry.
 *
 * v7.5.2 Changes (Dec 27, 2025):
 * - Fixed C4-infographic and C5-diagram to render HTML content instead of placeholder
 * - Added getInfographicContent() and getDiagramContent() helpers
 * - Now passes svgContent to ElementManager for content mode rendering
 *
 * v7.5.1 Changes:
 * - UUID-based element IDs: {slide_id}_{type}_{uuid8} instead of slide-{index}-{slot}
 * - Elements now have parent_slide_id for cascade delete support
 * - Added 'content' element type for L-series layouts (Text Service ownership)
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
   * Generate a UUID-based element ID
   * Format: {slide_id}_{element_type}_{uuid8}
   * Example: slide_a3f7e8c2d5b1_textbox_f8c2d5b1
   *
   * @param {string} slideId - The parent slide's UUID (e.g., 'slide_a3f7e8c2d5b1')
   * @param {string} elementType - Element type (e.g., 'textbox', 'image', 'content')
   * @returns {string} UUID-based element ID
   */
  function generateElementId(slideId, elementType) {
    // Generate 8-char hex UUID
    const uuid8 = Array.from(crypto.getRandomValues(new Uint8Array(4)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
    return `${slideId}_${elementType}_${uuid8}`;
  }

  /**
   * Generate a legacy-compatible element ID for backward compatibility
   * Used during transition period when slides may not have slide_id yet
   *
   * @param {number} slideIndex - The slide index
   * @param {string} slotName - The slot name
   * @returns {string} Legacy element ID
   */
  function generateLegacyElementId(slideIndex, slotName) {
    return `slide-${slideIndex}-${slotName}`;
  }

  /**
   * Mapping from slot names/tags to Element Types
   */
  const SLOT_TO_ELEMENT_TYPE = {
    // Text slots -> TextBox
    'title': 'textbox',
    'subtitle': 'textbox',
    'footer': 'textbox',
    'author_info': 'textbox',  // H1-structured presenter/author info (NOT footer)
    'body': 'textbox',
    'body_left': 'textbox',     // L03 left text below chart
    'body_right': 'textbox',    // L03 right text below chart
    'text': 'textbox',          // L27 main text area

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

    // Hero template specific slots (H1-H3)
    'background': 'image',      // Full-bleed background image (H1, H2, H3)
    'section_number': 'textbox', // H2 large section number (180px)
    'contact_info': 'textbox',   // H3 contact information

    // L-series content slots -> 'content' element type (Text Service owns these)
    'content': 'content',       // L25 main content area
    'hero': 'content',          // L29 full-bleed hero content
    'chart1': 'content',        // L03 left chart area
    'chart2': 'content',        // L03 right chart area
    'rich_content': 'content',  // Alternative name for L25 content

    // NOTE: 'content_left', 'content_right' for C/S-series are NOT 'content' type
    // They use slotDef.tag to determine type:
    // - S1: content_left.tag='visual', content_right.tag='body'
    // - S2: content.tag='body' (becomes textbox)
    // - S3: content_left/right.tag='visual'
    // - S4: content_left/right.tag='body'
  };

  /**
   * v7.5.10: Chart type to grid size mapping
   * Sizes are in grid units (60px per unit)
   * Used to constrain chart elements to appropriate sizes instead of full slot width
   */
  const CHART_GRID_SIZES = {
    pie: { cols: 12, rows: 11 },
    doughnut: { cols: 12, rows: 11 },
    line: { cols: 16, rows: 11 },
    bar: { cols: 14, rows: 11 },
    bar_vertical: { cols: 14, rows: 11 },
    bar_horizontal: { cols: 16, rows: 10 },
    scatter: { cols: 15, rows: 11 },
    bubble: { cols: 15, rows: 11 },
    polar_area: { cols: 12, rows: 11 },
    polarArea: { cols: 12, rows: 11 },
    radar: { cols: 12, rows: 11 },
    area: { cols: 16, rows: 11 },
    waterfall: { cols: 16, rows: 11 },
    default: { cols: 16, rows: 11 }
  };

  /**
   * v7.5.10: Detect chart type from chart HTML content
   * Parses Chart.js configuration to find the chart type
   *
   * @param {string} chartHtml - The chart HTML content
   * @returns {string} Chart type or 'default'
   */
  function detectChartTypeFromHtml(chartHtml) {
    if (!chartHtml) return 'default';

    // Check for Chart.js type configurations (both quote styles)
    if (chartHtml.includes('type: "pie"') || chartHtml.includes("type: 'pie'") || chartHtml.includes('type:"pie"')) return 'pie';
    if (chartHtml.includes('type: "doughnut"') || chartHtml.includes("type: 'doughnut'") || chartHtml.includes('type:"doughnut"')) return 'doughnut';
    if (chartHtml.includes('type: "line"') || chartHtml.includes("type: 'line'") || chartHtml.includes('type:"line"')) return 'line';
    if (chartHtml.includes('type: "bar"') || chartHtml.includes("type: 'bar'") || chartHtml.includes('type:"bar"')) return 'bar';
    if (chartHtml.includes('type: "scatter"') || chartHtml.includes("type: 'scatter'") || chartHtml.includes('type:"scatter"')) return 'scatter';
    if (chartHtml.includes('type: "bubble"') || chartHtml.includes("type: 'bubble'") || chartHtml.includes('type:"bubble"')) return 'bubble';
    if (chartHtml.includes('type: "polarArea"') || chartHtml.includes("type: 'polarArea'") || chartHtml.includes('type:"polarArea"')) return 'polarArea';
    if (chartHtml.includes('type: "radar"') || chartHtml.includes("type: 'radar'") || chartHtml.includes('type:"radar"')) return 'radar';

    return 'default';
  }

  /**
   * v7.5.10: Calculate constrained chart position within slot bounds
   * Instead of using the full slot width, constrains the chart to its natural size
   *
   * @param {Object} slotDef - The slot definition with gridRow and gridColumn
   * @param {string} chartType - The detected chart type
   * @returns {Object} Constrained position {gridRow, gridColumn}
   */
  function getConstrainedChartPosition(slotDef, chartType) {
    const size = CHART_GRID_SIZES[chartType] || CHART_GRID_SIZES.default;

    // Parse slot bounds
    const [slotRowStart] = slotDef.gridRow.split('/').map(Number);
    const [slotColStart] = slotDef.gridColumn.split('/').map(Number);

    return {
      gridRow: `${slotRowStart}/${slotRowStart + size.rows}`,
      gridColumn: `${slotColStart}/${slotColStart + size.cols}`
    };
  }

  /**
   * Create all elements for a template on a slide
   *
   * @param {HTMLElement} slideElement - The slide container element
   * @param {number} slideIndex - 0-based slide index
   * @param {string} templateId - Template ID (e.g., 'C6-image')
   * @param {Object} content - Content object from slide data
   * @param {Object} [presentation] - Optional presentation data (for derivative elements)
   * @param {number} [totalSlides] - Optional total slide count (for footer {total} variable)
   */
  function createElementsForTemplate(slideElement, slideIndex, templateId, content, presentation = null, totalSlides = 0) {
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

    // Get or generate slide_id for UUID-based element IDs
    // New presentations will have slide_id in dataset, legacy ones won't
    let slideId = slideElement.dataset.slideId;
    const useLegacyIds = !slideId;

    if (!slideId) {
      // Backward compatibility: generate temporary slide_id for this session
      // The backend will persist it on save
      slideId = `slide_${Array.from(crypto.getRandomValues(new Uint8Array(6)))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('')}`;
      slideElement.dataset.slideId = slideId;
      console.log(`[DirectElementCreator] Generated slide_id: ${slideId} for slide ${slideIndex}`);
    }

    console.log(`[DirectElementCreator] Creating elements for ${templateId} on slide ${slideIndex} (slide_id: ${slideId}, legacy: ${useLegacyIds})`);

    // v7.5.5: Get slide object from presentation for slide-level fields (e.g., background_image)
    const slide = presentation?.slides?.[slideIndex] || {};

    // Create each element from the template slots
    Object.entries(template.slots).forEach(([slotName, slotDef]) => {
      // CHECK: Does this element already exist (from restore phase)?
      // If element was moved/modified and saved, it gets restored before this runs.
      // Skip creation to avoid duplicates.

      // Check for both legacy and new format element IDs
      // CRITICAL FIX: Only search within THIS slide, not globally
      // Using document.getElementById() caused elements from adjacent slides to be incorrectly
      // detected as "stale" and deleted when inserting new slides (slide indexes shift but IDs don't)
      const legacyElementId = generateLegacyElementId(slideIndex, slotName);
      const existingLegacy = slideElement.querySelector(`#${CSS.escape(legacyElementId)}`);

      // Also check for UUID-based elements by data attribute
      const existingUUID = slideElement.querySelector(`[data-slot-name="${slotName}"][data-parent-slide-id="${slideId}"]`);

      const existingElement = existingLegacy || existingUUID;

      if (existingElement) {
        // v7.5.5: Instead of skipping, UPDATE position from template
        // This ensures template changes (e.g., footer width) take effect even on restored elements
        const templatePosition = {
          gridRow: slotDef.gridRow,
          gridColumn: slotDef.gridColumn
        };
        existingElement.style.gridRow = templatePosition.gridRow;
        existingElement.style.gridColumn = templatePosition.gridColumn;
        console.log(`[DirectElementCreator] Updated ${slotName} position from template on slide ${slideIndex}: row=${templatePosition.gridRow}, col=${templatePosition.gridColumn}`);
        return;  // Element exists, position updated from template
      }

      const elementType = getElementTypeForSlot(slotName, slotDef);

      console.log(`[DirectElementCreator] Creating ${elementType} for slot '${slotName}'`);

      // Create element context for UUID architecture
      const elementContext = {
        slideIndex,
        slideId,
        slotName,
        slotDef,
        content,
        useLegacyIds,
        presentation,   // For derivative elements (footer/logo)
        totalSlides,    // For footer {total} variable
        slide           // v7.5.5: For slide-level fields (background_image)
      };

      switch (elementType) {
        case 'textbox':
          createTextBox(elementContext);
          break;
        case 'image':
          createImage(elementContext);
          break;
        case 'chart':
          createChart(elementContext);
          break;
        case 'infographic':
          createInfographic(elementContext);
          break;
        case 'diagram':
          createDiagram(elementContext);
          break;
        case 'table':
          createTable(elementContext);
          break;
        case 'content':
          createContent(elementContext);
          break;
        default:
          console.warn(`[DirectElementCreator] Unknown element type: ${elementType}`);
      }
    });

    console.log(`[DirectElementCreator] Finished creating elements for ${templateId}`);
  }

  /**
   * Determine element type for a slot
   *
   * Priority order (most specific first):
   * 1. Check slot TAG - determines actual element type (body→textbox, chart→chart, content→content)
   * 2. Check slot NAME - fallback for slots without explicit tag
   * 3. Check accepts array
   * 4. Default to textbox
   *
   * This ensures C-series templates work correctly:
   * - C1-text: slot 'content' with tag 'body' → textbox (not content)
   * - C3-chart: slot 'content' with tag 'chart' → chart (not content)
   * - L25: slot 'content' with tag 'content' → content (Text Service)
   */
  function getElementTypeForSlot(slotName, slotDef) {
    // First check by slot TAG (more specific - determines actual element type)
    if (slotDef.tag && SLOT_TO_ELEMENT_TYPE[slotDef.tag]) {
      return SLOT_TO_ELEMENT_TYPE[slotDef.tag];
    }

    // Then check by slot name
    if (SLOT_TO_ELEMENT_TYPE[slotName]) {
      return SLOT_TO_ELEMENT_TYPE[slotName];
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
   * Render footer content from derivative elements configuration
   * Replaces template variables with actual values
   *
   * Template Variables:
   * - {title}: Presentation title from footer.values.title
   * - {page}: Current slide number (1-indexed)
   * - {total}: Total number of slides
   * - {date}: Date from footer.values.date
   * - {author}: Author from footer.values.author
   *
   * @param {Object} footerConfig - Footer configuration from derivative_elements
   * @param {number} slideIndex - 0-based slide index
   * @param {number} totalSlides - Total number of slides
   * @returns {string} Rendered footer content
   */
  function renderFooterFromDerivative(footerConfig, slideIndex, totalSlides) {
    if (!footerConfig || !footerConfig.template) return '';

    const { template, values = {} } = footerConfig;
    const pageNumber = slideIndex + 1;  // 1-indexed

    return template
      .replace(/\{title\}/g, values.title || '')
      .replace(/\{page\}/g, pageNumber.toString())
      .replace(/\{total\}/g, totalSlides.toString())
      .replace(/\{date\}/g, values.date || '')
      .replace(/\{author\}/g, values.author || '');
  }

  /**
   * Create a TextBox element
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds, presentation, totalSlides }
   */
  function createTextBox(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds, presentation, totalSlides } = ctx;
    const slotStyle = slotDef.style || {};

    // Check for derivative footer (presentation-level footer config)
    let textContent;
    if (slotName === 'footer' && presentation?.derivative_elements?.footer) {
      textContent = renderFooterFromDerivative(
        presentation.derivative_elements.footer,
        slideIndex,
        totalSlides
      );
      console.log(`[DirectElementCreator] Using derivative footer for slide ${slideIndex}: "${textContent}"`);
    } else {
      textContent = getTextContent(slotName, content, slotDef.defaultText);
    }

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'textbox');

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      content: textContent,
      style: {
        // DEFAULTS FIRST (for new elements without template)
        backgroundColor: 'transparent',
        borderWidth: 0,
        padding: 16,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'flex-start',
        // THEN spread slotStyle to OVERRIDE where template specifies
        ...slotStyle
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

        // Set data attributes for UUID architecture
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;

        // Fix inner content div for flex alignment and height propagation
        const contentDiv = element.querySelector('.textbox-content');
        if (contentDiv) {
          // For content/body slots, maintain height: 100% so template HTML can fill the space
          // For other slots (title, subtitle, footer), use auto to allow flex positioning
          const isContentSlot = slotName === 'content' || slotName === 'body' ||
                                slotName === 'content_left' || slotName === 'content_right';
          if (isContentSlot) {
            // Content slots need height inheritance for template grids to work
            contentDiv.style.height = '100%';
            contentDiv.style.minHeight = '100%';
            // Add bottom padding to prevent content from stretching into footer
            contentDiv.style.paddingBottom = '30px';
            contentDiv.style.boxSizing = 'border-box';
          } else {
            // Other slots (title, subtitle, footer) use auto for flex positioning
            contentDiv.style.minHeight = 'auto';
            contentDiv.style.height = 'auto';
          }
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
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds, presentation, totalSlides, slide }
   */
  function createImage(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds, presentation, slide } = ctx;

    // Check for derivative logo (presentation-level logo config)
    let imageUrl;
    if (slotName === 'logo' && presentation?.derivative_elements?.logo?.image_url) {
      imageUrl = presentation.derivative_elements.logo.image_url;
      console.log(`[DirectElementCreator] Using derivative logo for slide ${slideIndex}: "${imageUrl}"`);
    } else {
      // v7.5.5: Pass slide object for slide-level fields like background_image
      imageUrl = getImageUrl(slotName, content, slide);
    }

    // Handle text/emoji logos (non-URL content like emojis or HTML)
    if (slotName === 'logo' && imageUrl && typeof imageUrl === 'object' && imageUrl.type === 'text') {
      createLogoTextElement(ctx, imageUrl.content);
      return;
    }

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'image');

    console.log(`[DirectElementCreator] createImage() called:`, {
      slideIndex,
      slotName,
      elementId,
      imageUrl,
      isPlaceholder: !imageUrl,
      contentImageUrl: content?.image_url,
      contentLogo: content?.logo || content?.company_logo  // Support both for backwards compatibility
    });

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
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

    // Use dark placeholder color for background slot (hero templates)
    if (slotName === 'background' && !imageUrl) {
      config.placeholderColor = '#1e3a5f';  // Dark blue for hero background
      config.objectFit = 'cover';           // Background should cover the area
    }

    // Use compact placeholder text for logo slot (2×2 grid = 120×120px)
    if (slotName === 'logo' && !imageUrl) {
      config.placeholderText = 'Logo';       // Short text for compact placeholder
      config.slotName = 'logo';              // For slot-logo CSS class
    }

    const result = window.ElementManager.insertImage(slideIndex, config);

    if (result.success) {
      console.log(`[DirectElementCreator] Created Image: ${result.elementId} (placeholder: ${!imageUrl})`);

      // Set data attributes for UUID architecture
      const element = document.getElementById(result.elementId);
      if (element) {
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create Image: ${result.error}`);
    }
  }

  /**
   * Create a text-based logo element (for emojis or HTML text)
   * @param {Object} ctx - Element context
   * @param {string} logoContent - The emoji or text content to display
   */
  function createLogoTextElement(ctx, logoContent) {
    const { slideIndex, slideId, slotName, slotDef, useLegacyIds } = ctx;

    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'logo');

    console.log(`[DirectElementCreator] Creating text logo element:`, {
      slideIndex,
      slotName,
      elementId,
      logoContent
    });

    // Get the slide element
    const slide = document.querySelector(`[data-slide-index="${slideIndex}"]`);
    if (!slide) {
      console.error(`[DirectElementCreator] Slide ${slideIndex} not found for logo`);
      return;
    }

    // Create logo container directly (not using ElementManager for text logos)
    const logoContainer = document.createElement('div');
    logoContainer.id = elementId;
    logoContainer.className = 'dynamic-element logo-text-element';
    logoContainer.dataset.elementType = 'logo';
    logoContainer.dataset.slideIndex = slideIndex;
    logoContainer.dataset.parentSlideId = slideId;
    logoContainer.dataset.slotName = slotName;
    logoContainer.style.cssText = `
      grid-row: ${slotDef.gridRow};
      grid-column: ${slotDef.gridColumn};
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: ${getZIndexForSlot(slotName)};
      font-size: 48px;
    `;
    logoContainer.innerHTML = logoContent;

    slide.appendChild(logoContainer);
    console.log(`[DirectElementCreator] Created text logo: ${elementId}`);
  }

  /**
   * Create a Chart element (placeholder or content mode)
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds }
   *
   * v7.5.2: Updated to support chart HTML content from Analytics Service
   * Now extracts chart_html from content and passes to ElementManager for content mode rendering
   */
  function createChart(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds } = ctx;

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'chart');

    // Extract chart content from the content object
    const chartContent = getChartContent(slotName, content);

    // v7.5.10: Detect chart type and calculate constrained position
    // This prevents charts from spanning the full slot width (2/32 = 1800px)
    const chartType = detectChartTypeFromHtml(chartContent);
    const constrainedPosition = getConstrainedChartPosition(slotDef, chartType);

    console.log(`[DirectElementCreator] Chart type detected: ${chartType}, position: row=${constrainedPosition.gridRow}, col=${constrainedPosition.gridColumn}`);

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
      position: constrainedPosition,  // v7.5.10: Use constrained position, not full slot
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName),
      // v7.5.2: Pass the content - if null, ElementManager shows placeholder
      chartHtml: chartContent
    };

    const result = window.ElementManager.insertChart(slideIndex, config);

    if (result.success) {
      // Log whether content or placeholder mode
      const mode = chartContent ? 'content' : 'placeholder';
      console.log(`[DirectElementCreator] Created Chart (${mode}): ${result.elementId}`);

      // Set data attributes for UUID architecture
      const element = document.getElementById(result.elementId);
      if (element) {
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create Chart: ${result.error}`);
    }
  }

  /**
   * Create an Infographic element (placeholder or content mode)
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds }
   */
  function createInfographic(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds } = ctx;

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'infographic');

    // Extract infographic content from the content object
    const infographicContent = getInfographicContent(slotName, content);

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName),
      // Pass the content - if null, ElementManager shows placeholder
      svgContent: infographicContent
    };

    const result = window.ElementManager.insertInfographic(slideIndex, config);

    if (result.success) {
      // Log whether content or placeholder mode
      const mode = infographicContent ? 'content' : 'placeholder';
      console.log(`[DirectElementCreator] Created Infographic (${mode}): ${result.elementId}`);

      // Set data attributes for UUID architecture
      const element = document.getElementById(result.elementId);
      if (element) {
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create Infographic: ${result.error}`);
    }
  }

  /**
   * Create a Diagram element (placeholder or content mode)
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds }
   */
  function createDiagram(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds } = ctx;

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'diagram');

    // Extract diagram content from the content object
    const diagramContent = getDiagramContent(slotName, content);

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
      position: {
        gridRow: slotDef.gridRow,
        gridColumn: slotDef.gridColumn
      },
      draggable: true,
      resizable: true,
      zIndex: getZIndexForSlot(slotName),
      // Pass the content - if null, ElementManager shows placeholder
      svgContent: diagramContent
    };

    const result = window.ElementManager.insertDiagram(slideIndex, config);

    if (result.success) {
      // Log whether content or placeholder mode
      const mode = diagramContent ? 'content' : 'placeholder';
      console.log(`[DirectElementCreator] Created Diagram (${mode}): ${result.elementId}`);

      // Set data attributes for UUID architecture
      const element = document.getElementById(result.elementId);
      if (element) {
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create Diagram: ${result.error}`);
    }
  }

  /**
   * Create a Table element (placeholder)
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds }
   */
  function createTable(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds } = ctx;

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'table');

    const config = {
      id: elementId,
      parent_slide_id: slideId,  // v7.5.1: For cascade delete
      slot_name: slotName,       // v7.5.1: For slot mapping
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

      // Set data attributes for UUID architecture
      const element = document.getElementById(result.elementId);
      if (element) {
        element.dataset.parentSlideId = slideId;
        element.dataset.slotName = slotName;
      }
    } else {
      console.error(`[DirectElementCreator] Failed to create Table: ${result.error}`);
    }
  }

  /**
   * Create a Content element (L-series layouts - Text Service ownership)
   *
   * Content elements are:
   * - Read-only in layout builder (Text Service owns the HTML)
   * - Not draggable/resizable by default
   * - Can contain rich HTML content from Text Service
   *
   * @param {Object} ctx - Element context { slideIndex, slideId, slotName, slotDef, content, useLegacyIds }
   */
  function createContent(ctx) {
    const { slideIndex, slideId, slotName, slotDef, content, useLegacyIds } = ctx;

    // Generate element ID based on architecture mode
    const elementId = useLegacyIds
      ? generateLegacyElementId(slideIndex, slotName)
      : generateElementId(slideId, 'content');

    // Get content HTML from the appropriate field
    const contentHtml = getContentHtml(slotName, content, slotDef);

    // Determine format owner from slotDef (text_service, analytics_service, etc.)
    const formatOwner = slotDef.formatOwner || 'text_service';

    console.log(`[DirectElementCreator] Creating Content element:`, {
      elementId,
      slotName,
      formatOwner,
      hasContent: !!contentHtml
    });

    // Create the content element directly (no ElementManager.insertContent yet)
    // For now, create a div container that renders the HTML content
    const slideElement = document.querySelector(`section[data-slide-index="${slideIndex}"]`);
    if (!slideElement) {
      console.error(`[DirectElementCreator] Slide element not found for index ${slideIndex}`);
      return;
    }

    // Create the content container
    const contentElement = document.createElement('div');
    contentElement.id = elementId;
    contentElement.className = 'inserted-content content-element';
    contentElement.dataset.elementType = 'content';
    contentElement.dataset.parentSlideId = slideId;
    contentElement.dataset.slotName = slotName;
    contentElement.dataset.formatOwner = formatOwner;

    // Apply grid positioning
    contentElement.style.gridRow = slotDef.gridRow;
    contentElement.style.gridColumn = slotDef.gridColumn;
    contentElement.style.position = 'relative';
    contentElement.style.overflow = 'hidden';
    contentElement.style.zIndex = getZIndexForSlot(slotName);

    // Content elements are NOT editable in layout builder
    contentElement.contentEditable = 'false';
    contentElement.dataset.editable = 'false';
    contentElement.dataset.locked = 'true';

    // Set the HTML content
    contentElement.innerHTML = contentHtml || `
      <div class="content-placeholder" style="
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        background: #f3f4f6;
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        color: #6b7280;
        font-family: Poppins, sans-serif;
        font-size: 18px;
      ">
        Content (${formatOwner})
      </div>
    `;

    // Add to slide
    slideElement.appendChild(contentElement);

    console.log(`[DirectElementCreator] Created Content: ${elementId} (owner: ${formatOwner})`);
  }

  /**
   * Get HTML content for content elements (L-series)
   */
  function getContentHtml(slotName, content, slotDef) {
    if (!content) return '';

    // Map slot names to content fields
    const mapping = {
      'content': content.rich_content || content.content_html || content.body,
      'hero': content.hero_content || content.rich_content,
      'chart': content.chart_html || content.element_4,
      'chart1': content.chart_html_1 || content.element_4,
      'chart2': content.chart_html_2 || content.element_2,
      'diagram': content.diagram_html || content.element_3,
      'rich_content': content.rich_content
    };

    return mapping[slotName] || '';
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
      'content': content.rich_content || content.body || content.content_html,

      // Hero template specific slots (H1-H3)
      'section_number': content.section_number || content.chapter_number,
      'contact_info': content.contact_info || content.contact || content.email,
      'author_info': content.author_info || content.author || content.presenter
    };

    return mapping[slotName] || defaultText || '';
  }

  /**
   * Get image URL for a slot from the content object
   * Returns null if no valid URL, which triggers placeholder mode
   *
   * @param {string} slotName - The slot name
   * @param {Object} content - Content object from slide
   * @param {Object} [slide] - Optional slide object (for slide-level fields like background_image)
   */
  function getImageUrl(slotName, content, slide = {}) {
    if (!content) return null;

    // Helper to validate URL
    const isValidHttpUrl = (url) => url && typeof url === 'string' && url.startsWith('http');

    // Hero template background slot (H1, H2, H3)
    // IMPORTANT: background_image is stored at SLIDE level, not in content
    if (slotName === 'background') {
      const url = slide?.background_image || content.background_image || content.hero_image || content.image_url;
      console.log(`[DirectElementCreator] getImageUrl background: slide.background_image="${slide?.background_image}", content.background_image="${content.background_image}", result="${url}"`);
      return isValidHttpUrl(url) ? url : null;
    }

    // Main content area - C6-image
    if (slotName === 'content') {
      const url = content.image_url;
      return isValidHttpUrl(url) ? url : null;
    }

    // Logo slot - support both 'logo' and legacy 'company_logo' field names
    // Logo can be: URL (image), emoji, or text/HTML
    if (slotName === 'logo') {
      const logoContent = content.logo || content.company_logo;
      if (!logoContent) return null;
      // If it's a valid URL, return it for image mode
      if (isValidHttpUrl(logoContent)) return logoContent;
      // For emoji/text content, return special marker to trigger direct rendering
      return { type: 'text', content: logoContent };
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
   * Get infographic content (SVG/HTML) for a slot from the content object
   * Returns null if no valid content, which triggers placeholder mode
   */
  function getInfographicContent(slotName, content) {
    if (!content) return null;

    // For C4-infographic and V4-infographic-text layouts
    // Support multiple field names for flexibility
    if (slotName === 'content' || slotName === 'infographic') {
      return content.infographic_html ||    // API documented field
             content.infographic_svg ||     // Server default field
             content.svg_content ||         // InfographicElement model field
             content.html_content ||        // InfographicElement alt field
             null;
    }

    // For V4-infographic-text (visual left)
    if (slotName === 'visual_left' || slotName === 'visual') {
      return content.infographic_html ||
             content.visual_left_html ||
             content.infographic_svg ||
             null;
    }

    return null;
  }

  /**
   * Get diagram content (SVG/HTML) for a slot from the content object
   * Returns null if no valid content, which triggers placeholder mode
   *
   * v7.5.3 Fix: Added content_left support for V3-diagram-text layout
   */
  function getDiagramContent(slotName, content) {
    if (!content) return null;

    // For C5-diagram and V3-diagram-text layouts
    // v7.5.3: Added 'content_left' for V3-diagram-text (slot name is content_left, tag is diagram)
    if (slotName === 'content' || slotName === 'diagram' || slotName === 'content_left') {
      return content.diagram_html ||     // API documented field
             content.diagram_svg ||      // Alternative field
             content.svg_content ||      // DiagramElement model field
             content.mermaid_svg ||      // Mermaid rendered output
             null;
    }

    // For V3-diagram-text (visual left) - alternative slot names
    if (slotName === 'visual_left' || slotName === 'visual') {
      return content.diagram_html ||
             content.visual_left_html ||
             content.diagram_svg ||
             null;
    }

    return null;
  }

  /**
   * Get chart content (HTML) for a slot from the content object
   * Returns null if no valid content, which triggers placeholder mode
   *
   * v7.5.2: Added to fix analytics slides (C3-chart, V2-chart-text) rendering placeholders
   * Follows the same pattern as getInfographicContent() and getDiagramContent()
   */
  function getChartContent(slotName, content) {
    if (!content) return null;

    // For C3-chart and V2-chart-text layouts
    // C3-chart uses 'content' slot, V2-chart-text uses 'content_left' slot
    if (slotName === 'content' || slotName === 'content_left' || slotName === 'chart') {
      return content.chart_html ||        // API documented field
             content.analytics_html ||    // Alternative field name
             content.element_3 ||         // V2/C3 Analytics Service alias
             content.element_4 ||         // L-series element mapping
             null;
    }

    // For visual slots (V2-chart-text visual left alternative naming)
    if (slotName === 'visual_left' || slotName === 'visual') {
      return content.chart_html ||
             content.visual_left_html ||
             null;
    }

    return null;
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
      'caption_right': 1012,

      // Hero template slots (H1-H3)
      'background': 1,         // Full-bleed background - behind everything
      'section_number': 1014,  // H2 large section number
      'contact_info': 1015,    // H3 contact information
      'author_info': 1014      // H1-structured author/presenter info
    };
    return zIndexMap[slotName] || 1010;
  }

  // ===== DERIVATIVE ELEMENTS SYNC =====

  /**
   * Sync derivative elements (footer/logo) across all slides
   *
   * Call this when derivative_elements config changes to update all footer/logo
   * elements across all slides without re-rendering everything.
   *
   * @param {Object} presentation - Presentation data with derivative_elements
   * @param {number} totalSlides - Total number of slides
   */
  function syncDerivativeElements(presentation, totalSlides) {
    console.log('[DirectElementCreator] Syncing derivative elements across slides');

    if (!presentation?.derivative_elements) {
      console.log('[DirectElementCreator] No derivative elements to sync');
      return;
    }

    const { footer, logo } = presentation.derivative_elements;
    const slides = document.querySelectorAll('.reveal .slides > section');

    slides.forEach((slideElement, slideIndex) => {
      // Sync footer
      if (footer) {
        const footerElement = slideElement.querySelector('[data-slot-name="footer"]');
        if (footerElement) {
          const footerContent = renderFooterFromDerivative(footer, slideIndex, totalSlides);
          const contentDiv = footerElement.querySelector('.textbox-content');
          if (contentDiv) {
            contentDiv.innerHTML = footerContent;
            console.log(`[DirectElementCreator] Updated footer on slide ${slideIndex}: "${footerContent}"`);
          }
        }
      }

      // Sync logo
      if (logo?.image_url) {
        const logoElement = slideElement.querySelector('[data-slot-name="logo"]');
        if (logoElement) {
          const img = logoElement.querySelector('img');
          if (img) {
            img.src = logo.image_url;
            if (logo.alt_text) img.alt = logo.alt_text;
            console.log(`[DirectElementCreator] Updated logo on slide ${slideIndex}`);
          }
        }
      }
    });

    console.log(`[DirectElementCreator] Synced derivative elements across ${slides.length} slides`);
  }

  // ===== X-SERIES DYNAMIC LAYOUT SUPPORT =====

  /**
   * Create elements for an X-series dynamic layout
   *
   * X-series layouts have:
   * - Structural slots (title, subtitle, footer, logo, image) from the base template
   * - Dynamic zones for the content area (fetched from the API)
   *
   * @param {HTMLElement} slideElement - The slide container element
   * @param {number} slideIndex - 0-based slide index
   * @param {string} layoutId - X-series layout ID (e.g., "X1-a3f7e8c2")
   * @param {Object} content - Content object from slide data
   * @param {Object} layoutData - Layout data with zones array
   * @param {Object} [presentation] - Optional presentation data (for derivative elements)
   * @param {number} [totalSlides] - Optional total slide count (for footer {total} variable)
   */
  function createElementsForDynamicTemplate(slideElement, slideIndex, layoutId, content, layoutData, presentation = null, totalSlides = 0) {
    // Validate layout data
    if (!layoutData || !layoutData.zones || !layoutData.base_layout) {
      console.error(`[DirectElementCreator] Invalid layout data for ${layoutId}`);
      return;
    }

    // Get or generate slide_id for UUID-based element IDs
    let slideId = slideElement.dataset.slideId;
    const useLegacyIds = !slideId;

    if (!slideId) {
      slideId = `slide_${Array.from(crypto.getRandomValues(new Uint8Array(6)))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('')}`;
      slideElement.dataset.slideId = slideId;
      console.log(`[DirectElementCreator] Generated slide_id: ${slideId} for dynamic layout slide ${slideIndex}`);
    }

    console.log(`[DirectElementCreator] Creating elements for X-series ${layoutId} on slide ${slideIndex} (base: ${layoutData.base_layout})`);

    // Get the virtual template (registered by DynamicTemplates module)
    let template = typeof TEMPLATE_REGISTRY !== 'undefined' ? TEMPLATE_REGISTRY[layoutId] : null;

    // If not registered, create a virtual template on the fly
    if (!template && typeof window.DynamicTemplates !== 'undefined') {
      template = window.DynamicTemplates.createVirtualTemplate(layoutId, layoutData);
    }

    if (!template) {
      console.error(`[DirectElementCreator] Could not get template for ${layoutId}`);
      return;
    }

    // Create structural elements first (title, subtitle, footer, logo, image)
    const structuralSlots = ['title', 'subtitle', 'footer', 'logo', 'image'];

    for (const slotName of structuralSlots) {
      const slotDef = template.slots[slotName];
      if (!slotDef) continue;

      // Check if element already exists
      const legacyElementId = generateLegacyElementId(slideIndex, slotName);
      const existingLegacy = slideElement.querySelector(`#${CSS.escape(legacyElementId)}`);
      const existingUUID = slideElement.querySelector(`[data-slot-name="${slotName}"][data-parent-slide-id="${slideId}"]`);
      const existingElement = existingLegacy || existingUUID;

      if (existingElement) {
        // v7.5.5: Update position from template instead of skipping
        existingElement.style.gridRow = slotDef.gridRow;
        existingElement.style.gridColumn = slotDef.gridColumn;
        console.log(`[DirectElementCreator] Updated ${slotName} position from template (X-series)`);
        continue;
      }

      const elementType = getElementTypeForSlot(slotName, slotDef);
      const elementContext = {
        slideIndex,
        slideId,
        slotName,
        slotDef,
        content,
        useLegacyIds,
        presentation,
        totalSlides
      };

      switch (elementType) {
        case 'textbox':
          createTextBox(elementContext);
          break;
        case 'image':
          createImage(elementContext);
          break;
      }
    }

    // Now create zone elements for the dynamic content area
    createZoneElements(slideElement, slideIndex, slideId, layoutData.zones, content, useLegacyIds);

    console.log(`[DirectElementCreator] Finished creating elements for X-series ${layoutId}`);
  }

  /**
   * Create zone elements for dynamic content areas
   *
   * @param {HTMLElement} slideElement - The slide container
   * @param {number} slideIndex - Slide index
   * @param {string} slideId - Slide UUID
   * @param {Array} zones - Array of zone definitions
   * @param {Object} content - Content object
   * @param {boolean} useLegacyIds - Whether to use legacy IDs
   */
  function createZoneElements(slideElement, slideIndex, slideId, zones, content, useLegacyIds) {
    zones.forEach((zone, zoneIndex) => {
      const zoneId = zone.zone_id || `zone_${zoneIndex + 1}`;

      // Check if zone element already exists
      const existingZone = slideElement.querySelector(`[data-zone-id="${zoneId}"]`);
      if (existingZone) {
        // v7.5.5: Update position from template instead of skipping
        existingZone.style.gridRow = zone.grid_row;
        existingZone.style.gridColumn = zone.grid_column;
        console.log(`[DirectElementCreator] Updated zone ${zoneId} position from template`);
        return;
      }

      // Create the zone container element
      const zoneElement = document.createElement('div');
      zoneElement.className = 'inserted-element dynamic-zone zone-element';
      zoneElement.dataset.elementType = 'zone';
      zoneElement.dataset.zoneId = zoneId;
      zoneElement.dataset.zoneIndex = zoneIndex;
      zoneElement.dataset.parentSlideId = slideId;
      zoneElement.dataset.slotName = zoneId;

      // Generate element ID
      const elementId = useLegacyIds
        ? `slide-${slideIndex}-${zoneId}`
        : `${slideId}_zone_${Array.from(crypto.getRandomValues(new Uint8Array(4)))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('')}`;
      zoneElement.id = elementId;

      // Apply grid positioning
      zoneElement.style.gridRow = zone.grid_row;
      zoneElement.style.gridColumn = zone.grid_column;
      zoneElement.style.position = 'relative';
      zoneElement.style.zIndex = zone.z_index || (100 + zoneIndex);

      // Apply zone styling
      Object.assign(zoneElement.style, {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'flex-start',
        padding: '10px',
        overflow: 'hidden',
        fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
        fontSize: 'var(--theme-body-size, 24px)',
        color: 'var(--theme-text-body, #374151)'
      });

      // Set zone metadata
      if (zone.label) {
        zoneElement.dataset.zoneLabel = zone.label;
      }
      if (zone.content_type_hint) {
        zoneElement.dataset.contentTypeHint = zone.content_type_hint;
      }

      // Get zone content from content object
      const zoneContent = getZoneContent(zoneId, zoneIndex, zone, content);

      if (zoneContent) {
        // If we have content, render it
        zoneElement.innerHTML = zoneContent;
      } else {
        // Show placeholder
        zoneElement.innerHTML = `
          <div class="zone-placeholder" style="
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 100%;
            background: #f3f4f6;
            border: 2px dashed #d1d5db;
            border-radius: 6px;
            color: #6b7280;
            font-size: 16px;
          ">
            ${zone.label || `Zone ${zoneIndex + 1}`}
          </div>
        `;
      }

      // Add to slide
      slideElement.appendChild(zoneElement);

      console.log(`[DirectElementCreator] Created zone: ${elementId} (${zone.label || zoneId})`);
    });
  }

  /**
   * Get content for a specific zone from the content object
   *
   * @param {string} zoneId - Zone identifier
   * @param {number} zoneIndex - Zone index
   * @param {Object} zone - Zone definition
   * @param {Object} content - Content object
   * @returns {string|null} HTML content for the zone
   */
  function getZoneContent(zoneId, zoneIndex, zone, content) {
    if (!content) return null;

    // Check for direct zone content
    if (content.zones && content.zones[zoneId]) {
      return content.zones[zoneId];
    }

    // Check for indexed zone content
    if (content.zones && content.zones[zoneIndex]) {
      return content.zones[zoneIndex];
    }

    // Check for zone_X pattern
    const zoneKey = `zone_${zoneIndex + 1}`;
    if (content[zoneKey]) {
      return content[zoneKey];
    }

    // Check for content_type_hint mapping
    if (zone.content_type_hint && content[zone.content_type_hint]) {
      return content[zone.content_type_hint];
    }

    return null;
  }

  /**
   * Update a specific zone's content
   *
   * @param {HTMLElement} slideElement - The slide container
   * @param {string} zoneId - Zone identifier
   * @param {string} content - HTML content to set
   */
  function updateZoneContent(slideElement, zoneId, content) {
    const zoneElement = slideElement.querySelector(`[data-zone-id="${zoneId}"]`);
    if (!zoneElement) {
      console.warn(`[DirectElementCreator] Zone ${zoneId} not found`);
      return false;
    }

    zoneElement.innerHTML = content;
    return true;
  }

  /**
   * Get all zone elements from a slide
   *
   * @param {HTMLElement} slideElement - The slide container
   * @returns {NodeListOf<Element>} List of zone elements
   */
  function getZoneElements(slideElement) {
    return slideElement.querySelectorAll('.zone-element[data-zone-id]');
  }

  // ===== EXPOSE TO GLOBAL SCOPE =====

  window.createElementsForTemplate = createElementsForTemplate;
  window.createElementsForDynamicTemplate = createElementsForDynamicTemplate;
  window.createZoneElements = createZoneElements;
  window.updateZoneContent = updateZoneContent;
  window.getZoneElements = getZoneElements;
  window.syncDerivativeElements = syncDerivativeElements;
  window.renderFooterFromDerivative = renderFooterFromDerivative;  // Expose for UI preview

  console.log('[DirectElementCreator] Module loaded. Use createElementsForTemplate() for standard layouts, createElementsForDynamicTemplate() for X-series.');

})();
