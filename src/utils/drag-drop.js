/**
 * Drag-Drop Module for Layout Builder v7.5
 *
 * Provides grid-snapped drag and drop functionality for dynamic elements.
 * Works with the 32×18 grid system (1920×1080 base resolution).
 *
 * Exposed via window.DragDrop for ElementManager access.
 */

(function() {
  'use strict';

  // ===== GRID CONFIGURATION =====

  const GRID_COLS = 32;
  const GRID_ROWS = 18;
  const BASE_WIDTH = 1920;
  const BASE_HEIGHT = 1080;

  // ===== STATE =====

  let isDragging = false;
  let dragElement = null;
  let dragElementId = null;
  let startMouseX = 0;
  let startMouseY = 0;
  let startGridRow = '';
  let startGridColumn = '';
  let currentSlide = null;
  let gridSnapEnabled = true;

  // ===== MAKE ELEMENT DRAGGABLE =====

  /**
   * Enable drag-drop on an element
   *
   * @param {string} elementId - Element ID to make draggable
   */
  function makeDraggable(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
      console.warn(`DragDrop: Element not found: ${elementId}`);
      return;
    }

    // Add drag handle styling
    element.classList.add('draggable');

    // Mouse events
    element.addEventListener('mousedown', handleDragStart);

    // Touch events for mobile
    element.addEventListener('touchstart', handleTouchStart, { passive: false });
  }

  // ===== DRAG START =====

  /**
   * Handle mouse drag start
   *
   * @param {MouseEvent} e - Mouse event
   */
  function handleDragStart(e) {
    // Don't drag if clicking on interactive elements
    if (e.target.closest('input, textarea, [contenteditable="true"], canvas, button')) {
      return;
    }

    // Don't drag if not in edit mode
    if (document.body.getAttribute('data-mode') !== 'edit') {
      return;
    }

    const element = e.currentTarget;
    if (!element.classList.contains('draggable')) {
      return;
    }

    e.preventDefault();
    e.stopPropagation();

    startDrag(element, e.clientX, e.clientY);

    // Add document-level listeners
    document.addEventListener('mousemove', handleDragMove);
    document.addEventListener('mouseup', handleDragEnd);
  }

  /**
   * Handle touch drag start
   *
   * @param {TouchEvent} e - Touch event
   */
  function handleTouchStart(e) {
    if (e.target.closest('input, textarea, [contenteditable="true"], canvas, button')) {
      return;
    }

    if (document.body.getAttribute('data-mode') !== 'edit') {
      return;
    }

    const element = e.currentTarget;
    if (!element.classList.contains('draggable')) {
      return;
    }

    e.preventDefault();

    const touch = e.touches[0];
    startDrag(element, touch.clientX, touch.clientY);

    document.addEventListener('touchmove', handleTouchMove, { passive: false });
    document.addEventListener('touchend', handleTouchEnd);
  }

  /**
   * Initialize drag state
   *
   * @param {HTMLElement} element - Element being dragged
   * @param {number} clientX - Starting X coordinate
   * @param {number} clientY - Starting Y coordinate
   */
  function startDrag(element, clientX, clientY) {
    isDragging = true;
    dragElement = element;
    dragElementId = element.id;
    startMouseX = clientX;
    startMouseY = clientY;
    startGridRow = element.style.gridRow;
    startGridColumn = element.style.gridColumn;

    // Find parent slide
    currentSlide = element.closest('.reveal .slides > section');

    // Visual feedback
    element.classList.add('dragging');
    element.style.transition = 'none';

    // Select the element
    if (typeof window.ElementManager !== 'undefined') {
      window.ElementManager.selectElement(dragElementId);
    }
  }

  // ===== DRAG MOVE =====

  /**
   * Handle mouse drag move
   *
   * @param {MouseEvent} e - Mouse event
   */
  function handleDragMove(e) {
    if (!isDragging || !dragElement) return;
    e.preventDefault();
    updateDragPosition(e.clientX, e.clientY);
  }

  /**
   * Handle touch drag move
   *
   * @param {TouchEvent} e - Touch event
   */
  function handleTouchMove(e) {
    if (!isDragging || !dragElement) return;
    e.preventDefault();
    const touch = e.touches[0];
    updateDragPosition(touch.clientX, touch.clientY);
  }

  /**
   * Update element position during drag
   *
   * @param {number} clientX - Current X coordinate
   * @param {number} clientY - Current Y coordinate
   */
  function updateDragPosition(clientX, clientY) {
    if (!currentSlide) return;

    // Get slide bounds and scale
    const slideRect = currentSlide.getBoundingClientRect();
    const scaleX = slideRect.width / BASE_WIDTH;
    const scaleY = slideRect.height / BASE_HEIGHT;

    // Calculate grid cell size in current viewport
    const cellWidth = slideRect.width / GRID_COLS;
    const cellHeight = slideRect.height / GRID_ROWS;

    // Calculate movement in grid cells
    const deltaX = clientX - startMouseX;
    const deltaY = clientY - startMouseY;
    const colDelta = Math.round(deltaX / cellWidth);
    const rowDelta = Math.round(deltaY / cellHeight);

    // Parse current grid position
    const [rowStart, rowEnd] = parseGridSpan(startGridRow);
    const [colStart, colEnd] = parseGridSpan(startGridColumn);

    // Calculate element size in grid units
    const rowSpan = rowEnd - rowStart;
    const colSpan = colEnd - colStart;

    // Calculate new position with boundary constraints
    let newRowStart = rowStart + rowDelta;
    let newColStart = colStart + colDelta;

    // Boundary constraints (keep element within grid)
    newRowStart = Math.max(1, Math.min(GRID_ROWS - rowSpan + 1, newRowStart));
    newColStart = Math.max(1, Math.min(GRID_COLS - colSpan + 1, newColStart));

    const newRowEnd = newRowStart + rowSpan;
    const newColEnd = newColStart + colSpan;

    // Apply new position
    if (gridSnapEnabled) {
      dragElement.style.gridRow = `${newRowStart}/${newRowEnd}`;
      dragElement.style.gridColumn = `${newColStart}/${newColEnd}`;
    } else {
      // Free-form drag (not snapped to grid) - use transform
      dragElement.style.transform = `translate(${deltaX / scaleX}px, ${deltaY / scaleY}px)`;
    }
  }

  /**
   * Parse grid span string (e.g., "5/12" -> [5, 12])
   *
   * @param {string} span - Grid span string
   * @returns {number[]} [start, end]
   */
  function parseGridSpan(span) {
    if (!span) return [1, 5];

    const parts = span.split('/').map(s => parseInt(s.trim()));
    if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
      return parts;
    }
    if (parts.length === 1 && !isNaN(parts[0])) {
      return [parts[0], parts[0] + 4]; // Default span of 4
    }
    return [1, 5];
  }

  // ===== DRAG END =====

  /**
   * Handle mouse drag end
   *
   * @param {MouseEvent} e - Mouse event
   */
  function handleDragEnd(e) {
    document.removeEventListener('mousemove', handleDragMove);
    document.removeEventListener('mouseup', handleDragEnd);
    finalizeDrag();
  }

  /**
   * Handle touch drag end
   *
   * @param {TouchEvent} e - Touch event
   */
  function handleTouchEnd(e) {
    document.removeEventListener('touchmove', handleTouchMove);
    document.removeEventListener('touchend', handleTouchEnd);
    finalizeDrag();
  }

  /**
   * Finalize drag operation
   */
  function finalizeDrag() {
    if (!isDragging || !dragElement) return;

    // Remove visual feedback
    dragElement.classList.remove('dragging');
    dragElement.style.transition = '';
    dragElement.style.transform = '';

    // Check if position changed
    const newGridRow = dragElement.style.gridRow;
    const newGridColumn = dragElement.style.gridColumn;

    if (newGridRow !== startGridRow || newGridColumn !== startGridColumn) {
      // Update ElementManager
      if (typeof window.ElementManager !== 'undefined') {
        window.ElementManager.updatePosition(dragElementId, {
          gridRow: newGridRow,
          gridColumn: newGridColumn
        });
      }

      console.log(`DragDrop: Moved ${dragElementId} to row:${newGridRow} col:${newGridColumn}`);
    }

    // Reset state
    isDragging = false;
    dragElement = null;
    dragElementId = null;
    currentSlide = null;
  }

  // ===== POSITION API =====

  /**
   * Get element's current grid position
   *
   * @param {string} elementId - Element ID
   * @returns {Object|null} Position {gridRow, gridColumn}
   */
  function getPosition(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return null;

    return {
      gridRow: element.style.gridRow,
      gridColumn: element.style.gridColumn
    };
  }

  /**
   * Set element's grid position
   *
   * @param {string} elementId - Element ID
   * @param {string} gridRow - Grid row (e.g., "5/12")
   * @param {string} gridColumn - Grid column (e.g., "3/20")
   */
  function setPosition(elementId, gridRow, gridColumn) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Validate bounds
    const [rowStart, rowEnd] = parseGridSpan(gridRow);
    const [colStart, colEnd] = parseGridSpan(gridColumn);

    if (rowStart < 1 || rowEnd > GRID_ROWS + 1 ||
        colStart < 1 || colEnd > GRID_COLS + 1) {
      console.warn(`DragDrop: Position out of bounds: row ${gridRow}, col ${gridColumn}`);
      return;
    }

    element.style.gridRow = gridRow;
    element.style.gridColumn = gridColumn;

    // Update ElementManager
    if (typeof window.ElementManager !== 'undefined') {
      window.ElementManager.updatePosition(elementId, { gridRow, gridColumn });
    }
  }

  /**
   * Enable or disable grid snapping
   *
   * @param {boolean} enabled - Whether to snap to grid
   */
  function setGridSnap(enabled) {
    gridSnapEnabled = enabled;
  }

  // ===== RESIZE SUPPORT =====

  // Resize state
  let isResizing = false;
  let resizeElement = null;
  let resizeElementId = null;
  let resizeHandle = null;
  let resizeStartX = 0;
  let resizeStartY = 0;
  let resizeStartGridRow = '';
  let resizeStartGridColumn = '';
  let resizeSlide = null;

  // Minimum size in grid units
  const MIN_COLS = 2;
  const MIN_ROWS = 1;

  /**
   * Make element resizable with 8-point handles
   *
   * @param {string} elementId - Element ID
   * @param {Object} [options] - Options
   * @param {number} [options.minCols=2] - Minimum column span
   * @param {number} [options.minRows=1] - Minimum row span
   */
  function makeResizable(elementId, options = {}) {
    const element = document.getElementById(elementId);
    if (!element) {
      console.warn(`DragDrop: Element not found for resize: ${elementId}`);
      return;
    }

    const minCols = options.minCols || MIN_COLS;
    const minRows = options.minRows || MIN_ROWS;

    // Store min size on element for reference
    element.dataset.minCols = minCols;
    element.dataset.minRows = minRows;

    // Add resizable class
    element.classList.add('resizable');

    // Create 8 resize handles (4 corners + 4 edges)
    const handles = ['nw', 'n', 'ne', 'e', 'se', 's', 'sw', 'w'];

    handles.forEach(direction => {
      // Check if handle already exists
      if (element.querySelector(`.resize-handle-${direction}`)) {
        return;
      }

      const handle = document.createElement('div');
      handle.className = `resize-handle resize-handle-${direction}`;
      handle.dataset.direction = direction;

      // Mouse events
      handle.addEventListener('mousedown', (e) => handleResizeStart(e, elementId, direction));

      // Touch events
      handle.addEventListener('touchstart', (e) => handleResizeTouchStart(e, elementId, direction), { passive: false });

      element.appendChild(handle);
    });

    console.log(`DragDrop: Made ${elementId} resizable`);
  }

  /**
   * Handle resize start (mouse)
   */
  function handleResizeStart(e, elementId, direction) {
    e.preventDefault();
    e.stopPropagation();

    // Only in edit mode
    if (document.body.getAttribute('data-mode') !== 'edit') {
      return;
    }

    const element = document.getElementById(elementId);
    if (!element) return;

    startResize(element, elementId, direction, e.clientX, e.clientY);

    document.addEventListener('mousemove', handleResizeMove);
    document.addEventListener('mouseup', handleResizeEnd);
  }

  /**
   * Handle resize start (touch)
   */
  function handleResizeTouchStart(e, elementId, direction) {
    e.preventDefault();
    e.stopPropagation();

    if (document.body.getAttribute('data-mode') !== 'edit') {
      return;
    }

    const element = document.getElementById(elementId);
    if (!element) return;

    const touch = e.touches[0];
    startResize(element, elementId, direction, touch.clientX, touch.clientY);

    document.addEventListener('touchmove', handleResizeTouchMove, { passive: false });
    document.addEventListener('touchend', handleResizeTouchEnd);
  }

  /**
   * Initialize resize state
   */
  function startResize(element, elementId, direction, clientX, clientY) {
    isResizing = true;
    resizeElement = element;
    resizeElementId = elementId;
    resizeHandle = direction;
    resizeStartX = clientX;
    resizeStartY = clientY;
    resizeStartGridRow = element.style.gridRow;
    resizeStartGridColumn = element.style.gridColumn;
    resizeSlide = element.closest('.reveal .slides > section');

    // Visual feedback
    element.classList.add('resizing');
    element.style.transition = 'none';

    // Select the element
    if (typeof window.ElementManager !== 'undefined') {
      window.ElementManager.selectElement(elementId);
    }
  }

  /**
   * Handle resize move (mouse)
   */
  function handleResizeMove(e) {
    if (!isResizing || !resizeElement) return;
    e.preventDefault();
    updateResizePosition(e.clientX, e.clientY);
  }

  /**
   * Handle resize move (touch)
   */
  function handleResizeTouchMove(e) {
    if (!isResizing || !resizeElement) return;
    e.preventDefault();
    const touch = e.touches[0];
    updateResizePosition(touch.clientX, touch.clientY);
  }

  /**
   * Update element size during resize
   */
  function updateResizePosition(clientX, clientY) {
    if (!resizeSlide || !resizeElement) return;

    // Get slide bounds
    const slideRect = resizeSlide.getBoundingClientRect();
    const cellWidth = slideRect.width / GRID_COLS;
    const cellHeight = slideRect.height / GRID_ROWS;

    // Calculate movement in grid cells
    const deltaX = clientX - resizeStartX;
    const deltaY = clientY - resizeStartY;
    const colDelta = Math.round(deltaX / cellWidth);
    const rowDelta = Math.round(deltaY / cellHeight);

    // Parse starting position
    const [rowStart, rowEnd] = parseGridSpan(resizeStartGridRow);
    const [colStart, colEnd] = parseGridSpan(resizeStartGridColumn);

    // Get min sizes
    const minCols = parseInt(resizeElement.dataset.minCols) || MIN_COLS;
    const minRows = parseInt(resizeElement.dataset.minRows) || MIN_ROWS;

    // Calculate new values based on handle direction
    let newRowStart = rowStart;
    let newRowEnd = rowEnd;
    let newColStart = colStart;
    let newColEnd = colEnd;

    switch (resizeHandle) {
      case 'n':  // North (top edge)
        newRowStart = Math.max(1, Math.min(rowEnd - minRows, rowStart + rowDelta));
        break;
      case 's':  // South (bottom edge)
        newRowEnd = Math.max(rowStart + minRows, Math.min(GRID_ROWS + 1, rowEnd + rowDelta));
        break;
      case 'e':  // East (right edge)
        newColEnd = Math.max(colStart + minCols, Math.min(GRID_COLS + 1, colEnd + colDelta));
        break;
      case 'w':  // West (left edge)
        newColStart = Math.max(1, Math.min(colEnd - minCols, colStart + colDelta));
        break;
      case 'nw': // Northwest corner
        newRowStart = Math.max(1, Math.min(rowEnd - minRows, rowStart + rowDelta));
        newColStart = Math.max(1, Math.min(colEnd - minCols, colStart + colDelta));
        break;
      case 'ne': // Northeast corner
        newRowStart = Math.max(1, Math.min(rowEnd - minRows, rowStart + rowDelta));
        newColEnd = Math.max(colStart + minCols, Math.min(GRID_COLS + 1, colEnd + colDelta));
        break;
      case 'sw': // Southwest corner
        newRowEnd = Math.max(rowStart + minRows, Math.min(GRID_ROWS + 1, rowEnd + rowDelta));
        newColStart = Math.max(1, Math.min(colEnd - minCols, colStart + colDelta));
        break;
      case 'se': // Southeast corner
        newRowEnd = Math.max(rowStart + minRows, Math.min(GRID_ROWS + 1, rowEnd + rowDelta));
        newColEnd = Math.max(colStart + minCols, Math.min(GRID_COLS + 1, colEnd + colDelta));
        break;
    }

    // Apply new size
    resizeElement.style.gridRow = `${newRowStart}/${newRowEnd}`;
    resizeElement.style.gridColumn = `${newColStart}/${newColEnd}`;
  }

  /**
   * Handle resize end (mouse)
   */
  function handleResizeEnd(e) {
    document.removeEventListener('mousemove', handleResizeMove);
    document.removeEventListener('mouseup', handleResizeEnd);
    finalizeResize();
  }

  /**
   * Handle resize end (touch)
   */
  function handleResizeTouchEnd(e) {
    document.removeEventListener('touchmove', handleResizeTouchMove);
    document.removeEventListener('touchend', handleResizeTouchEnd);
    finalizeResize();
  }

  /**
   * Finalize resize operation
   */
  function finalizeResize() {
    if (!isResizing || !resizeElement) return;

    // Remove visual feedback
    resizeElement.classList.remove('resizing');
    resizeElement.style.transition = '';

    // Check if size changed
    const newGridRow = resizeElement.style.gridRow;
    const newGridColumn = resizeElement.style.gridColumn;

    if (newGridRow !== resizeStartGridRow || newGridColumn !== resizeStartGridColumn) {
      // Update ElementManager
      if (typeof window.ElementManager !== 'undefined') {
        window.ElementManager.updatePosition(resizeElementId, {
          gridRow: newGridRow,
          gridColumn: newGridColumn
        });
      }

      console.log(`DragDrop: Resized ${resizeElementId} to row:${newGridRow} col:${newGridColumn}`);
    }

    // Reset state
    isResizing = false;
    resizeElement = null;
    resizeElementId = null;
    resizeHandle = null;
    resizeSlide = null;
  }

  /**
   * Remove resize handles from element
   *
   * @param {string} elementId - Element ID
   */
  function removeResizable(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.classList.remove('resizable');
    element.querySelectorAll('.resize-handle').forEach(h => h.remove());
  }

  // ===== KEYBOARD SUPPORT =====

  // Arrow key nudging for selected elements
  document.addEventListener('keydown', (e) => {
    // Only when not typing in an input
    if (e.target.closest('input, textarea, [contenteditable="true"]')) {
      return;
    }

    // Only in edit mode
    if (document.body.getAttribute('data-mode') !== 'edit') {
      return;
    }

    // Get selected element
    const selected = window.ElementManager?.getSelectedElement();
    if (!selected) return;

    const element = document.getElementById(selected.id);
    if (!element) return;

    const [rowStart, rowEnd] = parseGridSpan(element.style.gridRow);
    const [colStart, colEnd] = parseGridSpan(element.style.gridColumn);
    const rowSpan = rowEnd - rowStart;
    const colSpan = colEnd - colStart;

    let newRowStart = rowStart;
    let newColStart = colStart;

    switch (e.key) {
      case 'ArrowUp':
        newRowStart = Math.max(1, rowStart - 1);
        break;
      case 'ArrowDown':
        newRowStart = Math.min(GRID_ROWS - rowSpan + 1, rowStart + 1);
        break;
      case 'ArrowLeft':
        newColStart = Math.max(1, colStart - 1);
        break;
      case 'ArrowRight':
        newColStart = Math.min(GRID_COLS - colSpan + 1, colStart + 1);
        break;
      case 'Delete':
      case 'Backspace':
        e.preventDefault();
        window.ElementManager?.deleteElement(selected.id);
        return;
      default:
        return;
    }

    e.preventDefault();

    const newGridRow = `${newRowStart}/${newRowStart + rowSpan}`;
    const newGridColumn = `${newColStart}/${newColStart + colSpan}`;

    setPosition(selected.id, newGridRow, newGridColumn);
  });

  // ===== EXPOSE API =====

  window.DragDrop = {
    makeDraggable: makeDraggable,
    makeResizable: makeResizable,
    removeResizable: removeResizable,
    getPosition: getPosition,
    setPosition: setPosition,
    setGridSnap: setGridSnap,

    // Constants for external use
    GRID_COLS: GRID_COLS,
    GRID_ROWS: GRID_ROWS
  };

  console.log('DragDrop initialized');

})();
