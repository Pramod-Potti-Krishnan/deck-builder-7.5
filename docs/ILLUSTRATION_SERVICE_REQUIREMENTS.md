# Illustration Service Requirements for Layout Builder v7.5

This document specifies the API requirements for Illustration Service to integrate with Layout Builder's illustration/icon insertion features.

## Overview

Layout Builder needs Illustration Service to provide:
1. **Vector illustrations (SVG)** for insertion into slides
2. **Icons and symbols** matching presentation themes
3. **Diagrams and flowcharts** as vector graphics
4. **Decorative elements** (shapes, patterns, backgrounds)

---

## API 1: Generate Illustration

### Purpose
Generate an AI-powered vector illustration based on a concept.

### Endpoint Suggestion
```
POST /api/illustration/generate
```

### Request Format
```typescript
{
  presentationId: string,
  concept: string,             // What to illustrate (e.g., "teamwork", "cloud computing")
  type: IllustrationType,      // See types below
  style: {
    variant: 'flat' | 'outlined' | 'filled' | 'gradient' | 'isometric' | '3d',
    strokeWidth?: number,      // For outlined style (1-4)
    cornerRadius?: number      // Rounded corners
  },
  colors: {
    primary: string,           // Main color (hex)
    secondary?: string,        // Accent color (hex)
    background?: string,       // Background color (hex or 'transparent')
    palette?: string[]         // Additional colors
  },
  dimensions: {
    width: number,             // Target width in pixels
    height: number,            // Target height in pixels
    preserveAspectRatio: boolean
  },
  context?: {
    slideTitle?: string,
    presentationTopic?: string,
    industry?: string
  }
}
```

### Illustration Types
| Type | Description | Use Case |
|------|-------------|----------|
| `icon` | Simple symbolic icon | Feature highlights, bullet points |
| `scene` | Complex illustration | Hero images, concept visualization |
| `character` | People/avatar illustrations | Team slides, user personas |
| `object` | Product/object illustration | Product features, physical items |
| `abstract` | Abstract shapes/patterns | Backgrounds, decorations |
| `diagram` | Process/flow diagram | Workflows, architectures |
| `infographic` | Data-driven graphic | Statistics, comparisons |
| `logo-style` | Brand-like illustration | Branded concepts |

### Response Format
```typescript
{
  success: boolean,
  svg: string,                 // Complete SVG markup
  illustrationId: string,      // Unique ID
  dimensions: {
    width: number,
    height: number,
    viewBox: string            // SVG viewBox attribute
  },
  colors: {
    used: string[]             // Colors actually used in SVG
  },
  metadata: {
    type: string,
    style: string,
    generationTime: number     // Milliseconds
  },
  error?: string
}
```

---

## API 2: Get Icon Set

### Purpose
Retrieve themed icons from a predefined set.

### Endpoint Suggestion
```
GET /api/illustration/icons
```

### Request Parameters
```typescript
{
  category?: string,           // e.g., 'business', 'technology', 'arrows'
  search?: string,             // Search term
  style: 'flat' | 'outlined' | 'filled',
  color: string,               // Primary color to apply
  size: number,                // Target size in pixels (square)
  page?: number,
  limit?: number               // Max 100
}
```

### Response Format
```typescript
{
  success: boolean,
  icons: Array<{
    id: string,
    name: string,
    category: string,
    svg: string,               // SVG markup
    keywords: string[]
  }>,
  pagination: {
    page: number,
    totalPages: number,
    totalIcons: number
  }
}
```

### Icon Categories
- `business`: briefcase, chart, handshake, presentation, money
- `technology`: computer, cloud, code, database, security
- `arrows`: up, down, left, right, curved, circular
- `communication`: email, chat, phone, video, notification
- `people`: user, team, audience, speaker, customer
- `general`: check, cross, star, heart, flag, bookmark

---

## API 3: Generate Diagram

### Purpose
Generate vector diagrams (flowcharts, org charts, etc.)

### Endpoint Suggestion
```
POST /api/illustration/diagram
```

### Request Format
```typescript
{
  presentationId: string,
  diagramType: 'flowchart' | 'orgchart' | 'process' | 'cycle' | 'hierarchy' | 'venn' | 'timeline',
  data: DiagramData,           // Structure varies by type
  style: {
    nodeShape: 'rectangle' | 'rounded' | 'circle' | 'diamond',
    connectorStyle: 'straight' | 'curved' | 'angled',
    labelPosition: 'inside' | 'outside' | 'below'
  },
  colors: {
    primary: string,
    secondary: string,
    connector: string,
    text: string
  },
  dimensions: {
    width: number,
    height: number
  }
}
```

### Diagram Data Structures

#### Flowchart
```typescript
{
  nodes: Array<{
    id: string,
    label: string,
    type: 'start' | 'end' | 'process' | 'decision' | 'io'
  }>,
  edges: Array<{
    from: string,
    to: string,
    label?: string
  }>
}
```

#### Org Chart
```typescript
{
  nodes: Array<{
    id: string,
    name: string,
    title?: string,
    parentId?: string
  }>
}
```

#### Process/Cycle
```typescript
{
  steps: Array<{
    label: string,
    description?: string
  }>,
  circular: boolean            // Connect last to first
}
```

#### Timeline
```typescript
{
  events: Array<{
    date: string,
    label: string,
    description?: string
  }>,
  orientation: 'horizontal' | 'vertical'
}
```

### Response Format
```typescript
{
  success: boolean,
  svg: string,
  diagramId: string,
  dimensions: {
    width: number,
    height: number,
    viewBox: string
  },
  error?: string
}
```

---

## SVG Output Requirements

### Structure
```svg
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {width} {height}"
     width="{width}"
     height="{height}"
     id="illustration-{id}">

  <!-- Optional background -->
  <rect width="100%" height="100%" fill="{backgroundColor}" />

  <!-- Illustration content -->
  <g id="content">
    <!-- Paths, shapes, text -->
  </g>

</svg>
```

### Requirements
1. **Valid SVG 1.1** - Compatible with all modern browsers
2. **Inline styles** - No external stylesheets
3. **No external references** - No `xlink:href` to external files
4. **Optimized** - Minified, no unnecessary metadata
5. **Accessible** - Include `<title>` and `aria-label`
6. **ID-prefixed** - All internal IDs prefixed with illustration ID

### Color Application
- Use `currentColor` for elements that should inherit color
- Or apply provided hex colors directly to `fill` and `stroke`

### Size Optimization
- **Icons**: < 2KB
- **Simple illustrations**: < 10KB
- **Complex scenes**: < 50KB
- **Diagrams**: < 20KB

---

## Layout Builder Integration

### How Layout Builder Will Use These APIs

1. **insertIllustration** (or via insertShape with SVG):
   ```javascript
   {
     action: 'insertShape',
     params: {
       slideIndex: 0,
       shape: 'custom',        // Custom SVG shape
       position: { gridRow: '5/12', gridColumn: '3/15' },
       svgContent: '...',      // From Illustration Service
       draggable: true
     }
   }
   ```

2. **SVG rendering**:
   - Layout Builder injects SVG into positioned container
   - Scales using CSS (width/height 100%)
   - Maintains aspect ratio via viewBox

3. **HTML output**:
   ```html
   <div id="illust-abc123" class="dynamic-element inserted-illustration"
        style="grid-row: 5/12; grid-column: 3/15;">
     <svg viewBox="0 0 400 300" style="width: 100%; height: 100%;">
       <!-- SVG content -->
     </svg>
   </div>
   ```

---

## Theme Integration

### Color Mapping

Illustrations should use theme colors:

| Theme Variable | Illustration Use |
|---------------|------------------|
| `primaryColor` | Main shapes, fills |
| `secondaryColor` | Accents, highlights |
| `textColor` | Labels, text elements |
| `backgroundColor` | SVG background (if not transparent) |

### Style Matching

| Presentation Style | Illustration Style |
|-------------------|-------------------|
| Corporate/Professional | flat, outlined, minimal |
| Creative/Startup | gradient, filled, colorful |
| Technical | outlined, isometric |
| Modern/Minimal | flat, monochrome |

---

## Common Use Cases in Slides

### Icon Placement
- Bullet point icons: 60×60px
- Feature icons: 120×120px
- Section icons: 200×200px

### Illustration Placement
| Use Case | Grid Position | Recommended Size |
|----------|---------------|------------------|
| Hero illustration | cols 2-16, rows 4-16 | 800×700 |
| Side illustration | cols 2-12, rows 4-17 | 600×800 |
| Accent decoration | cols 26-31, rows 2-6 | 300×240 |
| Inline diagram | cols 3-30, rows 6-14 | 1600×480 |

---

## Performance Considerations

### Response Time Expectations
| Operation | Expected | Max |
|-----------|----------|-----|
| Icon fetch | < 200ms | 500ms |
| Simple illustration | < 2s | 5s |
| Complex scene | < 5s | 15s |
| Diagram generation | < 3s | 10s |

### Caching
- Icons should be heavily cached (immutable)
- Generated illustrations cached by parameters
- SVG served with compression (gzip/brotli)

---

## Error Handling

### Error Codes
| Code | Meaning |
|------|---------|
| `INVALID_TYPE` | Unknown illustration type |
| `INVALID_COLORS` | Invalid color format |
| `GENERATION_FAILED` | AI generation failed |
| `DIAGRAM_INVALID` | Invalid diagram data structure |
| `TOO_COMPLEX` | Diagram too complex to render |

### Fallback Behavior
Return a placeholder SVG:
```svg
<svg viewBox="0 0 200 200">
  <rect width="200" height="200" fill="#f3f4f6" rx="8"/>
  <text x="100" y="105" text-anchor="middle" fill="#9ca3af" font-size="14">
    Illustration unavailable
  </text>
</svg>
```

---

## Security Considerations

1. **SVG Sanitization**: Remove any `<script>`, `onclick`, etc.
2. **No external resources**: No external fonts, images, or stylesheets
3. **Size limits**: Max SVG size 100KB
4. **Validation**: Validate SVG structure before returning

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial specification |

---

## Contact

For questions about these requirements, contact the Layout Builder team.
