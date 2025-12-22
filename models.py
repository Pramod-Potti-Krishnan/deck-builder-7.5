"""
Pydantic models for v7.5-main: 6-Layout Architecture

Layouts:
- L01: Centered Chart with Text Below
- L02: Left Diagram with Text on Right
- L03: Two Charts in Columns with Text Below
- L25: Main Content Shell (rich content area)
- L27: Image Left with Content Right
- L29: Full-Bleed Slides (hero/section slides)
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, Literal, Dict, Any, List
from uuid import uuid4
import re


# ==================== Valid Layout Types ====================
# All supported layouts: Backend (L01-L29) + Frontend Templates (H1-H3, C1-C5, V1-V4, I1-I4, S3-S4, B1)
# Plus dynamic X-series layouts (X1-X5 with hash suffix)

ValidLayoutType = Literal[
    # Backend layouts
    "L01", "L02", "L03", "L25", "L27", "L29",
    # Frontend templates - Hero
    "H1-generated", "H1-structured", "H2-section", "H3-closing",
    # Frontend templates - Content
    "C1-text", "C3-chart", "C4-infographic", "C5-diagram",
    # Frontend templates - Visual + Text (V series)
    "V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text",
    # Frontend templates - Image Split (I series)
    "I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow",
    # Frontend templates - Split
    "S3-two-visuals", "S4-comparison",
    # Frontend templates - Blank
    "B1-blank"
]

# Set of all predefined layout IDs for validation
PREDEFINED_LAYOUTS = {
    "L01", "L02", "L03", "L25", "L27", "L29",
    "H1-generated", "H1-structured", "H2-section", "H3-closing",
    "C1-text", "C3-chart", "C4-infographic", "C5-diagram",
    "V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text",
    "I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow",
    "S3-two-visuals", "S4-comparison",
    "B1-blank"
}

# X-Series pattern: X{1-5}-{8 hex characters}
X_SERIES_PATTERN = re.compile(r'^X[1-5]-[a-f0-9]{8}$')


def validate_layout_id(layout_id: str) -> str:
    """
    Validate a layout ID - accepts predefined layouts and X-series dynamic layouts.

    Valid formats:
    - Predefined: L01, C1-text, H1-structured, etc.
    - X-Series: X1-a3f7e8c2, X2-b4c9d1e3, etc.
    """
    if layout_id in PREDEFINED_LAYOUTS:
        return layout_id
    if X_SERIES_PATTERN.match(layout_id):
        return layout_id
    raise ValueError(
        f"Invalid layout ID: {layout_id}. Must be a predefined layout or X-series format (X[1-5]-[hash8])"
    )


# ==================== L25: Main Content Shell ====================

class L25Content(BaseModel):
    """
    L25: Main content shell with large content area for Text Service.

    Structure:
    - Title: Row 2 (layout_builder formats)
    - Subtitle: Row 3 (layout_builder formats)
    - Rich Content: Rows 5-16 (text_service owns - full creative control)
    - Footer: Row 18 (optional presentation name and company logo)

    Content Area Dimensions:
    - Grid: 12 rows × 30 columns (rows 5-16, cols 2-31)
    - Pixels: 1800px wide × 720px tall (at 1920×1080 resolution)

    Format Ownership:
    - slide_title, subtitle: layout_builder (plain text)
    - rich_content: text_service (HTML with full styling control)
    - presentation_name, company_logo: optional footer fields
    """
    slide_title: str = Field(
        ...,
        max_length=80,
        description="Slide title (layout_builder formats)"
    )
    subtitle: Optional[str] = Field(
        None,
        max_length=120,
        description="Subtitle (layout_builder formats)"
    )
    rich_content: str = Field(
        ...,
        description="Rich HTML content from Text Service (1800px × 720px content area)"
    )
    presentation_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Presentation name for footer left section (optional)"
    )
    company_logo: Optional[str] = Field(
        None,
        description="Company logo URL or HTML for footer right section (optional, legacy field)"
    )
    logo: Optional[str] = Field(
        None,
        description="Logo content: URL, emoji, or HTML (preferred over company_logo)"
    )


# ==================== L29: Hero Full-Bleed ====================

class L29Content(BaseModel):
    """
    L29: Hero full-bleed layout for maximum creative impact.

    Structure:
    - Hero Content: Full slide (rows 1-18, cols 1-32)
    - No title, no subtitle, no footer
    - Text Service has complete control over entire slide

    Content Area Dimensions:
    - Grid: 18 rows × 32 columns (entire slide)
    - Pixels: 1920px wide × 1080px tall (full HD resolution)

    Format Ownership:
    - hero_content: text_service (complete HTML with full styling)

    Use Cases:
    - Opening hero images with overlaid text
    - Full-screen calls to action
    - Immersive brand experiences
    - Video backgrounds with text overlays
    """
    hero_content: str = Field(
        ...,
        description="Full-bleed HTML content from Text Service (1920px × 1080px)"
    )


# ==================== Flexible Content Model ====================

class FlexibleContent(BaseModel):
    """
    Flexible content model for L01, L02, L03, L27 layouts.
    Accepts any dictionary of string keys to string values.
    """
    class Config:
        extra = "allow"  # Allow additional fields

    def model_dump(self, **kwargs):
        """Override to return all fields including extra ones."""
        return {**self.__dict__, **self.__pydantic_extra__}


# ==================== Text Box Models ====================

class TextBoxPosition(BaseModel):
    """
    Position and dimensions for a text box using CSS Grid coordinates.

    The presentation uses a 32×18 grid system on 1920×1080 resolution.
    Grid values are in 'start/end' format (1-indexed).
    """
    grid_row: str = Field(
        ...,
        description="CSS grid-row value (e.g., '5/10' for rows 5-9)",
        examples=["5/10", "8/12", "3/6"]
    )
    grid_column: str = Field(
        ...,
        description="CSS grid-column value (e.g., '3/15' for columns 3-14)",
        examples=["3/15", "10/25", "2/32"]
    )

    @field_validator('grid_row', 'grid_column')
    @classmethod
    def validate_grid_value(cls, v: str) -> str:
        """Validate grid values are in 'start/end' format."""
        if '/' not in v:
            raise ValueError("Grid value must be in 'start/end' format")
        parts = v.split('/')
        if len(parts) != 2:
            raise ValueError("Grid value must have exactly two parts")
        try:
            start, end = int(parts[0]), int(parts[1])
        except ValueError:
            raise ValueError("Grid values must be integers")
        if start >= end:
            raise ValueError("Start must be less than end")
        if start < 1:
            raise ValueError("Start must be at least 1")
        return v


class TextBoxStyle(BaseModel):
    """
    Visual styling options for a text box.

    Default: Transparent overlay (no background, no border).

    Supports both individual properties AND shorthand values:
    - padding: Can be int (pixels) OR string shorthand like "25px 0px"
    - border: Can use border_color/border_width OR border shorthand like "1px solid #ddd"
    - vertical_align: Maps to flexbox justify-content ('top', 'middle', 'bottom')
    """
    background_color: Optional[str] = Field(
        default="transparent",
        description="Background color (hex, rgba, or 'transparent')",
        examples=["#ffffff", "rgba(255,255,255,0.8)", "transparent"]
    )
    border_color: Optional[str] = Field(
        default="transparent",
        description="Border color in hex format"
    )
    border_width: int = Field(
        default=0, ge=0, le=20,
        description="Border width in pixels"
    )
    border: Optional[str] = Field(
        default=None,
        description="Border shorthand (e.g., '1px solid #ddd'). Overrides border_width/border_color if set.",
        examples=["1px solid #ddd", "2px dashed #333", "none"]
    )
    border_radius: int = Field(
        default=0, ge=0, le=50,
        description="Border radius in pixels"
    )
    padding: Optional[Union[int, str]] = Field(
        default=16,
        description="Padding - either int (pixels) or shorthand string (e.g., '25px 0px', '10px 20px 10px 20px')",
        examples=[16, "25px 0px", "10px 20px 10px 20px"]
    )
    vertical_align: Optional[str] = Field(
        default=None,
        description="Vertical alignment of content ('top', 'middle', 'bottom'). Maps to flexbox justify-content.",
        examples=["top", "middle", "bottom"]
    )
    opacity: float = Field(
        default=1.0, ge=0.0, le=1.0,
        description="Opacity value (0.0 to 1.0)"
    )
    box_shadow: Optional[str] = Field(
        default=None,
        description="CSS box-shadow value"
    )


class TextContentStyle(BaseModel):
    """
    Text formatting styles for text box content.

    These styles are applied to the text content inside the text box,
    separate from the container styles (background, border, etc.).
    Set via postMessage commands from the frontend formatting panel.
    """
    color: Optional[str] = Field(
        default=None,
        description="Text color (hex or CSS color value)"
    )
    font_family: Optional[str] = Field(
        default=None,
        description="Font family (e.g., 'Inter, sans-serif')"
    )
    font_size: Optional[str] = Field(
        default=None,
        description="Font size with unit (e.g., '32px', '1.5rem')"
    )
    font_weight: Optional[str] = Field(
        default=None,
        description="Font weight (e.g., 'normal', 'bold', '600')"
    )
    font_style: Optional[str] = Field(
        default=None,
        description="Font style (e.g., 'normal', 'italic')"
    )
    text_align: Optional[str] = Field(
        default=None,
        description="Text alignment (left, center, right, justify)"
    )
    line_height: Optional[str] = Field(
        default=None,
        description="Line height (e.g., '1.5', '24px')"
    )
    letter_spacing: Optional[str] = Field(
        default=None,
        description="Letter spacing (e.g., '0.5px', '0.1em')"
    )
    text_decoration: Optional[str] = Field(
        default=None,
        description="Text decoration (e.g., 'none', 'underline')"
    )
    text_transform: Optional[str] = Field(
        default=None,
        description="Text case transformation (e.g., 'uppercase', 'lowercase', 'capitalize', 'none')",
        examples=["uppercase", "lowercase", "capitalize", "none"]
    )


class TextBox(BaseModel):
    """
    A text box element that can be placed on any slide.

    Text boxes are overlay elements that float above the main layout content.
    They support rich HTML content with inline styling for multi-style text.
    Text boxes have elevated z-index (1000+) to appear above other elements.

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: textbox_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"textbox_{uuid4().hex[:8]}",
        description="Unique identifier for the text box (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=1000, ge=1, le=10000,
        description="Layer order (higher = on top). Text boxes start at 1000."
    )
    content: str = Field(
        default="",
        description="Rich HTML content with inline styles"
    )
    style: TextBoxStyle = Field(
        default_factory=TextBoxStyle,
        description="Visual styling options (container: background, border, etc.)"
    )
    text_style: Optional[TextContentStyle] = Field(
        default=None,
        description="Text formatting styles (content: color, font, alignment, etc.)"
    )
    css_classes: Optional[List[str]] = Field(
        default=None,
        description="Custom CSS class names for additional styling (e.g., ['slot-content', 'slot-type-bod'])",
        examples=[["slot-content", "slot-type-bod"], ["highlight-box"]]
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental edits when True"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        """Sanitize content to prevent XSS attacks."""
        # Prevent script injection
        if re.search(r'<script', v, re.IGNORECASE):
            raise ValueError("Script tags are not allowed in text box content")
        # Prevent event handler injection
        if re.search(r'\bon\w+\s*=', v, re.IGNORECASE):
            raise ValueError("Event handlers are not allowed in text box content")
        # Size limit (100KB)
        if len(v.encode('utf-8')) > 100 * 1024:
            raise ValueError("Content exceeds maximum size of 100KB")
        return v


# ==================== Image Element Models ====================

class ImageElement(BaseModel):
    """
    An image element that can be placed on any slide.

    Supports two modes:
    1. Placeholder mode (no image_url) - Shows "Drag images here" UI
    2. Content mode (image_url provided) - Shows actual image

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: image_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"image_{uuid4().hex[:8]}",
        description="Unique identifier for the image element (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=100, ge=1, le=10000,
        description="Layer order (higher = on top)"
    )
    image_url: Optional[str] = Field(
        default=None,
        description="Image URL (null for placeholder mode)"
    )
    alt_text: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Alt text for accessibility"
    )
    object_fit: str = Field(
        default="cover",
        description="CSS object-fit: cover, contain, fill, none, scale-down"
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental edits when True"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )


# ==================== Chart Element Models ====================

class ChartElement(BaseModel):
    """
    A chart element that can be placed on any slide.

    Supports two modes:
    1. Placeholder mode (no chart_html/chart_config) - Shows chart placeholder UI
    2. Content mode (chart_html or chart_config provided) - Shows actual chart

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: chart_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"chart_{uuid4().hex[:8]}",
        description="Unique identifier for the chart element (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=100, ge=1, le=10000,
        description="Layer order (higher = on top)"
    )
    chart_type: Optional[str] = Field(
        default=None,
        description="Chart type: bar, line, pie, doughnut, radar, scatter, bubble, etc."
    )
    chart_config: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Chart.js configuration object"
    )
    chart_html: Optional[str] = Field(
        default=None,
        description="Pre-rendered HTML content from Analytics Service"
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental edits when True"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )


# ==================== Infographic Element Models ====================

class InfographicElement(BaseModel):
    """
    An infographic element that can be placed on any slide.

    Supports two modes:
    1. Placeholder mode (no svg_content) - Shows infographic placeholder UI
    2. Content mode (svg_content provided) - Shows actual infographic

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: infographic_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"infographic_{uuid4().hex[:8]}",
        description="Unique identifier for the infographic element (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=100, ge=1, le=10000,
        description="Layer order (higher = on top)"
    )
    infographic_type: Optional[str] = Field(
        default=None,
        description="Infographic type: timeline, process, comparison, hierarchy, statistics, etc."
    )
    svg_content: Optional[str] = Field(
        default=None,
        description="SVG content from Illustrator Service"
    )
    html_content: Optional[str] = Field(
        default=None,
        description="Pre-rendered HTML content (alternative to svg_content)"
    )
    items: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Data items for the infographic"
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental edits when True"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )


# ==================== Diagram Element Models ====================

class DiagramElement(BaseModel):
    """
    A diagram element that can be placed on any slide.

    Supports two modes:
    1. Placeholder mode (no svg_content/mermaid_code) - Shows diagram placeholder UI
    2. Content mode (svg_content or mermaid_code provided) - Shows actual diagram

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: diagram_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"diagram_{uuid4().hex[:8]}",
        description="Unique identifier for the diagram element (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=100, ge=1, le=10000,
        description="Layer order (higher = on top)"
    )
    diagram_type: Optional[str] = Field(
        default=None,
        description="Diagram type: flowchart, sequence, class, state, entity, gantt, pie, mindmap, etc."
    )
    mermaid_code: Optional[str] = Field(
        default=None,
        description="Mermaid.js diagram code"
    )
    svg_content: Optional[str] = Field(
        default=None,
        description="Pre-rendered SVG content"
    )
    html_content: Optional[str] = Field(
        default=None,
        description="Pre-rendered HTML content (alternative to svg_content/mermaid_code)"
    )
    direction: str = Field(
        default="TB",
        description="Layout direction: TB (top-bottom), LR (left-right), BT, RL"
    )
    theme: str = Field(
        default="default",
        description="Diagram theme: default, dark, forest, neutral"
    )
    locked: bool = Field(
        default=False,
        description="Prevent accidental edits when True"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )


# ==================== Content Element Models ====================

class ContentElement(BaseModel):
    """
    A content element for L-series layouts (L25, L29, L01, L02, L03).

    Content elements represent the main content area owned by Text Service.
    They are read-only in the layout builder (cannot be dragged/edited).
    Used for: rich_content, hero_content, charts, diagrams from L-series.

    UUID Architecture (v7.5.1):
    - id: Stable UUID-based identifier (format: content_{uuid8})
    - parent_slide_id: Foreign key to parent slide's slide_id (for cascade delete)
    """
    id: str = Field(
        default_factory=lambda: f"content_{uuid4().hex[:8]}",
        description="Unique identifier for the content element (UUID-based)"
    )
    parent_slide_id: Optional[str] = Field(
        default=None,
        description="Parent slide's slide_id (foreign key for cascade delete). Null for legacy elements."
    )
    slot_name: str = Field(
        ...,
        description="Slot name from template registry (e.g., 'content', 'hero', 'chart', 'diagram')"
    )
    position: TextBoxPosition = Field(
        ...,
        description="Grid position and dimensions"
    )
    z_index: int = Field(
        default=100, ge=1, le=10000,
        description="Layer order (higher = on top)"
    )
    content_html: str = Field(
        default="",
        description="HTML content from Text Service or other content provider"
    )
    content_type: str = Field(
        default="html",
        description="Content type: html, chart, diagram, infographic"
    )
    format_owner: str = Field(
        default="text_service",
        description="Service that owns formatting: text_service, analytics_service, illustrator_service"
    )
    editable: bool = Field(
        default=False,
        description="Whether content can be edited in layout builder (usually False for Text Service content)"
    )
    locked: bool = Field(
        default=True,
        description="Prevent accidental edits when True (default True for content elements)"
    )
    visible: bool = Field(
        default=True,
        description="Show/hide without deleting"
    )


# ==================== Slide Model ====================

class Slide(BaseModel):
    """
    Individual slide with layout, content, and overlay elements.

    UUID Architecture (v7.5.1):
    - slide_id: Stable UUID for this slide (format: slide_{uuid12})
    - All child elements reference parent_slide_id for cascade delete

    Element types:
    - text_boxes: Overlay text elements with rich HTML content
    - images: Image elements (placeholder or actual images)
    - charts: Chart elements (placeholder or actual Chart.js charts)
    - infographics: Infographic elements (placeholder or SVG content)
    - diagrams: Diagram elements (placeholder, Mermaid, or SVG content)
    - contents: Content elements for L-series main content areas

    All element types are persisted and restored on load.
    """
    slide_id: str = Field(
        default_factory=lambda: f"slide_{uuid4().hex[:12]}",
        description="Stable UUID for this slide (not index-based). Used by child elements for cascade delete."
    )
    layout: str = Field(
        ...,
        description="Layout identifier: predefined (L01-L29, H1-H3, C1-C5, etc.) or X-series dynamic (X1-a3f7e8c2)"
    )

    @field_validator('layout')
    @classmethod
    def validate_layout_field(cls, v: str) -> str:
        """Validate layout ID - accepts predefined layouts and X-series dynamic layouts."""
        return validate_layout_id(v)

    content: Union[L25Content, L29Content, Dict[str, Any]] = Field(
        ...,
        description="Layout-specific content (structured for L25/L29, flexible dict for others)"
    )
    background_color: Optional[str] = Field(
        None,
        description="Slide background color in hex format (e.g., #FF5733, #1a1a1a)"
    )
    background_image: Optional[str] = Field(
        None,
        description="Slide background image URL or data URI (base64). Uses background-size: cover."
    )
    text_boxes: List[TextBox] = Field(
        default_factory=list,
        description="List of text box overlays on this slide (max 20)"
    )
    images: List[ImageElement] = Field(
        default_factory=list,
        description="List of image elements on this slide (max 20)"
    )
    charts: List[ChartElement] = Field(
        default_factory=list,
        description="List of chart elements on this slide (max 10)"
    )
    infographics: List[InfographicElement] = Field(
        default_factory=list,
        description="List of infographic elements on this slide (max 10)"
    )
    diagrams: List[DiagramElement] = Field(
        default_factory=list,
        description="List of diagram elements on this slide (max 10)"
    )
    contents: List[ContentElement] = Field(
        default_factory=list,
        description="List of content elements on this slide (L-series main content areas, max 5)"
    )

    @field_validator('text_boxes')
    @classmethod
    def validate_text_boxes_limit(cls, v: List[TextBox]) -> List[TextBox]:
        """Limit text boxes per slide."""
        if len(v) > 20:
            raise ValueError("Maximum 20 text boxes per slide")
        return v

    @field_validator('images')
    @classmethod
    def validate_images_limit(cls, v: List[ImageElement]) -> List[ImageElement]:
        """Limit images per slide."""
        if len(v) > 20:
            raise ValueError("Maximum 20 images per slide")
        return v

    @field_validator('charts')
    @classmethod
    def validate_charts_limit(cls, v: List[ChartElement]) -> List[ChartElement]:
        """Limit charts per slide."""
        if len(v) > 10:
            raise ValueError("Maximum 10 charts per slide")
        return v

    @field_validator('infographics')
    @classmethod
    def validate_infographics_limit(cls, v: List[InfographicElement]) -> List[InfographicElement]:
        """Limit infographics per slide."""
        if len(v) > 10:
            raise ValueError("Maximum 10 infographics per slide")
        return v

    @field_validator('diagrams')
    @classmethod
    def validate_diagrams_limit(cls, v: List[DiagramElement]) -> List[DiagramElement]:
        """Limit diagrams per slide."""
        if len(v) > 10:
            raise ValueError("Maximum 10 diagrams per slide")
        return v

    @field_validator('contents')
    @classmethod
    def validate_contents_limit(cls, v: List[ContentElement]) -> List[ContentElement]:
        """Limit content elements per slide."""
        if len(v) > 5:
            raise ValueError("Maximum 5 content elements per slide")
        return v


# ==================== Derivative Elements Models ====================

class FooterConfig(BaseModel):
    """
    Configuration for presentation-level footer.

    Footer content is defined ONCE at the presentation level and automatically
    rendered on ALL slides. Supports template variables that are substituted
    at render time.

    Template Variables:
    - {title}: Presentation title or custom title value
    - {page}: Current slide number (auto-populated, 1-indexed)
    - {total}: Total number of slides (auto-populated)
    - {date}: Date value (user-defined)
    - {author}: Author name (user-defined)

    Example template: "{title} | Page {page} of {total} | {date}"
    Example output: "Q4 Business Review | Page 3 of 12 | December 2024"
    """
    template: str = Field(
        default="{title} | Page {page}",
        max_length=200,
        description="Footer template with variables like {title}, {page}, {total}, {date}, {author}"
    )
    values: Dict[str, str] = Field(
        default_factory=dict,
        description="Variable values: {'title': 'My Presentation', 'date': 'Dec 2024', 'author': 'John'}"
    )
    style: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional style overrides for footer text (fontSize, color, fontFamily, etc.)"
    )


class LogoConfig(BaseModel):
    """
    Configuration for presentation-level logo.

    Logo is defined ONCE at the presentation level and automatically
    rendered on ALL slides. The position is determined by each template's
    logo slot definition.

    The logo image is shared across all slides, but its grid position
    may vary based on the template (e.g., bottom-right corner for most
    templates, but different position for hero slides).
    """
    image_url: Optional[str] = Field(
        default=None,
        description="Logo image URL. If None, logo slot shows placeholder or is hidden."
    )
    alt_text: str = Field(
        default="Logo",
        max_length=100,
        description="Alt text for accessibility"
    )


class DerivativeElements(BaseModel):
    """
    Presentation-level elements that are rendered consistently across all slides.

    "Derivative elements" are elements whose content/image derives from a single
    source at the presentation level, not from individual slide data.

    - Footer: Same text template (with auto page numbers) across all slides
    - Logo: Same image across all slides (position varies by template)

    When a user edits footer/logo on ANY slide, it updates the presentation-level
    config and instantly syncs to all other slides.
    """
    footer: Optional[FooterConfig] = Field(
        default=None,
        description="Presentation-level footer configuration. If set, overrides per-slide footer content."
    )
    logo: Optional[LogoConfig] = Field(
        default=None,
        description="Presentation-level logo configuration. If set, overrides per-slide logo content."
    )


# ==================== Theme Models ====================

class ThemeColors(BaseModel):
    """
    Color palette for a presentation theme.

    Defines colors for both standard (light) and hero (dark) slide profiles.
    All colors are optional with sensible defaults for a professional blue theme.
    """
    # Primary brand colors
    primary: str = Field(
        default="#1e40af",
        description="Main brand color"
    )
    primary_light: Optional[str] = Field(
        default="#3b82f6",
        description="Lighter variant of primary"
    )
    primary_dark: Optional[str] = Field(
        default="#1e3a8a",
        description="Darker variant of primary"
    )
    accent: Optional[str] = Field(
        default="#f59e0b",
        description="Accent/highlight color"
    )

    # Background colors
    background: str = Field(
        default="#ffffff",
        description="Main background color"
    )
    background_alt: Optional[str] = Field(
        default="#f8fafc",
        description="Alternate/subtle background"
    )

    # Text colors - Standard profile (dark text on light background)
    text_primary: str = Field(
        default="#1f2937",
        description="Primary text color (titles, headings)"
    )
    text_secondary: str = Field(
        default="#6b7280",
        description="Secondary text color (subtitles, captions)"
    )
    text_body: str = Field(
        default="#374151",
        description="Body text color"
    )

    # Text colors - Hero profile (light text on dark background)
    hero_text_primary: str = Field(
        default="#ffffff",
        description="Hero slide primary text (white)"
    )
    hero_text_secondary: str = Field(
        default="#e5e7eb",
        description="Hero slide secondary text"
    )
    hero_background: str = Field(
        default="#1e3a5f",
        description="Hero slide background color"
    )

    # Footer color
    footer_text: Optional[str] = Field(
        default="#6b7280",
        description="Footer text color"
    )

    # Border color
    border: Optional[str] = Field(
        default="#e5e7eb",
        description="Border/divider color"
    )

    # Tertiary colors (for groupings, borders, dividers)
    tertiary_1: Optional[str] = Field(
        default="#f3f4f6",
        description="Lightest tertiary color"
    )
    tertiary_2: Optional[str] = Field(
        default="#d1d5db",
        description="Medium tertiary color"
    )
    tertiary_3: Optional[str] = Field(
        default="#9ca3af",
        description="Darkest tertiary color"
    )

    # Chart colors (for data visualization)
    chart_1: Optional[str] = Field(
        default="#3b82f6",
        description="Primary chart color"
    )
    chart_2: Optional[str] = Field(
        default="#10b981",
        description="Secondary chart color"
    )
    chart_3: Optional[str] = Field(
        default="#f59e0b",
        description="Third chart color"
    )
    chart_4: Optional[str] = Field(
        default="#ef4444",
        description="Fourth chart color"
    )
    chart_5: Optional[str] = Field(
        default="#8b5cf6",
        description="Fifth chart color"
    )
    chart_6: Optional[str] = Field(
        default="#ec4899",
        description="Sixth chart color"
    )


class ThemeTypographySlot(BaseModel):
    """Typography settings for a specific slot type."""
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    line_height: Optional[str] = None
    text_shadow: Optional[str] = None


class ThemeTypography(BaseModel):
    """Typography settings for standard and hero profiles."""
    font_family: str = Field(
        default="Poppins, sans-serif",
        description="Primary font family"
    )
    font_family_heading: Optional[str] = Field(
        default=None,
        description="Font family for headings (falls back to font_family if not set)"
    )
    standard: Optional[Dict[str, ThemeTypographySlot]] = Field(
        default=None,
        description="Typography for standard slides: {title, subtitle, body, footer}"
    )
    hero: Optional[Dict[str, ThemeTypographySlot]] = Field(
        default=None,
        description="Typography for hero slides: {title, subtitle, footer}"
    )


class ThemeSpacing(BaseModel):
    """
    Spacing configuration for a theme.

    Controls padding and gaps between elements.
    """
    slide_padding: str = Field(
        default="60px",
        description="Padding around slide content"
    )
    element_gap: str = Field(
        default="24px",
        description="Gap between elements"
    )
    section_gap: str = Field(
        default="48px",
        description="Gap between major sections"
    )


class ThemeEffects(BaseModel):
    """
    Visual effects configuration for a theme.

    Controls shadows, border radius, and other visual effects.
    """
    border_radius: str = Field(
        default="8px",
        description="Default border radius for elements"
    )
    shadow_small: str = Field(
        default="0 1px 3px rgba(0,0,0,0.1)",
        description="Small shadow for subtle depth"
    )
    shadow_medium: str = Field(
        default="0 4px 6px rgba(0,0,0,0.1)",
        description="Medium shadow for cards and panels"
    )
    shadow_large: str = Field(
        default="0 10px 15px rgba(0,0,0,0.1)",
        description="Large shadow for modals and dropdowns"
    )


class ThemeContentStyles(BaseModel):
    """
    Content styles for rich HTML elements.

    Defines styling for headings, paragraphs, lists, etc.
    """
    h1: Optional[Dict[str, str]] = Field(
        default=None,
        description="H1 heading styles: {fontSize, fontWeight, color, marginBottom}"
    )
    h2: Optional[Dict[str, str]] = Field(
        default=None,
        description="H2 heading styles"
    )
    h3: Optional[Dict[str, str]] = Field(
        default=None,
        description="H3 heading styles"
    )
    p: Optional[Dict[str, str]] = Field(
        default=None,
        description="Paragraph styles"
    )
    ul: Optional[Dict[str, str]] = Field(
        default=None,
        description="Unordered list styles"
    )
    li: Optional[Dict[str, str]] = Field(
        default=None,
        description="List item styles"
    )
    blockquote: Optional[Dict[str, str]] = Field(
        default=None,
        description="Blockquote styles"
    )


# ==================== Typography Response Models (Text Service) ====================

class TypographyToken(BaseModel):
    """
    Typography token for a text element type.

    Used by Text Service to calculate character constraints
    and apply consistent styling.
    """
    size: int = Field(
        ...,
        description="Font size in pixels (numeric)"
    )
    size_px: str = Field(
        ...,
        description="Font size as CSS value (e.g., '72px')"
    )
    weight: int = Field(
        default=400,
        description="Font weight (100-900)"
    )
    line_height: float = Field(
        default=1.4,
        description="Line height multiplier"
    )
    letter_spacing: str = Field(
        default="0",
        description="Letter spacing (e.g., '-0.02em', '0')"
    )
    color: str = Field(
        ...,
        description="Text color as hex"
    )
    text_transform: str = Field(
        default="none",
        description="Text transform: none, uppercase, lowercase, capitalize"
    )


class EmphasisToken(BaseModel):
    """Typography token for emphasized text (bold, strong)."""
    weight: int = Field(
        default=600,
        description="Font weight for emphasis"
    )
    color: str = Field(
        ...,
        description="Emphasis text color as hex"
    )
    style: str = Field(
        default="normal",
        description="Font style: normal, italic"
    )


class ListStylesToken(BaseModel):
    """Styling tokens for list elements."""
    bullet_type: str = Field(
        default="disc",
        description="Bullet type: disc, circle, square, dash, arrow, check, none"
    )
    bullet_color: str = Field(
        ...,
        description="Bullet color (typically theme primary)"
    )
    bullet_size: str = Field(
        default="0.4em",
        description="Bullet size relative to text"
    )
    list_indent: str = Field(
        default="1.5em",
        description="List indentation from left"
    )
    item_spacing: str = Field(
        default="0.5em",
        description="Space between list items"
    )
    numbered_style: str = Field(
        default="decimal",
        description="Numbered list format: decimal, lower-alpha, upper-alpha, lower-roman, upper-roman"
    )
    nested_indent: str = Field(
        default="1.5em",
        description="Additional indent for nested lists"
    )


class TextboxDefaultsToken(BaseModel):
    """Default styling for text box containers."""
    background: str = Field(
        default="transparent",
        description="Background color"
    )
    background_gradient: Optional[str] = Field(
        default=None,
        description="CSS gradient string or null"
    )
    border_width: str = Field(
        default="0px",
        description="Border width"
    )
    border_color: str = Field(
        default="transparent",
        description="Border color"
    )
    border_radius: str = Field(
        default="8px",
        description="Corner radius"
    )
    padding: str = Field(
        default="16px",
        description="Inner padding"
    )
    box_shadow: str = Field(
        default="none",
        description="Box shadow"
    )


class TypographyTokens(BaseModel):
    """Collection of all typography tokens."""
    h1: TypographyToken
    h2: TypographyToken
    h3: TypographyToken
    h4: TypographyToken
    body: TypographyToken
    subtitle: TypographyToken
    caption: TypographyToken
    emphasis: EmphasisToken


class ThemeTypographyResponse(BaseModel):
    """
    Response model for GET /api/themes/{theme_id}/typography.

    Provides complete typography tokens for Text Service to calculate
    character constraints and apply theme-consistent styling.
    """
    theme_id: str = Field(
        ...,
        description="Theme identifier"
    )
    font_family: str = Field(
        ...,
        description="Primary font family"
    )
    font_family_heading: str = Field(
        ...,
        description="Heading font family (may equal font_family)"
    )
    tokens: TypographyTokens = Field(
        ...,
        description="Typography tokens for each text element type"
    )
    list_styles: ListStylesToken = Field(
        ...,
        description="List/bullet styling tokens"
    )
    textbox_defaults: TextboxDefaultsToken = Field(
        ...,
        description="Default text box container styling"
    )
    char_width_ratio: float = Field(
        ...,
        description="Average character width / font size ratio for this font"
    )


class ThemeConfig(BaseModel):
    """
    Complete theme configuration.

    Used for defining predefined themes in the theme registry.
    Contains colors, typography, spacing, effects, and content styles.
    """
    id: str = Field(
        ...,
        description="Unique theme identifier (e.g., 'corporate-blue')"
    )
    name: str = Field(
        ...,
        description="Display name (e.g., 'Corporate Blue')"
    )
    description: Optional[str] = Field(
        default=None,
        description="Theme description"
    )
    colors: ThemeColors = Field(
        default_factory=ThemeColors,
        description="Color palette"
    )
    typography: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Typography settings (fontFamily, standard profile, hero profile)"
    )
    spacing: Optional[ThemeSpacing] = Field(
        default=None,
        description="Spacing configuration"
    )
    effects: Optional[ThemeEffects] = Field(
        default=None,
        description="Visual effects (shadows, border-radius)"
    )
    content_styles: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Content body styles for h1/h2/h3/p tags"
    )
    is_custom: bool = Field(
        default=False,
        description="Whether this is a user-created theme"
    )


class ThemeOverrides(BaseModel):
    """
    Granular theme overrides for presentation-level customization.

    Allows overriding any aspect of a theme without creating a full custom theme.
    All fields are optional - only provided fields override the base theme.
    """
    colors: Optional[Dict[str, str]] = Field(
        default=None,
        description="Color overrides: {'primary': '#custom', 'accent': '#custom', ...}"
    )
    typography: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Typography overrides: {'font_family': 'Inter', 'title_size': '52px', ...}"
    )
    spacing: Optional[Dict[str, str]] = Field(
        default=None,
        description="Spacing overrides: {'slide_padding': '40px', 'element_gap': '32px', ...}"
    )
    effects: Optional[Dict[str, str]] = Field(
        default=None,
        description="Effects overrides: {'border_radius': '12px', 'shadow_small': '...', ...}"
    )
    content_styles: Optional[Dict[str, Dict[str, str]]] = Field(
        default=None,
        description="Content style overrides: {'h1': {'fontSize': '40px'}, ...}"
    )


class PresentationThemeConfig(BaseModel):
    """
    Presentation-level theme configuration.

    References a theme by ID (predefined or custom UUID) and allows granular overrides.
    This is what gets stored on each presentation.

    Enhanced in v7.5.4 to support:
    - Custom theme IDs (UUIDs from ls_user_themes)
    - Full theme overrides (colors, typography, spacing, effects)
    """
    theme_id: str = Field(
        default="corporate-blue",
        description="Reference to predefined theme ID or custom theme UUID"
    )
    is_custom: bool = Field(
        default=False,
        description="True if theme_id references a user custom theme (UUID)"
    )
    overrides: Optional[ThemeOverrides] = Field(
        default=None,
        description="Granular theme overrides (colors, typography, spacing, effects)"
    )
    # Legacy support - mapped to overrides.colors internally
    color_overrides: Optional[Dict[str, str]] = Field(
        default=None,
        description="[LEGACY] Per-presentation color overrides. Use 'overrides.colors' instead."
    )


# ==================== User Custom Theme Models ====================

class UserCustomThemeCreate(BaseModel):
    """
    Request model for creating a user custom theme.

    Can create either a fully custom theme or inherit from a predefined theme.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Theme name"
    )
    description: Optional[str] = Field(
        default=None,
        description="Theme description"
    )
    base_theme_id: Optional[str] = Field(
        default=None,
        description="Base theme to inherit from (e.g., 'corporate-blue'). NULL for fully custom."
    )
    colors: Optional[ThemeColors] = Field(
        default=None,
        description="Color configuration (required for fully custom themes)"
    )
    typography: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Typography configuration"
    )
    spacing: Optional[ThemeSpacing] = Field(
        default=None,
        description="Spacing configuration"
    )
    effects: Optional[ThemeEffects] = Field(
        default=None,
        description="Visual effects configuration"
    )
    content_styles: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Content styles for HTML elements"
    )


class UserCustomThemeUpdate(BaseModel):
    """
    Request model for updating a user custom theme.

    All fields are optional - only provided fields will be updated.
    """
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated theme name"
    )
    description: Optional[str] = Field(
        default=None,
        description="Updated theme description"
    )
    colors: Optional[ThemeColors] = Field(
        default=None,
        description="Updated color configuration"
    )
    typography: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Updated typography configuration"
    )
    spacing: Optional[ThemeSpacing] = Field(
        default=None,
        description="Updated spacing configuration"
    )
    effects: Optional[ThemeEffects] = Field(
        default=None,
        description="Updated visual effects configuration"
    )
    content_styles: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Updated content styles"
    )
    is_public: Optional[bool] = Field(
        default=None,
        description="Make theme public in gallery"
    )


class UserCustomTheme(BaseModel):
    """
    Complete user custom theme model (from database).

    Represents a theme stored in ls_user_themes table.
    """
    id: str = Field(
        ...,
        description="Theme UUID"
    )
    user_id: str = Field(
        ...,
        description="Owner user ID"
    )
    name: str = Field(
        ...,
        description="Theme name"
    )
    description: Optional[str] = Field(
        default=None,
        description="Theme description"
    )
    base_theme_id: Optional[str] = Field(
        default=None,
        description="Base theme ID if inheriting"
    )
    theme_config: Dict[str, Any] = Field(
        ...,
        description="Full theme configuration JSONB"
    )
    created_at: str = Field(
        ...,
        description="Creation timestamp"
    )
    updated_at: str = Field(
        ...,
        description="Last update timestamp"
    )
    is_public: bool = Field(
        default=False,
        description="Whether theme is public"
    )


class UserCustomThemeResponse(BaseModel):
    """Response model for user custom theme operations."""
    success: bool = Field(..., description="Whether operation succeeded")
    theme: Optional[UserCustomTheme] = Field(None, description="Theme data")
    message: str = Field(..., description="Success or error message")


class UserCustomThemeListResponse(BaseModel):
    """Response model for listing user themes."""
    success: bool = Field(..., description="Whether operation succeeded")
    themes: List[UserCustomTheme] = Field(..., description="List of themes")
    count: int = Field(..., description="Number of themes")


# ==================== Presentation Model ====================

class Presentation(BaseModel):
    """
    Complete presentation with multiple slides.

    Derivative Elements (v7.5.2):
    The derivative_elements field contains presentation-level footer and logo
    configurations that are automatically rendered across all slides.

    Theme System (v7.5.3):
    The theme_config field references a theme from the global registry with
    optional color overrides for presentation-level customization.
    """
    title: str = Field(
        ...,
        max_length=200,
        description="Presentation title"
    )
    slides: list[Slide] = Field(
        ...,
        min_items=1,
        description="List of slides"
    )
    derivative_elements: Optional[DerivativeElements] = Field(
        default=None,
        description="Presentation-level footer and logo that appear on all slides"
    )
    theme_config: Optional[PresentationThemeConfig] = Field(
        default=None,
        description="Theme configuration with optional color overrides"
    )


# ==================== Response Models ====================

class PresentationResponse(BaseModel):
    """Response after creating a presentation."""
    id: str = Field(..., description="Presentation UUID")
    url: str = Field(..., description="Presentation viewer URL")
    message: str = Field(..., description="Success message")


# ==================== Content Update Models ====================

class SlideContentUpdate(BaseModel):
    """
    Model for updating slide content.
    All fields are optional - only provided fields will be updated.
    """
    slide_title: Optional[str] = Field(
        None,
        max_length=80,
        description="Updated slide title"
    )
    subtitle: Optional[str] = Field(
        None,
        max_length=120,
        description="Updated subtitle"
    )
    rich_content: Optional[str] = Field(
        None,
        description="Updated rich HTML content"
    )
    hero_content: Optional[str] = Field(
        None,
        description="Updated hero content (for L29)"
    )
    # Support for other layout-specific fields
    element_1: Optional[str] = Field(None, description="Layout-specific element 1")
    element_2: Optional[str] = Field(None, description="Layout-specific element 2")
    element_3: Optional[str] = Field(None, description="Layout-specific element 3")
    element_4: Optional[str] = Field(None, description="Layout-specific element 4")
    element_5: Optional[str] = Field(None, description="Layout-specific element 5")
    presentation_name: Optional[str] = Field(None, description="Presentation name")
    company_logo: Optional[str] = Field(None, description="Company logo (legacy field)")
    logo: Optional[str] = Field(None, description="Logo content: URL, emoji, or HTML")
    # Background customization fields
    background_color: Optional[str] = Field(None, description="Slide background color (hex format)")
    background_image: Optional[str] = Field(None, description="Slide background image URL or data URI")
    # Text boxes (dynamically added elements)
    text_boxes: Optional[List[TextBox]] = Field(
        None,
        description="List of text box overlays on this slide"
    )
    # Image elements
    images: Optional[List[ImageElement]] = Field(
        None,
        description="List of image elements on this slide"
    )
    # Chart elements
    charts: Optional[List[ChartElement]] = Field(
        None,
        description="List of chart elements on this slide"
    )
    # Infographic elements
    infographics: Optional[List[InfographicElement]] = Field(
        None,
        description="List of infographic elements on this slide"
    )
    # Diagram elements
    diagrams: Optional[List[DiagramElement]] = Field(
        None,
        description="List of diagram elements on this slide"
    )
    # Content elements (L-series main content areas)
    contents: Optional[List[ContentElement]] = Field(
        None,
        description="List of content elements on this slide (L-series main content areas)"
    )


class PresentationMetadataUpdate(BaseModel):
    """Model for updating presentation metadata."""
    title: Optional[str] = Field(
        None,
        max_length=200,
        description="Updated presentation title"
    )


class BatchSlideUpdate(BaseModel):
    """Model for batch updating multiple slides."""
    slides: list[SlideContentUpdate] = Field(
        ...,
        description="List of slide content updates (index matches slide position)"
    )
    updated_by: str = Field(
        default="user",
        description="Who made the update: 'user', 'director_agent', etc."
    )
    change_summary: Optional[str] = Field(
        None,
        description="Brief description of changes made"
    )


# ==================== Version History Models ====================

class VersionMetadata(BaseModel):
    """Metadata for a presentation version."""
    version_id: str = Field(..., description="Unique version identifier")
    created_at: str = Field(..., description="ISO timestamp of version creation")
    created_by: str = Field(..., description="Who created this version: 'user', 'director_agent', etc.")
    change_summary: Optional[str] = Field(
        None,
        description="Brief description of changes in this version"
    )
    presentation_id: str = Field(..., description="Parent presentation ID")


class VersionHistoryResponse(BaseModel):
    """Response containing version history."""
    presentation_id: str = Field(..., description="Presentation ID")
    current_version_id: str = Field(..., description="Currently active version")
    versions: list[VersionMetadata] = Field(..., description="List of all versions")


class RestoreVersionRequest(BaseModel):
    """Request to restore a specific version."""
    create_backup: bool = Field(
        default=True,
        description="Whether to create a backup of current state before restore"
    )


# ==================== Section Regeneration Models (Phase 2: World-Class Editor) ====================

class SectionRegenerationRequest(BaseModel):
    """
    Request model for AI-powered section regeneration.

    This is part of Phase 2: World-Class Editor with AI-Powered Regeneration.
    Users can select specific sections within slides and request AI to regenerate
    them with custom instructions.
    """
    slide_index: int = Field(
        ...,
        ge=0,
        description="Zero-based index of the slide containing the section"
    )
    section_id: str = Field(
        ...,
        description="Unique section ID (e.g., 'slide-0-section-title')"
    )
    section_type: str = Field(
        ...,
        description="Type of section (title, subtitle, body, chart, diagram, image, text, content, hero)"
    )
    user_instruction: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's instruction for how to regenerate the section"
    )
    current_content: str = Field(
        ...,
        description="Current HTML content of the section"
    )
    layout: str = Field(
        ...,
        description="Layout type of the slide (L01, L02, L03, L25, L27, L29)"
    )


class SectionRegenerationResponse(BaseModel):
    """
    Response model for section regeneration.
    Contains the updated section content and metadata.
    """
    success: bool = Field(..., description="Whether regeneration succeeded")
    updated_content: str = Field(..., description="New HTML content for the section")
    section_id: str = Field(..., description="ID of the regenerated section")
    section_type: str = Field(..., description="Type of section that was regenerated")
    message: Optional[str] = Field(None, description="Success or error message")
    regeneration_metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the regeneration (e.g., AI model used, processing time)"
    )


# ==================== Slide CRUD Operations Models ====================

class AddSlideRequest(BaseModel):
    """
    Request model for adding a new slide to a presentation.

    The slide will be inserted at the specified position, or appended
    at the end if no position is provided.
    """
    layout: str = Field(
        ...,
        description="Layout type: predefined (L01-L29, H1-H3, C1-C5, etc.) or X-series dynamic (X1-a3f7e8c2)"
    )
    position: Optional[int] = Field(
        None,
        ge=0,
        description="Position to insert the slide (0-based). If not provided, appends at end."
    )
    content: Optional[Dict[str, Any]] = Field(
        None,
        description="Initial content for the slide. Uses layout defaults if not provided."
    )
    background_color: Optional[str] = Field(
        None,
        description="Background color in hex format (e.g., #FF5733)"
    )
    background_image: Optional[str] = Field(
        None,
        description="Background image URL or data URI"
    )

    @field_validator('layout')
    @classmethod
    def validate_add_layout(cls, v: str) -> str:
        """Validate layout ID - accepts predefined layouts and X-series dynamic layouts."""
        return validate_layout_id(v)


class ReorderSlidesRequest(BaseModel):
    """
    Request model for reordering slides within a presentation.

    Moves a slide from one position to another, shifting other slides
    accordingly.
    """
    from_index: int = Field(
        ...,
        ge=0,
        description="Current position of the slide to move (0-based)"
    )
    to_index: int = Field(
        ...,
        ge=0,
        description="New position for the slide (0-based)"
    )


class ChangeLayoutRequest(BaseModel):
    """
    Request model for changing a slide's layout type.

    Optionally preserves compatible content fields when switching layouts.
    """
    new_layout: str = Field(
        ...,
        description="New layout type: predefined (L01-L29, H1-H3, C1-C5, etc.) or X-series dynamic (X1-a3f7e8c2)"
    )
    preserve_content: bool = Field(
        True,
        description="Attempt to preserve compatible content fields when changing layouts"
    )
    content_mapping: Optional[Dict[str, str]] = Field(
        None,
        description="Manual field mapping from old to new layout: {'old_field': 'new_field'}"
    )

    @field_validator('new_layout')
    @classmethod
    def validate_change_layout(cls, v: str) -> str:
        """Validate layout ID - accepts predefined layouts and X-series dynamic layouts."""
        return validate_layout_id(v)


class DuplicateSlideRequest(BaseModel):
    """
    Request model for duplicating a slide.
    """
    insert_after: bool = Field(
        True,
        description="If True, insert duplicate after source slide. If False, insert before."
    )


class BulkDeleteSlidesRequest(BaseModel):
    """
    Request model for deleting multiple slides at once.
    Supports both sequential ranges and scattered indices.
    """
    indices: List[int] = Field(
        ...,
        description="List of 0-based slide indices to delete. Can be in any order."
    )


# ==================== Text Box CRUD Models ====================

class TextBoxCreateRequest(BaseModel):
    """
    Request model for creating a new text box on a slide.

    Position uses CSS Grid coordinates (32 columns × 18 rows).
    """
    position: TextBoxPosition = Field(
        ...,
        description="Grid position for the text box"
    )
    content: Optional[str] = Field(
        default="",
        description="Initial HTML content"
    )
    style: Optional[TextBoxStyle] = Field(
        default=None,
        description="Visual styling options (uses defaults if not provided)"
    )
    z_index: Optional[int] = Field(
        default=None,
        description="Z-index layer (auto-assigned if not provided)"
    )


class TextBoxUpdateRequest(BaseModel):
    """
    Request model for updating an existing text box.

    All fields are optional - only provided fields will be updated.
    """
    position: Optional[TextBoxPosition] = Field(
        None,
        description="Updated grid position"
    )
    content: Optional[str] = Field(
        None,
        description="Updated HTML content"
    )
    style: Optional[TextBoxStyle] = Field(
        None,
        description="Updated visual styling"
    )
    text_style: Optional[TextContentStyle] = Field(
        None,
        description="Updated text content styling"
    )
    css_classes: Optional[List[str]] = Field(
        None,
        description="Updated CSS class names"
    )
    z_index: Optional[int] = Field(
        None,
        description="Updated z-index layer"
    )
    locked: Optional[bool] = Field(
        None,
        description="Lock/unlock the text box"
    )
    visible: Optional[bool] = Field(
        None,
        description="Show/hide the text box"
    )


class ElementClassesUpdateRequest(BaseModel):
    """
    Request model for updating CSS classes on any element.
    """
    css_classes: List[str] = Field(
        ...,
        description="List of CSS class names to apply",
        examples=[["slot-content", "slot-type-bod"]]
    )
    replace: bool = Field(
        default=True,
        description="If true, replaces all custom classes; if false, adds to existing"
    )


class ElementClassesResponse(BaseModel):
    """
    Response model for element classes update.
    """
    success: bool
    element_id: str
    css_classes: List[str]


class TextBoxResponse(BaseModel):
    """Response model for text box operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    text_box: Optional[TextBox] = Field(None, description="The text box data")
    message: str = Field(..., description="Success or error message")


class TextBoxListResponse(BaseModel):
    """Response model for listing text boxes on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    text_boxes: List[TextBox] = Field(..., description="List of text boxes")
    count: int = Field(..., description="Number of text boxes")


# ==================== Image Element CRUD Models ====================

class ImageCreateRequest(BaseModel):
    """Request model for creating a new image element on a slide."""
    position: TextBoxPosition = Field(..., description="Grid position for the image")
    image_url: Optional[str] = Field(default=None, description="Image URL (null for placeholder mode)")
    alt_text: Optional[str] = Field(default=None, max_length=500, description="Alt text for accessibility")
    object_fit: str = Field(default="cover", description="CSS object-fit: cover, contain, fill, none, scale-down")
    z_index: Optional[int] = Field(default=None, description="Z-index (auto-assigned if not provided)")


class ImageUpdateRequest(BaseModel):
    """Request model for updating an existing image element."""
    position: Optional[TextBoxPosition] = None
    image_url: Optional[str] = None
    alt_text: Optional[str] = Field(default=None, max_length=500)
    object_fit: Optional[str] = None
    z_index: Optional[int] = None
    locked: Optional[bool] = None
    visible: Optional[bool] = None


class ImageResponse(BaseModel):
    """Response model for image element operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    image: Optional[ImageElement] = Field(None, description="The image element data")
    message: str = Field(..., description="Success or error message")


class ImageListResponse(BaseModel):
    """Response model for listing images on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    images: List[ImageElement] = Field(..., description="List of image elements")
    count: int = Field(..., description="Number of images")


# ==================== Chart Element CRUD Models ====================

class ChartCreateRequest(BaseModel):
    """Request model for creating a new chart element on a slide."""
    position: TextBoxPosition = Field(..., description="Grid position for the chart")
    chart_type: Optional[str] = Field(default=None, description="Chart type: bar, line, pie, doughnut, etc.")
    chart_config: Optional[Dict[str, Any]] = Field(default=None, description="Chart.js configuration object")
    chart_html: Optional[str] = Field(default=None, description="Pre-rendered HTML from Analytics Service")
    z_index: Optional[int] = Field(default=None, description="Z-index (auto-assigned if not provided)")


class ChartUpdateRequest(BaseModel):
    """Request model for updating an existing chart element."""
    position: Optional[TextBoxPosition] = None
    chart_type: Optional[str] = None
    chart_config: Optional[Dict[str, Any]] = None
    chart_html: Optional[str] = None
    z_index: Optional[int] = None
    locked: Optional[bool] = None
    visible: Optional[bool] = None


class ChartResponse(BaseModel):
    """Response model for chart element operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    chart: Optional[ChartElement] = Field(None, description="The chart element data")
    message: str = Field(..., description="Success or error message")


class ChartListResponse(BaseModel):
    """Response model for listing charts on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    charts: List[ChartElement] = Field(..., description="List of chart elements")
    count: int = Field(..., description="Number of charts")


# ==================== Diagram Element CRUD Models ====================

class DiagramCreateRequest(BaseModel):
    """Request model for creating a new diagram element on a slide."""
    position: TextBoxPosition = Field(..., description="Grid position for the diagram")
    diagram_type: Optional[str] = Field(default=None, description="Diagram type: flowchart, sequence, etc.")
    mermaid_code: Optional[str] = Field(default=None, description="Mermaid.js diagram code")
    svg_content: Optional[str] = Field(default=None, description="Pre-rendered SVG content")
    html_content: Optional[str] = Field(default=None, description="Pre-rendered HTML content")
    direction: str = Field(default="TB", description="Layout direction: TB, LR, BT, RL")
    theme: str = Field(default="default", description="Diagram theme: default, dark, forest, neutral")
    z_index: Optional[int] = Field(default=None, description="Z-index (auto-assigned if not provided)")


class DiagramUpdateRequest(BaseModel):
    """Request model for updating an existing diagram element."""
    position: Optional[TextBoxPosition] = None
    diagram_type: Optional[str] = None
    mermaid_code: Optional[str] = None
    svg_content: Optional[str] = None
    html_content: Optional[str] = None
    direction: Optional[str] = None
    theme: Optional[str] = None
    z_index: Optional[int] = None
    locked: Optional[bool] = None
    visible: Optional[bool] = None


class DiagramResponse(BaseModel):
    """Response model for diagram element operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    diagram: Optional[DiagramElement] = Field(None, description="The diagram element data")
    message: str = Field(..., description="Success or error message")


class DiagramListResponse(BaseModel):
    """Response model for listing diagrams on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    diagrams: List[DiagramElement] = Field(..., description="List of diagram elements")
    count: int = Field(..., description="Number of diagrams")


# ==================== Infographic Element CRUD Models ====================

class InfographicCreateRequest(BaseModel):
    """Request model for creating a new infographic element on a slide."""
    position: TextBoxPosition = Field(..., description="Grid position for the infographic")
    infographic_type: Optional[str] = Field(default=None, description="Infographic type: timeline, process, etc.")
    svg_content: Optional[str] = Field(default=None, description="SVG content from Illustrator Service")
    html_content: Optional[str] = Field(default=None, description="Pre-rendered HTML content")
    items: Optional[List[Dict[str, Any]]] = Field(default=None, description="Data items for the infographic")
    z_index: Optional[int] = Field(default=None, description="Z-index (auto-assigned if not provided)")


class InfographicUpdateRequest(BaseModel):
    """Request model for updating an existing infographic element."""
    position: Optional[TextBoxPosition] = None
    infographic_type: Optional[str] = None
    svg_content: Optional[str] = None
    html_content: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    z_index: Optional[int] = None
    locked: Optional[bool] = None
    visible: Optional[bool] = None


class InfographicResponse(BaseModel):
    """Response model for infographic element operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    infographic: Optional[InfographicElement] = Field(None, description="The infographic element data")
    message: str = Field(..., description="Success or error message")


class InfographicListResponse(BaseModel):
    """Response model for listing infographics on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    infographics: List[InfographicElement] = Field(..., description="List of infographic elements")
    count: int = Field(..., description="Number of infographics")


# ==================== Content Element CRUD Models ====================

class ContentCreateRequest(BaseModel):
    """Request model for creating a new content element on a slide."""
    slot_name: str = Field(..., description="Slot name from template registry (e.g., 'content', 'hero')")
    position: TextBoxPosition = Field(..., description="Grid position for the content")
    content_html: str = Field(default="", description="HTML content from Text Service")
    content_type: str = Field(default="html", description="Content type: html, chart, diagram, infographic")
    format_owner: str = Field(default="text_service", description="Service that owns formatting")
    z_index: Optional[int] = Field(default=None, description="Z-index (auto-assigned if not provided)")


class ContentUpdateRequest(BaseModel):
    """Request model for updating an existing content element."""
    slot_name: Optional[str] = None
    position: Optional[TextBoxPosition] = None
    content_html: Optional[str] = None
    content_type: Optional[str] = None
    format_owner: Optional[str] = None
    z_index: Optional[int] = None
    editable: Optional[bool] = None
    locked: Optional[bool] = None
    visible: Optional[bool] = None


class ContentResponse(BaseModel):
    """Response model for content element operations."""
    success: bool = Field(..., description="Whether the operation succeeded")
    content: Optional[ContentElement] = Field(None, description="The content element data")
    message: str = Field(..., description="Success or error message")


class ContentListResponse(BaseModel):
    """Response model for listing content elements on a slide."""
    success: bool = Field(..., description="Whether the operation succeeded")
    slide_index: int = Field(..., description="The slide index")
    contents: List[ContentElement] = Field(..., description="List of content elements")
    count: int = Field(..., description="Number of content elements")


# ==================== AI Text Generation Models ====================

class TextGenerationRequest(BaseModel):
    """
    Request model for AI-powered text generation for text boxes.

    Routes to Text Service for content generation.
    """
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User prompt describing desired text content"
    )
    textbox_id: Optional[str] = Field(
        None,
        description="Target text box ID to inject result (optional)"
    )
    tone: Optional[str] = Field(
        default="professional",
        description="Desired tone: professional, casual, academic, persuasive"
    )
    length: Optional[str] = Field(
        default="medium",
        description="Desired length: short, medium, long"
    )
    format: Optional[str] = Field(
        default="paragraph",
        description="Output format: paragraph, bullets, numbered"
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context: presentation_title, slide_title, audience, etc."
    )
    max_characters: Optional[int] = Field(
        default=500, ge=50, le=2000,
        description="Maximum character limit for generated text"
    )


class TextGenerationResponse(BaseModel):
    """Response model for AI text generation."""
    success: bool = Field(..., description="Whether generation succeeded")
    content: str = Field(..., description="Generated HTML content")
    plain_text: Optional[str] = Field(None, description="Plain text version")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Generation metadata: tokens_used, model, generation_time_ms"
    )
    error: Optional[str] = Field(None, description="Error message if failed")


# ==================== Director Service Integration Models ====================
# These models support the 5 new endpoints for Director Service coordination


class SlotPixels(BaseModel):
    """Pixel dimensions for a slot."""
    x: float = Field(..., description="X position in pixels")
    y: float = Field(..., description="Y position in pixels")
    width: float = Field(..., description="Width in pixels")
    height: float = Field(..., description="Height in pixels")


class SlotDefinition(BaseModel):
    """Definition of a single slot within a template."""
    grid_row: str = Field(..., description="CSS grid row (e.g., '4/18')")
    grid_column: str = Field(..., description="CSS grid column (e.g., '2/32')")
    tag: str = Field(..., description="Content tag (title, body, chart, etc.)")
    accepts: List[str] = Field(..., description="Accepted content types")
    required: Optional[bool] = Field(default=False, description="Whether slot is required")
    description: Optional[str] = Field(default=None, description="Slot description")
    default_text: Optional[str] = Field(default=None, description="Default placeholder text")
    format_owner: Optional[str] = Field(default=None, description="Service that owns format (text_service, analytics_service)")
    pixels: Optional[SlotPixels] = Field(default=None, description="Computed pixel dimensions")


class LayoutSummary(BaseModel):
    """Summary of a layout for listing endpoints."""
    layout_id: str = Field(..., description="Layout ID (e.g., L25, C1-text)")
    name: str = Field(..., description="Human-readable name")
    series: str = Field(..., description="Layout series (H, C, V, I, S, B, L)")
    category: str = Field(..., description="Category (hero, content, visual, image, split, blank, backend)")
    description: str = Field(..., description="Layout description")
    theming_enabled: bool = Field(..., description="Whether theming is supported")
    base_layout: Optional[str] = Field(default=None, description="Base backend layout ID if applicable")
    primary_content_types: List[str] = Field(default=[], description="Primary content types this layout is designed for")
    main_content_dimensions: Optional[SlotPixels] = Field(default=None, description="Dimensions of main content area")


class LayoutDetailResponse(BaseModel):
    """Detailed layout response with full slot definitions."""
    layout_id: str = Field(..., description="Layout ID")
    name: str = Field(..., description="Human-readable name")
    series: str = Field(..., description="Layout series")
    category: str = Field(..., description="Category")
    description: str = Field(..., description="Layout description")
    theming_enabled: bool = Field(..., description="Whether theming is supported")
    base_layout: Optional[str] = Field(default=None, description="Base backend layout ID")
    slide_dimensions: Dict[str, Any] = Field(
        default={"width": 1920, "height": 1080, "unit": "pixels"},
        description="Slide dimensions"
    )
    slots: Dict[str, SlotDefinition] = Field(..., description="All slots with definitions")
    defaults: Dict[str, Any] = Field(default={}, description="Default values")


class LayoutListResponse(BaseModel):
    """Response for listing all layouts."""
    layouts: List[LayoutSummary] = Field(..., description="List of layout summaries")
    total: int = Field(..., description="Total number of layouts")
    categories: Dict[str, List[str]] = Field(default={}, description="Templates grouped by category")


class LayoutRecommendationRequest(BaseModel):
    """Request for layout recommendation."""
    content_type: str = Field(
        ...,
        description="Type of content: chart, diagram, text, hero, comparison, image, infographic"
    )
    topic_count: int = Field(
        default=1, ge=1, le=10,
        description="Number of topics/items to display"
    )
    service: str = Field(
        default="director",
        description="Requesting service: director, text-service, analytics-service"
    )
    variant: Optional[str] = Field(
        default=None,
        description="Content variant: single, split, comparison, etc."
    )
    preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional preferences: image_position, chart_type, etc."
    )


class LayoutRecommendation(BaseModel):
    """A single layout recommendation."""
    layout_id: str = Field(..., description="Recommended layout ID")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    reason: str = Field(..., description="Reason for recommendation")
    main_content_slots: List[Dict[str, Any]] = Field(
        default=[],
        description="Main content slots with pixel dimensions"
    )


class LayoutRecommendationResponse(BaseModel):
    """Response for layout recommendation."""
    recommended_layouts: List[LayoutRecommendation] = Field(
        ...,
        description="List of recommended layouts in order of preference"
    )
    fallback: str = Field(
        default="L25",
        description="Universal fallback layout if none match"
    )
    request_summary: Dict[str, Any] = Field(
        default={},
        description="Summary of the request parameters"
    )


class CanFitRequest(BaseModel):
    """Request to check if content can fit in a layout."""
    layout_id: str = Field(..., description="Layout ID to check")
    content_zones_needed: int = Field(
        default=1, ge=1, le=10,
        description="Number of content zones needed"
    )
    content_type: str = Field(
        ...,
        description="Type of content to fit: text, chart, diagram, image, etc."
    )


class CanFitResponse(BaseModel):
    """Response for can-fit check."""
    can_fit: bool = Field(..., description="Whether content can fit")
    layout_id: str = Field(..., description="Layout that was checked")
    content_zones_available: int = Field(..., description="Available zones for this content type")
    content_zones_needed: int = Field(..., description="Zones requested")
    suggested_layout: Optional[str] = Field(
        default=None,
        description="Alternative layout suggestion if content doesn't fit"
    )
    reason: str = Field(..., description="Explanation of the result")


class CapabilitiesResponse(BaseModel):
    """Response for service capabilities endpoint."""
    service: str = Field(default="layout-service", description="Service name")
    version: str = Field(..., description="Service version")
    status: str = Field(default="healthy", description="Service status")
    capabilities: Dict[str, Any] = Field(..., description="Service capabilities")
    template_series: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Information about each template series"
    )
    standard_zones: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Standard zone definitions"
    )
    endpoints: Dict[str, str] = Field(..., description="Available endpoints")


# ==================== X-Series: Dynamic Layout Models ====================
# X-series layouts dynamically split the content area of base templates (C1, I1-I4)
# into sub-zones based on content analysis.

# Valid base layouts for X-series
ValidXSeriesBase = Literal[
    "C1-text",              # X1 base - full content area
    "I1-image-left",        # X2 base - content right of image
    "I2-image-right",       # X3 base - content left of image
    "I3-image-left-narrow", # X4 base - wider content area
    "I4-image-right-narrow" # X5 base - wider content area
]

# Valid split directions
ValidSplitDirection = Literal["horizontal", "vertical", "grid"]


class ZonePixels(BaseModel):
    """Pixel coordinates for a zone within the content area."""
    x: int = Field(..., description="X position in pixels from slide left edge")
    y: int = Field(..., description="Y position in pixels from slide top edge")
    width: int = Field(..., description="Zone width in pixels")
    height: int = Field(..., description="Zone height in pixels")


class ZoneDefinition(BaseModel):
    """
    Definition of a sub-zone within the content area.

    Note: This is distinct from SlotDefinition which defines template slots.
    ZoneDefinition defines dynamic sub-zones created by splitting a content area.
    """
    zone_id: str = Field(..., description="Zone identifier (zone_1, zone_2, etc.)")
    label: Optional[str] = Field(default=None, description="Human-readable zone label")
    grid_row: str = Field(..., description="CSS grid row (e.g., '4/9')")
    grid_column: str = Field(..., description="CSS grid column (e.g., '2/32')")
    pixels: ZonePixels = Field(..., description="Pixel coordinates and dimensions")
    content_type_hint: Optional[str] = Field(
        default=None,
        description="Suggested content type: heading, bullets, paragraph, highlight, etc."
    )
    z_index: int = Field(default=100, description="Z-index for layering")


class DynamicLayoutRequest(BaseModel):
    """
    Request to generate a dynamic X-series layout.

    X-series layouts split the main content area of base templates into
    multiple sub-zones based on content requirements.

    X-Series Mapping:
    - X1 → C1-text (1800×840px content area)
    - X2 → I1-image-left (1200×840px content area)
    - X3 → I2-image-right (1140×840px content area)
    - X4 → I3-image-left-narrow (1500×840px content area)
    - X5 → I4-image-right-narrow (1440×840px content area)
    """
    base_layout: ValidXSeriesBase = Field(
        ...,
        description="Base layout to use (C1-text, I1-I4)"
    )
    content_type: str = Field(
        ...,
        description="Content type: agenda, use_case, comparison, features, timeline, process, custom"
    )
    zone_count: int = Field(
        default=3,
        ge=2, le=8,
        description="Number of zones to create (2-8)"
    )
    split_direction: Optional[ValidSplitDirection] = Field(
        default=None,
        description="Preferred split direction: horizontal, vertical, or grid"
    )
    split_pattern: Optional[str] = Field(
        default=None,
        description="Named split pattern (e.g., agenda-3-item, comparison-2col)"
    )
    zone_labels: Optional[List[str]] = Field(
        default=None,
        description="Optional labels for each zone"
    )
    custom_ratios: Optional[List[float]] = Field(
        default=None,
        description="Custom split ratios (must sum to 1.0)"
    )

    @field_validator('custom_ratios')
    @classmethod
    def validate_ratios(cls, v, info):
        if v is not None:
            if abs(sum(v) - 1.0) > 0.01:
                raise ValueError('custom_ratios must sum to 1.0')
            zone_count = info.data.get('zone_count', 3)
            if len(v) != zone_count:
                raise ValueError(f'custom_ratios length must match zone_count ({zone_count})')
        return v


class DynamicLayoutResponse(BaseModel):
    """
    Response containing a generated dynamic X-series layout.

    The layout_id follows the pattern X{series}-{hash8} where:
    - series: 1-5 corresponding to base layout
    - hash8: 8-character hash of the zone configuration

    This layout_id can be used like any other layout (C1, I1, etc.)
    for content generation and rendering.
    """
    layout_id: str = Field(
        ...,
        description="Unique layout ID (e.g., X1-a3f7e8c2)"
    )
    base_layout: ValidXSeriesBase = Field(
        ...,
        description="Base layout that was split"
    )
    name: str = Field(
        ...,
        description="Human-readable layout name"
    )
    description: Optional[str] = Field(
        default=None,
        description="Layout description"
    )
    content_type: str = Field(
        ...,
        description="Content type this layout is optimized for"
    )
    zones: List[ZoneDefinition] = Field(
        ...,
        description="List of zone definitions"
    )
    split_pattern: str = Field(
        ...,
        description="Split pattern used (preconfigured or custom)"
    )
    split_direction: ValidSplitDirection = Field(
        ...,
        description="Direction of the split"
    )
    content_area: ZonePixels = Field(
        ...,
        description="Original content area that was split"
    )
    reusable: bool = Field(
        default=True,
        description="Whether this layout can be reused"
    )
    created_at: Optional[str] = Field(
        default=None,
        description="ISO timestamp of creation"
    )


class DynamicLayoutListResponse(BaseModel):
    """Response for listing dynamic layouts."""
    layouts: List[DynamicLayoutResponse] = Field(
        ...,
        description="List of dynamic layouts"
    )
    total: int = Field(..., description="Total number of layouts")
    by_base: Dict[str, int] = Field(
        default={},
        description="Count of layouts by base template"
    )
    by_content_type: Dict[str, int] = Field(
        default={},
        description="Count of layouts by content type"
    )
