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
