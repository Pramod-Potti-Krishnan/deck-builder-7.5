# Theming API - Frontend Integration Guide

## Overview

The **Theming System** provides consistent visual styling across all slides in a presentation:
- **Theme Selection**: Choose from 4 predefined themes (corporate-blue, minimal-gray, vibrant-orange, dark-mode)
- **Color Overrides**: Customize individual colors while inheriting the rest from the base theme
- **CSS Variable Injection**: Themes are applied via CSS custom properties for instant updates

Key characteristics:
- **Presentation-level** - Theme is stored at the presentation level, applied globally
- **Gradual Migration** - Templates opt-in via `themingEnabled` flag (H-series enabled)
- **Instant Preview** - Preview themes without saving via `previewTheme` action
- **Style Cascade** - 5-level priority: defaults → theme → template → overrides → inline

---

## Data Models

### PresentationThemeConfig
```typescript
interface PresentationThemeConfig {
  theme_id: string;                    // e.g., "corporate-blue", "dark-mode"
  color_overrides?: Record<string, string> | null;  // Optional accent color overrides
}
```

### ThemeConfig (Full Theme Definition)
```typescript
interface ThemeConfig {
  id: string;
  name: string;
  description: string;
  colors: ThemeColors;
  typography: ThemeTypography;
  content_styles?: ContentStyles | null;
  is_custom: boolean;
}
```

### ThemeColors
```typescript
interface ThemeColors {
  primary: string;           // Main brand color
  primary_light: string;     // Lighter variant
  primary_dark: string;      // Darker variant
  accent: string;            // Accent/highlight color
  background: string;        // Main background
  background_alt: string;    // Alternate background
  text_primary: string;      // Primary text color
  text_secondary: string;    // Secondary text color
  text_body: string;         // Body text color
  hero_text_primary: string; // Hero slide title color
  hero_text_secondary: string; // Hero slide subtitle color
  hero_background: string;   // Hero slide background
  footer_text: string;       // Footer text color
  border: string;            // Border color
}
```

**Color Key Mapping (camelCase ↔ snake_case):**
| JavaScript (camelCase) | Python (snake_case) | CSS Variable |
|------------------------|---------------------|--------------|
| `primary` | `primary` | `--theme-primary` |
| `primaryLight` | `primary_light` | `--theme-primary-light` |
| `textPrimary` | `text_primary` | `--theme-text-primary` |
| `heroTextPrimary` | `hero_text_primary` | `--theme-hero-text-primary` |
| `heroBackground` | `hero_background` | `--theme-hero-bg` |

---

## Available Themes

| Theme ID | Name | Description |
|----------|------|-------------|
| `corporate-blue` | Corporate Blue | Professional blue theme for business presentations (default) |
| `minimal-gray` | Minimal Gray | Clean, minimalist gray theme for modern presentations |
| `vibrant-orange` | Vibrant Orange | Energetic orange theme for creative presentations |
| `dark-mode` | Dark Mode | Dark theme for low-light environments |

---

## PostMessage API Reference

All commands follow the standard postMessage pattern:

```javascript
// Send command
iframe.contentWindow.postMessage({
  action: 'commandName',
  params: { /* parameters */ }
}, iframeOrigin);

// Receive response
window.addEventListener('message', (event) => {
  const { success, action, error, ...data } = event.data;
  // Handle response
});
```

---

### 1. List Themes

Get all available predefined themes.

**Action:** `listThemes`

**Parameters:** None

**Response:**
```javascript
{
  success: true,
  action: 'listThemes',
  themes: ['corporate-blue', 'minimal-gray', 'vibrant-orange', 'dark-mode'],
  defaultTheme: 'corporate-blue'
}
```

**Example:**
```javascript
iframe.contentWindow.postMessage({
  action: 'listThemes'
}, iframeOrigin);
```

---

### 2. Get Theme

Get the current theme configuration for the presentation.

**Action:** `getTheme`

**Parameters:** None

**Response:**
```javascript
{
  success: true,
  action: 'getTheme',
  themeConfig: {
    theme_id: 'corporate-blue',
    color_overrides: null
  }
}
```

**Example:**
```javascript
iframe.contentWindow.postMessage({
  action: 'getTheme'
}, iframeOrigin);
```

---

### 3. Set Theme

Set the presentation theme. Changes are persisted to the database and CSS variables are injected.

**Action:** `setTheme`

**Parameters:**
```typescript
{
  themeId: string;                           // Required: theme identifier
  colorOverrides?: Record<string, string>;   // Optional: color overrides
}
```

**Response:**
```javascript
{
  success: true,
  action: 'setTheme',
  themeConfig: {
    theme_id: 'vibrant-orange',
    color_overrides: { primary: '#ff5500' }
  },
  message: 'Theme set to vibrant-orange'
}
```

**Examples:**

```javascript
// Set theme without overrides
iframe.contentWindow.postMessage({
  action: 'setTheme',
  params: {
    themeId: 'dark-mode'
  }
}, iframeOrigin);

// Set theme with color overrides
iframe.contentWindow.postMessage({
  action: 'setTheme',
  params: {
    themeId: 'corporate-blue',
    colorOverrides: {
      primary: '#0066cc',
      accent: '#ff6600'
    }
  }
}, iframeOrigin);
```

---

### 4. Preview Theme

Preview a theme without saving to database. Useful for theme picker UI.

**Action:** `previewTheme`

**Parameters:**
```typescript
{
  themeId: string;                           // Required: theme identifier
  colorOverrides?: Record<string, string>;   // Optional: color overrides
}
```

**Response:**
```javascript
{
  success: true,
  action: 'previewTheme',
  message: 'Theme preview applied (not saved)'
}
```

**Example:**
```javascript
// Preview dark mode theme
iframe.contentWindow.postMessage({
  action: 'previewTheme',
  params: {
    themeId: 'dark-mode'
  }
}, iframeOrigin);

// Preview with custom primary color
iframe.contentWindow.postMessage({
  action: 'previewTheme',
  params: {
    themeId: 'corporate-blue',
    colorOverrides: {
      primary: '#00aa00'
    }
  }
}, iframeOrigin);
```

---

## REST API Endpoints

In addition to postMessage, you can call these REST endpoints directly:

### GET /api/themes
List all available themes.

```bash
curl "http://localhost:8504/api/themes"
```

**Response:**
```json
{
  "predefined": ["corporate-blue", "minimal-gray", "vibrant-orange", "dark-mode"],
  "default": "corporate-blue",
  "themes": {
    "corporate-blue": { /* full theme config */ },
    "minimal-gray": { /* full theme config */ },
    ...
  }
}
```

### GET /api/themes/{theme_id}
Get a specific theme's full configuration.

```bash
curl "http://localhost:8504/api/themes/dark-mode"
```

### GET /api/presentations/{id}/theme
Get the current theme configuration for a presentation.

```bash
curl "http://localhost:8504/api/presentations/{id}/theme"
```

**Response:**
```json
{
  "theme_config": {
    "theme_id": "corporate-blue",
    "color_overrides": null
  },
  "resolved_theme": {
    "id": "corporate-blue",
    "name": "Corporate Blue",
    "colors": { /* with overrides applied */ },
    ...
  }
}
```

### PUT /api/presentations/{id}/theme
Set the presentation theme.

```bash
curl -X PUT "http://localhost:8504/api/presentations/{id}/theme" \
  -H "Content-Type: application/json" \
  -d '{
    "theme_id": "vibrant-orange",
    "color_overrides": {
      "primary": "#ff5500"
    }
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Theme set to 'vibrant-orange'",
  "theme_config": {
    "theme_id": "vibrant-orange",
    "color_overrides": { "primary": "#ff5500" }
  },
  "resolved_theme": { /* full theme with overrides applied */ }
}
```

---

## Frontend Implementation Guide

### Theme Picker Panel

Recommended UI for theme selection:

```
+--------------------------------------------------+
|  Presentation Theme                         [X]  |
+--------------------------------------------------+
|                                                  |
|  SELECT THEME                                    |
|  +--------+ +--------+ +--------+ +--------+     |
|  |  Blue  | |  Gray  | | Orange | |  Dark  |     |
|  | [====] | | [====] | | [====] | | [====] |     |
|  +--------+ +--------+ +--------+ +--------+     |
|       *                                          |
|                                                  |
|  CUSTOMIZE COLORS (Optional)                     |
|  Primary:    [#1e40af] [color picker]            |
|  Accent:     [#f59e0b] [color picker]            |
|  [Reset to theme defaults]                       |
|                                                  |
+--------------------------------------------------+
|                              [Cancel]  [Apply]   |
+--------------------------------------------------+
```

### Implementation Steps

1. **List available themes** when opening picker:
```javascript
iframe.contentWindow.postMessage({ action: 'listThemes' }, origin);
```

2. **Get current theme** to show selection:
```javascript
iframe.contentWindow.postMessage({ action: 'getTheme' }, origin);
```

3. **Live preview** as user clicks themes:
```javascript
iframe.contentWindow.postMessage({
  action: 'previewTheme',
  params: {
    themeId: 'dark-mode'
  }
}, origin);
```

4. **Save selection** when user clicks Apply:
```javascript
iframe.contentWindow.postMessage({
  action: 'setTheme',
  params: {
    themeId: selectedThemeId,
    colorOverrides: hasOverrides ? colorOverrides : undefined
  }
}, origin);
```

5. **Restore on cancel** if user cancels after previewing:
```javascript
// Restore original theme
iframe.contentWindow.postMessage({
  action: 'previewTheme',
  params: {
    themeId: originalThemeId,
    colorOverrides: originalOverrides
  }
}, origin);
```

6. **Handle response** and close panel on success:
```javascript
window.addEventListener('message', (event) => {
  if (event.data.action === 'setTheme') {
    if (event.data.success) {
      showToast('Theme applied!');
      closeThemePicker();
    } else {
      showError(event.data.error);
    }
  }
});
```

---

## CSS Variables Reference

The theming system injects these CSS custom properties:

### Color Variables
| Variable | Description |
|----------|-------------|
| `--theme-primary` | Primary brand color |
| `--theme-primary-light` | Lighter primary variant |
| `--theme-primary-dark` | Darker primary variant |
| `--theme-accent` | Accent/highlight color |
| `--theme-bg` | Main background color |
| `--theme-bg-alt` | Alternate background color |
| `--theme-text-primary` | Primary text color |
| `--theme-text-secondary` | Secondary text color |
| `--theme-text-body` | Body text color |
| `--theme-hero-text-primary` | Hero slide title color |
| `--theme-hero-text-secondary` | Hero slide subtitle color |
| `--theme-hero-bg` | Hero slide background color |
| `--theme-footer-text` | Footer text color |
| `--theme-border` | Border color |

### Typography Variables
| Variable | Description |
|----------|-------------|
| `--theme-font-family` | Font family (default: Poppins) |
| `--theme-title-size` | Standard title size (42px) |
| `--theme-subtitle-size` | Standard subtitle size (24px) |
| `--theme-body-size` | Body text size (20px) |
| `--theme-hero-title-size` | Hero title size (72px) |
| `--theme-hero-subtitle-size` | Hero subtitle size (32px) |

### Using Variables in Custom CSS
```css
.my-custom-element {
  color: var(--theme-text-primary);
  background: var(--theme-bg-alt);
  border: 1px solid var(--theme-border);
}

.my-accent-button {
  background: var(--theme-accent);
  color: white;
}
```

---

## Style Cascade

Styles are computed with this priority (lowest to highest):

1. **SLOT_STYLE_DEFAULTS** - Base typography for standard/hero profiles
2. **Theme typography** - Theme-specific overrides
3. **Template-specific** - Per-template slot styles
4. **Color overrides** - Presentation-level color customizations
5. **Inline overrides** - Per-element inline styles

Templates must have `themingEnabled: true` to use the cascade. Currently enabled:
- H1-generated, H1-structured (Title slides)
- H2-section (Section dividers)
- H3-closing (Closing slides)

---

## Error Handling

All postMessage responses include `success` and `error` fields:

```javascript
// Success
{
  success: true,
  action: 'setTheme',
  themeConfig: { ... }
}

// Error
{
  success: false,
  action: 'setTheme',
  error: 'Theme not found: invalid-theme'
}
```

Common errors:
- `Theme not found: {theme_id}` - Invalid theme identifier
- `No presentation ID available` - Presentation not loaded
- `Failed to set theme` - API error

---

## Database Migration

Before using the theming system, ensure the database column exists:

```sql
-- Add theme_config column to presentations table
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS theme_config JSONB;

-- Optional: Index for faster theme queries
CREATE INDEX IF NOT EXISTS idx_ls_presentations_theme
ON ls_presentations ((theme_config->>'theme_id'));

-- Optional: Comment for documentation
COMMENT ON COLUMN ls_presentations.theme_config IS
'Presentation theme configuration. Structure:
{
  "theme_id": "corporate-blue",
  "color_overrides": {
    "primary": "#custom-color"
  }
}';
```

Run this migration in Supabase SQL Editor:
`migrations/002_add_theme_config.sql`

---

## Version

- **API Version**: 1.0
- **Document Date**: December 2024
- **Layout Service**: v7.5-main
