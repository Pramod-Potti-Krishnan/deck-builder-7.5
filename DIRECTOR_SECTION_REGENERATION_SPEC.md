# Director Service: Section Regeneration API Specification

**Version:** 1.0
**Date:** 2025-01-24
**Status:** Phase 3 Requirements for Layout Builder v7.5-main
**Feature:** AI-Powered Section Regeneration

---

## Overview

The Layout Builder v7.5-main now supports **section-based AI regeneration**, allowing users to select specific sections within slides and request AI-powered content improvements. This document specifies the API requirements for Director Service to support this feature.

### User Experience Flow

1. User opens presentation in Layout Builder viewer
2. User clicks "📋 Review Mode" button
3. User selects one or more sections (title, body, chart, etc.)
4. User enters instruction: "Make this more engaging with examples"
5. Layout Builder calls Director Service to regenerate selected sections
6. Director returns enhanced content for each section
7. Layout Builder updates sections with smooth animations

---

## Why Section-Based Regeneration?

### Current Limitation: Full-Slide Regeneration
Currently, when users want to improve content, they must regenerate entire slides, which:
- Overwrites sections that were already perfect
- Forces users to re-edit unchanged sections
- Wastes API tokens and processing time
- Creates frustration when only one part needs improvement

### Solution: Surgical Content Updates
Section-based regeneration enables:
- **Precision**: Update only the title, or only the body text
- **Efficiency**: Regenerate 3 bullet points instead of entire slide
- **Iteration**: Refine specific elements without touching others
- **Speed**: Faster processing for small content chunks
- **Cost**: Lower token usage for targeted improvements

### Real-World Example

**Scenario**: User has a slide with:
- ✅ Perfect title: "Q4 Revenue Performance"
- ✅ Perfect chart: Beautiful visualization of data
- ❌ Boring body text: "Revenue increased. Sales were good."

**Current Flow** (Full-Slide Regeneration):
```
User: "Make the body text more engaging"
→ Director regenerates ENTIRE slide
→ May change the perfect title
→ May alter the chart configuration
→ Wastes tokens on unchanged sections
```

**New Flow** (Section Regeneration):
```
User: Selects ONLY the body text section
User: "Make this more engaging with specific examples"
→ Director regenerates ONLY the body text
→ Title stays perfect
→ Chart stays perfect
→ Only body text improved: "Q4 revenue surged 23% YoY, driven by..."
```

---

## API Endpoint Specification

### Endpoint

```
POST /api/regenerate-section
```

### Request Schema

```json
{
  "presentation_context": {
    "presentation_id": "uuid",
    "presentation_title": "Q4 Business Review",
    "slide_index": 2,
    "total_slides": 15,
    "slide_layout": "L25"
  },
  "section_context": {
    "section_id": "slide-2-section-body",
    "section_type": "body",
    "current_content": "<div><p>Revenue increased. Sales were good.</p></div>",
    "content_format": "html",
    "max_length": 500
  },
  "regeneration_request": {
    "user_instruction": "Make this more engaging with specific examples and data points",
    "tone": "professional",
    "preserve_structure": true,
    "preserve_formatting": true
  },
  "surrounding_context": {
    "slide_title": "Q4 Revenue Performance",
    "slide_subtitle": "Regional Breakdown",
    "other_sections": [
      {
        "section_type": "chart",
        "description": "Bar chart showing revenue by region"
      }
    ]
  }
}
```

### Request Field Descriptions

#### `presentation_context` (required)
Provides context about the presentation and slide:
- `presentation_id`: UUID of the presentation
- `presentation_title`: Title for thematic context
- `slide_index`: Zero-based position in presentation
- `total_slides`: Total number of slides (for pacing context)
- `slide_layout`: Layout type (L01, L02, L03, L25, L27, L29)

#### `section_context` (required)
Details about the specific section being regenerated:
- `section_id`: Unique identifier (format: `slide-{index}-section-{type}`)
- `section_type`: One of: `title`, `subtitle`, `body`, `chart`, `diagram`, `image`, `text`, `content`, `hero`
- `current_content`: Existing HTML content to be improved
- `content_format`: Always `"html"` for now
- `max_length`: Character limit for generated content (optional)

#### `regeneration_request` (required)
User's regeneration instructions:
- `user_instruction`: Natural language instruction from user
- `tone`: Desired tone (professional, casual, formal, enthusiastic, etc.)
- `preserve_structure`: Whether to keep HTML structure (true/false)
- `preserve_formatting`: Whether to maintain styling (true/false)

#### `surrounding_context` (optional but recommended)
Context from other sections to ensure coherence:
- `slide_title`: Title of the slide
- `slide_subtitle`: Subtitle of the slide
- `other_sections`: Array of other sections on the slide for context

---

### Response Schema

```json
{
  "success": true,
  "section_id": "slide-2-section-body",
  "section_type": "body",
  "updated_content": "<div><p>Q4 revenue surged 23% YoY, reaching $4.2M, driven by strong performance in APAC (+35%) and EMEA (+28%). Key wins included the TechCorp enterprise deal ($1.2M ARR) and successful product launch in Southeast Asia.</p></div>",
  "metadata": {
    "model_used": "claude-sonnet-4.5",
    "processing_time_ms": 1250,
    "tokens_used": 145,
    "content_length": 287,
    "changes_made": [
      "Added specific percentage data (23% YoY)",
      "Included regional breakdowns (APAC +35%, EMEA +28%)",
      "Added concrete examples (TechCorp deal, Southeast Asia launch)",
      "Enhanced engagement with specific dollar amounts"
    ],
    "preserved_elements": [
      "HTML structure (div > p)",
      "Professional tone",
      "Focus on Q4 revenue"
    ]
  },
  "warnings": [],
  "alternatives": [
    {
      "variant": "more_concise",
      "content": "<div><p>Q4 revenue jumped 23% to $4.2M, with APAC and EMEA driving growth through major enterprise wins.</p></div>",
      "description": "More concise version focusing on key metrics"
    }
  ]
}
```

### Response Field Descriptions

#### Top-Level Fields
- `success`: Boolean indicating if regeneration succeeded
- `section_id`: Echo of the section ID from request
- `section_type`: Echo of the section type from request
- `updated_content`: New HTML content (ready to inject into DOM)

#### `metadata` (required)
Processing details:
- `model_used`: AI model used for generation
- `processing_time_ms`: Time taken to generate
- `tokens_used`: Token count for billing/tracking
- `content_length`: Character count of generated content
- `changes_made`: Array of specific improvements made
- `preserved_elements`: Array of elements that were kept

#### `warnings` (optional)
Array of warning messages:
- Content exceeded max_length (truncated)
- Unable to preserve exact formatting
- User instruction conflicted with context

#### `alternatives` (optional)
Array of alternative versions:
- `variant`: Name of the variant (e.g., "more_concise", "more_detailed")
- `content`: HTML content of the alternative
- `description`: What makes this variant different

---

## Section Types and Regeneration Patterns

### Section Types by Layout

#### L01: Centered Chart with Text Below
- `title`: Slide title
- `subtitle`: Subtitle or context
- `chart`: Chart/visualization (ApexCharts/Chart.js HTML)
- `body`: Body text below chart

#### L02: Left Diagram with Text on Right
- `title`: Slide title
- `subtitle`: Subtitle
- `diagram`: Left-side diagram/image
- `text`: Right-side text content

#### L03: Two Charts in Columns with Text Below
- `title`: Slide title
- `subtitle`: Subtitle
- `chart1`: Left chart
- `chart2`: Right chart
- `body-left`: Left body text
- `body-right`: Right body text

#### L25: Main Content Shell (Most Common)
- `title`: Slide title
- `subtitle`: Subtitle
- `content`: Rich content area (1800×720px)

#### L27: Image Left with Content Right
- `title`: Slide title
- `subtitle`: Subtitle
- `image`: Left-side image
- `text`: Right-side text content

#### L29: Full-Bleed Hero Slide
- `hero`: Full-slide content (1920×1080px)

---

## Regeneration Scenarios and Expected Behavior

### Scenario 1: Title Enhancement
```json
{
  "section_type": "title",
  "current_content": "Sales Report",
  "user_instruction": "Make this title more compelling and specific"
}
```

**Expected Output:**
```html
"Q4 2024 Sales Performance: Record-Breaking Quarter"
```

**Director Should:**
- Keep it concise (≤80 characters)
- Make it specific and compelling
- Maintain professional tone
- Preserve HTML structure (if any)

---

### Scenario 2: Body Text with Data
```json
{
  "section_type": "body",
  "current_content": "<p>Revenue increased significantly this quarter.</p>",
  "user_instruction": "Add specific numbers and regional breakdown",
  "surrounding_context": {
    "slide_title": "Q4 Revenue Growth",
    "other_sections": [
      {
        "section_type": "chart",
        "description": "Bar chart showing 23% YoY growth"
      }
    ]
  }
}
```

**Expected Output:**
```html
<p>Revenue surged 23% year-over-year to $4.2M in Q4, with exceptional growth in APAC (+35%) and EMEA (+28%). North America maintained steady performance at +12%, while our new Southeast Asia market contributed $450K in its first full quarter.</p>
```

**Director Should:**
- Reference data from chart context
- Add specific percentages and amounts
- Structure information clearly
- Maintain HTML formatting

---

### Scenario 3: Chart Description Update
```json
{
  "section_type": "chart",
  "current_content": "<canvas id=\"chart-123\"></canvas><script>new Chart(...)</script>",
  "user_instruction": "Change the chart title to be more descriptive",
  "preserve_structure": true
}
```

**Expected Output:**
```html
<canvas id="chart-123"></canvas>
<script>
  new Chart(document.getElementById('chart-123'), {
    type: 'bar',
    data: { /* existing data */ },
    options: {
      plugins: {
        title: {
          display: true,
          text: 'Regional Revenue Performance (Q4 2024)' // CHANGED
        }
      }
    }
  });
</script>
```

**Director Should:**
- Preserve the entire chart structure
- Only modify the requested element (title)
- Keep all data and configuration intact
- Validate JavaScript syntax

---

### Scenario 4: Hero Content Regeneration
```json
{
  "section_type": "hero",
  "current_content": "<div style=\"font-size: 48px;\">Welcome</div>",
  "user_instruction": "Make this more visually striking with gradient and animation"
}
```

**Expected Output:**
```html
<div style="
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-size: 72px;
  font-weight: bold;
  color: white;
  text-shadow: 0 4px 12px rgba(0,0,0,0.3);
  animation: fadeInScale 1s ease-out;
">
  Welcome to the Future
</div>
<style>
@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
```

**Director Should:**
- Create visually appealing designs
- Use modern CSS (gradients, shadows, animations)
- Ensure responsive scaling
- Follow design best practices

---

## Content Constraints and Guidelines

### HTML Generation Rules

1. **Valid HTML**: All output must be valid, well-formed HTML
2. **No External Dependencies**: Avoid requiring external CSS/JS unless already in layout
3. **Inline Styles**: Prefer inline styles for portability
4. **Responsive**: Content should scale appropriately
5. **Accessibility**: Include alt text, ARIA labels where needed

### Content Length Guidelines

| Section Type | Recommended Max | Hard Limit |
|--------------|----------------|------------|
| title | 80 characters | 100 characters |
| subtitle | 120 characters | 150 characters |
| body | 500 characters | 1000 characters |
| content | 2000 characters | 5000 characters |
| hero | 1000 characters | 3000 characters |

### Style Guidelines

1. **Fonts**: Use system fonts or fonts already loaded in viewer
   - `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif`
2. **Colors**: Maintain brand consistency or use professional palette
3. **Spacing**: Use consistent padding/margins
4. **Typography**: Clear hierarchy with appropriate font sizes

---

## Chart and Visualization Regeneration

### Supported Chart Libraries

The Layout Builder uses:
- **ApexCharts** 3.45.0 (for most business charts)
- **Chart.js** 4.4.0 + plugins (for specialized charts)

### Chart Regeneration Patterns

#### Pattern 1: Update Chart Data
```json
{
  "section_type": "chart",
  "user_instruction": "Update the data to show Q4 instead of Q3",
  "preserve_structure": true
}
```

**Director Should:**
- Locate data array in chart configuration
- Update values while preserving structure
- Adjust labels (Q3 → Q4)
- Maintain chart type and styling

#### Pattern 2: Change Chart Type
```json
{
  "section_type": "chart",
  "user_instruction": "Convert this bar chart to a line chart",
  "preserve_structure": false
}
```

**Director Should:**
- Change chart type parameter
- Adjust options for new chart type
- Preserve data values
- Ensure visual coherence

#### Pattern 3: Add Chart Elements
```json
{
  "section_type": "chart",
  "user_instruction": "Add a trend line showing 15% growth",
  "preserve_structure": true
}
```

**Director Should:**
- Add trend line dataset
- Calculate appropriate values
- Style trend line distinctly
- Update legend if needed

---

## Error Handling

### Expected Error Responses

```json
{
  "success": false,
  "error": {
    "code": "CONTENT_TOO_LONG",
    "message": "Generated content exceeds max_length constraint",
    "details": {
      "generated_length": 1200,
      "max_length": 500,
      "truncated_content": "<div>...</div>"
    }
  },
  "section_id": "slide-2-section-body",
  "fallback_content": "<div><p>Original content preserved due to error</p></div>"
}
```

### Error Codes

| Code | Description | Recovery Action |
|------|-------------|-----------------|
| `CONTENT_TOO_LONG` | Generated content exceeds max_length | Provide truncated version |
| `INVALID_INSTRUCTION` | User instruction unclear or conflicting | Request clarification |
| `CONTEXT_INSUFFICIENT` | Not enough context to regenerate | Request more context |
| `FORMAT_MISMATCH` | Cannot preserve requested format | Return best-effort alternative |
| `CHART_PARSE_ERROR` | Cannot parse chart configuration | Return original content |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Provide retry-after time |

---

## Performance Requirements

### Response Time Targets

| Section Type | Target Response Time | Max Acceptable |
|--------------|---------------------|----------------|
| title, subtitle | < 1 second | 2 seconds |
| body, text | < 2 seconds | 4 seconds |
| chart (minor edits) | < 2 seconds | 4 seconds |
| chart (full regen) | < 4 seconds | 8 seconds |
| content, hero | < 3 seconds | 6 seconds |

### Token Optimization

- **Small sections** (title, subtitle): Aim for <100 tokens
- **Medium sections** (body, text): Aim for <300 tokens
- **Large sections** (content, hero): Aim for <800 tokens
- **Charts**: Variable, but minimize prompt tokens

---

## Context Optimization Strategies

### Minimal Context (Fast, Lower Quality)
```json
{
  "section_context": {
    "section_type": "body",
    "current_content": "Revenue increased."
  },
  "regeneration_request": {
    "user_instruction": "Add numbers"
  }
}
```

### Rich Context (Slower, Higher Quality)
```json
{
  "presentation_context": {
    "presentation_title": "Q4 Business Review",
    "slide_layout": "L25"
  },
  "section_context": {
    "section_type": "body",
    "current_content": "Revenue increased."
  },
  "regeneration_request": {
    "user_instruction": "Add numbers"
  },
  "surrounding_context": {
    "slide_title": "Q4 Revenue Performance",
    "other_sections": [
      {
        "section_type": "chart",
        "description": "Bar chart showing 23% YoY growth, $4.2M total"
      }
    ]
  }
}
```

**Recommendation**: Layout Builder will send rich context by default. Director should use all available context to produce coherent, accurate content.

---

## Integration Timeline

### Phase 3A: Basic Integration (Week 1-2)
- ✅ Layout Builder: API client implementation
- ✅ Director: Basic endpoint with title/subtitle/body regeneration
- ✅ Testing: Unit tests for API contract
- ✅ Deployment: Staging environment

### Phase 3B: Chart Support (Week 3-4)
- ✅ Director: Chart parsing and regeneration
- ✅ Layout Builder: Chart validation
- ✅ Testing: Chart regeneration scenarios
- ✅ Deployment: Production rollout (feature flag)

### Phase 3C: Advanced Features (Week 5-6)
- ✅ Alternative generations
- ✅ Rich metadata and change tracking
- ✅ Performance optimization
- ✅ Full production release

---

## Testing Requirements

### Director Service Must Provide

1. **Test Endpoint**: `/api/regenerate-section/test` for integration testing
2. **Mock Mode**: Flag to return deterministic results for testing
3. **Health Check**: `/api/health` endpoint for monitoring

### Test Scenarios to Support

1. **Title Regeneration**: Short, concise improvements
2. **Body Regeneration**: Paragraph-level enhancements
3. **Chart Regeneration**: Data and configuration updates
4. **Error Handling**: Invalid inputs, rate limits, timeouts
5. **Edge Cases**: Empty content, very long content, special characters

---

## Security Considerations

### Input Validation
- Sanitize HTML to prevent XSS attacks
- Validate section types against allowed values
- Limit content length to prevent DoS
- Rate limit requests per user/presentation

### Content Safety
- Filter inappropriate content
- Preserve user data integrity
- Don't expose sensitive information
- Comply with content policies

---

## Monitoring and Analytics

### Metrics to Track

1. **Performance**: Response times by section type
2. **Quality**: User acceptance rate (did they keep the change?)
3. **Usage**: Requests per section type
4. **Errors**: Error rates by error code
5. **Tokens**: Token usage per request

### Recommended Logging

```json
{
  "timestamp": "2025-01-24T12:34:56Z",
  "request_id": "uuid",
  "presentation_id": "uuid",
  "section_type": "body",
  "section_length": 287,
  "processing_time_ms": 1250,
  "tokens_used": 145,
  "model_used": "claude-sonnet-4.5",
  "user_instruction_length": 45,
  "success": true
}
```

---

## API Client Implementation (Layout Builder Side)

### Example Usage

```javascript
async function regenerateSection(presentationId, sectionData) {
  const response = await fetch(
    `${DIRECTOR_API_URL}/api/regenerate-section`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_TOKEN}`
      },
      body: JSON.stringify({
        presentation_context: {
          presentation_id: presentationId,
          presentation_title: window.PRESENTATION_DATA.title,
          slide_index: sectionData.slideIndex,
          total_slides: window.PRESENTATION_DATA.slides.length,
          slide_layout: sectionData.layout
        },
        section_context: {
          section_id: sectionData.sectionId,
          section_type: sectionData.sectionType,
          current_content: sectionData.content,
          content_format: 'html'
        },
        regeneration_request: {
          user_instruction: userInstruction,
          tone: 'professional',
          preserve_structure: true,
          preserve_formatting: true
        },
        surrounding_context: getSurroundingContext(sectionData.slideIndex)
      })
    }
  );

  const result = await response.json();

  if (result.success) {
    updateSectionInDOM(result.section_id, result.updated_content);
  } else {
    handleError(result.error);
  }
}
```

---

## Appendix: Complete Example Request/Response

### Example Request

```json
{
  "presentation_context": {
    "presentation_id": "3c7ada03-694c-4e0d-ab7c-7d1b05fdc2ba",
    "presentation_title": "Q4 2024 Business Review",
    "slide_index": 2,
    "total_slides": 12,
    "slide_layout": "L25"
  },
  "section_context": {
    "section_id": "slide-2-section-content",
    "section_type": "content",
    "current_content": "<div style='padding: 20px;'><h2>Revenue Highlights</h2><ul><li>Good quarter</li><li>Revenue increased</li><li>Customers happy</li></ul></div>",
    "content_format": "html",
    "max_length": 1000
  },
  "regeneration_request": {
    "user_instruction": "Make this more specific with actual numbers and percentages. Add executive-level insights.",
    "tone": "professional",
    "preserve_structure": true,
    "preserve_formatting": true
  },
  "surrounding_context": {
    "slide_title": "Q4 Revenue Performance",
    "slide_subtitle": "Record-Breaking Quarter",
    "other_sections": [
      {
        "section_type": "chart",
        "description": "Bar chart showing quarterly revenue: Q1 $3.2M, Q2 $3.5M, Q3 $3.8M, Q4 $4.2M"
      }
    ]
  }
}
```

### Example Response

```json
{
  "success": true,
  "section_id": "slide-2-section-content",
  "section_type": "content",
  "updated_content": "<div style='padding: 20px;'>\n  <h2 style='color: #1f2937; font-size: 28px; margin-bottom: 16px;'>Revenue Highlights: Record Q4 Performance</h2>\n  <ul style='font-size: 18px; line-height: 1.8; color: #374151;'>\n    <li><strong>23% YoY Growth:</strong> Revenue reached $4.2M in Q4, up from $3.4M in Q4 2023</li>\n    <li><strong>Regional Expansion:</strong> APAC drove growth with +35%, followed by EMEA at +28%</li>\n    <li><strong>Customer Retention:</strong> NRR of 118% with zero churn among enterprise accounts</li>\n    <li><strong>Strategic Wins:</strong> TechCorp deal ($1.2M ARR) and FinanceHub partnership ($800K ARR)</li>\n  </ul>\n  <p style='margin-top: 20px; font-size: 16px; color: #6b7280; font-style: italic;'>Key Insight: Enterprise segment now represents 67% of total revenue, up from 52% in Q3, indicating successful market positioning.</p>\n</div>",
  "metadata": {
    "model_used": "claude-sonnet-4.5",
    "processing_time_ms": 1847,
    "tokens_used": 312,
    "content_length": 892,
    "changes_made": [
      "Added specific revenue numbers ($4.2M, $3.4M)",
      "Included YoY growth percentage (23%)",
      "Added regional breakdown (APAC +35%, EMEA +28%)",
      "Included NRR metric (118%) and churn data",
      "Added specific customer examples (TechCorp, FinanceHub)",
      "Added executive insight about enterprise segment shift",
      "Enhanced formatting with bold emphasis on key metrics",
      "Improved visual hierarchy with font sizes and colors"
    ],
    "preserved_elements": [
      "Original HTML structure (div > h2 + ul + p)",
      "20px padding from original style",
      "Professional tone throughout",
      "List format for key points"
    ]
  },
  "warnings": [],
  "alternatives": [
    {
      "variant": "more_concise",
      "content": "<div style='padding: 20px;'><h2>Q4 Revenue Highlights</h2><ul><li>$4.2M revenue (+23% YoY)</li><li>APAC +35%, EMEA +28%</li><li>118% NRR, 0% enterprise churn</li><li>Major wins: TechCorp ($1.2M), FinanceHub ($800K)</li></ul></div>",
      "description": "Condensed version for executive summary format"
    },
    {
      "variant": "with_visual_callouts",
      "content": "<div style='padding: 20px;'><div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 16px; border-radius: 8px; margin-bottom: 20px; text-align: center;'><div style='font-size: 48px; font-weight: bold;'>$4.2M</div><div style='font-size: 18px;'>Q4 Revenue (+23% YoY)</div></div><h2>Key Performance Drivers</h2><ul><li>Regional: APAC +35%, EMEA +28%</li><li>Retention: 118% NRR</li><li>Strategic Deals: $2M+ ARR from TechCorp & FinanceHub</li></ul></div>",
      "description": "Version with visual callout card for primary metric"
    }
  ]
}
```

---

## Questions for Director Team?

1. **Rate Limits**: What rate limits should we expect per user/API key?
2. **Authentication**: OAuth, API keys, or other auth method?
3. **Webhooks**: Should we support async processing for large sections?
4. **Versioning**: API versioning strategy (/v1/, /v2/)?
5. **Staging Environment**: URL and credentials for integration testing?
6. **SLA**: What uptime and response time SLA can we expect?

---

## Contact

**Layout Builder Team**
- Repository: https://github.com/Pramod-Potti-Krishnan/deck-builder-7.5
- Branch: `feature/world-class-editor-phase2`
- API Endpoint (Current Mock): `POST /api/presentations/{id}/regenerate-section`

**Next Steps**
1. Director team reviews this specification
2. Schedule API contract alignment meeting
3. Set up staging environment for integration
4. Begin Phase 3A implementation
5. Iterative testing and refinement

---

**End of Specification**
