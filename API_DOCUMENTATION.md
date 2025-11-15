# Layout Builder v7.5-main API Documentation

**Base URL**: `http://localhost:8504`
**Version**: 7.5.0
**Content-Type**: `application/json`

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Layout System](#layout-system)
5. [Request/Response Examples](#requestresponse-examples)
6. [Error Handling](#error-handling)
7. [Integration Guide](#integration-guide)

---

## Overview

The Layout Builder API provides programmatic access to create, manage, and view presentations using a 6-layout system optimized for data visualization, diagrams, text content, and title slides.

### Key Features
- **6 Production Layouts**: L01, L02, L03, L25, L27, L29
- **RESTful API**: Standard HTTP methods (GET, POST, DELETE)
- **JSON Format**: All requests and responses use JSON
- **Grid System**: 18 rows × 32 columns (1920×1080 resolution)
- **Format Ownership**: Clear separation between Layout Builder and Text Service responsibilities

### Architecture Philosophy
- **Layout Builder**: Provides structural shell and grid positioning
- **Text Service**: Owns content creation and HTML formatting
- **Director Agent**: Orchestrates layout selection and content generation

---

## Authentication

**Current Version**: No authentication required (internal API)

**Future Versions**: Will support:
- API Key authentication
- OAuth 2.0 for external integrations
- Rate limiting per client

---

## API Endpoints

### 1. Get API Information

**Endpoint**: `GET /`

**Description**: Returns API metadata and available endpoints

**Request**:
```bash
curl http://localhost:8504/
```

**Response**:
```json
{
  "message": "v7.5-main: 6-Layout System API",
  "version": "7.5.0",
  "layouts": ["L01", "L02", "L03", "L25", "L27", "L29"],
  "philosophy": "Text Service owns content creation, Layout Builder provides structure",
  "endpoints": {
    "layouts": "GET /api/layouts - Get layout specifications",
    "create_presentation": "POST /api/presentations",
    "get_presentation_data": "GET /api/presentations/{id}",
    "view_presentation": "GET /p/{id}",
    "list_presentations": "GET /api/presentations",
    "delete_presentation": "DELETE /api/presentations/{id}",
    "api_tester": "GET /tester",
    "docs": "/docs"
  }
}
```

---

### 2. Get Layout Specifications

**Endpoint**: `GET /api/layouts`

**Description**: Returns comprehensive information about all available layouts including grid dimensions, content fields, use cases, and interchangeability rules

**Request**:
```bash
curl http://localhost:8504/api/layouts
```

**Response**:
```json
{
  "version": "7.5.0",
  "total_layouts": 6,
  "grid_system": {
    "rows": 18,
    "columns": 32,
    "resolution": "1920x1080",
    "cell_size": "~60px × 60px"
  },
  "layouts": [
    {
      "id": "L01",
      "name": "Centered Chart or Diagram",
      "category": ["Analytic", "Diagram"],
      "purpose": "Large centered visual (chart OR diagram) with descriptive text",
      "chart_diagram_rule": "Charts and diagrams are mutually interchangeable",
      "grid_dimensions": {
        "slide_title": "Row 2, Cols 2-32 (30 grids wide × 1 grid tall)",
        "subtitle": "Row 3, Cols 2-32 (30 grids wide × 1 grid tall)",
        "chart_diagram": "Rows 5-15, Cols 2-32 (30 grids wide × 10 grids tall, 1800×600px)",
        "body_text": "Rows 15-17, Cols 2-32 (30 grids wide × 2 grids tall)",
        "footer": "Row 18",
        "logo": "Rows 17-19, Cols 30-32 (2×2 grid)"
      },
      "content_fields": {
        "required": ["slide_title", "element_1", "element_4", "element_3"],
        "optional": ["presentation_name", "company_logo"],
        "field_mapping": {
          "slide_title": "Slide title text",
          "element_1": "Subtitle/context text",
          "element_4": "Chart or diagram HTML",
          "element_3": "Body text below visual",
          "presentation_name": "Footer presentation name",
          "company_logo": "Footer company logo"
        }
      },
      "use_cases": ["Financial charts", "Process diagrams", "Data visualization", "Strategic frameworks"]
    }
    // ... other layouts (L02, L03, L25, L27, L29)
  ],
  "categories": {
    "Title": ["L29"],
    "Text": ["L25", "L27"],
    "Analytic": ["L01", "L02", "L03"],
    "Diagram": ["L01", "L02", "L25"]
  },
  "interchangeability_rules": {
    "charts_and_diagrams_interchangeable": ["L01", "L02"],
    "charts_only": ["L03"],
    "text_or_diagrams": ["L25"],
    "text_with_imagery": ["L27"],
    "title_slides_only": ["L29"]
  }
}
```

**Use Case**: Call this endpoint to dynamically discover available layouts and their specifications before creating presentations.

---

### 3. Create Presentation

**Endpoint**: `POST /api/presentations`

**Description**: Create a new presentation from JSON data

**Request Headers**:
```
Content-Type: application/json
```

**Request Body Schema**:
```json
{
  "title": "string (required) - Presentation title",
  "slides": [
    {
      "layout": "string (required) - Layout ID (L01, L02, L03, L25, L27, or L29)",
      "content": {
        "...": "object (required) - Content fields specific to the layout"
      }
    }
  ]
}
```

**Example Request**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q4 Business Review",
    "slides": [
      {
        "layout": "L29",
        "content": {
          "hero_content": "<div style=\"width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center;\"><h1 style=\"font-size: 96px; color: white; font-weight: 900;\">Q4 Business Review</h1><p style=\"font-size: 42px; color: rgba(255,255,255,0.9); margin-top: 32px;\">FY 2025 Performance</p></div>"
        }
      },
      {
        "layout": "L01",
        "content": {
          "slide_title": "Revenue Growth",
          "element_1": "Year-over-year comparison",
          "element_4": "<div>Chart HTML here</div>",
          "element_3": "Revenue increased 45% compared to Q4 2024",
          "presentation_name": "Q4 Business Review",
          "company_logo": "🏢"
        }
      }
    ]
  }'
```

**Success Response**:
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "url": "/p/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Presentation 'Q4 Business Review' created successfully"
}
```

**Status Codes**:
- `200 OK`: Presentation created successfully
- `400 Bad Request`: Invalid layout ID or malformed JSON
- `500 Internal Server Error`: Server error during creation

---

### 4. Get Presentation Data

**Endpoint**: `GET /api/presentations/{id}`

**Description**: Retrieve presentation data by ID

**Path Parameters**:
- `id` (string, required): Presentation UUID

**Example Request**:
```bash
curl http://localhost:8504/api/presentations/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Success Response**:
```json
{
  "title": "Q4 Business Review",
  "slides": [
    {
      "layout": "L29",
      "content": {
        "hero_content": "<div>...</div>"
      }
    },
    {
      "layout": "L01",
      "content": {
        "slide_title": "Revenue Growth",
        "element_1": "Year-over-year comparison",
        "element_4": "<div>Chart HTML here</div>",
        "element_3": "Revenue increased 45% compared to Q4 2024",
        "presentation_name": "Q4 Business Review",
        "company_logo": "🏢"
      }
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Presentation found and returned
- `404 Not Found`: Presentation ID not found
- `500 Internal Server Error`: Server error

---

### 5. List All Presentations

**Endpoint**: `GET /api/presentations`

**Description**: Get a list of all presentations

**Example Request**:
```bash
curl http://localhost:8504/api/presentations
```

**Success Response**:
```json
{
  "count": 3,
  "presentations": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Q4 Business Review",
      "created_at": "2025-01-14T10:30:00Z",
      "slide_count": 15
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "title": "Product Launch",
      "created_at": "2025-01-13T14:20:00Z",
      "slide_count": 8
    }
  ]
}
```

**Status Codes**:
- `200 OK`: List returned successfully
- `500 Internal Server Error`: Server error

---

### 6. Delete Presentation

**Endpoint**: `DELETE /api/presentations/{id}`

**Description**: Delete a presentation by ID

**Path Parameters**:
- `id` (string, required): Presentation UUID

**Example Request**:
```bash
curl -X DELETE http://localhost:8504/api/presentations/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Success Response**:
```json
{
  "success": true,
  "message": "Presentation a1b2c3d4-e5f6-7890-abcd-ef1234567890 deleted"
}
```

**Status Codes**:
- `200 OK`: Presentation deleted successfully
- `404 Not Found`: Presentation ID not found
- `500 Internal Server Error`: Server error

---

### 7. View Presentation in Browser

**Endpoint**: `GET /p/{id}`

**Description**: Renders presentation in interactive HTML viewer with Reveal.js

**Path Parameters**:
- `id` (string, required): Presentation UUID

**Example**:
```
http://localhost:8504/p/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response**: HTML page with interactive presentation

**Keyboard Controls**:
- `Arrow Keys`: Navigate between slides
- `G`: Toggle grid overlay
- `B`: Toggle border highlights
- `H`: Toggle help text
- `Esc`: Overview mode

---

## Layout System

### Layout Categories

| Category | Layouts | Purpose |
|----------|---------|---------|
| **Title Slides** | L29 | Opening, section breaks, closing slides |
| **Text Slides** | L25, L27 | Text-heavy content, explanations |
| **Analytic Slides** | L01, L02, L03 | Charts and data visualization |
| **Diagram Slides** | L01, L02, L25 | Process flows, frameworks, diagrams |

### Chart/Diagram Interchangeability

| Layout | Charts | Diagrams | Rule |
|--------|--------|----------|------|
| **L01** | ✅ | ✅ | Mutually interchangeable |
| **L02** | ✅ | ✅ | Mutually interchangeable |
| **L03** | ✅ | ❌ | Charts only |
| **L25** | ❌ | ✅ | Text or diagrams (via rich_content) |
| **L27** | ❌ | ❌ | Text with imagery |
| **L29** | ❌ | ❌ | Title slides only |

### Layout Selection Guide

**For Director Agent or External Applications**:

1. **Opening Slide**: Use **L29** (hero title)
2. **Section Break**: Use **L29** (section divider)
3. **Single Chart/Diagram with Description**: Use **L01**
4. **Complex Diagram with Explanation**: Use **L02**
5. **Comparing Two Charts**: Use **L03**
6. **Text-Heavy Explanation**: Use **L25**
7. **Product/Team Profile with Image**: Use **L27**
8. **Closing Slide**: Use **L29** (thank you)

---

## Request/Response Examples

### Example 1: Complete Presentation with All 6 Layouts

```json
{
  "title": "Complete Layout Showcase",
  "slides": [
    {
      "layout": "L29",
      "content": {
        "hero_content": "<div style='width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center;'><h1 style='font-size: 96px; color: white; font-weight: 900;'>Layout Showcase</h1><p style='font-size: 42px; color: rgba(255,255,255,0.9); margin-top: 32px;'>v7.5-main Demonstration</p></div>"
      }
    },
    {
      "layout": "L01",
      "content": {
        "slide_title": "Revenue Performance",
        "element_1": "Q4 2025 Results",
        "element_4": "<div style='background: #3b82f6; color: white; padding: 100px; text-align: center; font-size: 48px;'>Chart Placeholder</div>",
        "element_3": "Revenue increased 45% year-over-year",
        "presentation_name": "Layout Showcase",
        "company_logo": "🏢"
      }
    },
    {
      "layout": "L02",
      "content": {
        "slide_title": "System Architecture",
        "element_1": "High-level overview",
        "element_3": "<div style='background: #8b5cf6; color: white; padding: 150px; text-align: center; font-size: 36px;'>Diagram Placeholder</div>",
        "element_2": "The architecture consists of three main layers: presentation, business logic, and data access. Each layer is independently scalable and follows microservices patterns.",
        "presentation_name": "Layout Showcase",
        "company_logo": "🏢"
      }
    },
    {
      "layout": "L03",
      "content": {
        "slide_title": "Regional Comparison",
        "element_1": "North America vs Europe",
        "element_4": "<div style='background: #3b82f6; color: white; padding: 80px; text-align: center; font-size: 32px;'>Chart 1</div>",
        "element_2": "<div style='background: #10b981; color: white; padding: 80px; text-align: center; font-size: 32px;'>Chart 2</div>",
        "element_3": "North America showed 35% growth",
        "element_5": "Europe showed 28% growth",
        "presentation_name": "Layout Showcase",
        "company_logo": "🏢"
      }
    },
    {
      "layout": "L25",
      "content": {
        "slide_title": "Key Insights",
        "subtitle": "Q4 Performance Summary",
        "rich_content": "<div style='padding: 40px; font-size: 24px;'><h3 style='color: #1f2937; margin-bottom: 20px;'>Major Achievements</h3><ul style='line-height: 1.8;'><li>Revenue grew 45% YoY</li><li>Customer base expanded to 50 countries</li><li>Product line increased by 30%</li></ul><h3 style='color: #1f2937; margin-top: 40px; margin-bottom: 20px;'>Challenges</h3><ul style='line-height: 1.8;'><li>Supply chain disruptions in Q3</li><li>Increased competition in European markets</li></ul></div>",
        "presentation_name": "Layout Showcase",
        "company_logo": "🏢"
      }
    },
    {
      "layout": "L27",
      "content": {
        "slide_title": "Product Spotlight",
        "element_1": "Our flagship product",
        "image_url": "<div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); height: 100%; display: flex; align-items: center; justify-content: center; color: white; font-size: 48px; font-weight: bold;'>Product Image</div>",
        "main_content": "This revolutionary product combines cutting-edge technology with user-friendly design. Key features include real-time analytics, AI-powered insights, and seamless integration with existing systems. Customer satisfaction rating: 4.9/5.0.",
        "presentation_name": "Layout Showcase",
        "company_logo": "🏢"
      }
    },
    {
      "layout": "L29",
      "content": {
        "hero_content": "<div style='width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center;'><h1 style='font-size: 96px; color: white; font-weight: 900;'>Thank You</h1><p style='font-size: 32px; color: rgba(255,255,255,0.9); margin-top: 48px;'>Questions?</p></div>"
      }
    }
  ]
}
```

### Example 2: Python Integration

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8504"

# 1. Get layout specifications
response = requests.get(f"{BASE_URL}/api/layouts")
layouts = response.json()
print(f"Available layouts: {len(layouts['layouts'])}")

# 2. Create presentation
presentation_data = {
    "title": "Automated Report",
    "slides": [
        {
            "layout": "L29",
            "content": {
                "hero_content": "<div style='width: 100%; height: 100%; background: #1f2937; display: flex; align-items: center; justify-content: center;'><h1 style='font-size: 96px; color: white;'>Automated Report</h1></div>"
            }
        },
        {
            "layout": "L25",
            "content": {
                "slide_title": "Executive Summary",
                "rich_content": "<div style='padding: 40px; font-size: 24px;'><p>Key findings from automated analysis...</p></div>",
                "presentation_name": "Automated Report",
                "company_logo": "🏢"
            }
        }
    ]
}

response = requests.post(
    f"{BASE_URL}/api/presentations",
    headers={"Content-Type": "application/json"},
    json=presentation_data
)

result = response.json()
print(f"Presentation created: {result['url']}")
print(f"View at: {BASE_URL}{result['url']}")

# 3. Retrieve presentation
presentation_id = result['id']
response = requests.get(f"{BASE_URL}/api/presentations/{presentation_id}")
presentation = response.json()
print(f"Retrieved presentation with {len(presentation['slides'])} slides")

# 4. List all presentations
response = requests.get(f"{BASE_URL}/api/presentations")
all_presentations = response.json()
print(f"Total presentations: {all_presentations['count']}")
```

### Example 3: JavaScript/TypeScript Integration

```typescript
// API Client
const API_BASE_URL = 'http://localhost:8504';

interface Presentation {
  title: string;
  slides: Slide[];
}

interface Slide {
  layout: 'L01' | 'L02' | 'L03' | 'L25' | 'L27' | 'L29';
  content: Record<string, string>;
}

// Get layout specifications
async function getLayouts() {
  const response = await fetch(`${API_BASE_URL}/api/layouts`);
  const layouts = await response.json();
  console.log(`Available layouts: ${layouts.total_layouts}`);
  return layouts;
}

// Create presentation
async function createPresentation(data: Presentation) {
  const response = await fetch(`${API_BASE_URL}/api/presentations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();
  console.log(`Created: ${result.url}`);
  return result;
}

// Usage
const presentation: Presentation = {
  title: 'Quarterly Report',
  slides: [
    {
      layout: 'L29',
      content: {
        hero_content: '<div>Title Slide HTML</div>',
      },
    },
    {
      layout: 'L01',
      content: {
        slide_title: 'Performance Metrics',
        element_1: 'Q4 2025',
        element_4: '<div>Chart HTML</div>',
        element_3: 'Description text',
        presentation_name: 'Quarterly Report',
        company_logo: '🏢',
      },
    },
  ],
};

createPresentation(presentation);
```

---

## Dynamic Chart Integration

### Overview

Layout Builder v7.5-main **fully supports dynamic chart HTML** from the Analytics Microservice, including ApexCharts, Chart.js, D3.js, and other JavaScript-based visualization libraries.

**Supported Features**:
- ✅ Embedded `<script>` tags with complex JavaScript
- ✅ Template literals with backticks and `${}` expressions
- ✅ Special characters (backslashes, HTML tags, Unicode)
- ✅ Multiple charts on same slide (L03 layout)
- ✅ Real-time chart rendering in browser

### Recommended Layouts for Charts

| Layout | Best For | Chart Field | Dimensions |
|--------|----------|-------------|------------|
| **L01** | Single centered chart | `element_4` | 1800×600px |
| **L02** | Chart + explanation | `element_3` | 1260×720px |
| **L03** | Two comparison charts | `element_4`, `element_2` | 840×540px each |

### ApexCharts Example

```json
{
  "title": "Sales Dashboard",
  "slides": [
    {
      "layout": "L01",
      "content": {
        "slide_title": "Monthly Revenue Trend",
        "element_1": "Q1-Q4 2024 Performance",
        "element_4": "<div id='chart-revenue' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  var options = {\n    chart: { type: 'line', height: '100%' },\n    series: [{\n      name: 'Revenue',\n      data: [30, 40, 35, 50, 49, 60, 70, 91]\n    }],\n    xaxis: {\n      categories: [`Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`]\n    },\n    yaxis: {\n      labels: {\n        formatter: function(val) {\n          return `$${val}M`;\n        }\n      }\n    },\n    colors: ['#667eea'],\n    stroke: { curve: 'smooth', width: 3 }\n  };\n  var chart = new ApexCharts(document.querySelector('#chart-revenue'), options);\n  chart.render();\n})();\n</script>",
        "element_3": "Revenue grew 203% from January to August.",
        "presentation_name": "Sales Dashboard",
        "company_logo": "📊"
      }
    }
  ]
}
```

### JavaScript Escaping

Layout Builder automatically handles JavaScript context escaping to support:
- **Template literals**: `` `Hello ${name}` ``
- **Backslashes**: `C:\\Users\\Data`
- **Script tags**: `</script>` (escaped as `<\/script>`)
- **Unicode separators**: `\u2028`, `\u2029`

**Implementation** (server.py:199-216):
```python
presentation_json = json.dumps(presentation, ensure_ascii=False)
presentation_json_safe = (
    presentation_json
    .replace('\\', '\\\\')
    .replace('</', '<\\/')
    .replace('\u2028', '\\u2028')
    .replace('\u2029', '\\u2029')
)
```

### Best Practices

1. **Use IIFEs**: Wrap chart code in `(function() { ... })()` to avoid global scope pollution
2. **Unique IDs**: Use unique chart container IDs (e.g., `chart-{slide-id}-revenue`)
3. **Relative sizing**: Use `width: 100%; height: 100%` instead of fixed pixels
4. **Verify libraries**: Check if chart library is loaded before rendering

### Complete Documentation

📖 **Full Integration Guide**: See [docs/ANALYTICS_INTEGRATION_GUIDE.md](docs/ANALYTICS_INTEGRATION_GUIDE.md) for:
- Complete ApexCharts examples (bar, line, pie, area charts)
- Field mapping for all chart layouts (L01, L02, L03)
- Template literal usage patterns
- Troubleshooting guide
- Testing procedures

### Test Presentation

**Test File**: `test_analytics_apexcharts.json`

Create test presentation:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test_analytics_apexcharts.json
```

This test includes:
- L01 with template literal syntax
- L02 with special characters and backslashes
- L03 with dual charts
- Comprehensive JavaScript escaping validation

---

## Error Handling

### Error Response Format

All errors return JSON with the following structure:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Error | Description |
|-------------|-------|-------------|
| `400` | Bad Request | Invalid JSON, missing required fields, or invalid layout ID |
| `404` | Not Found | Presentation ID not found |
| `500` | Internal Server Error | Server error during processing |

### Error Examples

**Invalid Layout ID**:
```json
{
  "detail": "Invalid layout 'L99'. Valid layouts: ['L01', 'L02', 'L03', 'L25', 'L27', 'L29']"
}
```

**Missing Required Field**:
```json
{
  "detail": "Field validation error: 'title' is required"
}
```

**Presentation Not Found**:
```json
{
  "detail": "Presentation not found"
}
```

---

## Integration Guide

### For Director Agent

The Director Agent should follow this workflow when calling the Layout Builder API:

```
1. Receive user request
2. Analyze content requirements
3. Call GET /api/layouts to get layout specifications
4. Select appropriate layout based on:
   - Slide purpose (title, content, analytics, diagram)
   - Content type (text, chart, diagram, image)
   - Interchangeability rules
5. Call Text Service to generate HTML content for selected layout
6. Transform Text Service response to Layout Builder format
7. POST to /api/presentations with complete presentation JSON
8. Return presentation URL to user
```

**Example Director Agent Decision Tree**:

```python
def select_layout(slide_purpose, content_type):
    if slide_purpose == "opening" or slide_purpose == "closing":
        return "L29"

    elif slide_purpose == "section_break":
        return "L29"

    elif content_type == "single_chart":
        return "L01"

    elif content_type == "single_diagram":
        return "L01"

    elif content_type == "diagram_with_explanation":
        return "L02"

    elif content_type == "two_charts_comparison":
        return "L03"

    elif content_type == "text_heavy":
        return "L25"

    elif content_type == "image_with_text":
        return "L27"

    else:
        return "L25"  # Default to text-heavy layout
```

### For Text Service

Text Service should follow format ownership rules:

**L25 (Text-Heavy Content)**:
- Layout Builder owns: `slide_title`, `subtitle`
- Text Service owns: `rich_content` (full HTML with inline styles)

**L29 (Hero Slide)**:
- Text Service owns: `hero_content` (full HTML for entire slide)

**L01, L02, L03, L27**:
- Layout Builder owns: Titles and structural text
- Text Service provides: Charts, diagrams, and formatted content as HTML

### CORS Configuration

For cross-origin requests, configure allowed origins via environment variable:

```bash
export ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8000"
python server.py
```

Current default: `*` (allow all origins - development only)

---

## OpenAPI/Swagger Documentation

Interactive API documentation is available at:

```
http://localhost:8504/docs
```

This provides:
- Interactive API testing interface
- Request/response schemas
- Example requests
- Authentication information (when implemented)

---

## Versioning

**Current Version**: 7.5.0

**Version Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes to API or layout system
- **MINOR**: New features, new layouts
- **PATCH**: Bug fixes, performance improvements

**Version History**:
- `7.5.0` (2025-01-14): 6-layout system with comprehensive API

---

## Rate Limiting

**Current**: No rate limiting (internal API)

**Future Implementation**:
- 100 requests per minute per IP
- 1000 presentations per day per API key
- Burst allowance: 20 requests per 10 seconds

---

## Support

- **API Documentation**: `/docs` endpoint
- **Layout Specifications**: `/api/layouts` endpoint
- **Technical Support**: Contact Layout Builder team
- **Issue Reporting**: Include presentation JSON, error message, and expected behavior

---

**Last Updated**: 2025-01-14
**API Version**: 7.5.0
**Document Version**: 1.0
