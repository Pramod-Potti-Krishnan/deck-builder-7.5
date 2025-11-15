# Analytics Microservice Integration Guide
**Layout Builder v7.5-main**
*Version: 1.0 - Date: 2025-01-14*

---

## Table of Contents

1. [Overview](#overview)
2. [Supported Layouts for Charts](#supported-layouts-for-charts)
3. [Chart HTML Format](#chart-html-format)
4. [Field Mapping](#field-mapping)
5. [ApexCharts Integration](#apexcharts-integration)
6. [Complete Examples](#complete-examples)
7. [JavaScript Escaping Details](#javascript-escaping-details)
8. [Troubleshooting](#troubleshooting)
9. [Testing](#testing)

---

## Overview

The Layout Builder v7.5-main now **fully supports dynamic chart HTML** from the Analytics Microservice, including ApexCharts with embedded JavaScript, template literals, and complex configurations.

### Key Features

✅ **Full JavaScript Support**: `<script>` tags with template literals (`${}` expressions) work correctly
✅ **Pass-Through Architecture**: Chart HTML is rendered as-is, no modifications
✅ **Special Character Handling**: Backslashes, HTML tags, Unicode characters properly escaped
✅ **Multiple Charts**: Support for multiple charts on same slide (L03 layout)
✅ **Backward Compatible**: No impact on existing Text Service integration

### How It Works

1. **Analytics Microservice** generates complete chart HTML (including `<script>` tags)
2. **Layout Builder** receives HTML in content fields via POST `/api/presentations`
3. **JavaScript Escaping** (server.py:199-216) properly handles template literals
4. **Browser Rendering** executes chart JavaScript and renders visualizations

---

## Supported Layouts for Charts

The Analytics Microservice should use these **3 chart-optimized layouts**:

### L01: Centered Chart or Diagram
- **Best For**: Single large chart with description
- **Chart Area**: 1800×600px (centered)
- **Chart Field**: `element_4`
- **Description Field**: `element_3` (below chart)

### L02: Diagram Left with Text Right
- **Best For**: Chart with detailed explanation
- **Chart Area**: 1260×720px (left side, 2/3 width)
- **Chart Field**: `element_3`
- **Text Field**: `element_2` (right side, 1/3 width)

### L03: Two Charts Side-by-Side
- **Best For**: Comparison charts
- **Chart Areas**: Two 840×540px charts
- **Chart Fields**: `element_4` (left), `element_2` (right)
- **Description Fields**: `element_3` (left), `element_5` (right)

**Not Recommended**:
- **L25**: Use for text content, not charts (Text Service owns `rich_content`)
- **L29**: Use for title/hero slides only

---

## Chart HTML Format

### Basic Structure

All chart HTML follows this pattern:

```html
<div id="chart-{unique-id}" style="width: 100%; height: 100%;"></div>
<script>
(function() {
  // Your chart configuration
  var options = {
    chart: { type: 'line', height: '100%' },
    series: [{ name: 'Sales', data: [30, 40, 35, 50] }],
    xaxis: { categories: [`Q1`, `Q2`, `Q3`, `Q4`] }
  };

  // Render chart
  var chartEl = document.getElementById('chart-{unique-id}');
  // ... chart rendering logic ...
})();
</script>
```

### Critical Requirements

✅ **Use IIFEs** (Immediately Invoked Function Expressions): Wrap code in `(function() { ... })()`
✅ **Unique IDs**: Each chart needs unique container ID (`chart-{uuid}` or `chart-{slide-id}`)
✅ **Inline Styles**: Use `style="width: 100%; height: 100%;"` on container
✅ **Template Literals**: Safe to use backticks and `${}` expressions
✅ **Escape Special Chars**: Layout Builder handles this automatically

❌ **Avoid**:
- External script dependencies without checking availability
- Global variable pollution (use IIFEs)
- Hardcoded dimensions (use percentages)

---

## Field Mapping

### L01: Centered Chart

```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Chart title",
    "element_1": "Subtitle/context",
    "element_4": "<div id='chart-id'>...</div>\n<script>...</script>",
    "element_3": "Description below chart",
    "presentation_name": "Presentation Name",
    "company_logo": "Logo HTML or emoji"
  }
}
```

### L02: Chart + Explanation

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Chart title",
    "element_1": "Subtitle",
    "element_3": "<div id='chart-id'>...</div>\n<script>...</script>",
    "element_2": "Detailed explanation text (right side)",
    "presentation_name": "Presentation Name",
    "company_logo": "Logo HTML or emoji"
  }
}
```

### L03: Two Charts

```json
{
  "layout": "L03",
  "content": {
    "slide_title": "Comparison title",
    "element_1": "Subtitle",
    "element_4": "<div id='chart-left'>...</div>\n<script>...</script>",
    "element_2": "<div id='chart-right'>...</div>\n<script>...</script>",
    "element_3": "Left chart description",
    "element_5": "Right chart description",
    "presentation_name": "Presentation Name",
    "company_logo": "Logo HTML or emoji"
  }
}
```

---

## ApexCharts Integration

### Full ApexCharts Example (L01)

```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Revenue Performance",
    "element_1": "Q1-Q4 2024 Revenue Trends",
    "element_4": "<div id='chart-revenue-2024' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  var options = {\n    chart: {\n      type: 'line',\n      height: '100%',\n      toolbar: { show: false },\n      animations: { enabled: true }\n    },\n    series: [{\n      name: 'Revenue',\n      data: [30, 40, 35, 50, 49, 60, 70, 91]\n    }],\n    xaxis: {\n      categories: [`Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`, `Jul`, `Aug`],\n      title: { text: 'Month' }\n    },\n    yaxis: {\n      title: { text: 'Revenue ($M)' },\n      labels: {\n        formatter: function(val) {\n          return `$${val}M`;\n        }\n      }\n    },\n    colors: ['#667eea'],\n    stroke: { curve: 'smooth', width: 3 },\n    markers: { size: 6 },\n    title: {\n      text: `Revenue Trend (${8} months)`,\n      align: 'left'\n    },\n    tooltip: {\n      y: {\n        formatter: function(val) {\n          return `$${val} Million`;\n        }\n      }\n    }\n  };\n  \n  var chart = new ApexCharts(document.querySelector('#chart-revenue-2024'), options);\n  chart.render();\n})();\n</script>",
    "element_3": "Revenue increased 203% from January to August, showing strong growth trajectory.",
    "presentation_name": "Q3 Business Review",
    "company_logo": "📊"
  }
}
```

### Template Literal Usage

**Safe patterns** (all work correctly):

```javascript
// Backtick strings
var label = `Revenue: $${value}M`;

// Template expressions
var title = `Sales Data (${months.length} periods)`;

// Array with template literals
var categories = [`Jan`, `Feb`, `Mar`, `Apr`];

// Formatters with template literals
formatter: function(val) {
  return `$${val}K`;
}

// Nested expressions
var summary = `Total: ${values.reduce((a, b) => a + b, 0)} items`;
```

---

## Complete Examples

### Example 1: Bar Chart (L01)

```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Regional Sales Performance",
    "element_1": "Top 5 regions by revenue",
    "element_4": "<div id='chart-bar-regions' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  var regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East'];\n  var revenue = [45, 30, 25, 15, 10];\n  \n  var options = {\n    chart: { type: 'bar', height: '100%', toolbar: { show: false } },\n    series: [{ name: 'Revenue ($M)', data: revenue }],\n    xaxis: { categories: regions },\n    yaxis: {\n      labels: {\n        formatter: val => `$${val}M`\n      }\n    },\n    colors: ['#3b82f6'],\n    plotOptions: {\n      bar: { borderRadius: 8, horizontal: false }\n    },\n    dataLabels: {\n      enabled: true,\n      formatter: val => `$${val}M`\n    },\n    title: { text: `Revenue by Region (${regions.length} markets)` }\n  };\n  \n  var chart = new ApexCharts(document.querySelector('#chart-bar-regions'), options);\n  chart.render();\n})();\n</script>",
    "element_3": "North America leads with $45M in revenue, representing 36% of global sales.",
    "presentation_name": "Regional Analysis",
    "company_logo": "🌍"
  }
}
```

### Example 2: Pie Chart with Special Characters (L02)

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Market Share Distribution",
    "element_1": "Competitive landscape analysis",
    "element_3": "<div id='chart-pie-market' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  // Test special characters\n  var dataPath = `C:\\\\Analytics\\\\Data\\\\2024`;\n  var htmlFragment = '<div>Market Data</div>';\n  \n  var marketData = {\n    'Our Company': 35,\n    'Competitor A': 25,\n    'Competitor B': 20,\n    'Others': 20\n  };\n  \n  var options = {\n    chart: { type: 'pie', height: '100%' },\n    series: Object.values(marketData),\n    labels: Object.keys(marketData).map(key => `${key}: ${marketData[key]}%`),\n    colors: ['#667eea', '#764ba2', '#f093fb', '#f5576c'],\n    legend: {\n      position: 'bottom',\n      formatter: function(seriesName) {\n        return seriesName;\n      }\n    },\n    title: { text: `Market Share (${Object.keys(marketData).length} players)` },\n    dataLabels: {\n      formatter: function(val) {\n        return `${val.toFixed(1)}%`;\n      }\n    }\n  };\n  \n  var chart = new ApexCharts(document.querySelector('#chart-pie-market'), options);\n  chart.render();\n})();\n</script>",
    "element_2": "We maintain market leadership with 35% share, ahead of Competitor A (25%) and Competitor B (20%). The remaining 20% is fragmented among smaller players. Our position has strengthened by 5 percentage points year-over-year.",
    "presentation_name": "Competitive Analysis",
    "company_logo": "📈"
  }
}
```

### Example 3: Comparison Charts (L03)

```json
{
  "layout": "L03",
  "content": {
    "slide_title": "Revenue vs Costs Analysis",
    "element_1": "Monthly financial performance comparison",
    "element_4": "<div id='chart-revenue-monthly' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  var months = [`Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`];\n  var revenue = [30, 40, 35, 50, 49, 60];\n  \n  var options = {\n    chart: { type: 'area', height: '100%', toolbar: { show: false } },\n    series: [{ name: 'Revenue', data: revenue }],\n    xaxis: { categories: months },\n    yaxis: { labels: { formatter: val => `$${val}K` } },\n    colors: ['#4facfe'],\n    fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.3 } },\n    stroke: { curve: 'smooth', width: 2 },\n    title: { text: 'Revenue Trend' }\n  };\n  \n  var chart = new ApexCharts(document.querySelector('#chart-revenue-monthly'), options);\n  chart.render();\n})();\n</script>",
    "element_2": "<div id='chart-costs-monthly' style='width: 100%; height: 100%;'></div>\n<script>\n(function() {\n  var months = [`Jan`, `Feb`, `Mar`, `Apr`, `May`, `Jun`];\n  var costs = [25, 28, 27, 32, 30, 35];\n  \n  var options = {\n    chart: { type: 'area', height: '100%', toolbar: { show: false } },\n    series: [{ name: 'Costs', data: costs }],\n    xaxis: { categories: months },\n    yaxis: { labels: { formatter: val => `$${val}K` } },\n    colors: ['#f5576c'],\n    fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.3 } },\n    stroke: { curve: 'smooth', width: 2 },\n    title: { text: 'Cost Trend' }\n  };\n  \n  var chart = new ApexCharts(document.querySelector('#chart-costs-monthly'), options);\n  chart.render();\n})();\n</script>",
    "element_3": "Revenue grew 100% from $30K (Jan) to $60K (Jun), showing strong upward momentum.",
    "element_5": "Costs increased 40% from $25K (Jan) to $35K (Jun), maintaining healthy profit margins.",
    "presentation_name": "Financial Dashboard",
    "company_logo": "💰"
  }
}
```

---

## JavaScript Escaping Details

### How Layout Builder Handles Chart HTML

**Server-Side Processing** (server.py:199-216):

```python
# 1. Serialize presentation data to JSON
presentation_json = json.dumps(presentation, ensure_ascii=False)

# 2. Escape for JavaScript context
presentation_json_safe = (
    presentation_json
    .replace('\\', '\\\\')           # Backslashes
    .replace('</', '<\\/')           # Prevent </script> injection
    .replace('\u2028', '\\u2028')    # Line separator
    .replace('\u2029', '\\u2029')    # Paragraph separator
)

# 3. Inject into HTML
html = html.replace(
    "const PRESENTATION_DATA = null;",
    f"const PRESENTATION_DATA = {presentation_json_safe};"
)
```

### What Gets Escaped

| Character/Pattern | Original | Escaped | Reason |
|-------------------|----------|---------|--------|
| Backslash | `\` | `\\` | Prevent escape sequence issues |
| Script close tag | `</` | `<\/` | Prevent premature script closing |
| Line separator | `\u2028` | `\\u2028` | Prevent JS parsing errors |
| Paragraph separator | `\u2029` | `\\u2029` | Prevent JS parsing errors |

### What Works Now

✅ **Template literals**: `` `Hello ${name}` ``
✅ **Complex expressions**: `` `Total: ${values.reduce((a,b) => a+b)}` ``
✅ **Backslashes**: `C:\\Users\\Data`
✅ **HTML in strings**: `'<div>Test</div>'`
✅ **Script tags in strings**: `'</script>'` (properly escaped as `<\/script>`)
✅ **Unicode characters**: All properly handled

---

## Troubleshooting

### Issue: Chart HTML is Empty in Browser

**Symptoms**:
- `element_4` shows HTML in JSON file
- `element_4` shows empty (`""` or `"\n\n"`) in browser PRESENTATION_DATA
- JavaScript errors in console

**Cause**: Old version of Layout Builder without JavaScript escaping fix

**Solution**:
1. Verify you're using Layout Builder v7.5-main with server.py lines 199-216 fix
2. Check that `ensure_ascii=False` is present
3. Verify escaping chain (backslash → script tag → Unicode)

---

### Issue: Template Literals Cause Syntax Errors

**Symptoms**:
- Browser console shows "Unexpected token" or "Illegal character"
- Charts don't render
- `${expression}` appears as literal text

**Cause**: Template literal expressions being interpreted incorrectly

**Solution**:
- Already fixed in v7.5-main server.py
- Verify JSON escaping is active
- Check browser DevTools → Console for specific error

---

### Issue: Multiple Charts on Same Slide Conflict

**Symptoms**:
- Only first chart renders
- Charts overwrite each other
- JavaScript errors about duplicate IDs

**Cause**: Non-unique chart container IDs

**Solution**:
```javascript
// ❌ Bad: Same ID
<div id="chart"></div>

// ✅ Good: Unique IDs
<div id="chart-{slide-id}-revenue"></div>
<div id="chart-{slide-id}-costs"></div>
```

---

### Issue: Chart Doesn't Render (No Errors)

**Symptoms**:
- No JavaScript errors
- Chart container exists but empty
- ApexCharts code appears to run

**Cause**: ApexCharts library not loaded or chart initialization issue

**Solution**:
1. Include ApexCharts CDN in your HTML:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
   ```
2. Verify chart initialization happens after DOM load
3. Check that container has dimensions (`width: 100%; height: 100%`)

---

## Testing

### Test Presentation Available

**File**: `test_analytics_apexcharts.json`
**Purpose**: Comprehensive test of JavaScript escaping with realistic ApexCharts HTML

**Create Test Presentation**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test_analytics_apexcharts.json
```

**Verify Success**:
1. ✅ Response includes presentation `id` and `url`
2. ✅ Open URL in browser: `http://localhost:8504/p/{id}`
3. ✅ Press F12 → Console → No JavaScript errors
4. ✅ Charts render correctly on slides
5. ✅ Template literals with `${}` work
6. ✅ Special characters (backslashes, HTML tags) preserved

### Manual Testing Checklist

- [ ] L01 chart renders with template literals
- [ ] L02 chart renders with special characters
- [ ] L03 dual charts both render independently
- [ ] No JavaScript console errors
- [ ] PRESENTATION_DATA in DevTools shows complete HTML
- [ ] Chart interactions work (if applicable)
- [ ] Existing Text Service presentations still work

---

## Best Practices

### 1. Always Use IIFEs
```javascript
// ✅ Good
<script>
(function() {
  var localVar = 'safe';
  // chart code
})();
</script>

// ❌ Bad (pollutes global scope)
<script>
var globalVar = 'unsafe';
// chart code
</script>
```

### 2. Generate Unique IDs
```javascript
// ✅ Good: Include slide ID or UUID
var chartId = `chart-${slideId}-revenue`;
var chartEl = document.getElementById(chartId);

// ❌ Bad: Hardcoded ID (conflicts on multi-chart slides)
var chartEl = document.getElementById('chart');
```

### 3. Use Relative Sizing
```css
/* ✅ Good */
style="width: 100%; height: 100%;"

/* ❌ Bad (breaks responsive layout) */
style="width: 1800px; height: 600px;"
```

### 4. Handle Missing Libraries Gracefully
```javascript
// ✅ Good: Check library availability
if (typeof ApexCharts !== 'undefined') {
  var chart = new ApexCharts(element, options);
  chart.render();
} else {
  console.warn('ApexCharts library not loaded');
  element.innerHTML = '<div>Chart placeholder</div>';
}
```

---

## Support

**Issues**: Report to Layout Builder team
**Documentation**: `/docs/API_DOCUMENTATION.md`
**Test Files**: `test_analytics_apexcharts.json`
**Version**: v7.5-main (JavaScript escaping enabled)

---

**Last Updated**: 2025-01-14
**Status**: Production-Ready ✅
