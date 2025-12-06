# Element Properties API Documentation

> Frontend integration guide for v7.5-main element property management

## Overview

This document describes the REST APIs and postMessage commands available for managing element properties in presentations. The system supports:

- **CSS Classes** - Programmatic styling via custom class names
- **Vertical Alignment** - Top/middle/bottom alignment for text containers
- **Padding Shorthand** - CSS shorthand padding values (e.g., "25px 0px")
- **Border Shorthand** - CSS shorthand border values (e.g., "1px solid #ddd")
- **Text Transform** - Case transformation (uppercase, lowercase, capitalize)

---

## REST API Endpoints

### Base URL
```
http://localhost:8504
```

All endpoints support CORS and accept/return JSON.

---

### 1. Update Element CSS Classes

Update the CSS classes on any element (textbox, image, chart, etc.).

**Endpoint:** `PUT /api/presentations/{presentation_id}/slides/{slide_index}/elements/{element_id}/classes`

**Request Body:**
```json
{
  "css_classes": ["slot-content", "slot-type-bod", "custom-style"],
  "replace": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `css_classes` | `string[]` | Yes | List of CSS class names to apply |
| `replace` | `boolean` | No | If `true` (default), replaces all custom classes. If `false`, adds to existing. |

**Response:**
```json
{
  "success": true,
  "element_id": "textbox-abc123",
  "css_classes": ["slot-content", "slot-type-bod", "custom-style"]
}
```

**Example (JavaScript):**
```javascript
async function updateElementClasses(presentationId, slideIndex, elementId, classes) {
  const response = await fetch(
    `http://localhost:8504/api/presentations/${presentationId}/slides/${slideIndex}/elements/${elementId}/classes`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        css_classes: classes,
        replace: true
      })
    }
  );
  return response.json();
}

// Usage
await updateElementClasses('pres-123', 0, 'textbox-456', ['highlight', 'centered']);
```

---

### 2. Update TextBox Content and Style

Update a textbox's content, style, and classes in one request.

**Endpoint:** `PUT /api/presentations/{presentation_id}/slides/{slide_index}/textboxes/{textbox_id}`

**Request Body:**
```json
{
  "content": "<p>Updated content</p>",
  "style": {
    "background_color": "#ffffff",
    "border": "1px solid #ddd",
    "border_radius": 8,
    "padding": "25px 0px",
    "vertical_align": "middle"
  },
  "text_style": {
    "font_family": "Inter",
    "font_size": 24,
    "font_weight": "bold",
    "text_align": "center",
    "text_transform": "uppercase",
    "color": "#333333"
  },
  "css_classes": ["slot-content", "featured"]
}
```

**Style Properties:**

| Property | Type | Example | Description |
|----------|------|---------|-------------|
| `background_color` | `string` | `"#ffffff"` | Background color (hex or rgba) |
| `border` | `string` | `"1px solid #ddd"` | Border shorthand |
| `border_radius` | `int` | `8` | Border radius in pixels |
| `padding` | `int\|string` | `16` or `"25px 0px"` | Padding (integer or shorthand) |
| `vertical_align` | `string` | `"middle"` | Vertical alignment: `top`, `middle`, `bottom` |

**Text Style Properties:**

| Property | Type | Example | Description |
|----------|------|---------|-------------|
| `font_family` | `string` | `"Inter"` | Font family name |
| `font_size` | `int` | `24` | Font size in pixels |
| `font_weight` | `string` | `"bold"` | Font weight: `normal`, `bold`, `100`-`900` |
| `text_align` | `string` | `"center"` | Horizontal alignment: `left`, `center`, `right` |
| `text_transform` | `string` | `"uppercase"` | Case: `uppercase`, `lowercase`, `capitalize`, `none` |
| `color` | `string` | `"#333333"` | Text color |

**Example:**
```javascript
async function updateTextBox(presentationId, slideIndex, textboxId, updates) {
  const response = await fetch(
    `http://localhost:8504/api/presentations/${presentationId}/slides/${slideIndex}/textboxes/${textboxId}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    }
  );
  return response.json();
}

// Usage - update with new properties
await updateTextBox('pres-123', 0, 'textbox-456', {
  style: {
    border: '2px solid #007bff',
    padding: '20px 40px',
    vertical_align: 'middle'
  },
  text_style: {
    text_transform: 'uppercase',
    font_weight: 'bold'
  },
  css_classes: ['highlight-box', 'animate-in']
});
```

---

### 3. Insert New TextBox

Create a new textbox with all property options.

**Endpoint:** `POST /api/presentations/{presentation_id}/slides/{slide_index}/textboxes`

**Request Body:**
```json
{
  "content": "<h2>New Section</h2>",
  "grid_position": {
    "column_start": 2,
    "column_end": 32,
    "row_start": 4,
    "row_end": 18
  },
  "style": {
    "background_color": "rgba(0,0,0,0.05)",
    "border": "1px solid #e0e0e0",
    "border_radius": 8,
    "padding": "25px",
    "vertical_align": "top"
  },
  "text_style": {
    "font_family": "Inter",
    "font_size": 18,
    "font_weight": "normal",
    "text_align": "left",
    "text_transform": "none",
    "color": "#333333"
  },
  "css_classes": ["slot-content", "slot-type-bod"]
}
```

---

### 4. Get Element Properties Schema

Retrieve the complete schema of available element properties.

**Endpoint:** `GET /api/element-properties/schema`

**Response:**
```json
{
  "version": "7.5.1",
  "style_properties": {
    "background_color": { "type": "string", "description": "...", "examples": [...] },
    "border": { "type": "string", "description": "...", "examples": [...] },
    "padding": { "type": "int|string", "description": "...", "examples": [...] },
    "vertical_align": { "type": "string", "enum": ["top", "middle", "bottom"], ... },
    ...
  },
  "text_style_properties": { ... },
  "supported_css_class_patterns": [ ... ]
}
```

---

## postMessage API (iframe communication)

When the presentation viewer is embedded in an iframe, use postMessage to communicate with the presentation.

### Send Commands to Presentation

```javascript
// Get reference to the iframe
const iframe = document.getElementById('presentation-iframe');

// Send command
iframe.contentWindow.postMessage({
  type: 'command',
  action: 'updateElementClasses',
  payload: {
    elementId: 'textbox-123',
    classes: ['highlight', 'featured'],
    replace: true
  }
}, '*');
```

### Available postMessage Commands

#### Update Element Classes
```javascript
{
  type: 'command',
  action: 'updateElementClasses',
  payload: {
    elementId: 'textbox-123',
    classes: ['class1', 'class2'],
    replace: true  // optional, defaults to true
  }
}
```

#### Update TextBox Style
```javascript
{
  type: 'command',
  action: 'updateTextBoxStyle',
  payload: {
    elementId: 'textbox-123',
    style: {
      backgroundColor: '#ffffff',
      border: '1px solid #ddd',
      padding: '25px 0px',
      verticalAlign: 'middle'
    },
    textStyle: {
      fontSize: 24,
      fontWeight: 'bold',
      textAlign: 'center',
      textTransform: 'uppercase'
    }
  }
}
```

#### Insert TextBox
```javascript
{
  type: 'command',
  action: 'insertTextBox',
  payload: {
    slideIndex: 0,
    config: {
      content: '<p>New content</p>',
      gridPosition: { colStart: 2, colEnd: 32, rowStart: 4, rowEnd: 18 },
      style: { padding: '25px', verticalAlign: 'middle' },
      textStyle: { fontSize: 18 },
      cssClasses: ['custom-style']
    }
  }
}
```

### Listen for Responses

```javascript
window.addEventListener('message', (event) => {
  if (event.data.type === 'response') {
    console.log('Command result:', event.data.result);
  }

  if (event.data.type === 'elementUpdated') {
    console.log('Element was updated:', event.data.elementId);
  }
});
```

---

## Property Value Reference

### Vertical Alignment

| Value | CSS Equivalent | Description |
|-------|---------------|-------------|
| `top` | `flex-start` | Align content to top |
| `middle` | `center` | Center content vertically |
| `bottom` | `flex-end` | Align content to bottom |

### Padding Shorthand

| Format | Example | Description |
|--------|---------|-------------|
| Integer | `16` | All sides (16px) |
| Single value | `"25px"` | All sides |
| Two values | `"25px 0px"` | Top/bottom, left/right |
| Four values | `"10px 20px 10px 20px"` | Top, right, bottom, left |

### Border Shorthand

| Format | Example | Description |
|--------|---------|-------------|
| Full shorthand | `"1px solid #ddd"` | Width, style, color |
| Style options | `solid`, `dashed`, `dotted`, `double`, `none` | Border style |

### Text Transform

| Value | Example Input | Result |
|-------|---------------|--------|
| `uppercase` | "Hello World" | "HELLO WORLD" |
| `lowercase` | "Hello World" | "hello world" |
| `capitalize` | "hello world" | "Hello World" |
| `none` | "Hello World" | "Hello World" |

---

## Frontend Integration Examples

### Example 1: Properties Panel Integration

```javascript
class PropertiesPanel {
  constructor(presentationId) {
    this.presentationId = presentationId;
    this.selectedElement = null;
  }

  async onElementSelected(elementId, slideIndex) {
    this.selectedElement = { id: elementId, slideIndex };
    // Fetch current element state from API if needed
  }

  async updateVerticalAlign(value) {
    if (!this.selectedElement) return;

    await fetch(
      `/api/presentations/${this.presentationId}/slides/${this.selectedElement.slideIndex}/textboxes/${this.selectedElement.id}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          style: { vertical_align: value }
        })
      }
    );
  }

  async updatePadding(value) {
    if (!this.selectedElement) return;

    await fetch(
      `/api/presentations/${this.presentationId}/slides/${this.selectedElement.slideIndex}/textboxes/${this.selectedElement.id}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          style: { padding: value }  // e.g., "25px 0px"
        })
      }
    );
  }

  async updateCssClasses(classes) {
    if (!this.selectedElement) return;

    await fetch(
      `/api/presentations/${this.presentationId}/slides/${this.selectedElement.slideIndex}/elements/${this.selectedElement.id}/classes`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          css_classes: classes,
          replace: true
        })
      }
    );
  }
}
```

### Example 2: Batch Style Updates

```javascript
async function applyTemplate(presentationId, slideIndex, templateStyles) {
  const elements = templateStyles.elements;

  for (const element of elements) {
    await fetch(
      `/api/presentations/${presentationId}/slides/${slideIndex}/textboxes/${element.id}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          style: {
            border: element.border,
            padding: element.padding,
            vertical_align: element.verticalAlign,
            background_color: element.backgroundColor
          },
          text_style: {
            text_transform: element.textTransform,
            font_weight: element.fontWeight
          },
          css_classes: element.cssClasses
        })
      }
    );
  }
}

// Usage
await applyTemplate('pres-123', 0, {
  elements: [
    {
      id: 'textbox-title',
      padding: '0px',
      verticalAlign: 'bottom',
      textTransform: 'uppercase',
      fontWeight: 'bold',
      cssClasses: ['slide-title', 'hero-text']
    },
    {
      id: 'textbox-body',
      border: '1px solid #e0e0e0',
      padding: '25px',
      verticalAlign: 'top',
      cssClasses: ['slot-content', 'slot-type-bod']
    }
  ]
});
```

---

## Migration Guide

If you're upgrading from a previous version, note these changes:

### New Properties
- `style.border` - Use CSS shorthand instead of separate `border_width`/`border_color`
- `style.padding` - Now accepts shorthand strings like `"25px 0px"`
- `style.vertical_align` - New property for vertical text alignment
- `text_style.text_transform` - New property for case transformation
- `css_classes` - New property for custom CSS class management

### Backward Compatibility
- Integer padding values (e.g., `16`) still work as before
- Separate border properties still work but shorthand is preferred
- All existing API endpoints remain unchanged

---

## Error Handling

All endpoints return standard error responses:

```json
{
  "detail": "Element not found: textbox-invalid"
}
```

Common error codes:
- `404` - Presentation, slide, or element not found
- `400` - Invalid request body or property values
- `500` - Server error

**Example error handling:**
```javascript
async function safeUpdateElement(url, body) {
  try {
    const response = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('Update failed:', error.detail);
      return null;
    }

    return response.json();
  } catch (err) {
    console.error('Network error:', err);
    return null;
  }
}
```

---

## Related Documentation

- [Element Manager API](../src/utils/element-manager.js) - Client-side element management
- [Models Reference](../models.py) - Pydantic models for all data types
- [Server API](../server.py) - Full API implementation
