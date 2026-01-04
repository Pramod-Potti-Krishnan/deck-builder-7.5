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

  // ===== PROPERTY HELPERS =====

  /**
   * Map vertical align value to flexbox justifyContent
   * @param {string} value - 'top', 'middle', 'bottom'
   * @returns {string} Flexbox justify-content value
   */
  function mapVerticalAlign(value) {
    const map = {
      'top': 'flex-start',
      'middle': 'center',
      'bottom': 'flex-end'
    };
    return map[value] || 'flex-start';
  }

  /**
   * Reverse map justifyContent to vertical align value
   * @param {string} value - Flexbox justify-content value
   * @returns {string} Vertical align: 'top', 'middle', or 'bottom'
   */
  function reverseMapVerticalAlign(value) {
    const map = {
      'flex-start': 'top',
      'center': 'middle',
      'flex-end': 'bottom',
      'start': 'top',
      'end': 'bottom'
    };
    return map[value] || 'top';
  }

  /**
   * Parse padding value - supports shorthand like "25px 0px" or "10px 20px 10px 20px"
   * @param {string|number} padding - Padding value
   * @returns {string} CSS padding string
   */
  function parsePadding(padding) {
    if (typeof padding === 'number') return `${padding}px`;
    if (typeof padding === 'string') {
      // If it already has 'px' or other units, return as-is
      if (padding.includes('px') || padding.includes('em') || padding.includes('%')) {
        return padding;
      }
      // Otherwise treat as number
      return `${parseInt(padding) || 0}px`;
    }
    return '0px';
  }

  /**
   * Parse border shorthand - supports "1px solid #ddd" or separate properties
   * @param {string|Object} border - Border value or object
   * @returns {Object|null} Parsed border object or null if shorthand
   */
  function parseBorder(border) {
    if (typeof border === 'string') {
      // Shorthand format: "1px solid #ddd" or "2px dashed red"
      const match = border.match(/^(\d+(?:px)?)\s+(solid|dashed|dotted|double|none)\s+(.+)$/i);
      if (match) {
        return {
          shorthand: border,
          width: parseInt(match[1]) || 0,
          style: match[2].toLowerCase(),
          color: match[3]
        };
      }
    }
    return null;  // Use separate borderWidth/borderColor instead
  }

  /**
   * Format border shorthand from computed styles
   * @param {CSSStyleDeclaration} style - Computed style
   * @returns {string|null} Border shorthand or null
   */
  function formatBorderShorthand(style) {
    const width = parseInt(style.borderWidth) || parseInt(style.borderTopWidth) || 0;
    const styleVal = style.borderStyle || style.borderTopStyle || 'none';
    const color = style.borderColor || style.borderTopColor || 'transparent';

    if (width > 0 && styleVal !== 'none') {
      return `${width}px ${styleVal} ${color}`;
    }
    return null;
  }

  // ===== SCRIPT EXECUTION HELPER =====

  /**
   * Execute scripts sequentially, waiting for external scripts to load
   *
   * v7.5.4: Fix for chart edit button not working in C3/V2 templates
   * Problem: When using innerHTML to insert chart_html, scripts don't execute automatically.
   * The previous fix (v7.5.3) re-created script elements, but external scripts (with src attribute)
   * load asynchronously. This caused the editor function definition script to execute before
   * the external editor library finished loading.
   *
   * Solution: Execute scripts in order, using async/await to wait for external scripts to load
   * before continuing to the next script.
   *
   * @param {HTMLElement} contentDiv - Container element with scripts to execute
   * @returns {Promise<void>} Resolves when all scripts have executed
   */
  async function executeScriptsSequentially(contentDiv) {
    const scripts = Array.from(contentDiv.querySelectorAll('script'));
    let externalCount = 0;
    let inlineCount = 0;

    for (const oldScript of scripts) {
      const newScript = document.createElement('script');

      // Copy all attributes (src, type, async, defer, etc.)
      Array.from(oldScript.attributes).forEach(attr => {
        newScript.setAttribute(attr.name, attr.value);
      });

      if (oldScript.src) {
        // External script - wait for load before continuing
        externalCount++;
        await new Promise((resolve, reject) => {
          newScript.onload = () => {
            console.log(`[ElementManager] External script loaded: ${oldScript.src.split('/').pop()}`);
            resolve();
          };
          newScript.onerror = (err) => {
            console.error(`[ElementManager] External script failed to load: ${oldScript.src}`);
            // Resolve anyway to continue with other scripts (don't break the chain)
            resolve();
          };
          oldScript.parentNode.replaceChild(newScript, oldScript);
        });
      } else {
        // Inline script - copy content and execute immediately
        inlineCount++;
        newScript.textContent = oldScript.textContent;
        oldScript.parentNode.replaceChild(newScript, oldScript);
      }
    }

    console.log(`[ElementManager] Scripts executed sequentially (${inlineCount} inline, ${externalCount} external)`);
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

    const id = config.id || generateId('shape');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    // Using document.getElementById() could find elements in adjacent slides
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      // Since we're only searching within THIS slide, if found it's definitely on the correct slide
      console.log(`[ElementManager] Shape ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

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
    emitSlideContentChanged(slideIndex, 'add', 'shape');

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

    const id = config.id || generateId('table');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] Table ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    const position = config.position || { gridRow: '5/18', gridColumn: '2/32' };

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
    emitSlideContentChanged(slideIndex, 'add', 'table');

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
   * Supports two modes:
   * 1. Placeholder mode (no chartHtml/chartConfig) - Shows chart placeholder UI
   * 2. Content mode (chartHtml or chartConfig provided) - Shows actual chart
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Chart configuration
   * @param {string} [config.chartHtml] - Pre-formatted HTML from Analytics Service
   * @param {Object} [config.chartConfig] - Chart.js configuration
   * @param {Object} [config.position] - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @param {boolean} [config.resizable=true] - Enable resize handles
   * @param {string} [config.id] - Existing ID (for restoration)
   * @returns {Object} Result with elementId
   */
  function insertChart(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const isPlaceholderMode = !config.chartHtml && !config.chartConfig;
    const id = config.id || generateId('chart');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] Chart ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    const position = config.position || { gridRow: '5/18', gridColumn: '2/32' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = `dynamic-element inserted-element-placeholder inserted-chart${isPlaceholderMode ? ' placeholder-mode' : ''}`;
    container.dataset.elementType = 'chart';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${++zIndexCounter};
    `;

    if (isPlaceholderMode) {
      // Placeholder mode - show chart placeholder UI
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-placeholder-content">
          <div class="element-placeholder-icon">
            <svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="12" y="52" width="22" height="28" rx="2" fill="currentColor"/>
              <rect x="38" y="28" width="22" height="52" rx="2" fill="currentColor"/>
              <rect x="64" y="38" width="22" height="42" rx="2" fill="currentColor"/>
              <rect x="90" y="18" width="22" height="62" rx="2" fill="currentColor"/>
              <line x1="8" y1="82" x2="116" y2="82" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="element-placeholder-dots">
            <span></span><span></span><span></span>
          </div>
          <span class="element-placeholder-text">Generate chart...</span>
        </div>
        <button class="element-delete-button">×</button>
        <div class="element-type-badge">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 3v18h18" stroke="currentColor" stroke-width="2"/>
            <rect x="7" y="10" width="3" height="8" fill="currentColor"/>
            <rect x="12" y="6" width="3" height="12" fill="currentColor"/>
            <rect x="17" y="12" width="3" height="6" fill="currentColor"/>
          </svg>
        </div>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    } else {
      // Content mode - show actual chart
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-content"></div>
        <button class="element-delete-button">×</button>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      const contentDiv = container.querySelector('.element-content');

      if (config.chartHtml) {
        // v7.5.4: Execute embedded scripts from chart_html sequentially
        // This replaces the v7.5.3 fix which didn't wait for external scripts to load.
        // External scripts (like chart-spreadsheet-editor.js) must finish loading before
        // the editor function definition script runs, otherwise openChartEditor() is undefined.
        contentDiv.innerHTML = config.chartHtml;

        // Execute scripts in order, waiting for external scripts to load
        executeScriptsSequentially(contentDiv).catch(err => {
          console.error('[ElementManager] Script execution error:', err);
        });
      } else if (config.chartConfig && typeof Chart !== 'undefined') {
        // Create canvas for Chart.js
        const canvas = document.createElement('canvas');
        canvas.id = `canvas-${id}`;
        canvas.style.cssText = 'width:100%;height:100%;';
        contentDiv.appendChild(canvas);

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
            contentDiv.innerHTML = `<div style="color:#6b7280;text-align:center;">Chart error: ${error.message}</div>`;
          }
        }, 0);
      }

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    }

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Add to slide FIRST (element must be in DOM before makeDraggable/makeResizable)
    slide.appendChild(container);

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Enable resize if available and requested
    // Charts have minimum size of 4 columns × 3 rows
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id, { minCols: 4, minRows: 3 });
    }

    // Apply locked state if specified
    if (config.locked) {
      container.classList.add('element-locked');
    }

    // Apply hidden state if specified
    if (config.visible === false) {
      container.classList.add('element-hidden');
    }

    // Register element
    const elementData = {
      id: id,
      type: 'chart',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        chartType: config.chartConfig?.type || null,
        chartConfig: config.chartConfig || null,
        chartHtml: config.chartHtml || null,
        locked: config.locked || false,
        visible: config.visible !== false
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save only for NEW elements (not restoration)
    if (!config.id) {
      triggerAutoSave(slideIndex);
      emitSlideContentChanged(slideIndex, 'add', 'chart');
    }

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Update chart content
   *
   * @param {string} elementId - Chart element ID
   * @param {Object} chartConfig - Chart.js configuration
   * @param {Object} [metadata] - Chart metadata from AI service (optional)
   * @param {Object} [insights] - AI-generated insights (optional)
   * @returns {Object} Result
   */
  function updateChartConfig(elementId, chartConfig, metadata, insights) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'chart') {
      return { success: false, error: 'Chart element not found' };
    }

    // Remove placeholder mode
    element.classList.remove('placeholder-mode');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Destroy existing chart instance
    if (element.chartInstance) {
      element.chartInstance.destroy();
    }

    // Store metadata and insights in element dataset (for persistence and access)
    if (metadata) {
      element.dataset.chartMetadata = JSON.stringify(metadata);
      data.data.metadata = metadata;
    }
    if (insights) {
      element.dataset.chartInsights = JSON.stringify(insights);
      data.data.insights = insights;
    }

    // Create new chart
    let chartCreated = false;
    if (typeof Chart !== 'undefined') {
      const canvas = document.createElement('canvas');
      canvas.id = `canvas-${elementId}`;
      canvas.style.cssText = 'width:100%;height:100%;';
      contentDiv.innerHTML = '';
      contentDiv.appendChild(canvas);

      setTimeout(() => {
        try {
          const chart = new Chart(canvas, {
            type: chartConfig.type || 'bar',
            data: chartConfig.data,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              ...chartConfig.options
            }
          });
          element.chartInstance = chart;
          chartCreated = true;

          // Emit chartRendered event to parent (for frontend to know chart is ready)
          if (window.parent && window.parent !== window) {
            window.parent.postMessage({
              type: 'chartRendered',
              elementId: elementId,
              success: true,
              metadata: metadata || null,
              insights: insights || null
            }, '*');
            console.log('📤 postMessage: chartRendered', elementId);
          }
        } catch (error) {
          console.error('Chart update failed:', error);
          contentDiv.innerHTML = `<div style="color:#6b7280;text-align:center;">Chart error: ${error.message}</div>`;

          // Emit error event to parent
          if (window.parent && window.parent !== window) {
            window.parent.postMessage({
              type: 'chartRendered',
              elementId: elementId,
              success: false,
              error: error.message
            }, '*');
          }
        }
      }, 0);
    }

    // Update registry
    data.data.chartConfig = chartConfig;
    data.data.chartType = chartConfig.type || null;

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);
    emitSlideContentChanged(data.slideIndex, 'modify', 'chart');

    return { success: true };
  }

  /**
   * Set chart HTML content directly
   *
   * @param {string} elementId - Chart element ID
   * @param {string} chartHtml - HTML content for chart
   * @returns {Object} Result
   */
  function setChartHtml(elementId, chartHtml) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'chart') {
      return { success: false, error: 'Chart element not found' };
    }

    // Remove placeholder mode
    element.classList.remove('placeholder-mode');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Destroy existing chart instance
    if (element.chartInstance) {
      element.chartInstance.destroy();
      element.chartInstance = null;
    }

    // v7.5.4: Set HTML content and execute scripts sequentially
    contentDiv.innerHTML = chartHtml;

    // Execute scripts in order, waiting for external scripts to load
    executeScriptsSequentially(contentDiv).catch(err => {
      console.error('[ElementManager] Script execution error in setChartHtml:', err);
    });

    // Update registry
    data.data.chartHtml = chartHtml;

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);
    emitSlideContentChanged(data.slideIndex, 'modify', 'chart');

    return { success: true };
  }

  // ===== INSERT IMAGE =====

  /**
   * Insert an image element into a slide
   *
   * Supports two modes:
   * 1. Placeholder mode (no imageUrl) - Shows "Drag images here." UI
   * 2. Content mode (imageUrl provided) - Shows actual image
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Image configuration
   * @param {string} [config.imageUrl] - Image URL (optional - shows placeholder if not provided)
   * @param {string} [config.alt] - Alt text
   * @param {string} [config.objectFit] - CSS object-fit: cover|contain|fill
   * @param {Object} [config.position] - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @param {boolean} [config.resizable=true] - Enable resize handles
   * @param {string} [config.id] - Existing ID (for restoration)
   * @returns {Object} Result with elementId
   */
  function insertImage(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const isPlaceholderMode = !config.imageUrl;
    const id = config.id || generateId('image');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] Image ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    const position = config.position || { gridRow: '5/18', gridColumn: '2/32' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = `dynamic-element inserted-element-placeholder inserted-image${isPlaceholderMode ? ' placeholder-mode' : ''}`;
    container.dataset.elementType = 'image';
    container.dataset.slideIndex = slideIndex;

    // Add slot-specific class for compact styling (logo uses smaller placeholder)
    if (config.slotName === 'logo' || config.slot_name === 'logo') {
      container.classList.add('slot-logo');
    }
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${++zIndexCounter};
    `;

    if (isPlaceholderMode) {
      // Placeholder mode - show drag images UI
      // Support custom placeholder text and color for different slot types
      const placeholderText = config.placeholderText || 'Generate image...';

      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-placeholder-content">
          <div class="element-placeholder-icon">
            <svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="8" width="104" height="74" rx="6" stroke="currentColor" stroke-width="4" fill="none"/>
              <circle cx="35" cy="32" r="12" fill="currentColor"/>
              <path d="M12 68 L42 48 L62 58 L108 28" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="element-placeholder-dots">
            <span></span><span></span><span></span>
          </div>
          <span class="element-placeholder-text">${placeholderText}</span>
        </div>
        <button class="element-delete-button">×</button>
        <div class="element-type-badge">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
            <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>
            <path d="M21 15l-5-5L5 21" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Apply custom placeholder background color if specified
      if (config.placeholderColor) {
        container.style.backgroundColor = config.placeholderColor;
      }

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    } else {
      // Content mode - show actual image
      // Check if I-series layout - use no border-radius for edge-to-edge images
      const layoutAttr = slide.dataset?.layout || slide.closest('[data-layout]')?.dataset?.layout || '';
      const isISeriesLayout = /^I[1-4]-/.test(layoutAttr);
      const borderRadius = isISeriesLayout ? '0' : '6px';
      // I-series layouts use 'fill' to stretch image to complete grid cell
      const objectFit = isISeriesLayout ? 'fill' : (config.objectFit || 'cover');

      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-content">
          <img src="${config.imageUrl}" alt="${config.alt || ''}" style="width:100%;height:100%;object-fit:${objectFit};border-radius:${borderRadius};">
        </div>
        <button class="element-delete-button">×</button>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Handle load errors
      const img = container.querySelector('img');
      if (img) {
        img.onerror = () => {
          const contentDiv = container.querySelector('.element-content');
          if (contentDiv) {
            contentDiv.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;
                                              width:100%;height:100%;background:#f3f4f6;color:#6b7280;">
              Image unavailable
            </div>`;
          }
        };
      }

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    }

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Add to slide FIRST (element must be in DOM before makeDraggable/makeResizable)
    slide.appendChild(container);

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Enable resize if available and requested
    // Images have minimum size of 2 columns × 2 rows
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id, { minCols: 2, minRows: 2 });
    }

    // Apply locked state if specified
    if (config.locked) {
      container.classList.add('element-locked');
    }

    // Apply hidden state if specified
    if (config.visible === false) {
      container.classList.add('element-hidden');
    }

    // Register element
    const elementData = {
      id: id,
      type: 'image',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        imageUrl: config.imageUrl || null,
        alt: config.alt || null,
        objectFit: config.objectFit || 'cover',
        locked: config.locked || false,
        visible: config.visible !== false
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save only for NEW elements (not restoration)
    if (!config.id) {
      triggerAutoSave(slideIndex);
      emitSlideContentChanged(slideIndex, 'add', 'image');
    }

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Update image source
   *
   * @param {string} elementId - Image element ID
   * @param {string} imageUrl - New image URL
   * @param {string} [alt] - Alt text
   * @returns {Object} Result
   */
  function updateImageSource(elementId, imageUrl, alt) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'image') {
      return { success: false, error: 'Image element not found' };
    }

    // Remove placeholder mode
    element.classList.remove('placeholder-mode');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      // Create content div if it doesn't exist
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      // Insert after drag handle
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Set new image
    // Check if I-series layout for object-fit and border-radius
    const slide = element.closest('section[data-layout]');
    const layoutAttr = slide?.dataset?.layout || '';
    const isISeriesLayout = /^I[1-4]-/.test(layoutAttr);
    const objectFit = isISeriesLayout ? 'fill' : (data.data.objectFit || 'cover');
    const borderRadius = isISeriesLayout ? '0' : '6px';
    contentDiv.innerHTML = `<img src="${imageUrl}" alt="${alt || ''}" style="width:100%;height:100%;object-fit:${objectFit};border-radius:${borderRadius};">`;

    // Update registry
    data.data.imageUrl = imageUrl;
    data.data.alt = alt || null;

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);
    emitSlideContentChanged(data.slideIndex, 'modify', 'image');

    return { success: true };
  }

  // ===== INSERT INFOGRAPHIC =====

  /**
   * Insert an infographic element into a slide
   *
   * Supports two modes:
   * 1. Placeholder mode (no svgContent) - Shows infographic placeholder UI
   * 2. Content mode (svgContent provided) - Shows actual infographic
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Infographic configuration
   * @param {string} [config.svgContent] - SVG content (optional - shows placeholder if not provided)
   * @param {string} [config.infographicType] - Type: timeline, process, comparison, etc.
   * @param {Array} [config.items] - Data items for the infographic
   * @param {Object} [config.position] - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @param {boolean} [config.resizable=true] - Enable resize handles
   * @param {string} [config.id] - Existing ID (for restoration)
   * @returns {Object} Result with elementId
   */
  function insertInfographic(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const isPlaceholderMode = !config.svgContent;
    const id = config.id || generateId('infographic');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] Infographic ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    const position = config.position || { gridRow: '5/18', gridColumn: '2/32' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = `dynamic-element inserted-element-placeholder inserted-infographic${isPlaceholderMode ? ' placeholder-mode' : ''}`;
    container.dataset.elementType = 'infographic';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${++zIndexCounter};
    `;

    if (isPlaceholderMode) {
      // Placeholder mode - show infographic placeholder UI
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-placeholder-content">
          <div class="element-placeholder-icon">
            <svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="18" cy="22" r="9" fill="currentColor"/>
              <rect x="32" y="14" width="78" height="16" rx="8" fill="currentColor"/>
              <circle cx="18" cy="45" r="9" fill="currentColor"/>
              <rect x="32" y="37" width="78" height="16" rx="8" fill="currentColor"/>
              <circle cx="18" cy="68" r="9" fill="currentColor"/>
              <rect x="32" y="60" width="78" height="16" rx="8" fill="currentColor"/>
            </svg>
          </div>
          <div class="element-placeholder-dots">
            <span></span><span></span><span></span>
          </div>
          <span class="element-placeholder-text">Generate infographic...</span>
        </div>
        <button class="element-delete-button">×</button>
        <div class="element-type-badge">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="6" cy="6" r="2" fill="currentColor"/>
            <rect x="10" y="4" width="10" height="4" rx="2" fill="currentColor"/>
            <circle cx="6" cy="12" r="2" fill="currentColor"/>
            <rect x="10" y="10" width="10" height="4" rx="2" fill="currentColor"/>
            <circle cx="6" cy="18" r="2" fill="currentColor"/>
            <rect x="10" y="16" width="10" height="4" rx="2" fill="currentColor"/>
          </svg>
        </div>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    } else {
      // Content mode - show actual infographic
      container.classList.remove('inserted-element-placeholder');
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-content">${config.svgContent}</div>
        <button class="element-delete-button">×</button>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    }

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Add to slide FIRST (element must be in DOM before makeDraggable/makeResizable)
    slide.appendChild(container);

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Enable resize if available and requested
    // Infographics have minimum size of 3 columns × 3 rows
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id, { minCols: 3, minRows: 3 });
    }

    // Apply locked state if specified
    if (config.locked) {
      container.classList.add('element-locked');
    }

    // Apply hidden state if specified
    if (config.visible === false) {
      container.classList.add('element-hidden');
    }

    // Register element
    const elementData = {
      id: id,
      type: 'infographic',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        svgContent: config.svgContent || null,
        infographicType: config.infographicType || null,
        items: config.items || null,
        locked: config.locked || false,
        visible: config.visible !== false
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save only for NEW elements (not restoration)
    if (!config.id) {
      triggerAutoSave(slideIndex);
      emitSlideContentChanged(slideIndex, 'add', 'infographic');
    }

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Update infographic content
   *
   * @param {string} elementId - Infographic element ID
   * @param {string} svgContent - SVG content
   * @returns {Object} Result
   */
  function updateInfographicContent(elementId, svgContent) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'infographic') {
      return { success: false, error: 'Infographic element not found' };
    }

    // Remove placeholder styling
    element.classList.remove('inserted-element-placeholder');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Set SVG content
    contentDiv.innerHTML = svgContent;

    // Update registry
    data.data.svgContent = svgContent;

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);
    emitSlideContentChanged(data.slideIndex, 'modify', 'infographic');

    return { success: true };
  }

  // ===== INSERT DIAGRAM =====

  /**
   * Insert a diagram element into a slide
   *
   * Supports two modes:
   * 1. Placeholder mode (no svgContent/mermaidCode) - Shows diagram placeholder UI
   * 2. Content mode (svgContent or mermaidCode provided) - Shows actual diagram
   *
   * @param {number} slideIndex - Target slide (0-based)
   * @param {Object} config - Diagram configuration
   * @param {string} [config.svgContent] - Pre-rendered SVG content
   * @param {string} [config.mermaidCode] - Mermaid.js diagram code
   * @param {string} [config.diagramType] - Type: flowchart, sequence, class, etc.
   * @param {string} [config.direction] - Layout direction: TB, LR, BT, RL
   * @param {string} [config.theme] - Theme: default, dark, forest, neutral
   * @param {Object} [config.position] - Grid position {gridRow, gridColumn}
   * @param {boolean} [config.draggable=true] - Enable drag-drop
   * @param {boolean} [config.resizable=true] - Enable resize handles
   * @param {string} [config.id] - Existing ID (for restoration)
   * @returns {Object} Result with elementId
   */
  function insertDiagram(slideIndex, config) {
    const slide = getSlideElement(slideIndex);
    if (!slide) {
      return { success: false, error: `Slide ${slideIndex} not found` };
    }

    const isPlaceholderMode = !config.svgContent && !config.mermaidCode;
    const id = config.id || generateId('diagram');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] Diagram ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    const position = config.position || { gridRow: '5/18', gridColumn: '2/32' };

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = `dynamic-element inserted-element-placeholder inserted-diagram${isPlaceholderMode ? ' placeholder-mode' : ''}`;
    container.dataset.elementType = 'diagram';
    container.dataset.slideIndex = slideIndex;
    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${++zIndexCounter};
    `;

    if (isPlaceholderMode) {
      // Placeholder mode - show diagram placeholder UI
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-placeholder-content">
          <div class="element-placeholder-icon">
            <svg viewBox="0 0 120 90" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="8" y="8" width="32" height="22" rx="4" stroke="currentColor" stroke-width="4" fill="none"/>
              <rect x="44" y="34" width="32" height="22" rx="4" stroke="currentColor" stroke-width="4" fill="none"/>
              <rect x="80" y="8" width="32" height="22" rx="4" stroke="currentColor" stroke-width="4" fill="none"/>
              <rect x="44" y="60" width="32" height="22" rx="4" stroke="currentColor" stroke-width="4" fill="none"/>
              <path d="M24 30 L24 45 L44 45" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M96 30 L96 45 L76 45" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M60 56 L60 60" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="element-placeholder-dots">
            <span></span><span></span><span></span>
          </div>
          <span class="element-placeholder-text">Generate diagram...</span>
        </div>
        <button class="element-delete-button">×</button>
        <div class="element-type-badge">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="9" y="10" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="15" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <rect x="9" y="17" width="6" height="4" rx="1" stroke="currentColor" stroke-width="1.5"/>
            <path d="M6 7v3h3M18 7v3h-3M12 14v3" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </div>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    } else {
      // Content mode - show actual diagram
      container.classList.remove('inserted-element-placeholder');
      container.innerHTML = `
        <div class="element-drag-handle"></div>
        <div class="element-content"></div>
        <button class="element-delete-button">×</button>
        <div class="resize-handle resize-handle-w"></div>
        <div class="resize-handle resize-handle-e"></div>
        <div class="resize-handle resize-handle-s"></div>
        <div class="resize-handle resize-handle-se"></div>
      `;

      const contentDiv = container.querySelector('.element-content');

      if (config.svgContent) {
        contentDiv.innerHTML = config.svgContent;
      } else if (config.mermaidCode && typeof mermaid !== 'undefined') {
        // Render Mermaid diagram
        const mermaidId = `mermaid-${id}`;
        contentDiv.innerHTML = `<div id="${mermaidId}">${config.mermaidCode}</div>`;
        setTimeout(async () => {
          try {
            const { svg } = await mermaid.render(mermaidId + '-svg', config.mermaidCode);
            contentDiv.innerHTML = svg;
          } catch (error) {
            console.error('Mermaid render failed:', error);
            contentDiv.innerHTML = `<div style="color:#6b7280;text-align:center;">Diagram error: ${error.message}</div>`;
          }
        }, 0);
      }

      // Add delete button handler
      const deleteBtn = container.querySelector('.element-delete-button');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          deleteElement(id);
        });
      }
    }

    // Add click handler for selection
    container.addEventListener('click', (e) => {
      e.stopPropagation();
      selectElement(id);
    });

    // Add to slide FIRST (element must be in DOM before makeDraggable/makeResizable)
    slide.appendChild(container);

    // Enable drag-drop
    if (config.draggable !== false && typeof window.DragDrop !== 'undefined') {
      window.DragDrop.makeDraggable(id);
    }

    // Enable resize if available and requested
    // Diagrams have minimum size of 4 columns × 3 rows
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id, { minCols: 4, minRows: 3 });
    }

    // Apply locked state if specified
    if (config.locked) {
      container.classList.add('element-locked');
    }

    // Apply hidden state if specified
    if (config.visible === false) {
      container.classList.add('element-hidden');
    }

    // Register element
    const elementData = {
      id: id,
      type: 'diagram',
      slideIndex: slideIndex,
      position: position,
      zIndex: zIndexCounter,
      selected: false,
      data: {
        svgContent: config.svgContent || null,
        mermaidCode: config.mermaidCode || null,
        diagramType: config.diagramType || null,
        direction: config.direction || 'TB',
        theme: config.theme || 'default',
        locked: config.locked || false,
        visible: config.visible !== false
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save only for NEW elements (not restoration)
    if (!config.id) {
      triggerAutoSave(slideIndex);
      emitSlideContentChanged(slideIndex, 'add', 'diagram');
    }

    return {
      success: true,
      elementId: id,
      position: position
    };
  }

  /**
   * Update diagram content with SVG
   *
   * @param {string} elementId - Diagram element ID
   * @param {string} svgContent - SVG content
   * @returns {Object} Result
   */
  function updateDiagramSvg(elementId, svgContent) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'diagram') {
      return { success: false, error: 'Diagram element not found' };
    }

    // Remove placeholder styling
    element.classList.remove('inserted-element-placeholder');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Set SVG content
    contentDiv.innerHTML = svgContent;

    // Update registry
    data.data.svgContent = svgContent;

    // Trigger auto-save
    triggerAutoSave(data.slideIndex);
    emitSlideContentChanged(data.slideIndex, 'modify', 'diagram');

    return { success: true };
  }

  /**
   * Update diagram content with Mermaid code
   *
   * @param {string} elementId - Diagram element ID
   * @param {string} mermaidCode - Mermaid.js diagram code
   * @returns {Object} Result
   */
  async function updateDiagramMermaid(elementId, mermaidCode) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data || data.type !== 'diagram') {
      return { success: false, error: 'Diagram element not found' };
    }

    if (typeof mermaid === 'undefined') {
      return { success: false, error: 'Mermaid.js not loaded' };
    }

    // Remove placeholder styling
    element.classList.remove('inserted-element-placeholder');

    // Update content
    let contentDiv = element.querySelector('.element-content');
    if (!contentDiv) {
      contentDiv = document.createElement('div');
      contentDiv.className = 'element-content';
      const dragHandle = element.querySelector('.element-drag-handle');
      if (dragHandle) {
        dragHandle.after(contentDiv);
      } else {
        element.prepend(contentDiv);
      }
    }

    // Hide placeholder content
    const placeholderContent = element.querySelector('.element-placeholder-content');
    if (placeholderContent) {
      placeholderContent.style.display = 'none';
    }
    const typeBadge = element.querySelector('.element-type-badge');
    if (typeBadge) {
      typeBadge.style.display = 'none';
    }

    // Render Mermaid diagram
    try {
      const mermaidId = `mermaid-${elementId}-svg`;
      const { svg } = await mermaid.render(mermaidId, mermaidCode);
      contentDiv.innerHTML = svg;

      // Update registry
      data.data.mermaidCode = mermaidCode;
      data.data.svgContent = svg;

      // Trigger auto-save
      triggerAutoSave(data.slideIndex);
      emitSlideContentChanged(data.slideIndex, 'modify', 'diagram');

      return { success: true };
    } catch (error) {
      console.error('Mermaid render failed:', error);
      return { success: false, error: error.message };
    }
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

    // Use provided id (for restoration) or generate new one
    const id = config.id || generateId('textbox');

    // DUPLICATE PREVENTION: Skip if element already exists ON THIS SLIDE
    // CRITICAL FIX: Only search within THIS slide, not globally
    // Using document.getElementById() caused elements from adjacent slides to be incorrectly
    // detected as "stale" and deleted when inserting new slides (slide indexes shift but IDs don't)
    const existingElement = slide.querySelector(`#${CSS.escape(id)}`);
    if (existingElement) {
      console.log(`[ElementManager] TextBox ${id} already exists on slide ${slideIndex}, skipping creation`);
      return { success: true, elementId: id, alreadyExists: true };
    }

    // Support both nested position object and direct gridRow/gridColumn
    const position = config.position || {
      gridRow: config.gridRow || '6/12',
      gridColumn: config.gridColumn || '5/28'
    };
    const style = config.style || {};

    // Text boxes use elevated z-index
    const zIndex = config.zIndex || (++textBoxZIndexCounter);

    // Create container
    const container = document.createElement('div');
    container.id = id;
    container.className = 'dynamic-element inserted-textbox';
    container.dataset.elementType = 'textbox';
    container.dataset.slideIndex = slideIndex;
    // Build flexbox styles for vertical/horizontal alignment
    // justifyContent controls vertical when flexDirection is 'column'
    // alignItems controls horizontal when flexDirection is 'column'
    // Default to 'flex' instead of 'block' for better alignment support
    const display = style.display || 'flex';
    // Flex properties - support both camelCase (template-registry) and snake_case (auto-save)
    const flexDirection = style.flex_direction || style.flexDirection || 'column';
    // Support verticalAlign as a user-friendly property that maps to justifyContent
    const justifyContent = style.verticalAlign
      ? mapVerticalAlign(style.verticalAlign)
      : (style.justify_content || style.justifyContent || 'flex-start');
    const alignItems = style.align_items || style.alignItems || 'flex-start';

    // Parse padding - supports individual properties OR shorthand
    // Priority: individual properties > shorthand padding > default 16px
    // Also support snake_case from auto-save (padding_top, padding_left, etc.)
    const pt = style.padding_top !== undefined ? style.padding_top
             : style.paddingTop !== undefined ? style.paddingTop : null;
    const pr = style.padding_right !== undefined ? style.padding_right
             : style.paddingRight !== undefined ? style.paddingRight : null;
    const pb = style.padding_bottom !== undefined ? style.padding_bottom
             : style.paddingBottom !== undefined ? style.paddingBottom : null;
    const pl = style.padding_left !== undefined ? style.padding_left
             : style.paddingLeft !== undefined ? style.paddingLeft : null;

    let paddingValue;
    if (pt !== null || pr !== null || pb !== null || pl !== null) {
      // Use individual properties - defaultPad is the shorthand base or 16
      const defaultPad = style.padding !== undefined ? style.padding : 16;
      paddingValue = `${parsePadding(pt !== null ? pt : defaultPad)} ${parsePadding(pr !== null ? pr : defaultPad)} ${parsePadding(pb !== null ? pb : defaultPad)} ${parsePadding(pl !== null ? pl : defaultPad)}`;
    } else {
      // Use shorthand only
      paddingValue = parsePadding(style.padding !== undefined ? style.padding : 16);
    }

    // Parse border - supports shorthand like "1px solid #ddd"
    const borderParsed = parseBorder(style.border);
    let borderStyle;
    if (borderParsed) {
      borderStyle = borderParsed.shorthand;
    } else {
      const bw = style.borderWidth || style.border_width || 0;
      const bc = style.borderColor || style.border_color || 'transparent';
      borderStyle = `${bw}px solid ${bc}`;
    }

    container.style.cssText = `
      grid-row: ${position.gridRow};
      grid-column: ${position.gridColumn};
      z-index: ${zIndex};
      background: ${style.backgroundColor || style.background_color || 'transparent'};
      border: ${borderStyle};
      border-radius: ${style.borderRadius || style.border_radius || 0}px;
      padding: ${paddingValue};
      opacity: ${style.opacity || 1};
      box-shadow: ${style.boxShadow || style.box_shadow || 'none'};
      min-height: 60px;
      overflow: auto;
      cursor: ${config.draggable !== false ? 'move' : 'text'};
      position: relative;
      display: ${display};
      flex-direction: ${flexDirection};
      justify-content: ${justifyContent};
      align-items: ${alignItems};
    `;

    // Apply CSS classes if provided
    if (config.cssClasses && Array.isArray(config.cssClasses)) {
      config.cssClasses.forEach(cls => {
        if (cls && typeof cls === 'string') {
          container.classList.add(cls);
        }
      });
    }

    // Create centered drag handle at top (NOT contentEditable, so it can be dragged)
    // Styles and 9-dot grid pattern are in textbox.css via ::before pseudo-element
    const dragHandle = document.createElement('div');
    dragHandle.className = 'textbox-drag-handle';
    // 9-dot pattern is rendered via CSS ::before (no innerHTML needed)

    // Create editable content area
    // Only enable contentEditable in edit mode
    const isEditMode = document.body.dataset.mode === 'edit';
    const contentDiv = document.createElement('div');
    contentDiv.className = 'textbox-content';
    contentDiv.setAttribute('contenteditable', isEditMode ? 'true' : 'false');  // Respect current mode
    contentDiv.dataset.placeholder = config.placeholder || 'Click to edit text';
    contentDiv.innerHTML = config.content || '';
    // NOTE: min-height: 100% defeats justify-content positioning (e.g., bottom-align)
    // Use 'auto' when a non-default justifyContent is specified to allow flex alignment to work
    const contentMinHeight = (justifyContent && justifyContent !== 'flex-start') ? 'auto' : '100%';
    contentDiv.style.cssText = `
      width: 100%;
      min-height: ${contentMinHeight};
      outline: none;
      cursor: text;
      font-family: Inter, system-ui, -apple-system, sans-serif;
      font-size: 32px;
      line-height: 1.5;
      color: #1f2937;
      pointer-events: auto;
    `;

    // Apply saved text styles (from LHS formatting panel via postMessage)
    // These override the defaults above when restoring from database
    if (config.textStyle) {
      if (config.textStyle.color) contentDiv.style.color = config.textStyle.color;
      if (config.textStyle.font_family) contentDiv.style.fontFamily = config.textStyle.font_family;
      if (config.textStyle.font_size) contentDiv.style.fontSize = config.textStyle.font_size;
      if (config.textStyle.font_weight) contentDiv.style.fontWeight = config.textStyle.font_weight;
      if (config.textStyle.font_style) contentDiv.style.fontStyle = config.textStyle.font_style;
      if (config.textStyle.text_align) contentDiv.style.textAlign = config.textStyle.text_align;
      if (config.textStyle.line_height) contentDiv.style.lineHeight = config.textStyle.line_height;
      if (config.textStyle.letter_spacing) contentDiv.style.letterSpacing = config.textStyle.letter_spacing;
      if (config.textStyle.text_decoration) contentDiv.style.textDecoration = config.textStyle.text_decoration;
      if (config.textStyle.text_transform) contentDiv.style.textTransform = config.textStyle.text_transform;
    }

    // Handle input for auto-save
    contentDiv.addEventListener('input', () => {
      triggerAutoSave(slideIndex);
    });

    // NOTE: mousedown no longer stops propagation - drag-drop.js handles
    // threshold-based detection to distinguish click-to-edit vs drag-to-move

    // Click handler as fallback for focus/selection
    // (drag-drop.js also handles this via handlePendingDragEnd)
    contentDiv.addEventListener('click', (e) => {
      e.stopPropagation();
      contentDiv.focus();
      // Also select the text box (triggers postMessage to parent)
      selectElement(id);
    });

    // Focus handling
    contentDiv.addEventListener('focus', () => {
      container.classList.add('textbox-editing');
    });
    contentDiv.addEventListener('blur', () => {
      container.classList.remove('textbox-editing');
      // Emit content changed event when user finishes editing text (v7.5.4)
      emitSlideContentChanged(slideIndex, 'modify', 'text');
    });

    // Create delete button (appears on hover/selection)
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-button';
    deleteBtn.innerHTML = '×';
    deleteBtn.title = 'Delete text box';
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteElement(id);
    });

    container.appendChild(dragHandle);
    container.appendChild(contentDiv);
    container.appendChild(deleteBtn);

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
    // Text boxes have minimum size of 2 columns × 2 rows
    if (config.resizable !== false && typeof window.DragDrop?.makeResizable === 'function') {
      window.DragDrop.makeResizable(id, { minCols: 2, minRows: 2 });
    }

    // Apply locked state if specified
    if (config.locked) {
      container.classList.add('textbox-locked');
    }

    // Apply hidden state if specified
    if (config.visible === false) {
      container.classList.add('textbox-hidden');
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
        cssClasses: config.cssClasses || [],
        placeholder: config.placeholder,
        locked: config.locked || false,
        visible: config.visible !== false
      }
    };
    elementRegistry.set(id, elementData);

    // Trigger auto-save only for NEW text boxes (not restoration)
    // If id was provided in config, this is a restoration - skip auto-save
    if (!config.id) {
      triggerAutoSave(slideIndex);
      emitSlideContentChanged(slideIndex, 'add', 'text');
    }

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
      emitSlideContentChanged(data.slideIndex, 'modify', 'text');
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

    // Handle border - supports shorthand like "1px solid #ddd"
    if (style.border) {
      const borderParsed = parseBorder(style.border);
      if (borderParsed) {
        element.style.border = borderParsed.shorthand;
      }
    } else {
      if (style.borderColor || style.border_color) {
        element.style.borderColor = style.borderColor || style.border_color;
      }
      if (style.borderWidth !== undefined || style.border_width !== undefined) {
        element.style.borderWidth = (style.borderWidth || style.border_width || 0) + 'px';
      }
    }

    if (style.borderRadius !== undefined || style.border_radius !== undefined) {
      element.style.borderRadius = (style.borderRadius || style.border_radius || 0) + 'px';
    }

    // Handle padding - supports shorthand like "25px 0px"
    if (style.padding !== undefined) {
      element.style.padding = parsePadding(style.padding);
    }

    if (style.opacity !== undefined) {
      element.style.opacity = style.opacity;
    }
    if (style.boxShadow || style.box_shadow) {
      element.style.boxShadow = style.boxShadow || style.box_shadow;
    }

    // Handle vertical align - maps to justifyContent
    if (style.verticalAlign) {
      element.style.justifyContent = mapVerticalAlign(style.verticalAlign);
    }

    // Update registry
    data.data.style = { ...data.data.style, ...style };
    triggerAutoSave(data.slideIndex);

    return { success: true };
  }

  /**
   * Update CSS classes on an element
   * Allows programmatic control of custom CSS classes for styling
   *
   * @param {string} elementId - Element ID
   * @param {string[]} classes - Array of CSS class names to apply
   * @param {Object} [options] - Options
   * @param {boolean} [options.replace=true] - If true, replaces all custom classes; if false, adds to existing
   * @returns {Object} Result object
   */
  function updateElementClasses(elementId, classes, options = {}) {
    const element = document.getElementById(elementId);
    const data = elementRegistry.get(elementId);

    if (!element || !data) {
      return { success: false, error: 'Element not found' };
    }

    const replace = options.replace !== false;  // Default to replace mode

    // System classes to preserve (never remove these)
    const systemPrefixes = ['dynamic-element', 'inserted-', 'element-', 'textbox-'];

    if (replace) {
      // Remove all non-system classes first
      const currentClasses = Array.from(element.classList);
      currentClasses.forEach(cls => {
        const isSystem = systemPrefixes.some(prefix => cls.startsWith(prefix));
        if (!isSystem) {
          element.classList.remove(cls);
        }
      });
    }

    // Add new classes
    if (Array.isArray(classes)) {
      classes.forEach(cls => {
        if (cls && typeof cls === 'string') {
          element.classList.add(cls);
        }
      });
    }

    // Update registry
    data.data.cssClasses = Array.from(element.classList).filter(cls =>
      !systemPrefixes.some(prefix => cls.startsWith(prefix))
    );

    triggerAutoSave(data.slideIndex);

    return {
      success: true,
      elementId: elementId,
      cssClasses: data.data.cssClasses
    };
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
   * Extract formatting information from a text box element
   *
   * @param {HTMLElement} element - Text box container element
   * @returns {Object} Formatting properties
   */
  function extractTextBoxFormatting(element) {
    const contentDiv = element.querySelector('.textbox-content');
    if (!contentDiv) return null;

    const computedStyle = window.getComputedStyle(contentDiv);
    const containerStyle = window.getComputedStyle(element);

    // Extract CSS classes (excluding system classes)
    const cssClasses = Array.from(element.classList).filter(cls =>
      !cls.startsWith('dynamic-element') &&
      !cls.startsWith('inserted-') &&
      !cls.startsWith('element-') &&
      !cls.startsWith('textbox-')
    );

    // Extract vertical align from justifyContent
    const verticalAlign = reverseMapVerticalAlign(containerStyle.justifyContent);

    // Build padding shorthand string
    const pt = parseInt(containerStyle.paddingTop) || 0;
    const pr = parseInt(containerStyle.paddingRight) || 0;
    const pb = parseInt(containerStyle.paddingBottom) || 0;
    const pl = parseInt(containerStyle.paddingLeft) || 0;
    let paddingShorthand;
    if (pt === pr && pr === pb && pb === pl) {
      paddingShorthand = `${pt}px`;
    } else if (pt === pb && pl === pr) {
      paddingShorthand = `${pt}px ${pr}px`;
    } else {
      paddingShorthand = `${pt}px ${pr}px ${pb}px ${pl}px`;
    }

    return {
      fontFamily: computedStyle.fontFamily,
      fontSize: parseInt(computedStyle.fontSize) || 32,
      fontWeight: computedStyle.fontWeight,
      fontStyle: computedStyle.fontStyle,
      textDecoration: computedStyle.textDecoration,
      textTransform: computedStyle.textTransform,
      color: computedStyle.color,
      backgroundColor: containerStyle.backgroundColor,
      textAlign: computedStyle.textAlign,
      verticalAlign: verticalAlign,
      lineHeight: computedStyle.lineHeight,
      // Padding as shorthand string and detailed object
      paddingShorthand: paddingShorthand,
      padding: {
        top: pt,
        right: pr,
        bottom: pb,
        left: pl
      },
      // Border as shorthand and detailed object
      borderShorthand: formatBorderShorthand(containerStyle),
      border: {
        width: parseInt(containerStyle.borderWidth) || 0,
        color: containerStyle.borderColor,
        style: containerStyle.borderStyle
      },
      borderRadius: {
        topLeft: parseInt(containerStyle.borderTopLeftRadius) || 0,
        topRight: parseInt(containerStyle.borderTopRightRadius) || 0,
        bottomRight: parseInt(containerStyle.borderBottomRightRadius) || 0,
        bottomLeft: parseInt(containerStyle.borderBottomLeftRadius) || 0
      },
      // CSS classes (custom classes only, excluding system classes)
      cssClasses: cssClasses
    };
  }

  /**
   * Extract properties from a generic element
   *
   * @param {HTMLElement} element - Element container
   * @param {Object} data - Element data from registry
   * @returns {Object} Element properties
   */
  function extractElementProperties(element, data) {
    const rect = element.getBoundingClientRect();
    const computedStyle = window.getComputedStyle(element);

    // Base properties for all elements
    const properties = {
      position: {
        x: rect.left,
        y: rect.top
      },
      size: {
        width: rect.width,
        height: rect.height
      },
      rotation: 0, // Future: extract from transform
      locked: element.classList.contains('element-locked') || false,
      zIndex: parseInt(computedStyle.zIndex) || data.zIndex
    };

    // Add element-specific properties based on type
    switch (data.type) {
      case 'image':
        Object.assign(properties, extractImageProperties(element, data));
        break;
      case 'chart':
        Object.assign(properties, extractChartProperties(element, data));
        break;
      case 'table':
        Object.assign(properties, extractTableProperties(element, data));
        break;
      case 'infographic':
        Object.assign(properties, extractInfographicProperties(element, data));
        break;
      case 'diagram':
        Object.assign(properties, extractDiagramProperties(element, data));
        break;
    }

    return properties;
  }

  /**
   * Extract image-specific properties
   */
  function extractImageProperties(element, data) {
    const img = element.querySelector('.element-content img');
    const isPlaceholder = element.classList.contains('placeholder-mode');

    return {
      imageUrl: img ? img.src : null,
      altText: img ? img.alt : '',
      objectFit: img ? (img.style.objectFit || 'cover') : 'cover',
      isPlaceholder: isPlaceholder,
      opacity: parseFloat(element.style.opacity) || 1,
      borderRadius: element.style.borderRadius || '0px'
    };
  }

  /**
   * Extract chart-specific properties
   */
  function extractChartProperties(element, data) {
    const canvas = element.querySelector('canvas');
    const isPlaceholder = element.classList.contains('placeholder-mode');

    return {
      chartType: data.chartType || 'bar',
      chartData: data.chartData || null,
      isPlaceholder: isPlaceholder,
      hasCanvas: !!canvas
    };
  }

  /**
   * Extract table-specific properties
   */
  function extractTableProperties(element, data) {
    const table = element.querySelector('table');
    const isPlaceholder = element.classList.contains('placeholder-mode');

    let rows = 0, cols = 0;
    if (table) {
      const tableRows = table.querySelectorAll('tr');
      rows = tableRows.length;
      if (tableRows[0]) {
        cols = tableRows[0].querySelectorAll('td, th').length;
      }
    }

    return {
      rows: rows,
      columns: cols,
      hasHeader: table ? !!table.querySelector('thead') : false,
      isPlaceholder: isPlaceholder,
      tableData: data.tableData || null
    };
  }

  /**
   * Extract infographic-specific properties
   */
  function extractInfographicProperties(element, data) {
    const svg = element.querySelector('svg');
    const isPlaceholder = element.classList.contains('placeholder-mode');

    return {
      infographicType: data.infographicType || 'generic',
      hasSvg: !!svg,
      isPlaceholder: isPlaceholder
    };
  }

  /**
   * Extract diagram-specific properties
   */
  function extractDiagramProperties(element, data) {
    const svg = element.querySelector('svg');
    const isPlaceholder = element.classList.contains('placeholder-mode');

    return {
      diagramType: data.diagramType || 'generic',
      hasSvg: !!svg,
      isPlaceholder: isPlaceholder
    };
  }

  /**
   * Emit postMessage to parent window for element selection
   *
   * @param {string} elementId - Selected element ID
   * @param {Object} data - Element data from registry
   * @param {HTMLElement} element - DOM element
   */
  function emitSelectionEvent(elementId, data, element) {
    if (!window.parent || window.parent === window) return;

    if (data.type === 'textbox') {
      // Text box selected - emit textBoxSelected with formatting
      const formatting = extractTextBoxFormatting(element);
      window.parent.postMessage({
        type: 'textBoxSelected',
        elementId: elementId,
        formatting: formatting
      }, '*');
      console.log('📤 postMessage: textBoxSelected', elementId);
    } else {
      // Other element types - emit elementSelected
      const properties = extractElementProperties(element, data);
      window.parent.postMessage({
        type: 'elementSelected',
        elementId: elementId,
        elementType: data.type, // image, table, chart, shape
        properties: properties
      }, '*');
      console.log('📤 postMessage: elementSelected', data.type, elementId);
    }
  }

  /**
   * Emit postMessage to parent window for element deselection
   *
   * @param {string} elementId - Deselected element ID (optional)
   * @param {string} elementType - Element type (optional)
   */
  function emitDeselectionEvent(elementId, elementType) {
    if (!window.parent || window.parent === window) return;

    if (elementType === 'textbox') {
      window.parent.postMessage({
        type: 'textBoxDeselected'
      }, '*');
      console.log('📤 postMessage: textBoxDeselected');
    } else if (elementId) {
      window.parent.postMessage({
        type: 'elementDeselected',
        elementId: elementId
      }, '*');
      console.log('📤 postMessage: elementDeselected', elementId);
    }
  }

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

      // Emit postMessage to parent (for frontend format toolbar)
      emitSelectionEvent(elementId, data, element);

      // Legacy callback (for local handlers)
      if (typeof window.onElementSelected === 'function') {
        window.onElementSelected(data);
      }
    }
  }

  /**
   * Deselect all elements
   */
  function deselectAll() {
    const previousId = selectedElementId;
    let previousType = null;

    if (selectedElementId) {
      const element = document.getElementById(selectedElementId);
      const data = elementRegistry.get(selectedElementId);

      if (element) {
        element.classList.remove('element-selected');
      }
      if (data) {
        data.selected = false;
        previousType = data.type;
      }
    }
    selectedElementId = null;

    // Emit deselection event to parent
    if (previousId) {
      emitDeselectionEvent(previousId, previousType);
    }
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
    // Map element types: textbox -> text, shape -> shape, etc.
    const elementTypeMap = { textbox: 'text', shape: 'shape', table: 'table', chart: 'chart', image: 'image', infographic: 'infographic', diagram: 'diagram' };
    emitSlideContentChanged(data.slideIndex, 'delete', elementTypeMap[data.type] || data.type);

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

  /**
   * Emit slide_content_changed event to parent frame (v7.5.4)
   * Called after any user-initiated CRUD operation on slide content
   *
   * @param {number} slideIndex - Index of affected slide
   * @param {string} changeType - 'add' | 'modify' | 'delete'
   * @param {string} elementType - 'text' | 'image' | 'chart' | 'table' | 'diagram' | 'infographic' | 'shape' | 'slide'
   */
  function emitSlideContentChanged(slideIndex, changeType, elementType) {
    // Only emit in framed context
    if (!window.parent || window.parent === window) return;

    // Only emit for user-initiated changes (check edit mode)
    const container = document.querySelector('.reveal');
    if (!container || container.getAttribute('data-mode') !== 'edit') return;

    window.parent.postMessage({
      action: 'slide_content_changed',
      data: {
        slideIndex: slideIndex,
        changeType: changeType,  // 'add' | 'modify' | 'delete'
        elementType: elementType,
        timestamp: Date.now()
      }
    }, '*');

    console.log('📤 postMessage: slide_content_changed', { slideIndex, changeType, elementType });
  }

  // ===== GLOBAL EVENT HANDLERS =====

  // Deselect elements when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.dynamic-element')) {
      deselectAll();
    }
  });

  // ===== CLIPBOARD SUPPORT =====

  /**
   * Clipboard storage for copy/cut operations
   */
  let clipboardData = null;

  /**
   * Copy selected element to clipboard
   */
  function copyElement() {
    if (!selectedElementId) return { success: false, error: 'No element selected' };

    const data = elementRegistry.get(selectedElementId);
    const element = document.getElementById(selectedElementId);

    if (!data || !element) return { success: false, error: 'Element not found' };

    // For text boxes, capture content and styles
    if (data.type === 'textbox') {
      const contentDiv = element.querySelector('.textbox-content');
      clipboardData = {
        type: 'textbox',
        content: contentDiv ? contentDiv.innerHTML : '',
        position: { ...data.position },
        style: { ...data.data.style },
        textStyle: data.data.textStyle ? { ...data.data.textStyle } : null
      };
      console.log('📋 Copied text box to clipboard');
      return { success: true, message: 'Text box copied' };
    }

    return { success: false, error: 'Copy not supported for this element type' };
  }

  /**
   * Cut selected element (copy + delete)
   */
  function cutElement() {
    const copyResult = copyElement();
    if (copyResult.success) {
      deleteElement(selectedElementId);
      console.log('✂️ Cut text box');
      return { success: true, message: 'Text box cut' };
    }
    return copyResult;
  }

  /**
   * Paste element from clipboard
   */
  function pasteElement() {
    if (!clipboardData) return { success: false, error: 'Clipboard is empty' };

    // Find current slide index
    const currentSlide = document.querySelector('.reveal .slides > section.present');
    if (!currentSlide) return { success: false, error: 'No active slide' };

    const slides = document.querySelectorAll('.reveal .slides > section');
    let slideIndex = 0;
    slides.forEach((slide, idx) => {
      if (slide === currentSlide) slideIndex = idx;
    });

    if (clipboardData.type === 'textbox') {
      // Offset position slightly so paste is visible
      const position = { ...clipboardData.position };
      // Parse and offset the grid position
      const rowParts = position.gridRow.split('/');
      const colParts = position.gridColumn.split('/');
      position.gridRow = `${parseInt(rowParts[0]) + 1}/${parseInt(rowParts[1]) + 1}`;
      position.gridColumn = `${parseInt(colParts[0]) + 1}/${parseInt(colParts[1]) + 1}`;

      const result = insertTextBox(slideIndex, {
        position: position,
        content: clipboardData.content,
        style: clipboardData.style,
        textStyle: clipboardData.textStyle
      });

      if (result.success) {
        selectElement(result.elementId);
        console.log('📋 Pasted text box');
      }
      return result;
    }

    return { success: false, error: 'Paste not supported for this element type' };
  }

  // ===== KEYBOARD SHORTCUTS =====

  document.addEventListener('keydown', (e) => {
    // Check if user is typing in an editable area (don't intercept normal typing)
    const isEditing = e.target.isContentEditable ||
                      e.target.tagName === 'INPUT' ||
                      e.target.tagName === 'TEXTAREA';

    // Modifier key check (Cmd on Mac, Ctrl on Windows/Linux)
    const modKey = e.metaKey || e.ctrlKey;

    // Escape - Deselect
    if (e.key === 'Escape' && selectedElementId) {
      deselectAll();
      return;
    }

    // Delete/Backspace - Delete selected element (only if not editing text)
    if ((e.key === 'Delete' || e.key === 'Backspace') && selectedElementId && !isEditing) {
      e.preventDefault();
      deleteElement(selectedElementId);
      console.log('🗑️ Deleted element via keyboard');
      return;
    }

    // Ctrl/Cmd + C - Copy
    if (modKey && e.key === 'c' && selectedElementId && !isEditing) {
      e.preventDefault();
      copyElement();
      return;
    }

    // Ctrl/Cmd + X - Cut
    if (modKey && e.key === 'x' && selectedElementId && !isEditing) {
      e.preventDefault();
      cutElement();
      return;
    }

    // Ctrl/Cmd + V - Paste
    if (modKey && e.key === 'v' && clipboardData && !isEditing) {
      e.preventDefault();
      pasteElement();
      return;
    }

    // Ctrl/Cmd + Z - Undo (notify parent frame)
    if (modKey && e.key === 'z' && !isEditing) {
      // Emit undo request to parent frame
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'undoRequested' }, '*');
        console.log('↩️ Undo requested');
      }
      return;
    }

    // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y - Redo (notify parent frame)
    if (modKey && (e.key === 'y' || (e.shiftKey && e.key === 'z')) && !isEditing) {
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'redoRequested' }, '*');
        console.log('↪️ Redo requested');
      }
      return;
    }
  });

  // ===== EXPOSE API =====

  /**
   * Emit updated formatting for currently selected text box
   * Call this when formatting changes while a text box is selected
   */
  function emitFormattingUpdate() {
    if (!selectedElementId) return;

    const element = document.getElementById(selectedElementId);
    const data = elementRegistry.get(selectedElementId);

    if (element && data && data.type === 'textbox') {
      const formatting = extractTextBoxFormatting(element);
      if (window.parent && window.parent !== window) {
        window.parent.postMessage({
          type: 'textBoxSelected',
          elementId: selectedElementId,
          formatting: formatting
        }, '*');
        console.log('📤 postMessage: textBoxSelected (formatting update)', selectedElementId);
      }
    }
  }

  window.ElementManager = {
    // Insert methods
    insertShape: insertShape,
    insertTable: insertTable,
    insertChart: insertChart,
    insertImage: insertImage,
    insertTextBox: insertTextBox,
    insertInfographic: insertInfographic,
    insertDiagram: insertDiagram,

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

    // CSS classes method (works on any element)
    updateElementClasses: updateElementClasses,

    // Image specific methods
    updateImageSource: updateImageSource,

    // Chart specific methods
    updateChartConfig: updateChartConfig,
    setChartHtml: setChartHtml,

    // Infographic specific methods
    updateInfographicContent: updateInfographicContent,

    // Diagram specific methods
    updateDiagramSvg: updateDiagramSvg,
    updateDiagramMermaid: updateDiagramMermaid,

    // Clipboard methods (Ctrl/Cmd + C/X/V)
    copyElement: copyElement,
    cutElement: cutElement,
    pasteElement: pasteElement,

    // PostMessage events (for parent frame communication)
    emitFormattingUpdate: emitFormattingUpdate,
    extractTextBoxFormatting: extractTextBoxFormatting,
    emitSlideContentChanged: emitSlideContentChanged,

    // Property helpers (for programmatic use)
    utils: {
      mapVerticalAlign: mapVerticalAlign,
      reverseMapVerticalAlign: reverseMapVerticalAlign,
      parsePadding: parsePadding,
      parseBorder: parseBorder,
      formatBorderShorthand: formatBorderShorthand
    },

    // Registry access (for debugging)
    _registry: elementRegistry
  };

  console.log('ElementManager initialized');

})();
