"""
FastAPI server for v7.5-main: Simplified Layout Architecture

Port: 8504
Backend Layouts: L01, L02, L03, L25, L27, L29
Frontend Templates: H1-generated, H1-structured, H2-section, H3-closing,
                   C1-text, C3-chart, C4-infographic, C5-diagram,
                   V1-image-text, V2-chart-text, V3-diagram-text, V4-infographic-text,
                   I1-image-left, I2-image-right, I3-image-left-narrow, I4-image-right-narrow,
                   S3-two-visuals, S4-comparison, B1-blank
"""

import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from models import (
    Presentation,
    PresentationResponse,
    SlideContentUpdate,
    PresentationMetadataUpdate,
    VersionHistoryResponse,
    VersionMetadata,
    RestoreVersionRequest,
    SectionRegenerationRequest,
    SectionRegenerationResponse,
    AddSlideRequest,
    ReorderSlidesRequest,
    ChangeLayoutRequest,
    DuplicateSlideRequest,
    BulkDeleteSlidesRequest,
    # Text Box models
    TextBox,
    TextBoxPosition,
    TextBoxStyle,
    TextBoxCreateRequest,
    TextBoxUpdateRequest,
    TextBoxResponse,
    TextBoxListResponse,
    TextGenerationRequest,
    TextGenerationResponse,
    # Element property models
    ElementClassesUpdateRequest,
    ElementClassesResponse,
    TextContentStyle,
    # Derivative Elements models (presentation-level footer/logo)
    DerivativeElements,
    FooterConfig,
    LogoConfig,
    # Theme models
    ThemeColors,
    ThemeConfig,
    ThemeSpacing,
    ThemeEffects,
    ThemeOverrides,
    PresentationThemeConfig,
    # User Custom Theme models (v7.5.4)
    UserCustomTheme,
    UserCustomThemeCreate,
    UserCustomThemeUpdate,
    UserCustomThemeResponse,
    UserCustomThemeListResponse
)
from storage import storage
import copy


# ==================== Predefined Themes ====================

PREDEFINED_THEMES: dict[str, ThemeConfig] = {
    "corporate-blue": ThemeConfig(
        id="corporate-blue",
        name="Corporate Blue",
        description="Professional blue theme for business presentations",
        colors=ThemeColors(
            primary="#1e40af",
            primary_light="#3b82f6",
            primary_dark="#1e3a8a",
            accent="#f59e0b",
            background="#ffffff",
            background_alt="#f8fafc",
            text_primary="#1f2937",
            text_secondary="#6b7280",
            text_body="#374151",
            hero_text_primary="#ffffff",
            hero_text_secondary="#e5e7eb",
            hero_background="#1e3a5f",
            footer_text="#6b7280",
            border="#e5e7eb"
        ),
        typography={
            "fontFamily": "Poppins, sans-serif",
            "standard": {
                "title": {"fontSize": "42px", "fontWeight": "bold", "lineHeight": "1.2"},
                "subtitle": {"fontSize": "24px", "fontWeight": "normal", "lineHeight": "1.4"},
                "body": {"fontSize": "20px", "lineHeight": "1.6"},
                "footer": {"fontSize": "18px", "fontWeight": "500"}
            },
            "hero": {
                "title": {"fontSize": "72px", "fontWeight": "bold", "textShadow": "0 2px 4px rgba(0,0,0,0.3)"},
                "subtitle": {"fontSize": "32px", "fontWeight": "normal"},
                "footer": {"fontSize": "18px"}
            }
        },
        content_styles={
            "h1": {"fontSize": "36px", "fontWeight": "bold", "marginBottom": "16px"},
            "h2": {"fontSize": "28px", "fontWeight": "600", "marginBottom": "12px"},
            "h3": {"fontSize": "22px", "fontWeight": "600", "marginBottom": "8px"},
            "p": {"fontSize": "20px", "lineHeight": "1.6", "marginBottom": "12px"},
            "ul": {"paddingLeft": "24px", "marginBottom": "12px"},
            "li": {"marginBottom": "6px"}
        },
        is_custom=False
    ),
    "elegant-emerald": ThemeConfig(
        id="elegant-emerald",
        name="Elegant Emerald",
        description="Sophisticated theme with nature-inspired elegance",
        colors=ThemeColors(
            primary="#059669",
            primary_light="#10b981",
            primary_dark="#047857",
            accent="#fbbf24",
            background="#f0fdf4",
            background_alt="#ecfdf5",
            text_primary="#064e3b",
            text_secondary="#047857",
            text_body="#065f46",
            hero_text_primary="#ecfdf5",
            hero_text_secondary="#a7f3d0",
            hero_background="#064e3b",
            footer_text="#059669",
            border="#d1fae5"
        ),
        typography={
            "fontFamily": "Lato, sans-serif",
            "fontFamilyHeading": "Playfair Display, serif",
            "standard": {
                "title": {"fontSize": "46px", "fontWeight": "700", "lineHeight": "1.2"},
                "subtitle": {"fontSize": "22px", "fontWeight": "normal", "lineHeight": "1.4"},
                "body": {"fontSize": "20px", "lineHeight": "1.6"},
                "footer": {"fontSize": "16px", "fontWeight": "500"}
            },
            "hero": {
                "title": {"fontSize": "70px", "fontWeight": "700", "textShadow": "0 2px 4px rgba(0,0,0,0.2)"},
                "subtitle": {"fontSize": "28px", "fontWeight": "normal"},
                "footer": {"fontSize": "16px"}
            }
        },
        content_styles={
            "h1": {"fontSize": "38px", "fontWeight": "700", "marginBottom": "16px"},
            "h2": {"fontSize": "30px", "fontWeight": "600", "marginBottom": "12px"},
            "h3": {"fontSize": "24px", "fontWeight": "600", "marginBottom": "8px"},
            "p": {"fontSize": "20px", "lineHeight": "1.6", "marginBottom": "12px"},
            "ul": {"paddingLeft": "24px", "marginBottom": "12px"},
            "li": {"marginBottom": "6px"}
        },
        is_custom=False
    ),
    "vibrant-orange": ThemeConfig(
        id="vibrant-orange",
        name="Vibrant Orange",
        description="Energetic, bold theme for creative presentations",
        colors=ThemeColors(
            primary="#ea580c",
            primary_light="#f97316",
            primary_dark="#c2410c",
            accent="#0891b2",
            background="#fff7ed",  # Warm cream instead of white
            background_alt="#ffedd5",
            text_primary="#7c2d12",  # Dark brown-orange
            text_secondary="#9a3412",  # Rust
            text_body="#78350f",
            hero_text_primary="#ffffff",
            hero_text_secondary="#fed7aa",  # Peach
            hero_background="#c2410c",  # Burnt orange
            footer_text="#a8a29e",
            border="#fdba74"
        ),
        typography={
            "fontFamily": "Montserrat, sans-serif",
            "standard": {
                "title": {"fontSize": "44px", "fontWeight": "700", "lineHeight": "1.2"},
                "subtitle": {"fontSize": "26px", "fontWeight": "500", "lineHeight": "1.4"},
                "body": {"fontSize": "20px", "lineHeight": "1.6"},
                "footer": {"fontSize": "18px", "fontWeight": "500"}
            },
            "hero": {
                "title": {"fontSize": "76px", "fontWeight": "800", "textShadow": "0 3px 6px rgba(0,0,0,0.4)"},
                "subtitle": {"fontSize": "34px", "fontWeight": "500"},
                "footer": {"fontSize": "18px"}
            }
        },
        content_styles={
            "h1": {"fontSize": "40px", "fontWeight": "700", "marginBottom": "16px"},
            "h2": {"fontSize": "32px", "fontWeight": "600", "marginBottom": "12px"},
            "h3": {"fontSize": "26px", "fontWeight": "600", "marginBottom": "8px"},
            "p": {"fontSize": "20px", "lineHeight": "1.6", "marginBottom": "12px"},
            "ul": {"paddingLeft": "24px", "marginBottom": "12px"},
            "li": {"marginBottom": "6px"}
        },
        is_custom=False
    ),
    "dark-mode": ThemeConfig(
        id="dark-mode",
        name="Dark Mode",
        description="Modern, elegant dark theme with dramatic contrast",
        colors=ThemeColors(
            primary="#60a5fa",
            primary_light="#93c5fd",
            primary_dark="#3b82f6",
            accent="#fbbf24",  # Amber accent
            background="#111827",  # Charcoal
            background_alt="#1f2937",
            text_primary="#f9fafb",  # Near white
            text_secondary="#d1d5db",  # Light gray
            text_body="#e5e7eb",
            hero_text_primary="#ffffff",
            hero_text_secondary="#9ca3af",  # Muted gray
            hero_background="#030712",  # Near black
            footer_text="#6b7280",
            border="#374151"
        ),
        typography={
            "fontFamily": "Inter, sans-serif",
            "standard": {
                "title": {"fontSize": "40px", "fontWeight": "600", "lineHeight": "1.2"},
                "subtitle": {"fontSize": "22px", "fontWeight": "normal", "lineHeight": "1.4"},
                "body": {"fontSize": "20px", "lineHeight": "1.6"},
                "footer": {"fontSize": "16px", "fontWeight": "500"}
            },
            "hero": {
                "title": {"fontSize": "68px", "fontWeight": "600", "textShadow": "0 4px 8px rgba(0,0,0,0.6)"},
                "subtitle": {"fontSize": "30px", "fontWeight": "normal"},
                "footer": {"fontSize": "16px"}
            }
        },
        content_styles={
            "h1": {"fontSize": "36px", "fontWeight": "600", "marginBottom": "16px"},
            "h2": {"fontSize": "28px", "fontWeight": "500", "marginBottom": "12px"},
            "h3": {"fontSize": "22px", "fontWeight": "500", "marginBottom": "8px"},
            "p": {"fontSize": "20px", "lineHeight": "1.6", "marginBottom": "12px"},
            "ul": {"paddingLeft": "24px", "marginBottom": "12px"},
            "li": {"marginBottom": "6px"}
        },
        is_custom=False
    )
}

DEFAULT_THEME_ID = "corporate-blue"


# ==================== Helper Functions ====================

def get_default_content(layout: str) -> dict:
    """
    Get default content template for a layout type.

    These defaults provide a starting point for new slides.
    Supports both backend layouts (L01-L29) and frontend templates (H1, C1, S1, B1).
    """
    defaults = {
        # ========== BACKEND LAYOUTS ==========
        "L01": {
            "slide_title": "Chart Title",
            "element_1": "Subtitle",
            "element_4": "<div style='width:100%;height:400px;display:flex;align-items:center;justify-content:center;background:#f8fafc;border:2px dashed #cbd5e1;border-radius:8px;'><span style='color:#64748b;'>Chart placeholder</span></div>",
            "element_3": "Add descriptive text here"
        },
        "L02": {
            "slide_title": "Diagram Title",
            "element_1": "Diagram Label",
            "element_4": "<div style='width:100%;height:500px;display:flex;align-items:center;justify-content:center;background:#f8fafc;border:2px dashed #cbd5e1;border-radius:8px;'><span style='color:#64748b;'>Diagram placeholder</span></div>",
            "element_2": "<ul><li>Key point one</li><li>Key point two</li><li>Key point three</li></ul>"
        },
        "L03": {
            "slide_title": "Comparison View",
            "element_1": "Left Chart Title",
            "element_4": "<div style='width:100%;height:350px;display:flex;align-items:center;justify-content:center;background:#f8fafc;border:2px dashed #cbd5e1;border-radius:8px;'><span style='color:#64748b;'>Chart 1</span></div>",
            "element_2": "Right Chart Title",
            "element_5": "<div style='width:100%;height:350px;display:flex;align-items:center;justify-content:center;background:#f8fafc;border:2px dashed #cbd5e1;border-radius:8px;'><span style='color:#64748b;'>Chart 2</span></div>",
            "element_3": "Analysis and insights"
        },
        "L25": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle goes here",
            "rich_content": "<div style='padding: 20px;'><h2 style='color: #1f2937; margin-bottom: 16px;'>Content Heading</h2><p style='color: #374151; line-height: 1.6;'>Add your content here. This layout provides a large content area for rich text, lists, and formatted content.</p><ul style='margin-top: 16px; color: #374151;'><li>First point</li><li>Second point</li><li>Third point</li></ul></div>"
        },
        "L27": {
            "slide_title": "Image & Content",
            "element_1": "<div style='width:100%;height:600px;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);border-radius:8px;'><span style='color:white;font-size:24px;'>Image placeholder</span></div>",
            "element_2": "<h3 style='color:#1f2937;margin-bottom:12px;'>Description</h3><p style='color:#374151;line-height:1.6;'>Add descriptive content about the image on the left.</p>"
        },
        "L29": {
            "hero_content": "<div style='width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);'><h1 style='color:white;font-size:64px;font-weight:bold;text-shadow:2px 2px 8px rgba(0,0,0,0.3);margin-bottom:24px;'>Hero Title</h1><p style='color:rgba(255,255,255,0.8);font-size:24px;'>Subtitle or tagline goes here</p></div>"
        },

        # ========== FRONTEND TEMPLATES - HERO ==========
        "H1-generated": {
            "hero_content": "",
            "background_color": "#1f2937"
        },
        "H1-structured": {
            "slide_title": "Presentation Title",
            "subtitle": "Your tagline or subtitle here",
            "footer_text": "",
            "background_color": "#1e3a5f"
        },
        "H2-section": {
            "section_number": "#",
            "slide_title": "Section Title",
            "subtitle": "",
            "background_color": "#374151"
        },
        "H3-closing": {
            "slide_title": "Thank You",
            "subtitle": "Questions & Discussion",
            "contact_info": "",
            "background_color": "#1e3a5f"
        },

        # ========== FRONTEND TEMPLATES - CONTENT ==========
        # Default text values should match Template Builder v7.4 placeholders
        "C1-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "body": "Content Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        # C2-table REMOVED - merged into C1-text (tables are hypertext)
        "C3-chart": {
            "slide_title": "Chart Title",
            "subtitle": "Subtitle",
            "chart_html": "Chart Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "C4-infographic": {
            "slide_title": "Infographic Title",
            "subtitle": "Subtitle",
            "infographic_svg": "Infographic Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "C5-diagram": {
            "slide_title": "Diagram Title",
            "subtitle": "Subtitle",
            "diagram_svg": "Diagram Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        # C6-image REMOVED - use I series for image layouts

        # ========== FRONTEND TEMPLATES - VISUAL + TEXT (V Series) ==========
        "V1-image-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "Key Insights",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "V2-chart-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "chart_html": "",
            "body": "Key Insights",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "V3-diagram-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "diagram_svg": "",
            "body": "Key Insights",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "V4-infographic-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "infographic_svg": "",
            "body": "Key Insights",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },

        # ========== FRONTEND TEMPLATES - IMAGE SPLIT (I Series) ==========
        "I1-image-left": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "I2-image-right": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "I3-image-left-narrow": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "I4-image-right-narrow": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },

        # ========== FRONTEND TEMPLATES - SPLIT (S Series) ==========
        # S1-visual-text REMOVED - replaced by V series (V1-V4)
        # S2-image-content REMOVED - replaced by I series (I1-I4)
        "S3-two-visuals": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "visual_left": "Left Visual",
            "visual_right": "Right Visual",
            "caption_left": "Left Caption",
            "caption_right": "Right Caption",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "S4-comparison": {
            "slide_title": "Comparison",
            "subtitle": "Subtitle",
            "header_left": "Option A",
            "header_right": "Option B",
            "content_left": "Left Content",
            "content_right": "Right Content",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },

        # ========== FRONTEND TEMPLATES - BLANK ==========
        "B1-blank": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "canvas_content": "Canvas Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        }
    }
    return defaults.get(layout, defaults["L25"])


def map_content_to_layout(old_content: dict, old_layout: str, new_layout: str) -> dict:
    """
    Attempt to map content from one layout to another.

    Preserves compatible fields when switching between layouts.
    """
    result = {}

    # Title mapping - most layouts have slide_title
    if "slide_title" in old_content:
        result["slide_title"] = old_content["slide_title"]

    # Subtitle mapping for L25
    if "subtitle" in old_content and new_layout == "L25":
        result["subtitle"] = old_content["subtitle"]

    # Content mapping between L25 and L29
    if "rich_content" in old_content and new_layout == "L29":
        # Wrap rich_content in hero container
        result["hero_content"] = f"<div style='padding:40px;'>{old_content['rich_content']}</div>"
    elif "hero_content" in old_content and new_layout == "L25":
        # Use hero_content as rich_content
        result["rich_content"] = old_content["hero_content"]

    # Preserve element fields for flexible layouts
    for i in range(1, 6):
        field = f"element_{i}"
        if field in old_content and new_layout in ["L01", "L02", "L03", "L27"]:
            result[field] = old_content[field]

    return result


app = FastAPI(
    title="v7.5-main: Simplified Layout Builder API",
    description="6-layout system with Text Service creative control",
    version="7.5.0"
)

# Get allowed origins from environment
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for CSS and JS
src_dir = Path(__file__).parent / "src"
if src_dir.exists():
    app.mount("/src", StaticFiles(directory=str(src_dir)), name="src")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "v7.5-main: Simplified Layout Builder API with Content Editing",
        "version": "7.5.0",
        "layouts": {
            "backend": ["L01", "L02", "L03", "L25", "L27", "L29"],
            "frontend": {
                "hero": ["H1-generated", "H1-structured", "H2-section", "H3-closing"],
                "content": ["C1-text", "C3-chart", "C4-infographic", "C5-diagram"],
                "visual": ["V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text"],
                "image": ["I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow"],
                "split": ["S3-two-visuals", "S4-comparison"],
                "blank": ["B1-blank"]
            }
        },
        "philosophy": "Text Service owns content creation, Layout Builder provides structure",
        "features": [
            "Content editing",
            "Version history",
            "Undo/restore capabilities",
            "Derivative elements (presentation-level footer/logo)"
        ],
        "derivative_elements": {
            "description": "Footer and logo that appear consistently across all slides",
            "footer": {
                "template": "Template string with variables: {title}, {page}, {total}, {date}, {author}",
                "values": "Dictionary of variable values",
                "example": "{title} | Page {page} | {date}"
            },
            "logo": {
                "image_url": "URL of logo image to display on all slides"
            }
        },
        "endpoints": {
            "create_presentation": "POST /api/presentations",
            "get_presentation_data": "GET /api/presentations/{id}",
            "update_presentation_metadata": "PUT /api/presentations/{id}",
            "update_slide_content": "PUT /api/presentations/{id}/slides/{slide_index}",
            "add_slide": "POST /api/presentations/{id}/slides",
            "delete_slide": "DELETE /api/presentations/{id}/slides/{slide_index}",
            "reorder_slides": "PUT /api/presentations/{id}/slides/reorder",
            "duplicate_slide": "POST /api/presentations/{id}/slides/{slide_index}/duplicate",
            "change_slide_layout": "PUT /api/presentations/{id}/slides/{slide_index}/layout",
            "regenerate_section": "POST /api/presentations/{id}/regenerate-section",
            "get_version_history": "GET /api/presentations/{id}/versions",
            "restore_version": "POST /api/presentations/{id}/restore/{version_id}",
            "view_presentation": "GET /p/{id}",
            "list_presentations": "GET /api/presentations",
            "delete_presentation": "DELETE /api/presentations/{id}",
            "update_derivative_elements": "PUT /api/presentations/{id}/derivative-elements",
            "api_tester": "GET /tester",
            "docs": "/docs"
        }
    }


@app.post("/api/presentations", response_model=PresentationResponse)
async def create_presentation(request: Presentation):
    """
    Create a new presentation from JSON

    Request body:
    {
        "title": "My Presentation",
        "slides": [
            {
                "layout": "L29",
                "content": {
                    "hero_content": "<div style='...'>Title Slide with Presenter Info</div>"
                }
            },
            {
                "layout": "L25",
                "content": {
                    "slide_title": "Key Points",
                    "subtitle": "Overview",
                    "rich_content": "<div>...</div>"
                }
            },
            {
                "layout": "L29",
                "content": {
                    "hero_content": "<div>...</div>"
                }
            }
        ]
    }

    Returns:
    {
        "id": "uuid",
        "url": "/p/uuid",
        "message": "Presentation created successfully"
    }
    """
    try:
        # Convert request to dict
        presentation_data = request.model_dump()

        # Validate layouts (backend + frontend templates)
        valid_layouts = [
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
        for slide in presentation_data["slides"]:
            if slide["layout"] not in valid_layouts:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid layout '{slide['layout']}'. Valid layouts: {valid_layouts}"
                )
            # Apply defaults when content is empty or missing
            if not slide.get("content"):
                slide["content"] = get_default_content(slide["layout"])

        # Save to storage
        presentation_id = await storage.save(presentation_data)

        # Build response
        return PresentationResponse(
            id=presentation_id,
            url=f"/p/{presentation_id}",
            message=f"Presentation '{request.title}' created successfully"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating presentation: {str(e)}"
        )


@app.get("/api/presentations/{presentation_id}")
async def get_presentation_data(presentation_id: str):
    """Get presentation data by ID"""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        return JSONResponse(content=presentation)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving presentation: {str(e)}")


@app.get("/api/presentations")
async def list_presentations():
    """List all presentations"""
    try:
        presentations = await storage.list_all()
        return JSONResponse(content={
            "count": len(presentations),
            "presentations": presentations
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing presentations: {str(e)}")


@app.delete("/api/presentations/{presentation_id}")
async def delete_presentation(presentation_id: str):
    """Delete a presentation by ID"""
    try:
        success = await storage.delete(presentation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Presentation not found")

        return JSONResponse(content={
            "success": True,
            "message": f"Presentation {presentation_id} deleted"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting presentation: {str(e)}")


@app.put("/api/presentations/{presentation_id}")
async def update_presentation_metadata(
    presentation_id: str,
    update: PresentationMetadataUpdate,
    created_by: str = "user",
    change_summary: str = "Updated presentation metadata"
):
    """
    Update presentation metadata (title, etc.)

    Creates a version backup before updating.

    Query Parameters:
    - created_by: Who is making the update (default: "user")
    - change_summary: Description of changes (default: "Updated presentation metadata")
    """
    try:
        # Get update data (only non-None fields)
        updates = update.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")

        # Update with version tracking
        updated = await storage.update(
            presentation_id,
            updates,
            created_by=created_by,
            change_summary=change_summary,
            create_version=True
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Presentation not found")

        return JSONResponse(content={
            "success": True,
            "message": "Presentation updated successfully",
            "presentation": updated
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating presentation: {str(e)}")


# ==================== Derivative Elements (Presentation-Level Footer/Logo) ====================

@app.put("/api/presentations/{presentation_id}/derivative-elements")
async def update_derivative_elements(
    presentation_id: str,
    derivative_elements: DerivativeElements,
    created_by: str = "user",
    change_summary: str = "Updated derivative elements"
):
    """
    Update presentation-level derivative elements (footer and logo).

    Derivative elements are rendered consistently across all slides:
    - Footer: Uses template with variables like {title}, {page}, {date}
    - Logo: Same image displayed in logo slot on all slides

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the update (default: "user")
    - change_summary: Description of changes

    Request Body (DerivativeElements):
    {
        "footer": {
            "template": "{title} | Page {page} | {date}",
            "values": {
                "title": "Q4 Business Review",
                "date": "December 2024",
                "author": "John Smith"
            },
            "style": {
                "color": "#6b7280",
                "fontSize": "14px"
            }
        },
        "logo": {
            "image_url": "https://storage.example.com/logo.png",
            "alt_text": "Company Logo"
        }
    }

    Footer Template Variables:
    - {title}: Value from footer.values.title
    - {page}: Auto-populated slide number (1-indexed)
    - {total}: Auto-populated total slide count
    - {date}: Value from footer.values.date
    - {author}: Value from footer.values.author

    Returns:
    - success: Boolean
    - derivative_elements: Updated derivative elements configuration
    - message: Status message
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Convert to dict for storage
        derivative_data = derivative_elements.model_dump(exclude_none=True)

        # Update with version tracking
        updated = await storage.update(
            presentation_id,
            {"derivative_elements": derivative_data},
            created_by=created_by,
            change_summary=change_summary,
            create_version=True
        )

        if not updated:
            raise HTTPException(status_code=404, detail="Failed to update presentation")

        return JSONResponse(content={
            "success": True,
            "derivative_elements": updated.get("derivative_elements"),
            "message": "Derivative elements updated successfully"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating derivative elements: {str(e)}")


@app.get("/api/presentations/{presentation_id}/derivative-elements")
async def get_derivative_elements(presentation_id: str):
    """
    Get presentation-level derivative elements (footer and logo).

    Returns the current derivative elements configuration for the presentation.
    If not set, returns null for footer and logo.

    Path Parameters:
    - presentation_id: Presentation UUID

    Returns:
    - derivative_elements: Current configuration (or null if not set)
    - slide_count: Total number of slides (useful for {total} variable)
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        return JSONResponse(content={
            "derivative_elements": presentation.get("derivative_elements"),
            "slide_count": len(presentation.get("slides", []))
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting derivative elements: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/derivative-elements")
async def clear_derivative_elements(
    presentation_id: str,
    created_by: str = "user",
    change_summary: str = "Cleared derivative elements"
):
    """
    Clear all derivative elements from a presentation.

    This removes both footer and logo configuration, reverting to
    per-slide content for these elements.

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Update with version tracking
        updated = await storage.update(
            presentation_id,
            {"derivative_elements": None},
            created_by=created_by,
            change_summary=change_summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Derivative elements cleared"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing derivative elements: {str(e)}")


# ==================== Themes (Presentation Styling) ====================

@app.get("/api/themes")
async def list_themes():
    """
    List all available predefined themes.

    Returns:
    - predefined: List of theme IDs
    - default: Default theme ID
    - themes: Full theme configurations
    """
    return JSONResponse(content={
        "predefined": list(PREDEFINED_THEMES.keys()),
        "default": DEFAULT_THEME_ID,
        "themes": {
            theme_id: theme.model_dump()
            for theme_id, theme in PREDEFINED_THEMES.items()
        }
    })


@app.get("/api/themes/public")
async def list_public_themes():
    """
    List all public themes available in the gallery.

    Returns predefined themes + public user themes.
    Note: This endpoint must be defined before /api/themes/{theme_id}
          to avoid being matched by the parameterized route.
    """
    try:
        # Start with predefined themes
        all_themes = {
            "predefined": [
                {
                    "id": theme_id,
                    "name": theme.name,
                    "description": theme.description,
                    "is_predefined": True,
                    "colors": theme.colors.model_dump()
                }
                for theme_id, theme in PREDEFINED_THEMES.items()
            ],
            "user_public": []
        }

        # Add public user themes if Supabase available and table exists
        if hasattr(storage, 'supabase') and storage.supabase is not None:
            try:
                result = storage.supabase.client.table("ls_user_themes").select(
                    "id, name, description, theme_config, user_id, created_at"
                ).eq("is_public", True).order("created_at", desc=True).execute()

                if result.data:
                    all_themes["user_public"] = [
                        {
                            "id": t["id"],
                            "name": t["name"],
                            "description": t.get("description"),
                            "is_predefined": False,
                            "colors": t["theme_config"].get("colors", {}),
                            "created_at": t["created_at"]
                        }
                        for t in result.data
                    ]
            except Exception as table_error:
                # Table might not exist yet - that's okay, just return predefined themes
                print(f"[ThemeManager] Warning: Could not query user themes table: {table_error}")

        return JSONResponse(content={
            "success": True,
            "predefined_count": len(all_themes["predefined"]),
            "public_count": len(all_themes["user_public"]),
            "themes": all_themes
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing public themes: {str(e)}")


@app.get("/api/themes/{theme_id}")
async def get_theme(theme_id: str):
    """
    Get a specific theme by ID.

    Path Parameters:
    - theme_id: Theme identifier (e.g., "corporate-blue")

    Returns:
    - Full theme configuration including colors, typography, and content styles
    """
    theme = PREDEFINED_THEMES.get(theme_id)
    if not theme:
        raise HTTPException(
            status_code=404,
            detail=f"Theme '{theme_id}' not found. Available themes: {list(PREDEFINED_THEMES.keys())}"
        )
    return JSONResponse(content=theme.model_dump())


@app.get("/api/presentations/{presentation_id}/theme")
async def get_presentation_theme(presentation_id: str):
    """
    Get the current theme configuration for a presentation.

    Path Parameters:
    - presentation_id: Presentation UUID

    Returns:
    - theme_config: Presentation's theme reference and overrides
    - resolved_theme: Full theme with overrides applied
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Get theme config or default
        theme_config = presentation.get("theme_config") or {"theme_id": DEFAULT_THEME_ID}

        # Resolve full theme with overrides
        base_theme = PREDEFINED_THEMES.get(theme_config.get("theme_id", DEFAULT_THEME_ID))
        if not base_theme:
            base_theme = PREDEFINED_THEMES[DEFAULT_THEME_ID]

        resolved_theme = base_theme.model_dump()

        # Apply color overrides if present
        color_overrides = theme_config.get("color_overrides")
        if color_overrides:
            for key, value in color_overrides.items():
                if key in resolved_theme["colors"]:
                    resolved_theme["colors"][key] = value

        return JSONResponse(content={
            "theme_config": theme_config,
            "resolved_theme": resolved_theme
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting presentation theme: {str(e)}")


@app.put("/api/presentations/{presentation_id}/theme")
async def set_presentation_theme(
    presentation_id: str,
    theme_config: PresentationThemeConfig,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Set the theme for a presentation.

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - theme_id: Theme identifier (e.g., "corporate-blue")
    - color_overrides: Optional color overrides (e.g., {"primary": "#ff0000"})

    Example:
    {
        "theme_id": "corporate-blue",
        "color_overrides": {
            "primary": "#2563eb",
            "accent": "#dc2626"
        }
    }
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate theme_id exists
        if theme_config.theme_id not in PREDEFINED_THEMES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid theme_id '{theme_config.theme_id}'. Available themes: {list(PREDEFINED_THEMES.keys())}"
            )

        # Create change summary if not provided
        if not change_summary:
            change_summary = f"Set theme to '{theme_config.theme_id}'"
            if theme_config.color_overrides:
                change_summary += f" with {len(theme_config.color_overrides)} color override(s)"

        # Update presentation with theme config
        updated = await storage.update(
            presentation_id,
            {"theme_config": theme_config.model_dump()},
            created_by=created_by,
            change_summary=change_summary,
            create_version=True
        )

        # Resolve full theme with overrides
        base_theme = PREDEFINED_THEMES[theme_config.theme_id]
        resolved_theme = base_theme.model_dump()

        if theme_config.color_overrides:
            for key, value in theme_config.color_overrides.items():
                if key in resolved_theme["colors"]:
                    resolved_theme["colors"][key] = value

        return JSONResponse(content={
            "success": True,
            "message": f"Theme set to '{theme_config.theme_id}'",
            "theme_config": theme_config.model_dump(),
            "resolved_theme": resolved_theme
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting presentation theme: {str(e)}")


# ==================== User Custom Themes (v7.5.4) ====================

@app.post("/api/user/themes")
async def create_user_theme(
    theme: UserCustomThemeCreate,
    user_id: str = "anonymous"  # In production, this would come from auth
):
    """
    Create a new custom theme for a user.

    Query Parameters:
    - user_id: User identifier (required in production)

    Request Body:
    - name: Theme name (required)
    - description: Optional description
    - base_theme_id: ID of predefined theme to inherit from (optional)
    - colors: Color configuration (required for fully custom themes)
    - typography: Typography configuration (optional)
    - spacing: Spacing configuration (optional)
    - effects: Visual effects configuration (optional)
    - content_styles: Content styles for HTML elements (optional)

    Example - Inherit from predefined:
    {
        "name": "My Corporate Blue",
        "base_theme_id": "corporate-blue",
        "colors": {"primary": "#2563eb", "accent": "#dc2626"}
    }

    Example - Fully custom:
    {
        "name": "Brand Theme",
        "colors": {
            "primary": "#ff5500",
            "background": "#ffffff",
            "text_primary": "#1f2937",
            "hero_background": "#1a1a2e"
        }
    }
    """
    try:
        # Build theme_config JSONB
        theme_config = {}

        # If inheriting from base theme, merge with base
        if theme.base_theme_id:
            if theme.base_theme_id not in PREDEFINED_THEMES:
                raise HTTPException(
                    status_code=400,
                    detail=f"Base theme '{theme.base_theme_id}' not found. Available: {list(PREDEFINED_THEMES.keys())}"
                )
            # Start with base theme config
            base = PREDEFINED_THEMES[theme.base_theme_id]
            theme_config = {
                "colors": base.colors.model_dump(),
                "typography": base.typography,
                "content_styles": base.content_styles
            }

        # Apply provided configurations (override base if present)
        if theme.colors:
            if "colors" in theme_config:
                theme_config["colors"].update(theme.colors.model_dump(exclude_none=True))
            else:
                theme_config["colors"] = theme.colors.model_dump()

        if theme.typography:
            theme_config["typography"] = theme.typography

        if theme.spacing:
            theme_config["spacing"] = theme.spacing.model_dump()

        if theme.effects:
            theme_config["effects"] = theme.effects.model_dump()

        if theme.content_styles:
            theme_config["content_styles"] = theme.content_styles

        # Validate: fully custom themes must have colors
        if not theme.base_theme_id and "colors" not in theme_config:
            raise HTTPException(
                status_code=400,
                detail="Fully custom themes must provide colors configuration"
            )

        # Check if storage supports user themes (Supabase only)
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            # Filesystem fallback - store in memory or return error
            raise HTTPException(
                status_code=501,
                detail="User custom themes require Supabase storage. Currently using filesystem fallback."
            )

        # Insert into ls_user_themes table
        result = storage.supabase.client.table("ls_user_themes").insert({
            "user_id": user_id,
            "name": theme.name,
            "description": theme.description,
            "base_theme_id": theme.base_theme_id,
            "theme_config": theme_config,
            "is_public": False
        }).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create theme")

        created_theme = result.data[0]

        return JSONResponse(content={
            "success": True,
            "message": f"Custom theme '{theme.name}' created",
            "theme": {
                "id": created_theme["id"],
                "user_id": created_theme["user_id"],
                "name": created_theme["name"],
                "description": created_theme.get("description"),
                "base_theme_id": created_theme.get("base_theme_id"),
                "theme_config": created_theme["theme_config"],
                "created_at": created_theme["created_at"],
                "updated_at": created_theme["updated_at"],
                "is_public": created_theme.get("is_public", False)
            }
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating custom theme: {str(e)}")


@app.get("/api/user/themes")
async def list_user_themes(user_id: str = "anonymous"):
    """
    List all custom themes for a user.

    Query Parameters:
    - user_id: User identifier

    Returns:
    - themes: List of user's custom themes
    - count: Number of themes
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            return JSONResponse(content={
                "success": True,
                "themes": [],
                "count": 0,
                "message": "User themes require Supabase storage"
            })

        result = storage.supabase.client.table("ls_user_themes").select("*").eq(
            "user_id", user_id
        ).order("created_at", desc=True).execute()

        themes = result.data or []

        return JSONResponse(content={
            "success": True,
            "themes": themes,
            "count": len(themes)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing user themes: {str(e)}")


@app.get("/api/user/themes/{theme_id}")
async def get_user_theme(theme_id: str, user_id: str = "anonymous"):
    """
    Get a specific user custom theme by ID.

    Path Parameters:
    - theme_id: Theme UUID

    Query Parameters:
    - user_id: User identifier

    Returns:
    - theme: Full theme configuration
    - resolved_theme: Theme with base theme values merged in
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            raise HTTPException(status_code=501, detail="User themes require Supabase storage")

        result = storage.supabase.client.table("ls_user_themes").select("*").eq(
            "id", theme_id
        ).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")

        theme = result.data[0]

        # Check access: user owns it or it's public
        if theme["user_id"] != user_id and not theme.get("is_public", False):
            raise HTTPException(status_code=403, detail="Access denied to this theme")

        # Resolve theme: merge with base if applicable
        resolved_theme = theme["theme_config"].copy()
        if theme.get("base_theme_id"):
            base = PREDEFINED_THEMES.get(theme["base_theme_id"])
            if base:
                # Merge base theme with custom overrides
                base_config = {
                    "colors": base.colors.model_dump(),
                    "typography": base.typography,
                    "content_styles": base.content_styles
                }
                # Deep merge: base values + custom overrides
                for key, value in base_config.items():
                    if key not in resolved_theme:
                        resolved_theme[key] = value
                    elif isinstance(value, dict) and isinstance(resolved_theme.get(key), dict):
                        merged = value.copy()
                        merged.update(resolved_theme[key])
                        resolved_theme[key] = merged

        return JSONResponse(content={
            "success": True,
            "theme": theme,
            "resolved_theme": resolved_theme
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user theme: {str(e)}")


@app.put("/api/user/themes/{theme_id}")
async def update_user_theme(
    theme_id: str,
    update: UserCustomThemeUpdate,
    user_id: str = "anonymous"
):
    """
    Update a user custom theme.

    Path Parameters:
    - theme_id: Theme UUID

    Query Parameters:
    - user_id: User identifier

    Request Body (all optional):
    - name: Updated theme name
    - description: Updated description
    - colors: Updated color configuration
    - typography: Updated typography
    - spacing: Updated spacing
    - effects: Updated effects
    - content_styles: Updated content styles
    - is_public: Make theme public
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            raise HTTPException(status_code=501, detail="User themes require Supabase storage")

        # Verify ownership
        existing = storage.supabase.client.table("ls_user_themes").select("*").eq(
            "id", theme_id
        ).eq("user_id", user_id).execute()

        if not existing.data or len(existing.data) == 0:
            raise HTTPException(status_code=404, detail="Theme not found or access denied")

        current_theme = existing.data[0]

        # Build update payload
        updates = {}

        if update.name is not None:
            updates["name"] = update.name

        if update.description is not None:
            updates["description"] = update.description

        if update.is_public is not None:
            updates["is_public"] = update.is_public

        # Update theme_config if any config fields provided
        theme_config = current_theme["theme_config"].copy()
        config_updated = False

        if update.colors is not None:
            theme_config["colors"] = update.colors.model_dump()
            config_updated = True

        if update.typography is not None:
            theme_config["typography"] = update.typography
            config_updated = True

        if update.spacing is not None:
            theme_config["spacing"] = update.spacing.model_dump()
            config_updated = True

        if update.effects is not None:
            theme_config["effects"] = update.effects.model_dump()
            config_updated = True

        if update.content_styles is not None:
            theme_config["content_styles"] = update.content_styles
            config_updated = True

        if config_updated:
            updates["theme_config"] = theme_config

        if not updates:
            return JSONResponse(content={
                "success": True,
                "message": "No changes provided",
                "theme": current_theme
            })

        # Update in database
        result = storage.supabase.client.table("ls_user_themes").update(
            updates
        ).eq("id", theme_id).execute()

        updated_theme = result.data[0] if result.data else current_theme

        return JSONResponse(content={
            "success": True,
            "message": f"Theme '{updated_theme['name']}' updated",
            "theme": updated_theme
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user theme: {str(e)}")


@app.delete("/api/user/themes/{theme_id}")
async def delete_user_theme(theme_id: str, user_id: str = "anonymous"):
    """
    Delete a user custom theme.

    Path Parameters:
    - theme_id: Theme UUID

    Query Parameters:
    - user_id: User identifier
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            raise HTTPException(status_code=501, detail="User themes require Supabase storage")

        # Delete (RLS will ensure user owns it)
        result = storage.supabase.client.table("ls_user_themes").delete().eq(
            "id", theme_id
        ).eq("user_id", user_id).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Theme not found or access denied")

        return JSONResponse(content={
            "success": True,
            "message": "Theme deleted"
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user theme: {str(e)}")


@app.post("/api/user/themes/{theme_id}/duplicate")
async def duplicate_user_theme(
    theme_id: str,
    user_id: str = "anonymous",
    new_name: str = None
):
    """
    Duplicate an existing theme (own or public).

    Path Parameters:
    - theme_id: Theme UUID to duplicate

    Query Parameters:
    - user_id: User identifier
    - new_name: Name for the duplicated theme (optional)
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            raise HTTPException(status_code=501, detail="User themes require Supabase storage")

        # Get source theme
        result = storage.supabase.client.table("ls_user_themes").select("*").eq(
            "id", theme_id
        ).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Theme not found")

        source = result.data[0]

        # Check access: user owns it or it's public
        if source["user_id"] != user_id and not source.get("is_public", False):
            raise HTTPException(status_code=403, detail="Access denied to this theme")

        # Create duplicate
        duplicate_name = new_name or f"{source['name']} (Copy)"

        new_result = storage.supabase.client.table("ls_user_themes").insert({
            "user_id": user_id,
            "name": duplicate_name,
            "description": source.get("description"),
            "base_theme_id": source.get("base_theme_id"),
            "theme_config": source["theme_config"],
            "is_public": False
        }).execute()

        new_theme = new_result.data[0]

        return JSONResponse(content={
            "success": True,
            "message": f"Theme duplicated as '{duplicate_name}'",
            "theme": new_theme
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error duplicating theme: {str(e)}")


@app.post("/api/user/themes/{theme_id}/publish")
async def publish_user_theme(theme_id: str, user_id: str = "anonymous"):
    """
    Make a user theme public in the gallery.

    Path Parameters:
    - theme_id: Theme UUID

    Query Parameters:
    - user_id: User identifier
    """
    try:
        if not hasattr(storage, 'supabase') or storage.supabase is None:
            raise HTTPException(status_code=501, detail="User themes require Supabase storage")

        result = storage.supabase.client.table("ls_user_themes").update({
            "is_public": True
        }).eq("id", theme_id).eq("user_id", user_id).execute()

        if not result.data or len(result.data) == 0:
            raise HTTPException(status_code=404, detail="Theme not found or access denied")

        return JSONResponse(content={
            "success": True,
            "message": "Theme is now public",
            "theme": result.data[0]
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing theme: {str(e)}")


@app.get("/api/presentations/{presentation_id}/theme/css-variables")
async def get_presentation_theme_css_variables(presentation_id: str):
    """
    Get CSS variables for a presentation's theme.

    Returns all CSS custom properties that should be injected into :root
    for the presentation's theme to take effect.

    Path Parameters:
    - presentation_id: Presentation UUID

    Returns:
    - css_variables: Dictionary of CSS variable name -> value
    - css_string: Ready-to-inject CSS string
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Get theme config
        theme_config = presentation.get("theme_config") or {"theme_id": DEFAULT_THEME_ID}
        theme_id = theme_config.get("theme_id", DEFAULT_THEME_ID)
        is_custom = theme_config.get("is_custom", False)

        # Get base theme
        if is_custom and hasattr(storage, 'supabase') and storage.supabase:
            # Load custom theme from database
            result = storage.supabase.client.table("ls_user_themes").select("*").eq(
                "id", theme_id
            ).execute()
            if result.data:
                custom_theme = result.data[0]
                resolved_config = custom_theme["theme_config"]
                # Merge with base if applicable
                if custom_theme.get("base_theme_id"):
                    base = PREDEFINED_THEMES.get(custom_theme["base_theme_id"])
                    if base:
                        base_config = {
                            "colors": base.colors.model_dump(),
                            "typography": base.typography
                        }
                        for key, value in base_config.items():
                            if key not in resolved_config:
                                resolved_config[key] = value
            else:
                # Fallback to predefined
                base_theme = PREDEFINED_THEMES.get(DEFAULT_THEME_ID)
                resolved_config = {
                    "colors": base_theme.colors.model_dump(),
                    "typography": base_theme.typography
                }
        else:
            base_theme = PREDEFINED_THEMES.get(theme_id, PREDEFINED_THEMES[DEFAULT_THEME_ID])
            resolved_config = {
                "colors": base_theme.colors.model_dump(),
                "typography": base_theme.typography,
                "spacing": base_theme.spacing.model_dump() if base_theme.spacing else None,
                "effects": base_theme.effects.model_dump() if base_theme.effects else None
            }

        # Apply overrides
        overrides = theme_config.get("overrides") or {}
        legacy_color_overrides = theme_config.get("color_overrides")

        # Handle legacy color_overrides
        if legacy_color_overrides and not overrides.get("colors"):
            overrides["colors"] = legacy_color_overrides

        # Apply color overrides
        if overrides.get("colors"):
            for key, value in overrides["colors"].items():
                if "colors" in resolved_config and key in resolved_config["colors"]:
                    resolved_config["colors"][key] = value

        # Apply typography overrides
        if overrides.get("typography"):
            if "typography" not in resolved_config:
                resolved_config["typography"] = {}
            resolved_config["typography"].update(overrides["typography"])

        # Apply spacing overrides
        if overrides.get("spacing"):
            if "spacing" not in resolved_config:
                resolved_config["spacing"] = {}
            resolved_config["spacing"].update(overrides["spacing"])

        # Apply effects overrides
        if overrides.get("effects"):
            if "effects" not in resolved_config:
                resolved_config["effects"] = {}
            resolved_config["effects"].update(overrides["effects"])

        # Build CSS variables
        css_variables = {}
        colors = resolved_config.get("colors", {})

        # Color variables
        color_mapping = {
            "primary": "--theme-primary",
            "primary_light": "--theme-primary-light",
            "primary_dark": "--theme-primary-dark",
            "accent": "--theme-accent",
            "background": "--theme-bg",
            "background_alt": "--theme-bg-alt",
            "text_primary": "--theme-text-primary",
            "text_secondary": "--theme-text-secondary",
            "text_body": "--theme-text-body",
            "hero_text_primary": "--theme-hero-text-primary",
            "hero_text_secondary": "--theme-hero-text-secondary",
            "hero_background": "--theme-hero-bg",
            "footer_text": "--theme-footer-text",
            "border": "--theme-border"
        }

        for color_key, css_var in color_mapping.items():
            if color_key in colors and colors[color_key]:
                css_variables[css_var] = colors[color_key]

        # Typography variables
        typography = resolved_config.get("typography") or {}
        if typography:
            if typography.get("fontFamily"):
                css_variables["--theme-font-family"] = typography["fontFamily"]
            # Standard profile
            standard = typography.get("standard", {})
            if standard.get("title", {}).get("fontSize"):
                css_variables["--theme-title-size"] = standard["title"]["fontSize"]
            if standard.get("title", {}).get("fontWeight"):
                css_variables["--theme-title-weight"] = standard["title"]["fontWeight"]
            if standard.get("subtitle", {}).get("fontSize"):
                css_variables["--theme-subtitle-size"] = standard["subtitle"]["fontSize"]
            if standard.get("body", {}).get("fontSize"):
                css_variables["--theme-body-size"] = standard["body"]["fontSize"]
            if standard.get("footer", {}).get("fontSize"):
                css_variables["--theme-footer-size"] = standard["footer"]["fontSize"]
            # Hero profile
            hero = typography.get("hero", {})
            if hero.get("title", {}).get("fontSize"):
                css_variables["--theme-hero-title-size"] = hero["title"]["fontSize"]
            if hero.get("title", {}).get("fontWeight"):
                css_variables["--theme-hero-title-weight"] = hero["title"]["fontWeight"]
            if hero.get("subtitle", {}).get("fontSize"):
                css_variables["--theme-hero-subtitle-size"] = hero["subtitle"]["fontSize"]

        # Spacing variables
        spacing = resolved_config.get("spacing") or {}
        if spacing:
            if spacing.get("slide_padding"):
                css_variables["--theme-slide-padding"] = spacing["slide_padding"]
            if spacing.get("element_gap"):
                css_variables["--theme-element-gap"] = spacing["element_gap"]
            if spacing.get("section_gap"):
                css_variables["--theme-section-gap"] = spacing["section_gap"]

        # Effects variables
        effects = resolved_config.get("effects") or {}
        if effects:
            if effects.get("border_radius"):
                css_variables["--theme-border-radius"] = effects["border_radius"]
            if effects.get("shadow_small"):
                css_variables["--theme-shadow-small"] = effects["shadow_small"]
            if effects.get("shadow_medium"):
                css_variables["--theme-shadow-medium"] = effects["shadow_medium"]
            if effects.get("shadow_large"):
                css_variables["--theme-shadow-large"] = effects["shadow_large"]

        # Build CSS string
        css_lines = [f"  {var}: {value};" for var, value in css_variables.items()]
        css_string = ":root {\n" + "\n".join(css_lines) + "\n}"

        return JSONResponse(content={
            "success": True,
            "css_variables": css_variables,
            "css_string": css_string,
            "theme_id": theme_id,
            "is_custom": is_custom
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting theme CSS variables: {str(e)}")


# ==================== Reorder Slides (must come before {slide_index} routes) ====================

@app.put("/api/presentations/{presentation_id}/slides/reorder")
async def reorder_slides(
    presentation_id: str,
    request: ReorderSlidesRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Move a slide from one position to another.

    Creates a version backup before reordering.

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - from_index: Current position of the slide (0-based)
    - to_index: New position for the slide (0-based)
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        slides = presentation["slides"]
        slide_count = len(slides)

        # Validate indices
        if request.from_index < 0 or request.from_index >= slide_count:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid from_index {request.from_index}. Valid range: 0-{slide_count - 1}"
            )
        if request.to_index < 0 or request.to_index >= slide_count:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid to_index {request.to_index}. Valid range: 0-{slide_count - 1}"
            )

        # No change needed if same position
        if request.from_index == request.to_index:
            return JSONResponse(content={
                "success": True,
                "message": "Slide is already at the requested position",
                "slide_order": [s["layout"] for s in slides]
            })

        # Move the slide
        slide = slides.pop(request.from_index)
        slides.insert(request.to_index, slide)

        # Save with version tracking
        summary = change_summary or f"Moved slide from position {request.from_index + 1} to {request.to_index + 1}"
        updated = await storage.update(
            presentation_id,
            {"slides": slides},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide moved from position {request.from_index + 1} to {request.to_index + 1}",
            "slide_order": [s["layout"] for s in updated["slides"]]
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reordering slides: {str(e)}")


# ==================== Update Slide Content ====================

@app.put("/api/presentations/{presentation_id}/slides/{slide_index}")
async def update_slide_content(
    presentation_id: str,
    slide_index: int,
    update: SlideContentUpdate,
    created_by: str = "user",
    change_summary: str = "Updated slide content"
):
    """
    Update content of a specific slide

    Creates a version backup before updating.

    Path Parameters:
    - presentation_id: Presentation UUID
    - slide_index: Zero-based slide index

    Query Parameters:
    - created_by: Who is making the update (default: "user")
    - change_summary: Description of changes (default: "Updated slide content")

    Request Body: SlideContentUpdate with optional fields to update
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {slide_index}. Presentation has {len(presentation['slides'])} slides"
            )

        # Get update data (only non-None fields)
        updates = update.model_dump(exclude_unset=True)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")

        # Handle text_boxes separately - they go at slide level, not in content
        if "text_boxes" in updates:
            text_boxes_data = updates.pop("text_boxes")
            presentation["slides"][slide_index]["text_boxes"] = text_boxes_data

        # Update slide content (remaining fields)
        if updates:
            presentation["slides"][slide_index]["content"].update(updates)

        # Save with version tracking
        updated = await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=change_summary or f"Updated slide {slide_index + 1}",
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide {slide_index + 1} updated successfully",
            "slide": updated["slides"][slide_index]
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating slide: {str(e)}")


# ==================== Batch Update All Slides (Auto-Save) ====================

@app.put("/api/presentations/{presentation_id}/slides")
async def update_all_slides(
    presentation_id: str,
    request: Request
):
    """
    Batch update multiple slides (for auto-save from editor).

    This endpoint accepts an array of slide updates and applies them all at once,
    which is more efficient than calling the individual slide endpoint multiple times.

    Request Body:
    {
        "slides": [
            { "slide_title": "...", "text_boxes": [...], ... },
            { "rich_content": "...", ... },
            ...
        ],
        "updated_by": "user",
        "change_summary": "Auto-save from editor"
    }
    """
    try:
        data = await request.json()
        slides_data = data.get("slides", [])
        updated_by = data.get("updated_by", "user")
        change_summary = data.get("change_summary", "Auto-save")

        if not slides_data:
            raise HTTPException(status_code=400, detail="No slides data provided")

        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Update each slide
        slides_updated = 0
        for i, slide_update in enumerate(slides_data):
            if i < len(presentation["slides"]):
                # Handle element types at slide level (not in content)
                # Text boxes
                if "text_boxes" in slide_update:
                    presentation["slides"][i]["text_boxes"] = slide_update.pop("text_boxes")

                # Images
                if "images" in slide_update:
                    presentation["slides"][i]["images"] = slide_update.pop("images")

                # Charts
                if "charts" in slide_update:
                    presentation["slides"][i]["charts"] = slide_update.pop("charts")

                # Infographics
                if "infographics" in slide_update:
                    presentation["slides"][i]["infographics"] = slide_update.pop("infographics")

                # Diagrams
                if "diagrams" in slide_update:
                    presentation["slides"][i]["diagrams"] = slide_update.pop("diagrams")

                # Handle content fields
                for key, value in slide_update.items():
                    if value is not None:
                        presentation["slides"][i]["content"][key] = value

                slides_updated += 1

        # Save with version tracking
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=updated_by,
            change_summary=change_summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Updated {slides_updated} slides",
            "slides_updated": slides_updated
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error batch updating slides: {str(e)}")


@app.get("/api/presentations/{presentation_id}/versions", response_model=VersionHistoryResponse)
async def get_version_history(presentation_id: str):
    """
    Get version history for a presentation

    Returns list of all versions with metadata.
    """
    try:
        # Check if presentation exists
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Get version history
        history = await storage.get_version_history(presentation_id)

        if not history:
            # No versions yet - return empty history
            return VersionHistoryResponse(
                presentation_id=presentation_id,
                current_version_id=presentation.get("version_id", "current"),
                versions=[]
            )

        # Convert to response model
        versions = [
            VersionMetadata(
                version_id=v["version_id"],
                created_at=v["created_at"],
                created_by=v["created_by"],
                change_summary=v.get("change_summary"),
                presentation_id=presentation_id
            )
            for v in history.get("versions", [])
        ]

        return VersionHistoryResponse(
            presentation_id=presentation_id,
            current_version_id=presentation.get("version_id", "current"),
            versions=versions
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving version history: {str(e)}")


@app.post("/api/presentations/{presentation_id}/restore/{version_id}")
async def restore_version(
    presentation_id: str,
    version_id: str,
    request: RestoreVersionRequest = RestoreVersionRequest(create_backup=True)
):
    """
    Restore a presentation to a specific version

    Path Parameters:
    - presentation_id: Presentation UUID
    - version_id: Version ID to restore

    Request Body:
    - create_backup: Whether to backup current state before restoring (default: true)
    """
    try:
        # Check if presentation exists
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Restore version
        restored = await storage.restore_version(
            presentation_id,
            version_id,
            create_backup=request.create_backup
        )

        if not restored:
            raise HTTPException(
                status_code=404,
                detail=f"Version {version_id} not found for presentation {presentation_id}"
            )

        return JSONResponse(content={
            "success": True,
            "message": f"Presentation restored to version {version_id}",
            "presentation": restored
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error restoring version: {str(e)}")


# ==================== Ghost Element Cleanup (v7.5.1) ====================

def is_element_valid_for_slide(element: dict, slide_id: str, slide_index: int) -> bool:
    """
    Check if an element belongs to this slide (supports both old and new ID formats).

    New format: Uses parent_slide_id field AND UUID-based element IDs
    Old format: Uses index-based ID like 'slide-{N}-{slotName}'

    IMPORTANT: For old-format IDs (slide-{N}-*), we ALWAYS check the index
    even if parent_slide_id is set, because migration may have incorrectly
    set parent_slide_id on ghost elements.

    Returns True if element is valid for this slide.
    """
    element_id = element.get('id', '')
    parent_id = element.get('parent_slide_id')

    # Check old-format IDs FIRST (slide-{N}-{slotName})
    # These are the source of ghost elements - index must match!
    if element_id.startswith('slide-'):
        parts = element_id.split('-')
        if len(parts) >= 2 and parts[1].isdigit():
            element_slide_index = int(parts[1])
            # Ghost element if index doesn't match current slide
            return element_slide_index == slide_index

    # New UUID format: check parent_slide_id
    # Format: {slide_id}_{type}_{uuid} or just UUID-based
    if parent_id:
        return parent_id == slide_id

    # Unknown format or legacy element without parent reference
    # Keep by default for backward compatibility
    return True


@app.post("/api/presentations/{presentation_id}/cleanup-orphans")
async def cleanup_orphan_elements(presentation_id: str):
    """
    Remove orphaned elements from a corrupted presentation.

    This endpoint fixes the "ghost elements" problem where elements from
    deleted slides appear on other slides due to index-based ID corruption.

    What it does:
    1. Ensures all slides have a slide_id
    2. Removes elements with parent_slide_id not matching any slide
    3. Removes elements with old index-based IDs that don't match current slide
    4. Logs all removed elements for audit

    Returns:
    - success: Whether cleanup succeeded
    - removed_elements: Number of orphaned elements removed
    - details: Breakdown by element type and slide
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        removed_count = 0
        details = {"slides": []}

        # Process each slide
        for slide_index, slide in enumerate(presentation.get('slides', [])):
            slide_details = {
                "slide_index": slide_index,
                "slide_id": slide.get('slide_id'),
                "removed": {}
            }

            # Ensure slide has a slide_id (migration for old presentations)
            if not slide.get('slide_id'):
                from uuid import uuid4
                slide['slide_id'] = f"slide_{uuid4().hex[:12]}"
                slide_details["slide_id"] = slide['slide_id']
                slide_details["generated_slide_id"] = True

            slide_id = slide['slide_id']

            # Clean each element type
            for element_type in ['text_boxes', 'images', 'charts', 'infographics', 'diagrams', 'contents']:
                original_elements = slide.get(element_type, [])
                original_count = len(original_elements)

                # Filter to only valid elements
                valid_elements = [
                    el for el in original_elements
                    if is_element_valid_for_slide(el, slide_id, slide_index)
                ]

                # Track removed elements
                removed = original_count - len(valid_elements)
                if removed > 0:
                    slide_details["removed"][element_type] = removed
                    removed_count += removed

                    # Log removed element IDs for debugging
                    removed_ids = [
                        el.get('id') for el in original_elements
                        if not is_element_valid_for_slide(el, slide_id, slide_index)
                    ]
                    print(f"[Cleanup] Slide {slide_index} ({slide_id}): Removed {removed} {element_type}: {removed_ids}")

                # Update slide with cleaned elements
                slide[element_type] = valid_elements

            if slide_details["removed"]:
                details["slides"].append(slide_details)

        # Save cleaned presentation if changes were made
        if removed_count > 0:
            await storage.update(presentation_id, presentation, {
                "change_summary": f"Cleanup: removed {removed_count} orphaned elements",
                "updated_by": "cleanup_service"
            })

        return {
            "success": True,
            "removed_elements": removed_count,
            "details": details,
            "message": f"Removed {removed_count} orphaned elements" if removed_count > 0 else "No orphaned elements found"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during cleanup: {str(e)}")


@app.post("/api/presentations/{presentation_id}/regenerate-section", response_model=SectionRegenerationResponse)
async def regenerate_section(
    presentation_id: str,
    request: SectionRegenerationRequest
):
    """
    Regenerate a specific section within a slide using AI.

    Part of Phase 2: World-Class Editor with AI-Powered Regeneration.

    This endpoint allows users to select specific sections within slides
    and request AI to regenerate them with custom instructions.

    Path Parameters:
    - presentation_id: Presentation UUID

    Request Body:
    - slide_index: Zero-based slide index
    - section_id: Unique section ID (e.g., 'slide-0-section-title')
    - section_type: Type of section (title, subtitle, body, etc.)
    - user_instruction: How to regenerate the section
    - current_content: Current HTML content of the section
    - layout: Layout type (L01, L02, L03, L25, L27, L29)

    Returns:
    - success: Whether regeneration succeeded
    - updated_content: New HTML content for the section
    - section_id: ID of the regenerated section
    - message: Success or error message

    Note: Phase 2 uses mock AI regeneration for testing.
          Phase 3 will integrate with Director Service for real AI regeneration.
    """
    try:
        # Validate presentation exists
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if request.slide_index < 0 or request.slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {request.slide_index}. Presentation has {len(presentation['slides'])} slides"
            )

        # Phase 2: Mock AI Regeneration (for testing without Director Service)
        # In Phase 3, this will call Director Service API
        import time
        processing_start = time.time()

        # Mock regeneration: Add AI-enhanced indicator to demonstrate functionality
        mock_enhanced_content = f"""<div class="ai-enhanced">
{request.current_content}
<div style="font-size: 11px; color: #10b981; margin-top: 8px; font-style: italic;">
✨ Enhanced with AI: "{request.user_instruction}"
</div>
</div>"""

        processing_time = time.time() - processing_start

        # Return regenerated content
        return SectionRegenerationResponse(
            success=True,
            updated_content=mock_enhanced_content,
            section_id=request.section_id,
            section_type=request.section_type,
            message=f"Section regenerated successfully (mock)",
            regeneration_metadata={
                "processing_time_ms": round(processing_time * 1000, 2),
                "ai_model": "mock-v1 (Phase 2 testing)",
                "user_instruction": request.user_instruction,
                "layout": request.layout
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error regenerating section: {str(e)}"
        )


# ==================== Slide CRUD Operations ====================

# IMPORTANT: Bulk delete must be defined BEFORE single delete
# because "/slides/bulk" would otherwise match "/slides/{slide_index}"
@app.delete("/api/presentations/{presentation_id}/slides/bulk")
async def delete_slides_bulk(
    presentation_id: str,
    request: BulkDeleteSlidesRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Delete multiple slides at once from a presentation.

    Supports both sequential ranges (e.g., slides 3-7) and scattered indices (e.g., slides 2, 5, 9).
    Creates a single version backup before deletion.
    Must leave at least 1 slide remaining.

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - indices: List of 0-based slide indices to delete (can be in any order)

    Returns:
    - success: Boolean
    - message: Status message
    - deleted_count: Number of slides deleted
    - deleted_indices: List of indices that were deleted (sorted)
    - remaining_slide_count: Number of slides remaining
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        slides = presentation.get("slides", [])
        total_slides = len(slides)

        # Remove duplicates and sort indices
        unique_indices = list(set(request.indices))

        # Validate: at least one index provided
        if not unique_indices:
            raise HTTPException(status_code=400, detail="At least one slide index is required")

        # Validate: all indices are within range
        invalid_indices = [i for i in unique_indices if i < 0 or i >= total_slides]
        if invalid_indices:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide indices: {invalid_indices}. Valid range: 0-{total_slides - 1}"
            )

        # Validate: must leave at least 1 slide
        if len(unique_indices) >= total_slides:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete all slides. Presentation has {total_slides} slides and you're trying to delete {len(unique_indices)}. At least 1 slide must remain."
            )

        # Sort indices in DESCENDING order to delete from end first
        # This preserves valid indices during iteration
        sorted_indices_desc = sorted(unique_indices, reverse=True)

        # Collect deleted slides for response
        deleted_slides = []
        for idx in sorted_indices_desc:
            deleted_slides.append(slides.pop(idx))

        # Clean up ghost elements from remaining slides (v7.5.1)
        # After deletion, slides shift down but element IDs don't update
        ghost_count = 0
        for idx, slide in enumerate(slides):
            slide_id = slide.get('slide_id', '')
            for element_type in ['text_boxes', 'images', 'charts', 'infographics', 'diagrams', 'contents']:
                if element_type in slide and slide[element_type]:
                    original_count = len(slide[element_type])
                    slide[element_type] = [
                        el for el in slide[element_type]
                        if is_element_valid_for_slide(el, slide_id, idx)
                    ]
                    ghost_count += original_count - len(slide[element_type])

        if ghost_count > 0:
            logger.info(f"Cleaned {ghost_count} ghost elements after bulk slide deletion",
                       presentation_id=presentation_id, deleted_indices=sorted(unique_indices))

        # Save with version tracking
        summary = change_summary or f"Bulk deleted {len(unique_indices)} slides: indices {sorted(unique_indices)}"
        updated = await storage.update(
            presentation_id,
            {"slides": slides},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"{len(unique_indices)} slide(s) deleted successfully",
            "deleted_count": len(unique_indices),
            "deleted_indices": sorted(unique_indices),
            "remaining_slide_count": len(updated["slides"])
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error bulk deleting slides: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}")
async def delete_slide(
    presentation_id: str,
    slide_index: int,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Delete a slide at a specific index.

    Creates a version backup before deleting.
    Cannot delete the last remaining slide.

    Path Parameters:
    - presentation_id: Presentation UUID
    - slide_index: Zero-based slide index to delete

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {slide_index}. Presentation has {len(presentation['slides'])} slides"
            )

        # Prevent deleting the last slide
        if len(presentation["slides"]) <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete the only slide. A presentation must have at least one slide."
            )

        # Remove the slide
        deleted_slide = presentation["slides"].pop(slide_index)

        # Clean up ghost elements from remaining slides (v7.5.1)
        # After deletion, slides shift down but element IDs don't update
        # e.g., slide-6-title on what is now slide 5 is a ghost element
        ghost_count = 0
        for idx, slide in enumerate(presentation["slides"]):
            slide_id = slide.get('slide_id', '')
            for element_type in ['text_boxes', 'images', 'charts', 'infographics', 'diagrams', 'contents']:
                if element_type in slide and slide[element_type]:
                    original_count = len(slide[element_type])
                    slide[element_type] = [
                        el for el in slide[element_type]
                        if is_element_valid_for_slide(el, slide_id, idx)
                    ]
                    ghost_count += original_count - len(slide[element_type])

        if ghost_count > 0:
            logger.info(f"Cleaned {ghost_count} ghost elements after slide deletion",
                       presentation_id=presentation_id, deleted_slide_index=slide_index)

        # Save with version tracking
        summary = change_summary or f"Deleted slide {slide_index + 1}"
        updated = await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide {slide_index + 1} deleted successfully",
            "slide_count": len(updated["slides"]),
            "deleted_slide": deleted_slide
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting slide: {str(e)}")


@app.post("/api/presentations/{presentation_id}/slides")
async def add_slide(
    presentation_id: str,
    request: AddSlideRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Add a new slide to a presentation.

    Creates a version backup before adding.
    The slide is inserted at the specified position, or appended at the end.

    Path Parameters:
    - presentation_id: Presentation UUID

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - layout: Layout type (L01, L02, L03, L25, L27, L29)
    - position: Where to insert (optional, defaults to end)
    - content: Initial content (optional, uses defaults)
    - background_color: Background color (optional)
    - background_image: Background image (optional)
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate layout (backend + frontend templates)
        valid_layouts = [
            "L01", "L02", "L03", "L25", "L27", "L29",
            "H1-generated", "H1-structured", "H2-section", "H3-closing",
            "C1-text", "C3-chart", "C4-infographic", "C5-diagram",
            "V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text",
            "I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow",
            "S3-two-visuals", "S4-comparison",
            "B1-blank"
        ]
        if request.layout not in valid_layouts:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid layout '{request.layout}'. Valid layouts: {valid_layouts}"
            )

        # Create new slide with default or provided content
        content = request.content if request.content else get_default_content(request.layout)
        new_slide = {
            "layout": request.layout,
            "content": content
        }

        # Add optional background fields
        if request.background_color:
            new_slide["background_color"] = request.background_color
        if request.background_image:
            new_slide["background_image"] = request.background_image

        # Determine insert position
        position = request.position
        if position is None or position >= len(presentation["slides"]):
            position = len(presentation["slides"])
            presentation["slides"].append(new_slide)
        else:
            position = max(0, position)
            presentation["slides"].insert(position, new_slide)

        # Save with version tracking
        summary = change_summary or f"Added {request.layout} slide at position {position + 1}"
        updated = await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide added at position {position + 1}",
            "slide_index": position,
            "slide": new_slide,
            "slide_count": len(updated["slides"])
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding slide: {str(e)}")


# ==================== Duplicate Slide ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/duplicate")
async def duplicate_slide(
    presentation_id: str,
    slide_index: int,
    request: DuplicateSlideRequest = DuplicateSlideRequest(),
    created_by: str = "user",
    change_summary: str = None
):
    """
    Duplicate a slide.

    Creates a version backup before duplicating.
    The duplicate is inserted after the source slide by default.

    Path Parameters:
    - presentation_id: Presentation UUID
    - slide_index: Index of slide to duplicate (0-based)

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - insert_after: If True, insert after source. If False, insert before. (default: True)
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {slide_index}. Presentation has {len(presentation['slides'])} slides"
            )

        # Deep copy the slide
        duplicated = copy.deepcopy(presentation["slides"][slide_index])

        # Determine insert position
        new_index = slide_index + 1 if request.insert_after else slide_index
        presentation["slides"].insert(new_index, duplicated)

        # Save with version tracking
        summary = change_summary or f"Duplicated slide {slide_index + 1}"
        updated = await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide {slide_index + 1} duplicated at position {new_index + 1}",
            "new_slide_index": new_index,
            "slide": duplicated,
            "slide_count": len(updated["slides"])
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error duplicating slide: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/layout")
async def change_slide_layout(
    presentation_id: str,
    slide_index: int,
    request: ChangeLayoutRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Change the layout of a slide.

    Creates a version backup before changing.
    Optionally preserves compatible content fields.

    Path Parameters:
    - presentation_id: Presentation UUID
    - slide_index: Index of slide to modify (0-based)

    Query Parameters:
    - created_by: Who is making the change (default: "user")
    - change_summary: Description of change

    Request Body:
    - new_layout: New layout type (L01, L02, L03, L25, L27, L29)
    - preserve_content: Attempt to preserve compatible fields (default: True)
    - content_mapping: Manual field mapping {'old_field': 'new_field'}
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {slide_index}. Presentation has {len(presentation['slides'])} slides"
            )

        # Validate new layout (backend + frontend templates)
        valid_layouts = [
            "L01", "L02", "L03", "L25", "L27", "L29",
            "H1-generated", "H1-structured", "H2-section", "H3-closing",
            "C1-text", "C3-chart", "C4-infographic", "C5-diagram",
            "V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text",
            "I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow",
            "S3-two-visuals", "S4-comparison",
            "B1-blank"
        ]
        if request.new_layout not in valid_layouts:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid layout '{request.new_layout}'. Valid layouts: {valid_layouts}"
            )

        old_layout = presentation["slides"][slide_index]["layout"]
        old_content = presentation["slides"][slide_index]["content"]

        # No change needed if same layout
        if old_layout == request.new_layout:
            return JSONResponse(content={
                "success": True,
                "message": f"Slide is already using layout {request.new_layout}",
                "slide": presentation["slides"][slide_index]
            })

        # Map content if preserving
        new_content = {}
        if request.preserve_content:
            new_content = map_content_to_layout(old_content, old_layout, request.new_layout)

        # Apply manual content mapping if provided
        if request.content_mapping:
            for old_field, new_field in request.content_mapping.items():
                if old_field in old_content:
                    new_content[new_field] = old_content[old_field]

        # Merge with defaults for any missing required fields
        default_content = get_default_content(request.new_layout)
        for key, value in default_content.items():
            if key not in new_content:
                new_content[key] = value

        # Update the slide
        presentation["slides"][slide_index]["layout"] = request.new_layout
        presentation["slides"][slide_index]["content"] = new_content

        # Save with version tracking
        summary = change_summary or f"Changed slide {slide_index + 1} from {old_layout} to {request.new_layout}"
        updated = await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Slide layout changed from {old_layout} to {request.new_layout}",
            "slide": updated["slides"][slide_index]
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error changing slide layout: {str(e)}")


# ==================== Text Box CRUD Endpoints ====================

def ensure_slide_elements(slide_data: dict) -> dict:
    """
    Ensure slide data has all element arrays for backward compatibility.
    Called when loading presentations created before these features.
    """
    if 'text_boxes' not in slide_data:
        slide_data['text_boxes'] = []
    if 'images' not in slide_data:
        slide_data['images'] = []
    if 'charts' not in slide_data:
        slide_data['charts'] = []
    if 'infographics' not in slide_data:
        slide_data['infographics'] = []
    if 'diagrams' not in slide_data:
        slide_data['diagrams'] = []
    return slide_data


# Backward compatibility alias
def ensure_slide_text_boxes(slide_data: dict) -> dict:
    """Backward compatibility alias for ensure_slide_elements."""
    return ensure_slide_elements(slide_data)


def get_next_textbox_z_index(text_boxes: list) -> int:
    """Get the next available z-index for a new text box."""
    if not text_boxes:
        return 1000  # Base z-index for text boxes
    max_z = max(tb.get('z_index', 1000) for tb in text_boxes)
    return max_z + 1


@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/textboxes", response_model=TextBoxResponse)
async def create_text_box(
    presentation_id: str,
    slide_index: int,
    request: TextBoxCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Create a new text box on a slide.

    Text boxes are overlay elements that float above the main layout content.
    They support rich HTML content and can be positioned anywhere on the slide.
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        # Ensure text_boxes array exists (backward compatibility)
        presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
        text_boxes = presentation["slides"][slide_index]["text_boxes"]

        # Check limit
        if len(text_boxes) >= 20:
            raise HTTPException(status_code=400, detail="Maximum 20 text boxes per slide")

        # Create new text box
        new_textbox = TextBox(
            position=request.position,
            content=request.content or "",
            style=request.style or TextBoxStyle(),
            z_index=request.z_index or get_next_textbox_z_index(text_boxes)
        )

        # Add to slide
        text_boxes.append(new_textbox.model_dump())

        # Save with version tracking
        summary = change_summary or f"Added text box to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return TextBoxResponse(
            success=True,
            text_box=new_textbox,
            message=f"Text box created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating text box: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/textboxes", response_model=TextBoxListResponse)
async def list_text_boxes(presentation_id: str, slide_index: int):
    """Get all text boxes on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        # Ensure text_boxes exists
        slide = ensure_slide_text_boxes(presentation["slides"][slide_index])
        text_boxes = slide.get("text_boxes", [])

        return TextBoxListResponse(
            success=True,
            slide_index=slide_index,
            text_boxes=[TextBox(**tb) for tb in text_boxes],
            count=len(text_boxes)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing text boxes: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/textboxes/{textbox_id}", response_model=TextBoxResponse)
async def update_text_box(
    presentation_id: str,
    slide_index: int,
    textbox_id: str,
    request: TextBoxUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """
    Update an existing text box.

    Only provided fields will be updated; others remain unchanged.
    """
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        # Ensure text_boxes exists
        presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
        text_boxes = presentation["slides"][slide_index]["text_boxes"]

        # Find the text box
        textbox_idx = None
        for idx, tb in enumerate(text_boxes):
            if tb.get("id") == textbox_id:
                textbox_idx = idx
                break

        if textbox_idx is None:
            raise HTTPException(status_code=404, detail=f"Text box not found: {textbox_id}")

        # Update fields
        current_tb = text_boxes[textbox_idx]
        update_data = request.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    current_tb["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                elif key == "style":
                    current_tb["style"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    current_tb[key] = value

        # Save with version tracking
        summary = change_summary or f"Updated text box on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return TextBoxResponse(
            success=True,
            text_box=TextBox(**current_tb),
            message=f"Text box updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating text box: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/textboxes/{textbox_id}")
async def delete_text_box(
    presentation_id: str,
    slide_index: int,
    textbox_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete a text box from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        # Ensure text_boxes exists
        presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
        text_boxes = presentation["slides"][slide_index]["text_boxes"]

        # Find and remove the text box
        original_count = len(text_boxes)
        text_boxes[:] = [tb for tb in text_boxes if tb.get("id") != textbox_id]

        if len(text_boxes) == original_count:
            raise HTTPException(status_code=404, detail=f"Text box not found: {textbox_id}")

        # Save with version tracking
        summary = change_summary or f"Deleted text box from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": f"Text box deleted",
            "textbox_id": textbox_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting text box: {str(e)}")


# ==================== AI Text Generation Endpoint ====================

@app.post("/api/textbox/generate", response_model=TextGenerationResponse)
async def generate_text_box_content(request: TextGenerationRequest):
    """
    Generate AI text content for text boxes.

    Currently returns mock content. Future: routes to Text Service.
    """
    try:
        # Phase 5: Mock implementation
        # TODO: Route to Text Service at TEXT_SERVICE_URL in future

        prompt = request.prompt
        tone = request.tone or "professional"
        length = request.length or "medium"
        format_type = request.format or "paragraph"

        # Generate mock content based on format
        if format_type == "bullets":
            mock_content = f"""<ul style="margin: 0; padding-left: 24px; color: #374151; line-height: 1.8;">
<li>Key insight based on: "{prompt[:50]}..."</li>
<li>Supporting point with relevant details</li>
<li>Additional consideration for context</li>
</ul>"""
        elif format_type == "numbered":
            mock_content = f"""<ol style="margin: 0; padding-left: 24px; color: #374151; line-height: 1.8;">
<li>First point related to: "{prompt[:40]}..."</li>
<li>Second point with supporting evidence</li>
<li>Third point concluding the thought</li>
</ol>"""
        else:
            mock_content = f"""<p style="margin: 0; color: #374151; line-height: 1.6;">
This is AI-generated content based on your prompt: "{prompt[:60]}...".
In a {tone} tone, this {length} response provides relevant information
that addresses your request. The content has been tailored to fit
the presentation context and maintain consistency with your overall message.
</p>"""

        # Strip HTML for plain text version
        import re
        plain_text = re.sub(r'<[^>]+>', '', mock_content).strip()
        plain_text = re.sub(r'\s+', ' ', plain_text)

        return TextGenerationResponse(
            success=True,
            content=mock_content,
            plain_text=plain_text,
            metadata={
                "model": "mock-v1",
                "tokens_used": 0,
                "generation_time_ms": 100,
                "note": "Mock content - Text Service integration pending"
            }
        )

    except Exception as e:
        return TextGenerationResponse(
            success=False,
            content="",
            error=str(e)
        )


# ==================== Element Properties API ====================

@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/elements/{element_id}/classes",
         response_model=ElementClassesResponse)
async def update_element_classes(
    presentation_id: str,
    slide_index: int,
    element_id: str,
    request: ElementClassesUpdateRequest
):
    """
    Update CSS classes on any element (textbox, image, chart, etc.).

    This endpoint updates the css_classes property on the specified element.
    The actual rendering is done client-side via postMessage to the iframe.

    Args:
        presentation_id: Presentation UUID
        slide_index: 0-based slide index
        element_id: Element ID (e.g., 'textbox-abc123')
        request: Contains css_classes array and replace mode

    Returns:
        ElementClassesResponse with updated classes list
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=404, detail=f"Slide {slide_index} not found")

        slide = presentation["slides"][slide_index]

        # Find element - check text_boxes first
        element_found = False
        element_type = None

        text_boxes = slide.get("text_boxes", [])
        for tb in text_boxes:
            if tb.get("id") == element_id:
                element_found = True
                element_type = "textbox"
                # Update css_classes
                if request.replace:
                    tb["css_classes"] = request.css_classes
                else:
                    existing = tb.get("css_classes", []) or []
                    tb["css_classes"] = list(set(existing + request.css_classes))
                break

        # Check other element types (images, charts, etc.)
        if not element_found:
            for elem_type in ["images", "charts", "infographics", "diagrams"]:
                elements = slide.get(elem_type, [])
                for elem in elements:
                    if elem.get("id") == element_id:
                        element_found = True
                        element_type = elem_type.rstrip("s")  # Remove plural 's'
                        if request.replace:
                            elem["css_classes"] = request.css_classes
                        else:
                            existing = elem.get("css_classes", []) or []
                            elem["css_classes"] = list(set(existing + request.css_classes))
                        break
                if element_found:
                    break

        if not element_found:
            raise HTTPException(
                status_code=404,
                detail=f"Element {element_id} not found on slide {slide_index}"
            )

        # Save presentation
        await storage.save(presentation_id, presentation)

        # Get final css_classes for response
        final_classes = []
        if element_type == "textbox":
            for tb in text_boxes:
                if tb.get("id") == element_id:
                    final_classes = tb.get("css_classes", [])
                    break
        else:
            for elem in slide.get(f"{element_type}s", []):
                if elem.get("id") == element_id:
                    final_classes = elem.get("css_classes", [])
                    break

        return ElementClassesResponse(
            success=True,
            element_id=element_id,
            css_classes=final_classes
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/element-properties/schema")
async def get_element_properties_schema():
    """
    Return the schema for element properties.

    This endpoint provides documentation for the frontend about
    available element properties, their types, and valid values.
    Useful for building properties panels and validation.
    """
    return {
        "textbox_style": {
            "background_color": {
                "type": "string",
                "description": "Background color (hex, rgba, or 'transparent')",
                "examples": ["#ffffff", "rgba(255,255,255,0.8)", "transparent"]
            },
            "border_color": {
                "type": "string",
                "description": "Border color in hex format"
            },
            "border_width": {
                "type": "integer",
                "description": "Border width in pixels",
                "min": 0,
                "max": 20
            },
            "border": {
                "type": "string",
                "description": "Border shorthand (overrides border_width/border_color)",
                "examples": ["1px solid #ddd", "2px dashed #333", "none"]
            },
            "border_radius": {
                "type": "integer",
                "description": "Border radius in pixels",
                "min": 0,
                "max": 50
            },
            "padding": {
                "type": ["integer", "string"],
                "description": "Padding - int (pixels) or shorthand string",
                "examples": [16, "25px 0px", "10px 20px 10px 20px"]
            },
            "vertical_align": {
                "type": "string",
                "description": "Vertical alignment (maps to flexbox justify-content)",
                "enum": ["top", "middle", "bottom"]
            },
            "opacity": {
                "type": "number",
                "description": "Opacity value",
                "min": 0.0,
                "max": 1.0
            },
            "box_shadow": {
                "type": "string",
                "description": "CSS box-shadow value"
            }
        },
        "text_content_style": {
            "color": {"type": "string", "description": "Text color"},
            "font_family": {"type": "string", "description": "Font family"},
            "font_size": {"type": "string", "description": "Font size with unit", "examples": ["32px", "1.5rem"]},
            "font_weight": {"type": "string", "description": "Font weight", "examples": ["normal", "bold", "600"]},
            "font_style": {"type": "string", "description": "Font style", "examples": ["normal", "italic"]},
            "text_align": {"type": "string", "description": "Text alignment", "enum": ["left", "center", "right", "justify"]},
            "line_height": {"type": "string", "description": "Line height", "examples": ["1.5", "24px"]},
            "letter_spacing": {"type": "string", "description": "Letter spacing", "examples": ["0.5px", "0.1em"]},
            "text_decoration": {"type": "string", "description": "Text decoration", "enum": ["none", "underline", "line-through"]},
            "text_transform": {"type": "string", "description": "Text case", "enum": ["none", "uppercase", "lowercase", "capitalize"]}
        },
        "css_classes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Custom CSS class names for additional styling",
            "examples": [["slot-content", "slot-type-bod"], ["highlight-box"]]
        },
        "position": {
            "grid_row": {"type": "string", "description": "CSS grid-row value", "examples": ["5/10", "8/12"]},
            "grid_column": {"type": "string", "description": "CSS grid-column value", "examples": ["3/15", "10/25"]}
        }
    }


@app.get("/p/{presentation_id}", response_class=HTMLResponse)
async def view_presentation(presentation_id: str):
    """View a presentation in the browser"""
    try:
        # Get presentation data
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Read viewer template
        viewer_path = Path(__file__).parent / "viewer" / "presentation-viewer.html"
        if not viewer_path.exists():
            raise HTTPException(status_code=500, detail="Viewer template not found")

        with open(viewer_path, "r") as f:
            html = f.read()

        # Inject presentation data with JavaScript context escaping
        # This enables ApexCharts and other chart libraries with <script> tags
        # See: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#rule-3
        presentation_json = json.dumps(presentation, ensure_ascii=False)

        # Escape ONLY what json.dumps() doesn't handle for JavaScript context
        # NOTE: We do NOT escape backslashes - json.dumps() already handles that correctly
        presentation_json_safe = (
            presentation_json
            .replace('</', '<\\/')           # Prevent </script> tag injection
            .replace('\u2028', '\\u2028')    # Escape line separator (breaks JS)
            .replace('\u2029', '\\u2029')    # Escape paragraph separator (breaks JS)
        )

        html = html.replace(
            "const PRESENTATION_DATA = null;",
            f"const PRESENTATION_DATA = {presentation_json_safe};"
        )

        # Add headers to allow iframe embedding from any origin
        return HTMLResponse(
            content=html,
            headers={
                "Content-Security-Policy": "frame-ancestors *",  # Allow embedding in any iframe
                "X-Frame-Options": "ALLOWALL",  # Legacy header for older browsers
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering presentation: {str(e)}")


@app.get("/tester", response_class=HTMLResponse)
async def api_tester():
    """API testing interface"""
    tester_path = Path(__file__).parent / "viewer" / "api-tester.html"

    if not tester_path.exists():
        return HTMLResponse(content="""
        <html>
            <head><title>API Tester</title></head>
            <body>
                <h1>v7.5-main API Tester</h1>
                <p>API tester interface not yet created. Use /docs for API documentation.</p>
                <p><a href="/docs">Go to API Docs</a></p>
            </body>
        </html>
        """)

    with open(tester_path, "r") as f:
        return HTMLResponse(content=f.read())


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8504))
    uvicorn.run(app, host="0.0.0.0", port=port)
