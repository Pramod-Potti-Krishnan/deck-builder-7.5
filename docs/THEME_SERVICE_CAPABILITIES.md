# Theme Service Capabilities

**Service**: Layout Service v7.5-main
**Version**: 7.5.7
**Last Updated**: December 2024

---

## Overview

The Theme Service provides comprehensive visual theming for presentations, including:

- **4 Predefined Themes** with distinct color palettes and typography
- **User Custom Themes** with full CRUD operations
- **Theme Inheritance** from predefined base themes
- **Granular Overrides** for colors, typography, spacing, and effects
- **Real-time Preview** without database persistence
- **CSS Variable System** for instant visual updates

---

## Quick Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/themes` | GET | List all predefined themes |
| `/api/themes/public` | GET | List predefined + public user themes |
| `/api/themes/{theme_id}` | GET | Get specific theme details |
| `/api/themes/{theme_id}/typography` | GET | **NEW** - Get typography tokens for Text Service |
| `/api/presentations/{id}/theme` | GET | Get presentation's theme |
| `/api/presentations/{id}/theme` | PUT | Set presentation theme |
| `/api/presentations/{id}/theme/css-variables` | GET | Get theme as CSS variables |
| `/api/user/themes` | POST | Create custom theme |
| `/api/user/themes` | GET | List user's custom themes |
| `/api/user/themes/{id}` | GET | Get custom theme details |
| `/api/user/themes/{id}` | PUT | Update custom theme |
| `/api/user/themes/{id}` | DELETE | Delete custom theme |
| `/api/user/themes/{id}/duplicate` | POST | Clone a theme |
| `/api/user/themes/{id}/publish` | POST | Make theme public |

### PostMessage Actions

| Action | Description |
|--------|-------------|
| `listThemes` | Get available predefined themes |
| `getTheme` | Get current presentation theme (data only) |
| `setTheme` | Apply and save theme |
| `previewTheme` | Preview theme without saving |
| `createCustomTheme` | Create new user theme |
| `getUserThemes` | List user's theme library |
| `getCustomTheme` | Get specific custom theme |
| `updateCustomTheme` | Update custom theme |
| `deleteCustomTheme` | Delete custom theme |
| `duplicateCustomTheme` | Clone a theme |
| `saveThemeToLibrary` | Save current theme to library |
| `getPublicThemes` | Get all public themes |
| `getThemeCssVariables` | Get CSS variable string |
| `applyCssVariables` | Apply CSS variables directly |

---

## Predefined Themes

### Available Themes (4)

| Theme ID | Name | Primary Color | Accent | Description |
|----------|------|---------------|--------|-------------|
| `corporate-blue` | Corporate Blue | `#1e40af` | `#f59e0b` | Professional business theme (default) |
| `elegant-emerald` | Elegant Emerald | `#059669` | `#fbbf24` | Sophisticated nature-inspired theme |
| `vibrant-orange` | Vibrant Orange | `#ea580c` | `#0891b2` | Energetic creative theme |
| `dark-mode` | Dark Mode | `#60a5fa` | `#fbbf24` | Modern dark theme |

### Theme Color Palette

Each theme defines **14 color properties**:

```
Primary Colors (3)
├── primary           # Main brand color
├── primary_light     # Lighter variant
└── primary_dark      # Darker variant

Semantic Colors (5)
├── accent            # Highlight/CTA color
├── background        # Main background
├── background_alt    # Alternate background
├── border            # Border color
└── footer_text       # Footer text

Text Colors (3)
├── text_primary      # Primary text
├── text_secondary    # Secondary text
└── text_body         # Body text

Hero Slide Colors (3)
├── hero_text_primary    # Hero title color
├── hero_text_secondary  # Hero subtitle color
└── hero_background      # Hero slide background
```

---

## Theme Data Model

### Full Theme Structure

```typescript
interface Theme {
  id: string;
  name: string;
  description?: string;
  colors: ThemeColors;
  typography: ThemeTypography;
  spacing?: ThemeSpacing;
  effects?: ThemeEffects;
  content_styles?: ContentStyles;
  is_custom: boolean;
}

interface ThemeColors {
  primary: string;
  primary_light: string;
  primary_dark: string;
  accent: string;
  background: string;
  background_alt: string;
  text_primary: string;
  text_secondary: string;
  text_body: string;
  hero_text_primary: string;
  hero_text_secondary: string;
  hero_background: string;
  footer_text: string;
  border: string;
}

interface ThemeTypography {
  font_family: string;
  font_family_heading?: string;

  // Standard slides
  title_size: string;
  title_weight: string;
  title_line_height: string;
  subtitle_size: string;
  subtitle_weight: string;
  subtitle_line_height: string;
  body_size: string;
  body_line_height: string;
  footer_size: string;
  footer_weight: string;

  // Hero slides
  hero_title_size: string;
  hero_title_weight: string;
  hero_title_shadow: string;
  hero_subtitle_size: string;
  hero_subtitle_weight: string;
}

interface ThemeSpacing {
  slide_padding: string;    // Default: "60px"
  element_gap: string;      // Default: "24px"
  section_gap: string;      // Default: "48px"
}

interface ThemeEffects {
  border_radius: string;    // Default: "8px"
  shadow_small: string;
  shadow_medium: string;
  shadow_large: string;
}
```

### Presentation Theme Config (stored)

```typescript
interface PresentationThemeConfig {
  theme_id: string;
  is_custom?: boolean;
  overrides?: {
    colors?: Partial<ThemeColors>;
    typography?: Partial<ThemeTypography>;
    spacing?: Partial<ThemeSpacing>;
    effects?: Partial<ThemeEffects>;
  };
}
```

---

## CSS Variables Reference

The theme system injects **40+ CSS custom properties** that can be used in any component.

### Color Variables

| Variable | Description |
|----------|-------------|
| `--theme-primary` | Primary brand color |
| `--theme-primary-light` | Light primary variant |
| `--theme-primary-dark` | Dark primary variant |
| `--theme-accent` | Accent/highlight color |
| `--theme-bg` | Main background |
| `--theme-bg-alt` | Alternate background |
| `--theme-text-primary` | Primary text color |
| `--theme-text-secondary` | Secondary text color |
| `--theme-text-body` | Body text color |
| `--theme-hero-text-primary` | Hero title color |
| `--theme-hero-text-secondary` | Hero subtitle color |
| `--theme-hero-bg` | Hero background |
| `--theme-footer-text` | Footer text color |
| `--theme-border` | Border color |

### Typography Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-font-family` | Primary font | Poppins |
| `--theme-font-family-heading` | Heading font | (inherits) |
| `--theme-title-size` | Title size | 48px |
| `--theme-title-weight` | Title weight | bold |
| `--theme-subtitle-size` | Subtitle size | 32px |
| `--theme-body-size` | Body size | 24px |
| `--theme-hero-title-size` | Hero title | 72px |
| `--theme-hero-subtitle-size` | Hero subtitle | 32px |

### Spacing Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-slide-padding` | Slide padding | 60px |
| `--theme-element-gap` | Element gap | 24px |
| `--theme-section-gap` | Section gap | 48px |

### Effect Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `--theme-border-radius` | Border radius | 8px |
| `--theme-shadow-small` | Small shadow | 0 1px 3px rgba(0,0,0,0.1) |
| `--theme-shadow-medium` | Medium shadow | 0 4px 6px rgba(0,0,0,0.1) |
| `--theme-shadow-large` | Large shadow | 0 10px 15px rgba(0,0,0,0.1) |

---

## API Details

### 1. GET /api/themes

List all predefined themes.

**Response:**
```json
{
  "predefined": ["corporate-blue", "elegant-emerald", "vibrant-orange", "dark-mode"],
  "default": "corporate-blue",
  "themes": {
    "corporate-blue": { /* full theme object */ }
  }
}
```

### 2. GET /api/themes/{theme_id}

Get specific theme details.

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

### 3. GET /api/presentations/{id}/theme

Get presentation's current theme.

**Response:**
```json
{
  "theme_config": {
    "theme_id": "corporate-blue",
    "is_custom": false,
    "overrides": null
  },
  "resolved_theme": { /* fully resolved theme with overrides applied */ }
}
```

### 4. PUT /api/presentations/{id}/theme

Set presentation theme with optional overrides.

**Request:**
```json
{
  "theme_id": "vibrant-orange",
  "is_custom": false,
  "overrides": {
    "colors": {
      "primary": "#ff5500",
      "accent": "#00aa00"
    },
    "typography": {
      "font_family": "Inter, sans-serif"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Theme set to 'vibrant-orange'",
  "theme_config": { /* saved config */ },
  "resolved_theme": { /* full resolved theme */ }
}
```

### 5. POST /api/user/themes

Create a new custom theme.

**Request:**
```json
{
  "name": "My Brand Theme",
  "description": "Company brand colors",
  "base_theme_id": "corporate-blue",
  "colors": { "primary": "#ff5500" },
  "typography": { "font_family": "Inter, sans-serif" },
  "spacing": { "slide_padding": "40px" },
  "effects": { "border_radius": "12px" }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Custom theme 'My Brand Theme' created",
  "theme": {
    "id": "uuid",
    "name": "My Brand Theme",
    "user_id": "user-uuid",
    "base_theme_id": "corporate-blue",
    "theme_config": { /* merged config */ },
    "is_public": false
  }
}
```

### 6. GET /api/presentations/{id}/theme/css-variables

Get theme as CSS variables string.

**Response:**
```json
{
  "css_variables": {
    "--theme-primary": "#1e40af",
    "--theme-accent": "#f59e0b"
  },
  "css_string": ":root { --theme-primary: #1e40af; --theme-accent: #f59e0b; ... }"
}
```

### 7. GET /api/themes/{theme_id}/typography (NEW v7.5.7)

Returns typography tokens for Text Service character constraint calculations.

**Response:**
```json
{
  "theme_id": "corporate-blue",
  "font_family": "Poppins, sans-serif",
  "font_family_heading": "Poppins, sans-serif",
  "tokens": {
    "h1": {"size": 72, "size_px": "72px", "weight": 700, "line_height": 1.2, "letter_spacing": "-0.02em", "color": "#1f2937"},
    "h2": {"size": 42, "size_px": "42px", "weight": 700, "line_height": 1.3, "color": "#1f2937"},
    "h3": {"size": 22, "size_px": "22px", "weight": 600, "line_height": 1.4, "color": "#1f2937"},
    "h4": {"size": 18, "size_px": "18px", "weight": 600, "line_height": 1.4, "color": "#374151"},
    "body": {"size": 20, "size_px": "20px", "weight": 400, "line_height": 1.6, "color": "#374151"},
    "subtitle": {"size": 24, "size_px": "24px", "weight": 400, "line_height": 1.5, "color": "#6b7280"},
    "caption": {"size": 16, "size_px": "16px", "weight": 400, "line_height": 1.4, "color": "#6b7280"},
    "emphasis": {"weight": 600, "color": "#1f2937", "style": "normal"}
  },
  "list_styles": {
    "bullet_type": "disc",
    "bullet_color": "#1e40af",
    "bullet_size": "0.4em",
    "list_indent": "24px",
    "item_spacing": "6px",
    "numbered_style": "decimal",
    "nested_indent": "1.5em"
  },
  "textbox_defaults": {
    "background": "transparent",
    "border_radius": "8px",
    "padding": "16px",
    "box_shadow": "none"
  },
  "char_width_ratio": 0.5
}
```

**Character Width Ratios by Theme:**

| Theme | Font | Char Ratio |
|-------|------|------------|
| corporate-blue | Poppins | 0.50 |
| elegant-emerald | Lato | 0.47 |
| vibrant-orange | Montserrat | 0.52 |
| dark-mode | Inter | 0.48 |

**Text Service Integration:**

```python
# Calculate character constraints using typography tokens
typography = requests.get(f"{THEME_SERVICE}/api/themes/{theme_id}/typography").json()

font_size = typography["tokens"]["body"]["size"]  # 20
line_height = typography["tokens"]["body"]["line_height"]  # 1.6
char_ratio = typography["char_width_ratio"]  # 0.5

# Calculate for a 1800px wide content area
content_width = 1800
avg_char_width = font_size * char_ratio  # 10px
chars_per_line = content_width / avg_char_width  # 180

# Apply list styling
bullet_color = typography["list_styles"]["bullet_color"]  # "#1e40af"
```

---

## PostMessage API

### Send Command Pattern

```javascript
iframe.contentWindow.postMessage({
  action: 'actionName',
  params: { /* parameters */ }
}, iframeOrigin);
```

### Receive Response Pattern

```javascript
window.addEventListener('message', (event) => {
  const { success, action, error, ...data } = event.data;
  if (success) {
    // Handle success
  } else {
    console.error(error);
  }
});
```

### Key Actions

#### setTheme (Apply and Save)

```javascript
iframe.postMessage({
  action: 'setTheme',
  params: {
    themeId: 'corporate-blue',
    isCustom: false,
    overrides: {
      colors: { primary: '#ff5500' }
    }
  }
});
```

#### previewTheme (Preview Only)

```javascript
iframe.postMessage({
  action: 'previewTheme',
  params: {
    themeId: 'dark-mode',
    overrides: { colors: { accent: '#00ff00' } }
  }
});
```

#### createCustomTheme

```javascript
iframe.postMessage({
  action: 'createCustomTheme',
  params: {
    name: 'My Theme',
    baseThemeId: 'corporate-blue',
    colors: { primary: '#ff5500' }
  }
});
```

---

## Theme Support by Template

Currently, only **H-series (hero) templates** fully respond to theme CSS variables:

| Template | Theme Support | Notes |
|----------|---------------|-------|
| H1-generated | YES | Full theming |
| H1-structured | YES | Full theming |
| H2-section | YES | Full theming |
| H3-closing | YES | Full theming |
| C1-C5 | Partial | Colors via CSS variables |
| V1-V4 | Partial | Colors via CSS variables |
| I1-I4 | Partial | Colors via CSS variables |
| S3-S4 | Partial | Colors via CSS variables |
| B1-blank | NO | No theming |
| L02, L25, L29 | Partial | Backend layouts |

---

## Style Cascade Priority

Styles are computed with this priority (lowest to highest):

1. **Slot Defaults** - Base typography from slot definitions
2. **Theme Typography** - Theme-specific overrides
3. **Template-specific** - Per-template slot styles
4. **Color Overrides** - Presentation-level customizations
5. **Inline Styles** - Per-element inline overrides

---

## Auto-Apply on Load

Themes are **automatically applied** when a presentation loads:

1. Viewer checks `theme_config.theme_id` in presentation data
2. If found, applies that theme's CSS variables
3. If not found, applies default theme (`corporate-blue`)

**Frontend does NOT need to call any theme action on page load.**

---

## Database Schema

### presentations table

```sql
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS theme_config JSONB;
```

### user_themes table

```sql
CREATE TABLE ls_user_themes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  base_theme_id VARCHAR(50),
  theme_config JSONB NOT NULL,
  is_public BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

---

## Usage Examples

### Basic Theme Selection

```javascript
// List available themes
iframe.postMessage({ action: 'listThemes' });

// Apply a theme
iframe.postMessage({
  action: 'setTheme',
  params: { themeId: 'dark-mode' }
});
```

### Theme with Custom Colors

```javascript
iframe.postMessage({
  action: 'setTheme',
  params: {
    themeId: 'corporate-blue',
    overrides: {
      colors: {
        primary: '#ff5500',
        accent: '#00aa00'
      }
    }
  }
});
```

### Create Brand Theme

```javascript
iframe.postMessage({
  action: 'createCustomTheme',
  params: {
    name: 'Acme Corp',
    description: 'Official company theme',
    baseThemeId: 'corporate-blue',
    colors: {
      primary: '#AC1E2D',
      accent: '#FFD700',
      hero_background: '#1a1a1a'
    },
    typography: {
      font_family: 'Roboto, sans-serif',
      hero_title_size: '80px'
    }
  }
});
```

### Live Preview for Theme Picker

```javascript
// Preview on hover/click (doesn't save)
themeButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    iframe.postMessage({
      action: 'previewTheme',
      params: { themeId: btn.dataset.themeId }
    });
  });
});

// Save on confirm
confirmBtn.addEventListener('click', () => {
  iframe.postMessage({
    action: 'setTheme',
    params: { themeId: selectedThemeId }
  });
});
```

---

## Changelog

### v7.5.7 (December 2024)
- Added `GET /api/themes/{theme_id}/typography` endpoint for Text Service
- Typography tokens for h1-h4, body, subtitle, caption, emphasis
- List styles with bullet_type, bullet_color, item_spacing
- Textbox defaults for container styling
- Font char_width_ratio for character constraint calculations
- Support for both predefined and custom user themes

### v7.5.6 (December 2024)
- Added Elegant Emerald theme
- Enhanced typography controls

### v7.5.4 (December 2024)
- Added user custom themes (CRUD)
- Added spacing and effects overrides
- Added public theme sharing
- New CSS variables for spacing/effects

### v7.5.3 (December 2024)
- Initial theme system
- 4 predefined themes
- Color overrides support
- PostMessage API

---

## Files Reference

| File | Description |
|------|-------------|
| `src/themes/theme-registry.js` | Client-side theme definitions |
| `src/themes/theme-manager.js` | CSS variable injection |
| `src/styles/theme-variables.css` | CSS variable defaults |
| `migrations/002_add_theme_config.sql` | theme_config column |
| `migrations/003_add_user_custom_themes.sql` | user_themes table |
