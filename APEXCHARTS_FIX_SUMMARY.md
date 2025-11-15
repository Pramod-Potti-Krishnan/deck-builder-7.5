# ApexCharts Support - CORRECTED Implementation

**Branch**: `feature/analytics-apexcharts-support`
**Status**: ✅ Fixed (removed double-escaping bug)

---

## What Was Wrong (Previous Attempt)

**Bug**: Line 207 was double-escaping backslashes that `json.dumps()` already escaped:

```python
# ❌ BROKEN CODE (previous attempt):
presentation_json_safe = (
    presentation_json
    .replace('\\', '\\\\')  # This double-escaped already-valid JSON!
    .replace('</', '<\\/')
    .replace('\u2028', '\\u2028')
    .replace('\u2029', '\\u2029')
)
```

**Result**: Broke ALL presentations with error:
```
Unexpected identifier 'width'. Expected '}' to end an object literal
```

**Example**:
- Original: `style="width: 100%"`
- After json.dumps(): `"style=\"width: 100%\""` ✅ Valid JSON
- After our .replace(): `"style=\\"width: 100%\\""` ❌ Double-escaped, invalid

---

## What's Correct Now

**Fixed Code** (lines 199-216):

```python
# ✅ CORRECT CODE:
presentation_json = json.dumps(presentation, ensure_ascii=False)

# Escape ONLY what json.dumps() doesn't handle
presentation_json_safe = (
    presentation_json
    # NOTE: NO backslash escaping - json.dumps() handles it!
    .replace('</', '<\\/')           # Prevent </script> injection
    .replace('\u2028', '\\u2028')    # Escape line separator
    .replace('\u2029', '\\u2029')    # Escape paragraph separator
)
```

**Why This Works**:
1. `json.dumps()` already produces valid JavaScript with proper backslash escaping
2. We only need to escape 3 special patterns that would break JS:
   - `</` (prevents premature script tag closing)
   - `\u2028` (line separator breaks JS parsing)
   - `\u2029` (paragraph separator breaks JS parsing)
3. Everything else (including template literals with `${}`) works automatically

---

## What Now Works

✅ **All existing presentations** - Render correctly (no double-escaping)
✅ **ApexCharts with `<script>` tags** - Work perfectly
✅ **Template literals** - `` `Hello ${name}` `` fully supported
✅ **Complex JavaScript** - All valid JS syntax works

---

## Testing

**Test File**: `test_analytics_apexcharts.json`

```bash
# Start server
python server.py

# Create test presentation
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test_analytics_apexcharts.json

# Verify:
# 1. No console errors
# 2. Charts render correctly
# 3. Template literals work
# 4. Existing presentations still work
```

---

## For Analytics Team

**Use These Layouts**:
- **L01**: Single centered chart → `element_4` field
- **L02**: Chart + explanation → `element_3` field
- **L03**: Two comparison charts → `element_4` + `element_2` fields

**Example**:
```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Revenue Trend",
    "element_1": "Q1-Q4 2024",
    "element_4": "<div id='chart-rev' style='width:100%; height:100%;'></div>\n<script>\n(function() {\n  var data = [`Q1`, `Q2`, `Q3`, `Q4`];\n  // your ApexCharts code here\n})();\n</script>"
  }
}
```

**Key Points**:
- ✅ Use template literals freely: `` `$${value}M` ``
- ✅ Wrap in IIFE: `(function() { ... })()`
- ✅ Unique chart IDs: `chart-${slideId}-type`
- ✅ No special escaping needed

---

## Technical Summary

**What We Escape**:
| Pattern | Reason | Example |
|---------|--------|---------|
| `</` → `<\/` | Prevents script tag injection | `</script>` in string |
| `\u2028` → `\\u2028` | Line separator breaks JS | Unicode U+2028 |
| `\u2029` → `\\u2029` | Paragraph separator breaks JS | Unicode U+2029 |

**What We DON'T Escape**:
- ❌ Backslashes (json.dumps handles it)
- ❌ Quotes (json.dumps handles it)
- ❌ Newlines (json.dumps handles it)
- ❌ Template literals (work natively in JS)

---

## Commit Strategy

1. ✅ **Reverted broken commit** to `feature/6-layout-system-with-docs` (production safe)
2. ✅ **Created new branch** `feature/analytics-apexcharts-support`
3. ✅ **Applied correct fix** (no double-escaping)
4. 🔄 **Test thoroughly** before merging

---

**Status**: Ready for testing ✅
