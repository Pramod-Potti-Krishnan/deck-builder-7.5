# Ghost Elements Fix - Implementation Progress

**Last Updated:** 2025-12-07
**Status:** COMPLETE ✅

## Latest Fix: C1-C6 Element Type Mapping & Grid Positions
- **Issue:** C1-C6 content elements incorrectly mapped to 'content' (Text Service) type
- **Root Cause:** `getElementTypeForSlot()` checked slot NAME before TAG
  - C-series uses slot name `content` with different tags (body, table, chart, etc.)
  - `'content': 'content'` in SLOT_TO_ELEMENT_TYPE matched first ❌
- **Fix 1:** Changed priority in `getElementTypeForSlot()` to check TAG before slot name ✅
  - Now C3-chart: slot `content` with tag `chart` → creates chart element
  - L25/L29: tag `content` → creates content element (Text Service)
- **Fix 2:** Updated C1-C6 grid positions to match v7.4-template-builder ✅
  - title: `gridRow: '1/3'` → `'2/3'`
  - content: `gridRow: '4/17'` → `'5/17'`
  - footer: `gridRow: '17/19'` → `'18/19'`, `gridColumn: '2/10'` → `'2/7'`
  - logo: `gridRow: '17/19'` → `'18/19'`

## Previous Fix: L29 Auto-Save Selector Mismatch (Commit f6cd245)
- **Issue:** L29 hero content edits showed "Saved" but were lost on refresh
- **Root Cause:** Selector mismatch in `auto-save.js` line 220
  - L29.js uses: `class="hero-content-area"` and `data-section-type="hero"`
  - auto-save.js looked for: `.hero-content, [data-section="hero"]` ❌
- **Fix:** Updated selector to `.hero-content-area, [data-section-type="hero"]` ✅

## Completed Tasks

### 1. Backend Schema Changes (models.py) - COMPLETE ✅
- [x] Added `parent_slide_id` to `TextBox` model (line 287-290)
- [x] Added `parent_slide_id` to `ImageElement` model (line 359-362)
- [x] Added `parent_slide_id` to `ChartElement` model (line 412-415)
- [x] Added `parent_slide_id` to `InfographicElement` model (line 464-467)
- [x] Added `parent_slide_id` to `DiagramElement` model (line 516-519)
- [x] Updated ID format from `{type}-{uuid12}` to `{type}_{uuid8}` for all elements
- [x] Added `slide_id` to `Slide` model (line 638-641)
- [x] Added `ContentElement` model for new 'content' element type (lines 558-615)
- [x] Added `contents` field to `Slide` model (line 678-681)
- [x] Added `contents` field to `SlideContentUpdate` model (lines 818-822)
- [x] Added validator for contents limit (lines 723-729)

### 2. Backend Validation & Cleanup (server.py) - COMPLETE ✅
- [x] Added `is_element_valid_for_slide()` helper function (lines 834-860)
- [x] Added `cleanup_orphan_elements()` endpoint at `/api/presentations/{id}/cleanup-orphans` (lines 863-954)
- [x] Auto-generates slide_id for old presentations during cleanup
- [x] Logs removed element IDs for debugging

### 3. L-Series Element Mapping (template-registry.js) - COMPLETE ✅
- [x] Added L25 (Main Content Shell) with content, title, subtitle, footer, logo slots
- [x] Added L29 (Hero Full-Bleed) with hero slot (content type)
- [x] Added L27 (Image Left with Content Right) with image, title, subtitle, text, footer, logo
- [x] Added L01 (Centered Chart with Text Below) with chart, title, subtitle, body, footer, logo
- [x] Added L02 (Left Diagram with Text Right) with diagram, title, subtitle, text, footer, logo
- [x] Added L03 (Two Charts in Columns) with chart1, chart2, body_left, body_right, title, subtitle, footer, logo
- [x] Added formatOwner attribute for content slots (text_service, analytics_service)

### 4. Frontend UUID Changes (direct-element-creator.js) - COMPLETE ✅
- [x] Added `generateElementId()` function for UUID-based element IDs
- [x] Added `generateLegacyElementId()` for backward compatibility
- [x] Updated SLOT_TO_ELEMENT_TYPE with L-series slots (content, hero, chart1, chart2, body_left, body_right, text)
- [x] Updated createElementsForTemplate() to get/generate slide_id
- [x] Updated all creation functions to use elementContext pattern
- [x] Added parent_slide_id and slot_name to all element configs
- [x] Added data-parent-slide-id and data-slot-name attributes to created elements
- [x] Added createContent() function for L-series content elements
- [x] Added getContentHtml() for mapping content slot names to content fields

### 5. Frontend UUID Changes (slot-converter.js) - COMPLETE ✅
- [x] Update buildTextBoxConfigFromSlot() with UUID-based IDs
- [x] Update buildImageConfigFromSlot() with UUID-based IDs
- [x] Update buildVisualElementConfig() with UUID-based IDs
- [x] Add parent_slide_id and slot_name to all configs
- [x] Add data attributes to converted elements

### 6. Auto-Save Validation (auto-save.js) - COMPLETE ✅
- [x] Update collectTextBoxes() to validate parent_slide_id
- [x] Update collectImages() to validate parent_slide_id
- [x] Update collectCharts() to validate parent_slide_id
- [x] Update collectInfographics() to validate parent_slide_id
- [x] Update collectDiagrams() to validate parent_slide_id
- [x] Add collectContents() for content elements
- [x] Skip orphaned elements during collection
- [x] Include slide_id in save payload

### 7. L-Series Renderers - COMPLETE ✅
- [x] Add data-slot-name attributes to L01.js (title, subtitle, chart, body, footer, logo)
- [x] Add data-slot-name attributes to L02.js (title, subtitle, diagram, text, footer, logo)
- [x] Add data-slot-name attributes to L03.js (title, subtitle, chart1, chart2, body_left, body_right, footer, logo)
- [x] Add data-slot-name attributes to L25.js (title, subtitle, content, footer, logo)
- [x] Add data-slot-name attributes to L27.js (image, title, subtitle, text, footer, logo)
- [x] Add data-slot-name attributes to L29.js (hero)

### 8. Migration Script - COMPLETE ✅
- [x] Create add_slide_ids.py migration script
  - Supports dry-run mode (--dry-run)
  - Can migrate single presentation (--presentation-id)
  - Optional ID regeneration for legacy elements (--regenerate-ids)
  - Works with both local file storage and Supabase

---

## Files Modified So Far

| File | Lines Changed | Description |
|------|---------------|-------------|
| `models.py` | 271-295, 343-366, 396-423, 448-475, 500-527, 558-615, 638-641, 678-681, 723-729, 818-822 | Added parent_slide_id, slide_id, ContentElement model |
| `server.py` | 834-954 | Added cleanup-orphans endpoint with validation |
| `template-registry.js` | 1341-1792 | Added L-series templates (L01, L02, L03, L25, L27, L29) |
| `direct-element-creator.js` | Full file | UUID architecture, content element type |
| `slot-converter.js` | Full file | UUID architecture, parent ownership |
| `auto-save.js` | 198-275, 278-372, 375-450, 453-522, 524-587, 589-659, 661-725 | Parent validation, slide_id, collectContents() |
| `L01.js` | 24-80 | Added data-slot-name, data-format-owner attributes |
| `L02.js` | 48-103 | Added data-slot-name, data-format-owner attributes |
| `L03.js` | 24-100 | Added data-slot-name, data-format-owner attributes |
| `L25.js` | 42-98 | Added data-slot-name attributes |
| `L27.js` | 24-78 | Added data-slot-name attributes |
| `L29.js` | 46-59 | Added data-slot-name attribute |
| `migrations/add_slide_ids.py` | New file | Migration script for existing data |

---

## Key Code Patterns

### Element ID Format (New)
```javascript
// Old format (problematic - index-based):
id = `slide-${slideIndex}-${slotName}`;  // slide-16-title

// New format (UUID-based):
id = `${slideId}_${elementType}_${uuid8}`;  // slide_a3f7e8c2d5b1_textbox_f8c2d5b1
```

### Element Context Pattern (Frontend)
```javascript
const elementContext = {
  slideIndex,
  slideId,
  slotName,
  slotDef,
  content,
  useLegacyIds  // true if slide doesn't have slide_id yet
};
```

### Parent Slide Reference
```python
parent_slide_id: Optional[str] = Field(
    default=None,
    description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
)
```

### Content Element (New Type)
```javascript
// L-series content slots map to 'content' element type
// Text Service owns these - read-only in layout builder
{
  id: generateElementId(slideId, 'content'),
  parent_slide_id: slideId,
  slot_name: slotName,
  format_owner: slotDef.formatOwner || 'text_service',
  editable: false,
  locked: true
}
```

---

## Plan File Location
Full plan: `/Users/pk1980/.claude/plans/cozy-cuddling-waffle.md`
