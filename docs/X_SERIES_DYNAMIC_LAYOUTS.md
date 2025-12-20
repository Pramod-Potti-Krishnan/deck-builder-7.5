# X-Series Dynamic Layouts

**Service**: Layout Service v7.5-main
**Version**: 7.5.7
**Last Updated**: December 2024

---

## Overview

X-series layouts are **dynamically generated layouts** that intelligently split the content area of base templates into multiple sub-zones. Unlike static templates where content areas are fixed, X-series layouts adapt to content requirements by dividing the main content area based on content type analysis.

### Key Concept

```
Standard Layout (C1-text):
┌──────────────────────────────────────┐
│ Title                                │
│ Subtitle                             │
├──────────────────────────────────────┤
│                                      │
│         Single Content Area          │
│            (1800×840px)              │
│                                      │
├──────────────────────────────────────┤
│ Footer                         Logo  │
└──────────────────────────────────────┘

X-Series Layout (X1-a3f7e8c2):
┌──────────────────────────────────────┐
│ Title                                │
│ Subtitle                             │
├──────────────────────────────────────┤
│ Zone 1: Main Goal (heading)          │
├──────────────────────────────────────┤
│ Zone 2: Key Point 1 (bullets)        │
├──────────────────────────────────────┤
│ Zone 3: Key Point 2 (bullets)        │
├──────────────────────────────────────┤
│ Footer                         Logo  │
└──────────────────────────────────────┘
```

**What stays the same**: Title, subtitle, footer, logo, image (for I-series)
**What changes**: Content area is split into multiple sub-zones

---

## X-Series Mapping

| X-Series | Base Template | Content Area Dimensions | Use Case |
|----------|---------------|------------------------|----------|
| **X1** | C1-text | 1800×840px (30 cols × 14 rows) | Full-width content slides |
| **X2** | I1-image-left | 1200×840px (20 cols × 14 rows) | Image left, multi-zone right |
| **X3** | I2-image-right | 1140×840px (19 cols × 14 rows) | Image right, multi-zone left |
| **X4** | I3-image-left-narrow | 1500×840px (25 cols × 14 rows) | Narrow image left, wide content |
| **X5** | I4-image-right-narrow | 1440×840px (24 cols × 14 rows) | Narrow image right, wide content |

### Layout ID Format

```
X{series}-{hash8}
│    │       │
│    │       └── 8-character hash (deterministic from zone config)
│    └────────── Series number (1-5)
└──────────────── X prefix indicating dynamic layout
```

Examples: `X1-a3f7e8c2`, `X2-56097840`, `X1-b06f5f23`

---

## API Reference

### Base URL
```
/api/dynamic-layouts
```

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Generate a new dynamic layout |
| `/{layout_id}` | GET | Get layout details |
| `/` | GET | List all dynamic layouts |
| `/{layout_id}` | DELETE | Delete a dynamic layout |
| `/patterns` | GET | List preconfigured split patterns |
| `/base-layouts` | GET | List available base layouts |

---

## Creating Dynamic Layouts

### POST `/api/dynamic-layouts/generate`

Generate a new X-series layout by specifying how to split the content area.

#### Request Body

```json
{
  "base_layout": "C1-text",           // Required: Base template (C1-text, I1-I4)
  "content_type": "agenda",           // Required: Content type identifier
  "zone_count": 3,                    // Optional: Number of zones (2-8, default: 3)
  "split_direction": "horizontal",    // Optional: horizontal, vertical, or grid
  "split_pattern": "agenda-3-item",   // Optional: Use preconfigured pattern
  "zone_labels": ["Goal", "P1", "P2"],// Optional: Custom labels for zones
  "custom_ratios": [0.35, 0.35, 0.30] // Optional: Custom split ratios (must sum to 1.0)
}
```

#### Response

```json
{
  "layout_id": "X1-84d76fe0",
  "base_layout": "C1-text",
  "name": "X1 Agenda (3 zones)",
  "description": "Dynamic agenda layout based on C1-text",
  "content_type": "agenda",
  "zones": [
    {
      "zone_id": "zone_1",
      "label": "Main Goal",
      "grid_row": "4/8",
      "grid_column": "2/32",
      "pixels": { "x": 60, "y": 180, "width": 1800, "height": 294 },
      "content_type_hint": "heading",
      "z_index": 100
    },
    {
      "zone_id": "zone_2",
      "label": "Key Point 1",
      "grid_row": "8/12",
      "grid_column": "2/32",
      "pixels": { "x": 60, "y": 474, "width": 1800, "height": 294 },
      "content_type_hint": "bullets",
      "z_index": 101
    },
    {
      "zone_id": "zone_3",
      "label": "Key Point 2",
      "grid_row": "12/16",
      "grid_column": "2/32",
      "pixels": { "x": 60, "y": 768, "width": 1800, "height": 252 },
      "content_type_hint": "bullets",
      "z_index": 102
    }
  ],
  "split_pattern": "agenda-3-item",
  "split_direction": "horizontal",
  "content_area": { "x": 60, "y": 180, "width": 1800, "height": 840 },
  "reusable": true,
  "created_at": "2025-12-18T06:12:18.051052"
}
```

---

## Preconfigured Split Patterns

The system includes **10 preconfigured patterns** optimized for common content types.

### GET `/api/dynamic-layouts/patterns`

### Horizontal Splits (Rows)

| Pattern | Zones | Ratios | Best For |
|---------|-------|--------|----------|
| `agenda-3-item` | 3 | 35%, 35%, 30% | Agenda slides with 3 items |
| `agenda-5-item` | 5 | 25%, 20%, 20%, 18%, 17% | Detailed agenda with 5 items |
| `use-case-3row` | 3 | 25%, 50%, 25% | Problem-Solution-Benefits |
| `timeline-4row` | 4 | 25% each | Process/timeline with 4 phases |

### Vertical Splits (Columns)

| Pattern | Zones | Ratios | Best For |
|---------|-------|--------|----------|
| `comparison-2col` | 2 | 50%, 50% | Side-by-side comparison |
| `feature-3col` | 3 | 33%, 34%, 33% | Feature showcase |

### Grid Splits

| Pattern | Zones | Grid | Best For |
|---------|-------|------|----------|
| `grid-2x2` | 4 | 2 rows × 2 cols | Quadrant layouts |
| `grid-2x3` | 6 | 2 rows × 3 cols | 6-item showcase |

### I-Series Specific

| Pattern | Zones | Ratios | Best For |
|---------|-------|--------|----------|
| `image-split-2row` | 2 | 50%, 50% | Image + 2 text blocks |
| `image-split-3row` | 3 | 33% each | Image + 3 text blocks |

---

## Usage Examples

### Example 1: Agenda Slide with Pattern

```bash
curl -X POST "http://localhost:8504/api/dynamic-layouts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "base_layout": "C1-text",
    "content_type": "agenda",
    "split_pattern": "agenda-3-item"
  }'
```

### Example 2: Custom 4-Zone Layout

```bash
curl -X POST "http://localhost:8504/api/dynamic-layouts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "base_layout": "C1-text",
    "content_type": "custom",
    "zone_count": 4,
    "split_direction": "horizontal",
    "custom_ratios": [0.20, 0.30, 0.30, 0.20],
    "zone_labels": ["Header", "Main Content", "Supporting", "Footer"]
  }'
```

### Example 3: Image + Multi-Zone (X2)

```bash
curl -X POST "http://localhost:8504/api/dynamic-layouts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "base_layout": "I1-image-left",
    "content_type": "feature",
    "split_pattern": "image-split-3row",
    "zone_labels": ["Key Feature", "Benefits", "Call to Action"]
  }'
```

### Example 4: Comparison Layout (Vertical Split)

```bash
curl -X POST "http://localhost:8504/api/dynamic-layouts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "base_layout": "C1-text",
    "content_type": "comparison",
    "split_pattern": "comparison-2col",
    "zone_labels": ["Before", "After"]
  }'
```

### Example 5: Grid Layout (2×3)

```bash
curl -X POST "http://localhost:8504/api/dynamic-layouts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "base_layout": "C1-text",
    "content_type": "features",
    "split_pattern": "grid-2x3",
    "zone_labels": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5", "Feature 6"]
  }'
```

---

## Using X-Series Layouts in Slides

Once created, X-series layout IDs can be used like any other layout:

### In Slide Creation

```json
{
  "layout": "X1-84d76fe0",
  "content": {
    "slide_title": "Project Roadmap",
    "subtitle": "Q1 2025 Objectives",
    "zones": {
      "zone_1": "<h3>Main Goal</h3><p>Increase market share by 15%</p>",
      "zone_2": "<ul><li>Launch new product line</li><li>Expand to 3 new markets</li></ul>",
      "zone_3": "<ul><li>Hire 20 new team members</li><li>Establish partnerships</li></ul>"
    }
  }
}
```

### Content Mapping Options

Zone content can be provided in multiple formats:

```json
// Option 1: By zone_id
"zones": {
  "zone_1": "<content>",
  "zone_2": "<content>"
}

// Option 2: By index
"zones": {
  "0": "<content>",
  "1": "<content>"
}

// Option 3: By zone_X key
"zone_1": "<content>",
"zone_2": "<content>"
```

---

## Frontend Integration

### JavaScript API

```javascript
// Check if layout is X-series
if (isXSeriesLayout('X1-84d76fe0')) {
  // Fetch layout details
  const layout = await DynamicTemplates.fetchDynamicLayout('X1-84d76fe0');

  // Register in template registry (optional)
  DynamicTemplates.registerDynamicLayout('X1-84d76fe0', layout);

  // Create elements for slide
  createElementsForDynamicTemplate(slideElement, slideIndex, layoutId, content, layout);
}
```

### Available Functions

| Function | Description |
|----------|-------------|
| `isXSeriesLayout(id)` | Check if ID matches X-series pattern |
| `getXSeriesNumber(id)` | Get series number (1-5) from ID |
| `getXSeriesBaseLayout(id)` | Get base template (C1-text, etc.) |
| `DynamicTemplates.fetchDynamicLayout(id)` | Fetch layout from API |
| `DynamicTemplates.registerDynamicLayout(id, data)` | Register in TEMPLATE_REGISTRY |
| `createElementsForDynamicTemplate(...)` | Create DOM elements for zones |

---

## Zone Definition Structure

Each zone in a dynamic layout contains:

```typescript
interface ZoneDefinition {
  zone_id: string;           // Unique identifier (zone_1, zone_2, etc.)
  label: string;             // Human-readable label
  grid_row: string;          // CSS Grid row (e.g., "4/8")
  grid_column: string;       // CSS Grid column (e.g., "2/32")
  pixels: {
    x: number;               // Pixel X position
    y: number;               // Pixel Y position
    width: number;           // Zone width in pixels
    height: number;          // Zone height in pixels
  };
  content_type_hint: string; // Suggested content type (heading, bullets, etc.)
  z_index: number;           // Stacking order
}
```

---

## Database Schema

Dynamic layouts are stored in `ls_dynamic_layouts`:

```sql
CREATE TABLE ls_dynamic_layouts (
    layout_id VARCHAR(20) PRIMARY KEY,      -- X1-a3f7e8c2
    base_layout VARCHAR(30) NOT NULL,       -- C1-text, I1-image-left, etc.
    name VARCHAR(100) NOT NULL,
    description TEXT,
    content_type VARCHAR(50) NOT NULL,
    split_pattern VARCHAR(50) NOT NULL,
    split_direction VARCHAR(20) NOT NULL,
    zone_count INTEGER NOT NULL,
    zones JSONB NOT NULL,
    content_area JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT TRUE
);
```

---

## Best Practices

### 1. Choose the Right Base Layout

- **X1 (C1-text)**: Full-width content, no images
- **X2-X5 (I-series)**: When you need an image alongside zoned content

### 2. Use Preconfigured Patterns When Possible

Patterns are optimized for readability and visual balance:
- `agenda-*` for agenda/overview slides
- `comparison-*` for side-by-side comparisons
- `use-case-*` for problem-solution structures
- `grid-*` for multi-item showcases

### 3. Keep Zone Count Reasonable

- **2-4 zones**: Ideal for most content types
- **5-6 zones**: Use for detailed agendas or feature lists
- **7-8 zones**: Reserved for data-heavy slides (use sparingly)

### 4. Provide Meaningful Labels

Zone labels help content generators and users understand purpose:
```json
"zone_labels": ["Problem Statement", "Our Solution", "Key Benefits"]
```

### 5. Reuse Layouts When Possible

Dynamic layouts are designed to be reusable. Query existing layouts before creating new ones:
```bash
curl "http://localhost:8504/api/dynamic-layouts?content_type=agenda"
```

---

## Validation Rules

| Field | Constraint |
|-------|------------|
| `base_layout` | Must be C1-text, I1-I4 |
| `zone_count` | 2-8 zones |
| `split_direction` | horizontal, vertical, or grid |
| `custom_ratios` | Must sum to 1.0 (±0.01 tolerance) |
| `layout_id` | Pattern: `X[1-5]-[a-f0-9]{8}` |

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid base_layout` | Unsupported template | Use C1-text or I1-I4 |
| `Zone count out of range` | <2 or >8 zones | Adjust zone_count |
| `Ratios don't sum to 1.0` | Invalid custom_ratios | Ensure sum ≈ 1.0 |
| `Layout not found` | Invalid layout_id | Verify ID format |
| `Unknown split pattern` | Invalid pattern name | Check `/patterns` endpoint |

---

## Files Reference

| File | Description |
|------|-------------|
| `server.py` | API endpoints implementation |
| `models.py` | Pydantic models for request/response |
| `src/layout_registry.py` | SPLIT_PATTERNS, CONTENT_AREAS, helper functions |
| `src/renderers/dynamic-templates.js` | Frontend rendering for X-series |
| `src/utils/direct-element-creator.js` | Zone element creation |
| `src/templates/template-registry.js` | X-series utilities and validation |
| `migrations/004_add_dynamic_layouts.sql` | Database schema |

---

## Changelog

### v7.5.7 (December 2024)
- Initial X-series implementation
- 10 preconfigured split patterns
- Support for C1-text and I1-I4 base layouts
- Frontend rendering with zone elements
- Database persistence with Supabase
- Full CRUD API endpoints
