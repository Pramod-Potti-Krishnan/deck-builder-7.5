# Layout Builder v7.5-main: Comprehensive Codebase Analysis

**Analysis Date**: November 19, 2025  
**Version**: 7.5.0  
**Port**: 8504  
**Status**: Production-Ready

---

## Executive Summary

v7.5-main is a **simplified presentation layout service** that provides structural scaffolding for presentations while maintaining complete creative control ownership boundaries between the Layout Builder and Text Service components. The system supports 6 layouts (L01-L03, L25, L27, L29) built on a 32×18 CSS Grid system, with persistent storage via Supabase and fallback filesystem storage.

**Key Characteristics**:
- Minimal architecture: 2 core layouts (L25, L29) + 4 analytics/diagram layouts (L01-L03, L27)
- Clear format ownership model: Layout Builder manages structure, Text Service owns content areas
- FastAPI-based REST API with version history and content editing capabilities
- Reveal.js-powered presentation viewer with interactive debugging tools
- Hybrid storage: Supabase (primary) + Filesystem (fallback) with optional in-memory caching

---

## Table of Contents

1. [Overall Project Structure](#overall-project-structure)
2. [Main Components](#main-components)
3. [Key Files and Their Roles](#key-files-and-their-roles)
4. [Technology Stack](#technology-stack)
5. [Entry Points and Execution Flow](#entry-points-and-execution-flow)
6. [Data Models and Schemas](#data-models-and-schemas)
7. [API Endpoints and Interfaces](#api-endpoints-and-interfaces)
8. [Configuration and Environment Setup](#configuration-and-environment-setup)
9. [Notable Patterns and Architectural Decisions](#notable-patterns-and-architectural-decisions)
10. [Storage Architecture](#storage-architecture)
11. [Frontend Components](#frontend-components)
12. [Testing Strategy](#testing-strategy)

---

## 1. Overall Project Structure

```
v7.5-main/
├── server.py                    # FastAPI application entry point (port 8504)
├── models.py                    # Pydantic data models (3 core models)
├── config.py                    # Configuration management
├── storage.py                   # Filesystem storage implementation
├── storage_supabase.py          # Supabase storage implementation
├── logger.py                    # Structured JSON logging
│
├── src/                         # Frontend assets
│   ├── renderers/              # 6 layout renderer components
│   │   ├── L01.js              # Centered chart/diagram
│   │   ├── L02.js              # Diagram left, text right
│   │   ├── L03.js              # Two charts side-by-side
│   │   ├── L25.js              # Main content shell
│   │   ├── L27.js              # Image left, content right
│   │   └── L29.js              # Hero full-bleed
│   │
│   ├── styles/                 # CSS for presentation system
│   │   ├── content-area.css    # Content isolation styles
│   │   ├── edit-mode.css       # Edit mode UI styles
│   │   └── core/
│   │       ├── reset.css       # CSS reset
│   │       ├── grid-system.css # 32×18 grid system
│   │       └── borders.css     # Border debug utilities
│   │
│   ├── utils/                  # Client-side utilities
│   │   ├── format_ownership.js # Format owner detection
│   │   └── edit-mode.js        # Edit mode functionality
│   │
│   └── core/
│       └── reveal-config.js    # Reveal.js configuration
│
├── viewer/                     # Presentation viewer
│   └── presentation-viewer.html # Main viewer template
│
├── storage/                    # Local filesystem storage
│   ├── presentations/          # Presentation JSON files
│   └── versions/               # Version history files
│
├── tests/                      # Test suite
│   ├── test_editing_api.py     # API endpoint tests
│   ├── test_l02_html_support.py # Layout tests
│   ├── test_all_6_layouts_fixed.json # Full layout test data
│   ├── test_analytics_apexcharts.json # Analytics integration test
│   ├── test_real_apexcharts.json     # ApexCharts test
│   └── README.md               # Test documentation
│
├── docs/                       # Comprehensive documentation
│   ├── ARCHITECTURE.md         # System architecture
│   ├── LAYOUT_SPECIFICATIONS.md # Layout technical specs
│   ├── CONTENT_GENERATION_GUIDE.md # Content creation patterns
│   ├── CONTENT_EDITING_USER_GUIDE.md # Editing interface guide
│   ├── FRONTEND_INTEGRATION_GUIDE.md # Frontend integration
│   ├── L02_DIRECTOR_INTEGRATION_GUIDE.md # Director agent integration
│   ├── SUPABASE_SETUP.md       # Supabase configuration
│   ├── SUPABASE_MIGRATION_GUIDE.md # Supabase migration
│   └── recent/                 # Recent fix documentation
│
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── README.md                  # Main documentation
├── Procfile                   # Railway deployment config
└── railway.toml               # Railway configuration
```

### Directory Hierarchy

**Python Core** (3 files):
- `server.py`: FastAPI application
- `models.py`: Data validation
- `config.py`: Settings management

**Storage Layer** (3 files):
- `storage.py`: Filesystem backend
- `storage_supabase.py`: Supabase backend
- `logger.py`: Logging infrastructure

**Frontend** (src/ directory):
- 6 layout renderers (JavaScript)
- CSS grid system and styles
- Reveal.js viewer integration
- Format ownership utilities

**Tests**: 6 test files covering all layouts and features

**Documentation**: 10+ markdown files with comprehensive guides

---

## 2. Main Components

### 2.1 Core Components (Backend)

#### **FastAPI Server** (`server.py`)
- REST API for presentation CRUD operations
- Version history and restore functionality
- Presentation viewer rendering
- CORS middleware for cross-origin requests
- Static file mounting for CSS/JS assets
- 472 lines of well-documented code

**Responsibilities**:
- Handle HTTP requests/responses
- Validate incoming presentation data
- Route to appropriate storage backend
- Generate viewer HTML with injected presentation data
- Manage version history operations

#### **Data Models** (`models.py`)
- 3 Pydantic models for structured data validation
- Typed field definitions with constraints
- Support for 6 layouts with flexible content schemas
- Update models for partial modifications
- Version history models

**Core Models**:
1. `Presentation`: Complete presentation (title + slides)
2. `Slide`: Individual slide (layout + content)
3. `L25Content`: Main content shell fields
4. `L29Content`: Hero full-bleed fields
5. `FlexibleContent`: Dynamic content for other layouts
6. `SlideContentUpdate`: Partial update model
7. `VersionMetadata`: Version tracking

#### **Configuration** (`config.py`)
- Environment-based settings using pydantic-settings
- Supabase integration configuration
- Caching parameters
- Feature flags for storage backend selection
- Validation methods for configuration state

**Manages**:
- Server port and CORS origins
- Supabase credentials and bucket
- Cache TTL and max size
- Feature flags (Supabase, local cache)
- Storage directory path

### 2.2 Storage Layer

#### **Filesystem Storage** (`storage.py`)
- Local JSON file-based storage (development/fallback)
- Version history support with structured directories
- Metadata tracking (created_at, created_by, change_summary)
- Async/await pattern for consistency
- Graceful fallback when Supabase unavailable

**Directory Structure**:
- `storage/presentations/`: UUID.json files
- `storage/versions/{uuid}/`: Version history per presentation
- `storage/versions/{uuid}/index.json`: Version metadata index

#### **Supabase Storage** (`storage_supabase.py`)
- Tier 1: PostgreSQL for metadata and primary storage
- Tier 2: Supabase Storage for JSON backup files
- Tier 3: Optional in-memory cache with LRU eviction
- LocalCache class with TTL-based expiration
- 350+ lines implementing complete storage interface

**Features**:
- Local cache with configurable TTL and max size
- LRU eviction when cache reaches capacity
- Transparent fallback to Supabase if cache miss
- Version history stored in PostgreSQL
- Comprehensive error logging

### 2.3 Logging Infrastructure

#### **Structured Logging** (`logger.py`)
- JSON-formatted structured logs
- Separate loggers for storage operations
- Context-aware logging with key-value pairs
- DEBUG, INFO, WARNING, ERROR levels
- Console output for development and deployment monitoring

**Log Format**:
```json
{
  "timestamp": "2025-11-16T10:30:00.000Z",
  "level": "INFO",
  "logger": "storage",
  "message": "Presentation saved",
  "presentation_id": "uuid-here",
  "storage_backend": "supabase"
}
```

### 2.4 Frontend Components

#### **Layout Renderers** (6 JavaScript files)
Each renderer function generates HTML for a specific layout:

**L01.js** - Centered Chart/Diagram
- 1800×600px centered visual
- Title and subtitle
- Descriptive text below
- Footer with presentation name and logo

**L02.js** - Diagram Left, Text Right
- Diagram on left (1260×720px)
- Text on right with rich content
- 2/3 + 1/3 column split
- Subtitle support

**L03.js** - Two Charts Side-by-Side
- Two 840×540px charts
- Comparison layout
- Title and subtitle
- Shared footer

**L25.js** - Main Content Shell
- Title (layout builder manages)
- Subtitle (layout builder manages)
- Rich content area 1800×720px (text service owns)
- Optional footer with presentation name and logo
- Primary layout for 80% of slides

**L27.js** - Image Left, Content Right
- Full-height image on left (720×1080px)
- Content area on right
- Title above content
- Logo positioning

**L29.js** - Hero Full-Bleed
- Complete 1920×1080px slide
- Text service owns entire slide
- No structural elements
- Used for title, section breaks, ending slides
- Maximum creative control

#### **Grid System** (`src/styles/core/grid-system.css`)
- 32-column × 18-row CSS Grid system
- !important overrides for consistency
- Grid overlay visualization (press 'G')
- Border highlighting mode (press 'B')
- Safe zone indicators (columns 2-31, rows 2-17)
- Responsive media queries

#### **Format Ownership Utility** (`src/utils/format_ownership.js`)
- `detectFormatOwner()`: Determine field ownership
- `renderWithOwnership()`: Conditional rendering based on owner
- `isTextServiceOwned()`: Check if field owned by text service
- `isLayoutBuilderOwned()`: Check if field owned by layout builder

**Ownership Rules**:
- **Layout Builder fields**: slide_title, subtitle, header, caption
- **Text Service fields**: rich_content, hero_content, bullets, quote_text
- Respects explicit `format_owner` field in content

#### **Edit Mode** (`src/utils/edit-mode.js`)
- Enable/disable edit mode (press 'E')
- In-place content editing
- Save changes to backend (Ctrl+S)
- Cancel edits (Esc)
- Version history viewing
- Keyboard shortcuts

#### **Reveal.js Integration** (`src/core/reveal-config.js`)
- Reveal.js 4.5.0 initialization
- Navigation configuration
- Transition settings
- Touch/keyboard controls
- Plugin initialization

### 2.5 Presentation Viewer

#### **presentation-viewer.html**
- Main entry point for presentation viewing
- Reveal.js-powered slide navigation
- Dynamic slide rendering from server-injected JSON
- Chart library support (ApexCharts, Chart.js)
- Edit mode UI components
- Debug tools (grid overlay, borders)
- Keyboard shortcuts handler

**Key Features**:
- Presentation data injected as JavaScript constant
- Renderer registry (6 layouts)
- Script execution for inline chart rendering
- Edit mode controls
- Help/documentation system
- Version history modal

---

## 3. Key Files and Their Roles

| File | Type | Purpose | Size | Key Functions |
|------|------|---------|------|----------------|
| `server.py` | Python | FastAPI application | 472 lines | 11 API endpoints |
| `models.py` | Python | Pydantic models | 234 lines | 10 data model classes |
| `config.py` | Python | Configuration | 253 lines | Settings management |
| `storage.py` | Python | Filesystem backend | 350+ lines | File-based storage |
| `storage_supabase.py` | Python | Supabase backend | 350+ lines | Cloud storage with cache |
| `logger.py` | Python | Logging | 150+ lines | Structured JSON logs |
| `L01.js` through `L29.js` | JavaScript | Layout renderers | ~50 lines each | HTML generation |
| `grid-system.css` | CSS | Grid infrastructure | 225 lines | 32×18 grid + overlays |
| `format_ownership.js` | JavaScript | Ownership utility | 138 lines | Format owner detection |
| `presentation-viewer.html` | HTML | Main viewer | 400+ lines | Slide rendering + UI |
| `ARCHITECTURE.md` | Docs | System design | Detailed | High-level architecture |
| `LAYOUT_SPECIFICATIONS.md` | Docs | Layout specs | Detailed | Grid positions, dimensions |

---

## 4. Technology Stack

### Backend
- **Framework**: FastAPI 0.104.0+
- **Server**: Uvicorn (async ASGI)
- **Validation**: Pydantic 2.0.0+ (with pydantic-settings)
- **Database/Storage**: Supabase (PostgreSQL + Storage)
- **Fallback Storage**: Filesystem (JSON)
- **Logging**: Python logging + custom JSON formatter
- **Language**: Python 3.8+

### Frontend
- **Presentation Framework**: Reveal.js 4.5.0
- **Charting Libraries**: 
  - ApexCharts 3.45.0
  - Chart.js 4.4.0
  - ChartDataLabels 2.2.0
- **CSS**: Pure CSS (no framework)
- **JavaScript**: Vanilla JS (no frameworks)
- **Grid System**: CSS Grid (18 rows × 32 columns)

### Infrastructure & Deployment
- **Cloud Hosting**: Railway
- **Runtime**: Python 3.x with Uvicorn
- **Port**: 8504
- **Process Manager**: Procfile (Railway)
- **Environment**: Docker-compatible

### Dependencies Summary
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-multipart>=0.0.6
supabase>=2.8.0
python-dotenv==1.0.0
pydantic-settings==2.1.0
```

**Total Dependencies**: 7 core packages + transitive dependencies

---

## 5. Entry Points and Execution Flow

### 5.1 Server Startup

```
server.py → if __name__ == "__main__"
  ├─ Load PORT from environment (default 8504)
  ├─ Initialize FastAPI app
  ├─ Configure CORS middleware
  ├─ Mount static files (/src)
  ├─ Create storage instance (Supabase + fallback)
  └─ Run uvicorn on 0.0.0.0:8504
```

### 5.2 Presentation Creation Flow

```
POST /api/presentations
  ├─ Request validation (Pydantic model)
  ├─ Layout validation (L01-L29)
  ├─ Storage.save()
  │   ├─ Generate UUID
  │   ├─ Add metadata (created_at)
  │   └─ Save to Supabase (primary) or filesystem (fallback)
  ├─ Generate presentation ID
  └─ Return response {id, url, message}
```

### 5.3 Presentation Viewing Flow

```
GET /p/{presentation_id}
  ├─ Load presentation from storage
  ├─ Read viewer template (presentation-viewer.html)
  ├─ Inject presentation JSON into template
  ├─ Escape JavaScript special characters
  └─ Return HTML with embedded data
```

### 5.4 Frontend Rendering Flow

```
presentation-viewer.html loads
  ├─ Parse PRESENTATION_DATA constant
  ├─ Initialize Reveal.js
  ├─ For each slide:
  │   ├─ Get layout (L01-L29)
  │   ├─ Call appropriate renderer function
  │   ├─ Insert HTML into DOM
  │   └─ Execute inline scripts (charts)
  ├─ Attach keyboard event listeners
  ├─ Load chart libraries (Chart.js, ApexCharts)
  └─ Ready for user interaction
```

### 5.5 Content Editing Flow

```
PUT /api/presentations/{id}/slides/{index}
  ├─ Load current presentation
  ├─ Validate slide index
  ├─ Create version backup
  ├─ Merge update with existing content
  ├─ Save updated presentation
  └─ Return updated slide
```

### 5.6 Keyboard Shortcut Handlers

**In Presentation Viewer**:
- `G`: Toggle grid overlay
- `B`: Toggle border highlights
- `C`: Toggle content area debug mode
- `E`: Toggle edit mode
- `Ctrl+S`: Save changes
- `Esc`: Cancel edits
- `?`: Show help text
- Arrow keys: Navigate slides

---

## 6. Data Models and Schemas

### 6.1 Presentation Model

```python
class Presentation(BaseModel):
    title: str              # Max 200 chars
    slides: List[Slide]     # Min 1 slide

class Slide(BaseModel):
    layout: Literal["L01", "L02", "L03", "L25", "L27", "L29"]
    content: Union[L25Content, L29Content, Dict[str, Any]]
```

### 6.2 L25 Content Model (Main Content Shell)

```python
class L25Content(BaseModel):
    slide_title: str                    # Max 80 chars (required)
    subtitle: Optional[str]             # Max 120 chars
    rich_content: str                   # HTML (required)
    presentation_name: Optional[str]    # Max 100 chars (footer left)
    company_logo: Optional[str]         # HTML/image (footer right)
```

**Grid Positions**:
- Row 2: slide_title
- Row 3: subtitle
- Rows 5-16: rich_content (1800×720px)
- Row 18: footer (presentation_name + company_logo)

### 6.3 L29 Content Model (Hero Full-Bleed)

```python
class L29Content(BaseModel):
    hero_content: str  # HTML (required, full 1920×1080px)
```

**Grid Position**: Rows 1-18, Columns 1-32 (full slide)

### 6.4 Flexible Content Model (L01, L02, L03, L27)

```python
class FlexibleContent(BaseModel):
    class Config:
        extra = "allow"  # Accept any additional fields
    
    # Support for dynamic elements:
    # element_1, element_2, element_3, element_4, element_5
    # slide_title, subtitle
    # presentation_name, company_logo
```

### 6.5 Update Models

```python
class SlideContentUpdate(BaseModel):
    # All fields optional
    slide_title: Optional[str]
    subtitle: Optional[str]
    rich_content: Optional[str]
    hero_content: Optional[str]
    element_1 through element_5: Optional[str]
    presentation_name: Optional[str]
    company_logo: Optional[str]

class PresentationMetadataUpdate(BaseModel):
    title: Optional[str]  # Max 200 chars
```

### 6.6 Version History Models

```python
class VersionMetadata(BaseModel):
    version_id: str
    created_at: str              # ISO timestamp
    created_by: str              # "user", "director_agent", etc.
    change_summary: Optional[str]
    presentation_id: str

class VersionHistoryResponse(BaseModel):
    presentation_id: str
    current_version_id: str
    versions: List[VersionMetadata]
```

### 6.7 Response Models

```python
class PresentationResponse(BaseModel):
    id: str              # Presentation UUID
    url: str             # "/p/{id}"
    message: str         # Success message
```

---

## 7. API Endpoints and Interfaces

### 7.1 Complete API Reference

#### **Presentations**

```
POST /api/presentations
├─ Create new presentation
├─ Request: Presentation model
└─ Response: PresentationResponse {id, url, message}

GET /api/presentations
├─ List all presentations
└─ Response: {count: int, presentations: List}

GET /api/presentations/{id}
├─ Get presentation data
└─ Response: Presentation JSON

PUT /api/presentations/{id}
├─ Update presentation metadata (title)
├─ Query params: created_by, change_summary
├─ Request: PresentationMetadataUpdate
└─ Response: {success, message, presentation}

DELETE /api/presentations/{id}
├─ Delete presentation
└─ Response: {success, message}
```

#### **Slide Content Editing**

```
PUT /api/presentations/{id}/slides/{slide_index}
├─ Update specific slide content
├─ Path: presentation_id (UUID), slide_index (0-based)
├─ Query params: created_by, change_summary
├─ Request: SlideContentUpdate (partial)
└─ Response: {success, message, slide}
```

#### **Version History**

```
GET /api/presentations/{id}/versions
├─ Get version history
└─ Response: VersionHistoryResponse

POST /api/presentations/{id}/restore/{version_id}
├─ Restore presentation to specific version
├─ Query param: create_backup (default: true)
├─ Request: RestoreVersionRequest
└─ Response: {success, message, presentation}
```

#### **Viewer & Utilities**

```
GET /p/{id}
├─ View presentation in browser
└─ Response: HTML with embedded presentation data

GET /tester
├─ API testing interface
└─ Response: HTML tester UI

GET /docs
├─ FastAPI automatic API documentation
└─ Response: Swagger UI

GET /
├─ API root with feature summary
└─ Response: {message, version, endpoints, ...}
```

### 7.2 Request/Response Examples

**Create Presentation**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Q4 Results",
    "slides": [
      {
        "layout": "L29",
        "content": {
          "hero_content": "<div>Title slide HTML</div>"
        }
      }
    ]
  }'
```

**Response**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "/p/550e8400-e29b-41d4-a716-446655440000",
  "message": "Presentation 'Q4 Results' created successfully"
}
```

**Update Slide**:
```bash
curl -X PUT http://localhost:8504/api/presentations/{id}/slides/0 \
  -H "Content-Type: application/json" \
  -d '{
    "rich_content": "<div>New content</div>"
  }' \
  -G --data-urlencode "created_by=director_agent" \
  --data-urlencode "change_summary=Updated content area"
```

---

## 8. Configuration and Environment Setup

### 8.1 Environment Variables

**Server Configuration**:
```env
PORT=8504
ALLOWED_ORIGINS=*
```

**Supabase Configuration**:
```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...
SUPABASE_BUCKET=ls-presentation-data
```

**Feature Flags**:
```env
ENABLE_SUPABASE=true
ENABLE_LOCAL_CACHE=true
CACHE_TTL_SECONDS=3600
MAX_CACHE_SIZE=1000
```

**Storage**:
```env
STORAGE_DIR=storage/presentations
```

### 8.2 Configuration Loading

**Priority Order**:
1. Environment variables (.env file)
2. Pydantic default values
3. Fallback values in code

**Validation**:
```python
settings = get_settings()
if settings.is_supabase_configured():
    # Use Supabase
else:
    # Use filesystem (ephemeral)
```

### 8.3 .env Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Set Supabase credentials:
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-secret-key
```

3. Optional: Customize other settings:
```bash
PORT=8504
ENABLE_SUPABASE=true
CACHE_TTL_SECONDS=3600
```

### 8.4 Railway Deployment

**Procfile**:
```
web: python server.py
```

**Environment Variables on Railway**:
- Railway automatically sets `PORT`
- Set Supabase credentials in Railway dashboard
- Set `ALLOWED_ORIGINS` for production

---

## 9. Notable Patterns and Architectural Decisions

### 9.1 Format Ownership Model

**Philosophy**: Clear responsibility boundaries between services

```
Text Service ─────────────────────► Layout Builder
  Generates HTML for:                Manages structural:
  - rich_content (L25)               - slide_title
  - hero_content (L29)               - subtitle
  - element_2, element_3 (L02)       - Layout grid
  - bullets, content                 - Footer components
  - Full creative control            - Responsive behavior
```

**Implementation**:
- Format owner detection in `format_ownership.js`
- Data models document ownership explicitly
- Renderers respect ownership boundaries
- No conflicts between style systems

### 9.2 Hybrid Storage Architecture

**Three-Tier Storage Strategy**:

```
Tier 1 (Fastest) ─────► In-Memory Local Cache
                         (TTL-based, LRU eviction)
                              │
Tier 2 (Persistent) ──────► Supabase Storage
                         (PostgreSQL + Files)
                              │
Tier 3 (Fallback) ───────► Filesystem JSON
                         (Always available)
```

**Benefits**:
- Fast reads from cache for frequently accessed presentations
- Persistent storage in Supabase for production
- Automatic fallback to filesystem if Supabase unavailable
- Transparent to API consumers

### 9.3 Version History Implementation

**Storage Strategy**:
```
storage/presentations/{uuid}.json     # Current state
storage/versions/{uuid}/index.json    # Version metadata
storage/versions/{uuid}/v_{ts}_{id}.json  # Version snapshots
```

**Version Creation**:
- Automatic backup before each update
- Metadata: timestamp, creator, change summary
- Restore capability with optional backup

### 9.4 Grid System Architecture

**32×18 Grid**:
- Universal coordinate system
- 32 columns × 18 rows for predictable layouts
- !important overrides for consistency
- No margins/padding on slide container

**Visualization Tools**:
- Grid overlay (press 'G')
- Border highlights (press 'B')
- Content area debug (press 'C')
- Safe zone indicators

### 9.5 Renderer Registry Pattern

**Dynamic Layout Loading**:
```javascript
const RENDERERS = {
  'L01': window.renderL01,
  'L02': window.renderL02,
  'L03': window.renderL03,
  'L25': window.renderL25,
  'L27': window.renderL27,
  'L29': window.renderL29
};

const renderer = RENDERERS[layout];
const slideHTML = renderer(content);
```

**Benefits**:
- Extensible: Easy to add new layouts
- Isolated: Each renderer is independent
- Testable: Renderers are pure functions
- Maintainable: Single responsibility per renderer

### 9.6 Async/Await Pattern

**Consistent Asynchronous Operations**:
```python
async def save(presentation_data):
    # File I/O
    # Supabase operations
    # All return awaitable results

async def load(presentation_id):
    # Cache lookup
    # Supabase query
    # Filesystem read
```

**Rationale**:
- Non-blocking I/O operations
- Scalable for multiple concurrent requests
- Consistent interface for all storage backends
- Ready for async frameworks

### 9.7 Pydantic Validation

**Strong Type Safety**:
```python
class Presentation(BaseModel):
    title: str = Field(..., max_length=200)
    slides: list[Slide] = Field(..., min_items=1)
```

**Benefits**:
- Type hints for IDE support
- Automatic validation on instantiation
- Clear field constraints (length, ranges)
- Auto-generated OpenAPI schemas
- Security: Prevents invalid data

### 9.8 CORS Middleware Configuration

**Flexible Origin Control**:
```python
allowed_origins = [origin.strip() 
                  for origin in allowed_origins_env.split(",")]

app.add_middleware(CORSMiddleware, 
                 allow_origins=allowed_origins, ...)
```

**Use Cases**:
- Development: `*` allows all origins
- Production: Specific origins like `https://deckster.xyz`
- Multiple origins: Comma-separated list

### 9.9 Static File Mounting

**Efficient CSS/JS Serving**:
```python
src_dir = Path(__file__).parent / "src"
if src_dir.exists():
    app.mount("/src", StaticFiles(...))
```

**Benefits**:
- Avoids FastAPI overhead for static assets
- Browser caching with query parameters
- Static file server optimization

### 9.10 Error Handling Strategy

**Consistent HTTP Responses**:
```python
try:
    # Operation
except HTTPException:
    raise  # Already formatted
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Error: {str(e)}"
    )
```

**Coverage**:
- 404: Presentation not found
- 400: Invalid input/layout
- 422: Validation error (Pydantic)
- 500: Server error

---

## 10. Storage Architecture

### 10.1 Filesystem Storage

**Directory Structure**:
```
storage/
├── presentations/
│   ├── {uuid-1}.json
│   ├── {uuid-2}.json
│   └── ...
└── versions/
    ├── {uuid-1}/
    │   ├── index.json (metadata)
    │   ├── v_20251116_120000_abc123.json
    │   ├── v_20251116_120500_def456.json
    │   └── ...
    └── {uuid-2}/
        └── ...
```

**File Format** (presentations):
```json
{
  "id": "uuid",
  "title": "Presentation Title",
  "created_at": "2025-11-16T10:30:00",
  "slides": [
    {
      "layout": "L25",
      "content": {...}
    }
  ]
}
```

**Version Index Format**:
```json
{
  "presentation_id": "uuid",
  "versions": [
    {
      "version_id": "v_20251116_120000_abc123",
      "created_at": "2025-11-16T12:00:00",
      "created_by": "user",
      "change_summary": "Updated slide content"
    }
  ]
}
```

### 10.2 Supabase Storage

**Database Schema** (conceptual):
```sql
presentations
├── id (UUID, PK)
├── title (TEXT)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── data (JSONB)

versions
├── id (UUID, PK)
├── presentation_id (UUID, FK)
├── version_id (TEXT)
├── created_at (TIMESTAMP)
├── created_by (TEXT)
├── change_summary (TEXT)
└── data (JSONB)
```

**Storage Bucket**:
```
ls-presentation-data/
├── {uuid-1}.json
├── {uuid-2}.json
└── ...
```

### 10.3 Local Cache (Tier 1)

**Cache Class**:
```python
class LocalCache:
    def __init__(self, max_size=1000, ttl_seconds=3600):
        self.cache: Dict[str, Dict] = {}
        self.timestamps: Dict[str, datetime] = {}
```

**Operations**:
- `get(key)`: Returns cached item if not expired
- `set(key, value)`: Adds to cache with current timestamp
- `invalidate(key)`: Removes from cache
- **LRU Eviction**: Oldest item removed when at capacity

**Benefits**:
- Reduces Supabase queries
- Fast reads for frequently accessed presentations
- TTL-based freshness guarantee
- Configurable size limits

### 10.4 Storage Backend Selection

**Configuration**:
```python
def get_storage_backend():
    if settings.is_supabase_configured():
        return "supabase"
    return "filesystem"
```

**Automatic Fallback**:
1. Try Supabase (if configured)
2. Fall back to filesystem (if Supabase fails)
3. Always available, graceful degradation

---

## 11. Frontend Components

### 11.1 Presentation Viewer Template

**Structure**:
```html
<!DOCTYPE html>
<html>
  <head>
    <!-- Reveal.js CSS -->
    <!-- v7.5 custom CSS -->
    <!-- Chart libraries -->
  </head>
  <body>
    <!-- Help text overlay -->
    <!-- Edit mode controls -->
    <!-- Reveal.js slides container -->
    <!-- Scripts: Reveal.js, Chart.js, ApexCharts -->
    <!-- v7.5 utilities and renderers -->
    <!-- Presentation data injection -->
  </body>
</html>
```

### 11.2 Slide Rendering Pipeline

**Process**:
1. Load `PRESENTATION_DATA` from window constant
2. For each slide:
   - Get layout identifier (L01-L29)
   - Look up renderer function
   - Call renderer with content object
   - Get HTML string
   - Parse into DOM elements
   - Extract and execute scripts
   - Append to slides container
3. Reveal.js initializes with populated slides

### 11.3 Chart Library Integration

**ApexCharts**:
- Loaded from CDN (3.45.0)
- Used for line, bar, pie, area charts
- Works with innerHTML-injected content
- Responsive sizing

**Chart.js**:
- Loaded from CDN (4.4.0)
- Includes ChartDataLabels plugin
- Fixed scatter chart bug vs v3.x
- Canvas-based rendering

**Integration**:
```javascript
// Inline in HTML content
<div id="chart"></div>
<script>
  new ApexCharts(document.getElementById('chart'), {
    // Chart configuration
  }).render();
</script>
```

### 11.4 Edit Mode Implementation

**Features**:
- Toggle via button or 'E' key
- In-place contentEditable on text fields
- Save changes (Ctrl+S)
- Cancel edits (Esc)
- Version history modal

**Backend Integration**:
```javascript
// Save changes
await fetch(`/api/presentations/${id}/slides/${index}`, {
  method: 'PUT',
  body: JSON.stringify(updates)
});

// Restore version
await fetch(`/api/presentations/${id}/restore/${version_id}`, {
  method: 'POST'
});
```

### 11.5 Keyboard Shortcuts

**Navigation**:
- Arrow Left/Right: Navigate slides
- Esc: Overview mode

**Debugging**:
- `G`: Grid overlay toggle
- `B`: Border highlights toggle
- `C`: Content area debug mode
- `?`: Show help

**Editing**:
- `E`: Toggle edit mode
- `Ctrl+S`: Save changes
- `Esc`: Cancel edits

---

## 12. Testing Strategy

### 12.1 Test Files Overview

| File | Type | Focus |
|------|------|-------|
| `test_editing_api.py` | Python/pytest | API endpoints, version history |
| `test_l02_html_support.py` | Python/pytest | Layout rendering, HTML support |
| `test_all_6_layouts_fixed.json` | JSON data | All 6 layouts |
| `test_analytics_apexcharts.json` | JSON data | Analytics integration |
| `test_real_apexcharts.json` | JSON data | Chart.js rendering |

### 12.2 Test Coverage Areas

**API Endpoints**:
- ✅ Create presentation
- ✅ Get presentation
- ✅ Update metadata
- ✅ Update slide content
- ✅ List presentations
- ✅ Delete presentation
- ✅ Version history
- ✅ Restore version
- ✅ View presentation

**Layouts**:
- ✅ L01: Centered chart
- ✅ L02: Diagram left + text right
- ✅ L03: Two charts side-by-side
- ✅ L25: Main content shell
- ✅ L27: Image left + content right
- ✅ L29: Hero full-bleed

**Features**:
- ✅ Content editing
- ✅ Version history
- ✅ Chart rendering
- ✅ HTML support
- ✅ Analytics integration
- ✅ Footer components

### 12.3 Running Tests

**Python Tests**:
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_editing_api.py

# Verbose output
pytest tests/ -v
```

**JSON Tests** (via API):
```bash
# Start server
python server.py

# In another terminal:
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_all_6_layouts_fixed.json
```

### 12.4 Test Data Examples

**Minimal Presentation** (test_presentation.json):
```json
{
  "title": "Test Presentation",
  "slides": [{
    "layout": "L25",
    "content": {
      "slide_title": "Hello",
      "rich_content": "<p>World</p>"
    }
  }]
}
```

**Comprehensive Test** (test_all_6_layouts_fixed.json):
- Tests all 6 layouts
- Various content types
- Footer elements
- Validates complete system

---

## Summary: Key Takeaways

### Strengths
1. **Clear Architecture**: Format ownership model prevents conflicts
2. **Simplified System**: 6 layouts vs 24 in v7.2
3. **Persistent Storage**: Supabase + filesystem fallback
4. **Version History**: Complete undo/restore capability
5. **Developer Experience**: Comprehensive documentation
6. **Extensible Design**: Easy to add new layouts
7. **Production Ready**: Deployment on Railway with environment configuration

### Core Responsibilities
- **Layout Builder**: Structure (grid, titles, footers)
- **Text Service**: Content (rich HTML areas)
- **Director Agent**: Orchestration (layout selection)

### Technical Excellence
- Pydantic for type safety
- FastAPI for API design
- Reveal.js for presentation display
- CSS Grid for reliable positioning
- Structured JSON logging for debugging
- Async/await for scalability

### Deployment Readiness
- Environment-based configuration
- Graceful fallback strategies
- CORS middleware for cross-origin requests
- Static file optimization
- Structured error handling
- Comprehensive logging

---

**End of Analysis**
