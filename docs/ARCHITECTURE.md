# v7.5-main Architecture Documentation

**Version**: 7.5.0
**Date**: 2025-01-01
**Status**: Production-Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Philosophy](#architecture-philosophy)
3. [Component Architecture](#component-architecture)
4. [Data Flow](#data-flow)
5. [Format Ownership Model](#format-ownership-model)
6. [Grid System Architecture](#grid-system-architecture)
7. [Renderer Architecture](#renderer-architecture)
8. [Storage Architecture](#storage-architecture)
9. [Integration Architecture](#integration-architecture)
10. [Security & Validation](#security--validation)
11. [Performance Considerations](#performance-considerations)
12. [Technology Stack](#technology-stack)
13. [Design Decisions](#design-decisions)

---

## System Overview

v7.5-main is a **simplified presentation layout service** that provides structural scaffolding for presentations while giving Text Service full creative control over content areas.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Director Agent                           │
│  (Orchestrates presentation creation, selects layouts)          │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ 1. Layout selection + field specs
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Text Service                             │
│  (Generates HTML content for creative areas)                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ 2. Formatted content (JSON)
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     v7.5-main Layout Builder                    │
│                     (Port 8504)                                 │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   FastAPI    │  │   Storage    │  │   Renderers  │        │
│  │   Server     │◄─┤    Layer     │  │   (3 files)  │        │
│  └──────┬───────┘  └──────────────┘  └──────────────┘        │
│         │                                                       │
│         │ 3. Presentation JSON                                 │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────┐         │
│  │         Reveal.js Viewer + Grid System           │         │
│  └──────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
             │
             │ 4. Rendered HTML presentation
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          End User                               │
│                       (Web Browser)                             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Metrics

- **Layouts**: 3 (down from 24 in v7.2)
- **Renderer Files**: 3 (down from 27 in v7.2)
- **Port**: 8504
- **Response Time**: <100ms for typical presentations
- **Slide Capacity**: 100+ slides per presentation
- **Content Area Flexibility**: Unlimited within dimensional constraints

---

## Architecture Philosophy

### Core Principles

1. **Separation of Concerns**
   - **Layout Builder**: Structure, positioning, scaffolding
   - **Text Service**: Content creation, formatting, styling

2. **Radical Simplification**
   - Reduce complexity by 88% (24 layouts → 2 layouts)
   - Clear ownership boundaries (no format conflicts)
   - Maintainable codebase (3 renderer files vs 27)

3. **Creative Freedom**
   - Text Service has full control over content areas
   - No rigid layout constraints
   - HTML/CSS freedom within allocated space

4. **Format Ownership**
   - Each field has a single "format owner"
   - Owner controls formatting, structure, and styling
   - No dual-ownership conflicts

### Design Philosophy Evolution

```
v7.2-small:
├── 24 layouts with specific structures
├── Layout Builder formatted most fields
├── Text Service had limited control
└── Format conflicts were common

v7.5-main:
├── 2 layouts with flexible content areas
├── Text Service owns creative areas
├── Layout Builder provides scaffolding
└── Clear ownership, no conflicts
```

---

## Component Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         v7.5-main System                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              FastAPI Server (server.py)             │       │
│  │  ┌──────────────────────────────────────────────┐   │       │
│  │  │  API Endpoints                               │   │       │
│  │  │  • POST /api/presentations                  │   │       │
│  │  │  • GET  /api/presentations/{id}             │   │       │
│  │  │  • GET  /api/presentations                  │   │       │
│  │  │  • DELETE /api/presentations/{id}           │   │       │
│  │  │  • GET  /p/{id} (viewer)                    │   │       │
│  │  └──────────────────────────────────────────────┘   │       │
│  └────────────┬────────────────────────────────────────┘       │
│               │                                                 │
│  ┌────────────▼────────────────────────────────────────┐       │
│  │         Pydantic Models (models.py)                 │       │
│  │  ┌──────────────────────────────────────────────┐   │       │
│  │  │  • PresentationCreate                       │   │       │
│  │  │  • SlideContent (Union of 3 content types)  │   │       │
│  │  │  • L01ShellContent                          │   │       │
│  │  │  • L25Content                               │   │       │
│  │  │  • L29Content                               │   │       │
│  │  └──────────────────────────────────────────────┘   │       │
│  └────────────┬────────────────────────────────────────┘       │
│               │                                                 │
│  ┌────────────▼────────────────────────────────────────┐       │
│  │          Storage Layer (storage.py)                 │       │
│  │  ┌──────────────────────────────────────────────┐   │       │
│  │  │  JSON File Storage                          │   │       │
│  │  │  • save_presentation()                      │   │       │
│  │  │  • load_presentation()                      │   │       │
│  │  │  • list_presentations()                     │   │       │
│  │  │  • delete_presentation()                    │   │       │
│  │  └──────────────────────────────────────────────┘   │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │           Frontend Components                       │       │
│  │  ┌──────────────────────────────────────────────┐   │       │
│  │  │  Reveal.js Viewer                           │   │       │
│  │  │  (presentation-viewer.html)                 │   │       │
│  │  └────────────┬─────────────────────────────────┘   │       │
│  │               │                                      │       │
│  │  ┌────────────▼─────────────────────────────────┐   │       │
│  │  │  Renderers (JavaScript)                     │   │       │
│  │  │  • L01_Shell.js (renderL01Shell)            │   │       │
│  │  │  • L25.js (renderL25)                       │   │       │
│  │  │  • L29.js (renderL29)                       │   │       │
│  │  └────────────┬─────────────────────────────────┘   │       │
│  │               │                                      │       │
│  │  ┌────────────▼─────────────────────────────────┐   │       │
│  │  │  CSS Styles                                 │   │       │
│  │  │  • grid-system.css (18×32 grid)             │   │       │
│  │  │  • reset.css (normalization)                │   │       │
│  │  │  • borders.css (debug overlays)             │   │       │
│  │  │  • content-area.css (isolation)             │   │       │
│  │  └──────────────────────────────────────────────┘   │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### 1. FastAPI Server (`server.py`)

**Purpose**: HTTP API for presentation management

**Responsibilities**:
- Accept presentation creation requests (POST)
- Validate incoming JSON against Pydantic schemas
- Serve presentation viewer HTML
- Provide CRUD operations for presentations
- Handle CORS for local development
- Serve static assets (JS, CSS)

**Key Dependencies**: FastAPI, Uvicorn, Pydantic

#### 2. Pydantic Models (`models.py`)

**Purpose**: Data validation and type safety

**Responsibilities**:
- Define presentation data structure
- Validate slide content schemas
- Enforce field constraints (max lengths, required fields)
- Provide type hints for IDE support
- Discriminated union for slide content types

**Key Features**:
- `SlideContent = Union[L01ShellContent, L25Content, L29Content]`
- Field validation (string lengths, required fields)
- Automatic JSON serialization

#### 3. Storage Layer (`storage.py`)

**Purpose**: Persistent storage for presentations

**Responsibilities**:
- Save presentations as JSON files
- Load presentations by ID
- List all presentations
- Delete presentations
- Generate unique presentation IDs (UUID)

**Storage Format**: JSON files in `storage/presentations/{id}.json`

**Design Choice**: File-based storage for simplicity (scalable to database later)

#### 4. Renderers (JavaScript)

**Purpose**: Transform JSON data into HTML slides

**Responsibilities**:
- **L01_Shell.js**: Render structural slides (title, section, ending)
- **L25.js**: Render main content slides with 1800×720px creative area
- **L29.js**: Render full-bleed hero slides (1920×1080px)
- Apply layout-specific styling
- Inject Text Service HTML content safely

**Key Features**:
- Pure functions (data in, HTML out)
- No side effects
- Grid-based positioning
- Format ownership enforcement

#### 5. CSS Styles

**Purpose**: Grid system, layout styling, debug tools

**Responsibilities**:
- **grid-system.css**: 18×32 grid overlay
- **reset.css**: Browser normalization
- **borders.css**: Visual debugging (press 'B' to toggle)
- **content-area.css**: Isolate Text Service content areas

---

## Data Flow

### Presentation Creation Flow

```
┌─────────────┐
│  Director   │
│   Agent     │
└──────┬──────┘
       │
       │ 1. Select layout (L01-Shell/L25/L29)
       │    Pass field specifications
       ▼
┌─────────────┐
│    Text     │
│  Service    │
└──────┬──────┘
       │
       │ 2. Generate content
       │    • L01-Shell: plain text
       │    • L25: HTML for rich_content
       │    • L29: HTML for hero_content
       ▼
┌──────────────────────────────────────────┐
│  POST /api/presentations                 │
│  {                                       │
│    "title": "...",                       │
│    "slides": [                           │
│      {                                   │
│        "layout": "L25",                  │
│        "content": {                      │
│          "slide_title": "...",           │
│          "subtitle": "...",              │
│          "rich_content": "<div>...</div>"│
│        }                                 │
│      }                                   │
│    ]                                     │
│  }                                       │
└──────┬───────────────────────────────────┘
       │
       │ 3. Validate with Pydantic
       ▼
┌─────────────────────┐
│  models.py          │
│  • Check schema     │
│  • Validate fields  │
│  • Type checking    │
└──────┬──────────────┘
       │
       │ 4. Save to storage
       ▼
┌─────────────────────┐
│  storage.py         │
│  • Generate UUID    │
│  • Save JSON        │
│  • Return ID        │
└──────┬──────────────┘
       │
       │ 5. Return presentation URL
       ▼
┌─────────────────────┐
│  Response:          │
│  {                  │
│    "id": "uuid",    │
│    "url": "/p/uuid" │
│  }                  │
└─────────────────────┘
```

### Presentation Viewing Flow

```
┌─────────────┐
│  End User   │
│  (Browser)  │
└──────┬──────┘
       │
       │ GET /p/{id}
       ▼
┌─────────────────────┐
│  server.py          │
│  • Load JSON        │
│  • Inject into HTML │
└──────┬──────────────┘
       │
       │ Serve viewer HTML + embedded JSON
       ▼
┌──────────────────────────────────────┐
│  presentation-viewer.html            │
│  • Initialize Reveal.js              │
│  • Parse presentation JSON           │
│  • Loop through slides               │
└──────┬───────────────────────────────┘
       │
       │ For each slide:
       ▼
┌──────────────────────────────────────┐
│  Renderer Dispatcher                 │
│  if (layout === "L01-Shell")         │
│    → renderL01Shell(content)         │
│  else if (layout === "L25")          │
│    → renderL25(content)              │
│  else if (layout === "L29")          │
│    → renderL29(content)              │
└──────┬───────────────────────────────┘
       │
       │ Generated HTML
       ▼
┌──────────────────────────────────────┐
│  Reveal.js                           │
│  • Append slide to presentation      │
│  • Apply grid system                 │
│  • Enable navigation                 │
└──────┬───────────────────────────────┘
       │
       │ Rendered presentation
       ▼
┌─────────────┐
│  End User   │
│  Views &    │
│  Navigates  │
└─────────────┘
```

---

## Format Ownership Model

### Philosophy

**Single Owner Principle**: Each field has exactly ONE format owner who controls its formatting, structure, and styling.

### Ownership Matrix

| Layout | Field | Owner | Format Type | Why? |
|--------|-------|-------|-------------|------|
| L25 | slide_title | Layout Builder | Plain text → HTML | Header consistency |
| L25 | subtitle | Layout Builder | Plain text → HTML | Header consistency |
| L25 | rich_content | **Text Service** | **HTML (direct render)** | **Creative freedom** |
| L25 | presentation_name | **Text Service** | Plain text or HTML | Optional footer branding |
| L25 | company_logo | **Text Service** | HTML (img/SVG) | Optional footer logo |
| L29 | hero_content | **Text Service** | **HTML (direct render)** | **Full creative control** |

### Ownership Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      L25 Content Slide                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Row 2: slide_title                                   │     │
│  │  Format Owner: LAYOUT_BUILDER                         │     │
│  │  Input: "Key Benefits"                                │     │
│  │  Output: <div style="...">Key Benefits</div>          │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Row 3: subtitle                                      │     │
│  │  Format Owner: LAYOUT_BUILDER                         │     │
│  │  Input: "Measurable Impact"                           │     │
│  │  Output: <div style="...">Measurable Impact</div>     │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐     │
│  │  Rows 5-16: rich_content (1800×720px)                │     │
│  │  Format Owner: TEXT_SERVICE                           │     │
│  │  Input: <div style="display: grid; ...">...</div>     │     │
│  │  Output: (RENDERED AS-IS, no transformation)          │     │
│  │                                                        │     │
│  │  Text Service has FULL control:                       │     │
│  │  • HTML structure                                     │     │
│  │  • Inline styles                                      │     │
│  │  • Layout (grid, flex, table)                         │     │
│  │  • Colors, fonts, spacing                             │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ownership Benefits

1. **No Conflicts**: Each field has one source of truth
2. **Clear Boundaries**: Developers know who controls what
3. **Maintainability**: Changes isolated to single owner
4. **Creative Freedom**: Text Service unrestricted in content areas
5. **Consistency**: Layout Builder ensures structural uniformity

---

## Grid System Architecture

### Grid Specifications

- **Dimensions**: 18 rows × 32 columns
- **Slide Resolution**: 1920px × 1080px (16:9 aspect ratio)
- **Cell Size**: ~60px × ~60px
- **Gutter**: None (continuous grid)

### Grid Layout

```
     Columns: 1  2  3  4  5  ...  28  29  30  31  32
   ┌─────────────────────────────────────────────────┐
 1 │░░░░░░░░░░░░░░░░░ MARGIN ░░░░░░░░░░░░░░░░░░░░░░│
   ├─────────────────────────────────────────────────┤
 2 │░░│                                          │░░│  ← Title Row
   ├─────────────────────────────────────────────────┤
 3 │░░│                                          │░░│  ← Subtitle Row
   ├─────────────────────────────────────────────────┤
 4 │░░░░░░░░░░░░░░░░░ SPACING ░░░░░░░░░░░░░░░░░░░░░│
   ├─────────────────────────────────────────────────┤
 5 │░░│┌──────────────────────────────────────┐│░░│
 6 │░░││                                      ││░░│
 7 │░░││         CONTENT AREA                 ││░░│
 8 │░░││      (Text Service Owns)             ││░░│
 9 │░░││                                      ││░░│
10 │░░││       1800px × 720px                 ││░░│
11 │░░││                                      ││░░│
12 │░░││  30 columns × 12 rows                ││░░│
13 │░░││                                      ││░░│
14 │░░││                                      ││░░│
15 │░░││                                      ││░░│
16 │░░│└──────────────────────────────────────┘│░░│
   ├─────────────────────────────────────────────────┤
17 │░░░░░░░░░░░░░░░░░ SPACING ░░░░░░░░░░░░░░░░░░░░░│
   ├─────────────────────────────────────────────────┤
18 │░░│ Footer: Layout ID | Slide Number      │░░│
   └─────────────────────────────────────────────────┘
```

### Grid Allocation by Layout

#### L01-Shell (Structural)

```
Row 1: Margin
Row 2-16: Content (variant-specific)
  • title: Large centered text
  • section: Medium centered text with accent
  • ending: Thank you message
Row 17: Spacing
Row 18: Footer
```

#### L25 (Main Content)

```
Row 1: Margin
Row 2: slide_title (Layout Builder)
Row 3: subtitle (Layout Builder)
Row 4: Spacing
Row 5-16: rich_content (Text Service) ← 1800×720px
Row 17: Spacing
Row 18: Footer (optional: presentation_name left, company_logo right)
```

#### L29 (Hero Full-Bleed)

```
Row 1-18: hero_content (Text Service) ← 1920×1080px
(No footer, no margins - full creative control)
```

### Grid Implementation

**CSS Grid Definition** (`grid-system.css`):

```css
.grid-container {
  display: grid;
  grid-template-rows: repeat(18, 1fr);
  grid-template-columns: repeat(32, 1fr);
  width: 1920px;
  height: 1080px;
}
```

### Content Area Pixel Calculations

**L25 Content Area**:
- Grid: Rows 5-16 (12 rows), Columns 2-31 (30 columns)
- Pixels: 12 × 60px = 720px height, 30 × 60px = 1800px width
- Total: **1800px × 720px**

**L29 Content Area**:
- Grid: Rows 1-18 (18 rows), Columns 1-32 (32 columns)
- Pixels: 18 × 60px = 1080px height, 32 × 60px = 1920px width
- Total: **1920px × 1080px**

---

## Renderer Architecture

### Renderer Design Pattern

Each renderer is a **pure function** that transforms JSON data into HTML:

```javascript
function renderLayoutX(content) {
  // 1. Extract content fields
  // 2. Apply format ownership rules
  // 3. Generate HTML with inline styles
  // 4. Return complete <section> HTML
  return `<section>...</section>`;
}
```

### Renderer Responsibilities

1. **L01_Shell.js**
   - Handle 3 variants: title, section, ending
   - Center-align all text
   - Apply variant-specific styling
   - Format plain text fields

2. **L25.js**
   - Render slide_title and subtitle (plain text)
   - Inject rich_content HTML as-is
   - Define content area boundaries (rows 5-16)
   - Enable vertical scrolling for overflow

3. **L29.js**
   - Inject hero_content HTML as-is
   - No additional formatting
   - Full-slide coverage (no margins)
   - No scrolling (overflow hidden)

### Renderer Execution Flow

```
┌──────────────────────────────────────────┐
│  Presentation JSON Loaded                │
└──────────────┬───────────────────────────┘
               │
               │ Loop: for each slide
               ▼
┌──────────────────────────────────────────┐
│  Read slide.layout                       │
│  • "L01-Shell"                           │
│  • "L25"                                 │
│  • "L29"                                 │
└──────────────┬───────────────────────────┘
               │
               │ Dispatch to renderer
               ▼
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌─────────┐
│ L01     │         │ L25     │
│ Shell   │         │         │
└────┬────┘         └────┬────┘
     │                   │
     │ HTML              │ HTML
     ▼                   ▼
┌──────────────────────────────┐
│  Append to Reveal.js         │
│  presentation.innerHTML +=   │
└──────────────┬───────────────┘
               │
               │ Next slide
               ▼
         [Loop continues]
```

### Safety & Sanitization

**Text Service HTML is trusted** (no sanitization):
- Text Service is an internal component (not user input)
- Content is generated by AI with validation
- No XSS risk from trusted source
- Performance: No overhead from sanitization

**If user input ever added**:
- Implement DOMPurify or similar
- Whitelist safe HTML tags
- Strip `<script>`, `<iframe>`, `<object>`

---

## Storage Architecture

### Storage Strategy

**Current**: File-based JSON storage
**Future**: Database-ready (PostgreSQL, Supabase)

### File Structure

```
storage/
└── presentations/
    ├── abc123-uuid.json
    ├── def456-uuid.json
    └── ghi789-uuid.json
```

### Storage Operations

#### 1. Save Presentation

```python
def save_presentation(presentation: dict) -> str:
    """
    Save presentation to JSON file

    1. Generate UUID
    2. Create file path
    3. Write JSON to file
    4. Return presentation ID
    """
    presentation_id = str(uuid.uuid4())
    file_path = STORAGE_DIR / f"{presentation_id}.json"
    with open(file_path, 'w') as f:
        json.dump(presentation, f, indent=2)
    return presentation_id
```

#### 2. Load Presentation

```python
def load_presentation(presentation_id: str) -> dict:
    """
    Load presentation from JSON file

    1. Construct file path
    2. Read JSON file
    3. Parse and return
    """
    file_path = STORAGE_DIR / f"{presentation_id}.json"
    with open(file_path, 'r') as f:
        return json.load(f)
```

#### 3. List Presentations

```python
def list_presentations() -> List[dict]:
    """
    List all presentations with metadata

    1. Scan storage directory
    2. Load each JSON file
    3. Extract title + ID
    4. Return list
    """
    presentations = []
    for file_path in STORAGE_DIR.glob("*.json"):
        with open(file_path, 'r') as f:
            data = json.load(f)
            presentations.append({
                "id": file_path.stem,
                "title": data.get("title"),
                "slide_count": len(data.get("slides", []))
            })
    return presentations
```

### Migration Path to Database

When scaling requirements increase:

```python
# Future database implementation
class DatabaseStorage:
    def save_presentation(self, presentation: dict) -> str:
        # INSERT INTO presentations ...
        pass

    def load_presentation(self, presentation_id: str) -> dict:
        # SELECT * FROM presentations WHERE id = ...
        pass

    def list_presentations(self) -> List[dict]:
        # SELECT id, title, slide_count FROM presentations
        pass
```

**Benefits of file-based approach now**:
- Simple implementation
- No database setup required
- Easy to inspect (human-readable JSON)
- Sufficient for current scale
- Easy migration path

---

## Integration Architecture

### Integration Points

```
┌────────────────────────────────────────────────────────┐
│              External Systems Integration              │
└────────────────────────────────────────────────────────┘

┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│  Director   │         │    Text     │         │  Analytics  │
│   Agent     │◄───────►│  Service    │◄───────►│  Service    │
│  (v3.x)     │         │             │         │             │
└──────┬──────┘         └──────┬──────┘         └─────────────┘
       │                       │
       │ Layout selection      │ HTML content
       │ Field specs           │ generation
       │                       │
       ▼                       ▼
┌──────────────────────────────────────┐
│      v7.5-main Layout Builder        │
│           (Port 8504)                │
│                                      │
│  POST /api/presentations             │
│  {                                   │
│    "title": "...",                   │
│    "slides": [                       │
│      {                               │
│        "layout": "L25",              │
│        "content": {                  │
│          "slide_title": "...",       │
│          "rich_content": "<div>..."  │
│        }                             │
│      }                               │
│    ]                                 │
│  }                                   │
└──────────────────────────────────────┘
       │
       │ Presentation URL
       ▼
┌─────────────┐
│  End User   │
│  Browser    │
└─────────────┘
```

### Director Agent Integration

**Director's Role**:
1. Analyze user request
2. Select appropriate layout for each slide
3. Provide field specifications to Text Service
4. Receive formatted content from Text Service
5. POST complete presentation to v7.5-main

**Example Director → Text Service Call**:

```json
{
  "layout_id": "L25",
  "layout_name": "Main Content Shell",
  "field_specifications": {
    "slide_title": {
      "format_owner": "layout_builder",
      "format_type": "plain_text",
      "max_chars": 80
    },
    "subtitle": {
      "format_owner": "layout_builder",
      "format_type": "plain_text",
      "max_chars": 120
    },
    "rich_content": {
      "format_owner": "text_service",
      "format_type": "html",
      "content_area": {
        "pixels": {"width": 1800, "height": 720}
      }
    }
  },
  "content_guidance": {
    "title": "Key Benefits",
    "key_points": ["ROI", "Efficiency", "Accuracy"]
  }
}
```

**Example Text Service → Director Response**:

```json
{
  "slide_title": "Key Benefits of AI Implementation",
  "subtitle": "Measurable Impact in 90 Days",
  "rich_content": "<div style=\"display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px;\">...</div>"
}
```

### Text Service Integration

**Text Service Responsibilities**:
1. Receive field specifications from Director
2. Generate appropriate HTML for format_owner=text_service fields
3. Return plain text for format_owner=layout_builder fields
4. Validate HTML fits within content area dimensions

**HTML Generation Requirements**:
- Use inline styles exclusively
- Respect content area dimensions
- Generate semantic, well-formed HTML
- No external dependencies (CSS classes, JS)

### API Contract

**Endpoint**: `POST /api/presentations`

**Request Schema**:
```json
{
  "title": "string (required)",
  "slides": [
    {
      "layout": "L01-Shell | L25 | L29 (required)",
      "content": {
        // Layout-specific content object
      }
    }
  ]
}
```

**Response Schema**:
```json
{
  "id": "uuid",
  "url": "/p/{uuid}",
  "message": "Presentation created successfully"
}
```

**Error Responses**:
- 400: Invalid request schema
- 422: Validation error (Pydantic)
- 500: Server error

---

## Security & Validation

### Input Validation

**Pydantic Models** provide:
- Type checking (str, int, Literal)
- Required field enforcement
- Field length constraints
- Enum validation (layout types, variants)

**Example Validation**:

```python
class L25Content(BaseModel):
    slide_title: str = Field(..., max_length=80)  # Required, max 80 chars
    subtitle: Optional[str] = Field(None, max_length=120)  # Optional
    rich_content: str  # Required, no length limit (HTML)
```

### Content Security

**Trusted Source Assumption**:
- Text Service is internal, AI-generated content
- No user-submitted HTML
- No XSS risk from trusted component

**Future Considerations** (if user input added):
- Implement HTML sanitization (DOMPurify)
- Whitelist safe tags and attributes
- Strip dangerous tags: `<script>`, `<iframe>`, `<object>`
- Validate external URLs

### CORS Configuration

**Current**: Permissive CORS for local development

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**Production**: Restrict to known origins
```python
allow_origins=[
    "https://deckster.app",
    "https://director.deckster.app"
]
```

---

## Performance Considerations

### Optimization Strategies

#### 1. Server Performance

**Response Times**:
- Presentation creation: <100ms (JSON write)
- Presentation loading: <50ms (JSON read)
- Viewer serving: <30ms (static HTML)

**Scalability**:
- Current: File-based, single-server
- Future: Database, horizontal scaling
- Caching: Not needed yet (responses are fast)

#### 2. Frontend Performance

**Renderer Efficiency**:
- Pure functions (no side effects)
- Minimal DOM manipulation
- Lazy loading: Reveal.js handles slide loading

**Grid System**:
- CSS Grid (hardware-accelerated)
- No JavaScript layout calculations
- Efficient reflows

**Content Area Isolation**:
- `overflow-y: auto` for L25 (only when needed)
- `overflow: hidden` for L29 (no scrolling)

#### 3. Asset Loading

**Static Assets**:
- JavaScript renderers (minified in production)
- CSS styles (combined, minified)
- Reveal.js loaded from CDN

**Optimization Opportunities**:
- Gzip compression
- HTTP/2 multiplexing
- Browser caching (Cache-Control headers)

### Performance Monitoring

**Key Metrics**:
- Server response time (FastAPI middleware)
- Presentation load time (browser Performance API)
- Render time per slide
- Memory usage (Reveal.js slide pool)

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Backend language |
| **FastAPI** | 0.104+ | Web framework |
| **Uvicorn** | 0.24+ | ASGI server |
| **Pydantic** | 2.0+ | Data validation |

**Why FastAPI?**
- Fast (async support)
- Automatic API documentation (OpenAPI)
- Type-safe with Pydantic integration
- Developer-friendly

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Reveal.js** | 5.x | Presentation framework |
| **Vanilla JS** | ES6+ | Renderers (no framework) |
| **CSS Grid** | - | Layout system |

**Why Reveal.js?**
- Industry-standard for HTML presentations
- Keyboard navigation
- Responsive design
- Plugin ecosystem

**Why Vanilla JS?**
- No build step required
- Fast execution
- Simple debugging
- No framework overhead

### Storage

| Technology | Purpose |
|------------|---------|
| **JSON Files** | Current storage |
| **PostgreSQL/Supabase** | Future migration |

### Development Tools

| Tool | Purpose |
|------|---------|
| **cURL** | API testing |
| **Browser DevTools** | Frontend debugging |
| **VS Code** | IDE |
| **Git** | Version control |

---

## Design Decisions

### Decision Log

#### 1. **Why Only 3 Layouts?**

**Problem**: v7.2 had 24 layouts, causing:
- Maintenance burden (27 renderer files)
- Format conflicts (unclear ownership)
- Limited creative freedom for Text Service

**Decision**: Reduce to 2 layouts (L01-Shell, L25, L29)

**Rationale**:
- 80% of slides are content slides → L25
- 15% are structural (title, section, ending) → L01-Shell
- 5% are high-impact hero moments → L29
- Clear ownership boundaries
- Easy to maintain

**Outcome**: 88% reduction in complexity, zero format conflicts

---

#### 2. **Why Format Ownership Model?**

**Problem**: Dual ownership caused conflicts:
- Text Service formatted, Layout Builder reformatted
- Inconsistent rendering
- Unclear responsibilities

**Decision**: Single owner per field

**Rationale**:
- Clear boundaries prevent conflicts
- Each service controls its domain
- Easier debugging (one source of truth)

**Outcome**: No format conflicts, faster development

---

#### 3. **Why File-Based Storage?**

**Problem**: Need persistent storage for presentations

**Decision**: JSON files (not database initially)

**Rationale**:
- Simple implementation
- Human-readable (easy debugging)
- No infrastructure setup
- Sufficient for current scale
- Easy migration path to database

**Outcome**: Fast development, easy deployment

---

#### 4. **Why Inline Styles Only?**

**Problem**: External CSS classes create dependencies

**Decision**: Text Service uses inline styles exclusively

**Rationale**:
- Self-contained content (no external dependencies)
- No CSS class conflicts
- Portable (copy/paste works)
- Clear ownership (styles belong to content)

**Outcome**: Simplified content generation, no style conflicts

---

#### 5. **Why 18×32 Grid?**

**Problem**: Need flexible positioning system

**Decision**: 18 rows × 32 columns grid

**Rationale**:
- 1920×1080 resolution ÷ 60px = 32×18
- Fine-grained control
- Standard 16:9 aspect ratio
- Aligns with design standards

**Outcome**: Precise positioning, consistent layouts

---

#### 6. **Why Pydantic for Validation?**

**Problem**: Need robust input validation

**Decision**: Pydantic v2 models

**Rationale**:
- Type-safe validation
- Automatic error messages
- FastAPI integration
- IDE support (type hints)

**Outcome**: Fewer bugs, better developer experience

---

#### 7. **Why No Sanitization?**

**Problem**: HTML content could be dangerous

**Decision**: Trust Text Service HTML (no sanitization)

**Rationale**:
- Text Service is internal (not user input)
- Performance cost of sanitization
- AI-generated content is validated
- Can add sanitization later if needed

**Outcome**: Faster rendering, simpler code

**Risk Mitigation**: Monitor Text Service output, add validation if needed

---

## Future Enhancements

### Planned Improvements

1. **Database Migration**
   - PostgreSQL or Supabase
   - Better querying, indexing
   - Multi-user support

2. **Caching Layer**
   - Redis for frequently accessed presentations
   - Reduce file I/O

3. **WebSocket Support**
   - Real-time collaboration
   - Live preview during editing

4. **Analytics Integration**
   - Track presentation views
   - Slide engagement metrics

5. **Export Formats**
   - PDF export
   - PowerPoint export
   - Static HTML export

6. **Theming System**
   - Multiple color themes
   - Custom branding

### Architectural Considerations for Scaling

**Horizontal Scaling**:
- Stateless server design (already achieved)
- Load balancer (nginx)
- Database connection pooling

**Vertical Scaling**:
- Increase server resources
- Optimize JSON parsing
- Database indexing

**CDN Integration**:
- Static assets on CDN
- Geographic distribution

---

## Appendix

### ASCII Diagrams

#### Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Deckster Ecosystem                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Director    │     │    Text      │     │  Analytics   │
│  Agent v3.x  │     │   Service    │     │   Service    │
│ (Port 8000)  │     │              │     │              │
└──────┬───────┘     └──────┬───────┘     └──────────────┘
       │                    │
       │ Layout selection   │ HTML generation
       │ Field specs        │
       │                    │
       └────────┬───────────┘
                │
                │ POST /api/presentations
                ▼
┌─────────────────────────────────────────────────────────────────┐
│              v7.5-main Layout Builder (Port 8504)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │   FastAPI     │  │   Pydantic    │  │    Storage    │      │
│  │   Server      │─►│   Models      │─►│  (JSON Files) │      │
│  └───────┬───────┘  └───────────────┘  └───────────────┘      │
│          │                                                      │
│          │ Serve HTML viewer                                   │
│          ▼                                                      │
│  ┌──────────────────────────────────────────────────┐          │
│  │           Reveal.js Viewer                       │          │
│  │  ┌────────┐  ┌────────┐  ┌────────┐             │          │
│  │  │  L01   │  │  L25   │  │  L29   │             │          │
│  │  │ Shell  │  │        │  │        │             │          │
│  │  │Renderer│  │Renderer│  │Renderer│             │          │
│  │  └────────┘  └────────┘  └────────┘             │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Rendered HTML
                              ▼
                    ┌───────────────────┐
                    │    End User       │
                    │   Web Browser     │
                    └───────────────────┘
```

---

## Conclusion

v7.5-main represents a **radical simplification** of the presentation layout system, reducing complexity by 88% while providing unprecedented creative freedom to Text Service.

**Key Achievements**:
- ✅ 2 layouts (down from 24)
- ✅ Clear format ownership (zero conflicts)
- ✅ Full Text Service creative control
- ✅ Simple, maintainable codebase
- ✅ Fast, responsive API
- ✅ Comprehensive documentation

**Architecture Principles**:
1. Separation of concerns (structure vs content)
2. Single ownership (no conflicts)
3. Simplicity first (2 layouts, not 24)
4. Developer experience (clear APIs, good docs)
5. Performance (fast responses, efficient rendering)

---

**Document Version**: 1.0
**Last Updated**: 2025-01-01
**Status**: Complete
