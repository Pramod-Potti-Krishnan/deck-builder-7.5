/**
 * Element Manager for Layout Builder v7.5
 *
 * Manages dynamic elements (shapes, tables, charts, images) in slides.
 * Provides CRUD operations, element registry, and selection state.
 *
 * Exposed via window.ElementManager for postMessage handler access.
 */

(function() {
  'use strict';

  // ===== ELEMENT REGISTRY =====

  /**
   * Registry of all managed elements
   * Key: elementId, Value: ElementData
   */
  const elementRegistry = new Map();

  /**
   * Currently selected element ID
   */
  let selectedElementId = null;

  /**
   * Z-index counter for layering
   */
  let zIndexCounter = 100;

  // ===== ELEMENT DATA STRUCTURE =====

  /**
   * @typedef {Object} ElementData
   * @property {string} id - Unique element ID
   * @property {string} type - Element type: shape|table|chart|image
   * @property {number} slideIndex - Slide containing this element
   * @property {Object} position - Grid position {gridRow, gridColumn}
   * @property {number} zIndex - Layer order
   * @property {boolean} selected - Selection state
   * @property {Object} data - Type-specific data
   */

  // ===== ID GENERATION =====

  /**
   * Generate unique element ID
   *
   * @param {string} type - Element type
   * @returns {string} Unique ID
   */
  function generateId(type) {
    const timestamp = Date.now().toString(36);
    const random = Math.random().toString(36).substring(2, 8);
    return `${type}-${timestamp}-${random}`;
  }

  // ===== INSERT SHAPE =====

  /**
   * Insert a shape element into a slide
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Shape configuration
   * @param {string} config.shape - Shape type: rect|circle|triangle|arrow|line|star
   * @param {Object} config.position - Grid position {gridRow, gridColumn}
   * @param {Object} [config.style] - Shape styling {fill, stroke, strokeWidth, opacity}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @returns {Object} Result with elementId
   */
  function insertShape(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const id = generateId('shape');
    const position = config.position || { gridRow: '8/12', gridColumn: '10/22' };
    const style = config.style || {};
    const fill = style.fill || '#3b82f6';
    const stroke = style.stroke || '#1e40af';
    const strokeWidth = style.strokeWidth || 2;
    const opacity = style.opacity || 1;

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-shape';
    container.dataset.elementType = 'shape';
    container.dataset.shapeType = config.shape || 'rect';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: ${++zIndexCounter};
      opacity: ${opacity};
      cursor: ${config.draggable !== false ? 'move' : 'default'};
    `;

    // Generate SVG
    const svgContent = generateShapeSVG(config.shape || 'rect', fill, stroke, strokeWidth);
    container.innerHTML = svgContent;

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Enable drag-drop if requested
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Add to slide
    slide.appendChild(container);

    // Register element
    const elementData = {
      id: id,
      type: 'shape',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        shapeType: config.shape || 'rect',
        style: { fill, stroke, strokeWidth, opacity }
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save
    triggerAutoSave(slideIndex);

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Generate SVG markup for a shape
   *
   * @param {string} shapeType - Shape type
   * @param {string} fill - Fill color
   * @param {string} stroke - Stroke color
   * @param {number} strokeWidth - Stroke width
   * @returns {string} SVG markup
   */
  function generateShapeSVG(shapeType, fill, stroke, strokeWidth) {
    const shapes = {
      rect: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <rect x="${strokeWidth}" y="${strokeWidth}"
              width="${100 - strokeWidth * 2}" height="${100 - strokeWidth * 2}"
              fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" rx="8"/>
      </svg>`,

      circle: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <circle cx="50" cy="50" r="${48 - strokeWidth}"
                fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"/>
      </svg>`,

      triangle: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <polygon points="50,${strokeWidth} ${100 - strokeWidth},${100 - strokeWidth} ${strokeWidth},${100 - strokeWidth}"
                 fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"
                 stroke-linejoin="round"/>
      </svg>`,

      arrow: `<svg viewBox="0 0 100 50" style="width:100%;height:100%">
        <polygon points="0,15 65,15 65,0 100,25 65,50 65,35 0,35"
                 fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"
                 stroke-linejoin="round"/>
      </svg>`,

      line: `<svg viewBox="0 0 100 20" style="width:100%;height:100%">
        <line x1="0" y1="10" x2="100" y2="10"
              stroke="${stroke}" stroke-width="${strokeWidth * 2}" stroke-linecap="round"/>
      </svg>`,

      star: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <polygon points="50,${strokeWidth} 61,35 97,35 68,57 79,91 50,70 21,91 32,57 3,35 39,35"
                 fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"
                 stroke-linejoin="round"/>
      </svg>`,

      roundedRect: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <rect x="${strokeWidth}" y="${strokeWidth}"
              width="${100 - strokeWidth * 2}" height="${100 - strokeWidth * 2}"
              fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" rx="20"/>
      </svg>`,

      diamond: `<svg viewBox="0 0 100 100" style="width:100%;height:100%">
        <polygon points="50,${strokeWidth} ${100 - strokeWidth},50 50,${100 - strokeWidth} ${strokeWidth},50"
                 fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}"
                 stroke-linejoin="round"/>
      </svg>`
    };

    return shapes[shapeType] || shapes.rect;
  }

  // ===== INSERT TABLE =====

  /**
   * Insert a table element into a slide
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Table configuration
   * @param {string} [config.tableHtml] - Pre-formatted HTML from Text Service
   * @param {number} [config.rows] - Number of rows (if no tableHtml)
   * @param {number} [config.cols] - Number of columns (if no tableHtml)
   * @param {string[][]} [config.data] - Initial cell data
   * @param {Object} config.position - Grid position {gridRow, gridColumn}
   * @param {Object} [config.style] - Table styling
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @returns {Object} Result with elementId
   */
  function insertTable(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const id = generateId('table');
    const position = config.position || { gridRow: '5/14', gridColumn: '3/30' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-table';
    container.dataset.elementType = 'table';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      overflow: auto;
      z-index: ${++zIndexCounter};
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      cursor: ${config.draggable !== false ? 'move' : 'default'};
    `;

    // Use provided HTML or generate table
    if (config.tableHtml) {
      container.innerHTML = config.tableHtml;
    } else {
      const rows = config.rows || 3;
      const cols = config.cols || 3;
      const data = config.data || [];
      const style = config.style || {};
      container.innerHTML = generateTableHTML(rows, cols, data, style);
    }

    // Add cell edit listeners
    container.querySelectorAll('td, th').forEach(cell => {
      if (cell.contentEditable === 'true') {
        cell.addEventListener('input', () => {
          triggerAutoSave(slideIndex);
        });
      }
    });

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      // Don't select if clicking on editable cell
      if (e.target.tagName === 'TD' || e.target.tagName === 'TH') {
        return;
      }
      e.stopPropagation();
      selectElement(id);
    });

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Add to slide
    slide.appendChild(container);

    // Register element
    const elementData = {
      id: id,
      type: 'table',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        rows: config.rows,
        cols: config.cols
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save
    triggerAutoSave(slideIndex);

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Generate HTML table markup
   */
  function generateTableHTML(rows, cols, data, style) {
    const headerBg = style.headerBackground || '#1e40af';
    const headerColor = style.headerTextColor || '#ffffff';
    const borderColor = style.borderColor || '#e5e7eb';
    const cellBg = style.cellBackground || '#ffffff';
    const altBg = style.alternateBackground || '#f9fafb';

    let html = `<table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif;font-size:16px;">`;

    for (let r = 0; r < rows; r++) {
      html += '<tr>';
      const isHeader = r === 0 && style.headerRow !== false;
      const tag = isHeader ? 'th' : 'td';
      const bg = isHeader ? headerBg : (r % 2 === 0 ? cellBg : altBg);
      const color = isHeader ? headerColor : 'inherit';

      for (let c = 0; c < cols; c++) {
        const cellData = data[r]?.[c] || '';
        html += `<${tag} contenteditable="true"
                  style="background:${bg};color:${color};padding:12px 16px;
                         border:1px solid ${borderColor};
                         font-weight:${isHeader ? '600' : '400'};">
                  ${cellData}
                </${tag}>`;
      }
      html += '</tr>';
    }

    html += '</table>';
    return html;
  }

  // ===== INSERT CHART =====

  /**
   * Insert a chart element into a slide
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Chart configuration
   * @param {string} [config.chartHtml] - Pre-formatted HTML from Analytics Service
   * @param {Object} [config.chartConfig] - Chart.js configuration
   * @param {Object} config.position - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @returns {Object} Result with elementId
   */
  function insertChart(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const id = generateId('chart');
    const position = config.position || { gridRow: '4/15', gridColumn: '3/30' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-chart';
    container.dataset.elementType = 'chart';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: ${++zIndexCounter};
      background: white;
      border-radius: 8px;
      padding: 16px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow: visible;
      cursor: ${config.draggable !== false ? 'move' : 'default'};
    `;

    // Use provided HTML or create chart from config
    if (config.chartHtml) {
      container.innerHTML = config.chartHtml;
    } else if (config.chartConfig && typeof Chart !== 'undefined') {
      // Create canvas for Chart.js
      const canvas = document.createElement('canvas');
      canvas.id = `canvas-${id}`;
      canvas.style.cssText = 'width:100%;height:100%;';
      container.appendChild(canvas);

      // Initialize chart after container is in DOM
      setTimeout(() => {
        try {
          const chart = new Chart(canvas, {
            type: config.chartConfig.type || 'bar',
            data: config.chartConfig.data,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              ...config.chartConfig.options
            }
          });
          container.chartInstance = chart;
        } catch (error) {
          console.error('Chart creation failed:', error);
          container.innerHTML = `<div style="color:#6b7280;text-align:center;">Chart error: ${error.message}</div>`;
        }
      }, 0);
    } else {
      container.innerHTML = '<div style="color:#6b7280;text-align:center;">Chart placeholder</div>';
    }

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Add to slide
    slide.appendChild(container);

    // Register element
    const elementData = {
      id: id,
      type: 'chart',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        chartType: config.chartConfig?.type || 'custom'
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save
    triggerAutoSave(slideIndex);

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  // ===== INSERT IMAGE =====

  /**
   * Insert an image element into a slide
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Image configuration
   * @param {string} config.imageUrl - Image URL
   * @param {string} [config.alt] - Alt text
   * @param {string} [config.objectFit] - CSS object-fit: cover|contain|fill
   * @param {Object} config.position - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @returns {Object} Result with elementId
   */
  function insertImage(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    if (!config.imageUrl) {
      return { success: false, error: 'imageUrl is required' };
    }

    const id = generateId('image');
    const position = config.position || { gridRow: '4/14', gridColumn: '3/20' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-image';
    container.dataset.elementType = 'image';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${++zIndexCounter};
      overflow: hidden;
      border-radius: 8px;
      cursor: ${config.draggable !== false ? 'move' : 'default'};
    `;

    // Create image
    const img = document.createElement('img');
    img.src = config.imageUrl;
    img.alt = config.alt || '';
    img.style.cssText = `
      width: 100%;
      height: 100%;
      object-fit: ${config.objectFit || 'cover'};
    `;

    // Handle load errors
    img.onerror = () => {
      container.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;
                                        width:100%;height:100%;background:#f3f4f6;color:#6b7280;">
        Image unavailable
      </div>`;
    };

    container.appendChild(img);

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Add to slide
    slide.appendChild(container);

    // Register element
    const elementData = {
      id: id,
      type: 'image',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        imageUrl: config.imageUrl,
        alt: config.alt,
        objectFit: config.objectFit
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save
    triggerAutoSave(slideIndex);

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  // ===== INSERT TEXT BOX =====

  /**
   * Z-index counter specifically for text boxes (elevated above other elements)
   */
  let textBoxZIndexCounter = 1000;

  /**
   * Insert a text box element into a slide
   *
   * Text boxes are overlay elements with elevated z-index (1000+)
   * that support rich text editing via contentEditable.
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Text box configuration
   * @param {Object} config.position - Grid position {gridRow, gridColumn}
   * @param {string} [config.content] - Initial HTML content
   * @param {Object} [config.style] - Styling options
   * @param {string} [config.placeholder] - Placeholder text
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @param {boolean} [config.resizable=true] - Enable resize handles
   * @returns {Object} Result with elementId
   */
  function insertTextBox(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const id = generateId('textbox');
    const position = config.position || { gridRow: '6/12', gridColumn: '5/28' };
    const style = config.style || {};

    // Text boxes use elevated z-index
    const zIndex = config.zIndex || (++textBoxZIndexCounter);

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-textbox';
    container.dataset.elementType = 'textbox';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${zIndex};
      background: ${style.backgroundColor || style.background_color || 'transparent'};
      border: ${style.borderWidth || style.border_width || 0}px solid ${style.borderColor || style.border_color || 'transparent'};
      border-radius: ${style.borderRadius || style.border_radius || 0}px;
      padding: ${style.padding || 16}px;
      opacity: ${style.opacity || 1};
      box-shadow: ${style.boxShadow || style.box_shadow || 'none'};
      min-height: 60px;
      overflow: auto;
      cursor: ${config.draggable !== false ? 'move' : 'text'};
      position: relative;
    `;

    // Create centered drag handle pill at top (NOT contentEditable, so it can be dragged)
    // Styles are primarily in textbox.css - minimal inline styles here
    const dragHandle = document.createElement('div');
    dragHandle.className = 'textbox-drag-handle';
    // Add grip icon (6 dots pattern)
    dragHandle.innerHTML = '<span style="color: white; font-size: 14px; line-height: 1; letter-spacing: 3px;">⋮⋮</span>';

    // Create editable content area
    const contentDiv = document.createElement('div');
    contentDiv.className = 'textbox-content';
    contentDiv.contentEditable = 'true';
    contentDiv.dataset.placeholder = config.placeholder || 'Click to add text...';
    contentDiv.innerHTML = config.content || '';
    contentDiv.style.cssText = `
      width: 100%;
      min-height: 100%;
      outline: none;
      cursor: text;
      font-family: Inter, system-ui, -apple-system, sans-serif;
      font-size: 32px;
      line-height: 1.5;
      color: #1f2937;
    `;

    // Handle input for auto-save
    contentDiv.addEventListener('input', () => {
      triggerAutoSave(slideIndex);
    });

    // Prevent drag when clicking on text content (but allow on drag handle)
    contentDiv.addEventListener('mousedown', (e) => {
      e.stopPropagation();
    });

    // Focus handling
    contentDiv.addEventListener('focus', () => {
      container.classList.add('textbox-editing');
    });
    contentDiv.addEventListener('blur', () => {
      container.classList.remove('textbox-editing');
    });

    container.appendChild(dragHandle);
    container.appendChild(contentDiv);

    // Add click handler for selection (on container border/padding)
    container.addEventListener('click', (e) => {
      if (e.target === container) {
        e.stopPropagation();
        selectElement(id);
      }
    });

    // Add to slide FIRST (element must be in DOM before makeDraggable/makeResizable)
    slide.appendChild(container);

    // Enable drag-drop on container (AFTER element is in DOM)
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Enable resize if available and requested (AFTER element is in DOM)
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id);
    }

    // Register element
    const elementData = {
      id: id,
      type: 'textbox',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndex,
      selected: false,
      data: {
        content: config.content || '',
        style: style,
        placeholder: config.placeholder
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save
    triggerAutoSave(slideIndex);

    return {
      success: true,
      elementId: id,
      position: position,
      zIndex: zIndex
    };
  }

  /**
   * Update text box content
   *
   * @param {string} elementId - Text box ID
   * @param {string} content - New HTML content
   * @param {boolean} [animate=false] - Animate the change
   */
  function updateTextBoxContent(elementId, content, animate = false) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'textbox') {
      return { success: false, error: 'Text box not found' };
    }

    const contentDiv = element.querySelector('.textbox-content');
    if (contentDiv) {
      if (animate) {
        contentDiv.style.transition = 'opacity 0.2s';
        contentDiv.style.opacity = '0';
        setTimeout(() => {
          contentDiv.innerHTML = content;
          contentDiv.style.opacity = '1';
        }, 200);
      } else {
        contentDiv.innerHTML = content;
      }
      data.data.content = content;
      triggerAutoSave(data.slideIndex);
    }

    return { success: true };
  }

  /**
   * Update text box style
   *
   * @param {string} elementId - Text box ID
   * @param {Object} style - Style updates
   */
  function updateTextBoxStyle(elementId, style) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'textbox') {
      return { success: false, error: 'Text box not found' };
    }

    // Apply style updates
    if (style.backgroundColor || style.background_color) {
      element.style.background = style.backgroundColor || style.background_color;
    }
    if (style.borderColor || style.border_color) {
      element.style.borderColor = style.borderColor || style.border_color;
    }
    if (style.borderWidth !== undefined || style.border_width !== undefined) {
      element.style.borderWidth = (style.borderWidth || style.border_width || 0) + 'px';
    }
    if (style.borderRadius !== undefined || style.border_radius !== undefined) {
      element.style.borderRadius = (style.borderRadius || style.border_radius || 0) + 'px';
    }
    if (style.padding !== undefined) {
      element.style.padding = style.padding + 'px';
    }
    if (style.opacity !== undefined) {
      element.style.opacity = style.opacity;
    }
    if (style.boxShadow || style.box_shadow) {
      element.style.boxShadow = style.boxShadow || style.box_shadow;
    }

    // Update registry
    data.data.style = { ...data.data.style, ...style };
    triggerAutoSave(data.slideIndex);

    return { success: true };
  }

  /**
   * Get text box content
   *
   * @param {string} elementId - Text box ID
   * @returns {Object} Content and plain text
   */
  function getTextBoxContent(elementId) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'textbox') {
      return { success: false, error: 'Text box not found' };
    }

    const contentDiv = element.querySelector('.textbox-content');
    const htmlContent = contentDiv ? contentDiv.innerHTML : '';
    const plainText = contentDiv ? contentDiv.textContent : '';

    return {
      success: true,
      elementId: elementId,
      content: htmlContent,
      plainText: plainText
    };
  }

  // ===== ELEMENT SELECTION =====

  /**
   * Select an element
   *
   * @param {string} elementId - Element to select
   */
  function selectElement(elementId) {
    // Deselect previous
    deselectAll();

    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (element && data) {
      element.classList.add('element-selected');
      data.selected = true;
      selectedElementId = elementId;

      // Notify about selection change
      if (typeof window.onElementSelected === 'function') {
        window.onElementSelected(data);
      }
    }
  }

  /**
   * Deselect all elements
   */
  function deselectAll() {
    if (selectedElementId) {
      const element = document.getElementById(selectedElementId);
      const data = elementRegistry.get(selectedElementId);

      if (element) {
        element.classList.remove('element-selected');
      }
      if (data) {
        data.selected = false;
      }
    }
    selectedElementId = null;
  }

  /**
   * Get currently selected element
   *
   * @returns {Object|null} Element data or null
   */
  function getSelectedElement() {
    if (!selectedElementId) return null;
    return elementRegistry.get(selectedElementId) || null;
  }

  // ===== ELEMENT QUERIES =====

  /**
   * Get element by ID
   *
   * @param {string} elementId - Element ID
   * @returns {Object|null} Element data
   */
  function getElementById(elementId) {
    return elementRegistry.get(elementId) || null;
  }

  /**
   * Get all elements on a slide
   *
   * @param {number} slideIndex - Slide index
   * @returns {Array} Array of element data
   */
  function getElementsBySlide(slideIndex) {
    const elements = [];
    elementRegistry.forEach((data) => {
      if (data.slideIndex === slideIndex) {
        elements.push(data);
      }
    });
    return elements;
  }

  // ===== ELEMENT MODIFICATION =====

  /**
   * Update element position
   *
   * @param {string} elementId - Element ID
   * @param {Object} position - New position {gridRow, gridColumn}
   */
  function updatePosition(elementId, position) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (element && data) {
      element.style.gridRow = position.gridRow;
      element.style.gridColumn = position.gridColumn;
      data.position = position;
      triggerAutoSave(data.slideIndex);
    }
  }

  /**
   * Delete an element
   *
   * @param {string} elementId - Element to delete
   * @returns {Object} Result
   */
  function deleteElement(elementId) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data) {
      return { success: false, error: 'Element not found' };
    }

    // Deselect if selected
    if (selectedElementId === elementId) {
      deselectAll();
    }

    // Remove from DOM
    element.remove();

    // Remove from registry
    elementRegistry.delete(elementId);

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);

    return { success: true };
  }

  /**
   * Bring element to front (highest z-index)
   *
   * @param {string} elementId - Element ID
   */
  function bringToFront(elementId) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (element && data) {
      const newZ = ++zIndexCounter;
      element.style.zIndex = newZ;
      data.zIndex = newZ;
    }
  }

  /**
   * Send element to back (lowest z-index)
   *
   * @param {string} elementId - Element ID
   */
  function sendToBack(elementId) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (element && data) {
      // Find lowest z-index
      let minZ = 100;
      elementRegistry.forEach((d) => {
        if (d.zIndex < minZ) minZ = d.zIndex;
      });

      const newZ = minZ - 1;
      element.style.zIndex = newZ;
      data.zIndex = newZ;
    }
  }

  // ===== HELPERS =====

  /**
   * Get slide element by index
   *
   * @param {number} slideIndex - Slide index
   * @returns {Element|null} Slide element
   */
  function getSlideElement(slideIndex) {
    const slides = document.querySelectorAll('.reveal .slides > section');
    return slides[slideIndex] || null;
  }

  /**
   * Trigger auto-save
   *
   * @param {number} slideIndex - Slide that changed
   */
  function triggerAutoSave(slideIndex) {
    if (typeof markContentChanged === 'function') {
      markContentChanged(slideIndex, 'element');
    }
  }

  // ===== GLOBAL CLICK HANDLER =====

  // Deselect elements when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.dynamic-element')) {
      deselectAll();
    }
  });

  // ===== EXPOSE API =====

  window.ElementManager = {
    // Insert methods
    insertShape: insertShape,
    insertTable: insertTable,
    insertChart: insertChart,
    insertImage: insertImage,
    insertTextBox: insertTextBox,

    // Query methods
    getElementById: getElementById,
    getElementsBySlide: getElementsBySlide,
    getSelectedElement: getSelectedElement,

    // Selection methods
    selectElement: selectElement,
    deselectAll: deselectAll,

    // Modification methods
    updatePosition: updatePosition,
    deleteElement: deleteElement,
    bringToFront: bringToFront,
    sendToBack: sendToBack,

    // Text box specific methods
    updateTextBoxContent: updateTextBoxContent,
    updateTextBoxStyle: updateTextBoxStyle,
    getTextBoxContent: getTextBoxContent,

    // Registry access (for debugging)
    _registry: elementRegistry
  };

  console.log('ElementManager initialized');

})();
