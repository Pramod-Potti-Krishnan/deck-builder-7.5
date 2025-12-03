# Layout Service - AI Orchestrator Integration Guide

## Overview

This document describes how the Visual Elements Orchestrator (Port 8090) integrates with the Layout Service (Port 8504) to provide AI-generated content injection.

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI CONTENT INJECTION FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐         ┌─────────────────────┐                      │
│  │  Visual Elements │         │   Layout Service    │                      │
│  │   Orchestrator   │ ──────▶ │   (Port 8504)       │                      │
│  │   (Port 8090)    │   PUT   │                     │                      │
│  └──────────────────┘         └─────────────────────┘                      │
│                                                                             │
│  After AI generates content, Orchestrator makes direct PUT requests        │
│  to Layout Service to inject content into presentation elements.           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    USER EDIT FLOW (Unchanged)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐    User types/edits     ┌─────────────────────┐              │
│  │ Frontend │ ──────────────────────▶ │   Layout Service    │              │
│  │ (React)  │      postMessage        │   (Port 8504)       │              │
│  └──────────┘                         └─────────────────────┘              │
│                                                                             │
│  User-typed content changes continue through the existing frontend         │
│  route via postMessage to the Layout Service iframe.                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints Used by Orchestrator

The Orchestrator calls the following Layout Service endpoints to inject AI-generated content:

### 1. Get Presentation
```
GET /api/presentations/{presentation_id}
```
Used to fetch current presentation state before updates.

### 2. Update Slide
```
PUT /api/presentations/{presentation_id}/slides/{slide_index}
```
Used to update element arrays within a slide.

**Query Parameters:**
- `created_by`: Attribution for the update (e.g., "orchestrator-chart")

**Request Body:**
```json
{
  "text_boxes": [...],
  "charts": [...],
  "images": [...],
  "infographics": [...],
  "diagrams": [...]
}
```

---

## Element Type Mapping

| Orchestrator Type | Layout Service Field | Content Fields |
|-------------------|---------------------|----------------|
| Chart | `charts` | `chart_config`, `chart_html`, `chart_type` |
| Diagram | `diagrams` | `svg_content`, `mermaid_code`, `diagram_type` |
| Text | `text_boxes` | `content` (HTML) |
| Table | `text_boxes` | `content` (HTML table) |
| Image | `images` | `image_url`, `alt_text` |
| Infographic | `infographics` | `svg_content`, `html_content`, `infographic_type` |

---

## Injection Flow Details

### Step-by-Step Process

1. **Orchestrator receives generation request** from frontend
2. **Orchestrator calls AI service** to generate content
3. **AI service returns generated content** (chart config, SVG, HTML, etc.)
4. **Orchestrator fetches current slide** from Layout Service
5. **Orchestrator updates element** in the appropriate array
6. **Orchestrator PUTs updated slide** back to Layout Service
7. **Orchestrator returns response** to frontend with injection status

### Example: Chart Injection

```
1. Frontend → Orchestrator: POST /chart
   {
     "element_id": "chart-1",
     "context": { "presentation_id": "pres-123", "slide_index": 2 },
     "prompt": "Show revenue growth"
   }

2. Orchestrator → Chart AI: Generate chart

3. Chart AI → Orchestrator: Chart.js config

4. Orchestrator → Layout Service: GET /api/presentations/pres-123
   Response: { slides: [...] }

5. Orchestrator: Find/create chart element in slide 2's charts array

6. Orchestrator → Layout Service: PUT /api/presentations/pres-123/slides/2
   {
     "charts": [
       {
         "id": "chart-1",
         "chart_config": { ... },
         "chart_type": "bar"
       }
     ]
   }

7. Orchestrator → Frontend:
   {
     "success": true,
     "chart_config": { ... },
     "injected": true
   }
```

---

## Version Tracking

All Orchestrator injections include a `created_by` attribution:

| Source | created_by Value |
|--------|-----------------|
| Chart generation | `orchestrator-chart` |
| Diagram generation | `orchestrator-diagram` |
| Text generation | `orchestrator-text` |
| Table generation | `orchestrator-table` |
| Image generation | `orchestrator-image` |
| Infographic generation | `orchestrator-infographic` |

This allows tracking which elements were AI-generated vs. user-created.

---

## Error Handling

### Injection Failures

If the Orchestrator cannot inject content into Layout Service:

1. **Generation still succeeds** - AI content is returned to frontend
2. **`injected: false`** in response
3. **`injection_error`** contains the error message
4. **Frontend can fallback** to manual injection via postMessage

### Common Injection Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Unable to connect to Layout service` | Layout Service not running | Start Layout Service |
| `Presentation {id} not found` | Invalid presentation ID | Check presentation exists |
| `Slide index {n} out of range` | Invalid slide index | Verify slide exists |

---

## Frontend Notification

After successful injection, the frontend should:

1. **Check `injected` field** in Orchestrator response
2. **If `true`**: Refresh the Layout Service iframe to see changes
3. **If `false`**: Use `postMessage` to manually inject the content

### Refresh Pattern

```typescript
// In frontend after receiving Orchestrator response
if (result.injected) {
  // Content was injected directly - refresh iframe
  const iframe = document.getElementById('presentation-iframe');
  iframe.contentWindow.postMessage({ type: 'REFRESH_SLIDE' }, '*');
} else {
  // Injection failed - manual update
  iframe.contentWindow.postMessage({
    type: 'UPDATE_ELEMENT',
    element_id: result.element_id,
    content: result.content
  }, '*');
}
```

---

## Configuration

### Orchestrator Settings

The Orchestrator connects to Layout Service via environment variable:

```env
LAYOUT_SERVICE_URL=http://localhost:8504
```

Default: `http://localhost:8504`

### Timeout

The Orchestrator uses a 30-second timeout for Layout Service requests. This is configured in the Orchestrator's `config.py`:

```python
SERVICE_TIMEOUT: float = 30.0
```

---

## Security Considerations

1. **Internal Communication Only**: Orchestrator-to-Layout Service communication is internal (same network)
2. **No Authentication Required**: Relies on network isolation
3. **Attribution Tracking**: All changes tracked via `created_by` parameter
4. **No Direct User Access**: Users cannot directly call injection endpoints

---

## Testing Integration

### Verify Layout Service is Running

```bash
curl http://localhost:8504/health
# Expected: {"status":"healthy"}
```

### Test Injection Manually

```bash
# Create a test presentation first, then:
curl -X PUT "http://localhost:8504/api/presentations/{id}/slides/0" \
  -H "Content-Type: application/json" \
  -d '{
    "charts": [{
      "id": "test-chart",
      "chart_type": "bar",
      "chart_config": {"type": "bar", "data": {}}
    }]
  }'
```

### Test via Orchestrator

```bash
curl -X POST "http://localhost:8090/chart" \
  -H "Content-Type: application/json" \
  -d '{
    "element_id": "chart-1",
    "context": {
      "presentation_id": "your-pres-id",
      "presentation_title": "Test",
      "slide_id": "slide-1",
      "slide_index": 0
    },
    "position": {"grid_row": "2/10", "grid_column": "2/14"},
    "prompt": "Show sample data",
    "chart_type": "bar",
    "generate_data": true
  }'
```

---

## Troubleshooting

### Issue: Content Not Appearing

1. **Check Orchestrator logs** for injection errors
2. **Verify presentation ID** is correct
3. **Check slide index** is within range
4. **Confirm Layout Service** is running on port 8504

### Issue: Injection Failing with Connection Error

1. **Verify Layout Service URL** in Orchestrator config
2. **Check network connectivity** between services
3. **Ensure Layout Service** is accepting connections

### Issue: Old Content Still Showing

1. **Refresh the iframe** after injection
2. **Check element ID** matches existing element
3. **Verify created_by** shows Orchestrator attribution

---

## Future Enhancements

1. **WebSocket Notifications**: Real-time updates when content is injected
2. **Batch Injection**: Multiple elements in single request
3. **Rollback Support**: Undo AI-generated changes
4. **Version History**: Track all AI generations for an element

---

## Related Documentation

- [Visual Elements Orchestrator API](../../visual_elements_orchestrator/v1.0/FRONTEND_API.md) - Full API reference for frontend
- [Layout Service API](./API.md) - Layout Service endpoint documentation
