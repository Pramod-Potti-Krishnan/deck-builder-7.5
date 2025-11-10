# v7.5-main: Simplified Layout Builder

**Version**: 7.5.0
**Port**: 8504
**Philosophy**: Text Service owns content creation, Layout Builder provides structure

---

## Overview

v7.5-main represents a **radical simplification** of the presentation layout system. Instead of managing 24+ complex layouts, we now have just **2 layouts** that give Text Service full creative control over content areas.

### The Problem We Solved

Previous versions (v7.2-small) had:
- 24 layouts with rigid structures
- Format conflicts between Text Service and Layout Builder
- Complex maintenance (24+ renderer files)
- Limited creative freedom for Text Service

### The v7.5 Solution

**Only 2 layouts**:
1. **L25**: Main content shell (1800×720px creative area)
2. **L29**: Full-bleed slides (1920×1080px) - for title/section/ending/hero

**Result**:
- Text Service has full creative control
- No format conflicts (clear ownership)
- Easy maintenance (2 renderer files)
- Unlimited layout possibilities within content areas

---

## Quick Start

### Installation

```bash
cd /path/to/v7.5-main

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (required for PDF/PPTX download)
playwright install chromium

# Start server
python server.py
```

Server runs on **http://localhost:8504**

**Dependencies**:
- Python 3.10+
- FastAPI, Uvicorn, Pydantic (for API server)
- Playwright, python-pptx, Pillow (for PDF/PPTX export)

### Create Your First Presentation

```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First v7.5 Presentation",
    "slides": [
      {
        "layout": "L29",
        "content": {
          "hero_content": "<div style=\"width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center;\"><h1 style=\"font-size: 96px; color: white; font-weight: 900;\">Welcome to v7.5</h1><p style=\"font-size: 42px; color: rgba(255,255,255,0.9); margin-top: 32px;\">Simplified Layout Architecture</p></div>"
        }
      },
      {
        "layout": "L25",
        "content": {
          "slide_title": "Key Benefits",
          "subtitle": "Why v7.5 is Better",
          "rich_content": "<div style=\"padding: 40px; font-size: 24px;\"><ul><li>Simpler</li><li>More flexible</li><li>Easier to maintain</li></ul></div>"
        }
      }
    ]
  }'
```

Response:
```json
{
  "id": "abc123...",
  "url": "/p/abc123...",
  "message": "Presentation created successfully"
}
```

View at: **http://localhost:8504/p/abc123...**

---

## The 2 Layouts

### L29: Full-Bleed Slides

**Use for**: Title slides, section dividers, ending slides, hero moments
**Content Area**: 1920px × 1080px (full slide)
**Format Owner**: Text Service owns `hero_content` field (complete creative control)

**Use Case 1 - Title Slide**:
```json
{
  "layout": "L29",
  "content": {
    "hero_content": "<div style=\"width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px;\"><h1 style=\"font-size: 96px; color: white; font-weight: 900; text-align: center;\">AI in Healthcare</h1><p style=\"font-size: 42px; color: rgba(255,255,255,0.9); text-align: center; margin-top: 32px;\">Transforming Patient Care</p><div style=\"margin-top: 64px; font-size: 28px; color: rgba(255,255,255,0.8);\">Dr. Jane Smith<br>Medical AI Labs</div></div>"
  }
}
```

**Use Case 2 - Section Divider**:
```json
{
  "layout": "L29",
  "content": {
    "hero_content": "<div style=\"width: 100%; height: 100%; background: #1f2937; display: flex; align-items: center; justify-content: center;\"><h2 style=\"font-size: 72px; color: white; font-weight: 700; border-left: 8px solid #3b82f6; padding-left: 40px;\">Implementation Roadmap</h2></div>"
  }
}
```

**Use Case 3 - Ending Slide**:
```json
{
  "layout": "L29",
  "content": {
    "hero_content": "<div style=\"width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center;\"><h1 style=\"font-size: 96px; color: white; font-weight: 900;\">Thank You</h1><p style=\"font-size: 32px; color: rgba(255,255,255,0.9); margin-top: 48px;\">Questions?</p></div>"
  }
}
```

### L25: Main Content Shell

**Use for**: 80% of your slides (main content)
**Content Area**: 1800px × 720px (Text Service controls)
**Format Owner**: Text Service owns `rich_content` field
**Footer**: Optional presentation name (left) and company logo (right)

**Example**:
```json
{
  "layout": "L25",
  "content": {
    "slide_title": "Key Metrics",
    "subtitle": "Q4 Performance",
    "rich_content": "<div style=\"display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;\"><div style=\"background: #3b82f6; color: white; padding: 32px; border-radius: 12px; text-align: center;\"><div style=\"font-size: 48px; font-weight: bold;\">25%</div><p>Cost Savings</p></div></div>",
    "presentation_name": "Q4 Business Review",
    "company_logo": "<img src='logo.png' style='height: 20px;'>"
  }
}
```

**Footer Fields** (both optional):
- `presentation_name`: Text displayed in footer left section (5 grids)
- `company_logo`: HTML/image displayed in footer right section (3 grids)

---

## Format Ownership Model

### Layout Builder Owns:
- **L25**: slide_title, subtitle
- **L29**: Nothing (Text Service owns entire slide)
- Grid positioning
- Slide backgrounds
- Footer metadata

### Text Service Owns:
- **L25**: rich_content (HTML with full styling)
- **L29**: hero_content (HTML with full styling) - including title/section/ending/hero slides
- Content creation and formatting
- HTML structure within content areas
- All inline styles and layout

---

## API Endpoints

### Create Presentation
```
POST /api/presentations
Content-Type: application/json

{
  "title": "Presentation Title",
  "slides": [...]
}

Response:
{
  "id": "uuid",
  "url": "/p/uuid",
  "message": "Success message"
}
```

### Get Presentation Data
```
GET /api/presentations/{id}

Response: { JSON presentation data }
```

### View Presentation
```
GET /p/{id}

Response: HTML viewer
```

### List All Presentations
```
GET /api/presentations

Response:
{
  "count": 5,
  "presentations": [...]
}
```

### Delete Presentation
```
DELETE /api/presentations/{id}

Response:
{
  "success": true,
  "message": "Deleted"
}
```

### Download Presentation as PDF
```
GET /api/presentations/{id}/download/pdf?landscape=true&quality=high

Parameters:
- landscape (boolean, default: true): Use landscape orientation
- print_background (boolean, default: true): Include backgrounds and gradients
- quality (string, default: "high"): Quality level - "high", "medium", or "low"

Response: PDF file download
```

**Example**:
```bash
# Download as PDF
curl "http://localhost:8504/api/presentations/{id}/download/pdf?quality=high" \
  -o presentation.pdf

# Or use a browser:
# http://localhost:8504/api/presentations/{id}/download/pdf
```

### Download Presentation as PPTX
```
GET /api/presentations/{id}/download/pptx?aspect_ratio=16:9&quality=high

Parameters:
- aspect_ratio (string, default: "16:9"): Aspect ratio - "16:9" or "4:3"
- quality (string, default: "high"): Image quality - "high", "medium", or "low"

Response: PPTX file download
```

**Example**:
```bash
# Download as PowerPoint
curl "http://localhost:8504/api/presentations/{id}/download/pptx?quality=high" \
  -o presentation.pptx

# Or use a browser:
# http://localhost:8504/api/presentations/{id}/download/pptx
```

**Quality Settings**:
- **high**: Full resolution (1920×1080) - Best quality, larger file size
- **medium**: 75% resolution (1440×810) - Good balance
- **low**: 50% resolution (960×540) - Smallest file size

---

## For Text Service Developers

### Required Reading
📖 **[Content Generation Guide](docs/CONTENT_GENERATION_GUIDE.md)** - Comprehensive guide on generating HTML for v7.5

### Quick Tips

**L25 Content Generation**:
```python
def generate_l25_content(slide_data):
    return {
        "slide_title": "Plain text (max 80 chars)",
        "subtitle": "Plain text (max 120 chars)",
        "rich_content": f"""
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; padding: 32px;">
                {generate_cards(slide_data.key_points)}
            </div>
        """,
        "presentation_name": "Q4 Business Review",  # Optional
        "company_logo": "<img src='logo.png' style='height: 20px;'>"  # Optional
    }
```

**L29 Content Generation**:
```python
def generate_l29_hero(slide_data):
    return {
        "hero_content": f"""
            <div style="width: 100%; height: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px;">
                <h1 style="font-size: 96px; color: white; font-weight: 900; text-align: center;">{slide_data.title}</h1>
                <p style="font-size: 42px; color: rgba(255,255,255,0.9); text-align: center; max-width: 1400px; margin-top: 48px;">{slide_data.tagline}</p>
            </div>
        """
    }
```

---

## Keyboard Shortcuts

When viewing presentations:
- **G**: Toggle grid overlay
- **B**: Toggle border highlights
- **C**: Toggle content area debug mode
- **?**: Show help text
- **Arrow keys**: Navigate slides
- **Esc**: Overview mode

---

## Directory Structure

```
v7.5-main/
├── server.py                      # FastAPI server (port 8504)
├── models.py                      # Pydantic models (including download options)
├── storage.py                     # JSON file storage
├── requirements.txt               # Python dependencies
├── test_downloads_manual.py       # Manual download testing script
├── converters/                    # Download/export converters
│   ├── __init__.py
│   ├── base.py                   # Base converter with screenshot capture
│   ├── pdf_converter.py          # PDF generation using Playwright
│   └── pptx_converter.py         # PPTX generation using python-pptx
├── tests/                         # Test suites
│   ├── __init__.py
│   └── conftest.py               # Pytest configuration and fixtures
├── src/
│   ├── renderers/
│   │   ├── L01_Shell.js          # Structural layout renderer
│   │   ├── L25.js                # Main content renderer
│   │   └── L29.js                # Hero full-bleed renderer
│   ├── styles/
│   │   ├── core/                 # Grid system, reset, borders
│   │   └── content-area.css      # Text Service isolation
│   ├── utils/
│   │   └── format_ownership.js   # Format ownership utility
│   └── core/
│       └── reveal-config.js      # Reveal.js configuration
├── viewer/
│   └── presentation-viewer.html  # Reveal.js viewer
├── storage/
│   └── presentations/            # JSON presentation files
└── docs/
    ├── CONTENT_GENERATION_GUIDE.md  # For Text Service devs
    └── ARCHITECTURE.md              # System architecture
```

---

## Testing

### Run Test Server
```bash
python server.py
```

### Test API
```bash
# Create presentation
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test-presentation.json

# List presentations
curl http://localhost:8504/api/presentations

# Get specific presentation
curl http://localhost:8504/api/presentations/{id}
```

### Manual Testing
1. Start server: `python server.py`
2. Navigate to: `http://localhost:8504/docs` (FastAPI auto-docs)
3. Test endpoints interactively
4. View presentations at `/p/{id}`

### Test Download Endpoints
```bash
# Run comprehensive download test
python3 test_downloads_manual.py
```

This script will:
1. Create a test presentation with 4 slides
2. Download it as PDF and PPTX
3. Validate file formats
4. Test error handling
5. Save outputs to `test_output/` directory

**Manual download testing**:
```bash
# 1. Create a presentation and get its ID
PRES_ID=$(curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test-presentation.json | jq -r '.id')

# 2. Download as PDF
curl "http://localhost:8504/api/presentations/$PRES_ID/download/pdf" \
  -o my_presentation.pdf

# 3. Download as PPTX
curl "http://localhost:8504/api/presentations/$PRES_ID/download/pptx" \
  -o my_presentation.pptx

# 4. Open files to verify
open my_presentation.pdf
open my_presentation.pptx
```

---

## Integration with Director

Director Agent should:
1. Select layout based on slide purpose:
   - Title slides → L29 (Director tells Text Service: "this is a title slide")
   - Section breaks → L29 (Director tells Text Service: "this is a section divider")
   - Main content → L25
   - Hero moments → L29 (Director tells Text Service: "this is a hero slide")
   - Ending slides → L29 (Director tells Text Service: "this is an ending slide")

2. Call Text Service with field specifications:
```python
{
  "layout_id": "L25",
  "field_specifications": {
    "rich_content": {
      "format_owner": "text_service",
      "content_area": {
        "pixels": {"width": 1800, "height": 720}
      }
    }
  }
}
```

3. Transform Text Service response → v7.5 format

4. POST to v7.5-main at port 8504

---

## Comparison with v7.2-small

| Feature | v7.2-small | v7.5-main |
|---------|-----------|-----------|
| Layouts | 24 layouts | 2 layouts |
| Port | 8503 | 8504 |
| Renderers | 27 files | 2 files |
| Format Ownership | Partial | Complete |
| Text Service Control | Limited | Full creative control |
| Maintenance | Complex | Simple |
| Content Areas | Fixed per layout | 1800×720 (L25), 1920×1080 (L29) |

---

## Migration from v7.2-small

v7.2-small is **preserved** and continues running on port 8503.

To migrate presentations:
1. Identify slide purposes (structural vs content)
2. Map to v7.5 layouts:
   - L01 (title) → L29 (Text Service generates title slide HTML)
   - L02 (section) → L29 (Text Service generates section divider HTML)
   - L03 (ending) → L29 (Text Service generates ending slide HTML)
   - L04-L24 → L25 or L29 (depending on content type)
3. Regenerate all content with Text Service (full HTML generation)
4. Test in v7.5-main

---

## Troubleshooting

### Content Not Rendering
- Check console for errors (F12)
- Verify JSON structure matches schema
- Ensure layout name is exact: "L01-Shell", "L25", or "L29"

### Content Overflows
- L25: Check content height ≤ 720px
- L29: Check content fits 1920×1080px exactly
- Press 'C' to debug content areas

### Styling Issues
- Use inline styles only (no CSS classes)
- Check for conflicting grid properties
- Verify HTML is well-formed

---

## Contributing

### Adding New Patterns

To add new HTML patterns for Text Service:
1. Create pattern in `docs/CONTENT_GENERATION_GUIDE.md`
2. Test with real content
3. Validate dimensions
4. Document usage

### Reporting Issues

Found a bug? Open an issue with:
- Presentation JSON
- Expected vs actual behavior
- Screenshots
- Browser/version

---

## License

Internal use only - Deckster project

---

## Version History

- **v7.5.0** (2025-01-01): Initial release
  - 2-layout system (L25 + L29)
  - Full Text Service creative control
  - L29 handles all full-bleed slides (title/section/ending/hero)
  - Content area isolation
  - Comprehensive documentation

---

## Support

- **Documentation**: `/docs/CONTENT_GENERATION_GUIDE.md`
- **API Docs**: `http://localhost:8504/docs`
- **Issues**: Contact Layout Builder team

---

**Ready to build amazing presentations with v7.5-main!** 🚀
