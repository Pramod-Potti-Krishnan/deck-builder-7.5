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

from pydantic import BaseModel, Field
from typing import Optional, Union, Literal, Dict, Any


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


# ==================== Slide Model ====================

class Slide(BaseModel):
    """Individual slide with layout and content."""
    layout: Literal["L01", "L02", "L03", "L25", "L27", "L29"] = Field(
        ...,
        description="Layout identifier"
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
