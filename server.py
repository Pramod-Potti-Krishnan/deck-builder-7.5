"""
FastAPI server for v7.5-main: Simplified Layout Architecture

Port: 8504
Backend Layouts: L01, L02, L03, L25, L27, L29
Frontend Templates: H1-generated, H1-structured, H2-section, H3-closing,
                   C1-text, C2-table, C3-chart, C4-infographic, C5-diagram, C6-image,
                   S1-visual-text, S2-image-content, S3-two-visuals, S4-comparison, B1-blank
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
    # Text Box models
    TextBox,
    TextBoxPosition,
    TextBoxStyle,
    TextBoxCreateRequest,
    TextBoxUpdateRequest,
    TextBoxResponse,
    TextBoxListResponse,
    TextGenerationRequest,
    TextGenerationResponse
)
from storage import storage
import copy


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
        "C2-table": {
            "slide_title": "Table Title",
            "subtitle": "Subtitle",
            "table_html": "Table Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
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
        "C6-image": {
            "slide_title": "Image Title",
            "subtitle": "Subtitle",
            "image_url": "Image Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },

        # ========== FRONTEND TEMPLATES - SPLIT ==========
        # Default text values should match Template Builder v7.4 placeholders
        "S1-visual-text": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "visual_content": "Visual Area",
            "body": "Key Insights",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
        "S2-image-content": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle",
            "image_url": "",
            "body": "Content Area",
            "footer_text": "Footer",
            "company_logo": "Logo"
        },
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
                "content": ["C1-text", "C2-table", "C3-chart", "C4-infographic", "C5-diagram", "C6-image"],
                "split": ["S1-visual-text", "S2-image-content", "S3-two-visuals", "S4-comparison"],
                "blank": ["B1-blank"]
            }
        },
        "philosophy": "Text Service owns content creation, Layout Builder provides structure",
        "features": ["Content editing", "Version history", "Undo/restore capabilities"],
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
            "C1-text", "C2-table", "C3-chart", "C4-infographic", "C5-diagram", "C6-image",
            # Frontend templates - Split
            "S1-visual-text", "S2-image-content", "S3-two-visuals", "S4-comparison",
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
            "C1-text", "C2-table", "C3-chart", "C4-infographic", "C5-diagram", "C6-image",
            "S1-visual-text", "S2-image-content", "S3-two-visuals", "S4-comparison",
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
            "C1-text", "C2-table", "C3-chart", "C4-infographic", "C5-diagram", "C6-image",
            "S1-visual-text", "S2-image-content", "S3-two-visuals", "S4-comparison",
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
