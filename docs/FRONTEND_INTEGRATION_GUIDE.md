# Frontend Integration Guide - v7.5-main Presentation Viewer

**Date**: December 1, 2025
**Version**: 7.5.3
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

### Review Mode Functions (AI-Powered Section Regeneration)

Review mode allows users to visually select slide sections for AI-powered regeneration. Introduced in Phase 2 as part of the world-class editor features.

#### Toggle Review Mode
```javascript
// Toggle review mode on/off (or press 'R' key)
iframeWindow.toggleReviewMode();

// Check if currently in review mode
const isReviewing = iframeWindow.document.body.getAttribute('data-mode') === 'review';
```

#### Enter Review Mode
```javascript
// Explicitly enter review mode
iframeWindow.enterReviewMode();
// Visual indicator appears, sections become selectable
```

#### Exit Review Mode
```javascript
// Explicitly exit review mode
iframeWindow.exitReviewMode();
// Clears selection and returns to normal view
```

#### Get Selected Sections
```javascript
// Get array of selected sections with metadata
const selectedSections = iframeWindow.getSelectedSections();
console.log(selectedSections);
// [
//   {
//     sectionId: "slide-0-section-title",
//     sectionType: "title",
//     slideIndex: 0,
//     content: "<div>Current content</div>",
//     layout: "L25"
//   }
// ]
```

#### Clear Selection
```javascript
// Clear all selected sections (keeps review mode active)
iframeWindow.clearSelection();
```

**Review Mode Keyboard Shortcuts**:
- **R** - Toggle review mode on/off
- **ESC** - Exit review mode and clear selection
- **Delete/Backspace** - Clear selection (keep review mode active)
- **Ctrl/Cmd+Click** - Multi-select sections

**Use Case**: Frontend AI Regeneration Panel
```javascript
// Frontend button to enable section selection
document.getElementById('select-sections-btn').addEventListener('click', () => {
  iframeWindow.enterReviewMode();
});

// Get selected sections and send to AI service
document.getElementById('regenerate-btn').addEventListener('click', () => {
  const sections = iframeWindow.getSelectedSections();

  if (sections.length === 0) {
    alert('Please select sections first');
    return;
  }

  // Send to Director Service for AI regeneration
  sections.forEach(section => {
    regenerateSection({
      slide_index: section.slideIndex,
      section_id: section.sectionId,
      section_type: section.sectionType,
      current_content: section.content,
      layout: section.layout,
      user_instruction: "Make it more engaging"
    });
  });
});
```

### Navigation Functions

#### Next/Previous Slide
```javascript
// Next slide
iframeWindow.Reveal.next();

// Previous slide
iframeWindow.Reveal.prev();

// Navigate to specific slide (0-based index)
iframeWindow.goToSlide(4);  // Goes to 5th slide
```

#### Get Current Slide Info
```javascript
const slideInfo = iframeWindow.getCurrentSlideInfo();
console.log(slideInfo);
// {
//   index: 2,        // 0-based (3rd slide)
//   total: 10,
//   layoutId: "L02"
// }
// Note: Frontend should display as "Slide ${index + 1} / ${total}" for 1-based user display
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
    <button id="review-btn">📋 Review</button>
    <button id="save-btn" style="display: none;">💾 Save</button>
    <button id="regenerate-btn" style="display: none;">🤖 Regenerate</button>
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

    // Toggle review mode
    document.getElementById('review-btn').addEventListener('click', () => {
      if (iframeWindow) {
        iframeWindow.toggleReviewMode();

        // Show/hide regenerate button
        const isReviewing = iframeWindow.document.body.getAttribute('data-mode') === 'review';
        document.getElementById('regenerate-btn').style.display = isReviewing ? 'block' : 'none';
        document.getElementById('review-btn').textContent = isReviewing ? '❌ Exit Review' : '📋 Review';
      }
    });

    // Regenerate selected sections
    document.getElementById('regenerate-btn').addEventListener('click', () => {
      if (iframeWindow) {
        const sections = iframeWindow.getSelectedSections();

        if (sections.length === 0) {
          alert('Please select sections first by clicking on them');
          return;
        }

        // Send to AI regeneration API
        console.log('Regenerating sections:', sections);
        // TODO: Call Director Service API for each section
        sections.forEach(section => {
          console.log(`Regenerate ${section.sectionType} on slide ${section.slideIndex}`);
        });
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
| **ESC** | Toggle overview mode (or exit review mode) |
| **E** | Toggle edit mode |
| **R** | Toggle review mode (AI section selection) |
| **Ctrl+S** | Save changes (in edit mode) |
| **Delete/Backspace** | Clear selection (in review mode) |
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

### Cross-Origin Issues - postMessage Required

⚠️ **IMPORTANT**: When embedding from a different domain (cross-origin), you **CANNOT** use direct `iframe.contentWindow` access due to browser Same-Origin Policy.

**Why Direct Access Fails**:
```javascript
// ❌ DOES NOT WORK cross-origin
const iframeWindow = iframe.contentWindow;
iframeWindow.Reveal.next();  // ❌ SecurityError: Blocked cross-origin access
```

**The Solution: postMessage API**

The viewer now includes a postMessage bridge for cross-origin communication. Use `postMessage` to send commands:

```javascript
// ✅ WORKS cross-origin
const iframe = document.getElementById('presentation-iframe');

// Send command via postMessage
iframe.contentWindow.postMessage(
  { action: 'nextSlide' },
  'https://web-production-f0d13.up.railway.app'
);

// Listen for response
window.addEventListener('message', (event) => {
  if (event.data.action === 'nextSlide' && event.data.success) {
    console.log('✅ Slide navigated');
  }
});
```

**Available Actions**:

**Navigation**:
- `nextSlide` - Navigate to next slide
- `prevSlide` - Navigate to previous slide
- `goToSlide` - Navigate to specific slide (params: {index: number})
- `getCurrentSlideInfo` - Get current slide information

**Edit Mode**:
- `toggleEditMode` - Toggle edit mode on/off
- `saveAllChanges` - Save all edits
- `cancelEdits` - Cancel edits
- `showVersionHistory` - Show version history modal

**Review Mode** (AI Section Selection):
- `toggleReviewMode` - Toggle review mode on/off
- `enterReviewMode` - Explicitly enter review mode
- `exitReviewMode` - Explicitly exit review mode
- `getSelectedSections` - Get array of selected sections with metadata
- `clearSelection` - Clear all selected sections

**Overview Mode**:
- `toggleOverview` - Toggle overview mode
- `isOverviewActive` - Check if overview is active

**Debug**:
- `toggleGridOverlay` - Toggle grid overlay
- `toggleBorderHighlight` - Toggle border highlighting

**Complete Cross-Origin Example**:

```javascript
const iframe = document.getElementById('presentation-iframe');
const targetOrigin = 'https://web-production-f0d13.up.railway.app';

// Helper function to send commands
function sendCommand(action, params = {}) {
  return new Promise((resolve) => {
    const handler = (event) => {
      if (event.data.action === action) {
        window.removeEventListener('message', handler);
        resolve(event.data);
      }
    };
    window.addEventListener('message', handler);
    iframe.contentWindow.postMessage({ action, params }, targetOrigin);
  });
}

// Usage examples
async function navigateNext() {
  const result = await sendCommand('nextSlide');
  if (result.success) {
    console.log('✅ Next slide');
  }
}

async function getSlideInfo() {
  const result = await sendCommand('getCurrentSlideInfo');
  if (result.success) {
    console.log(`Slide ${result.data.index} / ${result.data.total}`);
  }
}

async function toggleEdit() {
  const result = await sendCommand('toggleEditMode');
  if (result.success) {
    console.log(`Edit mode: ${result.isEditing ? 'ON' : 'OFF'}`);
  }
}

// Review mode examples
async function toggleReview() {
  const result = await sendCommand('toggleReviewMode');
  if (result.success) {
    console.log(`Review mode: ${result.isReviewing ? 'ON' : 'OFF'}`);
  }
}

async function getSelectedSections() {
  const result = await sendCommand('getSelectedSections');
  if (result.success) {
    console.log('Selected sections:', result.data);
    // result.data is array of section objects with metadata
    return result.data;
  }
}

async function clearSelection() {
  const result = await sendCommand('clearSelection');
  if (result.success) {
    console.log('✅ Selection cleared');
  }
}
```

**Security Notes**:
- The viewer validates message origins before executing commands
- Allowed origins: localhost, Railway, Vercel, Netlify domains, deckster.xyz (production)
- Unauthorized origins are rejected with console warnings

**Same-Origin Deployment**:
If both frontend and viewer are on the same domain, direct access works:
```javascript
// ✅ Works when same origin (e.g., both on localhost:3002)
iframeWindow.Reveal.next();
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
  goToSlide(index: number): void;  // 0-based index
  getCurrentSlideInfo(): {
    index: number;    // 0-based index (frontend adds 1 for display)
    total: number;
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

## Slide CRUD Operations (NEW in v7.5.2)

The presentation viewer now supports full slide management via postMessage:

### Add Slide

```javascript
// Add a new slide at a specific position
iframe.contentWindow.postMessage({
  action: 'addSlide',
  params: {
    layout: 'L25',     // L01, L02, L03, L25, L27, L29
    position: 2,       // Optional: 0-based index. If omitted, appends at end
    content: {         // Optional: Custom content. Uses defaults if omitted
      slide_title: 'New Slide',
      subtitle: 'Custom subtitle',
      rich_content: '<p>Your content here</p>'
    }
  }
}, targetOrigin);

// Response
// { action: 'addSlide', success: true, data: { slideIndex: 2, slideCount: 6 } }
```

### Delete Slide

```javascript
// Delete slide at index
iframe.contentWindow.postMessage({
  action: 'deleteSlide',
  params: { index: 3 }  // 0-based slide index
}, targetOrigin);

// Response
// { action: 'deleteSlide', success: true, data: { deletedIndex: 3, slideCount: 5 } }
```

### Reorder Slides

```javascript
// Move slide from one position to another
iframe.contentWindow.postMessage({
  action: 'reorderSlides',
  params: {
    from_index: 0,  // Current position (0-based)
    to_index: 3     // New position (0-based)
  }
}, targetOrigin);

// Response
// { action: 'reorderSlides', success: true, data: { slideOrder: ['L25','L29','L25','L01'] } }
```

### Duplicate Slide

```javascript
// Duplicate slide at index
iframe.contentWindow.postMessage({
  action: 'duplicateSlide',
  params: {
    index: 2,           // 0-based slide index
    insert_after: true  // Optional: Insert after source (default: true)
  }
}, targetOrigin);

// Response
// { action: 'duplicateSlide', success: true, data: { newSlideIndex: 3, slideCount: 7 } }
```

### Change Slide Layout

```javascript
// Change layout of existing slide
iframe.contentWindow.postMessage({
  action: 'changeSlideLayout',
  params: {
    index: 1,              // 0-based slide index
    new_layout: 'L29',     // Target layout
    preserve_content: true // Optional: Try to map content (default: true)
  }
}, targetOrigin);

// Response
// { action: 'changeSlideLayout', success: true, data: { previousLayout: 'L25', newLayout: 'L29' } }
```

### Get Available Layouts

```javascript
// Get list of available layout templates
iframe.contentWindow.postMessage({
  action: 'getSlideLayouts'
}, targetOrigin);

// Response
// { action: 'getSlideLayouts', success: true, data: [
//   { id: 'L01', name: 'Centered Chart', icon: '📊' },
//   { id: 'L02', name: 'Diagram Left', icon: '🔲' },
//   { id: 'L25', name: 'Content Shell', icon: '📝' },
//   { id: 'L29', name: 'Full-Bleed Hero', icon: '🎯' }
// ]}
```

### Get Slide Info

```javascript
// Get detailed info about a specific slide
iframe.contentWindow.postMessage({
  action: 'getSlideInfo',
  params: { slideIndex: 0 }
}, targetOrigin);

// Response
// { action: 'getSlideInfo', success: true, data: {
//   layout: 'L25',
//   title: 'Welcome Slide',
//   hasBackgroundImage: false,
//   backgroundColor: null
// }}
```

---

## Rich Text Formatting (NEW in v7.5.2)

When in edit mode, selecting text displays a floating toolbar with formatting options.

### Available Formatting Options

| Feature | Button | Keyboard Shortcut |
|---------|--------|-------------------|
| **Bold** | B | Ctrl/Cmd + B |
| **Italic** | I | Ctrl/Cmd + I |
| **Underline** | U | Ctrl/Cmd + U |
| **Strikethrough** | S | - |
| **Font Size** | Dropdown (8-48px) | - |
| **Font Family** | Dropdown | - |
| **Text Color** | Color picker | - |
| **Highlight Color** | Color picker | - |
| **Align Left** | ◀ | - |
| **Align Center** | ▮ | - |
| **Align Right** | ▶ | - |
| **Bullet List** | • | - |
| **Numbered List** | 1. | - |

### Toolbar Behavior

- Toolbar appears automatically when text is selected in edit mode
- Positioned above the selection (or below if near viewport top)
- Stays visible while formatting, hides when clicking elsewhere
- All formatting uses native `document.execCommand()` for compatibility

---

## Auto-Save System (NEW in v7.5.2)

Content is automatically saved with debouncing to prevent excessive API calls.

### Configuration

- **Debounce Delay**: 2500ms (2.5 seconds of inactivity)
- **Retry Attempts**: 3 attempts with 1 second delay
- **Change Tracking**: Per-slide tracking of modified fields

### Status Indicator

The bottom-right corner shows save status:

| Status | Indicator | Description |
|--------|-----------|-------------|
| **Saved** | 🟢 Green | All changes saved |
| **Unsaved** | 🟡 Yellow (pulsing) | Pending changes |
| **Saving** | 🔵 Blue (spinner) | Save in progress |
| **Error** | 🔴 Red | Save failed (click to retry) |

### PostMessage Commands

```javascript
// Force immediate save
iframe.contentWindow.postMessage({ action: 'forceSave' }, targetOrigin);

// Check for pending changes
iframe.contentWindow.postMessage({ action: 'getPendingChanges' }, targetOrigin);
// Response: { hasPending: true, slideCount: 2, slides: [0, 3] }
```

### Browser Warnings

If there are unsaved changes and the user tries to leave the page, a browser warning will appear asking for confirmation.

---

## Text Formatting API (NEW in v7.5.3)

Programmatic text formatting via postMessage, complementing the toolbar UI.

### Format Text

Apply formatting to selected text or an entire section:

```javascript
// Format current selection
iframe.contentWindow.postMessage({
  action: 'formatText',
  params: {
    bold: true,              // true | false | 'toggle'
    italic: true,
    underline: false,
    strikethrough: false,
    fontSize: '24px',        // '8px' to '48px' or execCommand sizes '1'-'7'
    fontFamily: 'Inter',     // Any valid font family
    color: '#1e40af',        // Hex color for text
    backgroundColor: '#fef3c7', // Hex color for highlight
    alignment: 'center',     // 'left' | 'center' | 'right' | 'justify'
    listType: 'bullet'       // 'bullet' | 'numbered' | 'none'
  }
}, targetOrigin);

// Response
// { action: 'formatText', success: true, applied: ['bold', 'italic', 'fontSize', 'color'] }
```

### Format Entire Section

Apply formatting to all content in a specific section:

```javascript
iframe.contentWindow.postMessage({
  action: 'formatText',
  params: {
    sectionId: 'slide-0-section-title',  // Target section by ID
    applyToAll: true,                     // Apply to entire section content
    bold: true,
    color: '#1e40af'
  }
}, targetOrigin);
```

### Get Selection Info

Get information about the current text selection:

```javascript
iframe.contentWindow.postMessage({
  action: 'getSelectionInfo'
}, targetOrigin);

// Response
// {
//   action: 'getSelectionInfo',
//   success: true,
//   data: {
//     hasSelection: true,
//     selectedText: 'Hello World',
//     sectionId: 'slide-0-section-title',
//     slideIndex: 0,
//     formatting: {
//       bold: true,
//       italic: false,
//       underline: false,
//       strikethrough: false,
//       fontSize: '3',
//       fontFamily: 'Inter',
//       color: 'rgb(30, 64, 175)',
//       backgroundColor: '',
//       alignment: { left: true, center: false, right: false, justify: false },
//       bulletList: false,
//       numberedList: false
//     }
//   }
// }
```

### Update Section Content

Replace the HTML content of a specific section:

```javascript
iframe.contentWindow.postMessage({
  action: 'updateSectionContent',
  params: {
    slideIndex: 0,
    sectionId: 'slide-0-section-title',
    content: '<h1 style="color: #1e40af;">New Title</h1>'
  }
}, targetOrigin);

// Response
// { action: 'updateSectionContent', success: true }
```

---

## Dynamic Elements API (NEW in v7.5.3)

Insert and manage shapes, tables, charts, and images with drag-and-drop repositioning.

### Grid System

All elements are positioned on a **32×18 grid** (based on 1920×1080 resolution):
- **Columns**: 1-32 (each column is 60px at base resolution)
- **Rows**: 1-18 (each row is 60px at base resolution)
- Grid positions use CSS grid syntax: `"start/end"` (e.g., `"5/12"` spans columns/rows 5 through 11)

### Insert Shape

Insert SVG shapes (rectangles, circles, arrows, etc.):

```javascript
iframe.contentWindow.postMessage({
  action: 'insertShape',
  params: {
    slideIndex: 0,
    type: 'rectangle',        // 'rectangle' | 'circle' | 'arrow' | 'line' | 'triangle' | custom SVG
    gridRow: '5/10',          // Grid row position (1-18)
    gridColumn: '3/15',       // Grid column position (1-32)
    fill: '#3b82f6',          // Fill color (hex)
    stroke: '#1e40af',        // Stroke color (hex)
    strokeWidth: 2,           // Stroke width in pixels
    svgContent: '<svg>...</svg>'  // Optional: Custom SVG (overrides type)
  }
}, targetOrigin);

// Response
// {
//   action: 'insertShape',
//   success: true,
//   data: {
//     elementId: 'shape-1701388800000-abc123',
//     type: 'shape',
//     slideIndex: 0,
//     position: { gridRow: '5/10', gridColumn: '3/15' }
//   }
// }
```

### Insert Table

Insert HTML tables (typically from Text Service):

```javascript
iframe.contentWindow.postMessage({
  action: 'insertTable',
  params: {
    slideIndex: 0,
    gridRow: '4/14',
    gridColumn: '2/31',
    tableHtml: `
      <table>
        <thead>
          <tr><th>Metric</th><th>Q3</th><th>Q4</th></tr>
        </thead>
        <tbody>
          <tr><td>Revenue</td><td>$1.2M</td><td>$1.5M</td></tr>
          <tr><td>Growth</td><td>12%</td><td>25%</td></tr>
        </tbody>
      </table>
    `
  }
}, targetOrigin);

// Response
// {
//   action: 'insertTable',
//   success: true,
//   data: {
//     elementId: 'table-1701388800000-xyz789',
//     type: 'table',
//     slideIndex: 0,
//     position: { gridRow: '4/14', gridColumn: '2/31' }
//   }
// }
```

### Insert Chart

Insert Chart.js charts (typically from Analytics Service):

```javascript
iframe.contentWindow.postMessage({
  action: 'insertChart',
  params: {
    slideIndex: 0,
    gridRow: '3/16',
    gridColumn: '2/20',
    chartConfig: {
      type: 'bar',
      data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
          label: 'Revenue',
          data: [12, 19, 15, 25],
          backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
          legend: { display: true, position: 'top' }
        }
      }
    }
  }
}, targetOrigin);

// Response
// {
//   action: 'insertChart',
//   success: true,
//   data: {
//     elementId: 'chart-1701388800000-def456',
//     type: 'chart',
//     slideIndex: 0,
//     chartType: 'bar',
//     position: { gridRow: '3/16', gridColumn: '2/20' }
//   }
// }
```

**Supported Chart Types** (via Analytics Service):
- `bar`, `line`, `pie`, `doughnut`, `radar`, `polarArea`
- `scatter`, `bubble`, `area`, `combo`
- `treemap`, `heatmap`, `funnel`, `waterfall`, `sankey`

### Insert Image

Insert images (typically from Image Service):

```javascript
iframe.contentWindow.postMessage({
  action: 'insertImage',
  params: {
    slideIndex: 0,
    gridRow: '2/17',
    gridColumn: '18/32',
    imageUrl: 'https://images.unsplash.com/photo-xxxxx',
    alt: 'Team collaboration photo'
  }
}, targetOrigin);

// Response
// {
//   action: 'insertImage',
//   success: true,
//   data: {
//     elementId: 'image-1701388800000-ghi012',
//     type: 'image',
//     slideIndex: 0,
//     position: { gridRow: '2/17', gridColumn: '18/32' }
//   }
// }
```

### Delete Element

Remove a dynamic element by ID:

```javascript
iframe.contentWindow.postMessage({
  action: 'deleteElement',
  params: {
    elementId: 'chart-1701388800000-def456'
  }
}, targetOrigin);

// Response
// { action: 'deleteElement', success: true }
```

### Element Drag-and-Drop

All inserted elements are automatically draggable in edit mode:
- **Mouse drag**: Click and drag to reposition
- **Arrow keys**: Nudge selected element by 1 grid cell
- **Delete/Backspace**: Remove selected element
- **Grid snapping**: Elements snap to the 32×18 grid

### Element Selection

Elements can be selected by clicking in edit mode:
- Selected elements show a blue border
- Only one element can be selected at a time
- Click outside to deselect

---

## Service Integration Pattern (v7.5.3)

The Layout Builder acts as an orchestration layer, receiving content from external services:

### Text Service Integration

```javascript
// 1. Request content from Text Service
const textResponse = await fetch('https://text-service/api/generate-section', {
  method: 'POST',
  body: JSON.stringify({
    section_type: 'rich_content',
    prompt: 'Create 3 bullet points about market trends',
    theme: 'corporate-blue'
  })
});
const { html } = await textResponse.json();

// 2. Insert into Layout Builder
iframe.contentWindow.postMessage({
  action: 'updateSectionContent',
  params: {
    slideIndex: 0,
    sectionId: 'slide-0-section-content',
    content: html
  }
}, targetOrigin);
```

### Analytics Service Integration

```javascript
// 1. Request chart from Analytics Service
const chartResponse = await fetch('https://analytics-service/api/charts/bar', {
  method: 'POST',
  body: JSON.stringify({
    data: [12, 19, 15, 25],
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    title: 'Quarterly Revenue'
  })
});
const { chartConfig } = await chartResponse.json();

// 2. Insert into Layout Builder
iframe.contentWindow.postMessage({
  action: 'insertChart',
  params: {
    slideIndex: 0,
    gridRow: '3/16',
    gridColumn: '2/20',
    chartConfig: chartConfig
  }
}, targetOrigin);
```

### Image Service Integration

```javascript
// 1. Request image from Image Service
const imageResponse = await fetch('https://image-service/api/generate', {
  method: 'POST',
  body: JSON.stringify({
    prompt: 'Professional team collaboration',
    aspect_ratio: '16:9',
    style: 'photorealistic'
  })
});
const { image_url } = await imageResponse.json();

// 2. Insert into Layout Builder
iframe.contentWindow.postMessage({
  action: 'insertImage',
  params: {
    slideIndex: 0,
    gridRow: '2/17',
    gridColumn: '18/32',
    imageUrl: image_url,
    alt: 'Team collaboration'
  }
}, targetOrigin);
```

---

## Complete CRUD Example

```javascript
const iframe = document.getElementById('presentation-iframe');
const targetOrigin = 'https://web-production-f0d13.up.railway.app';

// Helper for postMessage commands
function sendCommand(action, params = {}) {
  return new Promise((resolve) => {
    const handler = (event) => {
      if (event.data.action === action) {
        window.removeEventListener('message', handler);
        resolve(event.data);
      }
    };
    window.addEventListener('message', handler);
    iframe.contentWindow.postMessage({ action, params }, targetOrigin);
  });
}

// Example: Create a slide at position 2 with custom content
async function addCustomSlide() {
  const result = await sendCommand('addSlide', {
    layout: 'L25',
    position: 2,
    content: {
      slide_title: 'New Analysis',
      subtitle: 'Key Findings',
      rich_content: '<ul><li>Point 1</li><li>Point 2</li></ul>'
    }
  });

  if (result.success) {
    console.log(`Added slide at index ${result.data.slideIndex}`);
    // Navigate to new slide
    await sendCommand('goToSlide', { index: result.data.slideIndex });
  }
}

// Example: Duplicate current slide and change its layout
async function duplicateAsHero() {
  const slideInfo = await sendCommand('getCurrentSlideInfo');
  const currentIndex = slideInfo.data.index;

  // Duplicate
  const dupResult = await sendCommand('duplicateSlide', {
    index: currentIndex,
    insert_after: true
  });

  // Change layout to hero
  if (dupResult.success) {
    await sendCommand('changeSlideLayout', {
      index: dupResult.data.newSlideIndex,
      new_layout: 'L29'
    });
  }
}

// Example: Delete slide with confirmation
async function deleteCurrentSlide() {
  const slideInfo = await sendCommand('getCurrentSlideInfo');

  if (slideInfo.data.total <= 1) {
    alert('Cannot delete the last slide');
    return;
  }

  if (confirm(`Delete slide ${slideInfo.data.index + 1}?`)) {
    const result = await sendCommand('deleteSlide', {
      index: slideInfo.data.index
    });

    if (result.success) {
      console.log(`Deleted. ${result.data.slideCount} slides remaining`);
    }
  }
}
```

---

## API Endpoints Reference (v7.5.2)

### REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/presentations` | Create new presentation |
| GET | `/api/presentations/{id}` | Get presentation data |
| PUT | `/api/presentations/{id}` | Update presentation metadata |
| DELETE | `/api/presentations/{id}` | Delete presentation |
| PUT | `/api/presentations/{id}/slides/{index}` | Update slide content |
| POST | `/api/presentations/{id}/slides` | Add new slide |
| DELETE | `/api/presentations/{id}/slides/{index}` | Delete slide |
| PUT | `/api/presentations/{id}/slides/reorder` | Reorder slides |
| POST | `/api/presentations/{id}/slides/{index}/duplicate` | Duplicate slide |
| PUT | `/api/presentations/{id}/slides/{index}/layout` | Change slide layout |
| GET | `/api/presentations/{id}/versions` | Get version history |
| POST | `/api/presentations/{id}/restore/{versionId}` | Restore version |
| POST | `/api/presentations/{id}/regenerate-section` | AI section regeneration |

### Swagger Documentation

Full API documentation available at: `/docs`

---

## Version History

### v7.5.3 (December 1, 2025)
- ✅ **Text Formatting API** - Programmatic formatting via postMessage
  - `formatText` - Apply bold, italic, underline, font size, color, alignment
  - `getSelectionInfo` - Get current selection and formatting state
  - `updateSectionContent` - Replace section HTML content
- ✅ **Dynamic Elements API** - Insert and manage visual elements
  - `insertShape` - Insert SVG shapes with grid positioning
  - `insertTable` - Insert HTML tables with drag support
  - `insertChart` - Insert Chart.js charts (15 types)
  - `insertImage` - Insert images with aspect ratio support
  - `deleteElement` - Remove dynamic elements
- ✅ **Grid-Snapped Drag & Drop** - 32×18 grid system for element positioning
- ✅ **Keyboard Navigation** - Arrow keys for nudging, Delete for removal
- ✅ **Service Integration** - Orchestration layer for Text/Analytics/Image services
- ✅ **FormatAPI Module** - `window.FormatAPI` for direct function access
- ✅ **ElementManager Module** - `window.ElementManager` for element CRUD
- ✅ **DragDrop Module** - `window.DragDrop` for position management

### v7.5.2 (November 30, 2025)
- ✅ Slide CRUD operations (add, delete, reorder, duplicate, change layout)
- ✅ Rich text formatting toolbar with full styling options
- ✅ Auto-save with debounce (2.5 second delay)
- ✅ Save status indicator with visual feedback
- ✅ Layout templates with default content
- ✅ PostMessage handlers for all CRUD operations
- ✅ Keyboard shortcuts for text formatting (Ctrl+B/I/U)
- ✅ Browser warning for unsaved changes

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

**Last Updated**: 2025-12-01
**Version**: 7.5.3
