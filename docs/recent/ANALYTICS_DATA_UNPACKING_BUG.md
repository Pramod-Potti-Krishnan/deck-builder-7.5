# Analytics Service - Data Unpacking Bug Report

**Date**: November 19, 2025
**Service**: Analytics Microservice v3
**Severity**: P0 - Critical
**Affected Charts**: 3/13 (23%)
**Status**: ⚠️ Requires Analytics Team Fix

---

## Executive Summary

Three Analytics chart types (bar_grouped, area_stacked, bar_stacked) are failing to render due to incorrect data unpacking in the Analytics Service chart generation code. The API accepts data correctly (100% success), but the chart generation logic fails to extract nested datasets from the data structure.

**Impact**:
- Charts render completely blank or show only "Item 0" text
- Error messages like "Grouped bar chart requires 'datasets' in data"
- 23% of Analytics charts are broken

**Root Cause**: Chart generators expect flat data structure but receive nested array structure `[{datasets: [...], labels: [...]}]` and fail to unpack `data[0]`.

---

## Affected Chart Types

### 1. **bar_grouped** (Grouped Bar Chart)
**Error Message**:
```
"Grouped bar chart requires 'datasets' in data"
```

**Symptom**: Chart doesn't render, error displayed in UI

**Root Cause**: Code attempts `data.get('datasets')` which returns `undefined` because datasets is nested in `data[0]`

---

### 2. **area_stacked** (Stacked Area Chart)
**Symptom**: Renders blank with only "Item 0" text visible

**Root Cause**: Similar data unpacking issue - code doesn't extract `data[0]` before accessing `datasets` and `labels`

---

### 3. **bar_stacked** (Stacked Bar Chart)
**Symptom**: Renders blank with only "Item 0" text visible

**Root Cause**: Same pattern as area_stacked - missing `data[0]` unpacking

---

## Technical Analysis

### Data Structure Received by Chart Generators

**Actual Data Structure** (what Analytics receives):
```javascript
[
  {
    datasets: [
      {
        label: "Q1 Sales",
        data: [120, 190, 300, 500],
        backgroundColor: "#3b82f6"
      },
      {
        label: "Q2 Sales",
        data: [150, 220, 350, 600],
        backgroundColor: "#10b981"
      }
    ],
    labels: ["Jan", "Feb", "Mar", "Apr"]
  }
]
```

**Expected by Current Code** (what code assumes):
```javascript
{
  datasets: [...],
  labels: [...]
}
```

### Current Code Pattern (WRONG ❌)

```javascript
function generateGroupedBarChart(data) {
  // This returns undefined!
  const datasets = data.get('datasets');  // TypeError or undefined
  const labels = data.get('labels');       // TypeError or undefined

  if (!datasets) {
    throw new Error("Grouped bar chart requires 'datasets' in data");
  }

  return `
    <script>
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ${JSON.stringify(labels)},
          datasets: ${JSON.stringify(datasets)}
        },
        options: {...}
      });
    </script>
  `;
}
```

**Why It Fails**:
1. `data` is an array `[{...}]`, not an object
2. Arrays don't have `.get()` method (undefined)
3. Even with bracket notation `data['datasets']`, it fails because datasets is in `data[0]`
4. Result: `datasets` and `labels` are undefined
5. Chart.js receives empty data and renders blank

---

### Correct Code Pattern (RIGHT ✅)

```javascript
function generateGroupedBarChart(data) {
  // Unpack data from array wrapper
  const chartData = Array.isArray(data) ? data[0] : data;

  // Now extract datasets and labels from the correct object
  const datasets = chartData.datasets || [];
  const labels = chartData.labels || [];

  if (!datasets || datasets.length === 0) {
    throw new Error("Grouped bar chart requires 'datasets' in data");
  }

  return `
    <script>
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ${JSON.stringify(labels)},
          datasets: ${JSON.stringify(datasets)}
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'top'
            }
          },
          scales: {
            x: {
              stacked: false
            },
            y: {
              stacked: false,
              beginAtZero: true
            }
          }
        }
      });
    </script>
  `;
}
```

**Why It Works**:
1. Checks if data is array and unwraps: `data[0]`
2. Falls back to data if already unwrapped
3. Correctly extracts `datasets` and `labels` from unwrapped object
4. Provides default empty arrays if missing
5. Chart.js receives proper data structure

---

## Fix Implementation Guide

### Step 1: Locate Chart Generation Code

**Files to Update** (in Analytics Microservice v3):
```
analytics_microservice_v3/
├── src/
│   ├── chart_generators/
│   │   ├── bar_grouped.py (or .js/.ts)
│   │   ├── area_stacked.py (or .js/.ts)
│   │   └── bar_stacked.py (or .js/.ts)
```

### Step 2: Apply Data Unpacking Pattern

**For Each Affected Chart Generator**, add this pattern at the start:

```python
# Python example
def generate_chart_html(data: Union[List, Dict]) -> str:
    # Unpack data if wrapped in array
    if isinstance(data, list) and len(data) > 0:
        chart_data = data[0]
    else:
        chart_data = data

    # Extract datasets and labels
    datasets = chart_data.get('datasets', [])
    labels = chart_data.get('labels', [])

    # Validate required data
    if not datasets:
        raise ValueError("Chart requires 'datasets' in data")

    # Continue with chart generation...
```

```javascript
// JavaScript/TypeScript example
function generateChartHTML(data) {
  // Unpack data if wrapped in array
  const chartData = Array.isArray(data) ? data[0] : data;

  // Extract datasets and labels
  const datasets = chartData.datasets || [];
  const labels = chartData.labels || [];

  // Validate required data
  if (!datasets || datasets.length === 0) {
    throw new Error("Chart requires 'datasets' in data");
  }

  // Continue with chart generation...
}
```

### Step 3: Update Each Chart Type

#### **bar_grouped (Grouped Bar Chart)**

**Current Code Location**: Find where grouped bar chart HTML is generated

**Required Changes**:
```javascript
// Add at function start
const chartData = Array.isArray(data) ? data[0] : data;
const datasets = chartData.datasets || [];
const labels = chartData.labels || [];

// Update Chart.js config
options: {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  },
  scales: {
    x: {
      stacked: false  // NOT stacked for grouped
    },
    y: {
      stacked: false,  // NOT stacked for grouped
      beginAtZero: true
    }
  }
}
```

#### **area_stacked (Stacked Area Chart)**

**Current Code Location**: Find where stacked area chart HTML is generated

**Required Changes**:
```javascript
// Add at function start
const chartData = Array.isArray(data) ? data[0] : data;
const datasets = chartData.datasets || [];
const labels = chartData.labels || [];

// Update Chart.js config
type: 'line',  // Area charts use 'line' type with fill
data: {
  labels: labels,
  datasets: datasets.map(ds => ({
    ...ds,
    fill: true,  // Enable fill for area effect
    tension: 0.4  // Smooth lines
  }))
},
options: {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    filler: {
      propagate: false
    }
  },
  scales: {
    x: {
      stacked: true  // Stacked on x-axis
    },
    y: {
      stacked: true,  // Stacked on y-axis
      beginAtZero: true
    }
  },
  interaction: {
    mode: 'index',
    intersect: false
  }
}
```

#### **bar_stacked (Stacked Bar Chart)**

**Current Code Location**: Find where stacked bar chart HTML is generated

**Required Changes**:
```javascript
// Add at function start
const chartData = Array.isArray(data) ? data[0] : data;
const datasets = chartData.datasets || [];
const labels = chartData.labels || [];

// Update Chart.js config
type: 'bar',
data: {
  labels: labels,
  datasets: datasets
},
options: {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    }
  },
  scales: {
    x: {
      stacked: true  // Stacked on x-axis
    },
    y: {
      stacked: true,  // Stacked on y-axis
      beginAtZero: true
    }
  }
}
```

---

## Testing Checklist

### Unit Testing (Analytics Service)

Create test cases for each chart type:

```javascript
describe('Chart Data Unpacking', () => {
  test('bar_grouped handles array-wrapped data', () => {
    const input = [{
      datasets: [{label: 'Q1', data: [1, 2, 3]}],
      labels: ['A', 'B', 'C']
    }];

    const html = generateGroupedBarChart(input);
    expect(html).toContain('datasets');
    expect(html).toContain('labels');
    expect(html).not.toContain('undefined');
  });

  test('bar_grouped handles direct object data', () => {
    const input = {
      datasets: [{label: 'Q1', data: [1, 2, 3]}],
      labels: ['A', 'B', 'C']
    };

    const html = generateGroupedBarChart(input);
    expect(html).toContain('datasets');
    expect(html).toContain('labels');
  });

  test('area_stacked handles array-wrapped data', () => {
    const input = [{
      datasets: [{label: 'Series 1', data: [10, 20, 30]}],
      labels: ['Jan', 'Feb', 'Mar']
    }];

    const html = generateStackedAreaChart(input);
    expect(html).toContain('stacked: true');
    expect(html).toContain('fill: true');
  });

  test('bar_stacked handles array-wrapped data', () => {
    const input = [{
      datasets: [{label: 'Product A', data: [100, 200, 300]}],
      labels: ['Q1', 'Q2', 'Q3']
    }];

    const html = generateStackedBarChart(input);
    expect(html).toContain('stacked: true');
  });
});
```

### Integration Testing (with Layout Builder v7.5)

**Test Presentation Setup**:
```bash
# Create test presentations for each chart type
POST /api/analytics/generate
{
  "chart_type": "bar_grouped",
  "data": [{
    "datasets": [
      {"label": "Q1 2025", "data": [120, 190, 300], "backgroundColor": "#3b82f6"},
      {"label": "Q2 2025", "data": [150, 220, 350], "backgroundColor": "#10b981"}
    ],
    "labels": ["Product A", "Product B", "Product C"]
  }],
  "title": "Quarterly Sales Comparison"
}
```

**Validation Steps**:
1. ✅ Chart renders (not blank)
2. ✅ All datasets visible
3. ✅ Labels display correctly
4. ✅ No console errors
5. ✅ Tooltips work on hover
6. ✅ Legend displays all series
7. ✅ Colors match dataset configuration
8. ✅ Layout Builder displays chart in L01/L02/L03 layouts

### Visual Validation Checklist

Test each chart type with real data:

- [ ] **bar_grouped**:
  - [ ] Multiple bars side-by-side (not stacked)
  - [ ] Each dataset has different color
  - [ ] Legend shows all datasets
  - [ ] Tooltips work correctly
  - [ ] No "Item 0" text
  - [ ] No error messages

- [ ] **area_stacked**:
  - [ ] Areas stack on top of each other
  - [ ] Fill colors visible
  - [ ] Smooth curves (tension: 0.4)
  - [ ] Legend shows all series
  - [ ] Tooltips show correct values
  - [ ] Y-axis scales appropriately

- [ ] **bar_stacked**:
  - [ ] Bars stack vertically
  - [ ] Total height represents sum
  - [ ] Each segment has different color
  - [ ] Legend shows all datasets
  - [ ] Tooltips show individual and total values
  - [ ] No gaps between segments

---

## Success Metrics

| Metric | Before Fix | After Fix | Target |
|--------|-----------|-----------|--------|
| bar_grouped Success | 0% (error) | 100% | ✅ 100% |
| area_stacked Success | 0% (blank) | 100% | ✅ 100% |
| bar_stacked Success | 0% (blank) | 100% | ✅ 100% |
| Overall Analytics Success | 77% (10/13) | 100% (13/13) | ✅ 100% |
| Console Errors | 1 error | 0 errors | ✅ 0 |

---

## Timeline & Priority

**Priority**: P0 (Critical)
**Estimated Fix Time**: 30 minutes per chart type (1.5 hours total)
**Testing Time**: 30 minutes
**Total Time**: ~2 hours

**Recommended Schedule**:
1. Day 1 Morning: Fix bar_grouped (30 min)
2. Day 1 Morning: Fix area_stacked (30 min)
3. Day 1 Afternoon: Fix bar_stacked (30 min)
4. Day 1 Afternoon: Test all 3 charts (30 min)
5. Day 1 EOD: Deploy to staging
6. Day 2 Morning: Validate with Layout Builder v7.5
7. Day 2 Afternoon: Deploy to production

---

## Related Issues

### Layout Builder CDN Fix (COMPLETED ✅)

**Date**: November 19, 2025
**Fix**: Added 5 missing Chart.js plugin CDNs to Layout Builder v7.5
**Impact**: Fixed 7 other chart types (treemap, heatmap, matrix, boxplot, candlestick, financial, sankey)
**Success Rate Improvement**: 23% → 77% (3/13 → 10/13)

**File Modified**: `viewer/presentation-viewer.html`
**CDNs Added**:
- chartjs-chart-treemap@2.3.0
- chartjs-chart-matrix@2.0.1
- chartjs-chart-box-and-violin-plot@3.0.0
- chartjs-chart-financial@0.1.0
- chartjs-chart-sankey@0.11.0

---

## Combined Impact

### Before Any Fixes
- **Working Charts**: 3/13 (23%)
- **Broken Charts**: 10/13 (77%)
  - 7 broken: Missing CDN plugins (Layout Builder issue)
  - 3 broken: Data unpacking bug (Analytics issue)

### After Layout Builder CDN Fix
- **Working Charts**: 10/13 (77%)
- **Broken Charts**: 3/13 (23%)
  - 3 broken: Data unpacking bug (Analytics issue) ⬅️ **THIS ISSUE**

### After Analytics Data Unpacking Fix
- **Working Charts**: 13/13 (100%) ✅
- **Broken Charts**: 0/13 (0%) ✅

---

## Code Examples Repository

### Complete Working Examples

#### Example 1: Grouped Bar Chart (Fixed)
```javascript
function generateGroupedBarChart(data) {
  // Unpack data
  const chartData = Array.isArray(data) ? data[0] : data;
  const datasets = chartData.datasets || [];
  const labels = chartData.labels || [];

  // Validate
  if (!datasets || datasets.length === 0) {
    throw new Error("Grouped bar chart requires 'datasets' in data");
  }

  return `
    <div style="width: 100%; height: 100%; position: relative;">
      <canvas id="chart-${Date.now()}"></canvas>
      <script>
        (function() {
          const ctx = document.getElementById('chart-${Date.now()}').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ${JSON.stringify(labels)},
              datasets: ${JSON.stringify(datasets)}
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                },
                title: {
                  display: false
                }
              },
              scales: {
                x: {
                  stacked: false
                },
                y: {
                  stacked: false,
                  beginAtZero: true
                }
              }
            }
          });
        })();
      </script>
    </div>
  `;
}
```

#### Example 2: Stacked Area Chart (Fixed)
```javascript
function generateStackedAreaChart(data) {
  // Unpack data
  const chartData = Array.isArray(data) ? data[0] : data;
  const datasets = chartData.datasets || [];
  const labels = chartData.labels || [];

  // Validate
  if (!datasets || datasets.length === 0) {
    throw new Error("Stacked area chart requires 'datasets' in data");
  }

  // Add fill and tension for area effect
  const areaDatasets = datasets.map(ds => ({
    ...ds,
    fill: true,
    tension: 0.4
  }));

  return `
    <div style="width: 100%; height: 100%; position: relative;">
      <canvas id="chart-${Date.now()}"></canvas>
      <script>
        (function() {
          const ctx = document.getElementById('chart-${Date.now()}').getContext('2d');
          new Chart(ctx, {
            type: 'line',
            data: {
              labels: ${JSON.stringify(labels)},
              datasets: ${JSON.stringify(areaDatasets)}
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                },
                filler: {
                  propagate: false
                }
              },
              scales: {
                x: {
                  stacked: true
                },
                y: {
                  stacked: true,
                  beginAtZero: true
                }
              },
              interaction: {
                mode: 'index',
                intersect: false
              }
            }
          });
        })();
      </script>
    </div>
  `;
}
```

#### Example 3: Stacked Bar Chart (Fixed)
```javascript
function generateStackedBarChart(data) {
  // Unpack data
  const chartData = Array.isArray(data) ? data[0] : data;
  const datasets = chartData.datasets || [];
  const labels = chartData.labels || [];

  // Validate
  if (!datasets || datasets.length === 0) {
    throw new Error("Stacked bar chart requires 'datasets' in data");
  }

  return `
    <div style="width: 100%; height: 100%; position: relative;">
      <canvas id="chart-${Date.now()}"></canvas>
      <script>
        (function() {
          const ctx = document.getElementById('chart-${Date.now()}').getContext('2d');
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ${JSON.stringify(labels)},
              datasets: ${JSON.stringify(datasets)}
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                }
              },
              scales: {
                x: {
                  stacked: true
                },
                y: {
                  stacked: true,
                  beginAtZero: true
                }
              }
            }
          });
        })();
      </script>
    </div>
  `;
}
```

---

## Contact & Support

**For Questions About This Bug**:
- **Analytics Team**: Implement data unpacking fix
- **Layout Builder Team**: CDN fix completed (Nov 19, 2025)
- **Test Coordination**: Validate end-to-end after both fixes

**Related Documentation**:
- Chart.js 4.x Documentation: https://www.chartjs.org/docs/latest/
- Layout Builder v7.5 Integration Guide: `/docs/FRONTEND_INTEGRATION_GUIDE.md`
- Analytics API Documentation: (link to Analytics docs)

---

**Report Generated**: November 19, 2025
**Report Author**: Layout Builder Team
**Status**: Ready for Analytics Team Implementation

**End of Report**
