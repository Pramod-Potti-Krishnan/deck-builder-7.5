# Layout Builder v7.5-main - Layout Specifications

**Version**: v7.5-main
**Total Layouts**: 6 (L01, L02, L03, L25, L27, L29)
**Grid System**: 18 rows × 32 columns
**Resolution**: 1920px × 1080px (16:9 aspect ratio)
**Grid Cell Size**: ~60px × 60px

---

## Layout Categories

### Title Slides
- **L29**: Full-bleed hero slides for openings, closings, and section breaks

### Text Slides
- **L25**: Text-heavy content with rich HTML formatting area
- **L27**: Image-focused layout with full-height image and text content

### Analytic Slides
- **L01**: Centered chart or diagram with descriptive text
- **L02**: Diagram-left with explanatory text on right
- **L03**: Two charts side-by-side for comparison

### Diagram Slides
- **L01**: Supports diagrams (interchangeable with charts)
- **L02**: Supports diagrams (interchangeable with charts)
- **L25**: Supports diagram-based content in rich_content area

---

## Slide Background Support

**NEW FEATURE**: All layouts now support optional slide backgrounds.

### Background Color

- **Field**: `background_color` (optional)
- **Format**: Hex color code (e.g., `#FF5733`, `#1a1a1a`, `#f0f9ff`)
- **Applies to**: Entire slide area (full 1920×1080px)
- **Default**: White background if not specified

### Background Image

- **Field**: `background_image` (optional)
- **Format**: URL or data URI (base64)
  - HTTP/HTTPS URLs: `https://example.com/image.jpg`
  - Data URIs: `data:image/png;base64,iVBORw0KGgo...`
- **Rendering**:
  - `background-size: cover` (fills entire slide)
  - `background-position: center` (centered alignment)
  - `background-repeat: no-repeat` (no tiling)
- **Applies to**: Entire slide area (full 1920×1080px)

### Priority and Fallback Behavior

When both `background_color` and `background_image` are provided:
1. **Image displays first** (primary background)
2. **Color acts as fallback** (shown if image fails to load or has transparency)
3. If neither is provided, default white background is used

### Example Usage

```json
{
  "layout": "L25",
  "background_color": "#f0f9ff",
  "background_image": "https://example.com/background.jpg",
  "content": {
    "slide_title": "Presentation Title",
    "rich_content": "<div>Your content here</div>"
  }
}
```

### Supported Layouts

All 6 layouts support backgrounds:
- ✅ **L01** - Chart/Diagram with background
- ✅ **L02** - Two-column with background
- ✅ **L03** - Dual charts with background
- ✅ **L25** - Main content with background
- ✅ **L27** - Image + content with background
- ✅ **L29** - Full-bleed hero with background

### Best Practices

1. **Text Readability**: Ensure sufficient contrast between background and text
2. **Image Size**: Use images sized for 1920×1080 or larger for best quality
3. **File Size**: For data URIs, keep images under 1MB for optimal performance
4. **Fallback Color**: Always provide a fallback color when using images
5. **Content Visibility**: Test that all content elements are visible on the background

---

## L01: Centered Chart or Diagram

### Purpose
Large centered visual (chart OR diagram) with title, subtitle, and descriptive text below.

### Layout Structure
```
┌─────────────────────────────────────────────────────────┐
│ Row 2:  slide_title (centered)                          │
│ Row 3:  subtitle/element_1 (centered)                   │
│                                                          │
│ Rows 5-15:  element_4 (CHART or DIAGRAM)               │
│             30 grids wide × 10 grids tall               │
│             (1800px × 600px)                            │
│                                                          │
│ Rows 15-17: element_3 (body text)                      │
│             30 grids wide × 2 grids tall                │
│                                                          │
│ Row 18: footer (presentation_name)                      │
│         company_logo (rows 17-19, cols 30-32)           │
└─────────────────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type |
|---------|---------------|---------------|------------|------|
| Title | `slide_title` | Row 2, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Subtitle | `element_1` | Row 3, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Chart/Diagram | `element_4` | Rows 5-15, Cols 2-32 | 30 grids wide × 10 grids tall (1800×600px) | HTML/Chart/Diagram |
| Body Text | `element_3` | Rows 15-17, Cols 2-32 | 30 grids wide × 2 grids tall | Text |
| Footer Name | `presentation_name` | Row 18, Cols 2-7 | 6 grids wide × 1 grid tall | Text |
| Company Logo | `company_logo` | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | Image/Emoji |

### Content Fields
```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Chart Title",
    "element_1": "Subtitle or context",
    "element_4": "<div>Chart or Diagram HTML</div>",
    "element_3": "Descriptive text below the visual",
    "presentation_name": "Presentation Name",
    "company_logo": "🏢"
  }
}
```

### Use Cases
- Financial performance charts
- Process flow diagrams
- Data visualization with context
- Strategic framework diagrams
- **Charts and diagrams are mutually interchangeable**

---

## L02: Diagram Left with Text Right

### Purpose
Diagram or process flow on left (2/3 width) with detailed explanatory text on right (1/3 width).

**v7.5.1 Enhancement**: Full HTML support for both element_3 (diagram/chart) and element_2 (observations/explanation). Auto-detects content type and applies appropriate rendering.

### Layout Structure
```
┌────────────────────────────────────────────────────┐
│ Row 2:  slide_title (full width)                  │
│ Row 3:  element_1 (subtitle, full width)          │
│                                                    │
│         element_3              │  element_2        │
│         (DIAGRAM or CHART)     │  (observations)   │
│         21 grids wide          │  9 grids wide     │
│         × 12 grids tall        │  × 12 grids tall  │
│         (1260px × 720px)       │  (540px × 720px)  │
│                                                    │
│ Row 18: footer                                     │
└────────────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type |
|---------|---------------|---------------|------------|------|
| Title | `slide_title` | Row 2, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Subtitle | `element_1` | Row 3, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Diagram/Chart | `element_3` | Rows 5-17, Cols 2-23 | 21 grids wide × 12 grids tall (1260×720px) | **HTML/Text** |
| Observations/Explanation | `element_2` | Rows 5-17, Cols 23-32 | 9 grids wide × 12 grids tall (540×720px) | **HTML/Text** |
| Footer Name | `presentation_name` | Row 18, Cols 2-7 | 6 grids wide × 1 grid tall | Text |
| Company Logo | `company_logo` | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | Image/Emoji |

### Content Fields

**Option 1: Plain Text** (backward compatible)
```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Process Overview",
    "element_1": "Workflow explanation",
    "element_3": "<div>Diagram or Chart HTML</div>",
    "element_2": "Detailed explanation text for the diagram or chart",
    "presentation_name": "Presentation Name",
    "company_logo": "🏢"
  }
}
```

**Option 2: HTML Content** (recommended for Analytics/rich formatting)
```json
{
  "layout": "L02",
  "content": {
    "slide_title": "Quarterly Revenue Growth",
    "element_1": "FY 2024 Performance",
    "element_3": "<div class='chart-container' style='width: 1260px; height: 720px;'><canvas id='chart'></canvas><script>/* Chart.js code */</script></div>",
    "element_2": "<div style='padding: 32px; background: #f8f9fa; border-radius: 8px;'><h3 style='font-size: 20px; margin-bottom: 16px; color: #1f2937;'>Key Insights</h3><p style='font-size: 16px; line-height: 1.6; color: #374151;'>The line chart illustrates quarterly revenue growth...</p></div>",
    "presentation_name": "Analytics Demo",
    "company_logo": "🏢"
  }
}
```

**Important Notes**:
- **HTML Auto-Detection**: Renderer automatically detects HTML (checks for `<` character)
- **Plain Text Styling**: If plain text is provided, Layout Builder applies default typography
- **HTML Rendering**: If HTML is provided, it renders as-is without additional styling wrapper
- **Dimensions**: Analytics Service should use 1260×720px for element_3, 540×720px for element_2
- **Overflow**: element_3 uses `overflow: hidden`, element_2 uses `overflow: auto` for scrolling

### Use Cases
- Architecture diagrams with explanation
- System flow diagrams with details
- Process flows with step descriptions
- Technical diagrams requiring detailed text
- **Analytics charts with observations** (new in v7.5.1)
- Data visualizations with key insights
- **Charts and diagrams are mutually interchangeable**

---

## L03: Two Charts Side-by-Side

### Purpose
Side-by-side chart comparison layout. **Charts only - not for diagrams.**

### Layout Structure
```
┌──────────────────────────────────────────────────┐
│ Row 2:  slide_title (centered)                   │
│ Row 3:  element_1 (subtitle, centered)           │
│                                                  │
│  element_4          │         element_2          │
│  (Chart 1)          │         (Chart 2)          │
│  14 grids wide      │         14 grids wide      │
│  × 9 grids tall     │         × 9 grids tall     │
│  (840×540px)        │         (840×540px)        │
│                                                  │
│  element_3          │         element_5          │
│  (description)      │         (description)      │
│                                                  │
│ Row 18: footer                                   │
└──────────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type |
|---------|---------------|---------------|------------|------|
| Title | `slide_title` | Row 2, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Subtitle | `element_1` | Row 3, Cols 2-32 | 30 grids wide × 1 grid tall | Text |
| Left Chart | `element_4` | Rows 5-14, Cols 2-16 | 14 grids wide × 9 grids tall (840×540px) | HTML/Chart |
| Right Chart | `element_2` | Rows 5-14, Cols 17-31 | 14 grids wide × 9 grids tall (840×540px) | HTML/Chart |
| Left Description | `element_3` | Rows 14-17, Cols 2-16 | 14 grids wide × 3 grids tall | Text |
| Right Description | `element_5` | Rows 14-17, Cols 17-31 | 14 grids wide × 3 grids tall | Text |
| Footer Name | `presentation_name` | Row 18, Cols 2-7 | 6 grids wide × 1 grid tall | Text |
| Company Logo | `company_logo` | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | Image/Emoji |

### Content Fields
```json
{
  "layout": "L03",
  "content": {
    "slide_title": "Quarterly Comparison",
    "element_1": "Q1 vs Q2 Performance",
    "element_4": "<div>Chart 1 HTML</div>",
    "element_2": "<div>Chart 2 HTML</div>",
    "element_3": "Description for Chart 1",
    "element_5": "Description for Chart 2",
    "presentation_name": "Presentation Name",
    "company_logo": "🏢"
  }
}
```

### Use Cases
- Before/after comparisons
- Quarterly performance comparison
- Regional data comparison
- A/B testing results
- **Charts only - NOT for diagrams**

---

## L25: Text-Heavy Content Slide

### Purpose
Rich HTML content area for detailed text, lists, sections, or diagram-based content.

### Layout Structure
```
┌─────────────────────────────────────────────────┐
│ Row 2:  slide_title (42px, bold)                │
│ Row 3:  subtitle (24px, optional)               │
│                                                 │
│ Rows 5-17: rich_content                        │
│            30 grids wide × 12 grids tall        │
│            (1800px × 720px)                     │
│            Full creative control by text_service│
│                                                 │
│ Row 18: footer                                  │
└─────────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type | Owner |
|---------|---------------|---------------|------------|------|-------|
| Title | `slide_title` | Row 2, Cols 2-32 | 30 grids wide × 1 grid tall | Text | layout_builder |
| Subtitle | `subtitle` | Row 3, Cols 2-32 | 30 grids wide × 1 grid tall | Text | layout_builder |
| Rich Content | `rich_content` | Rows 5-17, Cols 2-32 | 30 grids wide × 12 grids tall (1800×720px) | HTML | text_service |
| Footer Name | `presentation_name` | Row 18, Cols 2-7 | 6 grids wide × 1 grid tall | Text | layout_builder |
| Company Logo | `company_logo` | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | Image/Emoji | layout_builder |

### Content Fields
```json
{
  "layout": "L25",
  "content": {
    "slide_title": "Detailed Analysis",
    "subtitle": "Key findings and recommendations",
    "rich_content": "<h3>Section 1</h3><ul><li>Point 1</li><li>Point 2</li></ul><h3>Section 2</h3><p>Detailed paragraph text...</p>",
    "presentation_name": "Presentation Name",
    "company_logo": "🏢"
  }
}
```

### Format Ownership
- **slide_title, subtitle**: Layout Builder (plain text → formatted HTML)
- **rich_content**: Text Service (receives HTML, renders as-is with full creative control)

### Use Cases
- Executive summaries with multiple sections
- Detailed methodology explanations
- Multi-paragraph analysis
- Bullet point lists with context
- **Can be used for text OR diagram-based slides**
- Rich HTML content including embedded diagrams

---

## L27: Image Left with Text Right

### Purpose
Full-height image on left with text content on right. **Text-based slides** with supporting imagery.

### Layout Structure
```
┌──────────────────────────────────────────────┐
│  image_url    │  Row 2: slide_title          │
│  (full height)│  Row 3: element_1 (subtitle) │
│  12 grids wide│                              │
│  × 18 grids   │  Rows 5-17: main_content     │
│  tall         │  (20 grids wide              │
│  (720×1080px) │   × 12 grids tall)           │
│               │                              │
│               │  Row 18: footer              │
└──────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type |
|---------|---------------|---------------|------------|------|
| Image | `image_url` | Rows 1-19, Cols 1-12 | 12 grids wide × 18 grids tall (720×1080px - full height) | Image/HTML |
| Title | `slide_title` | Row 2, Cols 13-32 | 20 grids wide × 1 grid tall | Text |
| Subtitle | `element_1` | Row 3, Cols 13-32 | 20 grids wide × 1 grid tall | Text |
| Main Content | `main_content` | Rows 5-17, Cols 13-32 | 20 grids wide × 12 grids tall | Text/HTML |
| Footer Name | `presentation_name` | Row 18, Cols 13-26 | 14 grids wide × 1 grid tall | Text |
| Company Logo | `company_logo` | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | Image/Emoji |

### Content Fields
```json
{
  "layout": "L27",
  "content": {
    "slide_title": "Product Overview",
    "element_1": "Revolutionary design meets functionality",
    "image_url": "<div>Image HTML or URL</div>",
    "main_content": "Detailed product description and features...",
    "presentation_name": "Presentation Name",
    "company_logo": "🏢"
  }
}
```

### Use Cases
- Product showcases with imagery
- Team member profiles with photos
- Case studies with supporting images
- Portfolio presentations
- **Text-based slides** with full-height imagery support

---

## L29: Hero Slide

### Purpose
Full-bleed hero slides for maximum impact. **Title slides** for openings, section breaks, and endings.

### Layout Structure
```
┌─────────────────────────────────────────────────┐
│                                                 │
│         hero_content (full slide)               │
│         32 grids wide × 18 grids tall           │
│         (1920px × 1080px - entire slide)        │
│                                                 │
│         Centered content, large typography      │
│                                                 │
│         Optional: presentation_name (bottom)    │
└─────────────────────────────────────────────────┘
```

### Element Specifications

| Element | Content Field | Grid Position | Dimensions | Type | Owner |
|---------|---------------|---------------|------------|------|-------|
| Hero Content | `hero_content` | Rows 1-18, Cols 1-32 | 32 grids wide × 18 grids tall (1920×1080px - full slide) | HTML | text_service |
| Presentation Name | `presentation_name` | Row 18, Cols 2-7 (optional) | 6 grids wide × 1 grid tall | Text | layout_builder |

### Content Fields
```json
{
  "layout": "L29",
  "content": {
    "hero_content": "<div style='height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;'><h1 style='font-size: 72px;'>Opening Title</h1><p style='font-size: 32px; margin-top: 24px;'>Subtitle or tagline</p></div>",
    "presentation_name": "Presentation Name"
  }
}
```

### Format Ownership
- **hero_content**: Text Service (full creative control, receives HTML)
- **presentation_name**: Layout Builder (optional footer)

### Use Cases
- Opening title slides
- Section break slides
- Closing/thank you slides
- Impact statement slides
- **Title slides** with maximum visual impact

---

## Chart/Diagram Interchangeability Rules

### Mutually Interchangeable (Charts ↔ Diagrams)
- **L01**: Charts and diagrams are **fully interchangeable**
- **L02**: Charts and diagrams are **fully interchangeable**

### Charts Only (No Diagrams)
- **L03**: **Charts only** - NOT suitable for diagrams due to side-by-side comparison focus

### Flexible Content
- **L25**: Can be used for **text OR diagram-based slides** via rich_content HTML area
- **L27**: **Text-based slides** with imagery (not for diagrams)
- **L29**: **Title slides** (not for charts or diagrams)

---

## Footer Specifications

All layouts except L29 include standard footer components:

### Footer Elements

| Component | Grid Position | Dimensions | Content Field |
|-----------|---------------|------------|---------------|
| Presentation Name | Row 18, Cols 2-7 | 6 grids wide × 1 grid tall | `presentation_name` |
| Company Logo | Rows 17-19, Cols 30-32 | 2 grids wide × 2 grids tall | `company_logo` |

### Footer Styling
- Presentation name: 18px font, left-aligned
- Company logo: Centered in 2×2 grid, max 50% of container size
- **No default borders** - borders only show when 'B' key pressed (yellow dotted outline)

---

## Typography Standards

### Title Elements (Layout Builder Formatted)
- **slide_title**: 32-42px, bold, #1f2937
- **subtitle**: 20-24px, regular, #6b7280
- **section_title**: 40px, bold, centered

### Body Text (Layout Builder Formatted)
- **body_text**: 18px, #1a1a1a, line-height 1.5
- **bullet_points**: 18px, line-height 1.6
- **main_content**: 18px, line-height 1.5

### Rich Content (Text Service Controlled)
- **rich_content** (L25): Full HTML control by text_service
- **hero_content** (L29): Full HTML control by text_service

---

## Grid System Reference

### Overall Grid
- **Total Rows**: 18
- **Total Columns**: 32
- **Cell Size**: ~60px × 60px
- **Total Resolution**: 1920px × 1080px (16:9)

### Common Grid Positions
- **Full width content**: Cols 2-32 (30 grids = 1800px)
- **Half width left**: Cols 2-16 (14 grids = 840px)
- **Half width right**: Cols 17-31 (14 grids = 840px)
- **2/3 width left**: Cols 2-23 (21 grids = 1260px)
- **1/3 width right**: Cols 24-32 (8 grids = 480px)

### Reserved Rows
- **Row 1**: Empty (margin)
- **Row 2**: slide_title
- **Row 3**: subtitle/element_1
- **Rows 4**: Empty (spacing)
- **Rows 5-17**: Main content area
- **Row 18**: Footer
- **Row 19**: Extended elements (logo)

---

## Layout Selection Guide

### When to Use Each Layout

| Layout | Best For | Key Feature | Content Type |
|--------|----------|-------------|--------------|
| **L01** | Single large visual with context | Centered chart/diagram | Analytic/Diagram |
| **L02** | Complex diagram with explanation | Left visual, right text | Analytic/Diagram |
| **L03** | Comparing two charts | Side-by-side charts | Analytic (charts only) |
| **L25** | Detailed written content or diagrams | Rich HTML area | Text/Diagram |
| **L27** | Image-focused storytelling | Full-height image | Text with imagery |
| **L29** | Maximum impact titles | Full-bleed hero | Title |

### Content Type Categories

**Title Slides**: L29
**Text Slides**: L25, L27
**Analytic Slides**: L01, L02, L03
**Diagram Slides**: L01, L02, L25

---

## Border Toggle Feature

Press **'B'** key to show colored dotted borders around all elements (debug mode):

| Element Type | Border Color | Purpose |
|--------------|--------------|---------|
| Slide title & subtitle | Light purple (#a78bfa) | Identify title elements |
| Text content | Light gray (#9ca3af) | Identify text areas |
| Charts | Blue (#3b82f6) | Identify chart containers |
| Diagrams | Purple (#8b5cf6) | Identify diagram containers |
| Images | Red (#ef4444) | Identify image containers |
| Rich content (L25) | Green (#10b981) | Identify HTML content area |
| Hero content (L29) | Orange (#f97316) | Identify hero area |
| Footer elements | Yellow (#fbbf24) | Identify footer components |

**Important**: Borders use `outline` (not `border`) to prevent content shifting - purely visual debug feature.

---

## Additional Features

### Keyboard Shortcuts
- **'G'**: Toggle grid overlay (18×32 grid)
- **'B'**: Toggle border highlighting (debug mode)
- **'H'**: Toggle help text
- **Arrow keys**: Navigate between slides

### Development Notes
- All layouts use 18×32 grid system
- Grid cells are approximately 60px × 60px
- Layouts are responsive and scale to viewport
- Format ownership clearly defined (layout_builder vs text_service)
- No content shifting when borders toggle

---

**Document Version**: v7.5-main
**Last Updated**: January 2025
**Total Supported Layouts**: 6 (L01, L02, L03, L25, L27, L29)
