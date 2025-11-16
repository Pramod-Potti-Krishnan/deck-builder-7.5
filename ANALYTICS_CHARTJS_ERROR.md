# Chart.js Tooltip Error - Analytics Service Issue

**Date**: November 16, 2025
**Presentation ID**: dd6d8551-64b3-4c13-91ed-f339667e387a
**Service**: Analytics Microservice v3
**Status**: Requires Analytics team fix

---

## Error Description

Browser console shows Chart.js error when rendering L02 analytics presentations:

```
TypeError: n.label.call is not a function. (In 'n.label.call(this,t)', 'n.label.call' is undefined)
    (anonymous function) (chart.min.js:13:158676)
```

**Error Location**: Chart.js tooltip callback execution
**Impact**: Chart renders but tooltip functionality may be broken
**Layout Builder Version**: v7.5.1
**Chart.js Version**: 3.9.1 (loaded in presentation-viewer.html)

---

## Root Cause

The error indicates that Chart.js is trying to call a `label` property as a function, but it's **not a function**.

This typically happens when:
1. **Tooltip callback syntax is incorrect** (Chart.js 2.x vs 3.x)
2. **label property is a string or number** instead of a function
3. **Missing or malformed tooltip configuration**

---

## Chart.js 3.x Correct Syntax

### ✅ Correct Tooltip Configuration

```javascript
options: {
  plugins: {
    tooltip: {
      callbacks: {
        label: function(context) {  // MUST be a function
          return context.dataset.label + ': ' + context.parsed.y;
        }
      }
    }
  }
}
```

### ❌ Common Mistakes

**1. Using string instead of function**:
```javascript
// WRONG - causes n.label.call error
tooltip: {
  callbacks: {
    label: 'Revenue'  // Not a function!
  }
}
```

**2. Chart.js 2.x syntax (incompatible with 3.x)**:
```javascript
// WRONG - old syntax
tooltips: {  // Should be 'tooltip' in v3
  callbacks: {
    label: function(tooltipItem, data) {  // Wrong parameters
      return data.datasets[tooltipItem.datasetIndex].label;
    }
  }
}
```

**3. Missing context parameter**:
```javascript
// WRONG - no parameter
tooltip: {
  callbacks: {
    label: function() {  // Missing context parameter
      return 'Value';
    }
  }
}
```

---

## Analytics Service Fix Required

### Step 1: Locate Chart.js Generation Code

Find where Analytics Service generates Chart.js code for L02 presentations.

Likely files:
- Analytics chart generation logic
- L02 template generation
- Chart.js configuration builder

### Step 2: Audit Tooltip Configurations

Search for all `tooltip` or `tooltips` configurations in Chart.js generation code.

Check for:
- ✅ `tooltip` (not `tooltips`)
- ✅ `callbacks.label` is a **function**
- ✅ Function has `context` parameter
- ✅ Using Chart.js 3.x syntax

### Step 3: Fix Tooltip Callbacks

**Template Example for Analytics Service**:

```javascript
// Chart.js 3.x compatible tooltip
const chartConfig = {
  type: 'line',
  data: {
    labels: ${JSON.stringify(labels)},
    datasets: [{
      label: '${label}',
      data: ${JSON.stringify(data)},
      borderColor: '${color}',
      tension: 0.4
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0
              }).format(context.parsed.y);
            }
            return label;
          }
        }
      },
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '$' + value.toLocaleString();
          }
        }
      }
    }
  }
};

new Chart(ctx, chartConfig);
```

### Step 4: Test Fix

**Create Test L02 Presentation**:
1. Generate L02 chart with Analytics Service
2. Send to Layout Builder
3. Verify in browser console:
   - ✅ No "n.label.call is not a function" error
   - ✅ Tooltips display correctly on hover
   - ✅ Chart renders properly

---

## Chart.js 3.x Migration Guide

If Analytics is using Chart.js 2.x syntax, migrate using:

### Key Changes from 2.x to 3.x

**1. Configuration Namespacing**:
```javascript
// v2.x
options: {
  tooltips: { ... },
  legend: { ... },
  title: { ... }
}

// v3.x
options: {
  plugins: {
    tooltip: { ... },
    legend: { ... },
    title: { ... }
  }
}
```

**2. Callback Parameters**:
```javascript
// v2.x
callbacks: {
  label: function(tooltipItem, data) {
    return data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
  }
}

// v3.x
callbacks: {
  label: function(context) {
    return context.dataset.data[context.dataIndex];
  }
}
```

**3. Context Object** (v3.x):
```javascript
context = {
  chart: Chart,
  dataIndex: number,
  dataset: object,
  datasetIndex: number,
  parsed: { x: number, y: number },
  raw: any,
  element: Element,
  label: string
}
```

---

## Testing Checklist for Analytics Team

Before deploying fix:

- [ ] Audit all Chart.js generation code
- [ ] Verify using Chart.js 3.x syntax (not 2.x)
- [ ] Confirm `tooltip` (not `tooltips`)
- [ ] Ensure `callbacks.label` is a function
- [ ] Test tooltip display on hover
- [ ] Verify no console errors
- [ ] Test with multiple chart types (line, bar, pie)
- [ ] Verify with different data sets
- [ ] Test on both local and Railway deployments

---

## Layout Builder Status

**Layout Builder v7.5.1** has completed its part:
- ✅ Fixed viewport dimensions (1920×1080px)
- ✅ L02 content now fits properly without overflow
- ✅ HTML rendering working correctly
- ✅ Grid system fixed

**Remaining Issue**: Chart.js tooltip error in **Analytics Service** generated code

---

## Next Steps

1. **Analytics Team**: Fix Chart.js tooltip configuration
2. **Analytics Team**: Test with Layout Builder v7.5.1
3. **Analytics Team**: Verify tooltips work correctly
4. **Director Team**: No changes needed, pass-through working correctly

---

## References

- **Chart.js 3.x Documentation**: https://www.chartjs.org/docs/latest/
- **Migration Guide**: https://www.chartjs.org/docs/latest/getting-started/v3-migration.html
- **Tooltip Configuration**: https://www.chartjs.org/docs/latest/configuration/tooltip.html
- **Tooltip Callbacks**: https://www.chartjs.org/docs/latest/configuration/tooltip.html#tooltip-callbacks

---

## Contact

For questions about this error:
- **Layout Builder**: Fixed (v7.5.1 deployed)
- **Analytics Service**: Needs fix (tooltip callback issue)
- **Test Presentation**: dd6d8551-64b3-4c13-91ed-f339667e387a on Railway

**End of Document**
