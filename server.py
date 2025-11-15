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

from models import Presentation, PresentationResponse
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
        "message": "v7.5-main: Simplified Layout Builder API",
        "version": "7.5.0",
        "layouts": ["L01", "L02", "L03", "L25", "L27", "L29"],
        "philosophy": "Text Service owns content creation, Layout Builder provides structure",
        "endpoints": {
            "create_presentation": "POST /api/presentations",
            "get_presentation_data": "GET /api/presentations/{id}",
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

        # Inject presentation data
        presentation_json = json.dumps(presentation)
        html = html.replace(
            "const PRESENTATION_DATA = null;",
            f"const PRESENTATION_DATA = {presentation_json};"
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
