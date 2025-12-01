# Analytics Service Requirements for Layout Builder v7.5

This document specifies the API requirements for Analytics Service to integrate with Layout Builder's chart insertion features.

## Overview

Layout Builder needs Analytics Service to provide:
1. **Chart HTML/JavaScript** for insertion via `insertChart` API
2. **Multiple chart types** (~15 types as supported by Analytics Service)
3. **Insight text** alongside visualizations
4. **Responsive, theme-aligned charts**

---

## API 1: Generate Chart

### Purpose
Generate a complete, renderable chart for insertion into a slide.

### Endpoint Suggestion
```
POST /api/analytics/generate-chart
```

### Request Format
```typescript
{
  presentationId: string,
  slideIndex: number,
  chartSpec: {
    type: ChartType,           // See supported types below
    data: ChartData,           // Data structure varies by type
    title?: string,            // Chart title
    subtitle?: string          // Chart subtitle
  },
  dimensions: {
    width: number,             // Pixels (e.g., 800)
    height: number,            // Pixels (e.g., 500)
    responsive: boolean        // Scale with container
  },
  theme: {
    primaryColor: string,      // Main chart color
    secondaryColor: string,    // Secondary series color
    backgroundColor: string,   // Chart background
    textColor: string,         // Labels, titles
    fontFamily: string,        // Font stack
    colorPalette: string[],    // Array of colors for series
    gridColor?: string,        // Grid lines
    borderRadius?: number      // Chart container radius
  },
  options?: {
    showLegend: boolean,       // Show legend
    legendPosition: 'top' | 'bottom' | 'left' | 'right',
    showValues: boolean,       // Show data labels
    showGrid: boolean,         // Show grid lines
    animation: boolean,        // Enable animations
    interactive: boolean       // Enable tooltips/hover
  }
}
```

### Supported Chart Types

| Type | Description | Use Case |
|------|-------------|----------|
| `bar` | Vertical bar chart | Comparing categories |
| `horizontalBar` | Horizontal bar chart | Long category names |
| `line` | Line chart | Trends over time |
| `area` | Filled area chart | Volume/magnitude trends |
| `pie` | Pie chart | Part-to-whole (< 6 items) |
| `donut` | Donut chart | Part-to-whole with center text |
| `scatter` | Scatter plot | Correlation analysis |
| `bubble` | Bubble chart | 3-variable comparison |
| `radar` | Radar/spider chart | Multi-dimensional comparison |
| `polarArea` | Polar area chart | Cyclical data |
| `treemap` | Treemap | Hierarchical proportions |
| `heatmap` | Heatmap/matrix | Two-dimensional patterns |
| `waterfall` | Waterfall chart | Sequential changes |
| `funnel` | Funnel chart | Conversion/pipeline |
| `gauge` | Gauge/meter | Single KPI |

### Data Structures by Chart Type

#### Bar, Line, Area Charts
```typescript
{
  labels: string[],            // X-axis labels
  datasets: Array<{
    label: string,             // Series name
    data: number[],            // Values
    color?: string             // Override series color
  }>
}
```

#### Pie, Donut Charts
```typescript
{
  labels: string[],            // Segment labels
  values: number[],            // Segment values
  colors?: string[]            // Segment colors
}
```

#### Scatter, Bubble Charts
```typescript
{
  datasets: Array<{
    label: string,
    data: Array<{
      x: number,
      y: number,
      r?: number               // Bubble radius (bubble chart only)
    }>
  }>
}
```

#### Treemap
```typescript
{
  data: Array<{
    name: string,
    value: number,
    children?: TreemapItem[]   // Nested items
  }>
}
```

#### Heatmap
```typescript
{
  xLabels: string[],
  yLabels: string[],
  values: number[][]           // 2D matrix [row][col]
}
```

### Response Format
```typescript
{
  success: boolean,
  chartHtml: string,           // Complete HTML with embedded JS
  chartId: string,             // Unique chart ID
  chartType: string,           // Confirmed chart type
  dimensions: {
    width: number,
    height: number
  },
  insights?: string[],         // AI-generated insights about data
  error?: string
}
```

---

## API 2: Generate Chart with Insights

### Purpose
Generate chart plus AI analysis of the data.

### Endpoint Suggestion
```
POST /api/analytics/generate-chart-with-insights
```

### Additional Request Fields
```typescript
{
  // ... same as generate-chart
  insightOptions: {
    count: number,             // Number of insights (1-5)
    type: 'summary' | 'trends' | 'anomalies' | 'recommendations',
    format: 'bullets' | 'paragraph'
  }
}
```

### Additional Response Fields
```typescript
{
  // ... same as generate-chart
  insights: {
    summary: string,           // One-line summary
    points: string[],          // Bullet points
    trend?: 'up' | 'down' | 'stable',
    keyMetric?: {
      label: string,
      value: string,
      change?: string          // e.g., '+15%'
    }
  }
}
```

---

## HTML Output Requirements

### Chart HTML Structure
```html
<div id="chart-{chartId}" class="analytics-chart"
     style="width: 100%; height: 100%; position: relative;">

  <!-- Chart Container -->
  <canvas id="canvas-{chartId}"></canvas>

  <!-- Or for complex charts like treemap/heatmap -->
  <div id="svg-container-{chartId}"></div>

  <!-- Embedded JavaScript -->
  <script>
    (function() {
      // Self-contained chart initialization
      // No global namespace pollution
      const chartConfig = { /* Chart.js config */ };
      const chart = new Chart(
        document.getElementById('canvas-{chartId}'),
        chartConfig
      );
    })();
  </script>
</div>
```

### Requirements
1. **Self-contained** - All JS in IIFE, no global variables
2. **Unique IDs** - Use chartId in all element IDs
3. **No external dependencies** - Chart.js already loaded in Layout Builder
4. **Responsive** - Use `responsive: true, maintainAspectRatio: false`
5. **Theme-aligned** - Apply provided colors and fonts
6. **Overflow safe** - No elements extending outside container

### Chart.js Plugins Available in Layout Builder
- `chartjs-chart-treemap`
- `chartjs-chart-matrix` (heatmap)
- `chartjs-chart-sankey`
- `chartjs-plugin-datalabels`
- ApexCharts (alternative for complex charts)
- D3.js (for custom visualizations)

---

## API 3: Update Chart Data

### Purpose
Update an existing chart's data without re-rendering.

### Endpoint Suggestion
```
PUT /api/analytics/update-chart/{chartId}
```

### Request Format
```typescript
{
  chartId: string,
  newData: ChartData,          // Same structure as original
  animate: boolean             // Animate transition
}
```

### Response Format
```typescript
{
  success: boolean,
  updateScript: string,        // JS to execute for update
  error?: string
}
```

### Update Script Example
```javascript
// Returned updateScript
(function() {
  const chart = Chart.getChart('canvas-{chartId}');
  if (chart) {
    chart.data = {newDataObject};
    chart.update('active');
  }
})();
```

---

## Layout Builder Integration

### How Layout Builder Will Use These APIs

1. **insertChart** postMessage handler:
   ```javascript
   // Frontend sends:
   {
     action: 'insertChart',
     params: {
       slideIndex: 0,
       position: { gridRow: '4/15', gridColumn: '3/30' },
       chartHtml: '...',     // From Analytics Service
       draggable: true
     }
   }
   ```

2. **Chart positioning**:
   - Layout Builder handles grid positioning (32×18 grid)
   - Analytics Service only provides chart content
   - Container sizing handled by Layout Builder

3. **Chart interactivity**:
   - Tooltips and hover effects work within iframe
   - Click events can bubble to Layout Builder if needed

### Dimension Recommendations

| Slide Area | Recommended Size | Grid Position |
|------------|-----------------|---------------|
| Full width | 1800×600 | rows 4-14, cols 2-31 |
| Half width | 840×500 | rows 4-13, cols 2-16 or 17-31 |
| Quarter | 400×400 | rows 4-10, cols 2-9 |

---

## Theme Integration

### Color Palette Generation

Analytics Service should generate a color palette from the provided theme colors:

```typescript
function generatePalette(primary: string, secondary: string): string[] {
  return [
    primary,           // First series
    secondary,         // Second series
    lighten(primary, 20),
    lighten(secondary, 20),
    darken(primary, 20),
    darken(secondary, 20),
    // ... additional colors
  ];
}
```

### Font Consistency

Use the provided `fontFamily` for all text:
- Chart title
- Axis labels
- Legend labels
- Data labels
- Tooltip text

---

## Performance Considerations

### Response Time Expectations
| Chart Type | Expected | Max |
|------------|----------|-----|
| Bar, Line, Pie | < 1s | 3s |
| Treemap, Heatmap | < 2s | 5s |
| With insights | < 3s | 8s |

### Chart Optimization
1. Limit data points to 100 for line/scatter charts
2. Aggregate data for large datasets
3. Use sampling for 1000+ points
4. Lazy-load animations

---

## Error Handling

### Error Codes
| Code | Meaning |
|------|---------|
| `INVALID_CHART_TYPE` | Unsupported chart type |
| `INVALID_DATA` | Data structure doesn't match type |
| `DATA_TOO_LARGE` | Dataset exceeds limits |
| `RENDER_FAILED` | Chart rendering failed |
| `INSIGHT_FAILED` | Insight generation failed |

### Fallback Behavior
If chart generation fails, return a placeholder:
```html
<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: #f3f4f6; border-radius: 8px;">
  <span style="color: #6b7280; font-size: 14px;">Chart unavailable</span>
</div>
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial specification |

---

## Contact

For questions about these requirements, contact the Layout Builder team.
