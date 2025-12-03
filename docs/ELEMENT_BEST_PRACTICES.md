# Element Best Practices Guide

## Overview

This document captures the design principles and implementation patterns learned from building dynamic slide elements (text boxes, images, charts, tables, etc.). Use this as a reference when adding new element types to ensure consistency and avoid relearning past lessons.

---

## Table of Contents

1. [Element Lifecycle](#1-element-lifecycle)
2. [DOM Structure](#2-dom-structure)
3. [Drag & Drop](#3-drag--drop)
4. [Resize Handles](#4-resize-handles)
5. [Selection & Deselection](#5-selection--deselection)
6. [PostMessage Events (Parent Frame Communication)](#6-postmessage-events-parent-frame-communication)
7. [Edit Mode Integration](#7-edit-mode-integration)
8. [Persistence & Auto-Save](#8-persistence--auto-save)
9. [Restoration on Page Load](#9-restoration-on-page-load)
10. [Backend API Requirements](#10-backend-api-requirements)
11. [UI/UX Best Practices](#11-uiux-best-practices)
12. [Common Pitfalls & Solutions](#12-common-pitfalls--solutions)
13. [Checklist for New Elements](#13-checklist-for-new-elements)

---

## 1. Element Lifecycle

Every dynamic element follows this lifecycle:

```
CREATE → INTERACT → SAVE → RELOAD → RESTORE
```

| Phase | Description | Key Functions |
|-------|-------------|---------------|
| CREATE | User adds element via UI or API | `insertElement()` |
| INTERACT | User drags, resizes, edits content | Event handlers |
| SAVE | Auto-save or manual save to backend | `collectElementData()`, API call |
| RELOAD | Page refresh or navigation | Server renders HTML |
| RESTORE | Rebuild elements from saved data | `restoreElements()` |

### Critical Insight
> Elements must be restored EXACTLY as they were saved. This means position, size, content, styles, and state (locked, visible) must all persist.

---

## 2. DOM Structure

### Standard Element Container Structure

```html
<div id="{type}-{timestamp}-{random}"
     class="dynamic-element inserted-{type}"
     data-element-type="{type}"
     data-slide-index="{slideIndex}"
     style="grid-row: {row}; grid-column: {col}; z-index: {z};">

  <!-- Drag Handle (optional, for complex elements) -->
  <div class="{type}-drag-handle">⋮⋮</div>

  <!-- Content Area -->
  <div class="{type}-content" contenteditable="true|false">
    {content}
  </div>

  <!-- Resize Handles (added dynamically) -->
  <div class="resize-handle resize-handle-se">↘</div>
  <!-- ... other corners ... -->
</div>
```

### Naming Conventions

| Item | Pattern | Example |
|------|---------|---------|
| Element ID | `{type}-{timestamp36}-{random6}` | `textbox-m3k9f2-a8b3c1` |
| Container class | `inserted-{type}` | `inserted-textbox`, `inserted-image` |
| Content class | `{type}-content` | `textbox-content`, `image-content` |
| Data attribute | `data-element-type` | `textbox`, `image`, `chart` |

### CSS Class States

```css
.inserted-{type}                    /* Base state */
.inserted-{type}.element-selected   /* User has selected */
.inserted-{type}.dragging           /* Currently being dragged */
.inserted-{type}.resizing           /* Currently being resized */
.inserted-{type}.{type}-editing     /* Content is being edited */
.inserted-{type}.{type}-locked      /* Cannot be moved/edited */
.inserted-{type}.{type}-hidden      /* Visibility toggled off */
```

---

## 3. Drag & Drop

### Implementation Pattern

```javascript
function makeDraggable(elementId) {
  const element = document.getElementById(elementId);

  // Find drag handle or use entire element
  const handle = element.querySelector('.{type}-drag-handle') || element;

  handle.addEventListener('mousedown', startDrag);

  function startDrag(e) {
    // IMPORTANT: Don't drag if clicking on interactive content
    if (e.target.isContentEditable ||
        e.target.tagName === 'INPUT' ||
        e.target.tagName === 'TEXTAREA') {
      return;
    }

    e.preventDefault();
    element.classList.add('dragging');

    // Track initial position
    const startX = e.clientX;
    const startY = e.clientY;
    const startRow = element.style.gridRow;
    const startCol = element.style.gridColumn;

    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
  }

  function onDrag(e) {
    // Calculate new grid position based on mouse movement
    // Update element.style.gridRow and element.style.gridColumn
  }

  function stopDrag(e) {
    element.classList.remove('dragging');
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);

    // IMPORTANT: Trigger auto-save after position change
    triggerAutoSave(slideIndex);
  }
}
```

### Key Learnings

1. **Drag Handle Separation**: For elements with editable content, use a separate drag handle (pill/bar at top) for guaranteed drag initiation.

2. **Threshold-Based Drag Detection (Click-to-Edit vs Drag-to-Move)**: Rather than blocking mousedown on content areas, use threshold detection to distinguish clicks from drags. This allows users to drag from anywhere on the element:
   ```javascript
   const DRAG_THRESHOLD = 5;  // pixels
   let pendingDrag = null;

   function handleMouseDown(e) {
     // Enter pending state - don't start drag yet
     pendingDrag = {
       element: e.currentTarget,
       startX: e.clientX,
       startY: e.clientY
     };
     document.addEventListener('mousemove', handlePendingMove);
     document.addEventListener('mouseup', handlePendingEnd);
   }

   function handlePendingMove(e) {
     const deltaX = Math.abs(e.clientX - pendingDrag.startX);
     const deltaY = Math.abs(e.clientY - pendingDrag.startY);
     const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

     if (distance >= DRAG_THRESHOLD) {
       // It's a drag - start actual drag operation
       window.getSelection()?.removeAllRanges();  // Clear text selection
       startDrag(pendingDrag.element, pendingDrag.startX, pendingDrag.startY);
       // Switch to drag listeners...
     }
   }

   function handlePendingEnd(e) {
     // It was a click (didn't move past threshold)
     // Focus content for editing
     contentEl.focus();
     selectElement(elementId);
     pendingDrag = null;
   }
   ```

3. **Grid-Based Positioning**: Use CSS Grid for positioning (`grid-row`, `grid-column`) not absolute pixels. This ensures responsive behavior.

4. **Visual Feedback During Drag**:
   - Add `.dragging` class for styling
   - Use `cursor: grabbing` (closed hand) to indicate element is "grabbed"
   - Add `user-select: none` to prevent accidental text selection
   ```css
   .inserted-textbox.dragging {
     cursor: grabbing !important;
     user-select: none !important;
     opacity: 0.9;
   }

   .inserted-textbox.dragging .textbox-content {
     pointer-events: none;
     user-select: none !important;
   }
   ```

5. **Drag Handle Still Works**: Even with threshold detection, the drag handle should start drag immediately (no threshold) for users who prefer that approach.

---

## 4. Resize Handles

### Implementation Pattern

```javascript
function makeResizable(elementId) {
  const element = document.getElementById(elementId);

  // Add handles to all corners
  const corners = ['nw', 'ne', 'sw', 'se'];
  corners.forEach(corner => {
    const handle = document.createElement('div');
    handle.className = `resize-handle resize-handle-${corner}`;
    handle.innerHTML = getResizeArrow(corner);
    element.appendChild(handle);

    handle.addEventListener('mousedown', (e) => startResize(e, corner));
  });
}
```

### Handle Positioning (CSS)

```css
.resize-handle {
  position: absolute;
  width: 24px;
  height: 24px;
  background: #1e40af;
  border: 2px solid white;
  border-radius: 4px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.resize-handle-nw { top: -12px; left: -12px; cursor: nwse-resize; }
.resize-handle-ne { top: -12px; right: -12px; cursor: nesw-resize; }
.resize-handle-sw { bottom: -12px; left: -12px; cursor: nesw-resize; }
.resize-handle-se { bottom: -12px; right: -12px; cursor: nwse-resize; }
```

### Key Learnings

1. **Visibility**: Only show handles in edit mode and when element is selected.

2. **Minimum Size**: Enforce minimum dimensions to prevent elements from becoming too small:
   ```javascript
   const minRows = 2;
   const minCols = 4;
   ```

3. **Aspect Ratio**: For images, hold Shift to maintain aspect ratio during resize.

4. **Content Scaling**: Decide if content scales with container or remains fixed size.

---

## 5. Selection & Deselection

### Selection State Management

```javascript
let selectedElementId = null;

function selectElement(elementId) {
  // Deselect previous
  deselectAll();

  const element = document.getElementById(elementId);
  if (element) {
    element.classList.add('element-selected');
    selectedElementId = elementId;

    // IMPORTANT: Emit postMessage to parent frame
    emitSelectionEvent(elementId);
  }
}

function deselectAll() {
  if (selectedElementId) {
    const element = document.getElementById(selectedElementId);
    if (element) {
      element.classList.remove('element-selected');
    }

    // IMPORTANT: Emit deselection event
    emitDeselectionEvent(selectedElementId);
  }
  selectedElementId = null;
}
```

### Deselection Triggers

```javascript
// Click outside any element
document.addEventListener('click', (e) => {
  if (!e.target.closest('.dynamic-element')) {
    deselectAll();
  }
});

// Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && selectedElementId) {
    deselectAll();
  }
});
```

### Key Learnings

1. **Click on Content = Selection**: When user clicks inside element content, ALSO trigger selection (for postMessage):
   ```javascript
   contentDiv.addEventListener('click', (e) => {
     e.stopPropagation();
     contentDiv.focus();
     selectElement(id);  // Don't forget this!
   });
   ```

2. **Selection Visual**: Clear visual indicator (border, shadow, handles visible) when selected.

---

## 6. PostMessage Events (Parent Frame Communication)

### Why PostMessage?

The slide viewer runs in an iframe. The parent application (React/Next.js) needs to know when elements are selected to show/hide formatting toolbars and panels.

### Required Events

#### Element Selected
```javascript
window.parent.postMessage({
  type: '{elementType}Selected',  // e.g., 'textBoxSelected', 'imageSelected'
  elementId: string,
  formatting: { ... } | null,     // Current formatting/properties
  properties: { ... }             // Position, size, etc.
}, '*');
```

#### Element Deselected
```javascript
window.parent.postMessage({
  type: '{elementType}Deselected',
  elementId: string  // Optional
}, '*');
```

### Formatting Object (for Text Elements)

```javascript
{
  fontFamily: string,
  fontSize: number,
  fontWeight: string,
  fontStyle: string,
  textDecoration: string,
  color: string,
  backgroundColor: string,
  textAlign: string,
  lineHeight: string,
  padding: { top, right, bottom, left },
  border: { width, color, style },
  borderRadius: { topLeft, topRight, bottomRight, bottomLeft }
}
```

### Properties Object (for All Elements)

```javascript
{
  position: { x: number, y: number },
  size: { width: number, height: number },
  rotation: number,
  locked: boolean,
  zIndex: number
}
```

### Implementation

```javascript
function emitSelectionEvent(elementId, data, element) {
  if (!window.parent || window.parent === window) return;

  if (data.type === 'textbox') {
    window.parent.postMessage({
      type: 'textBoxSelected',
      elementId: elementId,
      formatting: extractTextBoxFormatting(element)
    }, '*');
  } else if (data.type === 'image') {
    window.parent.postMessage({
      type: 'imageSelected',
      elementId: elementId,
      properties: extractElementProperties(element)
    }, '*');
  }
  // ... handle other types
}
```

### Key Learnings

1. **Check for Parent**: Always check `window.parent !== window` before posting.

2. **Emit on Every Click**: Even if already selected, re-emit to update formatting panel.

3. **Emit After Format Changes**: When formatting changes, emit updated event:
   ```javascript
   function emitFormattingUpdate() {
     if (selectedElementId) {
       emitSelectionEvent(selectedElementId, ...);
     }
   }
   ```

4. **Debug Logging**: Add console logs for debugging:
   ```javascript
   console.log('📤 postMessage: textBoxSelected', elementId);
   ```

---

## 7. Edit Mode Integration

### Mode Detection

```javascript
const isEditMode = document.body.dataset.mode === 'edit';
```

### Mode-Specific Behavior

| Feature | View Mode | Edit Mode |
|---------|-----------|-----------|
| contentEditable | `false` | `true` |
| Drag handles | Hidden | Visible |
| Resize handles | Hidden | Visible |
| Click behavior | Navigate/View | Select/Edit |
| Keyboard shortcuts | Disabled | Enabled |

### Toggling on Mode Change

```javascript
// When entering edit mode
function enableElementEditing() {
  document.querySelectorAll('.dynamic-element').forEach(el => {
    const content = el.querySelector('[class*="-content"]');
    if (content) {
      content.contentEditable = 'true';
    }
    // Show handles
    el.querySelectorAll('.resize-handle, .drag-handle').forEach(h => {
      h.style.display = 'flex';
    });
  });
}

// When exiting edit mode
function disableElementEditing() {
  document.querySelectorAll('.dynamic-element').forEach(el => {
    const content = el.querySelector('[class*="-content"]');
    if (content) {
      content.contentEditable = 'false';
    }
    // Hide handles
    el.querySelectorAll('.resize-handle, .drag-handle').forEach(h => {
      h.style.display = 'none';
    });
  });
}
```

### Key Learnings

1. **ContentEditable State**: Set `contentEditable` based on current mode at element creation AND when mode changes.

2. **Force Save on Exit**: Always save pending changes before exiting edit mode:
   ```javascript
   async function exitEditMode() {
     if (hasPendingChanges()) {
       await forceSave();
     }
     // ... rest of exit logic
   }
   ```

---

## 8. Persistence & Auto-Save

### Data Collection Pattern

```javascript
function collectElementData(slideElement, slideIndex) {
  const elements = [];

  slideElement.querySelectorAll('.inserted-{type}').forEach(el => {
    elements.push({
      id: el.id,
      position: {
        grid_row: el.style.gridRow,
        grid_column: el.style.gridColumn
      },
      z_index: parseInt(el.style.zIndex) || 1000,
      content: el.querySelector('.{type}-content')?.innerHTML || '',
      style: {
        background_color: el.style.backgroundColor,
        border_color: el.style.borderColor,
        border_width: parseInt(el.style.borderWidth) || 0,
        // ... other styles
      },
      locked: el.classList.contains('{type}-locked'),
      visible: !el.classList.contains('{type}-hidden')
    });
  });

  return elements;
}
```

### Auto-Save Integration

```javascript
// Trigger auto-save after any change
function triggerAutoSave(slideIndex) {
  if (typeof markContentChanged === 'function') {
    markContentChanged(slideIndex, 'element');
  }
}

// Call after: drag end, resize end, content edit, style change
```

### API Payload Structure

```javascript
{
  slides: [
    {
      slide_title: "...",
      rich_content: "...",
      text_boxes: [...],      // Array of text box data
      images: [...],          // Array of image data
      charts: [...],          // Array of chart data
      // ... other element types
    },
    // ... more slides
  ],
  updated_by: "user",
  change_summary: "Auto-save from editor"
}
```

### Key Learnings

1. **Element Data at Slide Level**: Store element arrays at the slide level, NOT inside the content object:
   ```javascript
   // CORRECT
   presentation.slides[i].text_boxes = [...]

   // WRONG
   presentation.slides[i].content.text_boxes = [...]
   ```

2. **Backend Model Must Accept Data**: Ensure the Pydantic model includes the field:
   ```python
   class SlideContentUpdate(BaseModel):
       text_boxes: Optional[List[TextBox]] = None
       images: Optional[List[Image]] = None
       # ...
   ```

3. **Batch Endpoint**: Use a single batch endpoint for auto-save efficiency:
   ```
   PUT /api/presentations/{id}/slides
   ```

---

## 9. Restoration on Page Load

### Server-Side: Inject Data into HTML

```python
# In view_presentation endpoint
html_content = html_content.replace(
    '// PRESENTATION_DATA_PLACEHOLDER',
    f'const PRESENTATION_DATA = {json.dumps(presentation)};'
)
```

### Client-Side: Restore Elements

```javascript
function restoreElements(slides) {
  slides.forEach((slide, slideIndex) => {
    // Restore text boxes
    if (slide.text_boxes?.length > 0) {
      slide.text_boxes.forEach(tb => {
        ElementManager.insertTextBox(slideIndex, {
          id: tb.id,              // IMPORTANT: Use saved ID
          position: tb.position,
          content: tb.content,
          style: tb.style,
          zIndex: tb.z_index,
          locked: tb.locked,
          visible: tb.visible
        });
      });
    }

    // Restore images, charts, etc.
    // ...
  });
}
```

### Key Learnings

1. **Preserve IDs**: When restoring, pass the saved ID to maintain element identity:
   ```javascript
   const id = config.id || generateId('textbox');  // Use saved or generate new
   ```

2. **Skip Auto-Save on Restore**: Don't trigger auto-save when restoring:
   ```javascript
   if (!config.id) {  // Only new elements trigger save
     triggerAutoSave(slideIndex);
   }
   ```

3. **URL Pattern Matching**: Ensure `getPresentationId()` matches actual URL pattern:
   ```javascript
   // If URL is /p/{id}
   const match = path.match(/\/p\/([^\/]+)/);

   // If URL is /viewer/{id}
   const match = path.match(/\/viewer\/([^\/]+)/);
   ```

---

## 10. Backend API Requirements

### Required Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/presentations/{id}/slides` | PUT | Batch update all slides (auto-save) |
| `/api/presentations/{id}/slides/{index}` | PUT | Update single slide |
| `/api/presentations/{id}/slides/{index}/{elements}` | GET | Get elements for slide |
| `/api/presentations/{id}/slides/{index}/{elements}` | POST | Add element to slide |
| `/api/presentations/{id}/slides/{index}/{elements}/{id}` | PUT | Update specific element |
| `/api/presentations/{id}/slides/{index}/{elements}/{id}` | DELETE | Delete element |

### Pydantic Models

```python
class ElementPosition(BaseModel):
    grid_row: str = "6/12"
    grid_column: str = "5/28"

class ElementStyle(BaseModel):
    background_color: Optional[str] = "transparent"
    border_color: Optional[str] = "transparent"
    border_width: Optional[int] = 0
    border_radius: Optional[int] = 0
    padding: Optional[int] = 16
    opacity: Optional[float] = 1.0
    box_shadow: Optional[str] = None

class BaseElement(BaseModel):
    id: str
    position: ElementPosition
    z_index: int = 1000
    locked: bool = False
    visible: bool = True

class TextBox(BaseElement):
    content: str = ""
    style: ElementStyle = ElementStyle()

class ImageElement(BaseElement):
    image_url: str
    alt_text: Optional[str] = ""
    object_fit: str = "cover"
```

---

## 11. UI/UX Best Practices

### Delete Button Pattern

Show a delete button that appears only on hover/selection:

```javascript
// Create delete button
const deleteBtn = document.createElement('button');
deleteBtn.className = 'delete-button';
deleteBtn.innerHTML = '×';
deleteBtn.title = 'Delete text box';
deleteBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  deleteElement(id);
});
container.appendChild(deleteBtn);
```

```css
.inserted-textbox .delete-button {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 22px;
  height: 22px;
  background: #ef4444;
  color: white;
  border: 2px solid white;
  border-radius: 50%;
  cursor: pointer;
  opacity: 0;  /* Hidden by default */
  transition: opacity 0.15s ease;
  z-index: 1002;
}

.inserted-textbox:hover .delete-button,
.inserted-textbox.element-selected .delete-button {
  opacity: 1;  /* Show on hover/selection */
}
```

### Drag Handle Pattern

For cleaner UI, hide drag handles by default and show on hover:

```css
.textbox-drag-handle {
  opacity: 0;  /* Hidden by default */
  transition: opacity 0.15s ease;
}

.inserted-textbox:hover .textbox-drag-handle,
.inserted-textbox.element-selected .textbox-drag-handle {
  opacity: 1;  /* Show on hover/selection */
}
```

### Keyboard Shortcuts (Cross-Platform)

Support both Mac (Cmd) and Windows/Linux (Ctrl):

```javascript
document.addEventListener('keydown', (e) => {
  // Check if user is typing in an editable area
  const isEditing = e.target.isContentEditable ||
                    e.target.tagName === 'INPUT' ||
                    e.target.tagName === 'TEXTAREA';

  // Modifier key check (Cmd on Mac, Ctrl on Windows/Linux)
  const modKey = e.metaKey || e.ctrlKey;

  // Delete/Backspace - Delete selected element (only if not editing)
  if ((e.key === 'Delete' || e.key === 'Backspace') && selectedElementId && !isEditing) {
    e.preventDefault();
    deleteElement(selectedElementId);
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

  // Ctrl/Cmd + Z - Undo
  if (modKey && e.key === 'z' && !e.shiftKey && !isEditing) {
    window.parent?.postMessage({ type: 'undoRequested' }, '*');
    return;
  }

  // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y - Redo
  if (modKey && (e.key === 'y' || (e.shiftKey && e.key === 'z')) && !isEditing) {
    window.parent?.postMessage({ type: 'redoRequested' }, '*');
    return;
  }
});
```

### Clipboard Implementation

```javascript
let clipboardData = null;

function copyElement() {
  if (!selectedElementId) return { success: false };

  const data = elementRegistry.get(selectedElementId);
  const element = document.getElementById(selectedElementId);

  if (data.type === 'textbox') {
    const contentDiv = element.querySelector('.textbox-content');
    clipboardData = {
      type: 'textbox',
      content: contentDiv?.innerHTML || '',
      position: { ...data.position },
      style: { ...data.data.style }
    };
    return { success: true };
  }
  return { success: false };
}

function cutElement() {
  const result = copyElement();
  if (result.success) {
    deleteElement(selectedElementId);
  }
  return result;
}

function pasteElement() {
  if (!clipboardData) return { success: false };

  // Offset position slightly for visibility
  const position = { ...clipboardData.position };
  const rowParts = position.gridRow.split('/');
  const colParts = position.gridColumn.split('/');
  position.gridRow = `${parseInt(rowParts[0]) + 1}/${parseInt(rowParts[1]) + 1}`;
  position.gridColumn = `${parseInt(colParts[0]) + 1}/${parseInt(colParts[1]) + 1}`;

  const result = insertTextBox(currentSlideIndex, {
    position,
    content: clipboardData.content,
    style: clipboardData.style
  });

  if (result.success) {
    selectElement(result.elementId);
  }
  return result;
}
```

---

## 12. Common Pitfalls & Solutions

### Pitfall 1: Elements Not Persisting

**Symptoms**: Elements disappear on page refresh

**Causes & Solutions**:
| Cause | Solution |
|-------|----------|
| Backend model missing field | Add field to Pydantic model |
| Data stored in wrong location | Store at slide level, not in content |
| Batch endpoint missing | Add `PUT /api/.../slides` endpoint |
| URL pattern mismatch | Fix regex in `getPresentationId()` |
| Server not restarted | Restart after backend changes |

### Pitfall 2: Element Deletions Not Persisting

**Symptoms**: Deleted elements reappear on page refresh

**Root Cause**: The `collectSlideContent()` function was only including `text_boxes` in the update payload when there were text boxes present. When all were deleted, the field wasn't sent, so the backend kept the old data.

**Solution**: ALWAYS include the element array in the save payload, even when empty:

```javascript
// ❌ WRONG - deletions won't persist
const textBoxes = collectTextBoxes(slideElement, index);
if (textBoxes.length > 0) {
  update.text_boxes = textBoxes;
}

// ✅ CORRECT - empty array tells backend to clear
const textBoxes = collectTextBoxes(slideElement, index);
update.text_boxes = textBoxes;  // Always include, even if []
```

**Key Insight**: The backend replaces the entire array:
```python
if "text_boxes" in slide_update:
    presentation["slides"][i]["text_boxes"] = slide_update.pop("text_boxes")
```

So sending `text_boxes: []` correctly clears all text boxes, but omitting `text_boxes` entirely means the backend keeps whatever was there before.

### Pitfall 3: Drag Not Working

**Symptoms**: Can't drag element, or content gets selected instead

**Solutions**:
- Add separate drag handle for elements with editable content
- Stop mousedown propagation on content area
- Check that drag handle has correct cursor style

### Pitfall 4: PostMessage Not Received

**Symptoms**: Format panel doesn't appear when selecting element

**Solutions**:
- Check `window.parent !== window` before posting
- Verify event type matches frontend listener
- Check browser console for postMessage logs
- Ensure selection triggers on content click too

### Pitfall 5: ContentEditable Not Working After Mode Toggle

**Symptoms**: Can't edit text after switching modes

**Solutions**:
- Re-set `contentEditable` attribute when mode changes
- Don't just add/remove CSS class, actually set the attribute
- Check for restored elements that might have wrong initial state

### Pitfall 6: Z-Index Issues

**Symptoms**: Elements appear behind other elements

**Solutions**:
- Use elevated z-index range for dynamic elements (1000+)
- Implement bring-to-front/send-to-back functions
- Track z-index counter separately per element type

---

## 13. Checklist for New Elements

Use this checklist when implementing a new element type:

### Setup
- [ ] Create element model in `models.py`
- [ ] Add field to `SlideContentUpdate` model
- [ ] Update batch endpoint to handle new element type
- [ ] Create CSS file `src/styles/{element}.css`

### DOM & Styling
- [ ] Define container structure with standard classes
- [ ] Add drag handle (if has editable content)
- [ ] Style for all states: default, selected, dragging, editing, locked

### Interaction
- [ ] Implement `insert{Element}()` function
- [ ] Add click handler for selection
- [ ] Add content click handler (stopPropagation + selectElement)
- [ ] Implement drag-drop via `DragDrop.makeDraggable()`
- [ ] Implement resize via `DragDrop.makeResizable()`
- [ ] Add keyboard shortcuts if needed

### PostMessage Events
- [ ] Emit `{element}Selected` with properties/formatting
- [ ] Emit `{element}Deselected` on deselection
- [ ] Add console.log for debugging
- [ ] Document event structure for frontend team

### Edit Mode
- [ ] Toggle contentEditable based on mode
- [ ] Show/hide handles based on mode
- [ ] Disable interaction in view mode

### Persistence
- [ ] Implement `collect{Element}Data()` function
- [ ] Trigger auto-save on all changes
- [ ] Handle element data in batch endpoint
- [ ] Store at slide level (not in content)

### Restoration
- [ ] Implement `restore{Elements}()` function
- [ ] Pass saved ID during restoration
- [ ] Skip auto-save trigger on restoration
- [ ] Test full cycle: create → save → reload → verify

### Testing
- [ ] Test create new element
- [ ] Test drag and drop
- [ ] Test resize
- [ ] Test content editing
- [ ] Test selection/deselection
- [ ] Test postMessage events
- [ ] Test persistence (save → refresh → verify)
- [ ] Test in both edit and view modes

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2024-12-02 | Added Section 11 (UI/UX Best Practices): delete button pattern, drag handle hover visibility, keyboard shortcuts (cross-platform), clipboard implementation. Added Pitfall 2: Element Deletions Not Persisting |
| 1.1 | 2024-12-02 | Added threshold-based drag detection (click-to-edit vs drag-to-move), grabbing cursor feedback |
| 1.0 | 2024-12-02 | Initial document based on text box implementation |

---

## Contributing

When you encounter new issues or discover better patterns, update this document:

1. Add to "Common Pitfalls" section
2. Update relevant sections with new learnings
3. Add to checklist if new requirement discovered
4. Update version history
