# L02 Layout - Director Integration Guide

**Version**: v7.5.1 (Updated)
**Date**: November 16, 2025
**Last Updated**: November 16, 2025 (overflow behavior clarification)
**Purpose**: Guide for Director Agent to properly format L02 slide content

---

## Overview

Layout Builder v7.5.1 now supports **full HTML rendering** for L02 layout's `element_2` and `element_3` fields. This eliminates the blank screen issue previously encountered with Analytics Service content.

### What Changed

**Before (v7.5.0)**:
- `element_2` expected plain text only
- HTML content caused rendering failures (blank screens)

**After (v7.5.1)**:
- `element_2` and `element_3` support **both HTML and plain text**
- Auto-detection determines content type
- Proper rendering for both Analytics charts and plain text

---

## L02 Layout Specifications

### Grid Layout
```
┌────────────────────────────────────────────────────┐
│                  slide_title                       │
│                  element_1 (subtitle)              │
│                                                    │
│         element_3              │  element_2        │
│         (chart/diagram)        │  (observations)   │
│         1260px × 720px         │  540px × 720px    │
│         (21 grids wide)        │  (9 grids wide)   │
│                                                    │
│ footer                                             │
└────────────────────────────────────────────────────┘
```

### Field Dimensions
| Field | Width | Height | Grid Position |
|-------|-------|--------|---------------|
| `element_3` | 1260px | 720px | Rows 5-17, Cols 2-23 (21 grids) |
| `element_2` | 540px | 720px | Rows 5-17, Cols 23-32 (9 grids) |

### Container Overflow Behavior (v7.5.1+)

**element_3 (Chart/Diagram Container)**:
- `overflow: visible` - Charts can extend beyond container (tooltips, legends visible)
- `display: block` - Proper block-level rendering
- No default borders (only debug borders with 'B' key toggle)

**element_2 (Observations/Text Container)**:
- `overflow: auto` - Long text content scrolls vertically
- Scrollbar appears automatically when content exceeds 720px height
- Ideal for detailed observations and analysis text

**Why This Matters**:
- Charts with tooltips or legends that extend beyond bounds will render correctly
- Text content that's too long won't overflow the slide - it scrolls instead
- No permanent borders by default - Layout Builder focuses on content, not decoration

### Viewport Requirements (CRITICAL)

**v7.5.1 Update**: Layout Builder uses **fixed 1920×1080px base dimensions** in Reveal.js.

**Why This Matters**:
- Grid system calculations assume 1920×1080px base
- Element dimensions (1260px, 540px) are **fixed pixel values**
- Responsive scaling was **removed** to prevent content overflow
- All layouts (L02, L25, etc.) depend on this fixed viewport

**For Analytics Service**:
- Use exact dimensions: **1260×720px** for element_3, **540×720px** for element_2
- Set explicit `width` and `height` in inline styles
- Set `position: relative` on chart containers for proper rendering
- Use `maintainAspectRatio: false` for Chart.js charts

---

## Content Format Options

### Option 1: Plain Text (Backward Compatible)

Director can send plain text for `element_2`, and Layout Builder will apply default styling:

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Process Architecture",
    "element_1": "System Overview",
    "element_3": "<div>...diagram HTML...</div>",
    "element_2": "This architecture demonstrates the flow of data through our system. The process begins at the API gateway and proceeds through authentication, routing, and business logic layers.",
    "presentation_name": "Technical Presentation",
    "company_logo": "🏢"
  }
}
```

**Layout Builder applies**:
- Font size: 20px
- Color: #374151
- Line height: 1.6

---

### Option 2: HTML Content (Recommended for Analytics)

Director can send fully formatted HTML for rich presentations:

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Quarterly Revenue Growth",
    "element_1": "FY 2024 Performance",
    "element_3": "<div class='l02-chart-container' style='width: 1260px; height: 720px;'>\n  <canvas id='revenue-chart'></canvas>\n  <script>\n    // Chart.js initialization\n    const ctx = document.getElementById('revenue-chart').getContext('2d');\n    new Chart(ctx, {\n      type: 'line',\n      data: { /* chart data */ },\n      options: { /* chart options */ }\n    });\n  </script>\n</div>",
    "element_2": "<div style='padding: 32px; background: #f8f9fa; border-radius: 8px; height: 100%;'>\n  <h3 style='font-size: 20px; font-weight: 600; margin: 0 0 16px 0; color: #1f2937;'>Key Insights</h3>\n  <p style='font-size: 16px; line-height: 1.6; color: #374151; margin: 0;'>\n    The line chart illustrates quarterly revenue growth, with figures increasing from $125,000 in Q1 to $195,000 in Q4, representing a 56% year-over-year growth. This upward trend indicates robust business performance and market demand.\n  </p>\n</div>",
    "presentation_name": "Analytics Report",
    "company_logo": "🏢"
  }
}
```

**Layout Builder renders HTML as-is** without additional styling wrapper.

---

## Analytics Service Integration

### Analytics Service v3 Response Format

When Analytics Service returns L02-formatted content, Director should pass it through **without modification**:

```json
// Analytics Service Response
{
  "layout": "L02",
  "content": {
    "element_3": "<div class='l02-chart-container' style='width: 1260px; height: 720px;'>...Chart.js code...</div>",
    "element_2": "<div style='padding: 32px; background: #f8f9fa; height: 100%;'><h3>Key Insights</h3><p>...</p></div>"
  },
  "metadata": {
    "analytics_type": "revenue_over_time",
    "chart_type": "line"
  }
}
```

### Director's Role

Director should:
1. **Receive** Analytics Service response
2. **Add** required metadata fields (slide_title, element_1, presentation_name, company_logo)
3. **Pass through** element_3 and element_2 HTML without modification
4. **Send** to Layout Builder

```python
# Director content_transformer.py example
def transform_analytics_l02(analytics_response, slide, presentation):
    return {
        "layout": "L02",
        "content": {
            "slide_title": slide.generated_title or slide.title,
            "element_1": slide.generated_subtitle or "",
            "element_3": analytics_response["content"]["element_3"],  # Pass through HTML
            "element_2": analytics_response["content"]["element_2"],  # Pass through HTML
            "presentation_name": presentation.footer_text,
            "company_logo": ""
        }
    }
```

**Important**: Do NOT strip HTML tags from `element_2` or `element_3`. Layout Builder v7.5.1 handles HTML properly.

---

## HTML Content Guidelines

### element_3 (Chart/Diagram) Best Practices

```html
<div class="l02-chart-container" style="width: 1260px; height: 720px; position: relative;">
  <!-- Chart.js canvas -->
  <canvas id="chart-id"></canvas>

  <!-- Inline script for Chart.js initialization -->
  <script>
    (function() {
      const ctx = document.getElementById('chart-id').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Q1', 'Q2', 'Q3', 'Q4'],
          datasets: [{
            label: 'Revenue',
            data: [125000, 145000, 162000, 195000],
            borderColor: '#3b82f6',
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: true },
            title: { display: false }
          }
        }
      });
    })();
  </script>
</div>
```

**Key Points**:
- Set explicit dimensions: 1260px × 720px
- Use `position: relative` for absolute positioning within
- Use IIFE `(function() { ... })()` for script isolation
- Set `maintainAspectRatio: false` for Chart.js

---

### element_2 (Observations/Text) Best Practices

```html
<div style="padding: 32px; background: #f8f9fa; border-radius: 8px; height: 100%; box-sizing: border-box; overflow-y: auto;">
  <h3 style="font-size: 20px; font-weight: 600; margin: 0 0 16px 0; color: #1f2937;">
    Key Insights
  </h3>
  <p style="font-size: 16px; line-height: 1.6; color: #374151; margin: 0 0 12px 0;">
    First paragraph with observations...
  </p>
  <p style="font-size: 16px; line-height: 1.6; color: #374151; margin: 0;">
    Second paragraph with additional insights...
  </p>
</div>
```

**Key Points**:
- Container dimensions: 540px × 720px (grid handles this)
- Use `height: 100%` to fill available space
- `overflow-y: auto` for scrolling long content
- Consistent typography: 16-20px font size
- Professional colors: #1f2937 (headings), #374151 (body text)
- Light background: #f8f9fa for contrast

---

## Common Patterns

### Pattern 1: Analytics Chart + Observations

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Market Share Analysis",
    "element_1": "Q4 2024 Results",
    "element_3": "<!-- Chart.js pie chart HTML -->",
    "element_2": "<div style='padding: 32px; background: #f8f9fa; height: 100%;'>\n  <h3 style='margin: 0 0 16px 0; font-size: 20px; color: #1f2937;'>Market Position</h3>\n  <p style='font-size: 16px; line-height: 1.6; color: #374151;'>Our market share has grown to 28% in Q4, representing a 5% increase from the previous quarter. This growth positions us as the second-largest player in the industry.</p>\n</div>",
    "presentation_name": "Strategic Review",
    "company_logo": "🏢"
  }
}
```

### Pattern 2: Diagram + Explanation

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "System Architecture",
    "element_1": "Cloud Infrastructure Overview",
    "element_3": "<div><!-- Mermaid or SVG diagram HTML --></div>",
    "element_2": "The architecture utilizes a microservices approach with API Gateway, Service Mesh, and distributed databases. Each service is independently deployable and scalable, ensuring system resilience and flexibility.",
    "presentation_name": "Technical Docs",
    "company_logo": "⚙️"
  }
}
```

---

## Troubleshooting

### Issue: Blank Screen

**Cause**: Old Director versions stripping HTML from element_2

**Solution**: Ensure Director v3.4+ passes Analytics HTML through without modification

---

### Issue: Content Overflow

**Cause**: element_2 HTML uses fixed width > 540px

**Solution**:
```html
<!-- Bad: Fixed width -->
<div style="width: 600px; ...">

<!-- Good: Relative width -->
<div style="width: 100%; max-width: 540px; ...">
```

---

### Issue: Chart Not Rendering

**Cause**: Chart.js script not executing or conflicts

**Solution**:
1. Use IIFE: `(function() { /* chart code */ })()`
2. Ensure Chart.js library loaded in presentation-viewer.html
3. Use unique canvas IDs: `chart-${slide_id}`

---

## Testing Checklist

Director integration should verify:

- [ ] Analytics content with HTML renders without blank screens
- [ ] Plain text content still renders with proper styling
- [ ] element_3 dimensions match 1260px × 720px
- [ ] element_2 dimensions match 540px × 720px
- [ ] Chart.js charts initialize and render
- [ ] Observations text is readable and properly formatted
- [ ] Overflow content scrolls in element_2
- [ ] No HTML is stripped from Analytics responses

---

## Example Test Cases

### Test Case 1: Analytics Revenue Chart

```bash
curl -X POST https://layout-builder-url/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "L02 Analytics Test",
    "slides": [{
      "layout": "L02",
      "content": {
        "slide_title": "Revenue Trend",
        "element_1": "FY 2024",
        "element_3": "<div style=\"width: 1260px; height: 720px;\"><canvas id=\"test-chart\"></canvas><script>(function(){const ctx=document.getElementById(\"test-chart\").getContext(\"2d\");new Chart(ctx,{type:\"line\",data:{labels:[\"Q1\",\"Q2\",\"Q3\",\"Q4\"],datasets:[{label:\"Revenue\",data:[100,120,140,180],borderColor:\"#3b82f6\"}]},options:{responsive:true,maintainAspectRatio:false}});})();</script></div>",
        "element_2": "<div style=\"padding: 32px; background: #f8f9fa; height: 100%;\"><h3>Key Insights</h3><p>Revenue increased 80% year-over-year.</p></div>",
        "presentation_name": "Test",
        "company_logo": "🏢"
      }
    }]
  }'
```

**Expected Result**: Chart renders on left, observations on right, no blank screen.

---

### Test Case 2: Plain Text (Backward Compatibility)

```bash
curl -X POST https://layout-builder-url/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "L02 Plain Text Test",
    "slides": [{
      "layout": "L02",
      "content": {
        "slide_title": "Process Flow",
        "element_1": "System Workflow",
        "element_3": "<div>Diagram placeholder</div>",
        "element_2": "This diagram shows the complete workflow from user request to data processing and response generation.",
        "presentation_name": "Test",
        "company_logo": "⚙️"
      }
    }]
  }'
```

**Expected Result**: Diagram on left, styled text on right.

---

## Summary

**Director should**:
✅ Pass through Analytics HTML for element_2 and element_3 without modification
✅ Add required metadata fields (slide_title, element_1, etc.)
✅ Respect dimensions: 1260×720px (element_3), 540×720px (element_2)
✅ Trust Layout Builder v7.5.1 to handle HTML rendering

**Director should NOT**:
❌ Strip HTML tags from Analytics content
❌ Modify styling in element_2 or element_3
❌ Wrap HTML content in additional containers
❌ Convert HTML to plain text

---

**End of Guide**

For questions or issues, refer to:
- Layout Specifications: `LAYOUT_SPECIFICATIONS.md`
- L02 Renderer Source: `src/renderers/L02.js`
- Analytics Integration Diagnosis: `L02_INTEGRATION_ISSUE_DIAGNOSIS.md`
