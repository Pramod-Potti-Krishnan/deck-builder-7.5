# Frontend Integration Guide - v7.5-main Presentation Viewer

**Date**: January 18, 2025
**Version**: 7.5.1
**Purpose**: Guide for embedding reveal.js presentations in frontend applications

---

## Overview

The v7.5-main presentation viewer is designed to be embedded in frontend applications via iframe. All UI controls (edit mode, overview mode, navigation) can be triggered programmatically from the parent window, eliminating the need for visible overlay buttons.

---

## Quick Start

### 1. Embed the Presentation

```html
<iframe
  id="presentation-iframe"
  src="https://web-production-f0d13.up.railway.app/p/YOUR_PRESENTATION_ID"
  width="100%"
  height="100%"
  frameborder="0"
  allow="fullscreen"
></iframe>
```

### 2. Access the Iframe Window

```javascript
const iframe = document.getElementById('presentation-iframe');
const iframeWindow = iframe.contentWindow;

// Wait for iframe to load
iframe.addEventListener('load', () => {
  console.log('Presentation loaded and ready');
  // Now you can call functions
});
```

---

## Available Functions

All functions are exposed on the iframe's `window` object and can be called from the parent window.

### Edit Mode Functions

#### Toggle Edit Mode
```javascript
// Toggle edit mode on/off
iframeWindow.toggleEditMode();

// Check if currently in edit mode
const isEditing = iframeWindow.document.body.getAttribute('data-mode') === 'edit';
```

#### Save Changes
```javascript
// Save all edits made in edit mode
iframeWindow.saveAllChanges();
```

#### Cancel Edits
```javascript
// Cancel edits and revert to original content
iframeWindow.cancelEdits();
```

#### Show Version History
```javascript
// Open version history modal
iframeWindow.showVersionHistory();
```

### Navigation Functions

#### Next/Previous Slide
```javascript
// Next slide
iframeWindow.Reveal.next();

// Previous slide
iframeWindow.Reveal.prev();

// Navigate to specific slide (1-based index)
iframeWindow.goToSlide(5);
```

#### Get Current Slide Info
```javascript
const slideInfo = iframeWindow.getCurrentSlideInfo();
console.log(slideInfo);
// {
//   index: 3,
//   total: 10,
//   element: <section>,
//   layoutId: "L02"
// }
```

### Overview Mode (Grid View)

#### Toggle Overview Mode
```javascript
// Toggle overview mode (grid view of all slides)
iframeWindow.toggleOverview();

// Check if in overview mode
const isOverview = iframeWindow.isOverviewActive();
```

**Use Case**: Show thumbnail grid at bottom of screen as navigator
```javascript
// Frontend button to show slide navigator
document.getElementById('show-navigator-btn').addEventListener('click', () => {
  iframeWindow.toggleOverview();
});
```

### Debug Functions

#### Grid Overlay (for developers)
```javascript
// Toggle grid overlay to verify layout alignment
iframeWindow.toggleGridOverlay();
```

#### Border Highlighting
```javascript
// Highlight all element borders for debugging
iframeWindow.toggleBorderHighlight();
```

---

## UI Control

### Hide All Edit UI (Default Behavior)

By default (as of v7.5.1), all edit UI elements are hidden:
- ✅ Edit mode button - hidden
- ✅ Edit controls panel - hidden
- ✅ Keyboard shortcuts panel - hidden
- ✅ Navigation arrows - **visible and clickable**

### Optional: Show Edit UI

If you want to enable the built-in edit UI:

```javascript
// Enable edit UI
iframeWindow.document.body.setAttribute('data-show-edit-ui', 'true');

// Disable edit UI
iframeWindow.document.body.setAttribute('data-show-edit-ui', 'false');
```

---

## Complete Example: Custom Frontend Controls

```html
<!DOCTYPE html>
<html>
<head>
  <title>Presentation Viewer</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      font-family: system-ui, sans-serif;
    }

    #presentation-container {
      width: 100vw;
      height: calc(100vh - 80px);
    }

    #presentation-iframe {
      width: 100%;
      height: 100%;
      border: none;
    }

    #controls {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      height: 80px;
      background: #1f2937;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      padding: 0 20px;
    }

    button {
      padding: 12px 24px;
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }

    button:hover {
      background: #2563eb;
      transform: translateY(-2px);
    }

    #slide-info {
      color: white;
      font-size: 14px;
      margin-left: auto;
    }
  </style>
</head>
<body>
  <div id="presentation-container">
    <iframe
      id="presentation-iframe"
      src="https://web-production-f0d13.up.railway.app/p/YOUR_PRESENTATION_ID"
    ></iframe>
  </div>

  <div id="controls">
    <button id="prev-btn">⬅️ Previous</button>
    <button id="next-btn">Next ➡️</button>
    <button id="overview-btn">📊 Overview</button>
    <button id="edit-btn">✏️ Edit</button>
    <button id="save-btn" style="display: none;">💾 Save</button>
    <div id="slide-info">Slide 1 / 10</div>
  </div>

  <script>
    const iframe = document.getElementById('presentation-iframe');
    let iframeWindow = null;

    // Wait for iframe to load
    iframe.addEventListener('load', () => {
      iframeWindow = iframe.contentWindow;
      console.log('✅ Presentation loaded');

      // Update slide info
      updateSlideInfo();
    });

    // Previous slide
    document.getElementById('prev-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.Reveal.prev();
        updateSlideInfo();
      }
    });

    // Next slide
    document.getElementById('next-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.Reveal.next();
        updateSlideInfo();
      }
    });

    // Toggle overview mode
    document.getElementById('overview-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.toggleOverview();
      }
    });

    // Toggle edit mode
    document.getElementById('edit-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.toggleEditMode();

        // Show/hide save button
        const isEditing = iframeWindow.document.body.getAttribute('data-mode') === 'edit';
        document.getElementById('save-btn').style.display = isEditing ? 'block' : 'none';
        document.getElementById('edit-btn').textContent = isEditing ? '❌ Cancel' : '✏️ Edit';
      }
    });

    // Save edits
    document.getElementById('save-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.saveAllChanges();
        document.getElementById('save-btn').style.display = 'none';
        document.getElementById('edit-btn').textContent = '✏️ Edit';
      }
    });

    // Update slide info
    function updateSlideInfo() {
      if (iframeWindow && iframeWindow.getCurrentSlideInfo) {
        const info = iframeWindow.getCurrentSlideInfo();
        document.getElementById('slide-info').textContent =
          `Slide ${info.index} / ${info.total}`;
      }
    }

    // Listen for slide changes in iframe
    setInterval(() => {
      if (iframeWindow) {
        updateSlideInfo();
      }
    }, 500);
  </script>
</body>
</html>
```

---

## Keyboard Shortcuts

The presentation viewer has built-in keyboard shortcuts:

| Key | Action |
|-----|--------|
| **Arrow Left/Right** | Previous/Next slide |
| **Arrow Up/Down** | Previous/Next slide |
| **ESC** | Toggle overview mode |
| **E** | Toggle edit mode |
| **Ctrl+S** | Save changes (in edit mode) |
| **G** | Toggle grid overlay (debug) |
| **B** | Toggle border highlighting (debug) |
| **H** | Toggle help text |

**Note**: These work when the iframe is focused. You can disable them or override with parent window handlers if needed.

---

## Troubleshooting

### Navigation Arrows Not Clickable

**Fixed in v7.5.1**: The keyboard shortcuts panel was blocking clicks with `z-index`. Now uses `pointer-events: none` to allow clicks through.

**Verify Fix**:
```javascript
// Check shortcuts panel CSS
const shortcuts = iframeWindow.document.querySelector('.edit-shortcuts');
console.log(getComputedStyle(shortcuts).pointerEvents); // Should be "none"
```

### Edit Button Still Visible

**Fixed in v7.5.1**: Edit UI is hidden by default. If you still see it:

```javascript
// Force hide edit UI
iframeWindow.document.body.setAttribute('data-show-edit-ui', 'false');
```

### Overview Mode Not Working

**Verify Reveal.js is loaded**:
```javascript
console.log(typeof iframeWindow.Reveal); // Should be "object"
console.log(typeof iframeWindow.toggleOverview); // Should be "function"
```

### Cross-Origin Issues

If embedding from a different domain, ensure CORS headers are set:
```
Access-Control-Allow-Origin: *
X-Frame-Options: ALLOWALL
```

---

## API Reference

### Edit Mode API

```typescript
interface EditModeAPI {
  toggleEditMode(): void;
  saveAllChanges(): Promise<void>;
  cancelEdits(): void;
  showVersionHistory(): void;
}
```

### Navigation API

```typescript
interface NavigationAPI {
  goToSlide(index: number): void;
  getCurrentSlideInfo(): {
    index: number;
    total: number;
    element: HTMLElement;
    layoutId: string;
  };
}

// Reveal.js native API
interface RevealAPI {
  next(): void;
  prev(): void;
  slide(h: number, v?: number): void;
  getTotalSlides(): number;
  getCurrentSlide(): HTMLElement;
  getIndices(): { h: number; v: number };
}
```

### Overview Mode API

```typescript
interface OverviewAPI {
  toggleOverview(): void;
  isOverviewActive(): boolean;
}
```

---

## Director Service Integration - Background Fields (NEW)

**NEW FEATURE**: All slides now support `background_color` and `background_image` fields.

### API Schema Updates

When the Director Service sends presentation data to the Layout Builder, it can now include optional background fields:

```typescript
interface Slide {
  layout: "L01" | "L02" | "L03" | "L25" | "L27" | "L29";
  content: object;  // Layout-specific content
  background_color?: string;   // NEW: Hex color (e.g., "#f0f9ff")
  background_image?: string;   // NEW: URL or data URI
}
```

### Usage Examples for Director Service

#### Example 1: Title Slide with Background Image

```javascript
{
  "layout": "L29",
  "background_image": "https://cdn.example.com/hero-image.jpg",
  "background_color": "#1a1a2e",  // Fallback if image fails
  "content": {
    "hero_content": "<div style='color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);'>Welcome to Our Presentation</div>"
  }
}
```

#### Example 2: Content Slide with Brand Color Background

```javascript
{
  "layout": "L25",
  "background_color": "#f0f9ff",  // Light blue brand color
  "content": {
    "slide_title": "Market Analysis",
    "subtitle": "Q4 2024 Results",
    "rich_content": "<div>Your content here</div>"
  }
}
```

#### Example 3: Slide without Background (Backward Compatible)

```javascript
{
  "layout": "L25",
  // No background fields - defaults to white
  "content": {
    "slide_title": "Standard Slide",
    "rich_content": "<div>Content</div>"
  }
}
```

### Background Field Specifications

| Field | Type | Format | Required | Default |
|-------|------|--------|----------|---------|
| `background_color` | string | Hex (#RRGGBB) | No | None (white) |
| `background_image` | string | URL or data URI | No | None |

### Priority and Behavior

1. **Both provided**: Image displays, color acts as fallback
2. **Color only**: Solid color background
3. **Image only**: Image with white fallback
4. **Neither**: Default white background

### Director Service Decision Logic

Recommended logic for when Director Service should add backgrounds:

```python
def should_add_background(slide_type, layout, theme):
    """
    Determine if and what background to add based on slide context.
    """
    # Hero/Title slides - use impactful images
    if layout == "L29" and slide_type in ["title", "section_divider", "ending"]:
        return {
            "background_image": theme.get_hero_image(),
            "background_color": theme.primary_color  # Fallback
        }

    # Analytics slides - subtle branded color
    elif layout in ["L01", "L02", "L03"] and theme.brand_colors_enabled:
        return {
            "background_color": theme.light_accent_color  # e.g., #f0f9ff
        }

    # Text-heavy slides - optional light tint
    elif layout == "L25" and theme.use_backgrounds:
        return {
            "background_color": theme.subtle_background  # e.g., #f8f9fa
        }

    # Default: no background
    else:
        return {}
```

### Validation Rules

The Layout Builder validates background fields:

- **background_color**: Must be valid hex format (`#` followed by 6 hex digits)
- **background_image**: Must be valid URL or data URI
- Both fields are optional
- Invalid values are ignored (slide falls back to white)

### Example: Complete Director API Call

```bash
curl -X POST https://web-production-f0d13.up.railway.app/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q4 Business Review",
    "slides": [
      {
        "layout": "L29",
        "background_image": "https://cdn.example.com/q4-hero.jpg",
        "background_color": "#1a1a2e",
        "content": {
          "hero_content": "<div>...</div>"
        }
      },
      {
        "layout": "L25",
        "background_color": "#f0f9ff",
        "content": {
          "slide_title": "Revenue Growth",
          "rich_content": "<div>...</div>"
        }
      }
    ]
  }'
```

### Best Practices for Director Service

1. **Always provide fallback color** when using `background_image`
2. **Use brand-aligned colors** for consistency across presentations
3. **Limit image backgrounds** to key slides (title, hero, sections)
4. **Test contrast ratios** to ensure text readability
5. **Keep images optimized** (1920×1080, under 1MB)
6. **Use data URIs sparingly** (for small images/logos only)

### Testing Background Integration

Test file available at: `tests/test_background_features.json`

```bash
# Load test presentation with various background configurations
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_background_features.json
```

---

## Version History

### v7.5.1 (January 18, 2025)
- ✅ Hidden edit UI by default for iframe embedding
- ✅ Fixed navigation arrows clickability (pointer-events fix)
- ✅ Exposed overview mode functions (`toggleOverview`, `isOverviewActive`)
- ✅ Added optional edit UI control via `data-show-edit-ui` attribute

### v7.5.0 (November 16, 2025)
- Initial release with 6 layouts (L01, L02, L03, L25, L27, L29)
- Edit mode with keyboard shortcuts
- Reveal.js 4.5.0 integration
- Chart.js 4.4.0 support

---

## Support

**Railway Production**: https://web-production-f0d13.up.railway.app
**Documentation**: `/agents/layout_builder_main/v7.5-main/docs/`
**Issues**: Report to backend team

---

**Last Updated**: 2025-01-18
**Version**: 7.5.1
