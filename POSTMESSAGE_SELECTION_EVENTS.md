# Layout Service: Selection Events Implementation

## Summary

The Layout Service (iframe) now emits `postMessage` events to the parent window when elements are selected or deselected. This enables the frontend's `TextBoxFormatPanel` to automatically show/hide based on user interactions within the slide.

---

## Events Implemented

### 1. `textBoxSelected`

Emitted when a text box is clicked or receives focus.

```javascript
window.parent.postMessage({
  type: 'textBoxSelected',
  elementId: 'textbox-xxx-yyy',
  formatting: {
    fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
    fontSize: 32,
    fontWeight: '400',
    fontStyle: 'normal',
    textDecoration: 'none',
    color: 'rgb(31, 41, 55)',
    backgroundColor: 'transparent',
    textAlign: 'start',
    lineHeight: '48px',
    padding: { top: 16, right: 16, bottom: 16, left: 16 },
    border: { width: 0, color: 'transparent', style: 'none' },
    borderRadius: { topLeft: 0, topRight: 0, bottomRight: 0, bottomLeft: 0 }
  }
}, '*')
```

### 2. `textBoxDeselected`

Emitted when a text box is deselected (click elsewhere, ESC key, or select another element).

```javascript
window.parent.postMessage({
  type: 'textBoxDeselected'
}, '*')
```

### 3. `elementSelected` (for other element types)

Emitted when a non-textbox element (image, table, chart, shape) is selected.

```javascript
window.parent.postMessage({
  type: 'elementSelected',
  elementId: 'image-xxx-yyy',
  elementType: 'image', // or 'table', 'chart', 'shape'
  properties: {
    position: { x: 100, y: 200 },
    size: { width: 400, height: 300 },
    rotation: 0,
    locked: false,
    zIndex: 101
  }
}, '*')
```

### 4. `elementDeselected`

Emitted when a non-textbox element is deselected.

```javascript
window.parent.postMessage({
  type: 'elementDeselected',
  elementId: 'image-xxx-yyy'
}, '*')
```

---

## Trigger Conditions

| User Action | Event Emitted |
|-------------|---------------|
| Click on text box | `textBoxSelected` |
| Click inside text box content | `textBoxSelected` |
| Click on image/table/chart/shape | `elementSelected` |
| Click on empty slide area | `textBoxDeselected` or `elementDeselected` |
| Press Escape key | `textBoxDeselected` or `elementDeselected` |
| Select a different element | Deselection of previous + Selection of new |

---

## Debug Logging

Console logs are emitted for each postMessage event:
- `📤 postMessage: textBoxSelected <elementId>`
- `📤 postMessage: textBoxDeselected`
- `📤 postMessage: elementSelected <type> <elementId>`
- `📤 postMessage: elementDeselected <elementId>`

---

## Additional API

Two new functions exposed via `window.ElementManager`:

### `emitFormattingUpdate()`
Call this after programmatically changing text box formatting to re-emit the `textBoxSelected` event with updated formatting values.

```javascript
// After applying formatting changes
window.ElementManager.emitFormattingUpdate();
```

### `extractTextBoxFormatting(element)`
Extract current formatting from a text box DOM element.

```javascript
const formatting = window.ElementManager.extractTextBoxFormatting(textboxElement);
```

---

## File Modified

`src/utils/element-manager.js`

### Changes Made:
1. Added `extractTextBoxFormatting()` helper function
2. Added `extractElementProperties()` helper function
3. Added `emitSelectionEvent()` to emit postMessage on selection
4. Added `emitDeselectionEvent()` to emit postMessage on deselection
5. Modified `selectElement()` to call `emitSelectionEvent()`
6. Modified `deselectAll()` to call `emitDeselectionEvent()`
7. Modified text box content click handler to also trigger selection
8. Added ESC key handler for deselection
9. Exposed `emitFormattingUpdate()` and `extractTextBoxFormatting()` in API

---

## Testing Checklist

- [x] Click on text box -> `textBoxSelected` emitted
- [x] Click inside text box content -> `textBoxSelected` emitted
- [x] Click on empty slide -> `textBoxDeselected` emitted
- [x] Press ESC key -> `textBoxDeselected` emitted
- [x] Click on restored text box (after page reload) -> `textBoxSelected` emitted
- [x] Select different element -> Previous deselected, new selected
- [x] Formatting object includes all required properties

---

## Frontend Integration

The frontend is already listening at `presentation-viewer.tsx:1236-1260`. These events will automatically trigger the `TextBoxFormatPanel` to show/hide.

No frontend changes required - just deploy the updated Layout Service.
