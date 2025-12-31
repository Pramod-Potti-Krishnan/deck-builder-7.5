# Theme Customization API Documentation

**Version:** 7.5.4
**Last Updated:** December 8, 2024

This document describes the complete Theme Customization System for the Layout Service, enabling full control over presentation theming including colors, typography, spacing, and effects.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Predefined Themes](#predefined-themes)
4. [Theme Data Model](#theme-data-model)
5. [REST API Endpoints](#rest-api-endpoints)
6. [PostMessage API](#postmessage-api)
7. [CSS Variables Reference](#css-variables-reference)
8. [Integration Examples](#integration-examples)
9. [Migration Guide](#migration-guide)

---

## Overview

The Theme Customization System provides:

- **4 Predefined Themes**: Ready-to-use professional themes
- **User Custom Themes**: Create, save, and reuse themes across presentations
- **Theme Inheritance**: Extend predefined themes with custom overrides
- **Granular Control**: Customize colors, typography, spacing, and effects independently
- **Real-time Preview**: Preview theme changes before saving
- **CSS Variable Integration**: All theme properties map to CSS custom properties

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Predefined Theme** | Built-in themes (corporate-blue, minimal-gray, vibrant-orange, dark-mode) |
| **Custom Theme** | User-created theme stored in their library |
| **Theme Overrides** | Partial modifications to any theme property |
| **Base Theme** | The predefined theme a custom theme inherits from |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend Application                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Theme Picker   │  │  Theme Editor   │  │  Theme Library  │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │           │
│           └────────────────────┼────────────────────┘           │
│                                │                                 │
│                    ┌───────────▼───────────┐                    │
│                    │   PostMessage Bridge   │                    │
│                    └───────────┬───────────┘                    │
└────────────────────────────────┼────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Presentation Viewer    │
                    │   (iframe)               │
                    │  ┌──────────────────┐   │
                    │  │  ThemeManager.js  │   │
                    │  │  (CSS Variables)  │   │
                    │  └──────────────────┘   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │    Layout Service API    │
                    │  ┌──────────────────┐   │
                    │  │ Theme Endpoints   │   │
                    │  │ User Themes CRUD  │   │
                    │  └──────────────────┘   │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      Supabase DB         │
                    │  ┌──────────────────┐   │
                    │  │ ls_user_themes    │   │
                    │  │ ls_presentations  │   │
                    │  └──────────────────┘   │
                    └─────────────────────────┘
```

---

## Predefined Themes

### Available Themes

| Theme ID | Name | Description |
|----------|------|-------------|
| `corporate-blue` | Corporate Blue | Professional blue theme for business presentations |
| `minimal-gray` | Minimal Gray | Clean, minimalist gray theme for modern presentations |
| `vibrant-orange` | Vibrant Orange | Energetic orange theme for creative presentations |
| `dark-mode` | Dark Mode | Dark theme for low-light environments |

### Theme Colors Preview

#### Corporate Blue
```
Primary:     #1e40af (Blue)
Accent:      #f59e0b (Amber)
Background:  #ffffff (White)
Hero BG:     #1e3a5f (Dark Blue)
```

#### Minimal Gray
```
Primary:     #374151 (Gray)
Accent:      #10b981 (Emerald)
Background:  #ffffff (White)
Hero BG:     #1f2937 (Dark Gray)
```

#### Vibrant Orange
```
Primary:     #ea580c (Orange)
Accent:      #0891b2 (Cyan)
Background:  #ffffff (White)
Hero BG:     #9a3412 (Dark Orange)
```

#### Dark Mode
```
Primary:     #60a5fa (Light Blue)
Accent:      #fbbf24 (Amber)
Background:  #111827 (Dark)
Hero BG:     #030712 (Near Black)
```

---

## Theme Data Model

### Complete Theme Structure

```typescript
interface Theme {
  id: string;
  name: string;
  description?: string;

  colors: ThemeColors;
  typography: ThemeTypography;
  spacing: ThemeSpacing;
  effects: ThemeEffects;
  content_styles?: ContentStyles;
}

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
  hero_text_primary: string; // Hero slide primary text
  hero_text_secondary: string; // Hero slide secondary text
  hero_background: string;   // Hero slide background
  footer_text: string;       // Footer text color
  border: string;            // Border color
}

interface ThemeTypography {
  font_family: string;           // Primary font (default: "Poppins, sans-serif")
  font_family_heading?: string;  // Heading font (falls back to font_family)

  // Standard slides
  title_size: string;            // Default: "48px"
  title_weight: string;          // Default: "bold"
  title_line_height: string;     // Default: "1.2"

  subtitle_size: string;         // Default: "32px"
  subtitle_weight: string;       // Default: "normal"
  subtitle_line_height: string;  // Default: "1.4"

  body_size: string;             // Default: "24px"
  body_line_height: string;      // Default: "1.6"

  footer_size: string;           // Default: "14px"
  footer_weight: string;         // Default: "500"

  // Hero slides
  hero_title_size: string;       // Default: "72px"
  hero_title_weight: string;     // Default: "bold"
  hero_title_shadow: string;     // Default: "0 2px 4px rgba(0,0,0,0.3)"

  hero_subtitle_size: string;    // Default: "32px"
  hero_subtitle_weight: string;  // Default: "normal"
}

interface ThemeSpacing {
  slide_padding: string;    // Default: "60px"
  element_gap: string;      // Default: "24px"
  section_gap: string;      // Default: "48px"
}

interface ThemeEffects {
  border_radius: string;    // Default: "8px"
  shadow_small: string;     // Default: "0 1px 3px rgba(0,0,0,0.1)"
  shadow_medium: string;    // Default: "0 4px 6px rgba(0,0,0,0.1)"
  shadow_large: string;     // Default: "0 10px 15px rgba(0,0,0,0.1)"
}
```

### Theme Overrides Structure

When applying overrides, you only need to specify the properties you want to change:

```typescript
interface ThemeOverrides {
  colors?: Partial<ThemeColors>;
  typography?: Partial<ThemeTypography>;
  spacing?: Partial<ThemeSpacing>;
  effects?: Partial<ThemeEffects>;
}
```

---

## REST API Endpoints

### Base URL
```
https://your-layout-service.com/api
```

### List All Predefined Themes

```http
GET /api/themes
```

**Response:**
```json
{
  "predefined": ["corporate-blue", "minimal-gray", "vibrant-orange", "dark-mode"],
  "default": "corporate-blue",
  "themes": {
    "corporate-blue": { /* full theme object */ },
    "minimal-gray": { /* full theme object */ }
  }
}
```

### Get Specific Theme

```http
GET /api/themes/{theme_id}
```

**Response:**
```json
{
  "id": "corporate-blue",
  "name": "Corporate Blue",
  "description": "Professional blue theme for business presentations",
  "colors": { /* ThemeColors */ },
  "typography": { /* ThemeTypography */ },
  "content_styles": { /* ContentStyles */ }
}
```

### Get Public Themes (Predefined + User-Shared)

```http
GET /api/themes/public
```

**Response:**
```json
{
  "success": true,
  "predefined_count": 4,
  "public_count": 2,
  "themes": {
    "predefined": [
      { "id": "corporate-blue", "name": "Corporate Blue", "is_predefined": true, "colors": {...} }
    ],
    "user_public": [
      { "id": "uuid", "name": "User Theme", "is_predefined": false, "colors": {...} }
    ]
  }
}
```

---

### User Custom Themes API

#### Create Custom Theme

```http
POST /api/user/themes
Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "My Brand Theme",
  "description": "Company brand colors and fonts",
  "base_theme_id": "corporate-blue",
  "colors": {
    "primary": "#ff5500",
    "accent": "#00aa00"
  },
  "typography": {
    "font_family": "Inter, sans-serif",
    "title_size": "52px"
  },
  "spacing": {
    "slide_padding": "40px"
  },
  "effects": {
    "border_radius": "12px"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Custom theme 'My Brand Theme' created",
  "theme": {
    "id": "uuid-of-new-theme",
    "name": "My Brand Theme",
    "user_id": "user-uuid",
    "base_theme_id": "corporate-blue",
    "theme_config": { /* merged theme configuration */ },
    "created_at": "2024-12-08T...",
    "is_public": false
  }
}
```

#### List User's Themes

```http
GET /api/user/themes?user_id={user_id}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "themes": [
    {
      "id": "theme-uuid",
      "name": "My Brand Theme",
      "description": "...",
      "base_theme_id": "corporate-blue",
      "theme_config": {...},
      "created_at": "...",
      "updated_at": "...",
      "is_public": false
    }
  ]
}
```

#### Get Specific Custom Theme

```http
GET /api/user/themes/{theme_id}?user_id={user_id}
```

**Response:**
```json
{
  "success": true,
  "theme": {
    "id": "theme-uuid",
    "name": "My Brand Theme",
    "theme_config": {...},
    "resolved_theme": { /* fully resolved theme with base + overrides */ }
  }
}
```

#### Update Custom Theme

```http
PUT /api/user/themes/{theme_id}?user_id={user_id}
Content-Type: application/json
```

**Request Body (partial update):**
```json
{
  "name": "Updated Theme Name",
  "colors": {
    "primary": "#new-color"
  }
}
```

#### Delete Custom Theme

```http
DELETE /api/user/themes/{theme_id}?user_id={user_id}
```

#### Duplicate Custom Theme

```http
POST /api/user/themes/{theme_id}/duplicate?user_id={user_id}
Content-Type: application/json
```

**Request Body:**
```json
{
  "new_name": "My Theme Copy"
}
```

#### Publish Theme (Make Public)

```http
POST /api/user/themes/{theme_id}/publish?user_id={user_id}
```

---

### Presentation Theme API

#### Get Presentation Theme

```http
GET /api/presentations/{presentation_id}/theme
```

**Response:**
```json
{
  "theme_config": {
    "theme_id": "corporate-blue",
    "is_custom": false,
    "overrides": {
      "colors": { "primary": "#custom" }
    }
  },
  "resolved_theme": { /* fully resolved theme */ }
}
```

#### Set Presentation Theme

```http
PUT /api/presentations/{presentation_id}/theme
Content-Type: application/json
```

**Request Body:**
```json
{
  "theme_id": "corporate-blue",
  "is_custom": false,
  "overrides": {
    "colors": {
      "primary": "#ff5500",
      "accent": "#00aa00"
    },
    "typography": {
      "font_family": "Inter, sans-serif"
    },
    "spacing": {
      "slide_padding": "40px"
    },
    "effects": {
      "border_radius": "12px"
    }
  }
}
```

#### Get Theme CSS Variables

```http
GET /api/presentations/{presentation_id}/theme/css-variables
```

**Response:**
```json
{
  "css_variables": {
    "--theme-primary": "#1e40af",
    "--theme-accent": "#f59e0b",
    "--theme-bg": "#ffffff",
    "--theme-font-family": "Poppins, sans-serif"
  },
  "css_string": ":root { --theme-primary: #1e40af; --theme-accent: #f59e0b; ... }"
}
```

---

## PostMessage API

All theme operations can be performed via PostMessage to the presentation viewer iframe.

### Message Format

```javascript
iframe.contentWindow.postMessage({
  action: 'actionName',
  params: { /* action parameters */ }
}, '*');
```

### Listening for Responses

```javascript
window.addEventListener('message', (event) => {
  if (event.data.action === 'actionName') {
    if (event.data.success) {
      console.log('Success:', event.data);
    } else {
      console.error('Error:', event.data.error);
    }
  }
});
```

---

### Theme Actions Reference

#### setTheme

Apply a theme to the presentation with optional overrides.

```javascript
iframe.postMessage({
  action: 'setTheme',
  params: {
    themeId: 'corporate-blue',        // Required: theme ID
    isCustom: false,                   // Optional: true for user custom themes
    overrides: {                       // Optional: granular overrides
      colors: { primary: '#ff5500' },
      typography: { font_family: 'Inter' },
      spacing: { slide_padding: '40px' },
      effects: { border_radius: '12px' }
    }
  }
});
```

**Response:**
```json
{
  "action": "setTheme",
  "success": true,
  "themeConfig": { /* saved config */ },
  "resolvedTheme": { /* full resolved theme */ },
  "message": "Theme set to 'corporate-blue'"
}
```

#### previewTheme

Preview a theme without saving (for live UI preview).

```javascript
iframe.postMessage({
  action: 'previewTheme',
  params: {
    themeId: 'minimal-gray',
    overrides: {
      colors: { primary: '#custom' }
    }
  }
});
```

#### listThemes

Get list of available predefined themes.

```javascript
iframe.postMessage({ action: 'listThemes' });
```

**Response:**
```json
{
  "action": "listThemes",
  "success": true,
  "themes": ["corporate-blue", "minimal-gray", "vibrant-orange", "dark-mode"],
  "defaultTheme": "corporate-blue",
  "themeDetails": {
    "corporate-blue": { "id": "corporate-blue", "name": "Corporate Blue", "description": "..." }
  }
}
```

#### getTheme

Get current presentation theme.

```javascript
iframe.postMessage({
  action: 'getTheme',
  params: { presentationId: 'uuid' }  // Optional, uses current presentation
});
```

---

### User Theme Management Actions

#### createCustomTheme

Create a new custom theme in user's library.

```javascript
iframe.postMessage({
  action: 'createCustomTheme',
  params: {
    name: 'My Brand Theme',
    description: 'Company brand colors',
    baseThemeId: 'corporate-blue',  // Optional: inherit from predefined
    colors: { primary: '#ff5500', accent: '#00aa00' },
    typography: { font_family: 'Inter, sans-serif' },
    spacing: { slide_padding: '40px' },
    effects: { border_radius: '12px' }
  }
});
```

**Alternative format using overrides:**
```javascript
iframe.postMessage({
  action: 'createCustomTheme',
  params: {
    name: 'My Brand Theme',
    baseThemeId: 'corporate-blue',
    overrides: {
      colors: { primary: '#ff5500' },
      typography: { font_family: 'Inter' }
    }
  }
});
```

#### getUserThemes

Get all themes in user's library.

```javascript
iframe.postMessage({ action: 'getUserThemes' });
```

**Response:**
```json
{
  "action": "getUserThemes",
  "success": true,
  "themes": [ /* array of user themes */ ],
  "count": 3
}
```

#### getCustomTheme

Get a specific custom theme by ID.

```javascript
iframe.postMessage({
  action: 'getCustomTheme',
  params: { themeId: 'theme-uuid' }
});
```

#### updateCustomTheme

Update an existing custom theme.

```javascript
iframe.postMessage({
  action: 'updateCustomTheme',
  params: {
    themeId: 'theme-uuid',
    name: 'Updated Name',
    colors: { primary: '#new-color' }
  }
});
```

#### deleteCustomTheme

Delete a custom theme.

```javascript
iframe.postMessage({
  action: 'deleteCustomTheme',
  params: { themeId: 'theme-uuid' }
});
```

#### duplicateCustomTheme

Clone an existing theme.

```javascript
iframe.postMessage({
  action: 'duplicateCustomTheme',
  params: {
    themeId: 'theme-uuid',
    newName: 'Theme Copy'  // Optional
  }
});
```

#### saveThemeToLibrary

Save current presentation's theme to user's library.

```javascript
iframe.postMessage({
  action: 'saveThemeToLibrary',
  params: {
    name: 'My Saved Theme',
    description: 'Saved from presentation'
  }
});
```

#### getPublicThemes

Get all public themes (predefined + user-shared).

```javascript
iframe.postMessage({ action: 'getPublicThemes' });
```

**Response:**
```json
{
  "action": "getPublicThemes",
  "success": true,
  "predefinedThemes": [ /* predefined themes */ ],
  "userThemes": [ /* public user themes */ ]
}
```

#### getThemeCssVariables

Get CSS variables for current theme.

```javascript
iframe.postMessage({
  action: 'getThemeCssVariables',
  params: { presentationId: 'uuid' }  // Optional
});
```

**Response:**
```json
{
  "action": "getThemeCssVariables",
  "success": true,
  "cssVariables": { "--theme-primary": "#1e40af", ... },
  "cssString": ":root { --theme-primary: #1e40af; ... }"
}
```

#### applyCssVariables

Apply CSS variables directly (advanced use).

```javascript
iframe.postMessage({
  action: 'applyCssVariables',
  params: {
    cssVariables: {
      '--theme-primary': '#ff5500',
      '--theme-accent': '#00aa00',
      '--theme-font-family': 'Inter, sans-serif'
    }
  }
});
```

---

## CSS Variables Reference

All theme properties are exposed as CSS custom properties that can be used in your styles.

### Color Variables

| Variable | Description | Default (Corporate Blue) |
|----------|-------------|--------------------------|
| `--theme-primary` | Primary brand color | `#1e40af` |
| `--theme-primary-light` | Light primary variant | `#3b82f6` |
| `--theme-primary-dark` | Dark primary variant | `#1e3a8a` |
| `--theme-accent` | Accent/highlight color | `#f59e0b` |
| `--theme-bg` | Main background | `#ffffff` |
| `--theme-bg-alt` | Alternate background | `#f8fafc` |
| `--theme-text-primary` | Primary text | `#1f2937` |
| `--theme-text-secondary` | Secondary text | `#6b7280` |
| `--theme-text-body` | Body text | `#374151` |
| `--theme-hero-text-primary` | Hero primary text | `#ffffff` |
| `--theme-hero-text-secondary` | Hero secondary text | `#e5e7eb` |
| `--theme-hero-bg` | Hero background | `#1e3a5f` |
| `--theme-footer-text` | Footer text | `#6b7280` |
| `--theme-border` | Border color | `#e5e7eb` |

### Typography Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-font-family` | Primary font | `Poppins, sans-serif` |
| `--theme-font-family-heading` | Heading font | (inherits font-family) |
| `--theme-title-size` | Title font size | `48px` |
| `--theme-title-weight` | Title font weight | `bold` |
| `--theme-title-line-height` | Title line height | `1.2` |
| `--theme-subtitle-size` | Subtitle size | `32px` |
| `--theme-subtitle-weight` | Subtitle weight | `normal` |
| `--theme-subtitle-line-height` | Subtitle line height | `1.4` |
| `--theme-body-size` | Body text size | `24px` |
| `--theme-body-line-height` | Body line height | `1.6` |
| `--theme-footer-size` | Footer size | `14px` |
| `--theme-footer-weight` | Footer weight | `500` |
| `--theme-hero-title-size` | Hero title size | `72px` |
| `--theme-hero-title-weight` | Hero title weight | `bold` |
| `--theme-hero-title-shadow` | Hero title shadow | `0 2px 4px rgba(0,0,0,0.3)` |
| `--theme-hero-subtitle-size` | Hero subtitle size | `32px` |
| `--theme-hero-subtitle-weight` | Hero subtitle weight | `normal` |

### Spacing Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-slide-padding` | Slide padding | `60px` |
| `--theme-element-gap` | Gap between elements | `24px` |
| `--theme-section-gap` | Gap between sections | `48px` |

### Effect Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-border-radius` | Border radius | `8px` |
| `--theme-shadow-small` | Small shadow | `0 1px 3px rgba(0,0,0,0.1)` |
| `--theme-shadow-medium` | Medium shadow | `0 4px 6px rgba(0,0,0,0.1)` |
| `--theme-shadow-large` | Large shadow | `0 10px 15px rgba(0,0,0,0.1)` |

### Using CSS Variables

```css
/* In your component styles */
.my-element {
  background-color: var(--theme-primary);
  color: var(--theme-text-primary);
  font-family: var(--theme-font-family);
  padding: var(--theme-element-gap);
  border-radius: var(--theme-border-radius);
  box-shadow: var(--theme-shadow-medium);
}

.hero-section {
  background: var(--theme-hero-bg);
  color: var(--theme-hero-text-primary);
}
```

---

## Integration Examples

### Example 1: Theme Picker Component

```typescript
// React component example
import { useState, useEffect } from 'react';

interface ThemePickerProps {
  iframeRef: React.RefObject<HTMLIFrameElement>;
  onThemeChange: (themeId: string) => void;
}

export function ThemePicker({ iframeRef, onThemeChange }: ThemePickerProps) {
  const [themes, setThemes] = useState<any[]>([]);
  const [currentTheme, setCurrentTheme] = useState('corporate-blue');

  useEffect(() => {
    // Listen for theme list response
    const handleMessage = (event: MessageEvent) => {
      if (event.data.action === 'listThemes' && event.data.success) {
        setThemes(Object.values(event.data.themeDetails));
      }
    };
    window.addEventListener('message', handleMessage);

    // Request theme list
    iframeRef.current?.contentWindow?.postMessage({ action: 'listThemes' }, '*');

    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const handleThemeSelect = (themeId: string) => {
    iframeRef.current?.contentWindow?.postMessage({
      action: 'setTheme',
      params: { themeId }
    }, '*');
    setCurrentTheme(themeId);
    onThemeChange(themeId);
  };

  return (
    <div className="theme-picker">
      {themes.map(theme => (
        <button
          key={theme.id}
          className={currentTheme === theme.id ? 'active' : ''}
          onClick={() => handleThemeSelect(theme.id)}
        >
          {theme.name}
        </button>
      ))}
    </div>
  );
}
```

### Example 2: Color Customizer with Live Preview

```typescript
import { useState, useCallback, useRef } from 'react';
import debounce from 'lodash/debounce';

export function ColorCustomizer({ iframeRef, baseTheme }) {
  const [colors, setColors] = useState({
    primary: '#1e40af',
    accent: '#f59e0b'
  });

  // Debounced preview for performance
  const previewTheme = useCallback(
    debounce((newColors) => {
      iframeRef.current?.contentWindow?.postMessage({
        action: 'previewTheme',
        params: {
          themeId: baseTheme,
          overrides: { colors: newColors }
        }
      }, '*');
    }, 100),
    [baseTheme]
  );

  const handleColorChange = (colorKey: string, value: string) => {
    const newColors = { ...colors, [colorKey]: value };
    setColors(newColors);
    previewTheme(newColors);
  };

  const handleSave = () => {
    iframeRef.current?.contentWindow?.postMessage({
      action: 'setTheme',
      params: {
        themeId: baseTheme,
        overrides: { colors }
      }
    }, '*');
  };

  return (
    <div className="color-customizer">
      <div className="color-input">
        <label>Primary Color</label>
        <input
          type="color"
          value={colors.primary}
          onChange={(e) => handleColorChange('primary', e.target.value)}
        />
      </div>
      <div className="color-input">
        <label>Accent Color</label>
        <input
          type="color"
          value={colors.accent}
          onChange={(e) => handleColorChange('accent', e.target.value)}
        />
      </div>
      <button onClick={handleSave}>Apply Theme</button>
    </div>
  );
}
```

### Example 3: User Theme Library

```typescript
export function ThemeLibrary({ iframeRef, userId }) {
  const [userThemes, setUserThemes] = useState([]);
  const [publicThemes, setPublicThemes] = useState([]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data.action === 'getUserThemes' && event.data.success) {
        setUserThemes(event.data.themes);
      }
      if (event.data.action === 'getPublicThemes' && event.data.success) {
        setPublicThemes([
          ...event.data.predefinedThemes,
          ...event.data.userThemes
        ]);
      }
    };
    window.addEventListener('message', handleMessage);

    // Fetch themes
    iframeRef.current?.contentWindow?.postMessage({ action: 'getUserThemes' }, '*');
    iframeRef.current?.contentWindow?.postMessage({ action: 'getPublicThemes' }, '*');

    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const applyTheme = (theme) => {
    iframeRef.current?.contentWindow?.postMessage({
      action: 'setTheme',
      params: {
        themeId: theme.id,
        isCustom: !theme.is_predefined
      }
    }, '*');
  };

  const createTheme = () => {
    iframeRef.current?.contentWindow?.postMessage({
      action: 'createCustomTheme',
      params: {
        name: 'New Theme',
        baseThemeId: 'corporate-blue',
        colors: { primary: '#ff5500' }
      }
    }, '*');
  };

  const deleteTheme = (themeId) => {
    iframeRef.current?.contentWindow?.postMessage({
      action: 'deleteCustomTheme',
      params: { themeId }
    }, '*');
  };

  return (
    <div className="theme-library">
      <section>
        <h3>My Themes</h3>
        <button onClick={createTheme}>+ Create New Theme</button>
        {userThemes.map(theme => (
          <div key={theme.id} className="theme-card">
            <span>{theme.name}</span>
            <button onClick={() => applyTheme(theme)}>Apply</button>
            <button onClick={() => deleteTheme(theme.id)}>Delete</button>
          </div>
        ))}
      </section>

      <section>
        <h3>Public Themes</h3>
        {publicThemes.map(theme => (
          <div key={theme.id} className="theme-card">
            <span>{theme.name}</span>
            <button onClick={() => applyTheme(theme)}>Apply</button>
          </div>
        ))}
      </section>
    </div>
  );
}
```

### Example 4: Save Current Theme to Library

```typescript
export function SaveThemeButton({ iframeRef }) {
  const [saving, setSaving] = useState(false);

  const saveToLibrary = async () => {
    setSaving(true);

    const themeName = prompt('Enter theme name:');
    if (!themeName) {
      setSaving(false);
      return;
    }

    // Listen for response
    const handleMessage = (event: MessageEvent) => {
      if (event.data.action === 'saveThemeToLibrary') {
        setSaving(false);
        if (event.data.success) {
          alert(`Theme saved: ${event.data.theme.name}`);
        } else {
          alert(`Error: ${event.data.error}`);
        }
        window.removeEventListener('message', handleMessage);
      }
    };
    window.addEventListener('message', handleMessage);

    iframeRef.current?.contentWindow?.postMessage({
      action: 'saveThemeToLibrary',
      params: {
        name: themeName,
        description: 'Saved from presentation editor'
      }
    }, '*');
  };

  return (
    <button onClick={saveToLibrary} disabled={saving}>
      {saving ? 'Saving...' : 'Save Theme to Library'}
    </button>
  );
}
```

---

## Migration Guide

### From v7.5.3 to v7.5.4

#### Breaking Changes
None. All existing theme APIs remain backward compatible.

#### New Features

1. **Full Theme Overrides**: The `setTheme` action now accepts full overrides:
   ```javascript
   // Old (still works)
   { action: 'setTheme', params: { themeId: 'x', colorOverrides: {...} } }

   // New (recommended)
   { action: 'setTheme', params: { themeId: 'x', overrides: { colors: {...}, typography: {...} } } }
   ```

2. **User Theme Library**: New actions for managing custom themes:
   - `createCustomTheme`
   - `getUserThemes`
   - `updateCustomTheme`
   - `deleteCustomTheme`
   - `duplicateCustomTheme`
   - `saveThemeToLibrary`

3. **New CSS Variables**: Additional variables for spacing and effects:
   - `--theme-slide-padding`
   - `--theme-element-gap`
   - `--theme-section-gap`
   - `--theme-border-radius`
   - `--theme-shadow-small/medium/large`

#### Database Migration Required

Run the migration to create the user themes table:
```sql
-- Run: migrations/003_add_user_custom_themes.sql
```

---

## Troubleshooting

### Common Issues

#### Theme not applying
1. Ensure the iframe is fully loaded before sending messages
2. Check browser console for errors
3. Verify theme ID exists (use `listThemes` first)

#### Custom themes not saving
1. Verify the `ls_user_themes` table exists (run migration)
2. Check user_id is being passed correctly
3. Verify Supabase connection is working

#### CSS variables not updating
1. Check ThemeManager is loaded in the iframe
2. Verify the theme includes the property you're trying to set
3. Use browser DevTools to inspect `:root` CSS variables

### Debug Mode

Enable console logging for theme operations:
```javascript
// In browser console on the iframe
localStorage.setItem('THEME_DEBUG', 'true');
```

---

## Support

For questions or issues:
- Check the [Layout Service API Documentation](/api/docs)
- Review the [PostMessage Bridge Documentation](/docs/POSTMESSAGE_API.md)
- Contact the backend team for API issues
