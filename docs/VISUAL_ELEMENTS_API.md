# Visual Elements API Reference

## Overview

The Layout Service v7.5 supports four visual element types that can be inserted as placeholders and later populated with AI-generated or user-provided content:

| Element Type | Description | Use Case |
|-------------|-------------|----------|
| **Image** | Photo/illustration placeholder | Hero images, product photos, team photos |
| **Chart** | Data visualization placeholder | Bar charts, line charts, pie charts |
| **Infographic** | Information graphic placeholder | Statistics, timelines, process flows |
| **Diagram** | Technical diagram placeholder | Flowcharts, org charts, architecture diagrams |

All elements follow the same interaction pattern as TextBoxes:
- Can be inserted via postMessage API
- Support drag-and-drop repositioning
- Support resize handles (w, e, s, se)
- Can be selected/deselected
- Emit selection events to parent frame
- Auto-save to backend on changes

---

## Quick Start

### 1. Insert a Placeholder Element

```javascript
// From parent frame (frontend)
const iframe = document.getElementById('presentation-iframe');

// Insert an image placeholder
iframe.contentWindow.postMessage({
  action: 'insertImage',
  params: {
    slideIndex: 0,  // 0-based slide index
    gridRow: '3/10',
    gridColumn: '2/16'
  }
}, '*');
```

### 2. Listen for Response

```javascript
window.addEventListener('message', (event) => {
  if (event.data.action === 'insertImage') {
    if (event.data.success) {
      console.log('Image inserted:', event.data.elementId);
      // Store elementId for later content injection
    } else {
      console.error('Failed:', event.data.error);
    }
  }
});
```

### 3. Inject AI-Generated Content

```javascript
// After AI generates an image URL
iframe.contentWindow.postMessage({
  action: 'updateImageSource',
  params: {
    elementId: 'image-abc123-xyz789',
    imageUrl: 'https://example.com/generated-image.jpg',
    alt: 'AI-generated landscape'
  }
}, '*');
```

---

## PostMessage API Reference

### Element Insertion Commands

#### `insertImage`

Insert an image placeholder element.

**Request:**
```javascript
{
  action: 'insertImage',
  params: {
    slideIndex: number,      // Required: 0-based slide index
    gridRow?: string,        // Optional: CSS grid row (default: '4/14')
    gridColumn?: string,     // Optional: CSS grid column (default: '8/24')
    imageUrl?: string,       // Optional: Pre-populate with image URL
    alt?: string,            // Optional: Alt text for accessibility
    objectFit?: string,      // Optional: 'cover' | 'contain' | 'fill' (default: 'cover')
    zIndex?: number,         // Optional: Stack order (default: auto-assigned)
    id?: string              // Optional: Custom element ID (default: auto-generated)
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'insertImage',
  elementId: 'image-1701234567890-abc123',
  position: {
    gridRow: '4/14',
    gridColumn: '8/24'
  }
}
```

---

#### `insertChart`

Insert a chart placeholder element.

**Request:**
```javascript
{
  action: 'insertChart',
  params: {
    slideIndex: number,      // Required: 0-based slide index
    gridRow?: string,        // Optional: CSS grid row (default: '4/15')
    gridColumn?: string,     // Optional: CSS grid column (default: '3/30')
    chartType?: string,      // Optional: 'bar' | 'line' | 'pie' | 'doughnut' | etc.
    chartConfig?: object,    // Optional: Chart.js configuration object
    chartHtml?: string,      // Optional: Pre-rendered chart HTML
    zIndex?: number,
    id?: string
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'insertChart',
  elementId: 'chart-1701234567890-def456',
  position: {
    gridRow: '4/15',
    gridColumn: '3/30'
  }
}
```

---

#### `insertInfographic`

Insert an infographic placeholder element.

**Request:**
```javascript
{
  action: 'insertInfographic',
  params: {
    slideIndex: number,      // Required: 0-based slide index
    gridRow?: string,        // Optional: CSS grid row (default: '4/16')
    gridColumn?: string,     // Optional: CSS grid column (default: '5/28')
    infographicType?: string,// Optional: Type identifier
    svgContent?: string,     // Optional: Pre-rendered SVG content
    items?: array,           // Optional: Data items for rendering
    zIndex?: number,
    id?: string
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'insertInfographic',
  elementId: 'infographic-1701234567890-ghi789',
  position: {
    gridRow: '4/16',
    gridColumn: '5/28'
  }
}
```

---

#### `insertDiagram`

Insert a diagram placeholder element.

**Request:**
```javascript
{
  action: 'insertDiagram',
  params: {
    slideIndex: number,      // Required: 0-based slide index
    gridRow?: string,        // Optional: CSS grid row (default: '4/16')
    gridColumn?: string,     // Optional: CSS grid column (default: '5/28')
    diagramType?: string,    // Optional: 'flowchart' | 'sequence' | 'class' | 'er' | etc.
    mermaidCode?: string,    // Optional: Mermaid.js diagram code
    svgContent?: string,     // Optional: Pre-rendered SVG content
    direction?: string,      // Optional: 'TB' | 'BT' | 'LR' | 'RL' (default: 'TB')
    theme?: string,          // Optional: Mermaid theme (default: 'default')
    zIndex?: number,
    id?: string
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'insertDiagram',
  elementId: 'diagram-1701234567890-jkl012',
  position: {
    gridRow: '4/16',
    gridColumn: '5/28'
  }
}
```

---

### Content Update Commands

#### `updateImageSource`

Update an image element with actual image content.

**Request:**
```javascript
{
  action: 'updateImageSource',
  params: {
    elementId: string,       // Required: Element ID from insertion
    imageUrl: string,        // Required: Image URL to display
    alt?: string             // Optional: Alt text
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'updateImageSource'
}
```

**Behavior:**
- Removes placeholder UI (icon, text, dots)
- Removes `placeholder-mode` class
- Inserts `<img>` element with `object-fit` styling
- Element remains selectable, draggable, resizable

---

#### `updateChartConfig`

Update a chart element with Chart.js configuration.

**Request:**
```javascript
{
  action: 'updateChartConfig',
  params: {
    elementId: string,       // Required: Element ID
    chartConfig: {           // Required: Chart.js config object
      type: 'bar',
      data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
          label: 'Revenue',
          data: [12, 19, 3, 5],
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
```

---

#### `setChartHtml`

Update a chart element with pre-rendered HTML (for server-rendered charts).

**Request:**
```javascript
{
  action: 'setChartHtml',
  params: {
    elementId: string,       // Required: Element ID
    chartHtml: string        // Required: Complete HTML string
  }
}
```

---

#### `updateInfographicContent`

Update an infographic element with SVG content.

**Request:**
```javascript
{
  action: 'updateInfographicContent',
  params: {
    elementId: string,       // Required: Element ID
    svgContent: string       // Required: SVG markup string
  }
}
```

**Example SVG Content:**
```javascript
{
  action: 'updateInfographicContent',
  params: {
    elementId: 'infographic-abc123',
    svgContent: `
      <svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="20" y="20" width="360" height="60" fill="#3b82f6" rx="8"/>
        <text x="200" y="55" text-anchor="middle" fill="white" font-size="18">85% Complete</text>
        <rect x="20" y="100" width="306" height="40" fill="#3b82f6" rx="4"/>
        <rect x="20" y="100" width="360" height="40" fill="none" stroke="#e5e7eb" rx="4"/>
      </svg>
    `
  }
}
```

---

#### `updateDiagramSvg`

Update a diagram element with pre-rendered SVG.

**Request:**
```javascript
{
  action: 'updateDiagramSvg',
  params: {
    elementId: string,       // Required: Element ID
    svgContent: string       // Required: SVG markup string
  }
}
```

---

#### `updateDiagramMermaid`

Update a diagram element with Mermaid code (requires Mermaid.js to be loaded).

**Request:**
```javascript
{
  action: 'updateDiagramMermaid',
  params: {
    elementId: string,       // Required: Element ID
    mermaidCode: string      // Required: Mermaid diagram code
  }
}
```

**Example Mermaid Code:**
```javascript
{
  action: 'updateDiagramMermaid',
  params: {
    elementId: 'diagram-abc123',
    mermaidCode: `
      graph TD
        A[Start] --> B{Decision}
        B -->|Yes| C[Process 1]
        B -->|No| D[Process 2]
        C --> E[End]
        D --> E
    `
  }
}
```

---

### Element Management Commands

#### `deleteElement`

Delete any element (works for all element types).

**Request:**
```javascript
{
  action: 'deleteElement',
  params: {
    elementId: string        // Required: Element ID to delete
  }
}
```

**Response:**
```javascript
{
  success: true,
  action: 'deleteElement',
  elementId: 'image-abc123'
}
```

---

### Selection Events

When a user clicks on an element, the Layout Service emits a selection event to the parent frame:

```javascript
// Listen for element selection
window.addEventListener('message', (event) => {
  if (event.data.type === 'elementSelected') {
    console.log('Element selected:', {
      elementId: event.data.elementId,
      elementType: event.data.elementType,  // 'image' | 'chart' | 'infographic' | 'diagram'
      properties: event.data.properties
    });

    // Show appropriate properties panel in frontend
    showPropertiesPanel(event.data.elementType, event.data.properties);
  }
});
```

**Selection Event Payload:**
```javascript
{
  type: 'elementSelected',
  elementId: 'image-abc123-xyz789',
  elementType: 'image',  // 'image' | 'chart' | 'infographic' | 'diagram'
  properties: {
    position: {
      gridRow: '3/10',
      gridColumn: '2/16'
    },
    size: {
      width: 840,
      height: 420
    },
    zIndex: 101,
    locked: false,
    // Type-specific properties
    imageUrl: 'https://example.com/image.jpg',  // For image
    alt: 'Description'                           // For image
  }
}
```

---

## Grid System Reference

The slide uses a **32-column × 18-row** CSS grid on a **1920×1080px** canvas.

### Grid Positioning

```
gridRow: 'start/end'      // Row range (1-19)
gridColumn: 'start/end'   // Column range (1-33)
```

### Common Positions

| Position | gridRow | gridColumn | Size |
|----------|---------|------------|------|
| Full slide | '1/19' | '1/33' | 1920×1080 |
| Left half | '2/18' | '2/17' | 900×960 |
| Right half | '2/18' | '17/32' | 900×960 |
| Top-left quadrant | '2/10' | '2/17' | 900×480 |
| Center large | '3/16' | '4/30' | 1560×780 |
| Header area | '1/4' | '1/33' | 1920×180 |
| Content area | '4/17' | '2/32' | 1800×780 |

### Calculating Pixel Sizes

```javascript
const SLIDE_WIDTH = 1920;
const SLIDE_HEIGHT = 1080;
const COLUMNS = 32;
const ROWS = 18;

const columnWidth = SLIDE_WIDTH / COLUMNS;  // 60px per column
const rowHeight = SLIDE_HEIGHT / ROWS;      // 60px per row

// Example: gridColumn '5/25' = (25-5) * 60 = 1200px width
// Example: gridRow '3/15' = (15-3) * 60 = 720px height
```

---

## Data Models (Backend)

### ImageElement

```python
class ImageElement(BaseModel):
    id: str
    position: TextBoxPosition  # { grid_row: str, grid_column: str }
    z_index: int = 100
    image_url: Optional[str] = None
    alt_text: Optional[str] = None
    object_fit: str = "cover"  # 'cover' | 'contain' | 'fill'
    locked: bool = False
    visible: bool = True
```

### ChartElement

```python
class ChartElement(BaseModel):
    id: str
    position: TextBoxPosition
    z_index: int = 100
    chart_type: Optional[str] = None  # 'bar' | 'line' | 'pie' | etc.
    chart_config: Optional[Dict[str, Any]] = None  # Chart.js config
    chart_html: Optional[str] = None  # Pre-rendered HTML
    locked: bool = False
    visible: bool = True
```

### InfographicElement

```python
class InfographicElement(BaseModel):
    id: str
    position: TextBoxPosition
    z_index: int = 100
    infographic_type: Optional[str] = None
    svg_content: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    locked: bool = False
    visible: bool = True
```

### DiagramElement

```python
class DiagramElement(BaseModel):
    id: str
    position: TextBoxPosition
    z_index: int = 100
    diagram_type: Optional[str] = None  # 'flowchart' | 'sequence' | etc.
    mermaid_code: Optional[str] = None
    svg_content: Optional[str] = None
    direction: str = "TB"  # 'TB' | 'BT' | 'LR' | 'RL'
    theme: str = "default"
    locked: bool = False
    visible: bool = True
```

---

## Auto-Save Behavior

Elements are automatically saved to the backend when:
- An element is inserted
- An element is moved (drag-and-drop)
- An element is resized
- An element is deleted
- Content is updated

The auto-save has a **2.5 second debounce** to batch rapid changes.

### Saved Data Structure

```json
{
  "slides": [
    {
      "layout": "L25",
      "content": { ... },
      "text_boxes": [ ... ],
      "images": [
        {
          "id": "image-abc123",
          "position": { "grid_row": "3/10", "grid_column": "2/16" },
          "z_index": 101,
          "image_url": "https://example.com/image.jpg",
          "alt_text": "Mountain landscape",
          "object_fit": "cover",
          "locked": false,
          "visible": true
        }
      ],
      "charts": [ ... ],
      "infographics": [ ... ],
      "diagrams": [ ... ]
    }
  ]
}
```

---

## Element Restoration

When a presentation is loaded, saved elements are automatically restored:

1. TextBoxes are restored first
2. Images, Charts, Infographics, Diagrams are restored in order
3. Each element is re-created with proper event handlers
4. Elements with content (imageUrl, svgContent, etc.) display their content
5. Elements without content display placeholder UI

---

## CSS Classes Reference

### Base Classes

| Class | Description |
|-------|-------------|
| `.inserted-element-placeholder` | Base class for all placeholder elements |
| `.inserted-image` | Image-specific styling |
| `.inserted-chart` | Chart-specific styling |
| `.inserted-infographic` | Infographic-specific styling |
| `.inserted-diagram` | Diagram-specific styling |

### State Classes

| Class | Description |
|-------|-------------|
| `.placeholder-mode` | Element is showing placeholder UI |
| `.element-selected` | Element is currently selected |
| `.dragging` | Element is being dragged |
| `.resizing` | Element is being resized |
| `.element-locked` | Element is locked (no interaction) |
| `.element-hidden` | Element is hidden |

### Component Classes

| Class | Description |
|-------|-------------|
| `.element-drag-handle` | Drag handle (9-dot grid at top) |
| `.element-delete-button` | Delete button (× at top-right) |
| `.element-placeholder-content` | Container for placeholder icon/text |
| `.element-placeholder-icon` | SVG icon container |
| `.element-placeholder-text` | "Drag images here" text |
| `.element-type-badge` | Type indicator badge (bottom-right) |
| `.resize-handle` | Resize handles |
| `.element-content` | Actual content container |

---

## Integration Examples

### Example 1: Insert Image from AI Service

```javascript
class AIImageService {
  constructor(iframeRef) {
    this.iframe = iframeRef;
    this.pendingElements = new Map();

    // Listen for responses
    window.addEventListener('message', this.handleMessage.bind(this));
  }

  async insertAIImage(slideIndex, prompt, position) {
    // 1. Insert placeholder
    const insertPromise = new Promise((resolve) => {
      this.pendingElements.set('insertImage', resolve);
    });

    this.iframe.contentWindow.postMessage({
      action: 'insertImage',
      params: { slideIndex, ...position }
    }, '*');

    const insertResult = await insertPromise;
    const elementId = insertResult.elementId;

    // 2. Generate image with AI
    const imageUrl = await this.generateImage(prompt);

    // 3. Update element with generated image
    this.iframe.contentWindow.postMessage({
      action: 'updateImageSource',
      params: {
        elementId,
        imageUrl,
        alt: prompt
      }
    }, '*');

    return elementId;
  }

  handleMessage(event) {
    const { action, success, elementId } = event.data;
    if (this.pendingElements.has(action)) {
      this.pendingElements.get(action)(event.data);
      this.pendingElements.delete(action);
    }
  }

  async generateImage(prompt) {
    // Call your AI image generation API
    const response = await fetch('/api/ai/generate-image', {
      method: 'POST',
      body: JSON.stringify({ prompt })
    });
    const data = await response.json();
    return data.imageUrl;
  }
}

// Usage
const aiService = new AIImageService(document.getElementById('presentation-iframe'));
await aiService.insertAIImage(0, 'A serene mountain landscape at sunset', {
  gridRow: '3/12',
  gridColumn: '2/16'
});
```

### Example 2: Insert Chart from Data

```javascript
async function insertDataChart(iframe, slideIndex, chartData) {
  // 1. Insert placeholder
  iframe.contentWindow.postMessage({
    action: 'insertChart',
    params: {
      slideIndex,
      gridRow: '4/16',
      gridColumn: '3/30'
    }
  }, '*');

  // 2. Wait for insertion response
  const elementId = await waitForResponse('insertChart');

  // 3. Configure chart
  const chartConfig = {
    type: 'bar',
    data: {
      labels: chartData.labels,
      datasets: [{
        label: chartData.title,
        data: chartData.values,
        backgroundColor: '#3b82f6'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true },
        title: { display: true, text: chartData.title }
      }
    }
  };

  // 4. Update chart
  iframe.contentWindow.postMessage({
    action: 'updateChartConfig',
    params: { elementId, chartConfig }
  }, '*');
}
```

### Example 3: Properties Panel Integration

```javascript
// Frontend properties panel component
class ElementPropertiesPanel {
  constructor() {
    window.addEventListener('message', this.handleSelection.bind(this));
  }

  handleSelection(event) {
    if (event.data.type === 'elementSelected') {
      this.showPanel(event.data);
    }
  }

  showPanel({ elementId, elementType, properties }) {
    switch (elementType) {
      case 'image':
        this.showImageProperties(elementId, properties);
        break;
      case 'chart':
        this.showChartProperties(elementId, properties);
        break;
      case 'infographic':
        this.showInfographicProperties(elementId, properties);
        break;
      case 'diagram':
        this.showDiagramProperties(elementId, properties);
        break;
    }
  }

  showImageProperties(elementId, props) {
    // Render image-specific controls:
    // - Image URL input
    // - Alt text input
    // - Object fit selector (cover/contain/fill)
    // - Replace image button
    // - AI regenerate button
  }

  showChartProperties(elementId, props) {
    // Render chart-specific controls:
    // - Chart type selector
    // - Data editor
    // - Color picker
    // - AI regenerate button
  }

  // ... similar for infographic and diagram
}
```

---

## Troubleshooting

### Element Not Appearing

1. **Check grid position**: Ensure `gridRow` and `gridColumn` are within slide bounds (1-19, 1-33)
2. **Check z-index**: Element might be behind other elements
3. **Check visibility**: Element might have `element-hidden` class
4. **Check slide index**: Ensure `slideIndex` matches the currently visible slide

### Content Not Loading

1. **Check element ID**: Ensure you're using the correct `elementId` from insertion response
2. **Check content format**: SVG must be valid, image URL must be accessible
3. **Check CORS**: Image URLs must be CORS-enabled or same-origin

### Selection Not Working

1. **Check edit mode**: Selection only works in edit mode (`body[data-mode="edit"]`)
2. **Check locked state**: Locked elements cannot be selected
3. **Check z-index**: Click might be hitting a higher element

### Auto-Save Not Triggering

1. **Check network**: Look for PUT requests to `/api/presentations/{id}/slides`
2. **Check debounce**: Changes batch for 2.5 seconds before saving
3. **Check errors**: Look for console errors in Layout Service iframe

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-02 | Initial release with Image, Chart, Infographic, Diagram support |

---

## Support

For questions or issues:
- Check console logs in the Layout Service iframe
- Verify postMessage origin is allowed
- Check network tab for API errors
- Review element registry: `window.ElementManager.getAllElements()`
