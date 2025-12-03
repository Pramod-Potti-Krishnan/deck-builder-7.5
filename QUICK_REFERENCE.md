# Layout Builder v7.5-main: Quick Reference Guide

**Last Updated**: November 19, 2025  
**Version**: 7.5.0

---

## Quick Navigation

| Section | Purpose |
|---------|---------|
| [Project Overview](#project-overview) | High-level summary |
| [Core Files](#core-files) | Essential files and their purpose |
| [API Quick Start](#api-quick-start) | Common API operations |
| [Configuration](#configuration) | Environment setup |
| [Layouts at a Glance](#layouts-at-a-glance) | All 6 layout specifications |
| [Key Concepts](#key-concepts) | Important architectural patterns |
| [Common Tasks](#common-tasks) | How to do things |
| [Troubleshooting](#troubleshooting) | Common issues and fixes |

---

## Project Overview

**What is v7.5-main?**
A simplified presentation layout service that bridges Director Agent, Text Service, and presentation viewers.

**Key Statistics**:
- 6 layouts (L01-L03, L25, L27, L29)
- 32×18 CSS Grid system
- FastAPI backend (port 8504)
- Reveal.js viewer
- Supabase + filesystem storage
- ~1,500 lines of code total

**Philosophy**: Clear format ownership boundaries prevent conflicts between services.

---

## Core Files

### Backend (Python)

| File | Size | Purpose |
|------|------|---------|
| `server.py` | 472 lines | FastAPI REST API, 11 endpoints |
| `models.py` | 234 lines | Pydantic data models, 10 classes |
| `config.py` | 253 lines | Environment configuration management |
| `storage.py` | 350+ lines | Filesystem storage implementation |
| `storage_supabase.py` | 350+ lines | Supabase backend with cache |
| `logger.py` | 150+ lines | JSON structured logging |

### Frontend (JavaScript/CSS)

| File | Purpose |
|------|---------|
| `src/renderers/L*.js` | 6 layout renderers (L01-L29) |
| `src/styles/core/grid-system.css` | 32×18 grid + debug tools |
| `src/utils/format_ownership.js` | Format owner detection |
| `viewer/presentation-viewer.html` | Main viewer template |

### Configuration

| File | Purpose |
|------|---------|
| `.env.example` | Environment variable template |
| `Procfile` | Railway deployment config |
| `requirements.txt` | Python dependencies (7 packages) |

---

## API Quick Start

### Create a Presentation

```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Presentation",
    "slides": [
      {
        "layout": "L29",
        "content": {
          "hero_content": "<div>Title Slide</div>"
        }
      },
      {
        "layout": "L25",
        "content": {
          "slide_title": "Content Slide",
          "rich_content": "<p>Content here</p>"
        }
      }
    ]
  }'
```

### View Presentation

```bash
# After creation, visit in browser:
http://localhost:8504/p/{presentation_id}
```

### Update Slide Content

```bash
curl -X PUT http://localhost:8504/api/presentations/{id}/slides/0 \
  -H "Content-Type: application/json" \
  -d '{"rich_content": "<p>Updated</p>"}'
```

### Get Version History

```bash
curl http://localhost:8504/api/presentations/{id}/versions
```

### Restore Previous Version

```bash
curl -X POST http://localhost:8504/api/presentations/{id}/restore/{version_id} \
  -H "Content-Type: application/json" \
  -d '{"create_backup": true}'
```

### List All Presentations

```bash
curl http://localhost:8504/api/presentations
```

### Delete Presentation

```bash
curl -X DELETE http://localhost:8504/api/presentations/{id}
```

---

## Configuration

### Environment Variables

**Minimal Setup** (filesystem storage):
```env
PORT=8504
ALLOWED_ORIGINS=*
```

**Production Setup** (Supabase):
```env
PORT=8504
ALLOWED_ORIGINS=https://deckster.xyz
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-secret-key
SUPABASE_BUCKET=ls-presentation-data
ENABLE_SUPABASE=true
ENABLE_LOCAL_CACHE=true
CACHE_TTL_SECONDS=3600
```

### Setup Steps

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your settings

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run server:
```bash
python server.py
```

5. View API docs:
```
http://localhost:8504/docs
```

---

## Layouts at a Glance

### L01: Centered Chart/Diagram
```
┌─────────────────────────────┐
│ Title                        │
│ Subtitle                     │
│                              │
│  [1800×600px Chart/Diagram]  │
│                              │
│ Description text             │
│ Presentation Name  Logo      │
└─────────────────────────────┘
```

**Content Fields**:
- `slide_title`: Plain text
- `element_1`: Subtitle
- `element_4`: Chart/diagram HTML
- `element_3`: Description
- `presentation_name`, `company_logo`: Footer

### L02: Diagram Left, Text Right
```
┌──────────────┬─────────────┐
│              │ Title       │
│  Diagram     │ Text        │
│              │ Content     │
│  1260×720px  │             │
│              │ Footer      │
└──────────────┴─────────────┘
```

**Content Fields**:
- `slide_title`: Title
- `element_2`: Left diagram
- `element_3`: Right text content
- Footer optional

### L03: Two Charts Side-by-Side
```
┌──────────────┬──────────────┐
│ Title        │              │
│ Subtitle     │              │
│              │              │
│  Chart 1     │   Chart 2    │
│  840×540     │  840×540     │
│              │              │
│ Footer       │              │
└──────────────┴──────────────┘
```

**Content Fields**:
- `slide_title`: Title
- `element_1`: Subtitle
- `element_2`: Left chart
- `element_4`: Right chart

### L25: Main Content Shell
```
┌─────────────────────────────┐
│ Title (layout_builder)       │
│ Subtitle (layout_builder)    │
│                              │
│  [1800×720px Content Area]   │
│  (text_service owns this)    │
│                              │
│ Presentation Name   Logo     │
└─────────────────────────────┘
```

**Content Fields**:
- `slide_title`: Plain text (required)
- `subtitle`: Plain text (optional)
- `rich_content`: HTML (required, text_service)
- `presentation_name`: Footer left
- `company_logo`: Footer right

### L27: Image Left, Content Right
```
┌──────────────┬─────────────┐
│              │ Title       │
│   Image      │ Content     │
│  720×1080px  │ Area        │
│              │             │
│              │ Logo        │
└──────────────┴─────────────┘
```

**Content Fields**:
- `slide_title`: Title
- `element_1`: Left image
- `element_2`: Right content
- Footer optional

### L29: Hero Full-Bleed
```
┌─────────────────────────────┐
│                             │
│  [1920×1080px Full Slide]   │
│   (text_service owns this)  │
│                             │
└─────────────────────────────┘
```

**Content Fields**:
- `hero_content`: HTML (required, text_service owns entire slide)

---

## Key Concepts

### Format Ownership Model

**Layout Builder Owns**:
- `slide_title`: Structured labels
- `subtitle`: Descriptive text
- Grid positioning
- Responsive behavior
- Footer metadata

**Text Service Owns**:
- `rich_content` (L25): Full creative control over content area
- `hero_content` (L29): Full creative control over entire slide
- HTML generation
- Inline styling
- Element arrangement within areas

**Benefit**: No style conflicts, clear responsibilities

### Grid System

- **32 columns × 18 rows**
- CSS Grid-based positioning
- !important overrides for consistency
- Safe zone: columns 2-31, rows 2-17
- Debug tools: Press 'G' (grid), 'B' (borders), 'C' (content areas)

### Storage Architecture

**Three Tiers**:
1. **Tier 1**: In-memory cache (fastest, TTL-based)
2. **Tier 2**: Supabase (persistent, production)
3. **Tier 3**: Filesystem (fallback, always available)

**Selection**:
```python
if SUPABASE_CONFIGURED:
    # Check cache → Supabase → Done
else:
    # Use filesystem (ephemeral on Railway)
```

### Version History

- Automatic backup before each update
- Metadata: timestamp, creator, summary
- Restore to any previous version
- Optional backup before restore

---

## Common Tasks

### Add a New Layout

1. Create `src/renderers/LXX.js`:
```javascript
function renderLXX(content) {
  return `
    <section data-layout="LXX" class="grid-container">
      <!-- Your layout HTML -->
    </section>
  `;
}
```

2. Register in `presentation-viewer.html`:
```javascript
const RENDERERS = {
  'LXX': window.renderLXX,
  // ... existing layouts
};
```

3. Add to `models.py` valid layouts:
```python
valid_layouts = ["L01", "L02", "L03", "L25", "L27", "L29", "LXX"]
```

### Change Default Port

```bash
PORT=9000 python server.py
```

### Enable Supabase

1. Get credentials from Supabase dashboard
2. Set environment variables:
```env
SUPABASE_URL=https://...supabase.co
SUPABASE_SERVICE_KEY=...
ENABLE_SUPABASE=true
```

3. Restart server

### Customize Grid

Edit `src/styles/core/grid-system.css`:
```css
.reveal .slides section {
  grid-template-columns: repeat(32, 1fr) !important;
  grid-template-rows: repeat(18, 1fr) !important;
}
```

### Debug Presentation

While viewing at `http://localhost:8504/p/{id}`:

| Key | Action |
|-----|--------|
| `G` | Toggle grid overlay |
| `B` | Toggle border highlights |
| `C` | Toggle content area debug |
| `E` | Toggle edit mode |
| `?` | Show help |
| Arrow keys | Navigate slides |

### Test API

```bash
# Interactive documentation
http://localhost:8504/docs

# Or use curl/Postman
http://localhost:8504/api/presentations
```

---

## Troubleshooting

### Port Already in Use

```bash
lsof -i :8504
kill -9 [PID]

# Or use different port:
PORT=8505 python server.py
```

### Supabase Not Configured

**Error**: Presentations not persisting on restart

**Fix**: 
1. Check `.env` has `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`
2. Check `ENABLE_SUPABASE=true`
3. Restart server
4. Check logs for Supabase errors

**Fallback**: Uses filesystem (ephemeral)

### Chart Not Rendering

**Error**: Blank presentation or missing chart

**Check**:
1. Verify `<script>` tag is in HTML
2. Check Chart.js/ApexCharts library loaded (F12 console)
3. Verify chart container has explicit dimensions
4. Check browser console for JavaScript errors

**Solution**: Ensure chart HTML is complete and properly formatted

### Content Area Too Small

**Error**: Rich content overflows or looks cramped

**Remember**:
- L25 rich_content: 1800×720px max
- L29 hero_content: 1920×1080px full slide
- L01 element_4: 1800×600px
- L02 diagram: 1260×720px

**Fix**: Adjust content HTML to fit dimensions

### API Returns 422 Validation Error

**Error**: "Unprocessable Entity"

**Check**:
1. Required fields present? (title, slides, layout, content)
2. Layout name valid? (L01-L29 only)
3. Slide index in range?
4. Max lengths OK? (title: 200 chars, slide_title: 80 chars)

**Example Valid Request**:
```json
{
  "title": "Valid Title",
  "slides": [{
    "layout": "L25",
    "content": {
      "slide_title": "Hello",
      "rich_content": "<p>World</p>"
    }
  }]
}
```

### Presentations Lost After Restart

**Cause**: Using filesystem storage (ephemeral on Railway)

**Solution**: Enable Supabase in `.env`:
```env
ENABLE_SUPABASE=true
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-key
```

---

## Keyboard Shortcuts (Presentation Viewer)

| Key | Action |
|-----|--------|
| `←` / `→` | Navigate slides |
| `Esc` | Slide overview |
| `G` | Grid overlay on/off |
| `B` | Border highlights on/off |
| `C` | Content area debug on/off |
| `E` | Edit mode toggle |
| `Ctrl+S` | Save edits |
| `?` | Show help |
| `F` | Fullscreen |
| `S` | Speaker notes |

---

## Resource Files

| Path | Purpose |
|------|---------|
| `/docs/ARCHITECTURE.md` | Detailed system design |
| `/docs/LAYOUT_SPECIFICATIONS.md` | Grid positions and dimensions |
| `/docs/CONTENT_GENERATION_GUIDE.md` | How to generate HTML content |
| `/docs/L02_DIRECTOR_INTEGRATION_GUIDE.md` | Director Agent integration |
| `/tests/README.md` | Test documentation |
| `README.md` | Main project documentation |

---

## Summary

- **Fast Start**: `python server.py` (port 8504)
- **Create Presentation**: POST `/api/presentations`
- **View Presentation**: GET `/p/{id}`
- **Edit Content**: PUT `/api/presentations/{id}/slides/{index}`
- **API Docs**: GET `/docs` (Swagger UI)
- **All Layouts**: L01, L02, L03, L25, L27, L29
- **Storage**: Supabase (persistent) + Filesystem (fallback)
- **Grid**: 32 columns × 18 rows

---

**For detailed information, see `/CODEBASE_ANALYSIS.md`**
