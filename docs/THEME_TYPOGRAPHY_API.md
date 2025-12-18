# Theme Typography API

**Version**: v7.5.7
**Date**: December 2024
**Status**: Production

---

## Overview

The Theme Typography API provides granular typography tokens for the Text Service (Elementor) to calculate character constraints and apply theme-consistent styling. This endpoint transforms existing theme data into a text-service-friendly format.

---

## API Endpoint

### GET `/api/themes/{theme_id}/typography`

Returns complete typography tokens for a theme.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `theme_id` | string | Yes | Theme identifier (predefined ID or custom UUID) |

**Predefined Theme IDs:**
- `corporate-blue` (default)
- `elegant-emerald`
- `vibrant-orange`
- `dark-mode`

---

## Response Structure

```json
{
  "theme_id": "corporate-blue",
  "font_family": "Poppins, sans-serif",
  "font_family_heading": "Poppins, sans-serif",
  "tokens": {
    "h1": { ... },
    "h2": { ... },
    "h3": { ... },
    "h4": { ... },
    "body": { ... },
    "subtitle": { ... },
    "caption": { ... },
    "emphasis": { ... }
  },
  "list_styles": { ... },
  "textbox_defaults": { ... },
  "char_width_ratio": 0.5
}
```

---

## Typography Tokens

### Heading Tokens (h1-h4)

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `size` | int | Font size in pixels (numeric) | `72` |
| `size_px` | string | Font size as CSS value | `"72px"` |
| `weight` | int | Font weight (100-900) | `700` |
| `line_height` | float | Line height multiplier | `1.2` |
| `letter_spacing` | string | Letter spacing | `"-0.02em"` |
| `color` | string | Text color (hex) | `"#1f2937"` |
| `text_transform` | string | Text transform | `"none"` |

### Body, Subtitle, Caption Tokens

Same structure as heading tokens, with appropriate defaults for each text type.

### Emphasis Token

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `weight` | int | Font weight for emphasis | `600` |
| `color` | string | Emphasis text color | `"#1f2937"` |
| `style` | string | Font style | `"normal"` |

---

## List Styles

| Property | Type | Description | Options/Default |
|----------|------|-------------|-----------------|
| `bullet_type` | string | Bullet character type | `disc`, `circle`, `square`, `dash`, `arrow`, `check`, `none` |
| `bullet_color` | string | Bullet color (hex) | Theme primary color |
| `bullet_size` | string | Bullet size | `"0.4em"` |
| `list_indent` | string | List indentation | `"1.5em"` |
| `item_spacing` | string | Space between items | `"0.5em"` |
| `numbered_style` | string | Numbered list format | `decimal`, `lower-alpha`, `upper-alpha`, `lower-roman`, `upper-roman` |
| `nested_indent` | string | Nested list indent | `"1.5em"` |

---

## Textbox Defaults

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `background` | string | Background color | `"transparent"` |
| `background_gradient` | string/null | CSS gradient | `null` |
| `border_width` | string | Border width | `"0px"` |
| `border_color` | string | Border color | `"transparent"` |
| `border_radius` | string | Corner radius | `"8px"` |
| `padding` | string | Inner padding | `"16px"` |
| `box_shadow` | string | Box shadow | `"none"` |

---

## Character Width Ratios

The `char_width_ratio` is used to calculate average character width:

```
avg_char_width = font_size * char_width_ratio
```

| Font Family | Char Width Ratio |
|-------------|------------------|
| Poppins | 0.50 |
| Inter | 0.48 |
| Roboto | 0.47 |
| Open Sans | 0.49 |
| Montserrat | 0.52 |
| Lato | 0.47 |
| Playfair Display | 0.45 |
| (default) | 0.50 |

---

## Complete Response Examples

### Corporate Blue

```json
{
  "theme_id": "corporate-blue",
  "font_family": "Poppins, sans-serif",
  "font_family_heading": "Poppins, sans-serif",
  "tokens": {
    "h1": {
      "size": 72,
      "size_px": "72px",
      "weight": 700,
      "line_height": 1.2,
      "letter_spacing": "-0.02em",
      "color": "#1f2937",
      "text_transform": "none"
    },
    "h2": {
      "size": 42,
      "size_px": "42px",
      "weight": 700,
      "line_height": 1.3,
      "letter_spacing": "-0.01em",
      "color": "#1f2937",
      "text_transform": "none"
    },
    "h3": {
      "size": 22,
      "size_px": "22px",
      "weight": 600,
      "line_height": 1.4,
      "letter_spacing": "0",
      "color": "#1f2937",
      "text_transform": "none"
    },
    "h4": {
      "size": 18,
      "size_px": "18px",
      "weight": 600,
      "line_height": 1.4,
      "letter_spacing": "0",
      "color": "#374151",
      "text_transform": "none"
    },
    "body": {
      "size": 20,
      "size_px": "20px",
      "weight": 400,
      "line_height": 1.6,
      "letter_spacing": "0",
      "color": "#374151"
    },
    "subtitle": {
      "size": 24,
      "size_px": "24px",
      "weight": 400,
      "line_height": 1.5,
      "letter_spacing": "0",
      "color": "#6b7280",
      "text_transform": "none"
    },
    "caption": {
      "size": 16,
      "size_px": "16px",
      "weight": 400,
      "line_height": 1.4,
      "letter_spacing": "0.01em",
      "color": "#6b7280"
    },
    "emphasis": {
      "weight": 600,
      "color": "#1f2937",
      "style": "normal"
    }
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
    "background_gradient": null,
    "border_width": "0px",
    "border_color": "transparent",
    "border_radius": "8px",
    "padding": "16px",
    "box_shadow": "none"
  },
  "char_width_ratio": 0.5
}
```

### Dark Mode

```json
{
  "theme_id": "dark-mode",
  "font_family": "Inter, sans-serif",
  "font_family_heading": "Inter, sans-serif",
  "tokens": {
    "h1": {
      "size": 68,
      "size_px": "68px",
      "weight": 600,
      "line_height": 1.2,
      "letter_spacing": "-0.02em",
      "color": "#f9fafb",
      "text_transform": "none"
    },
    "body": {
      "size": 20,
      "size_px": "20px",
      "weight": 400,
      "line_height": 1.6,
      "letter_spacing": "0",
      "color": "#e5e7eb"
    }
  },
  "list_styles": {
    "bullet_color": "#60a5fa"
  },
  "char_width_ratio": 0.48
}
```

---

## Text Service Integration

### Calculating Character Constraints

```python
def calculate_text_constraints(grid_width, grid_height, typography):
    """Calculate max characters for a text element."""
    font_size = typography["tokens"]["body"]["size"]
    line_height = typography["tokens"]["body"]["line_height"]
    char_ratio = typography["char_width_ratio"]

    # Calculate pixel dimensions (60px per grid cell)
    content_width = (grid_width * 60) - 32  # minus padding
    content_height = (grid_height * 60) - 32

    # Calculate constraints
    avg_char_width = font_size * char_ratio
    line_height_px = font_size * line_height

    chars_per_line = content_width / avg_char_width
    max_lines = content_height / line_height_px
    max_characters = chars_per_line * max_lines * 0.9  # 90% fill

    return {
        "chars_per_line": int(chars_per_line),
        "max_lines": int(max_lines),
        "max_characters": int(max_characters)
    }
```

### Applying Theme Styles

```html
<div style="
  font-family: ${typography.font_family};
  font-size: ${typography.tokens.body.size_px};
  font-weight: ${typography.tokens.body.weight};
  line-height: ${typography.tokens.body.line_height};
  color: ${typography.tokens.body.color};
">
  <ul style="
    list-style-type: ${typography.list_styles.bullet_type};
    padding-left: ${typography.list_styles.list_indent};
  ">
    <li style="margin-bottom: ${typography.list_styles.item_spacing};">
      Item text
    </li>
  </ul>
</div>
```

---

## Error Responses

### 404 Not Found

```json
{
  "detail": "Theme 'unknown-theme' not found. Available predefined themes: ['corporate-blue', 'elegant-emerald', 'vibrant-orange', 'dark-mode']"
}
```

---

## Fallback Behavior

If the Theme Service is unavailable, the Text Service should use built-in defaults:

```python
DEFAULT_TYPOGRAPHY = {
    "font_family": "Poppins, sans-serif",
    "tokens": {
        "h1": {"size": 72, "weight": 700, "line_height": 1.2, "color": "#1f2937"},
        "h2": {"size": 42, "weight": 600, "line_height": 1.3, "color": "#1f2937"},
        "h3": {"size": 22, "weight": 600, "line_height": 1.4, "color": "#1f2937"},
        "h4": {"size": 18, "weight": 600, "line_height": 1.4, "color": "#374151"},
        "body": {"size": 20, "weight": 400, "line_height": 1.6, "color": "#374151"},
        "subtitle": {"size": 24, "weight": 400, "line_height": 1.5, "color": "#6b7280"},
        "caption": {"size": 16, "weight": 400, "line_height": 1.4, "color": "#9ca3af"},
        "emphasis": {"weight": 600, "color": "#1f2937"}
    },
    "char_width_ratio": 0.5
}
```

---

## cURL Examples

### Get Corporate Blue Typography

```bash
curl http://localhost:8504/api/themes/corporate-blue/typography
```

### Get All Predefined Themes

```bash
for theme in corporate-blue elegant-emerald vibrant-orange dark-mode; do
  echo "=== $theme ==="
  curl -s "http://localhost:8504/api/themes/$theme/typography" | jq '.char_width_ratio, .font_family'
done
```

---

## Changelog

### v7.5.7 (December 2024)
- Added `GET /api/themes/{theme_id}/typography` endpoint
- Added typography token models (`TypographyToken`, `ListStylesToken`, etc.)
- Added `build_typography_response()` transformation helper
- Added `FONT_CHAR_WIDTH_RATIOS` lookup table
- Support for both predefined and custom user themes
