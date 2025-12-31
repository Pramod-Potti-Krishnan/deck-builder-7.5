# Layout Service Theme API Reference

> **Version:** 7.5.5
> **Last Updated:** December 2024

## Theme API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/themes/sync` | GET | Bulk sync for Text Service/Director startup |
| `/api/themes/public` | GET | List all public themes (predefined + user) |
| `/api/themes/{theme_id}` | GET | Get single theme by ID |
| `/api/themes/{theme_id}/typography` | GET | Get typography tokens for Text Service |

---

## `/api/themes/sync`

Bulk sync endpoint for Text Service and Director. Returns all predefined themes in a single response with version tracking.

### Response Format

```json
{
  "themes": {
    "corporate-blue": {
      "typography": { "fontFamily": "...", "standard": {...}, "hero": {...} },
      "colors": {
        "primary": "#1e40af",
        "primary_light": "#3b82f6",
        "primary_dark": "#1e3a8a",
        "accent": "#f59e0b",
        "background": "#ffffff",
        "background_alt": "#f8fafc",
        "text_primary": "#1f2937",
        "text_secondary": "#6b7280",
        "text_body": "#374151",
        "hero_text_primary": "#ffffff",
        "hero_text_secondary": "#e5e7eb",
        "hero_background": "#1e3a5f",
        "footer_text": "#6b7280",
        "border": "#e5e7eb",
        "tertiary_1": "#f8fafc",
        "tertiary_2": "#e2e8f0",
        "tertiary_3": "#94a3b8",
        "chart_1": "#3b82f6",
        "chart_2": "#10b981",
        "chart_3": "#f59e0b",
        "chart_4": "#ef4444",
        "chart_5": "#8b5cf6",
        "chart_6": "#ec4899"
      },
      "content_styles": { "h1": {...}, "h2": {...}, ... }
    },
    "elegant-emerald": {...},
    "vibrant-orange": {...},
    "dark-mode": {...}
  },
  "version": "1.0.0",
  "last_updated": "2025-12-21T02:40:06.583045Z"
}
```

---

## Color Palette (23 keys per theme)

All color keys use **snake_case** for Python/Pydantic compatibility.

| Category | Keys | Description |
|----------|------|-------------|
| **Primary** | `primary`, `primary_light`, `primary_dark` | Main brand colors |
| **Accent** | `accent` | Highlight/emphasis color |
| **Background** | `background`, `background_alt` | Slide backgrounds |
| **Text (Standard)** | `text_primary`, `text_secondary`, `text_body` | Dark text on light bg |
| **Text (Hero)** | `hero_text_primary`, `hero_text_secondary`, `hero_background` | Light text on dark bg |
| **UI** | `footer_text`, `border` | UI element colors |
| **Tertiary** | `tertiary_1`, `tertiary_2`, `tertiary_3` | Groupings, borders, dividers |
| **Charts** | `chart_1` - `chart_6` | Data visualization colors |

---

## Predefined Themes

| Theme ID | Primary Color | Description | Chart Palette |
|----------|---------------|-------------|---------------|
| `corporate-blue` | #1e40af | Professional business presentations | Blue-first |
| `elegant-emerald` | #059669 | Nature-inspired elegance | Green-first |
| `vibrant-orange` | #ea580c | Energetic, creative presentations | Orange-first |
| `dark-mode` | #60a5fa | Modern dark theme | Brighter variants |

### Theme-Specific Chart Colors

| Theme | chart_1 | chart_2 | chart_3 | chart_4 | chart_5 | chart_6 |
|-------|---------|---------|---------|---------|---------|---------|
| corporate-blue | #3b82f6 | #10b981 | #f59e0b | #ef4444 | #8b5cf6 | #ec4899 |
| elegant-emerald | #10b981 | #3b82f6 | #f59e0b | #ef4444 | #8b5cf6 | #ec4899 |
| vibrant-orange | #f97316 | #3b82f6 | #10b981 | #ef4444 | #8b5cf6 | #ec4899 |
| dark-mode | #60a5fa | #34d399 | #fbbf24 | #f87171 | #a78bfa | #f472b6 |

---

## Frontend CSS Capabilities

### Deckster Typography Classes

Generated per theme for Text Service `styling_mode: "css_classes"`:

```css
.theme-{themeId} .deckster-t1        /* H1 style - largest heading */
.theme-{themeId} .deckster-t2        /* H2 style */
.theme-{themeId} .deckster-t3        /* H3 style */
.theme-{themeId} .deckster-t4        /* Body/paragraph style */
.theme-{themeId} .deckster-emphasis  /* Accent color emphasis */
.theme-{themeId} .deckster-bullets   /* Styled bullet list container */
.theme-{themeId} .deckster-bullet-item  /* Individual bullet item */
```

### ThemeManager JavaScript API

```javascript
// Generate CSS for a single theme
ThemeManager.generateDecksterClasses(themeId, theme)

// Generate CSS for all registered themes
ThemeManager.generateAllDecksterClasses()

// Inject deckster classes into document <head>
ThemeManager.injectDecksterClasses()
```

---

## Integration Examples

### Text Service Startup

```python
import requests

# Fetch all themes on startup
response = requests.get("http://layout-service/api/themes/sync")
data = response.json()

THEME_CACHE = data["themes"]
THEME_VERSION = data["version"]

# Access theme colors
corporate = THEME_CACHE["corporate-blue"]
primary_color = corporate["colors"]["primary"]  # "#1e40af"
chart_colors = [corporate["colors"][f"chart_{i}"] for i in range(1, 7)]
```

### Director Theme Lookup

```python
# Get theme for slide generation
theme = THEME_CACHE.get(theme_id, THEME_CACHE["corporate-blue"])
colors = theme["colors"]

# Use in slide generation instructions
generation_context = {
    "primary_color": colors["primary"],
    "accent_color": colors["accent"],
    "chart_palette": [colors[f"chart_{i}"] for i in range(1, 7)]
}
```

### Fallback Strategy

```python
# If Layout Service unreachable, use embedded presets
try:
    response = requests.get("http://layout-service/api/themes/sync", timeout=5)
    THEME_CACHE = response.json()["themes"]
    logger.info("Theme sync successful", source="layout_service")
except Exception as e:
    THEME_CACHE = EMBEDDED_THEME_PRESETS
    logger.warning("Using fallback themes", error=str(e))
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Dec 2024 | Initial release with 4 themes, 23 color keys, sync endpoint |
