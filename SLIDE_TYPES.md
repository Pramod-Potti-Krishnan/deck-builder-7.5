# Slide Types API Documentation

## Overview

This document describes all available slide types for the Deckster presentation system and how to use the API to add slides to presentations.

**API Base URL**: `http://localhost:8504` (development) or your production URL

**CORS**: Enabled for all origins (`*`)

---

## Quick Start

### Add a New Slide

```javascript
// Add a slide to an existing presentation
fetch('http://localhost:8504/api/presentations/{presentation_id}/slides', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    layout: 'C1-text',  // Any valid layout ID
    position: 2,        // Optional: insert at position (0-based), defaults to end
    content: {          // Optional: custom content, defaults provided
      slide_title: 'My Custom Title',
      subtitle: 'Custom subtitle',
      body: '<p>Your content here</p>'
    }
  })
});
```

### Response

```json
{
  "success": true,
  "message": "Slide added at position 3",
  "slide_index": 2,
  "slide": { "layout": "C1-text", "content": {...} },
  "slide_count": 5
}
```

---

## Available Slide Types

### Hero Slides (Full-Bleed)

| ID | Name | Description | Use Case |
|----|------|-------------|----------|
| `H1-generated` | Title Slide (AI) | Full canvas for AI-generated content | Opening slides with AI design |
| `H1-structured` | Title Slide (Manual) | Editable title, subtitle, background | Manual title slides |
| `H2-section` | Section Divider | Chapter/section breaks | Separating presentation sections |
| `H3-closing` | Closing Slide | Thank you with contact info | Ending slides |

### Content Slides (Single Content Area)

| ID | Name | Description | Use Case |
|----|------|-------------|----------|
| `C1-text` | Text Content | Body text with title/subtitle | Paragraphs, bullet points |
| `C2-table` | Table Slide | Data table area | Tabular data |
| `C3-chart` | Single Chart | Chart visualization | Single chart with title |
| `C4-infographic` | Single Infographic | Infographic area | Visual data stories |
| `C5-diagram` | Single Diagram | Diagram area | Process flows, org charts |
| `C6-image` | Single Image | Image with caption | Image-focused slides |

### Split Layout Slides (Two Columns)

| ID | Name | Description | Use Case |
|----|------|-------------|----------|
| `S1-visual-text` | Visual + Text | Chart/diagram left, text right | Data with analysis |
| `S2-image-content` | Image + Content | Full-height image left, content right | Image-driven content |
| `S3-two-visuals` | Two Visuals | Side-by-side visuals | Comparisons |
| `S4-comparison` | Comparison | Two columns with headers | Before/after, pros/cons |

### Blank Slides

| ID | Name | Description | Use Case |
|----|------|-------------|----------|
| `B1-blank` | Blank Canvas | Empty slide for free placement | Custom layouts |

---

## API Endpoints

### 1. Add Slide

```
POST /api/presentations/{presentation_id}/slides
```

**Request Body:**

```json
{
  "layout": "C1-text",
  "position": null,
  "content": {},
  "background_color": null,
  "background_image": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `layout` | string | Yes | Layout ID (see table above) |
| `position` | integer | No | Insert position (0-based). Defaults to end. |
| `content` | object | No | Initial content. Uses defaults if not provided. |
| `background_color` | string | No | CSS color for hero slides |
| `background_image` | string | No | URL for background image |

### 2. Delete Slide

```
DELETE /api/presentations/{presentation_id}/slides/{slide_index}
```

**Note:** Cannot delete the last remaining slide.

### 3. Duplicate Slide

```
POST /api/presentations/{presentation_id}/slides/{slide_index}/duplicate
```

**Request Body:**

```json
{
  "insert_after": true
}
```

### 4. Reorder Slides

```
PUT /api/presentations/{presentation_id}/slides/reorder
```

**Request Body:**

```json
{
  "from_index": 0,
  "to_index": 3
}
```

### 5. Change Slide Layout

```
PUT /api/presentations/{presentation_id}/slides/{slide_index}/layout
```

**Request Body:**

```json
{
  "new_layout": "S1-visual-text",
  "preserve_content": true,
  "content_mapping": {}
}
```

---

## Default Content by Layout

### Hero Templates

#### H1-generated
```json
{
  "hero_content": "",
  "background_color": "#1f2937"
}
```

#### H1-structured
```json
{
  "slide_title": "Presentation Title",
  "subtitle": "Your tagline or subtitle here",
  "footer_text": "",
  "background_color": "#1e3a5f"
}
```

#### H2-section
```json
{
  "section_number": "SECTION 01",
  "slide_title": "Section Title",
  "subtitle": "",
  "background_color": "#374151"
}
```

#### H3-closing
```json
{
  "slide_title": "Thank You",
  "subtitle": "Questions & Discussion",
  "contact_info": "",
  "background_color": "#1e3a5f"
}
```

### Content Templates

#### C1-text
```json
{
  "slide_title": "Slide Title",
  "subtitle": "",
  "body": ""
}
```

#### C2-table
```json
{
  "slide_title": "Table Title",
  "subtitle": "",
  "table_html": ""
}
```

#### C3-chart
```json
{
  "slide_title": "Chart Title",
  "subtitle": "",
  "chart_html": ""
}
```

#### C4-infographic
```json
{
  "slide_title": "Infographic Title",
  "subtitle": "",
  "infographic_svg": ""
}
```

#### C5-diagram
```json
{
  "slide_title": "Diagram Title",
  "subtitle": "",
  "diagram_svg": ""
}
```

#### C6-image
```json
{
  "slide_title": "Image Title",
  "subtitle": "",
  "image_url": ""
}
```

### Split Templates

#### S1-visual-text
```json
{
  "slide_title": "Visual + Text",
  "subtitle": "",
  "element_3": "",
  "element_2": ""
}
```

#### S2-image-content
```json
{
  "slide_title": "Image + Content",
  "subtitle": "",
  "image_url": "",
  "main_content": ""
}
```

#### S3-two-visuals
```json
{
  "slide_title": "Comparison",
  "subtitle": "",
  "element_4": "",
  "element_2": "",
  "element_3": "",
  "element_5": ""
}
```

#### S4-comparison
```json
{
  "slide_title": "Comparison",
  "subtitle": "",
  "header_left": "Option A",
  "header_right": "Option B",
  "content_left": "",
  "content_right": ""
}
```

### Blank Template

#### B1-blank
```json
{
  "slide_title": "",
  "subtitle": "",
  "canvas_content": ""
}
```

---

## Slot Definitions (Grid Positions)

All slides use a 32-column x 18-row grid (1920x1080px).

### Common Slots

| Slot | Grid Position | Description |
|------|--------------|-------------|
| `title` | Row 2-3, Col 2-32 | Main slide title |
| `subtitle` | Row 3-4, Col 2-32 | Subtitle text |
| `footer` | Row 18-19, Col 2-7 | Footer text |
| `logo` | Row 17-19, Col 30-32 | Company logo |

### Content Slots

| Slot | Grid Position | Accepts |
|------|--------------|---------|
| `content` (C1-C6) | Row 5-17, Col 2-32 | body, table, chart, infographic, diagram, image |
| `content_left` (S1) | Row 5-17, Col 2-17 | chart, infographic, diagram, image |
| `content_right` (S1) | Row 5-17, Col 18-32 | body, table, html |

### Hero Slots

| Slot | Grid Position | Accepts |
|------|--------------|---------|
| `background` | Row 1-19, Col 1-33 | image, color, gradient |
| `hero_content` | Row 1-19, Col 1-33 | Full canvas content |

---

## JavaScript Integration Example

```javascript
class SlideManager {
  constructor(baseUrl = 'http://localhost:8504') {
    this.baseUrl = baseUrl;
  }

  async addSlide(presentationId, layout, options = {}) {
    const response = await fetch(
      `${this.baseUrl}/api/presentations/${presentationId}/slides`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          layout,
          position: options.position,
          content: options.content,
          background_color: options.backgroundColor,
          background_image: options.backgroundImage
        })
      }
    );
    return response.json();
  }

  async deleteSlide(presentationId, slideIndex) {
    const response = await fetch(
      `${this.baseUrl}/api/presentations/${presentationId}/slides/${slideIndex}`,
      { method: 'DELETE' }
    );
    return response.json();
  }

  async duplicateSlide(presentationId, slideIndex, insertAfter = true) {
    const response = await fetch(
      `${this.baseUrl}/api/presentations/${presentationId}/slides/${slideIndex}/duplicate`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ insert_after: insertAfter })
      }
    );
    return response.json();
  }

  async reorderSlides(presentationId, fromIndex, toIndex) {
    const response = await fetch(
      `${this.baseUrl}/api/presentations/${presentationId}/slides/reorder`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from_index: fromIndex, to_index: toIndex })
      }
    );
    return response.json();
  }

  async changeLayout(presentationId, slideIndex, newLayout, preserveContent = true) {
    const response = await fetch(
      `${this.baseUrl}/api/presentations/${presentationId}/slides/${slideIndex}/layout`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          new_layout: newLayout,
          preserve_content: preserveContent
        })
      }
    );
    return response.json();
  }
}

// Usage
const slides = new SlideManager();

// Add a text slide at position 2
await slides.addSlide('presentation-uuid', 'C1-text', {
  position: 2,
  content: {
    slide_title: 'Key Findings',
    subtitle: 'Q4 2024 Results',
    body: '<ul><li>Revenue up 25%</li><li>Customer growth 40%</li></ul>'
  }
});

// Add a section divider
await slides.addSlide('presentation-uuid', 'H2-section', {
  content: {
    section_number: 'SECTION 02',
    slide_title: 'Financial Analysis'
  }
});

// Add a chart slide
await slides.addSlide('presentation-uuid', 'C3-chart', {
  content: {
    slide_title: 'Revenue Trends',
    chart_html: '<div id="chart-container">...</div>'
  }
});
```

---

## Viewing Presentations

```
GET /p/{presentation_id}
```

Returns HTML page with the rendered presentation.

**Example:** `http://localhost:8504/p/abc123-def456`

---

## Error Handling

All endpoints return standard error responses:

```json
{
  "detail": "Error message describing the issue"
}
```

Common error codes:
- `400`: Invalid request (bad layout, invalid index)
- `404`: Presentation or slide not found
- `500`: Server error

---

## Version History

The API automatically creates version backups before modifications. Use these endpoints to manage versions:

```
GET  /api/presentations/{id}/versions         # List versions
POST /api/presentations/{id}/restore/{ver_id} # Restore version
```

---

## postMessage API (for iframe integration)

When the presentation viewer is embedded in an iframe, you can control slide operations via `postMessage`. This is the **recommended approach** for frontend integration.

### Security

The viewer accepts postMessage from these origins:
- `localhost:*` (development)
- `*.up.railway.app` (Railway deployments)
- `*.vercel.app` (Vercel deployments)
- `*.netlify.app` (Netlify deployments)
- `deckster.xyz` and `www.deckster.xyz` (production)

### Basic Usage

```javascript
// Get reference to the iframe
const iframe = document.querySelector('iframe');

// Send command to iframe
iframe.contentWindow.postMessage({
  action: 'addSlide',
  params: {
    layout: 'C1-text',
    position: 2,
    content: { slide_title: 'New Slide' }
  }
}, '*');

// Listen for response
window.addEventListener('message', (event) => {
  if (event.data.action === 'addSlide') {
    console.log('Result:', event.data.success, event.data.message);
  }
});
```

### Slide CRUD Actions

#### addSlide

Add a new slide to the presentation.

```javascript
iframe.contentWindow.postMessage({
  action: 'addSlide',
  params: {
    layout: 'H2-section',           // Required: Layout ID
    position: 2,                     // Optional: 0-based index, defaults to end
    content: {                       // Optional: slide content
      section_number: 'SECTION 02',
      slide_title: 'Market Analysis'
    },
    background_color: '#1e3a5f',    // Optional: for hero slides
    background_image: 'https://...' // Optional: background image URL
  }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "addSlide",
  "message": "Slide added at position 3",
  "slide_index": 2,
  "slide_count": 5
}
```

#### deleteSlide

Delete a slide by index.

```javascript
iframe.contentWindow.postMessage({
  action: 'deleteSlide',
  params: {
    index: 2  // Required: 0-based slide index
  }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "deleteSlide",
  "message": "Slide 2 deleted"
}
```

#### duplicateSlide

Duplicate an existing slide.

```javascript
iframe.contentWindow.postMessage({
  action: 'duplicateSlide',
  params: {
    index: 1,           // Required: slide index to duplicate
    insert_after: true  // Optional: insert after (true) or before (false)
  }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "duplicateSlide",
  "message": "Slide duplicated",
  "new_slide_index": 2
}
```

#### reorderSlides

Move a slide from one position to another.

```javascript
iframe.contentWindow.postMessage({
  action: 'reorderSlides',
  params: {
    from_index: 0,  // Required: current position
    to_index: 3     // Required: new position
  }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "reorderSlides",
  "message": "Slide moved from position 0 to 3"
}
```

#### changeSlideLayout

Change the layout of an existing slide.

```javascript
iframe.contentWindow.postMessage({
  action: 'changeSlideLayout',
  params: {
    index: 1,                   // Required: slide index
    new_layout: 'S1-visual-text', // Required: new layout ID
    preserve_content: true      // Optional: keep existing content
  }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "changeSlideLayout",
  "message": "Layout changed to S1-visual-text"
}
```

### Query Actions

#### getSlideCount

Get the total number of slides.

```javascript
iframe.contentWindow.postMessage({
  action: 'getSlideCount',
  params: {}
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "getSlideCount",
  "data": { "count": 5 }
}
```

#### getSlideInfo

Get information about a specific slide.

```javascript
iframe.contentWindow.postMessage({
  action: 'getSlideInfo',
  params: { index: 0 }
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "getSlideInfo",
  "data": {
    "index": 0,
    "layout": "H1-structured",
    "content": { "slide_title": "...", "subtitle": "..." }
  }
}
```

#### getSlideLayouts

Get all available layout types.

```javascript
iframe.contentWindow.postMessage({
  action: 'getSlideLayouts',
  params: {}
}, '*');
```

**Response:**
```json
{
  "success": true,
  "action": "getSlideLayouts",
  "data": {
    "layouts": ["L01", "L02", "L03", "L25", "L27", "L29"],
    "descriptions": {
      "L01": "Centered Chart with Text Below",
      "L02": "Left Diagram with Text on Right",
      ...
    }
  }
}
```

### Navigation Actions

```javascript
// Go to next slide
iframe.contentWindow.postMessage({ action: 'nextSlide' }, '*');

// Go to previous slide
iframe.contentWindow.postMessage({ action: 'prevSlide' }, '*');

// Go to specific slide (0-based index)
iframe.contentWindow.postMessage({
  action: 'goToSlide',
  params: { index: 2 }
}, '*');

// Get current slide info
iframe.contentWindow.postMessage({ action: 'getCurrentSlideInfo' }, '*');
```

### Edit Mode Actions

```javascript
// Toggle edit mode
iframe.contentWindow.postMessage({ action: 'toggleEditMode' }, '*');

// Save all changes
iframe.contentWindow.postMessage({ action: 'saveAllChanges' }, '*');

// Force save immediately
iframe.contentWindow.postMessage({ action: 'forceSave' }, '*');

// Cancel edits
iframe.contentWindow.postMessage({ action: 'cancelEdits' }, '*');
```

### Complete Frontend Integration Example

```javascript
class PresentationController {
  constructor(iframeSelector) {
    this.iframe = document.querySelector(iframeSelector);
    this.pendingCallbacks = new Map();
    this.messageId = 0;

    // Listen for responses
    window.addEventListener('message', this.handleResponse.bind(this));
  }

  handleResponse(event) {
    const { action, success, error, ...data } = event.data;
    if (action && this.pendingCallbacks.has(action)) {
      const callback = this.pendingCallbacks.get(action);
      this.pendingCallbacks.delete(action);
      if (success) {
        callback.resolve(data);
      } else {
        callback.reject(new Error(error || 'Unknown error'));
      }
    }
  }

  sendCommand(action, params = {}) {
    return new Promise((resolve, reject) => {
      this.pendingCallbacks.set(action, { resolve, reject });
      this.iframe.contentWindow.postMessage({ action, params }, '*');

      // Timeout after 10 seconds
      setTimeout(() => {
        if (this.pendingCallbacks.has(action)) {
          this.pendingCallbacks.delete(action);
          reject(new Error('Request timeout'));
        }
      }, 10000);
    });
  }

  // Slide CRUD methods
  async addSlide(layout, options = {}) {
    return this.sendCommand('addSlide', { layout, ...options });
  }

  async deleteSlide(index) {
    return this.sendCommand('deleteSlide', { index });
  }

  async duplicateSlide(index, insertAfter = true) {
    return this.sendCommand('duplicateSlide', { index, insert_after: insertAfter });
  }

  async reorderSlides(fromIndex, toIndex) {
    return this.sendCommand('reorderSlides', { from_index: fromIndex, to_index: toIndex });
  }

  async changeLayout(index, newLayout, preserveContent = true) {
    return this.sendCommand('changeSlideLayout', {
      index,
      new_layout: newLayout,
      preserve_content: preserveContent
    });
  }

  // Navigation
  async goToSlide(index) {
    return this.sendCommand('goToSlide', { index });
  }

  async nextSlide() {
    return this.sendCommand('nextSlide');
  }

  async prevSlide() {
    return this.sendCommand('prevSlide');
  }
}

// Usage
const controller = new PresentationController('#presentation-iframe');

// Add a section divider
await controller.addSlide('H2-section', {
  content: { section_number: 'SECTION 03', slide_title: 'Summary' }
});

// Duplicate slide 2
await controller.duplicateSlide(2);

// Change slide 1 to chart layout
await controller.changeLayout(1, 'C3-chart');

// Delete slide 4
await controller.deleteSlide(4);
```

---

## Related Resources

- **API Documentation**: `/docs` (Swagger UI)
- **API Tester**: `/tester`
- **Template Registry**: `src/templates/template-registry.js`
- **postMessage Events**: `POSTMESSAGE_SELECTION_EVENTS.md`
