# Element Interactions Guide

This document provides comprehensive documentation for interactive debugging features, keyboard shortcuts, and the component-to-element type mapping architecture in the v7.5 layout builder.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Keyboard Shortcuts Reference](#2-keyboard-shortcuts-reference)
3. [Border Toggle Feature ('B' Key)](#3-border-toggle-feature-b-key)
4. [Grid Overlay Feature ('G' Key)](#4-grid-overlay-feature-g-key)
5. [Component-to-Element Type Mapping](#5-component-to-element-type-mapping)
6. [Template Builder Integration](#6-template-builder-integration)
7. [Developer Implementation Guide](#7-developer-implementation-guide)
8. [Recovery Documentation](#8-recovery-documentation)
9. [Best Practices](#9-best-practices)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Overview

The v7.5 layout builder includes powerful interactive debugging and development features:

- **Border Toggle**: Color-coded borders for visual debugging
- **Grid Overlay**: 32×18 grid visualization
- **Edit/Review Modes**: Content editing and AI regeneration
- **Element Types**: Reusable element patterns with drag/resize capabilities

### Target Audience

- **Developers**: Building and debugging templates
- **Template Designers**: Creating new slide layouts
- **QA Engineers**: Verifying layout positioning

### Related Documentation

- `SLIDE_TEMPLATE_TRANSLATION.md` - Grid system and slot definitions
- `ELEMENT_BEST_PRACTICES.md` - Element lifecycle and persistence

---

## 2. Keyboard Shortcuts Reference

### Quick Reference Table

| Key | Function | Handler Function | File Location |
|-----|----------|------------------|---------------|
| **B** | Toggle border highlight | `toggleBorderHighlight()` | `src/core/reveal-config.js:44-48` |
| **G** | Toggle grid overlay | `toggleGridOverlay()` | `src/core/reveal-config.js:24-39` |
| **C** | Toggle controls panel | `toggleControlsPanel()` | `src/core/reveal-config.js:53-60` |
| **H** | Toggle help text | `toggleHelpText()` | `src/core/reveal-config.js:65-72` |
| **R** | Enter review mode | `enterReviewMode()` | `src/utils/review-mode.js` |
| **E** | Toggle edit mode | `toggleEditMode()` | `src/utils/edit-mode.js` |

### Keyboard Binding Implementation

Located in `src/core/reveal-config.js`:

```javascript
keyboard: {
  71: () => { toggleGridOverlay(); },        // 'G' - Toggle grid overlay
  66: () => { toggleBorderHighlight(); },    // 'B' - Toggle border highlight
  67: () => { toggleControlsPanel(); },      // 'C' - Toggle controls panel
  72: () => { toggleHelpText(); },           // 'H' - Toggle help text
}
```

Key codes: G=71, B=66, C=67, H=72

---

## 3. Border Toggle Feature ('B' Key)

### How It Works

1. User presses 'B' key
2. `toggleBorderHighlight()` function executes
3. `show-borders` class is toggled on `document.body`
4. CSS rules activate color-coded outlines on elements
5. Console logs current state: "Border highlight: ON/OFF"

### Handler Implementation

```javascript
// src/core/reveal-config.js (lines 44-48)
function toggleBorderHighlight() {
  document.body.classList.toggle('show-borders');
  const isHighlighted = document.body.classList.contains('show-borders');
  console.log(`Border highlight: ${isHighlighted ? 'ON' : 'OFF'}`);
}
```

### Color Coding System

| Element Type | Color | Hex Code | CSS Selector(s) |
|--------------|-------|----------|-----------------|
| Chart containers | Blue | `#3b82f6` | `.chart-container` |
| Diagram containers | Purple | `#8b5cf6` | `.diagram-container` |
| Image containers | Red | `#ef4444` | `.image-container` |
| Text/Body content | Green | `#10b981` | `.body-primary`, `.text-content`, `.rich-content-area` |
| Title/Subtitle | Light Purple | `#a78bfa` | `.slide-title`, `.subtitle`, `.title-hero`, `.subtitle-hero` |
| Footer/Logo | Yellow | `#fbbf24` | `.footer-presentation-name`, `.footer-company-logo`, `.footer-hero`, `.logo-hero` |
| Hero content areas | Orange | `#f97316` | `.hero-content-area` |
| Inserted textboxes | Orange | `#f59e0b` | `.inserted-textbox` |
| Blank canvas | Pink | `#ec4899` | `.canvas` |
| Background elements | Cyan | `#06b6d4` | `.background-hero` |

### CSS Implementation

Located in `src/styles/core/borders.css` (lines 507-675):

```css
/* Content Area Borders (visible when 'B' pressed) */
body.show-borders .chart-container {
  outline: 2px dotted #3b82f6 !important;
  outline-offset: -2px !important;
}

body.show-borders .diagram-container {
  outline: 2px dotted #8b5cf6 !important;
  outline-offset: -2px !important;
}

/* ... additional rules for each element type */
```

### Why `outline` Instead of `border`?

- `outline` does NOT affect element dimensions
- Prevents layout shifts when toggling
- Uses `outline-offset: -2px` to draw inside the element

### Use Cases

1. **Debugging Layout**: Verify element boundaries match design
2. **Template Development**: Ensure grid positioning is correct
3. **Content Verification**: Check content area dimensions
4. **Troubleshooting**: Identify overlapping or misaligned elements

---

## 4. Grid Overlay Feature ('G' Key)

### How It Works

1. User presses 'G' key
2. `toggleGridOverlay()` creates or removes a grid overlay element
3. Overlay displays the 32×18 grid with numbered lines
4. Helps verify element positioning against grid system

### Grid Specifications

- **Columns**: 32 (numbered 1-32, grid lines 1-33)
- **Rows**: 18 (numbered 1-18, grid lines 1-19)
- **Aspect Ratio**: 16:9 (1920×1080 reference)

### Handler Implementation

```javascript
// src/core/reveal-config.js (lines 24-39)
function toggleGridOverlay() {
  let overlay = document.getElementById('grid-overlay');
  if (overlay) {
    overlay.remove();
    console.log('Grid overlay: OFF');
  } else {
    overlay = createGridOverlay();
    document.body.appendChild(overlay);
    console.log('Grid overlay: ON');
  }
}
```

---

## 5. Component-to-Element Type Mapping

### Element Types Overview

The layout builder has these core **Element Types** defined in `src/utils/element-manager.js`:

| Element Type | File Lines | Drag Handles | Resize Handles | Format Panel |
|--------------|------------|--------------|----------------|--------------|
| TextBox | 1491-1731 | Yes (3×3 dot grid) | Yes (W, E, S, SE) | Yes |
| Image | 721-955 | Yes | Yes | Partial |
| Chart | 347-660 | Yes | Yes | No |
| Infographic | 957-1178 | Yes | Yes | No |
| Diagram | 1180-1489 | Yes | Yes | No |
| Table | 207-345 | Yes | Yes | No |
| Shape | 58-205 | Yes | Yes | No |

### Component → Element Type Mapping

Template slots (components) map to Element Types as follows:

| Component | Element Type | Templates Using | Notes |
|-----------|--------------|-----------------|-------|
| `title` | TextBox | All | Full format panel support |
| `subtitle` | TextBox | Most | Full format panel support |
| `footer` | TextBox | All content | Full format panel support |
| `body` | TextBox | C1, S1-S4 | Text content area |
| `section_number` | TextBox | H2-section | Large number display |
| `contact_info` | TextBox | H3-closing | Contact information |
| `logo` | Image | All | Company logo, supports emoji |
| `background` | Image | H1-H3 | Full-bleed, z-index: 1 |
| `chart` | Chart | C3-chart | Chart.js integration |
| `diagram` | Diagram | C5-diagram | SVG/Mermaid support |
| `infographic` | Infographic | C4-infographic | SVG content |
| `image` | Image | C6-image, S2 | Image placeholder |
| `table` | TextBox | C2-table | HTML table (text-based) |
| `visual` | Visual (composite) | S1, S3 | Chart/Diagram/Infographic/Image |
| `canvas` | Custom | B1-blank | Freeform content |

### Slot Tag Reference

From `src/templates/template-registry.js`:

```javascript
// Tags determine semantic meaning and behavior
tag: 'title',      // Main slide title
tag: 'subtitle',   // Subtitle or tagline
tag: 'body',       // Text content area
tag: 'footer',     // Footer information
tag: 'logo',       // Company logo
tag: 'background', // Background layer
tag: 'chart',      // Chart placeholder
tag: 'diagram',    // Diagram placeholder
tag: 'visual',     // Generic visual (chart/diagram/infographic/image)
```

### Accepts Array Patterns

The `accepts` property defines what content types a slot can receive:

| Pattern | Description | Example Slots |
|---------|-------------|---------------|
| `['text']` | Plain text only | title, subtitle, footer |
| `['text', 'html']` | Text or HTML content | body, content |
| `['image']` | Image URL | logo |
| `['image', 'color', 'gradient']` | Background options | background |
| `['chart']` | Chart.js config | chart |
| `['diagram']` | SVG/Mermaid code | diagram |
| `['chart', 'infographic', 'diagram', 'image']` | Visual elements | visual |
| `['any']` | Unrestricted | B1-blank canvas |

---

## 6. Template Builder Integration

### Relationship Overview

```
┌─────────────────────────────────────────────────────┐
│            TEMPLATE BUILDER (v7.4)                  │
│  Visual Grid Editor → JSON Template Definitions     │
└────────────────────────┬────────────────────────────┘
                         │ Translation
                         ▼
┌─────────────────────────────────────────────────────┐
│           FRONTEND RENDERER (v7.5)                  │
│  template-registry.js → Renderer Functions → HTML   │
└─────────────────────────────────────────────────────┘
```

### Template Builder Output

Templates are stored as JSON in `v7.4-template-builder/storage/templates/`:

```json
{
  "template_id": "h1-structured-edit",
  "elements": [
    {
      "id": "title",
      "type": "text",
      "subtype": "title",
      "inline_styles": {
        "grid-row-start": "7",
        "grid-row-end": "10",
        "font-size": "48px"
      }
    }
  ]
}
```

### Frontend Registry Format

Translated to `src/templates/template-registry.js`:

```javascript
'H1-structured': {
  id: 'H1-structured',
  slots: {
    title: {
      gridRow: '7/10',
      gridColumn: '3/17',
      style: {
        fontSize: '48px',
        fontWeight: 'bold'
      }
    }
  }
}
```

### Translation Guide

See `docs/SLIDE_TEMPLATE_TRANSLATION.md` for:
- Grid position conversion formulas
- Flexbox alignment mapping
- Typography translation
- Color format conversion

---

## 7. Developer Implementation Guide

### Adding New Keyboard Shortcuts

1. Add handler function to `src/core/reveal-config.js`:

```javascript
function toggleYourFeature() {
  document.body.classList.toggle('your-feature-active');
  console.log('Your feature: ' + (active ? 'ON' : 'OFF'));
}

// Make globally available
window.toggleYourFeature = toggleYourFeature;
```

2. Add keyboard binding:

```javascript
keyboard: {
  // ... existing bindings
  XX: () => { toggleYourFeature(); },  // XX = key code
}
```

### Adding Border Colors for New Elements

Add CSS rule to `src/styles/core/borders.css`:

```css
body.show-borders .your-new-element-class {
  outline: 2px dotted #YOUR_HEX_COLOR !important;
  outline-offset: -2px !important;
}
```

### Adding New Element Types

1. Add insertion method to `src/utils/element-manager.js`:

```javascript
insertYourElement(slideIndex, config = {}) {
  const element = document.createElement('div');
  element.className = 'dynamic-element inserted-your-element';
  element.id = `your-element-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  // Add drag handle
  // Add resize handles
  // Add delete button
  // Add type badge

  // Register in elementRegistry
  this.elementRegistry.set(element.id, { /* element data */ });

  return element.id;
}
```

2. Add styles to `src/styles/elements.css`
3. Add border color to `src/styles/core/borders.css`
4. Update `collectElements()` in `src/utils/auto-save.js` if persistence needed

---

## 8. Recovery Documentation

This section provides critical file locations and function names for recovering from IDE crashes.

### Critical Files Summary

| Purpose | File Path |
|---------|-----------|
| Keyboard shortcuts | `src/core/reveal-config.js` |
| Border CSS rules | `src/styles/core/borders.css` |
| Grid overlay CSS | `src/styles/core/grid-system.css` |
| Element Manager | `src/utils/element-manager.js` |
| Template Registry | `src/templates/template-registry.js` |
| Style Builder | `src/renderers/style-builder.js` |
| Hero Renderers | `src/renderers/hero-templates.js` |
| Main Viewer | `viewer/presentation-viewer.html` |
| Auto-save | `src/utils/auto-save.js` |
| Drag-Drop | `src/utils/drag-drop.js` |
| Format API | `src/utils/format-api.js` |
| Edit Mode | `src/utils/edit-mode.js` |

### Key Function Locations

| Function | File | Lines |
|----------|------|-------|
| `toggleBorderHighlight()` | reveal-config.js | 44-48 |
| `toggleGridOverlay()` | reveal-config.js | 24-39 |
| `insertTextBox()` | element-manager.js | 1514-1696 |
| `insertImage()` | element-manager.js | 721-955 |
| `buildSlotStyle()` | style-builder.js | 21-70 |
| `renderH1Structured()` | hero-templates.js | 51-93 |
| `selectElement()` | element-manager.js | 1803-1850 |

### CSS Class Reference

| Class | Purpose | Applied By |
|-------|---------|------------|
| `show-borders` | Enables border highlight | `toggleBorderHighlight()` |
| `dynamic-element` | All inserted elements | ElementManager |
| `inserted-textbox` | Text box elements | `insertTextBox()` |
| `inserted-image` | Image elements | `insertImage()` |
| `element-selected` | Currently selected element | `selectElement()` |
| `slot-convertible` | Slots ready for conversion | Renderer functions |

### PostMessage Events

| Event Type | Direction | Purpose |
|------------|-----------|---------|
| `textBoxSelected` | iframe → parent | Format panel sync |
| `textBoxDeselected` | iframe → parent | Hide format panel |
| `elementSelected` | iframe → parent | Generic element selection |
| `setTextBoxFont` | parent → iframe | Apply font change |

---

## 9. Best Practices

### Template Development Workflow

1. **Design in Template Builder** (v7.4)
   - Use visual grid editor
   - Set positions, fonts, colors
   - Export as JSON

2. **Translate to Frontend**
   - Follow `SLIDE_TEMPLATE_TRANSLATION.md`
   - Update `template-registry.js`
   - Create/update renderer function

3. **Debug with Interactive Features**
   - Press 'B' to verify boundaries
   - Press 'G' to check grid alignment
   - Use DevTools for style inspection

4. **Test Persistence**
   - Make changes in edit mode
   - Refresh page
   - Verify changes persist

### Element Development Guidelines

1. **Always add border color** for new elements
2. **Include drag handle** with 3×3 dot pattern
3. **Include resize handles** (W, E, S, SE minimum)
4. **Register in elementRegistry** for state management
5. **Emit postMessage** for format panel integration
6. **Add to auto-save collection** if persistence needed

### Performance Considerations

- Use `outline` instead of `border` for debug visuals
- Lazy-load elements on non-visible slides
- Debounce auto-save operations
- Minimize DOM queries during drag operations

---

## 10. Troubleshooting

### Border Toggle Not Working

**Symptoms**: Pressing 'B' has no effect

**Solutions**:
1. Check CSS is loaded: Network tab → verify `borders.css` loaded
2. Check handler is bound: Console → type `toggleBorderHighlight` (should show function)
3. Check class toggle: Elements tab → verify `show-borders` class on `<body>`
4. Clear cache: Hard refresh (Cmd+Shift+R)

### Grid Overlay Misaligned

**Symptoms**: Grid lines don't match slide elements

**Solutions**:
1. Verify container dimensions (1920×1080 or 16:9 aspect)
2. Check for CSS transforms affecting positioning
3. Ensure overlay is inside correct parent element

### Keyboard Shortcuts Not Responding

**Symptoms**: Keys don't trigger features

**Solutions**:
1. Click inside slide area first (focus required)
2. Check Reveal.js keyboard config loaded
3. Verify no input field has focus
4. Check for conflicting keyboard handlers

### Format Panel Not Appearing on Element Selection

**Symptoms**: Clicking element doesn't show format panel

**Solutions**:
1. Verify `textBoxSelected` postMessage is sent (Console → filter by 'postMessage')
2. Check parent window message listener is set up
3. Ensure element has correct selection handling
4. Verify edit mode is active

### Element Not Persisting After Refresh

**Symptoms**: Added elements disappear on page reload

**Solutions**:
1. Check element has `dynamic-element` class
2. Verify element type has collector in `auto-save.js`
3. Check auto-save is triggering (Console → 'auto-save' messages)
4. Verify storage backend is receiving data

### Styles Not Applied to Converted Elements

**Symptoms**: Converted slots lose original styling

**Solutions**:
1. Extract computed styles, not just slot definitions
2. Ensure style properties are camelCase in JS, kebab-case in CSS
3. Check for CSS specificity conflicts
4. Verify inline styles are being applied

---

## Appendix: File Structure Reference

```
v7.5-main/
├── src/
│   ├── core/
│   │   └── reveal-config.js      # Keyboard shortcuts, feature toggles
│   ├── templates/
│   │   └── template-registry.js  # Slot definitions
│   ├── renderers/
│   │   ├── style-builder.js      # Slot → CSS conversion
│   │   ├── hero-templates.js     # H1-H3 renderers
│   │   ├── content-templates.js  # C1-C6 renderers
│   │   └── split-templates.js    # S1-S4 renderers
│   ├── styles/
│   │   ├── core/
│   │   │   ├── borders.css       # Border toggle CSS
│   │   │   └── grid-system.css   # Grid overlay CSS
│   │   └── elements.css          # Element styling
│   └── utils/
│       ├── element-manager.js    # Element Type definitions
│       ├── drag-drop.js          # Drag/resize handlers
│       ├── auto-save.js          # Persistence
│       ├── format-api.js         # Text formatting
│       └── edit-mode.js          # Edit/view mode
├── viewer/
│   └── presentation-viewer.html  # Main viewer, postMessage bridge
└── docs/
    ├── SLIDE_TEMPLATE_TRANSLATION.md
    ├── ELEMENT_BEST_PRACTICES.md
    └── ELEMENT_INTERACTIONS.md   # This file
```

---

*Created: December 4, 2025*
*Version: 1.0*
