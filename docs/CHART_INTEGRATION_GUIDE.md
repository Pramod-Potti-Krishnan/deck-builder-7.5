# Chart Integration Guide for Layout Service

> **Purpose:** Complete reference for integrating chart components into slides/templates.
> **Last Updated:** 2025-12-28
> **Applicable To:** C3-chart, V2-chart-text, L02, and any future chart-enabled templates

---

## Table of Contents
1. [Overview](#overview)
2. [Required CDN Scripts](#required-cdn-scripts)
3. [Chart HTML Structure](#chart-html-structure)
4. [Script Execution Order](#script-execution-order)
5. [Content Object Structure](#content-object-structure)
6. [Template Setup Requirements](#template-setup-requirements)
7. [ElementManager Integration](#elementmanager-integration)
8. [Edit Button Setup](#edit-button-setup)
9. [Common Issues & Fixes](#common-issues--fixes)
10. [Debugging Checklist](#debugging-checklist)

---

## Overview

Charts in the Layout Service come from the **Analytics Service** as pre-rendered HTML (`chart_html`). This HTML contains:
- A `<canvas>` element for Chart.js
- An edit button (✏️) for the spreadsheet editor
- Multiple `<script>` tags that must execute in order

**Key Insight:** When HTML is inserted via `innerHTML`, embedded `<script>` tags do NOT execute automatically (browser security feature). The Layout Service must manually re-execute these scripts.

---

## Required CDN Scripts

These scripts must be available globally (loaded in the HTML head or before chart rendering):

### 1. Chart.js (Required)
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```
- **Purpose:** Core charting library
- **Must be loaded:** Before any chart initialization script runs

### 2. Chart.js Plugins (Optional, based on chart type)
```html
<!-- For datalabels on charts -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>

<!-- For treemap charts -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-chart-treemap@2"></script>
```

### 3. Reveal.js (If using presentation mode)
```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4/dist/reveal.js"></script>
```
- **Purpose:** Charts integrate with Reveal.js slide events
- **Used for:** Re-initializing charts on slide change for animation replay

### Where to Load These
In `presentation-viewer.html` or equivalent viewer page:
```html
<head>
  <!-- Load Chart.js BEFORE any slides render -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
```

---

## Chart HTML Structure

The Analytics Service sends chart HTML with this structure:

```html
<div class="l02-chart-container" style="width: 1260px; height: 720px; position: relative; background: white; padding: 20px; box-sizing: border-box;">

  <!-- 1. CANVAS: Where Chart.js renders -->
  <canvas id="chart-slide-X"></canvas>

  <!-- 2. EDIT BUTTON: Opens spreadsheet editor -->
  <button class="chart-edit-btn"
          onclick="openChartEditor_chart_slide_X()"
          style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.6); color: white; border: none; padding: 8px; width: 36px; height: 36px; border-radius: 50%; cursor: pointer; font-size: 16px; z-index: 100;">
    ✏️
  </button>

  <!-- 3. SCRIPT 1: Chart Initialization -->
  <script>
    (function() {
      function initChart() {
        const ctx = document.getElementById('chart-slide-X').getContext('2d');
        const chart = new Chart(ctx, { /* config */ });

        // CRITICAL: Store reference for editor
        window.chartInstances = window.chartInstances || {};
        window.chartInstances['chart-slide-X'] = chart;
      }

      // Reveal.js integration
      if (typeof Reveal !== 'undefined') {
        Reveal.on('ready', initChart);
        Reveal.on('slidechanged', function(event) {
          if (event.currentSlide.querySelector('#chart-slide-X')) {
            initChart(); // Re-init for animation
          }
        });
      } else {
        initChart();
      }
    })();
  </script>

  <!-- 4. SCRIPT 2: External Editor Library (LOADS ASYNC) -->
  <script src="https://analytics-v30-production.up.railway.app/static/js/chart-spreadsheet-editor.js"></script>

  <!-- 5. SCRIPT 3: Editor Function Definitions -->
  <script>
    (function() {
      window.openChartEditor_chart_slide_X = function() {
        const chart = window.chartInstances?.['chart-slide-X'];
        if (!chart) {
          alert('Chart not ready. Please wait and try again.');
          return;
        }
        // Opens Excel-like editor modal
        openChartEditor('chart-slide-X', 'bar', extractedData, callbacks);
      };
    })();
  </script>

</div>
```

---

## Script Execution Order

**CRITICAL:** Scripts must execute in this exact order:

| Order | Script | Purpose | Dependencies |
|-------|--------|---------|--------------|
| 1 | Chart.js CDN | Core library | None (global) |
| 2 | Chart initialization | Creates chart instance | Chart.js |
| 3 | Editor library (external) | Provides `openChartEditor()` | None |
| 4 | Editor function definitions | Creates `openChartEditor_chart_slide_X()` | Editor library |

**Why Order Matters:**
- Script 4 calls `openChartEditor()` which is defined in Script 3
- If Script 4 runs before Script 3 finishes loading → `openChartEditor is undefined`
- External scripts (`<script src="...">`) load **asynchronously**

---

## Content Object Structure

### From Analytics Service

```javascript
// For C3-chart (full-width chart)
{
  "chart_html": "<div class='l02-chart-container'>...</div>",
  "element_3": "<div class='l02-chart-container'>...</div>"  // Alias
}

// For V2-chart-text (chart + text split)
{
  "chart_html": "<div class='l02-chart-container'>...</div>",
  "element_3": "<div class='l02-chart-container'>...</div>",  // Alias
  "body": "<p>Insights text...</p>",
  "element_2": "<p>Insights text...</p>"  // Alias
}

// For L02 (diagram/chart + text)
{
  "element_3": "<div class='l02-chart-container'>...</div>",  // Chart/diagram
  "element_2": "<p>Text content...</p>"
}
```

### Content Field Priority (in getChartContent)

```javascript
// Layout Service checks these fields in order:
content.chart_html      // Primary - API documented field
content.analytics_html  // Alternative field name
content.element_3       // V2/C3 Analytics Service alias
content.element_4       // L-series element mapping
```

---

## Template Setup Requirements

### For a Template to Support Charts

#### 1. Template Registry Definition
In `src/templates/template-registry.js`:

```javascript
'YOUR-TEMPLATE': {
  id: 'YOUR-TEMPLATE',
  name: 'Your Template Name',
  renderer: 'renderYourTemplate',
  slots: {
    chart_slot: {
      gridRow: '4/18',
      gridColumn: '2/20',
      tag: 'chart',           // CRITICAL: Must be 'chart'
      accepts: ['chart'],     // What content types are allowed
      description: 'Chart area'
    }
  }
}
```

#### 2. Renderer Function
In `src/renderers/your-template.js`:

```javascript
function renderYourTemplate(content, slide = {}, slideIndex = 0) {
  // MUST output data-direct-elements="true" for DirectElementCreator to work
  return `
    <section data-layout="YOUR-TEMPLATE"
             data-template="YOUR-TEMPLATE"
             class="grid-container"
             data-slide-index="${slideIndex}"
             data-direct-elements="true">
    </section>
  `;
}
```

#### 3. Content Extraction Support
In `src/utils/direct-element-creator.js`, ensure `getChartContent()` handles your slot name:

```javascript
function getChartContent(slotName, content) {
  // Add your slot name if different from existing ones
  if (slotName === 'content' || slotName === 'content_left' || slotName === 'chart' || slotName === 'your_slot') {
    return content.chart_html || content.analytics_html || content.element_3 || content.element_4 || null;
  }
}
```

---

## ElementManager Integration

### How Charts Are Inserted

1. **DirectElementCreator** calls `createChart()`
2. `createChart()` extracts HTML via `getChartContent()`
3. `createChart()` calls `ElementManager.insertChart(slideIndex, config)`
4. `insertChart()` creates container, sets innerHTML, executes scripts

### insertChart() Key Code

```javascript
// In src/utils/element-manager.js

function insertChart(slideIndex, config) {
  // ... container setup ...

  if (config.chartHtml) {
    // Set HTML content
    contentDiv.innerHTML = config.chartHtml;

    // v7.5.4: Execute scripts sequentially
    // External scripts wait for load before next script runs
    executeScriptsSequentially(contentDiv).catch(err => {
      console.error('[ElementManager] Script execution error:', err);
    });
  }
}
```

### Sequential Script Execution (v7.5.4 Fix)

```javascript
async function executeScriptsSequentially(contentDiv) {
  const scripts = Array.from(contentDiv.querySelectorAll('script'));

  for (const oldScript of scripts) {
    const newScript = document.createElement('script');

    // Copy all attributes
    Array.from(oldScript.attributes).forEach(attr => {
      newScript.setAttribute(attr.name, attr.value);
    });

    if (oldScript.src) {
      // EXTERNAL: Wait for load before continuing
      await new Promise((resolve) => {
        newScript.onload = resolve;
        newScript.onerror = resolve; // Continue even on error
        oldScript.parentNode.replaceChild(newScript, oldScript);
      });
    } else {
      // INLINE: Execute immediately
      newScript.textContent = oldScript.textContent;
      oldScript.parentNode.replaceChild(newScript, oldScript);
    }
  }
}
```

**Why This Matters:**
- `innerHTML` does NOT execute scripts (browser security)
- Creating new `<script>` elements triggers execution
- External scripts must finish loading before dependent scripts run

---

## Edit Button Setup

### Button HTML (from Analytics Service)

```html
<button class="chart-edit-btn"
        onclick="openChartEditor_chart_slide_X()"
        style="position: absolute; top: 10px; left: 10px;
               background: rgba(0,0,0,0.6); color: white;
               border: none; padding: 8px; width: 36px; height: 36px;
               border-radius: 50%; cursor: pointer; font-size: 16px; z-index: 100;
               transition: all 0.3s ease;"
        onmouseover="this.style.width='80px'; this.style.borderRadius='20px'; this.innerHTML='✏️ Edit';"
        onmouseout="this.style.width='36px'; this.style.borderRadius='50%'; this.innerHTML='✏️';">
  ✏️
</button>
```

### Required Window Globals

For the edit button to work, these must exist:

```javascript
// Created by Script 1 (chart initialization)
window.chartInstances = {};
window.chartInstances['chart-slide-X'] = chartInstance;

// Created by Script 3 (editor function definitions)
window.openChartEditor_chart_slide_X = function() { ... };

// Provided by Script 2 (external library)
window.openChartEditor = function(chartId, chartType, data, callbacks) { ... };
```

---

## Common Issues & Fixes

### Issue 1: Chart Shows Placeholder Instead of Content

**Symptoms:** Gray placeholder with "Generate chart..." text

**Causes:**
1. `chart_html` not in content object
2. `getChartContent()` not checking correct field name
3. Content object not passed to DirectElementCreator

**Fix:**
- Verify content object has `chart_html` field
- Check `getChartContent()` includes your content field name
- Add console logging to trace content flow

### Issue 2: Edit Button Does Nothing

**Symptoms:** Click ✏️ button, nothing happens, no errors

**Cause:** `openChartEditor_chart_slide_X()` is undefined because external library hasn't loaded

**Fix:** Ensure sequential script execution (v7.5.4):
- External scripts must wait for `onload` before next script
- Check console for: `[ElementManager] External script loaded: chart-spreadsheet-editor.js`

### Issue 3: Edit Button Shows "Chart not ready"

**Symptoms:** Alert says "Chart not ready. Please wait and try again."

**Cause:** Chart initialization script hasn't run, `window.chartInstances` is empty

**Fix:**
- Ensure Chart.js CDN is loaded globally
- Check Script 1 (initialization) executed
- Verify `window.chartInstances['chart-slide-X']` exists in console

### Issue 4: Chart Doesn't Animate on Slide Change

**Symptoms:** Chart appears but no animation when navigating to slide

**Cause:** Reveal.js integration not working

**Fix:**
- Ensure Reveal.js is loaded if using presentation mode
- Chart initialization script should listen for `slidechanged` event

---

## Debugging Checklist

### Before Chart Renders

- [ ] Chart.js CDN loaded in page `<head>`?
- [ ] Template has `data-direct-elements="true"` attribute?
- [ ] Slot definition has `tag: 'chart'`?
- [ ] `getChartContent()` checks your slot name?

### After Chart Should Render

- [ ] Content object has `chart_html` field? (console.log it)
- [ ] `insertChart()` called? (check console logs)
- [ ] Container div exists in DOM?
- [ ] Canvas element has ID matching script references?

### Edit Button Not Working

- [ ] Console shows: `[ElementManager] External script loaded: chart-spreadsheet-editor.js`?
- [ ] Console shows: `[ElementManager] Scripts executed sequentially (X inline, 1 external)`?
- [ ] `window.chartInstances['chart-slide-X']` exists? (check in console)
- [ ] `window.openChartEditor_chart_slide_X` is a function? (check in console)
- [ ] `window.openChartEditor` is a function? (from external library)

### Console Commands for Debugging

```javascript
// Check chart instances
console.log(window.chartInstances);

// Check editor function exists
console.log(typeof window.openChartEditor_chart_slide_0);

// Check external library loaded
console.log(typeof window.openChartEditor);

// Manually trigger editor (replace X with slide number)
window.openChartEditor_chart_slide_X();
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v7.5.3 | 2025-12-27 | Added script re-execution after innerHTML |
| v7.5.4 | 2025-12-28 | Sequential script execution for external scripts |
| v7.5.4+ | 2025-12-28 | Added element_3 alias support |

---

## Related Files

| File | Purpose |
|------|---------|
| `src/utils/element-manager.js` | `insertChart()`, `executeScriptsSequentially()` |
| `src/utils/direct-element-creator.js` | `createChart()`, `getChartContent()` |
| `src/templates/template-registry.js` | Template slot definitions |
| `src/renderers/split-templates.js` | V1-V4, S1-S4 renderers |
| `src/renderers/content-templates.js` | C1-C6 renderers |
| `presentation-viewer.html` | CDN script loading |

---

## Contact

- **Analytics Service:** https://analytics-v30-production.up.railway.app
- **Layout Service Branch:** feature/frontend-templates
