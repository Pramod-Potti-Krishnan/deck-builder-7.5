# Layout Service Response: Theme System Architecture Review

**Date:** 2025-12-20
**From:** Layout Service Team
**To:** Text Service Team, Director Team
**Re:** Review of THEME_SYSTEM_DESIGN.md (Section 4.3.2)

---

## Executive Summary

**✅ Layout Service confirms alignment with all requirements in Section 4.3.2.**

We have the infrastructure to serve as the canonical theme source. Minor additions needed for full 20+ color palette compliance.

---

## Current Capabilities

### 1. THEME REGISTRY ✅
**Files:** `src/themes/theme-registry.js`, `server.py` (PREDEFINED_THEMES)

| Theme ID | Name | Description |
|----------|------|-------------|
| `corporate-blue` | Corporate Blue | Professional business theme |
| `elegant-emerald` | Elegant Emerald | Nature-inspired sophistication |
| `vibrant-orange` | Vibrant Orange | Creative energy theme |
| `dark-mode` | Dark Mode | Low-light optimized |

Each theme includes:
- ✅ Full color palette (15 keys currently)
- ✅ Typography hierarchy (hero, standard, content)
- ✅ Content styles (h1-h3, p, ul, li)

### 2. THEME API ENDPOINTS ✅

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `GET /api/themes` | List all themes | Array of theme summaries |
| `GET /api/themes/{theme_id}` | **Full theme config** | Complete palette + typography |
| `GET /api/themes/{theme_id}/typography` | Typography for Text Service | Font metrics + char ratios |
| `GET /api/themes/public` | List public themes | Excludes user-private themes |

### 3. AVAILABLE SPACE ✅
**File:** `src/layout_registry.py`

We provide content area dimensions for each layout:

```python
CONTENT_AREAS = {
    "C1-text": {"content": {"rows": "4-18", "cols": "2-32"}},   # 30x14 grids = 1800x840px
    "L25":     {"content": {"rows": "5-17", "cols": "2-32"}},   # 30x12 grids = 1800x720px
    "L29":     {"content": {"rows": "1-19", "cols": "1-33"}},   # 32x18 grids = 1920x1080px
    # ... all 26 layouts defined
}
```

### 4. THEME CSS & BOX STYLING ✅
**Files:** `src/themes/theme-manager.js`, `src/renderers/style-builder.js`

- CSS custom properties for each theme
- Box fills, borders, backgrounds use palette colors
- Class-based theme switching (`theme-professional`, `theme-executive`, etc.)

---

## Sync Endpoint Answer

**Q:** Can you provide a sync endpoint so Director and Text Service can pull theme definitions?

**A: YES ✅**

### Option A: Use Existing Endpoint (Recommended for MVP)
```
GET /api/themes/{theme_id}

Response:
{
  "id": "corporate-blue",
  "name": "Corporate Blue",
  "colors": {
    "primary": "#1e40af",
    "primaryLight": "#3b82f6",
    ...15+ colors
  },
  "typography": {
    "fontFamily": "Poppins, sans-serif",
    "hero": {...},
    "standard": {...}
  }
}
```

Director/Text Service can call this on startup for each theme_id they need.

### Option B: Add Bulk Sync Endpoint (If Preferred)
```
GET /api/themes/sync

Response:
{
  "version": "1.0.0",
  "last_updated": "2025-12-20T12:00:00Z",
  "themes": {
    "corporate-blue": { ...full config... },
    "elegant-emerald": { ...full config... },
    "vibrant-orange": { ...full config... },
    "dark-mode": { ...full config... }
  }
}
```

---

## Action Items for Layout Service

| Task | Priority | Status |
|------|----------|--------|
| Add chart colors (`chart_1` - `chart_6`) to each theme | High | Pending |
| Add tertiary colors (`tertiary_1` - `tertiary_3`) | High | Pending |
| Add `/api/themes/sync` bulk endpoint | Medium | Pending |
| Add version tracking to theme registry | Low | Pending |

---

## Questions for Text Service Team

1. **Sync Format Preference:**
   Do you prefer Option A (per-theme fetch) or Option B (bulk sync)?

2. **Color Key Naming:**
   We currently use camelCase (`primaryLight`, `textPrimary`).
   Your doc shows snake_case (`primary_light`, `text_primary`).
   Which format should be canonical?

3. **Typography Token Names:**
   We have `t1, t2, t3, t4` + `hero`, `standard`.
   Your doc shows `deckster-t1, deckster-t2` CSS classes.
   Should we add a `cssClassName` field to typography tokens?

4. **Fallback Strategy:**
   If Layout Service is unreachable at startup, should Director/Text Service:
   - (a) Use embedded fallback themes?
   - (b) Fail startup?
   - (c) Retry with backoff?

5. **Custom Theme Sync:**
   Should `/api/themes/sync` include user-created custom themes, or only presets?

---

## Blurb for Text Service Team

```
Subject: RE: Theme System Architecture - Layout Service Confirms Alignment

Team,

We've reviewed THEME_SYSTEM_DESIGN.md and confirm Layout Service can fulfill
all responsibilities in Section 4.3.2:

✅ Host canonical THEME_REGISTRY - We have 4 themes with full palettes
✅ Provide available_space - All 26 layouts have content area dimensions
✅ Generate theme CSS - CSS custom properties ready
✅ Enable instant theme switching - CSS class swap, no regeneration

SYNC ENDPOINT: We can provide themes via:
- GET /api/themes/{theme_id} (exists now)
- GET /api/themes/sync (bulk, can add if preferred)

ACTION NEEDED: We'll add chart colors (chart_1-6) and tertiary colors
(tertiary_1-3) to complete the 20+ key palette spec.

QUESTIONS:
1. Prefer per-theme or bulk sync endpoint?
2. Color key naming: camelCase or snake_case?
3. What's your fallback if Layout Service is unreachable?

Please advise on the above. Ready to implement once confirmed.

Best,
Layout Service Team
```

---

## Implementation Plan

### Phase 1: Palette Expansion (High Priority)
1. Add to each theme in `server.py` PREDEFINED_THEMES:
   ```python
   "chart_1": "#3b82f6",
   "chart_2": "#10b981",
   "chart_3": "#f59e0b",
   "chart_4": "#ef4444",
   "chart_5": "#8b5cf6",
   "chart_6": "#ec4899",
   "tertiary_1": "#...",
   "tertiary_2": "#...",
   "tertiary_3": "#..."
   ```
2. Mirror in `theme-registry.js` for frontend

### Phase 2: Sync Endpoint (If Requested)
1. Add `GET /api/themes/sync` with version + timestamp
2. Include all predefined themes in single response
3. Add cache headers for performance

### Phase 3: CSS Class Generation (For Text Service)
1. Generate `.deckster-t1`, `.deckster-t2`, etc. classes
2. Include in theme CSS output
3. Document class names for Text Service usage

---

## Files to Modify

| File | Changes |
|------|---------|
| `server.py` | Add chart/tertiary colors to PREDEFINED_THEMES |
| `src/themes/theme-registry.js` | Mirror color additions |
| `src/themes/theme-manager.js` | Generate deckster-* CSS classes |
| `docs/THEME_API.md` | Document sync endpoint (if added) |
