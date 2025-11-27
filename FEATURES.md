# Layout Builder v7.5-main: Complete Features Guide

**Version**: 7.5.0
**Last Updated**: 2025-01-24
**Port**: 8504

---

## Table of Contents

1. [Core Features](#core-features)
2. [Layout System](#layout-system)
3. [Content Editing](#content-editing)
4. [AI-Powered Features (NEW)](#ai-powered-features-new)
5. [Customization Features](#customization-features)
6. [Developer Features](#developer-features)
7. [Integration Features](#integration-features)
8. [Debugging Tools](#debugging-tools)

---

## Core Features

### 1. **6-Layout Production System**

Complete presentation system with 6 specialized layouts covering all presentation needs:

| Layout | Purpose | Content Area | Best For |
|--------|---------|--------------|----------|
| **L01** | Centered Chart | 1800×600px chart + text | Single data visualization with explanation |
| **L02** | Diagram + Text | 1260×720px diagram + text | Process flows, architecture diagrams |
| **L03** | Dual Charts | Two 840×540px charts | Side-by-side comparison |
| **L25** | Main Content | 1800×720px rich content | 80% of slides - text, lists, grids |
| **L27** | Image + Text | 720×1080px image + text | Product showcases, case studies |
| **L29** | Full-Bleed Hero | 1920×1080px full slide | Titles, sections, endings |

**Key Benefits**:
- ✅ Covers all presentation scenarios
- ✅ Consistent grid system (18 rows × 32 columns)
- ✅ Clear format ownership (no conflicts)
- ✅ Text Service has full creative control

**Documentation**: `docs/LAYOUT_SPECIFICATIONS.md`

---

### 2. **Chart & Visualization Support**

**Supported Libraries**:
- **ApexCharts** 3.45.0 - Business charts (bar, line, area, pie, donut)
- **Chart.js** 4.4.0 + Plugins - Advanced charts (scatter, bubble, treemap, matrix, sankey)

**Extended Chart Types** (Chart.js):
- 📊 Treemap charts (hierarchical data)
- 🔥 Matrix charts (heatmaps)
- 📦 Box & Violin plots (statistical distributions)
- 📈 Financial charts (candlestick, OHLC)
- 🌊 Sankey diagrams (flow visualization)

**Features**:
- ✅ Interactive charts with hover tooltips
- ✅ Responsive scaling to fit content areas
- ✅ Data labels plugin for annotations
- ✅ Chart rendering validation and error handling
- ✅ Support for both HTML canvas and SVG rendering

**Chart Compatibility**:
- L01: Single chart (1800×600px)
- L02: Diagram/chart on left (1260×720px)
- L03: Two charts side-by-side (840×540px each)
- L25: Charts within rich content area (flexible sizing)

**Documentation**:
- `docs/recent/CHART_RENDERING_FIX_COMPLETE.md`
- `docs/recent/APEXCHARTS_FIX_SUMMARY.md`

---

### 3. **Format Ownership Model**

**Clear separation of responsibilities**:

#### Layout Builder Owns:
- Slide titles and subtitles (formatted by layout)
- Grid positioning and structure
- Slide backgrounds (color/image)
- Footer metadata
- Navigation and controls

#### Text Service Owns:
- **L25**: `rich_content` field (HTML with full styling control)
- **L29**: `hero_content` field (complete slide HTML)
- **All Other Layouts**: Content fields specific to each layout
- HTML structure within content areas
- All inline styles and creative decisions

**Benefits**:
- ✅ No format conflicts
- ✅ Clear accountability
- ✅ Predictable rendering
- ✅ Easy troubleshooting

**Documentation**: `docs/ARCHITECTURE.md`

---

## Layout System

### Layout Specifications

#### **L01: Centered Chart with Text Below**

```json
{
  "layout": "L01",
  "content": {
    "slide_title": "Q4 Revenue Performance",
    "element_1": "Regional Breakdown",
    "element_4": "<canvas id='chart1'>...</canvas><script>...</script>",
    "element_3": "<p>Revenue increased 23% YoY...</p>"
  }
}
```

**Grid Structure**:
- Title: Row 2, Columns 2-31
- Subtitle: Row 3, Columns 2-31
- Chart: Rows 5-14, Columns 7-26 (1800×600px)
- Body: Rows 15-17, Columns 7-26

**Use Cases**:
- Single metric visualization
- Key performance indicator with explanation
- Focused data story

---

#### **L02: Left Diagram with Right Text**

```json
{
  "layout": "L02",
  "content": {
    "slide_title": "System Architecture",
    "element_1": "Overview",
    "element_2": "<div>Architecture diagram HTML...</div>",
    "element_3": "<ul><li>Component 1</li><li>Component 2</li></ul>"
  }
}
```

**Grid Structure**:
- Title: Row 2, Columns 2-31
- Subtitle: Row 3, Columns 2-31
- Diagram (Left): Rows 5-17, Columns 2-22 (1260×720px)
- Text (Right): Rows 5-17, Columns 23-31

**Use Cases**:
- Architecture diagrams with explanations
- Process flows with step descriptions
- Technical diagrams with annotations

**Important**: See `docs/L02_DIRECTOR_INTEGRATION_GUIDE.md` for integration details

---

#### **L03: Two Charts in Columns**

```json
{
  "layout": "L03",
  "content": {
    "slide_title": "Regional Comparison",
    "element_1": "Q4 vs Q3",
    "element_2": "<canvas id='chart1'>...</canvas>",
    "element_3": "<canvas id='chart2'>...</canvas>",
    "element_4": "<p>North America performance...</p>",
    "element_5": "<p>EMEA performance...</p>"
  }
}
```

**Grid Structure**:
- Title: Row 2
- Subtitle: Row 3
- Chart 1 (Left): Rows 5-13, Columns 2-16 (840×540px)
- Chart 2 (Right): Rows 5-13, Columns 17-31 (840×540px)
- Body Left: Rows 14-17, Columns 2-16
- Body Right: Rows 14-17, Columns 17-31

**Use Cases**:
- Before/after comparisons
- Regional performance comparisons
- Metric correlations
- Trend analysis

---

#### **L25: Main Content Shell** ⭐ Most Used

```json
{
  "layout": "L25",
  "content": {
    "slide_title": "Key Takeaways",
    "subtitle": "Summary of Findings",
    "rich_content": "<div style='...'>Full HTML content</div>",
    "presentation_name": "Q4 Business Review",
    "company_logo": "<img src='logo.png'>"
  }
}
```

**Grid Structure**:
- Title: Row 2, Columns 2-31
- Subtitle: Row 3, Columns 2-31
- **Rich Content**: Rows 5-16, Columns 2-31 (1800×720px)
- Footer: Row 18 (optional)

**Content Area Dimensions**: 1800px × 720px (massive creative freedom)

**Use Cases** (80% of slides):
- Bullet point lists
- Multi-column layouts
- Card grids
- Tables and data
- Mixed content (text + images + charts)

---

#### **L27: Image Left with Content Right**

```json
{
  "layout": "L27",
  "content": {
    "slide_title": "Product Launch",
    "element_1": "New Features",
    "element_2": "<img src='product.jpg' style='width: 100%; height: 100%; object-fit: cover;'>",
    "element_3": "<ul><li>Feature 1</li><li>Feature 2</li></ul>"
  }
}
```

**Grid Structure**:
- Title: Row 2
- Subtitle: Row 3
- Image (Left): Rows 5-17, Columns 2-13 (720×1080px - full height)
- Text (Right): Rows 5-17, Columns 14-31

**Use Cases**:
- Product showcases
- Case studies
- Photo-driven stories
- Portfolio presentations

---

#### **L29: Full-Bleed Hero Slides**

```json
{
  "layout": "L29",
  "content": {
    "hero_content": "<div style='...'>Complete slide HTML</div>"
  }
}
```

**Grid Structure**: Full slide (1920×1080px - no restrictions)

**Use Cases**:
- 🎬 Opening title slides
- 📍 Section dividers
- 🎯 Call-to-action slides
- 👋 Thank you / ending slides
- 🚀 Hero moments

**Creative Freedom**: Complete control over entire slide

---

## Content Editing

### Version History & Restore

**Track every change** to presentations with automatic versioning:

#### Features:
- ✅ **Automatic Versioning**: Every edit creates a version snapshot
- ✅ **Version History**: View all past versions with timestamps
- ✅ **Restore Capability**: Roll back to any previous version
- ✅ **Change Tracking**: See who made changes and when
- ✅ **Backup on Restore**: Automatically backs up current state before restoring

#### API Endpoints:

**Get Version History**:
```bash
GET /api/presentations/{id}/versions
```

**Response**:
```json
{
  "presentation_id": "abc123",
  "current_version_id": "v5",
  "versions": [
    {
      "version_id": "v1",
      "created_at": "2025-01-24T10:00:00Z",
      "created_by": "user",
      "change_summary": "Initial creation"
    },
    {
      "version_id": "v2",
      "created_at": "2025-01-24T11:30:00Z",
      "created_by": "director_agent",
      "change_summary": "Updated slide 3 content"
    }
  ]
}
```

**Restore Version**:
```bash
POST /api/presentations/{id}/restore/{version_id}
```

**Slide-Level Editing**:
```bash
PUT /api/presentations/{id}/slides/{slide_index}
```

```json
{
  "slide_title": "Updated Title",
  "rich_content": "<div>New content</div>"
}
```

**Documentation**: `docs/CONTENT_EDITING_USER_GUIDE.md`

---

### Edit Mode UI ✨ NEW

**Sleek, modern editing interface** for content management:

#### Features:
- 🎨 **Icon-Based Controls**: Minimal, elegant circular buttons
- 💾 **Quick Save**: One-click save (Ctrl+S)
- ❌ **Cancel Edits**: Discard changes easily (ESC)
- 📋 **Version History**: Access past versions
- 🎯 **Visual Indicator**: Small badge shows edit mode is active

#### UI Elements:
- **Toggle Button**: ✏️ icon in top-right corner
- **Control Buttons**: Circular 44px buttons stacked vertically
  - 💾 Save
  - ❌ Cancel
  - 📋 History
- **Mode Badge**: Small circular indicator when editing

#### Keyboard Shortcuts:
- **E** - Toggle edit mode
- **Ctrl+S** - Save changes
- **ESC** - Cancel edits

**Implementation**: `src/styles/edit-mode.css`, `src/utils/edit-mode.js`

---

## AI-Powered Features (NEW)

### Section-Based AI Regeneration 🤖

**Phase 2: World-Class Editor** - Select and regenerate specific parts of slides with AI!

#### Overview:
Instead of regenerating entire slides, users can now:
1. Select specific sections (title, body, chart, etc.)
2. Enter natural language instructions
3. AI regenerates only those sections
4. Content updates with smooth animations

#### How It Works:

**1. Enter Review Mode**:
- Click "📋 Review Mode" button (top-left)
- Sections become selectable with visual highlighting

**2. Select Sections**:
- Click any section to select it (gets blue outline)
- **Ctrl/Cmd+Click** for multi-select
- Selection counter shows how many sections selected

**3. Enter AI Instructions**:
- Type instruction in floating panel: "Make this more engaging with examples"
- Click "Regenerate with AI"

**4. AI Updates Content**:
- Each section regenerates individually
- Smooth fade-in animation
- Green highlight shows what changed

#### Section Types:

| Layout | Selectable Sections |
|--------|-------------------|
| **L01** | title, subtitle, chart, body |
| **L02** | title, subtitle, diagram, text |
| **L03** | title, subtitle, chart1, chart2, body-left, body-right |
| **L25** | title, subtitle, content |
| **L27** | title, subtitle, image, text |
| **L29** | hero (entire slide) |

#### Visual Feedback:
- **Hover**: Dashed blue outline
- **Selected**: Solid blue outline + background tint
- **Updating**: Fade out → Update → Fade in
- **Changed**: Brief green highlight

#### API Endpoint:
```bash
POST /api/presentations/{id}/regenerate-section
```

**Request**:
```json
{
  "slide_index": 2,
  "section_id": "slide-2-section-body",
  "section_type": "body",
  "user_instruction": "Make this more engaging with specific examples",
  "current_content": "<p>Revenue increased.</p>",
  "layout": "L25"
}
```

**Response**:
```json
{
  "success": true,
  "updated_content": "<p>Revenue surged 23% YoY to $4.2M...</p>",
  "section_id": "slide-2-section-body",
  "message": "Section regenerated successfully"
}
```

#### Benefits:
- ✅ **Precision**: Update only what needs improvement
- ✅ **Efficiency**: Faster than full-slide regeneration
- ✅ **Cost**: Lower token usage
- ✅ **Iteration**: Refine specific elements
- ✅ **Speed**: Quick improvements without re-doing perfect content

**Documentation**:
- `PHASE2_PLAN.md` - Implementation plan
- `DIRECTOR_SECTION_REGENERATION_SPEC.md` - Director Service integration spec

**Implementation**:
- `src/utils/review-mode.js` - Selection logic
- `src/components/regeneration-panel.js` - API communication
- `src/styles/review-mode.css` - Visual styles
- `models.py` - Request/response models
- `server.py` - API endpoint

---

## Customization Features

### Slide Backgrounds

**Add visual appeal** with custom backgrounds on any layout:

#### Background Color:
```json
{
  "layout": "L25",
  "background_color": "#f0f9ff",
  "content": { ... }
}
```

Supports:
- ✅ Hex colors: `#FF5733`, `#1a1a2e`
- ✅ Named colors: `white`, `lightblue`
- ✅ RGB: `rgb(255, 87, 51)`

#### Background Image:
```json
{
  "layout": "L29",
  "background_image": "https://images.unsplash.com/photo-1557683316...",
  "background_color": "#1a1a2e",
  "content": { ... }
}
```

Supports:
- ✅ External URLs
- ✅ Data URIs (base64)
- ✅ Automatic `background-size: cover`
- ✅ Color fallback if image fails to load

#### Best Practices:
1. **Always provide fallback color** when using images
2. **Ensure text contrast** - light text on dark backgrounds
3. **Image size**: 1920×1080 or higher
4. **File size**: Keep under 1MB for performance
5. **Format**: JPG for photos, PNG for graphics

**Available on**: All 6 layouts (L01, L02, L03, L25, L27, L29)

---

## Developer Features

### PostMessage Bridge for Iframe Embedding

**Cross-origin communication** for iframe integration:

#### Capabilities:
- ✅ Navigate slides programmatically
- ✅ Toggle edit mode remotely
- ✅ Save/cancel edits from parent
- ✅ Toggle overview mode
- ✅ Toggle debug overlays
- ✅ Get current slide info

#### Security:
Validates origin before executing commands. Allowed origins:
- `localhost:*` (development)
- `127.0.0.1:*` (local)
- `*.up.railway.app` (Railway deployments)
- `*.vercel.app` (Vercel deployments)
- `*.netlify.app` (Netlify deployments)
- `deckster.xyz` (production)
- `www.deckster.xyz` (production)

#### Usage Example:

**Parent Window** (different origin):
```javascript
// Get iframe reference
const iframe = document.getElementById('presentation-iframe');

// Send command
iframe.contentWindow.postMessage({
  action: 'nextSlide'
}, 'http://localhost:8504');

// Listen for response
window.addEventListener('message', (event) => {
  if (event.origin === 'http://localhost:8504') {
    console.log('Response:', event.data);
  }
});
```

#### Available Commands:
- `nextSlide` - Go to next slide
- `prevSlide` - Go to previous slide
- `goToSlide` - Jump to specific slide index
- `getCurrentSlideInfo` - Get current slide metadata
- `toggleEditMode` - Enter/exit edit mode
- `saveAllChanges` - Save edits
- `cancelEdits` - Discard edits
- `showVersionHistory` - Show version history
- `toggleOverview` - Toggle overview mode
- `toggleGridOverlay` - Toggle grid debug overlay
- `toggleBorderHighlight` - Toggle border highlights

**Documentation**: `docs/FRONTEND_INTEGRATION_GUIDE.md`, `docs/FRONTEND_CORS_RESPONSE.md`

**Implementation**: `viewer/presentation-viewer.html` (lines 282-414)

---

### Section ID System

**Unique identifiers** for every editable section:

#### Format:
```
slide-{slideIndex}-section-{sectionType}
```

#### Examples:
- `slide-0-section-title` - Title on first slide
- `slide-2-section-body` - Body text on third slide
- `slide-5-section-chart1` - First chart on sixth slide

#### Data Attributes:
Every section element has:
```html
<div
  data-section-id="slide-2-section-body"
  data-section-type="body"
  data-slide-index="2"
>
  Content here...
</div>
```

#### Benefits:
- ✅ Enables section-based regeneration
- ✅ Precise DOM targeting
- ✅ Version control at section level
- ✅ Undo/redo for specific sections

**Implementation**: All 6 renderers (L01.js, L02.js, L03.js, L25.js, L27.js, L29.js)

---

## Integration Features

### Director Agent Integration

**Seamless integration** with Director Agent for content orchestration:

#### Workflow:
1. Director determines slide layout based on content purpose
2. Director calls Text Service with layout specifications
3. Text Service generates HTML content
4. Director transforms response to v7.5 format
5. Director POSTs to Layout Builder

#### Layout Selection Logic:
- **Title slides** → L29 (full-bleed hero)
- **Section breaks** → L29 (section divider)
- **Main content** → L25 (text-heavy)
- **Comparisons** → L03 (dual charts)
- **Diagrams** → L01 or L02 (depending on text amount)
- **Showcases** → L27 (image + text)
- **Endings** → L29 (thank you slide)

#### Field Specifications for Text Service:
```python
{
  "layout_id": "L25",
  "field_specifications": {
    "rich_content": {
      "format_owner": "text_service",
      "content_area": {
        "pixels": {"width": 1800, "height": 720}
      },
      "guidelines": "Full HTML with inline styles"
    }
  }
}
```

**Documentation**: `docs/L02_DIRECTOR_INTEGRATION_GUIDE.md`

---

### Text Service Integration

**Complete control** over content generation:

#### Content Generation Guidelines:
1. **Use inline styles only** (no CSS classes)
2. **Respect content area dimensions**
3. **Generate well-formed HTML**
4. **Include accessibility attributes**
5. **Use system fonts for performance**

#### Recommended Fonts:
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
```

#### Content Area Dimensions:

| Layout | Content Area | Pixels |
|--------|--------------|--------|
| L01 | Chart | 1800 × 600 |
| L02 | Diagram | 1260 × 720 |
| L03 | Each Chart | 840 × 540 |
| L25 | Rich Content | 1800 × 720 |
| L27 | Image | 720 × 1080 |
| L29 | Hero | 1920 × 1080 |

**Documentation**: `docs/CONTENT_GENERATION_GUIDE.md`

---

## Debugging Tools

### Grid Overlay

**Visual grid system** for debugging positioning:

- **Press 'G'**: Toggle 18×32 grid overlay
- Shows exact grid boundaries
- Helps verify content positioning
- Red grid lines on semi-transparent overlay

### Border Highlights

**Highlight all sections** with colored borders:

- **Press 'B'**: Toggle border highlights
- Different colors for different sections:
  - Title: Red
  - Subtitle: Blue
  - Content areas: Green
  - Charts: Purple
- 2px solid borders for visibility

### Content Area Debug

**Debug content areas** specifically:

- **Press 'C'**: Toggle content area debug mode
- Highlights all Text Service-owned areas
- Shows exact dimensions
- Verifies overflow issues

### Help Text

**Keyboard shortcuts** reminder:

- **Press '?'**: Show help text
- Displays for 3 seconds
- Lists all available shortcuts

### RevealJS Built-in Tools:

- **ESC**: Overview mode (see all slides)
- **S**: Speaker notes view
- **F**: Fullscreen mode
- **Arrow Keys**: Navigate slides

---

## API Reference

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/presentations` | POST | Create presentation |
| `/api/presentations` | GET | List all presentations |
| `/api/presentations/{id}` | GET | Get presentation data |
| `/api/presentations/{id}` | PUT | Update metadata |
| `/api/presentations/{id}` | DELETE | Delete presentation |
| `/p/{id}` | GET | View presentation (HTML) |
| `/docs` | GET | Interactive API docs |

### Edit Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/presentations/{id}/slides/{index}` | PUT | Update slide content |
| `/api/presentations/{id}/versions` | GET | Get version history |
| `/api/presentations/{id}/restore/{version_id}` | POST | Restore version |

### AI Endpoints (NEW)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/presentations/{id}/regenerate-section` | POST | Regenerate section with AI |

---

## Performance Characteristics

### Response Times:
- **Create Presentation**: < 100ms (typical)
- **Get Presentation**: < 50ms (typical)
- **Update Content**: < 150ms (with versioning)
- **Section Regeneration**: 1-4 seconds (depending on section type)

### Scalability:
- **Storage**: JSON files (simple, fast)
- **Concurrent Users**: Handles 100+ simultaneous viewers
- **Presentation Size**: Supports 100+ slides per presentation

### Browser Support:
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

---

## Technology Stack

### Backend:
- **FastAPI** 0.115.0 - High-performance API framework
- **Pydantic** 2.12.4 - Data validation
- **Python** 3.13+ - Runtime
- **Uvicorn** - ASGI server

### Frontend:
- **Reveal.js** 4.5.0 - Presentation framework
- **ApexCharts** 3.45.0 - Business charts
- **Chart.js** 4.4.0 - Advanced charts
- **Vanilla JavaScript** - No frameworks (fast, simple)

### Storage:
- **Filesystem** - JSON files
- **Version Control** - Automatic snapshots

---

## Feature Roadmap

### Phase 3 (Planned):
- ✅ **Director Service Integration** for real AI regeneration
- ✅ **Section History** - Track changes to individual sections
- ✅ **Undo/Redo** - Granular content reversal
- ✅ **Advanced Selection** - Keyboard shortcuts, select all
- ✅ **Collaboration** - Multi-user editing

### Phase 4 (Future):
- 🔮 **Real-time Collaboration** - Multiple users editing simultaneously
- 🔮 **Comments & Annotations** - Feedback on specific sections
- 🔮 **Export Options** - PDF, PowerPoint, Google Slides
- 🔮 **Template Library** - Pre-built slide templates
- 🔮 **Animation Controls** - Slide transitions and effects

---

## Getting Started

### Quick Start:
```bash
# Clone repository
git clone https://github.com/Pramod-Potti-Krishnan/deck-builder-7.5.git
cd deck-builder-7.5/agents/layout_builder_main/v7.5-main

# Install dependencies
pip install -r requirements.txt

# Start server
python server.py
```

### Access Points:
- **API Root**: http://localhost:8504
- **API Docs**: http://localhost:8504/docs
- **Create Presentation**: POST http://localhost:8504/api/presentations
- **View Presentation**: http://localhost:8504/p/{id}

---

## Documentation Index

### Essential Reading:
1. **README.md** - Quick start guide
2. **FEATURES.md** (this file) - Complete features reference
3. **docs/ARCHITECTURE.md** - System architecture
4. **docs/LAYOUT_SPECIFICATIONS.md** - Layout details
5. **docs/CONTENT_GENERATION_GUIDE.md** - Content creation guide

### Integration Guides:
- **docs/L02_DIRECTOR_INTEGRATION_GUIDE.md** - Director integration
- **docs/FRONTEND_INTEGRATION_GUIDE.md** - Frontend embedding
- **docs/CONTENT_EDITING_USER_GUIDE.md** - Editing features

### Phase 2 Documentation:
- **PHASE2_PLAN.md** - Section regeneration implementation plan
- **DIRECTOR_SECTION_REGENERATION_SPEC.md** - Director API specification

---

## Support & Contact

### Issues:
- GitHub Issues: https://github.com/Pramod-Potti-Krishnan/deck-builder-7.5/issues

### Documentation:
- Latest: `/docs` directory
- API Docs: http://localhost:8504/docs

---

**Ready to build world-class presentations with v7.5-main!** 🚀
