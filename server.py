"""
FastAPI server for v7.5-main: Simplified 6-Layout Architecture

Port: 8504
Layouts: L01, L02, L03, L25, L27, L29
"""

import os
import json
from fastapi import FastAPI, HTTPException
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
    RestoreVersionRequest
)
from storage import storage


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
        "layouts": ["L01", "L02", "L03", "L25", "L27", "L29"],
        "philosophy": "Text Service owns content creation, Layout Builder provides structure",
        "features": ["Content editing", "Version history", "Undo/restore capabilities"],
        "endpoints": {
            "create_presentation": "POST /api/presentations",
            "get_presentation_data": "GET /api/presentations/{id}",
            "update_presentation_metadata": "PUT /api/presentations/{id}",
            "update_slide_content": "PUT /api/presentations/{id}/slides/{slide_index}",
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

        # Validate layouts
        valid_layouts = ["L01", "L02", "L03", "L25", "L27", "L29"]
        for slide in presentation_data["slides"]:
            if slide["layout"] not in valid_layouts:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid layout '{slide['layout']}'. Valid layouts: {valid_layouts}"
                )

        # Save to storage
        presentation_id = storage.save(presentation_data)

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
        presentation = storage.load(presentation_id)
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
        presentations = storage.list_all()
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
        success = storage.delete(presentation_id)
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
        updated = storage.update(
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
        presentation = storage.load(presentation_id)
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

        # Update slide content
        presentation["slides"][slide_index]["content"].update(updates)

        # Save with version tracking
        updated = storage.update(
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


@app.get("/api/presentations/{presentation_id}/versions", response_model=VersionHistoryResponse)
async def get_version_history(presentation_id: str):
    """
    Get version history for a presentation

    Returns list of all versions with metadata.
    """
    try:
        # Check if presentation exists
        presentation = storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Get version history
        history = storage.get_version_history(presentation_id)

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
        presentation = storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Restore version
        restored = storage.restore_version(
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


@app.get("/p/{presentation_id}", response_class=HTMLResponse)
async def view_presentation(presentation_id: str):
    """View a presentation in the browser"""
    try:
        # Get presentation data
        presentation = storage.load(presentation_id)
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

        return HTMLResponse(content=html)

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
