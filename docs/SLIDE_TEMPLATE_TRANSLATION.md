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

### Typography Scale Reference

Working font sizes validated in actual templates:

| Template | Element | Font Size | Weight | Transform | Notes |
|----------|---------|-----------|--------|-----------|-------|
| H1-structured | title | 48px | bold | none | Poppins, white on dark |
| H1-structured | subtitle | 32px | normal | none | Poppins, muted gray (#94a3b8) |
| H1-structured | footer | 26px | bold | uppercase | Bottom-left positioning |
| H2-section | section_number | 180px | bold | none | Large display number |
| H2-section | title | 48px | bold | none | Section title |
| H3-closing | title | 48px | bold | none | "Thank You" text |
| H3-closing | contact | 24px | normal | none | Contact information |
| C1-text | title | 36px | bold | none | Content slide title |
| C1-text | body | 24px | normal | none | Body text |

**Important**: Template Builder font sizes may need adjustment. During H1 debugging, title was initially 72px but reduced to 48px for proper grid fit.

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

### The `defaultText` Property

The `defaultText` property serves three purposes:

1. **Template Builder Canvas**: Displayed as placeholder text while designing
2. **Content Fallback**: Used when `content.field_name` is empty or missing
3. **Generated Code**: Included in the fallback chain in renderer functions

**In Template Builder:**
```javascript
// Stored in the template JSON
{
  "label": "Title",
  "default_text": "Presentation Title",  // ← This becomes defaultText
  "content_binding": "content.slide_title"
}
```

**In Frontend Registry:**
```javascript
title: {
  // ... other properties
  defaultText: 'Presentation Title',
  description: 'Main presentation title'
}
```

**In Renderer Function:**
```javascript
${content.slide_title || template.slots.title.defaultText || ''}
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

### Common Translation Mistakes (Learned from H1 Debugging)

These mistakes were discovered and fixed during the H1-structured template work:

#### Mistake 1: Grid Width Interpretation

**WRONG**: Interpreting grid as full-width
```javascript
gridColumn: '3/31'   // Spans almost entire slide width
```

**CORRECT**: Title/subtitle typically only span left half
```javascript
gridColumn: '3/17'   // Left half only (leaves room for visual elements)
```

**Lesson**: Check the Template Builder visual carefully. Most text elements don't span the full width.

#### Mistake 2: Font Size Scaling

**WRONG**: Using Template Builder size directly without testing
```javascript
fontSize: '72px'     // Too large for the grid cell
```

**CORRECT**: Adjusted to fit the grid cell
```javascript
fontSize: '48px'     // Proper size for H1 title in its grid area
```

**Lesson**: Always test font sizes visually. The grid cell constrains the visual space.

#### Mistake 3: FlexDirection Property Confusion

When `flexDirection: 'column'` is set, the axis meanings SWAP:

**WRONG** (thinking in terms of row direction):
```javascript
alignItems: 'flex-end',       // ❌ This makes text go RIGHT, not BOTTOM
justifyContent: 'flex-start'  // ❌ This makes text go TOP, not LEFT
```

**CORRECT** (understanding column direction):
```javascript
alignItems: 'flex-start',     // ✓ LEFT (cross-axis in column mode)
justifyContent: 'flex-end'    // ✓ BOTTOM (main-axis in column mode)
```

**Memory Aid**: In `flexDirection: 'column'`:
- `alignItems` = **horizontal** (cross-axis)
- `justifyContent` = **vertical** (main-axis)

#### Mistake 4: Missing Content Field Fallbacks

**WRONG**: Only checking one field name
```javascript
${content.title || ''}
```

**CORRECT**: Checking multiple possible field names
```javascript
${content.slide_title || content.title || template.slots.title.defaultText || ''}
```

**Lesson**: Different content sources use different field names. Always provide fallbacks.

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

## 13. Interactive Debugging Features

### Border Highlight Toggle ('B' Key)

Press **'B'** to toggle color-coded borders around all slide elements. This is essential for debugging layout positioning and verifying element boundaries.

**Implementation:**
- Handler: `toggleBorderHighlight()` in `src/core/reveal-config.js` (lines 44-48)
- CSS: `src/styles/core/borders.css` (lines 507-675)
- Mechanism: Toggles `show-borders` class on `document.body`

### Color Coding System

| Element Type | Border Color | Hex Code | CSS Selector |
|--------------|--------------|----------|--------------|
| Charts | Blue | `#3b82f6` | `.chart-container` |
| Diagrams | Purple | `#8b5cf6` | `.diagram-container` |
| Images | Red | `#ef4444` | `.image-container` |
| Text/Body | Green | `#10b981` | `.body-primary`, `.text-content` |
| Title/Subtitle | Light Purple | `#a78bfa` | `.title-hero`, `.subtitle-hero` |
| Footer/Logo | Yellow | `#fbbf24` | `.footer-hero`, `.logo-hero` |
| Hero Areas | Orange | `#f97316` | `.hero-content-area` |
| Inserted Textboxes | Orange | `#f59e0b` | `.inserted-textbox` |
| Blank Canvas | Pink | `#ec4899` | `.canvas` |

### Other Keyboard Shortcuts

| Key | Function | Implementation |
|-----|----------|----------------|
| **B** | Toggle border highlight | `reveal-config.js:44-48` |
| **G** | Toggle grid overlay (32×18) | `reveal-config.js:24-39` |
| **C** | Toggle controls panel | `reveal-config.js:53-60` |
| **H** | Toggle help text | `reveal-config.js:65-72` |
| **R** | Review mode (AI regeneration) | `review-mode.js` |
| **E** | Toggle edit mode | `edit-mode.js` |

### Adding Border Support for New Elements

When adding new template slots or element types, add corresponding CSS rules:

```css
/* In borders.css, add: */
body.show-borders .your-new-element {
  outline: 2px dotted #YOUR_COLOR !important;
  outline-offset: -2px !important;
}
```

**Note**: Use `outline` instead of `border` to avoid affecting layout dimensions.

**Full documentation**: See `docs/ELEMENT_INTERACTIONS.md`

---

## 14. Slot Editability Attributes

For slots to be editable in the frontend, they must include specific HTML attributes. These enable the editing system to identify, select, and modify slot content.

### Required Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `class="slot-convertible"` | Marks the slot as convertible to editable element | `class="slot-convertible title-hero"` |
| `id` | Unique identifier for the slot | `id="slide-0-slot-title"` |
| `data-slot-type` | Semantic type of the slot | `data-slot-type="title"` |
| `data-editable` | Enables editing mode | `data-editable="true"` |
| `data-element-target` | Target element type for conversion | `data-element-target="textbox"` |
| `data-section-id` | Section identifier | `data-section-id="slide-0-section-title"` |
| `data-slide-index` | Index of the slide | `data-slide-index="0"` |

### Example Slot HTML

```html
<div class="slot-convertible title-hero"
     id="slide-${slideIndex}-slot-title"
     data-slot-type="title"
     data-section-id="slide-${slideIndex}-section-title"
     data-section-type="title"
     data-slide-index="${slideIndex}"
     data-editable="true"
     data-element-target="textbox"
     style="${buildSlotStyle('H1-structured', 'title')}">
  ${content.slide_title || 'Presentation Title'}
</div>
```

### Element Target Types

| Target | Use For |
|--------|---------|
| `textbox` | Text content (title, subtitle, body, footer) |
| `image` | Image slots |
| `chart` | Chart containers |
| `diagram` | Diagram containers |
| `background` | Background layers |

---

## 15. Content Field Binding Patterns

Different content sources (Director Agent, Text Service, user input) use different field names. Always implement a fallback chain.

### Field Name Reference

| Slot Type | Primary Field | Fallback Fields | Example |
|-----------|--------------|-----------------|---------|
| title | `slide_title` | `title`, `heading` | `${content.slide_title \|\| content.title \|\| ''}` |
| subtitle | `subtitle` | `tagline`, `subheading` | `${content.subtitle \|\| content.tagline \|\| ''}` |
| body | `rich_content` | `body_text`, `content` | `${content.rich_content \|\| content.body_text \|\| ''}` |
| footer | `presentation_name` | `footer_text`, `footer` | `${content.presentation_name \|\| content.footer_text \|\| ''}` |
| logo | `company_logo` | `logo`, `brand_logo` | `${content.company_logo \|\| ''}` |
| section_number | `section_number` | `number` | `${content.section_number \|\| '01'}` |
| contact | `contact_info` | `contact`, `email` | `${content.contact_info \|\| ''}` |

### Complete Fallback Pattern

```javascript
// In renderer function:
const title = content.slide_title
  || content.title
  || template.slots.title.defaultText
  || 'Untitled';
```

### Why Multiple Field Names?

- **Director Agent**: Uses `slide_title`, `section_number`
- **Text Service**: Uses `rich_content`, `formatted_text`
- **User Input**: May use simplified names like `title`, `body`
- **Legacy Data**: May have older field naming conventions

---

## 16. Helper Functions Reference

The `style-builder.js` file provides utility functions for consistent style generation.

### `buildSlotStyle(templateId, slotName)`

Converts a slot definition from `template-registry.js` to inline CSS.

**Input:**
```javascript
buildSlotStyle('H1-structured', 'title')
```

**Output:**
```css
grid-row-start: 7; grid-row-end: 10; grid-column-start: 3; grid-column-end: 17;
font-size: 48px; font-weight: bold; font-family: Poppins, sans-serif;
color: #ffffff; display: flex; flex-direction: column;
align-items: flex-start; justify-content: flex-end; text-align: left
```

**Conversion Rules:**
1. `gridRow: '7/10'` → `grid-row-start: 7; grid-row-end: 10`
2. `gridColumn: '3/17'` → `grid-column-start: 3; grid-column-end: 17`
3. camelCase → kebab-case: `fontSize` → `font-size`

### `buildSlotAttributes(templateId, slotName, slideIndex)`

Generates data attributes for slot editability.

**Input:**
```javascript
buildSlotAttributes('H1-structured', 'title', 0)
```

**Output:**
```html
data-slot-type="title" data-section-id="slide-0-section-title"
data-section-type="title" data-slide-index="0" data-editable="true"
```

### `buildBackgroundStyle(slide, content)`

Generates background CSS with proper fallbacks.

**Input:**
```javascript
buildBackgroundStyle(slide, content)
```

**Logic:**
```javascript
// Priority: slide settings > content settings > default
const bgImage = slide?.background_image || content?.background_image;
const bgColor = slide?.background_color || content?.background_color || '#1e3a5f';

if (bgImage) {
  return `background-image: url('${bgImage}'); background-size: cover; background-position: center;`;
}
return `background-color: ${bgColor};`;
```

### `getTemplateDefaultBackground(templateId)`

Returns default background color by template type.

| Template Type | Default Color |
|---------------|---------------|
| Hero (H1, H2, H3) | `#1e3a5f` (dark blue) |
| Content (C1-C6) | `#ffffff` (white) |
| Split (S1-S4) | `#ffffff` (white) |
| Blank (B1) | `#ffffff` (white) |

---

## 17. Background Layer Handling

Background elements require special handling to appear behind content.

### Z-Index Requirements

```javascript
// In slot style definition:
background: {
  gridRow: '1/19',
  gridColumn: '1/33',
  style: {
    zIndex: -1,  // CRITICAL: Must be negative to stay behind content
    // ... other styles
  }
}
```

### Image Cover Pattern

For background images that should fill the slot:

```html
<div class="background-layer" style="z-index: -1; ...">
  <img src="${content.background_image}"
       style="width: 100%; height: 100%; object-fit: cover; object-position: center;"
       alt="">
</div>
```

### Conditional Background Rendering

```javascript
// Only render background div if image exists
${content.background_image ? `
  <div class="background-layer" style="${buildSlotStyle(templateId, 'background')}">
    <img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">
  </div>
` : ''}
```

### Background Style Cascade

Priority order for background styles:
1. `slide.background_image` / `slide.background_color` (slide-specific)
2. `content.background_image` / `content.background_color` (content-provided)
3. Template default (from `getTemplateDefaultBackground()`)

---

## 18. Import/Edit/Republish Workflow

Templates can flow bidirectionally between v7.4 Template Builder and v7.5 Frontend.

### Workflow Diagram

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   v7.5 Frontend     │     │  v7.4 Template      │     │   v7.5 Frontend     │
│   (Production)      │────▶│     Builder         │────▶│   (Updated)         │
│                     │     │                     │     │                     │
│  hero-templates.js  │     │  Edit in canvas     │     │  hero-templates.js  │
│  template-registry  │     │  Modify properties  │     │  template-registry  │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
        │                           │                           │
        ▼                           ▼                           ▼
   v75_renderer_parser.py    v75_code_generator.py      Test & Deploy
```

### Step 1: Import Existing Template

```bash
# The parser reads v7.5 JS files and creates Template objects
python -c "
from v75_renderer_parser import V75RendererParser
parser = V75RendererParser()
templates = parser.parse_multi_renderer_file('v7.5-main/src/renderers/hero-templates.js')
print(templates.keys())  # ['H1-generated', 'H1-structured', 'H2-section', 'H3-closing']
"
```

### Step 2: Edit in Template Builder

1. Open Template Builder (`v7.4-template-builder/frontend/builder.html`)
2. Load the imported template
3. Modify grid positions, fonts, colors, alignment
4. Save changes

### Step 3: Generate Updated Code

```bash
# The generator creates new JS code from Template objects
python -c "
from v75_code_generator import V75CodeGenerator
gen = V75CodeGenerator()
# Generate renderer function
renderer_code = gen.generate_frontend_renderer('H1-structured', ...)
# Generate registry entry
registry_code = gen.generate_registry_entry('H1-structured', ...)
"
```

### Step 4: Publish to v7.5

1. Copy generated renderer function to appropriate file (`hero-templates.js`)
2. Copy registry entry to `template-registry.js`
3. Update cache-buster version in `presentation-viewer.html`

### Step 5: Verify

1. Hard refresh browser (Cmd+Shift+R)
2. Press 'B' to toggle border highlights
3. Check DevTools for correct inline styles
4. Test with actual content

---

## 19. Template Rollout Guide

After perfecting one template (like H1-structured), apply the same patterns to others.

### Template Type Reference

| Category | Templates | Key Characteristics |
|----------|-----------|---------------------|
| **Hero** | H1-structured, H1-generated, H2-section, H3-closing | Dark backgrounds, large text, centered/left layouts |
| **Content** | C1-text, C2-table, C3-chart, C4-infographic, C5-diagram, C6-image | Light backgrounds, content focus, format ownership |
| **Split** | S1-visual-text, S2-image-content, S3-two-visuals, S4-comparison | Two-column layouts, asymmetric grids |
| **Blank** | B1-blank | Minimal styling, canvas for custom content |

### Rollout Checklist Per Template

Use this checklist when translating each template:

#### Grid & Position
- [ ] Extract all slot grid positions from Template Builder
- [ ] Verify left/right width interpretation (full width vs. half width)
- [ ] Check for overlapping grid areas

#### Typography
- [ ] Map font family with fallback (`'Poppins, sans-serif'`)
- [ ] Verify font size fits grid cell (adjust if needed)
- [ ] Set font weight (bold/normal)
- [ ] Set text-transform if applicable (uppercase/capitalize/none)

#### Alignment (CRITICAL)
- [ ] Add `display: 'flex'` and `flexDirection: 'column'`
- [ ] Map HorizontalAlign → `alignItems` (flex-start/center/flex-end)
- [ ] Map VerticalAlign → `justifyContent` (flex-start/center/flex-end)
- [ ] Add matching `textAlign`

#### Colors
- [ ] Set text color with theme awareness
- [ ] Set background with proper fallbacks
- [ ] Use `zIndex: -1` for background layers

#### Editability
- [ ] Add `slot-convertible` class
- [ ] Add all required data attributes (see Section 14)
- [ ] Set appropriate `data-element-target`

#### Content Binding
- [ ] Implement field fallback chain (see Section 15)
- [ ] Include `defaultText` in fallback
- [ ] Test with empty content

#### Verification
- [ ] Update cache-buster version
- [ ] Test with 'B' key border toggle
- [ ] Test with different content lengths
- [ ] Test in edit mode ('E' key)
- [ ] Verify in DevTools

### Category-Specific Guidance

#### Hero Templates (H1, H2, H3)

```javascript
// Common patterns for hero templates:
style: {
  // Dark background default
  backgroundColor: '#1e3a5f',

  // Large, bold titles
  fontSize: '48px',
  fontWeight: 'bold',
  color: '#ffffff',

  // Bottom-left alignment is common
  alignItems: 'flex-start',
  justifyContent: 'flex-end'
}
```

**H2-section specifics:**
- Large section number (180px) positioned separately
- Title below section number

**H3-closing specifics:**
- "Thank You" or closing message
- Contact information slot
- May have call-to-action

#### Content Templates (C1-C6)

```javascript
// Common patterns for content templates:
style: {
  // Light background
  backgroundColor: '#ffffff',

  // Smaller fonts
  fontSize: '24px',
  color: '#1f2937',

  // Top-left alignment is common
  alignItems: 'flex-start',
  justifyContent: 'flex-start'
}
```

**Format Ownership:**
- Text slots: `format_ownership: 'text_service'` for AI-generated rich content
- Visual slots: `format_ownership: 'layout_builder'` for simple binding

#### Split Templates (S1-S4)

```javascript
// Grid typically divided:
left_content: {
  gridColumn: '2/17',  // Left ~50%
  gridRow: '2/18'
},
right_content: {
  gridColumn: '17/32', // Right ~50%
  gridRow: '2/18'
}
```

**Considerations:**
- May need asymmetric padding between columns
- Visual side typically has no text styling
- Text side inherits content template patterns

### Quick Start: Cloning H1 Patterns

When starting a new template, copy the H1-structured pattern:

1. **Copy the slot structure** from `template-registry.js`
2. **Adjust grid positions** for the new layout
3. **Keep the same flexbox pattern** (display, flexDirection, alignItems, justifyContent)
4. **Modify typography** (fontSize, fontWeight, fontFamily)
5. **Add template-specific slots** (section_number, contact_info, etc.)
6. **Update the renderer function** in the appropriate file
7. **Test thoroughly** with border toggle and DevTools

---

## 20. CSS Override Requirements for Slot Conversion

When slots are converted to Element Types (via `slot-converter.js`), CSS stylesheet rules can override JavaScript inline styles. This section documents the CSS `!important` rules required in `slot-converter.css` to ensure template properties are preserved.

### The Problem

The slot conversion pipeline is:
```
template-registry.js → slot-converter.js → element-manager.js → DOM Element
```

However, CSS stylesheets like `textbox.css` apply default styles that can override the inline styles set by JavaScript:

```css
/* textbox.css - these override inline styles! */
.textbox-content {
  min-height: 100%;   /* Defeats justify-content alignment */
  color: #374151;     /* Dark text - wrong for hero slides */
}
```

### Required CSS Rules in slot-converter.css

#### 1. Flexbox Layout for Converted Slots

```css
.inserted-textbox.converted-slot {
  display: flex !important;
  flex-direction: column !important;
}
```

#### 2. Slot-Specific Vertical Alignment

```css
/* Title needs bottom alignment */
.converted-slot.slot-title {
  justify-content: flex-end !important;
}

/* Subtitle and footer need top alignment */
.converted-slot.slot-subtitle,
.converted-slot.slot-footer {
  justify-content: flex-start !important;
}
```

#### 3. Content Div Height Override

```css
.inserted-textbox.converted-slot .textbox-content {
  min-height: auto !important;  /* Allow flexbox positioning */
  height: auto !important;
}
```

#### 4. Hero Slide Color Scheme (Dark Background)

```css
/* White text for hero slides (dark backgrounds) */
.hero-slide .inserted-textbox.converted-slot .textbox-content {
  color: #ffffff !important;
}

/* Subtitle gets muted color */
.hero-slide .converted-slot.slot-subtitle .textbox-content {
  color: #94a3b8 !important;
}
```

### When to Use `!important`

Use `!important` in `slot-converter.css` when:

| Scenario | Example | Reason |
|----------|---------|--------|
| Alignment properties | `justify-content: flex-end !important` | Overrides element-manager defaults |
| Color on hero slides | `color: #ffffff !important` | Overrides textbox.css dark default |
| Height constraints | `min-height: auto !important` | Allows flex alignment to work |

**Do NOT use `!important`** for properties that should be customizable by users (e.g., font-size, font-family when user can change them).

---

## 21. Hero vs Content Slide Color Schemes

Templates fall into two categories with different default color schemes.

### Hero Slides (H1, H2, H3)

| Property | Value | Reason |
|----------|-------|--------|
| Background | Dark (`#1e3a5f`, `#1f2937`) | Visual impact, supports background images |
| Title color | White (`#ffffff`) | Contrast on dark background |
| Subtitle color | Muted gray (`#94a3b8`) | Visible but secondary |
| Footer color | White (`#ffffff`) | Readable on dark background |

**CSS Implementation:**
```css
.hero-slide .inserted-textbox.converted-slot .textbox-content {
  color: #ffffff !important;
}

.hero-slide .converted-slot.slot-subtitle .textbox-content {
  color: #94a3b8 !important;
}
```

### Content Slides (C1-C6) and Split Slides (S1-S4)

| Property | Value | Reason |
|----------|-------|--------|
| Background | White (`#ffffff`) | Clean, readable |
| Title color | Dark gray (`#1f2937`) | Readable on light background |
| Body color | Medium gray (`#374151`) | Slightly lighter for body text |
| Footer color | Dark gray (`#1f2937`) | Consistent with title |

**CSS Implementation:**
```css
/* Content slides use dark text by default - no override needed */
/* The textbox.css default color: #374151 works correctly */

/* OR explicitly set for clarity: */
.content-slide .inserted-textbox.converted-slot .textbox-content {
  color: #1f2937 !important;
}
```

### Slide Category Detection

The slide's parent `<section>` element should have a category class:

```html
<!-- Hero slide -->
<section class="hero-slide" data-template="H1-structured">

<!-- Content slide -->
<section class="content-slide" data-template="C1-text">

<!-- Split slide -->
<section class="content-slide" data-template="S1-visual-text">
```

Alternatively, check template prefix:
- `H*` templates → hero-slide
- `C*` templates → content-slide
- `S*` templates → content-slide (typically light background)
- `B*` templates → content-slide (blank canvas)

---

## 22. Default Text (defaultText) Property

The `defaultText` property in `template-registry.js` serves as placeholder text shown when no content is provided.

### Source of defaultText

From Template Builder v7.4:

| Template Builder Field | Registry Property |
|----------------------|-------------------|
| `default_text` | `defaultText` |
| `label` (fallback) | Used if default_text empty |

### defaultText by Slot Type

| Slot | Typical defaultText | Purpose |
|------|---------------------|---------|
| `title` | `'Presentation Title'` | Shows placeholder for main title |
| `subtitle` | `'Your tagline or subtitle here'` | Describes purpose |
| `footer` | `'AUTHOR \| DATE'` | Format hint |
| `section_number` | `'01'` | Default numbering |
| `body` | `null` or empty | Body typically requires content |
| `logo` | `'Logo'` | Placeholder text |
| `contact_info` | `null` | Often empty |

### Using defaultText in Renderers

```javascript
// In renderer function:
const title = content.slide_title
  || content.title
  || template.slots.title.defaultText  // ← Uses defaultText as fallback
  || '';
```

### Using defaultText in Slot Converter

The `slot-converter.js` uses `defaultText` when creating TextBox elements:

```javascript
// In buildTextBoxConfigFromSlot():
return {
  // ...
  placeholder: slotDef.defaultText || `Enter ${slotName}...`,
  // ...
};

// In convertToTextBox():
const content = rawContent || slotDef.defaultText || '';
```

### Best Practice: Always Include defaultText

Every text slot should have a `defaultText` value:

```javascript
title: {
  gridRow: '7/10',
  gridColumn: '3/17',
  tag: 'title',
  accepts: ['text'],
  style: { /* ... */ },
  defaultText: 'Presentation Title',  // ← REQUIRED
  description: 'Main presentation title'
}
```

---

## 23. Complete Slot Definition Checklist

When adding or updating a slot in `template-registry.js`, ensure ALL properties are present:

### Required Properties

| Property | Required | Example |
|----------|----------|---------|
| `gridRow` | ✅ | `'7/10'` |
| `gridColumn` | ✅ | `'3/17'` |
| `tag` | ✅ | `'title'`, `'subtitle'`, `'body'`, `'footer'`, `'logo'`, `'background'` |
| `accepts` | ✅ | `['text']`, `['image']`, `['text', 'html']` |
| `style` | ✅ | `{ /* see below */ }` |
| `defaultText` | ✅ (for text) | `'Presentation Title'` |
| `description` | Recommended | `'Main presentation title'` |

### Required Style Properties

For TEXT slots (`tag: 'title'`, `'subtitle'`, `'body'`, `'footer'`):

```javascript
style: {
  // Typography (REQUIRED)
  fontSize: '48px',
  fontWeight: 'bold',
  fontFamily: 'Poppins, sans-serif',

  // Color (REQUIRED)
  color: '#ffffff',  // or '#1f2937' for content slides

  // Flexbox Alignment (REQUIRED)
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'flex-start',      // Horizontal: left/center/right
  justifyContent: 'flex-end',    // Vertical: top/center/bottom
  textAlign: 'left',

  // Optional
  textTransform: 'uppercase',    // If needed
  padding: '20px'                // If needed
}
```

For IMAGE/BACKGROUND slots (`tag: 'logo'`, `'background'`):

```javascript
style: {
  zIndex: -1,  // For background (behind content)
  // or zIndex: 1013 for logo (above content)
}
```

### Example: Complete Footer Slot

```javascript
footer: {
  gridRow: '16/18',
  gridColumn: '3/17',
  tag: 'footer',
  accepts: ['text'],
  style: {
    fontSize: '26px',
    fontWeight: 'bold',
    fontFamily: 'Poppins, sans-serif',
    color: '#ffffff',              // White for hero, #1f2937 for content
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',      // LEFT
    justifyContent: 'flex-start',  // TOP
    textAlign: 'left',
    textTransform: 'uppercase'
  },
  defaultText: 'AUTHOR | DATE',
  description: 'Date, presenter name, or other info'
}
```

---

## 24. Template Implementation Order

When rolling out template fixes, follow this recommended order:

### Phase 1: Hero Templates (Dark Background)
1. ✅ **H1-structured** - Title Slide (Manual) - COMPLETED
2. **H1-generated** - Title Slide (AI Generated)
3. **H2-section** - Section Divider
4. **H3-closing** - Closing Slide

**Common Hero Patterns:**
- Background: dark (#1e3a5f)
- Text: white (#ffffff)
- Subtitle: muted (#94a3b8)
- CSS class: `.hero-slide`

### Phase 2: Content Templates (Light Background)
5. **C1-text** - Text Content
6. **C2-table** - Table Slide
7. **C3-chart** - Single Chart
8. **C4-infographic** - Single Infographic
9. **C5-diagram** - Single Diagram
10. **C6-image** - Single Image

**Common Content Patterns:**
- Background: white (#ffffff)
- Title: dark (#1f2937)
- Body: medium gray (#374151)
- CSS class: `.content-slide`

### Phase 3: Split Templates (Light Background)
11. **S1-visual-text** - Visual + Text
12. **S2-image-content** - Image + Content
13. **S3-two-visuals** - Two Visuals
14. **S4-comparison** - Comparison

**Common Split Patterns:**
- Same as Content templates
- Two distinct grid regions
- May have asymmetric styling

### Phase 4: Blank Template
15. **B1-blank** - Blank Canvas

**Blank Pattern:**
- Minimal styling
- User-customizable

---

*Last updated: December 4, 2025*
*Version: 1.3*
