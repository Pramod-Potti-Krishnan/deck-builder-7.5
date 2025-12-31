# Frontend Template Update Guide

## Overview

This document describes the template reorganization changes that require frontend updates.

**Date:** December 2024
**Version:** 7.5.1

---

## Summary of Changes

### Removed Templates (4)
| Template ID | Replacement |
|-------------|-------------|
| `C2-table` | Merged into `C1-text` (tables are hypertext) |
| `C6-image` | Use `I1-image-left` or `I2-image-right` |
| `S1-visual-text` | Use `V1-V4` series (specific visual types) |
| `S2-image-content` | Use `I1-I4` series (image split layouts) |

### New Templates (8)

#### V Series - Visual + Text (4 templates)
Visual element on LEFT (cols 2-20), text insights on RIGHT (cols 20-32)

| Template ID | Visual Type | Description |
|-------------|-------------|-------------|
| `V1-image-text` | Image | Image with text insights |
| `V2-chart-text` | Chart | Chart with text insights |
| `V3-diagram-text` | Diagram | Diagram with text insights |
| `V4-infographic-text` | Infographic | Infographic with text insights |

#### I Series - Image Split (4 templates)
Full-height image with content area

| Template ID | Image Position | Image Width | Description |
|-------------|----------------|-------------|-------------|
| `I1-image-left` | LEFT | 12 cols (660px) | Wide image left |
| `I2-image-right` | RIGHT | 12 cols (660px) | Wide image right |
| `I3-image-left-narrow` | LEFT | 6 cols (330px) | Narrow image left |
| `I4-image-right-narrow` | RIGHT | 6 cols (330px) | Narrow image right |

---

## Final Template Catalog

### Categories

```javascript
TEMPLATE_CATEGORIES = {
  hero: ['H1-generated', 'H1-structured', 'H2-section', 'H3-closing'],
  content: ['C1-text', 'C3-chart', 'C4-infographic', 'C5-diagram'],
  visual: ['V1-image-text', 'V2-chart-text', 'V3-diagram-text', 'V4-infographic-text'],
  image: ['I1-image-left', 'I2-image-right', 'I3-image-left-narrow', 'I4-image-right-narrow'],
  split: ['S3-two-visuals', 'S4-comparison'],
  blank: ['B1-blank']
}
```

**Total: 19 templates**

---

## V Series Slot Definitions

All V series templates share the same layout structure:

### Grid Layout
```
┌─────────────────────────────────────────────────────────┐
│  Title (rows 1-3, cols 2-32)                            │
├─────────────────────────────────────────────────────────┤
│  Subtitle (rows 3-4, cols 2-32)                         │
├────────────────────────────┬────────────────────────────┤
│                            │                            │
│   Visual Content           │   Text Content             │
│   (rows 4-18, cols 2-20)   │   (rows 4-18, cols 20-32)  │
│                            │                            │
│   ~900x720px               │   ~600x720px               │
│                            │                            │
├────────────────────────────┴────────────────────────────┤
│  Footer (rows 18-19)                    Logo            │
└─────────────────────────────────────────────────────────┘
```

### Slot Specifications

| Slot | Grid Position | Accepts | Default Text |
|------|---------------|---------|--------------|
| `title` | rows 1-3, cols 2-32 | text | "Slide Title" |
| `subtitle` | rows 3-4, cols 2-32 | text | "Subtitle" |
| `content_left` | rows 4-18, cols 2-20 | *varies by template* | null |
| `content_right` | rows 4-18, cols 20-32 | body, table, html | "Key Insights" |
| `footer` | rows 18-19, cols 2-7 | text | "Footer" |
| `logo` | rows 17-19, cols 30-32 | image, emoji | null |

### Content Left Accepts (by template)

| Template | `content_left` Accepts | Tag |
|----------|------------------------|-----|
| V1-image-text | `['image']` | image |
| V2-chart-text | `['chart']` | chart |
| V3-diagram-text | `['diagram']` | diagram |
| V4-infographic-text | `['infographic']` | infographic |

---

## I Series Slot Definitions

### I1-image-left (Wide Image Left)

```
┌───────────────┬─────────────────────────────────────────┐
│               │  Title (rows 1-3, cols 12-32)           │
│               ├─────────────────────────────────────────┤
│    Image      │  Subtitle (rows 3-4, cols 12-32)        │
│    (full      ├─────────────────────────────────────────┤
│    height)    │                                         │
│               │  Content (rows 4-18, cols 12-32)        │
│  cols 1-12    │                                         │
│  660px wide   │                                         │
│               ├─────────────────────────────────────────┤
│               │  Footer                          Logo   │
└───────────────┴─────────────────────────────────────────┘
```

| Slot | Grid Position |
|------|---------------|
| `image` | rows 1-19, cols 1-12 |
| `title` | rows 1-3, cols 12-32 |
| `subtitle` | rows 3-4, cols 12-32 |
| `content` | rows 4-18, cols 12-32 |
| `footer` | rows 18-19, cols 12-17 |
| `logo` | rows 17-19, cols 30-32 |

### I2-image-right (Wide Image Right)

```
┌─────────────────────────────────────────┬───────────────┐
│  Title (rows 1-3, cols 1-21)            │               │
├─────────────────────────────────────────┤    Image      │
│  Subtitle (rows 3-4, cols 1-21)         │    (full      │
├─────────────────────────────────────────┤    height)    │
│                                         │               │
│  Content (rows 4-18, cols 1-21)         │  cols 21-33   │
│                                         │  660px wide   │
│                                         │               │
├─────────────────────────────────────────┤               │
│  Footer                          Logo   │               │
└─────────────────────────────────────────┴───────────────┘
```

| Slot | Grid Position |
|------|---------------|
| `image` | rows 1-19, cols 21-33 |
| `title` | rows 1-3, cols 1-21 |
| `subtitle` | rows 3-4, cols 1-21 |
| `content` | rows 4-18, cols 1-21 |
| `footer` | rows 18-19, cols 2-7 |
| `logo` | rows 17-19, cols 18-20 |

### I3-image-left-narrow (Narrow Image Left)

```
┌───────┬─────────────────────────────────────────────────┐
│       │  Title (rows 1-3, cols 7-32)                    │
│       ├─────────────────────────────────────────────────┤
│ Image │  Subtitle (rows 3-4, cols 7-32)                 │
│       ├─────────────────────────────────────────────────┤
│ cols  │                                                 │
│ 1-7   │  Content (rows 4-18, cols 7-32)                 │
│       │                                                 │
│ 330px │                                                 │
│       ├─────────────────────────────────────────────────┤
│       │  Footer                                  Logo   │
└───────┴─────────────────────────────────────────────────┘
```

| Slot | Grid Position |
|------|---------------|
| `image` | rows 1-19, cols 1-7 |
| `title` | rows 1-3, cols 7-32 |
| `subtitle` | rows 3-4, cols 7-32 |
| `content` | rows 4-18, cols 7-32 |
| `footer` | rows 18-19, cols 7-12 |
| `logo` | rows 17-19, cols 30-32 |

### I4-image-right-narrow (Narrow Image Right)

```
┌─────────────────────────────────────────────────┬───────┐
│  Title (rows 1-3, cols 1-26)                    │       │
├─────────────────────────────────────────────────┤ Image │
│  Subtitle (rows 3-4, cols 1-26)                 │       │
├─────────────────────────────────────────────────┤ cols  │
│                                                 │ 26-33 │
│  Content (rows 4-18, cols 1-26)                 │       │
│                                                 │ 330px │
│                                                 │       │
├─────────────────────────────────────────────────┤       │
│  Footer                          Logo           │       │
└─────────────────────────────────────────────────┴───────┘
```

| Slot | Grid Position |
|------|---------------|
| `image` | rows 1-19, cols 26-33 |
| `title` | rows 1-3, cols 1-26 |
| `subtitle` | rows 3-4, cols 1-26 |
| `content` | rows 4-18, cols 1-26 |
| `footer` | rows 18-19, cols 2-7 |
| `logo` | rows 17-19, cols 23-25 |

---

## Migration Guide

### 1. Update Template Picker UI

Remove from template picker:
- C2-table
- C6-image
- S1-visual-text
- S2-image-content

Add new categories and templates:

```javascript
// Add "Visual + Text" category
{
  name: 'Visual + Text',
  description: 'Visual element on left with text insights on right',
  templates: ['V1-image-text', 'V2-chart-text', 'V3-diagram-text', 'V4-infographic-text']
}

// Add "Image Split" category
{
  name: 'Image Split',
  description: 'Full-height image with content area',
  templates: ['I1-image-left', 'I2-image-right', 'I3-image-left-narrow', 'I4-image-right-narrow']
}
```

### 2. Update Renderers

Create new renderer functions (or use existing pattern):

```javascript
// V Series renderers
renderV1ImageText(slide, content)
renderV2ChartText(slide, content)
renderV3DiagramText(slide, content)
renderV4InfographicText(slide, content)

// I Series renderers
renderI1ImageLeft(slide, content)
renderI2ImageRight(slide, content)
renderI3ImageLeftNarrow(slide, content)
renderI4ImageRightNarrow(slide, content)
```

### 3. Update Thumbnail Images

Create thumbnail SVGs for the new templates:
- `visual-image-text.svg`
- `visual-chart-text.svg`
- `visual-diagram-text.svg`
- `visual-infographic-text.svg`
- `image-left-wide.svg`
- `image-right-wide.svg`
- `image-left-narrow.svg`
- `image-right-narrow.svg`

### 4. Handle Legacy Presentations

Existing presentations using removed templates should be handled:

```javascript
// Migration mapping
const TEMPLATE_MIGRATION = {
  'C2-table': 'C1-text',        // Tables work in C1-text
  'C6-image': 'I1-image-left',  // Single image -> I1
  'S1-visual-text': 'V1-image-text',  // Generic visual -> V1
  'S2-image-content': 'I1-image-left' // Image+content -> I1
};
```

---

## CSS Classes

New CSS classes for styling:

```css
/* V Series */
.template-v1-image-text { }
.template-v2-chart-text { }
.template-v3-diagram-text { }
.template-v4-infographic-text { }

/* I Series */
.template-i1-image-left { }
.template-i2-image-right { }
.template-i3-image-left-narrow { }
.template-i4-image-right-narrow { }

/* Category classes */
.category-visual { }
.category-image { }
```

---

## API Changes

### Valid Layout Values

The API now accepts these layouts:

```
Backend: L01, L02, L03, L25, L27, L29
Hero: H1-generated, H1-structured, H2-section, H3-closing
Content: C1-text, C3-chart, C4-infographic, C5-diagram
Visual: V1-image-text, V2-chart-text, V3-diagram-text, V4-infographic-text
Image: I1-image-left, I2-image-right, I3-image-left-narrow, I4-image-right-narrow
Split: S3-two-visuals, S4-comparison
Blank: B1-blank
```

### GET / Response

```json
{
  "layouts": {
    "frontend": {
      "hero": ["H1-generated", "H1-structured", "H2-section", "H3-closing"],
      "content": ["C1-text", "C3-chart", "C4-infographic", "C5-diagram"],
      "visual": ["V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text"],
      "image": ["I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow"],
      "split": ["S3-two-visuals", "S4-comparison"],
      "blank": ["B1-blank"]
    }
  }
}
```

---

## Checklist

- [ ] Remove C2-table, C6-image, S1-visual-text, S2-image-content from template picker
- [ ] Add V1-V4 templates to template picker
- [ ] Add I1-I4 templates to template picker
- [ ] Create thumbnail images for new templates
- [ ] Implement V series renderers
- [ ] Implement I series renderers
- [ ] Add category tabs for "Visual + Text" and "Image Split"
- [ ] Test all new templates render correctly
- [ ] Handle legacy presentation migration (optional)
- [ ] Update any hardcoded template references

---

## Questions?

Contact the backend team if you have questions about:
- Slot definitions or grid positions
- Content type handling
- API changes
