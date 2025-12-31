# Element CRUD API Documentation

Complete reference for element-level Create, Read, Update, Delete operations in the Layout Builder v7.5-main service.

## Base URL

```
/api/presentations/{presentation_id}/slides/{slide_index}
```

## Element Types Summary

| Type | Endpoint Path | Max Per Slide | ID Format |
|------|---------------|---------------|-----------|
| Text Boxes | `/textboxes` | 20 | `textbox_{uuid8}` |
| Images | `/images` | 20 | `image_{uuid8}` |
| Charts | `/charts` | 10 | `chart_{uuid8}` |
| Diagrams | `/diagrams` | 10 | `diagram_{uuid8}` |
| Infographics | `/infographics` | 10 | `infographic_{uuid8}` |
| Contents | `/contents` | 5 | `content_{uuid8}` |

## Common Query Parameters

All create, update, and delete operations support version tracking:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `created_by` | string | `"user"` | Who made the change |
| `change_summary` | string | auto-generated | Description of the change |

---

## Images API

### Create Image

**POST** `/api/presentations/{presentation_id}/slides/{slide_index}/images`

Creates a new image element on a slide.

**Request Body:**
```json
{
  "position": {
    "grid_row": "5/10",
    "grid_column": "3/15"
  },
  "image_url": "https://example.com/image.jpg",
  "alt_text": "Description of the image",
  "object_fit": "cover",
  "z_index": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `position` | object | Yes | Grid position (`grid_row`, `grid_column`) |
| `image_url` | string | No | Image URL (null for placeholder) |
| `alt_text` | string | No | Alt text for accessibility (max 500 chars) |
| `object_fit` | string | No | CSS object-fit: `cover`, `contain`, `fill`, `none`, `scale-down` (default: `cover`) |
| `z_index` | int | No | Z-index (auto-assigned if not provided) |

**Response:**
```json
{
  "success": true,
  "image": {
    "id": "image_a1b2c3d4",
    "parent_slide_id": "slide_abc123def456",
    "position": {"grid_row": "5/10", "grid_column": "3/15"},
    "image_url": "https://example.com/image.jpg",
    "alt_text": "Description of the image",
    "object_fit": "cover",
    "z_index": 100,
    "locked": false,
    "visible": true
  },
  "message": "Image created on slide 1"
}
```

### List Images

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/images`

**Response:**
```json
{
  "success": true,
  "slide_index": 0,
  "images": [...],
  "count": 3
}
```

### Get Single Image

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}`

**Response:**
```json
{
  "success": true,
  "image": {...},
  "message": "Image found"
}
```

### Update Image

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}`

Only provided fields are updated.

**Request Body:**
```json
{
  "image_url": "https://example.com/new-image.jpg",
  "alt_text": "Updated description",
  "locked": true
}
```

**Response:**
```json
{
  "success": true,
  "image": {...},
  "message": "Image updated"
}
```

### Delete Image

**DELETE** `/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}`

**Response:**
```json
{
  "success": true,
  "message": "Image deleted",
  "image_id": "image_a1b2c3d4"
}
```

---

## Charts API

### Create Chart

**POST** `/api/presentations/{presentation_id}/slides/{slide_index}/charts`

**Request Body:**
```json
{
  "position": {
    "grid_row": "4/14",
    "grid_column": "2/16"
  },
  "chart_type": "bar",
  "chart_config": {
    "type": "bar",
    "data": {...},
    "options": {...}
  },
  "chart_html": "<div class='chart'>...</div>",
  "z_index": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `position` | object | Yes | Grid position |
| `chart_type` | string | No | Chart type: `bar`, `line`, `pie`, `doughnut`, etc. |
| `chart_config` | object | No | Chart.js configuration object |
| `chart_html` | string | No | Pre-rendered HTML from Analytics Service |
| `z_index` | int | No | Z-index |

### List Charts

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/charts`

### Get Single Chart

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}`

### Update Chart

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}`

**Request Body (all fields optional):**
```json
{
  "chart_type": "line",
  "chart_config": {...},
  "locked": true
}
```

### Delete Chart

**DELETE** `/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}`

---

## Diagrams API

### Create Diagram

**POST** `/api/presentations/{presentation_id}/slides/{slide_index}/diagrams`

**Request Body:**
```json
{
  "position": {
    "grid_row": "4/14",
    "grid_column": "2/16"
  },
  "diagram_type": "flowchart",
  "mermaid_code": "graph TD\n  A-->B",
  "svg_content": "<svg>...</svg>",
  "html_content": "<div class='diagram'>...</div>",
  "direction": "TB",
  "theme": "default",
  "z_index": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `position` | object | Yes | Grid position |
| `diagram_type` | string | No | Type: `flowchart`, `sequence`, `class`, `state`, etc. |
| `mermaid_code` | string | No | Mermaid.js diagram code |
| `svg_content` | string | No | Pre-rendered SVG |
| `html_content` | string | No | Pre-rendered HTML |
| `direction` | string | No | Layout direction: `TB`, `LR`, `BT`, `RL` (default: `TB`) |
| `theme` | string | No | Theme: `default`, `dark`, `forest`, `neutral` (default: `default`) |
| `z_index` | int | No | Z-index |

### List Diagrams

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/diagrams`

### Get Single Diagram

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}`

### Update Diagram

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}`

**Request Body (all fields optional):**
```json
{
  "mermaid_code": "graph LR\n  A-->B-->C",
  "direction": "LR",
  "locked": true
}
```

### Delete Diagram

**DELETE** `/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}`

---

## Infographics API

### Create Infographic

**POST** `/api/presentations/{presentation_id}/slides/{slide_index}/infographics`

**Request Body:**
```json
{
  "position": {
    "grid_row": "4/14",
    "grid_column": "2/16"
  },
  "infographic_type": "timeline",
  "svg_content": "<svg>...</svg>",
  "html_content": "<div class='infographic'>...</div>",
  "items": [
    {"title": "Step 1", "description": "..."},
    {"title": "Step 2", "description": "..."}
  ],
  "z_index": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `position` | object | Yes | Grid position |
| `infographic_type` | string | No | Type: `timeline`, `process`, `comparison`, etc. |
| `svg_content` | string | No | SVG from Illustrator Service |
| `html_content` | string | No | Pre-rendered HTML |
| `items` | array | No | Data items for infographic generation |
| `z_index` | int | No | Z-index |

### List Infographics

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/infographics`

### Get Single Infographic

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}`

### Update Infographic

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}`

### Delete Infographic

**DELETE** `/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}`

---

## Contents API

Content elements are structured content regions managed by external services (Text Service, Analytics, etc.).

### Create Content Element

**POST** `/api/presentations/{presentation_id}/slides/{slide_index}/contents`

**Request Body:**
```json
{
  "slot_name": "content",
  "position": {
    "grid_row": "4/16",
    "grid_column": "2/31"
  },
  "content_html": "<div>Rich HTML content</div>",
  "content_type": "html",
  "format_owner": "text_service",
  "z_index": 100
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slot_name` | string | Yes | Slot name from template registry (e.g., `content`, `hero`) |
| `position` | object | Yes | Grid position |
| `content_html` | string | No | HTML content (default: empty) |
| `content_type` | string | No | Type: `html`, `chart`, `diagram`, `infographic` (default: `html`) |
| `format_owner` | string | No | Service owning formatting (default: `text_service`) |
| `z_index` | int | No | Z-index |

### List Content Elements

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/contents`

### Get Single Content Element

**GET** `/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}`

### Update Content Element

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}`

**Request Body (all fields optional):**
```json
{
  "content_html": "<div>Updated content</div>",
  "locked": true
}
```

### Delete Content Element

**DELETE** `/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}`

---

## Error Responses

### 400 Bad Request

Returned for validation errors:
- Invalid slide index
- Exceeded element limit
- Invalid position format

```json
{
  "detail": "Maximum 20 images per slide"
}
```

### 404 Not Found

Returned when resource doesn't exist:
- Presentation not found
- Slide index out of range
- Element not found

```json
{
  "detail": "Image not found: image_abc12345"
}
```

### 500 Internal Server Error

Returned for unexpected server errors:

```json
{
  "detail": "Error creating image: <error message>"
}
```

---

## Version Tracking

All modifications automatically create version entries for undo/restore capabilities.

### Access Version History

**GET** `/api/presentations/{presentation_id}/versions`

### Restore to Previous Version

**POST** `/api/presentations/{presentation_id}/restore/{version_id}`

---

## Position Format

Grid positions use CSS Grid format with 32 columns × 18 rows:

```json
{
  "grid_row": "start/end",
  "grid_column": "start/end"
}
```

**Examples:**
- Full width content: `{"grid_row": "4/16", "grid_column": "2/31"}`
- Top-right corner (2×2): `{"grid_row": "1/3", "grid_column": "31/33"}`
- Left half: `{"grid_row": "4/16", "grid_column": "2/16"}`

**Pixel Conversion:**
- Column width: 60px
- Row height: 60px
- X position: `(col_start - 1) × 60`
- Y position: `(row_start - 1) × 60`
- Width: `(col_end - col_start) × 60`
- Height: `(row_end - row_start) × 60`

---

## Example Workflows

### Add an Image to a Slide

```bash
# Create image
curl -X POST "http://localhost:8504/api/presentations/{pres_id}/slides/0/images" \
  -H "Content-Type: application/json" \
  -d '{
    "position": {"grid_row": "5/15", "grid_column": "3/15"},
    "image_url": "https://example.com/photo.jpg",
    "alt_text": "Team photo"
  }'
```

### Update a Chart's Configuration

```bash
# Update chart
curl -X PUT "http://localhost:8504/api/presentations/{pres_id}/slides/0/charts/{chart_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "chart_type": "line",
    "chart_config": {"type": "line", "data": {...}}
  }'
```

### Delete an Element

```bash
# Delete diagram
curl -X DELETE "http://localhost:8504/api/presentations/{pres_id}/slides/0/diagrams/{diagram_id}"
```

### List All Images on a Slide

```bash
curl "http://localhost:8504/api/presentations/{pres_id}/slides/0/images"
```

---

## Related Endpoints

### Slide-Level Content Update

For updating multiple slide properties at once:

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}`

### Element CSS Classes

For updating CSS classes on any element:

**PUT** `/api/presentations/{presentation_id}/slides/{slide_index}/elements/{element_id}/classes`
