# Text Box Cross-Origin API Reference

**Version**: 1.2
**Last Updated**: 2025-12-01
**For**: Frontend Team Integration

This document describes the complete postMessage API for managing text boxes in the presentation viewer iframe.

---

## Table of Contents

1. [Overview](#overview)
2. [Visual Design](#visual-design)
3. [Basic Communication Pattern](#basic-communication-pattern)
4. [Text Box CRUD Operations](#text-box-crud-operations)
5. [Text Formatting](#text-formatting)
6. [Box Styling](#box-styling)
7. [Position & Size](#position--size)
8. [State Management](#state-management)
9. [AI Content Generation](#ai-content-generation)
10. [Persistence & Restoration](#persistence--restoration)
11. [Backend REST API](#backend-rest-api)
12. [Examples](#examples)

---

## Overview

Text boxes are overlay elements that float above slide content with:
- **Elevated z-index** (1000+) - always on top of layout content
- **4-point resize handles** - left, right, bottom, and bottom-right corner
- **Draggable** within the slide grid (32×18 grid system)
- **Rich text editing** via contentEditable
- **Full formatting control** via cross-origin postMessage API
- **Auto-save** - changes are automatically persisted
- **Auto-restore** - text boxes are restored with full interactivity on page load

### Default Style
- **Border**: Grey dashed (`#6b7280`) in edit mode, hidden in view mode
- **Background**: Transparent
- **Text color**: Dark grey (`#374151`)
- **Font size**: 32px

---

## Visual Design

### Edit Mode Appearance

```
                    ┌─────────────────────────────────────────────────────┐
                    │           ┌──────────┐                              │
                    │           │  ⋮⋮      │  ← Light blue drag handle    │
                    │           └──────────┘    (62×26px pill)            │
┌────┐              │                                                     │              ┌────┐
│ ◀  │ ←───────────▶│         Click to edit text                         │◀────────────▶│ ▶  │
└────┘  Left handle │                                                     │ Right handle └────┘
        (42×42px)   │                                                     │  (42×42px)
                    │                                                     │
                    │  Grey dashed border (3px #6b7280)                   │
                    │                                                     │
                    └───────────────────────┬─────────────────────────────┘
                                            │                        ┌────┐
                                       ┌────┤                        │ ↘  │
                                       │ ▼  │ Bottom handle          └────┘
                                       └────┘ (42×42px)           Corner handle
                                                                    (48×48px)
```

### Handle Specifications

| Handle | Size | Position | Color | Shape |
|--------|------|----------|-------|-------|
| **Drag handle** | 62×26px | Top center, inside box | Light blue `#60a5fa` | Rounded pill |
| **Left (w)** | 42×42px | Left edge, half in/half out | Dark blue `#1e40af` | Square |
| **Right (e)** | 42×42px | Right edge, half in/half out | Dark blue `#1e40af` | Square |
| **Bottom (s)** | 42×42px | Bottom edge, half in/half out | Dark blue `#1e40af` | Square |
| **Bottom-right (se)** | 48×48px | Corner, half in/half out | Dark blue `#1e40af` | Square |

### View Mode
In view/present mode, text boxes are **completely transparent**:
- No border
- No handles
- No shadow
- Only the text content is visible

---

## Basic Communication Pattern

### Sending Commands

```javascript
// Get reference to the presentation iframe
const iframe = document.getElementById('presentation-iframe');

// Send a command
iframe.contentWindow.postMessage({
  action: 'insertTextBox',
  params: {
    gridRow: '5/10',
    gridColumn: '3/15'
  }
}, '*');  // Or specify origin for security
```

### Receiving Responses

```javascript
window.addEventListener('message', (event) => {
  // Validate origin if needed
  // if (event.origin !== 'expected-origin') return;

  const response = event.data;

  if (response.success) {
    console.log('Command succeeded:', response);
    // response.elementId - for insert operations
    // response.content - for get operations
    // response.formatting - for getTextBoxFormatting
  } else {
    console.error('Command failed:', response.error);
  }
});
```

---

## Text Box CRUD Operations

### insertTextBox

Create a new text box on a slide.

```javascript
iframe.contentWindow.postMessage({
  action: 'insertTextBox',
  params: {
    slideIndex: 0,              // Optional, defaults to current slide
    gridRow: '5/10',            // CSS grid-row (start/end)
    gridColumn: '3/15',         // CSS grid-column (start/end)
    content: '<p>Hello</p>',    // Optional, initial HTML content
    zIndex: 1001,               // Optional, defaults to auto-increment from 1000
    resizable: true,            // Optional, default true
    draggable: true,            // Optional, default true
    locked: false,              // Optional, default false
    visible: true               // Optional, default true
  }
}, '*');
```

**Response:**
```javascript
{
  success: true,
  action: 'insertTextBox',
  elementId: 'textbox-a1b2c3d4e5f6',
  slideIndex: 0
}
```

**Note:** When restoring text boxes, you can pass an `id` parameter to reuse the saved ID:
```javascript
params: {
  id: 'textbox-existing-id',  // Reuse existing ID (for restoration)
  // ... other params
}
```

### updateTextBoxContent

Update the HTML content of a text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'updateTextBoxContent',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    content: '<p><strong>Updated</strong> content</p>'
  }
}, '*');
```

### getTextBoxContent

Get the current HTML content of a text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'getTextBoxContent',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6'
  }
}, '*');
```

**Response:**
```javascript
{
  success: true,
  content: '<p><strong>Updated</strong> content</p>'
}
```

### getTextBoxes

Get all text boxes on a slide.

```javascript
iframe.contentWindow.postMessage({
  action: 'getTextBoxes',
  params: {
    slideIndex: 0  // Optional, defaults to current slide
  }
}, '*');
```

**Response:**
```javascript
{
  success: true,
  textBoxes: [
    { id: 'textbox-a1b2c3d4e5f6', gridRow: '5/10', gridColumn: '3/15' },
    { id: 'textbox-b2c3d4e5f6a1', gridRow: '12/16', gridColumn: '18/30' }
  ]
}
```

### deleteTextBox

Delete a text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'deleteTextBox',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6'
  }
}, '*');
```

### selectTextBox / deselectTextBox

Select or deselect a text box (shows selection outline).

```javascript
// Select
iframe.contentWindow.postMessage({
  action: 'selectTextBox',
  params: { elementId: 'textbox-a1b2c3d4e5f6' }
}, '*');

// Deselect
iframe.contentWindow.postMessage({
  action: 'deselectTextBox',
  params: {}
}, '*');
```

### bringTextBoxToFront / sendTextBoxToBack

Change z-index ordering.

```javascript
iframe.contentWindow.postMessage({
  action: 'bringTextBoxToFront',
  params: { elementId: 'textbox-a1b2c3d4e5f6' }
}, '*');

iframe.contentWindow.postMessage({
  action: 'sendTextBoxToBack',
  params: { elementId: 'textbox-a1b2c3d4e5f6' }
}, '*');
```

---

## Text Formatting

### applyTextFormatCommand

Apply rich text formatting using document.execCommand (works on selected text).

```javascript
// Bold
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',  // Optional, focuses the text box first
    command: 'bold'
  }
}, '*');

// Italic
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'italic' }
}, '*');

// Underline
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'underline' }
}, '*');

// Strikethrough
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'strikeThrough' }
}, '*');

// Subscript / Superscript
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'subscript' }
}, '*');

// Insert ordered/unordered list
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'insertUnorderedList' }
}, '*');

// Font color (on selection)
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'foreColor', value: '#ff0000' }
}, '*');

// Background/highlight color
iframe.contentWindow.postMessage({
  action: 'applyTextFormatCommand',
  params: { command: 'hiliteColor', value: '#ffff00' }
}, '*');
```

**Available commands:** `bold`, `italic`, `underline`, `strikeThrough`, `subscript`, `superscript`, `insertUnorderedList`, `insertOrderedList`, `indent`, `outdent`, `justifyLeft`, `justifyCenter`, `justifyRight`, `justifyFull`, `foreColor`, `hiliteColor`, `fontName`, `fontSize`, `removeFormat`

### setTextBoxFont

Set the font family for the entire text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxFont',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    fontFamily: 'Georgia, serif'
  }
}, '*');
```

### setTextBoxFontSize

Set the font size for the entire text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxFontSize',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    fontSize: 24  // Can be number (px) or string ('1.5rem')
  }
}, '*');
```

### setTextBoxColor

Set the text color for the entire text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxColor',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    color: '#1f2937'
  }
}, '*');
```

### setTextBoxAlignment

Set text alignment.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxAlignment',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    alignment: 'center'  // 'left', 'center', 'right', 'justify'
  }
}, '*');
```

### setTextBoxLineHeight

Set line height/spacing.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxLineHeight',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    lineHeight: '1.8'  // Can be number or string
  }
}, '*');
```

### setTextBoxLetterSpacing

Set letter spacing.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxLetterSpacing',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    letterSpacing: 2  // Can be number (px) or string
  }
}, '*');
```

### setTextBoxFontWeight

Set font weight for the entire text box.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxFontWeight',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    fontWeight: '600'  // '400', '500', '600', '700', 'normal', 'bold'
  }
}, '*');
```

### setTextBoxVerticalAlignment

Set vertical text alignment within the text box content area.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxVerticalAlignment',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    verticalAlignment: 'middle'  // 'top', 'middle', 'bottom'
  }
}, '*');
```

**Implementation:** Uses flexbox on `.textbox-content` with `justify-content: flex-start | center | flex-end`.

### setTextBoxParagraphSpacing

Set spacing before and after paragraphs.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxParagraphSpacing',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    marginTop: '10pt',      // Optional, spacing before paragraphs
    marginBottom: '12pt'    // Optional, spacing after paragraphs
  }
}, '*');
```

**Implementation:** Uses CSS custom properties `--para-margin-top` and `--para-margin-bottom`.

### setTextBoxColumns

Set multi-column text layout.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxColumns',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    columns: 2,           // 1-4 columns
    columnGap: '20px'     // Optional, default '20px'
  }
}, '*');
```

### setTextBoxIndents

Set text indentation (first line, left margin, right margin).

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxIndents',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    firstIndent: '20pt',   // Optional, first line indent
    leftIndent: '10pt',    // Optional, left margin
    rightIndent: '10pt'    // Optional, right margin
  }
}, '*');
```

---

## Box Styling

### setTextBoxBackground

Set background color or gradient.

```javascript
// Solid color
iframe.contentWindow.postMessage({
  action: 'setTextBoxBackground',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    backgroundColor: '#f3f4f6'
  }
}, '*');

// Gradient
iframe.contentWindow.postMessage({
  action: 'setTextBoxBackground',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    backgroundGradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  }
}, '*');

// Transparent (reset)
iframe.contentWindow.postMessage({
  action: 'setTextBoxBackground',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    backgroundColor: 'transparent'
  }
}, '*');
```

### setTextBoxBorder

Set border properties.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxBorder',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    borderWidth: 2,           // px
    borderColor: '#3b82f6',
    borderStyle: 'solid',     // 'solid', 'dashed', 'dotted', 'none'
    borderRadius: 8           // px
  }
}, '*');
```

### setTextBoxPadding

Set internal padding.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxPadding',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    padding: 24  // Can be number (px) or string ('16px 24px')
  }
}, '*');
```

### setTextBoxOpacity

Set opacity (0-1).

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxOpacity',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    opacity: 0.9
  }
}, '*');
```

### setTextBoxShadow

Set box shadow.

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxShadow',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
  }
}, '*');

// Remove shadow
iframe.contentWindow.postMessage({
  action: 'setTextBoxShadow',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    boxShadow: 'none'
  }
}, '*');
```

### setTextBoxAutosize

Enable/disable automatic text box sizing based on content.

```javascript
// Enable autosize (height adjusts to content)
iframe.contentWindow.postMessage({
  action: 'setTextBoxAutosize',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    autosize: true
  }
}, '*');

// Disable autosize (fixed height, content scrolls if overflow)
iframe.contentWindow.postMessage({
  action: 'setTextBoxAutosize',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    autosize: false
  }
}, '*');
```

**Behavior:**
- `autosize: true` - Sets `height: auto`, `minHeight: 60px`, `overflow: visible`
- `autosize: false` - Resets height, sets `overflow: auto`

### setTextBoxBorderPositions

Control which sides of the text box have borders.

```javascript
// Only bottom border
iframe.contentWindow.postMessage({
  action: 'setTextBoxBorderPositions',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    positions: ['bottom']
  }
}, '*');

// Left and right borders
iframe.contentWindow.postMessage({
  action: 'setTextBoxBorderPositions',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    positions: ['left', 'right']
  }
}, '*');

// All borders
iframe.contentWindow.postMessage({
  action: 'setTextBoxBorderPositions',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    positions: ['top', 'right', 'bottom', 'left']
  }
}, '*');
```

**Note:** Uses existing border width, style, and color from `data-borderWidth`, `data-borderStyle`, `data-borderColor` attributes (set by `setTextBoxBorder`). Defaults to `2px solid #6b7280`.

### setTextBoxBorderOffset

Set the space between content and border (additional padding when border is active).

```javascript
iframe.contentWindow.postMessage({
  action: 'setTextBoxBorderOffset',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    offset: '6pt'  // e.g., '6pt', '10px', '0.5em'
  }
}, '*');
```

### getTextBoxFormatting

Get all current formatting properties.

```javascript
iframe.contentWindow.postMessage({
  action: 'getTextBoxFormatting',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6'
  }
}, '*');
```

**Response:**
```javascript
{
  success: true,
  formatting: {
    // Text properties
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: '32px',
    fontWeight: '400',
    fontStyle: 'normal',
    textDecoration: 'none',
    color: 'rgb(55, 65, 81)',
    textAlign: 'left',
    lineHeight: '1.5',
    letterSpacing: 'normal',
    // Box properties
    backgroundColor: 'transparent',
    borderWidth: '3px',
    borderColor: 'rgb(107, 114, 128)',
    borderStyle: 'dashed',
    borderRadius: '6px',
    padding: '16px',
    opacity: '1',
    boxShadow: 'none'
  }
}
```

---

## Position & Size

### resizeTextBox

Resize a text box by changing grid position.

```javascript
iframe.contentWindow.postMessage({
  action: 'resizeTextBox',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    gridRow: '3/12',      // New row span
    gridColumn: '2/20'    // New column span
  }
}, '*');
```

**Grid System:**
- 32 columns × 18 rows
- Base resolution: 1920×1080
- Format: `'start/end'` (1-indexed)

---

## State Management

### setTextBoxLocked

Lock/unlock a text box (prevents editing and interaction).

```javascript
// Lock
iframe.contentWindow.postMessage({
  action: 'setTextBoxLocked',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    locked: true
  }
}, '*');

// Unlock
iframe.contentWindow.postMessage({
  action: 'setTextBoxLocked',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    locked: false
  }
}, '*');
```

### setTextBoxVisible

Show/hide a text box.

```javascript
// Hide
iframe.contentWindow.postMessage({
  action: 'setTextBoxVisible',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    visible: false
  }
}, '*');

// Show
iframe.contentWindow.postMessage({
  action: 'setTextBoxVisible',
  params: {
    elementId: 'textbox-a1b2c3d4e5f6',
    visible: true
  }
}, '*');
```

---

## AI Content Generation

### generateTextBoxContent

Generate AI content for a text box (currently mock, will integrate with Text Service).

```javascript
iframe.contentWindow.postMessage({
  action: 'generateTextBoxContent',
  params: {
    prompt: 'Write a compelling slide title about digital transformation',
    elementId: 'textbox-a1b2c3d4e5f6',  // Optional, auto-injects content
    style: 'professional',               // Optional
    maxLength: 100                        // Optional
  }
}, '*');
```

**Response:**
```javascript
{
  success: true,
  action: 'generateTextBoxContent',
  content: '<p>Generated content here...</p>',
  elementId: 'textbox-a1b2c3d4e5f6',
  injected: true
}
```

---

## Persistence & Restoration

### How Text Boxes Are Saved

Text boxes are automatically saved as part of the slide data:

```javascript
// Saved data structure (in slide.text_boxes array)
{
  id: 'textbox-a1b2c3d4e5f6',
  position: {
    grid_row: '5/10',
    grid_column: '3/15'
  },
  content: '<p>Hello World</p>',
  z_index: 1001,
  style: {
    background_color: 'transparent',
    border_width: 0,
    padding: 16,
    opacity: 1
  },
  locked: false,
  visible: true
}
```

### How Text Boxes Are Restored

When a presentation is loaded, text boxes are **automatically restored** with full interactivity:

1. After slides are rendered, `restoreTextBoxes()` is called
2. For each saved text box, `ElementManager.insertTextBox()` is called with:
   - The original `id` (preserved)
   - All position, content, and style properties
   - `locked` and `visible` states
3. Event handlers are re-attached (drag, resize, edit)
4. Auto-save is skipped during restoration to avoid unnecessary saves

**Result:** Text boxes work exactly the same after reload - draggable, resizable, and editable.

---

## Backend REST API

Text boxes are also accessible via REST API for server-side operations.

### Base URL
```
/api/presentations/{presentation_id}/slides/{slide_index}/textboxes
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/textboxes` | Create a new text box |
| GET | `/textboxes` | List all text boxes on slide |
| PUT | `/textboxes/{textbox_id}` | Update a text box |
| DELETE | `/textboxes/{textbox_id}` | Delete a text box |
| POST | `/api/textbox/generate` | Generate AI content |

### Create Text Box (POST)

```bash
curl -X POST "http://localhost:8504/api/presentations/{id}/slides/0/textboxes" \
  -H "Content-Type: application/json" \
  -d '{
    "position": {
      "grid_row": "5/10",
      "grid_column": "3/15"
    },
    "content": "<p>Hello World</p>",
    "style": {
      "background_color": "transparent",
      "border_width": 0,
      "padding": 16
    }
  }'
```

### Update Text Box (PUT)

```bash
curl -X PUT "http://localhost:8504/api/presentations/{id}/slides/0/textboxes/{textbox_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<p>Updated content</p>",
    "style": {
      "background_color": "#f3f4f6"
    }
  }'
```

---

## Examples

### Complete Flow: Add and Style a Text Box

```javascript
const iframe = document.getElementById('presentation-iframe');

// 1. Insert text box
iframe.contentWindow.postMessage({
  action: 'insertTextBox',
  params: {
    gridRow: '4/12',
    gridColumn: '2/16',
    content: '<p>Key Insights</p>'
  }
}, '*');

// Listen for response to get elementId
window.addEventListener('message', function handler(event) {
  if (event.data.action === 'insertTextBox' && event.data.success) {
    const elementId = event.data.elementId;

    // 2. Apply styling
    iframe.contentWindow.postMessage({
      action: 'setTextBoxFont',
      params: { elementId, fontFamily: 'Georgia, serif' }
    }, '*');

    iframe.contentWindow.postMessage({
      action: 'setTextBoxFontSize',
      params: { elementId, fontSize: 32 }
    }, '*');

    iframe.contentWindow.postMessage({
      action: 'setTextBoxAlignment',
      params: { elementId, alignment: 'center' }
    }, '*');

    iframe.contentWindow.postMessage({
      action: 'setTextBoxBackground',
      params: { elementId, backgroundColor: '#f0f9ff' }
    }, '*');

    iframe.contentWindow.postMessage({
      action: 'setTextBoxBorder',
      params: {
        elementId,
        borderWidth: 2,
        borderColor: '#3b82f6',
        borderRadius: 12
      }
    }, '*');

    window.removeEventListener('message', handler);
  }
});
```

### Building a Formatting Toolbar

```javascript
class TextBoxToolbar {
  constructor(iframeId) {
    this.iframe = document.getElementById(iframeId);
    this.selectedTextBox = null;
  }

  send(action, params) {
    this.iframe.contentWindow.postMessage({ action, params }, '*');
  }

  // Selection
  select(elementId) {
    this.selectedTextBox = elementId;
    this.send('selectTextBox', { elementId });
  }

  // Text formatting
  bold() {
    this.send('applyTextFormatCommand', {
      elementId: this.selectedTextBox,
      command: 'bold'
    });
  }

  italic() {
    this.send('applyTextFormatCommand', {
      elementId: this.selectedTextBox,
      command: 'italic'
    });
  }

  setFont(fontFamily) {
    this.send('setTextBoxFont', {
      elementId: this.selectedTextBox,
      fontFamily
    });
  }

  setFontSize(fontSize) {
    this.send('setTextBoxFontSize', {
      elementId: this.selectedTextBox,
      fontSize
    });
  }

  setColor(color) {
    this.send('setTextBoxColor', {
      elementId: this.selectedTextBox,
      color
    });
  }

  setAlignment(alignment) {
    this.send('setTextBoxAlignment', {
      elementId: this.selectedTextBox,
      alignment
    });
  }

  // Box styling
  setBackground(backgroundColor) {
    this.send('setTextBoxBackground', {
      elementId: this.selectedTextBox,
      backgroundColor
    });
  }

  setBorder(borderWidth, borderColor, borderRadius = 0) {
    this.send('setTextBoxBorder', {
      elementId: this.selectedTextBox,
      borderWidth,
      borderColor,
      borderRadius
    });
  }

  // AI generation
  generateContent(prompt) {
    this.send('generateTextBoxContent', {
      elementId: this.selectedTextBox,
      prompt
    });
  }

  // Delete
  delete() {
    this.send('deleteTextBox', { elementId: this.selectedTextBox });
    this.selectedTextBox = null;
  }
}

// Usage
const toolbar = new TextBoxToolbar('presentation-iframe');
toolbar.select('textbox-abc123');
toolbar.bold();
toolbar.setFont('Georgia');
toolbar.setBackground('#f0f0f0');
```

---

## CSS Classes

| Class | Description |
|-------|-------------|
| `.inserted-textbox` | Base text box container |
| `.element-selected` | Selected state (blue solid border) |
| `.textbox-editing` | Editing state (green border) |
| `.textbox-locked` | Locked state (no interaction) |
| `.textbox-hidden` | Hidden state (display: none) |
| `.dragging` | During drag operation |
| `.resizing` | During resize operation |
| `.textbox-content` | Inner editable content area |
| `.textbox-drag-handle` | Top drag handle pill |
| `.resize-handle` | Base resize handle class |
| `.resize-handle-w` | Left resize handle |
| `.resize-handle-e` | Right resize handle |
| `.resize-handle-s` | Bottom resize handle |
| `.resize-handle-se` | Bottom-right corner resize handle |

---

## File Locations

| File | Path | Description |
|------|------|-------------|
| Backend Models | `models.py` | TextBox, TextBoxPosition, TextBoxStyle Pydantic models |
| Backend API | `server.py` | REST endpoints for text box CRUD |
| Element Manager | `src/utils/element-manager.js` | insertTextBox, updateTextBoxContent, etc. |
| Drag & Drop | `src/utils/drag-drop.js` | makeDraggable, makeResizable with 4-point handles |
| Auto-Save | `src/utils/auto-save.js` | collectTextBoxes for persistence |
| CSS Styles | `src/styles/textbox.css` | Selection, editing, resize handle styles |
| PostMessage Bridge | `viewer/presentation-viewer.html` | All postMessage handlers + restoreTextBoxes() |

---

## Notes

1. **Edit Mode Required**: Most operations only work when `body[data-mode="edit"]` is set
2. **Auto-Save**: Changes trigger auto-save after 2.5 seconds of inactivity
3. **Auto-Restore**: Text boxes are automatically restored with full interactivity on page load
4. **Z-Index**: Text boxes start at z-index 1000, selected = 1500, dragging = 11000
5. **Grid System**: 32 columns × 18 rows, base 1920×1080
6. **AI Integration**: Currently mock; will integrate with Text Service at port 8000
7. **Handle Design**: 4 resize handles (not 8) - left, right, bottom, bottom-right corner
8. **Handle Position**: Resize handles are positioned ON the border (half inside, half outside)

---

## Changelog

### Version 1.2 (2025-12-01)
- Added 8 new formatting commands as requested by frontend team:
  - `setTextBoxFontWeight` - Set font weight (400, 500, 600, 700, normal, bold)
  - `setTextBoxVerticalAlignment` - Align content top/middle/bottom
  - `setTextBoxParagraphSpacing` - Set paragraph margins via CSS custom properties
  - `setTextBoxColumns` - Multi-column text layout (1-4 columns)
  - `setTextBoxIndents` - First line, left, and right indentation
  - `setTextBoxAutosize` - Auto-height based on content
  - `setTextBoxBorderPositions` - Control individual border sides (top/right/bottom/left)
  - `setTextBoxBorderOffset` - Space between content and border
- Added CSS custom properties for paragraph spacing (`--para-margin-top`, `--para-margin-bottom`)

### Version 1.1 (2025-12-01)
- Changed resize handles from 8-point to 4-point (w, e, s, se)
- New handle design: dark blue squares on border
- Drag handle: light blue pill at top inside the box
- Added text box restoration on page load
- Added `id` parameter to insertTextBox for restoration
- Added `locked` and `visible` parameters
- Added Persistence & Restoration section
- Added CSS Classes section
- Updated visual design documentation
