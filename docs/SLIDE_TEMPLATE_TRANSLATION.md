# Slide Template Translation Guide

This document describes how to translate template definitions from the **Template Builder** to the **Frontend Rendering System** (`template-registry.js`).

---

## Overview

The Template Builder is the source of truth for all slide template designs. When translating to the frontend:

1. **Template Builder** → defines visual design (grid positions, fonts, alignment, colors)
2. **`template-registry.js`** → stores slot definitions with styles
3. **`buildSlotStyle()`** → converts slot definitions to inline CSS
4. **Renderer functions** → generate HTML with inline styles

---

## 1. Grid System Translation

### Template Builder Grid Specifications

The Template Builder uses a **32×18 grid system**:
- **32 columns** (numbered 1-32, with grid lines 1-33)
- **18 rows** (numbered 1-18, with grid lines 1-19)

### How to Interpret Grid Positions

Template Builder shows positions as:
- `LeftTopGridPosition: (column, row)` - Top-left corner of the slot
- `RightBottomGridPosition: (column, row)` - Bottom-right corner of the slot

**IMPORTANT**: These are grid CELL numbers, not grid LINE numbers.

### Translation Formula

```
gridColumn: 'LeftTopColumn / (RightBottomColumn + 1)'
gridRow: 'LeftTopRow / (RightBottomRow + 1)'
```

### Example: H1-structured Title

| Template Builder | Value |
|------------------|-------|
| LeftTopGridPosition | (3, 7) |
| RightBottomGridPosition | (17, 10) |

**Translation:**
```javascript
gridColumn: '3/17',   // Start at column 3, end BEFORE column 17
gridRow: '7/10',      // Start at row 7, end BEFORE row 10
```

**Note**: The second number is the grid LINE where the slot ends. Since CSS grid uses grid lines (not cells), and Template Builder gives cell numbers, the formula accounts for this.

---

## 2. Flexbox Alignment Translation

### Critical Concept: `flexDirection: 'column'`

When `flexDirection: 'column'` is set:
- **Main axis** = VERTICAL (top to bottom)
- **Cross axis** = HORIZONTAL (left to right)

This means:
| Property | Controls | `flex-start` | `flex-end` | `center` |
|----------|----------|--------------|------------|----------|
| `justifyContent` | **VERTICAL** | TOP | BOTTOM | MIDDLE |
| `alignItems` | **HORIZONTAL** | LEFT | RIGHT | CENTER |

### Template Builder to CSS Mapping

| Template Builder Property | CSS Property | Mapping |
|---------------------------|--------------|---------|
| `HorizontalAlign: Left` | `alignItems` | `'flex-start'` |
| `HorizontalAlign: Center` | `alignItems` | `'center'` |
| `HorizontalAlign: Right` | `alignItems` | `'flex-end'` |
| `VerticalAlign: Top` | `justifyContent` | `'flex-start'` |
| `VerticalAlign: Middle` | `justifyContent` | `'center'` |
| `VerticalAlign: Bottom` | `justifyContent` | `'flex-end'` |

### Complete Alignment Example

**Template Builder:**
```
HorizontalAlign: Left
VerticalAlign: Bottom
```

**Frontend (`template-registry.js`):**
```javascript
style: {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-start',      // LEFT (horizontal)
  justifyContent: 'flex-end',    // BOTTOM (vertical)
  textAlign: 'left'              // Text within container
}
```

### Common Mistake to Avoid

**WRONG** (properties swapped):
```javascript
alignItems: 'flex-end',        // This means RIGHT, not BOTTOM!
justifyContent: 'flex-start'   // This means TOP, not LEFT!
```

**CORRECT**:
```javascript
alignItems: 'flex-start',      // LEFT (cross-axis = horizontal)
justifyContent: 'flex-end'     // BOTTOM (main-axis = vertical)
```

---

## 3. Typography Translation

### Font Properties

| Template Builder | CSS Property | Example |
|------------------|--------------|---------|
| Font | `fontFamily` | `'Poppins, sans-serif'` |
| FontSize | `fontSize` | `'48px'` |
| FontWeight | `fontWeight` | `'bold'` or `'600'` |
| TextTransform | `textTransform` | `'uppercase'`, `'capitalize'`, `'none'` |

### Font Family Reference

Common fonts used in templates:
```javascript
'Poppins, sans-serif'
'Inter, sans-serif'
'Roboto, sans-serif'
'Montserrat, sans-serif'
'Open Sans, sans-serif'
'Playfair Display, serif'
'Bebas Neue, sans-serif'
```

### Example Typography Translation

**Template Builder:**
```
Font: Poppins
FontSize: 48px
FontWeight: Bold
```

**Frontend:**
```javascript
style: {
  fontFamily: 'Poppins, sans-serif',
  fontSize: '48px',
  fontWeight: 'bold'
}
```

---

## 4. Color Translation

### Color Format

Template Builder may use various formats. Always convert to hex or rgba:

| Template Builder | Frontend CSS |
|------------------|--------------|
| `#ffffff` | `'#ffffff'` |
| `rgb(255, 255, 255)` | `'#ffffff'` or `'rgb(255, 255, 255)'` |
| `rgba(0,0,0,0.5)` | `'rgba(0, 0, 0, 0.5)'` |

### Common Colors

| Purpose | Example Colors |
|---------|----------------|
| Title (on dark bg) | `'#ffffff'` |
| Subtitle (muted) | `'#94a3b8'`, `'#9ca3af'` |
| Dark background | `'#1f2937'`, `'#0f172a'` |
| Accent | `'#3b82f6'`, `'#2563eb'` |

---

## 5. Slot Definition Structure

### Complete Slot Template

```javascript
slotName: {
  // Grid positioning (REQUIRED)
  gridRow: 'startRow/endRow',
  gridColumn: 'startCol/endCol',

  // Metadata
  tag: 'title',                    // Semantic tag: 'title', 'subtitle', 'body', 'footer', 'logo', 'background'
  accepts: ['text'],               // Content types: 'text', 'image', 'html', 'color', 'gradient'

  // Styles
  style: {
    // Typography
    fontSize: '48px',
    fontWeight: 'bold',
    fontFamily: 'Poppins, sans-serif',
    color: '#ffffff',
    textTransform: 'uppercase',    // Optional

    // Flexbox alignment (IMPORTANT - see Section 2)
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',      // Horizontal alignment
    justifyContent: 'flex-end',    // Vertical alignment
    textAlign: 'left',             // Text alignment within

    // Other (optional)
    zIndex: -1,                    // For background layers
    padding: '20px'                // If needed
  },

  // Content
  defaultText: 'Default placeholder text',
  description: 'Human-readable description for UI'
}
```

---

## 6. Template Categories and Naming

### Template ID Format

| Category | Prefix | Examples |
|----------|--------|----------|
| Hero slides | `H` | `H1-generated`, `H1-structured`, `H2-section`, `H3-closing` |
| Content slides | `C` | `C1-text`, `C2-table`, `C3-chart`, `C4-infographic`, `C5-diagram`, `C6-image` |
| Split layouts | `S` | `S1-visual-text`, `S2-image-content`, `S3-two-visuals`, `S4-comparison` |
| Blank | `B` | `B1-blank` |

### Common Slot Names

| Slot Name | Purpose |
|-----------|---------|
| `title` | Main slide title |
| `subtitle` | Subtitle or tagline |
| `body` | Main content area |
| `content` | Generic content area |
| `footer` | Footer text (date, author) |
| `logo` | Company logo |
| `background` | Background image/color layer |
| `section_number` | Section divider number |
| `contact_info` | Contact information (closing slides) |
| `left_content`, `right_content` | Split layout areas |

---

## 7. Translation Checklist

When translating a new template:

### Step 1: Extract Grid Positions
- [ ] Get `LeftTopGridPosition` (column, row)
- [ ] Get `RightBottomGridPosition` (column, row)
- [ ] Convert to `gridColumn` and `gridRow` format

### Step 2: Extract Typography
- [ ] Get `Font` → `fontFamily`
- [ ] Get `FontSize` → `fontSize`
- [ ] Get `FontWeight` → `fontWeight`
- [ ] Get `TextTransform` → `textTransform` (if specified)
- [ ] Get `Color` → `color`

### Step 3: Extract Alignment (CRITICAL)
- [ ] Get `HorizontalAlign` → `alignItems`
  - Left → `'flex-start'`
  - Center → `'center'`
  - Right → `'flex-end'`
- [ ] Get `VerticalAlign` → `justifyContent`
  - Top → `'flex-start'`
  - Middle → `'center'`
  - Bottom → `'flex-end'`
- [ ] Add `display: 'flex'` and `flexDirection: 'column'`
- [ ] Add matching `textAlign`

### Step 4: Add Metadata
- [ ] Set `tag` to semantic type
- [ ] Set `accepts` array for content types
- [ ] Set `defaultText` for placeholder
- [ ] Set `description` for UI

### Step 5: Verify
- [ ] Update cache-buster in `presentation-viewer.html`
- [ ] Test in browser with DevTools
- [ ] Compare visual output to Template Builder

---

## 8. buildSlotStyle() Reference

The `buildSlotStyle()` function in `style-builder.js` converts slot definitions to inline CSS:

### Input
```javascript
buildSlotStyle('H1-structured', 'title')
```

### Output
```css
grid-row-start: 7; grid-row-end: 10; grid-column-start: 3; grid-column-end: 17;
font-size: 48px; font-weight: bold; font-family: Poppins, sans-serif;
color: #ffffff; display: flex; flex-direction: column;
align-items: flex-start; justify-content: flex-end; text-align: left
```

### Conversion Rules
1. `gridRow: '7/10'` → `grid-row-start: 7; grid-row-end: 10`
2. `gridColumn: '3/17'` → `grid-column-start: 3; grid-column-end: 17`
3. camelCase → kebab-case: `fontSize` → `font-size`

---

## 9. Cache-Busting

After making changes to template files, update the cache-busters in `presentation-viewer.html`:

```html
<script src="/src/templates/template-registry.js?v=YYYYMMDD-fixN"></script>
<script src="/src/renderers/style-builder.js?v=YYYYMMDD-fixN"></script>
<script src="/src/renderers/hero-templates.js?v=YYYYMMDD-fixN"></script>
<script src="/src/renderers/content-templates.js?v=YYYYMMDD-fixN"></script>
<script src="/src/renderers/split-templates.js?v=YYYYMMDD-fixN"></script>
```

Increment the version (e.g., `fix1` → `fix2`) to force browsers to fetch new files.

---

## 10. Quick Reference: H1-structured Example

### Template Builder Specs

| Slot | Property | Value |
|------|----------|-------|
| **Title** | Font | Poppins |
| | FontSize | 48px |
| | FontWeight | Bold |
| | HorizontalAlign | Left |
| | VerticalAlign | Bottom |
| | LeftTopGridPosition | (3, 7) |
| | RightBottomGridPosition | (17, 10) |
| **Subtitle** | Font | Poppins |
| | FontSize | 32px |
| | HorizontalAlign | Left |
| | VerticalAlign | Top |
| | LeftTopGridPosition | (3, 10) |
| | RightBottomGridPosition | (17, 12) |

### Translated to template-registry.js

```javascript
'H1-structured': {
  id: 'H1-structured',
  name: 'Title Slide (Manual)',
  category: 'hero',
  slots: {
    title: {
      gridRow: '7/10',
      gridColumn: '3/17',
      tag: 'title',
      accepts: ['text'],
      style: {
        fontSize: '48px',
        fontWeight: 'bold',
        fontFamily: 'Poppins, sans-serif',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',      // LEFT
        justifyContent: 'flex-end',    // BOTTOM
        textAlign: 'left'
      },
      defaultText: 'Presentation Title',
      description: 'Main presentation title'
    },
    subtitle: {
      gridRow: '10/12',
      gridColumn: '3/17',
      tag: 'subtitle',
      accepts: ['text'],
      style: {
        fontSize: '32px',
        fontFamily: 'Poppins, sans-serif',
        color: '#94a3b8',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',      // LEFT
        justifyContent: 'flex-start',  // TOP
        textAlign: 'left'
      },
      defaultText: 'Presentation Subtitle',
      description: 'Subtitle or tagline'
    }
  }
}
```

---

## 11. Troubleshooting

### Issue: Text appears centered instead of left-aligned

**Check:**
1. Is `alignItems` set to `'flex-start'` (not `'flex-end'`)?
2. Is `flexDirection: 'column'` present?
3. Is `textAlign: 'left'` added?

### Issue: Element not in correct grid position

**Check:**
1. Is `gridColumn` format correct: `'startCol/endCol'`?
2. Is `gridRow` format correct: `'startRow/endRow'`?
3. Is the parent `<section>` element using `display: grid`?

### Issue: Styles not being applied

**Check:**
1. Did you update the cache-buster version?
2. Did you hard-refresh the browser (Cmd+Shift+R)?
3. Use DevTools to inspect the element's inline styles
4. Check browser Network tab to verify new JS files are loaded

### Issue: Font not rendering

**Check:**
1. Is the font loaded in `presentation-viewer.html` via Google Fonts?
2. Is `fontFamily` including a fallback (e.g., `'Poppins, sans-serif'`)?

---

## 12. Files Reference

| File | Purpose |
|------|---------|
| `src/templates/template-registry.js` | Slot definitions and styles |
| `src/renderers/style-builder.js` | Converts slots to inline CSS |
| `src/renderers/hero-templates.js` | Hero template renderers (H1-H3) |
| `src/renderers/content-templates.js` | Content template renderers (C1-C6) |
| `src/renderers/split-templates.js` | Split layout renderers (S1-S4) |
| `src/styles/core/grid-system.css` | 32×18 grid system CSS |
| `viewer/presentation-viewer.html` | Main viewer HTML with script loading |

---

*Last updated: December 4, 2025*
*Version: 1.0*
