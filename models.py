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
# All supported layouts: Backend (L01-L29) + Frontend Templates (H1-H3, C1-C6, S1-S4, B1)

ValidLayoutType = Literal[
    # Backend layouts
    "L01", "L02", "L03", "L25", "L27", "L29",
    # Frontend templates - Hero
    "H1-generated", "H1-structured", "H2-section", "H3-closing",
    # Frontend templates - Content
    "C1-text", "C2-table", "C3-chart", "C4-infographic", "C5-diagram", "C6-image",
    # Frontend templates - Split
    "S1-visual-text", "S2-image-content", "S3-two-visuals", "S4-comparison",
    # Frontend templates - Blank
    "B1-blank"
]


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
        description="Company logo URL or HTML for footer right section (optional)"
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
    border_radius: int = Field(
        default=0, ge=0, le=50,
        description="Border radius in pixels"
    )
    padding: int = Field(
        default=16, ge=0, le=100,
        description="Internal padding in pixels"
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


class TextBox(BaseModel):
    """
    A text box element that can be placed on any slide.

    Text boxes are overlay elements that float above the main layout content.
    They support rich HTML content with inline styling for multi-style text.
    Text boxes have elevated z-index (1000+) to appear above other elements.
    """
    id: str = Field(
        default_factory=lambda: f"textbox-{uuid4().hex[:12]}",
        description="Unique identifier for the text box"
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
    """
    id: str = Field(
        default_factory=lambda: f"image-{uuid4().hex[:12]}",
        description="Unique identifier for the image element"
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
    """
    id: str = Field(
        default_factory=lambda: f"chart-{uuid4().hex[:12]}",
        description="Unique identifier for the chart element"
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
    """
    id: str = Field(
        default_factory=lambda: f"infographic-{uuid4().hex[:12]}",
        description="Unique identifier for the infographic element"
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
    """
    id: str = Field(
        default_factory=lambda: f"diagram-{uuid4().hex[:12]}",
        description="Unique identifier for the diagram element"
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


# ==================== Slide Model ====================

class Slide(BaseModel):
    """
    Individual slide with layout, content, and overlay elements.

    Element types:
    - text_boxes: Overlay text elements with rich HTML content
    - images: Image elements (placeholder or actual images)
    - charts: Chart elements (placeholder or actual Chart.js charts)
    - infographics: Infographic elements (placeholder or SVG content)
    - diagrams: Diagram elements (placeholder, Mermaid, or SVG content)

    All element types are persisted and restored on load.
    """
    layout: ValidLayoutType = Field(
        ...,
        description="Layout identifier (backend L01-L29 or frontend H1-H3, C1-C6, S1-S4, B1)"
    )
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


# ==================== Presentation Model ====================

class Presentation(BaseModel):
    """Complete presentation with multiple slides."""
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
    company_logo: Optional[str] = Field(None, description="Company logo")
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
    layout: ValidLayoutType = Field(
        ...,
        description="Layout type for the new slide (backend L01-L29 or frontend H1-H3, C1-C6, S1-S4, B1)"
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
    new_layout: ValidLayoutType = Field(
        ...,
        description="New layout type for the slide (backend L01-L29 or frontend H1-H3, C1-C6, S1-S4, B1)"
    )
    preserve_content: bool = Field(
        True,
        description="Attempt to preserve compatible content fields when changing layouts"
    )
    content_mapping: Optional[Dict[str, str]] = Field(
        None,
        description="Manual field mapping from old to new layout: {'old_field': 'new_field'}"
    )


class DuplicateSlideRequest(BaseModel):
    """
    Request model for duplicating a slide.
    """
    insert_after: bool = Field(
        True,
        description="If True, insert duplicate after source slide. If False, insert before."
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
