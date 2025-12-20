"""
Layout Registry for Director Service Integration

This is a Python mirror of src/templates/template-registry.js
providing all 26 templates (backend L-series + frontend H/C/V/I/S/B-series)
with full slot definitions for Director Service coordination.

Grid System: 32 columns x 18 rows on 1920x1080 resolution
"""

from typing import Dict, List, Optional, Any

# ============================================
# GRID SYSTEM CONSTANTS
# ============================================

GRID_COLS = 32
GRID_ROWS = 18
SLIDE_WIDTH = 1920
SLIDE_HEIGHT = 1080
COL_WIDTH = SLIDE_WIDTH / GRID_COLS  # 60px
ROW_HEIGHT = SLIDE_HEIGHT / GRID_ROWS  # 60px


def grid_to_pixels(grid_row: str, grid_col: str) -> Dict[str, float]:
    """
    Convert CSS grid notation ('5/15') to pixel dimensions.

    Args:
        grid_row: Grid row specification like '5/15' (row 5 to 15)
        grid_col: Grid column specification like '2/32' (col 2 to 32)

    Returns:
        Dict with x, y, width, height in pixels
    """
    row_start, row_end = map(int, grid_row.split('/'))
    col_start, col_end = map(int, grid_col.split('/'))
    return {
        "x": (col_start - 1) * COL_WIDTH,
        "y": (row_start - 1) * ROW_HEIGHT,
        "width": (col_end - col_start) * COL_WIDTH,
        "height": (row_end - row_start) * ROW_HEIGHT
    }


def get_slot_with_pixels(slot: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich a slot definition with pixel dimensions."""
    enriched = slot.copy()
    if "grid_row" in slot and "grid_column" in slot:
        enriched["pixels"] = grid_to_pixels(slot["grid_row"], slot["grid_column"])
    return enriched


# ============================================
# TEMPLATE REGISTRY - All 26 Templates
# ============================================

TEMPLATE_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ========================================
    # HERO TEMPLATES (H Series)
    # ========================================

    "H1-generated": {
        "id": "H1-generated",
        "name": "Title Slide (AI Generated)",
        "category": "hero",
        "series": "H",
        "description": "Full-bleed title slide - AI generates entire design",
        "base_layout": "L29",
        "theming_enabled": True,
        "slots": {
            "hero": {
                "grid_row": "1/19",
                "grid_column": "1/33",
                "tag": "hero_content",
                "accepts": ["hero_content"],
                "required": True,
                "description": "Full slide canvas for AI-generated content"
            }
        },
        "defaults": {
            "background_color": "#1f2937"
        }
    },

    "H1-structured": {
        "id": "H1-structured",
        "name": "Title Slide (Manual)",
        "category": "hero",
        "series": "H",
        "description": "Structured title slide with editable title, subtitle, and customizable background",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "background": {
                "grid_row": "1/19",
                "grid_column": "1/33",
                "tag": "background",
                "accepts": ["image", "color", "gradient"],
                "description": "Background image or color"
            },
            "title": {
                "grid_row": "7/10",
                "grid_column": "3/17",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Presentation Title",
                "description": "Main presentation title"
            },
            "subtitle": {
                "grid_row": "10/12",
                "grid_column": "3/17",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Presentation Subtitle",
                "description": "Subtitle or tagline"
            },
            "author_info": {
                "grid_row": "16/18",
                "grid_column": "3/17",
                "tag": "author_info",
                "accepts": ["text"],
                "default_text": "AUTHOR | DATE",
                "description": "Presenter name, date, or other info"
            },
            "logo": {
                "grid_row": "16/18",
                "grid_column": "28/31",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo",
                "description": "Company logo"
            }
        },
        "defaults": {
            "background_color": "#1e3a5f"
        }
    },

    "H2-section": {
        "id": "H2-section",
        "name": "Section Divider",
        "category": "hero",
        "series": "H",
        "description": "Chapter/section break slide",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "background": {
                "grid_row": "1/19",
                "grid_column": "1/33",
                "tag": "background",
                "accepts": ["image", "color", "gradient"],
                "description": "Background image or color"
            },
            "section_number": {
                "grid_row": "6/11",
                "grid_column": "11/17",
                "tag": "section_number",
                "accepts": ["text"],
                "default_text": "#",
                "description": "Section number placeholder"
            },
            "title": {
                "grid_row": "6/11",
                "grid_column": "17/31",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Section Title",
                "description": "Section title"
            }
        },
        "defaults": {
            "background_color": "#374151"
        }
    },

    "H3-closing": {
        "id": "H3-closing",
        "name": "Closing Slide",
        "category": "hero",
        "series": "H",
        "description": "Thank you / closing slide with contact info",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "background": {
                "grid_row": "1/19",
                "grid_column": "1/33",
                "tag": "background",
                "accepts": ["image", "color", "gradient"],
                "description": "Background image or color"
            },
            "title": {
                "grid_row": "6/9",
                "grid_column": "3/31",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Thank You",
                "description": "Closing message"
            },
            "subtitle": {
                "grid_row": "9/11",
                "grid_column": "5/29",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "We appreciate your time",
                "description": "Additional message or call to action"
            },
            "contact_info": {
                "grid_row": "12/15",
                "grid_column": "8/26",
                "tag": "contact",
                "accepts": ["text", "html"],
                "default_text": "email@company.com | www.company.com",
                "description": "Contact details, website, social links"
            },
            "logo": {
                "grid_row": "16/18",
                "grid_column": "26/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo",
                "description": "Company logo"
            }
        },
        "defaults": {
            "background_color": "#1e3a5f"
        }
    },

    # ========================================
    # CONTENT TEMPLATES (C Series)
    # ========================================

    "C1-text": {
        "id": "C1-text",
        "name": "Text Content",
        "category": "content",
        "series": "C",
        "description": "Standard slide with body text (paragraphs, bullets)",
        "base_layout": "L25",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/32",
                "tag": "body",
                "accepts": ["body", "html"],
                "required": True,
                "default_text": "Content Area",
                "description": "Main text content area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "C3-chart": {
        "id": "C3-chart",
        "name": "Single Chart",
        "category": "content",
        "series": "C",
        "description": "Slide with one chart visualization",
        "base_layout": "L25",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/32",
                "tag": "chart",
                "accepts": ["chart"],
                "required": True,
                "default_text": "Chart Area",
                "description": "Chart placeholder area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "C4-infographic": {
        "id": "C4-infographic",
        "name": "Single Infographic",
        "category": "content",
        "series": "C",
        "description": "Slide with one infographic",
        "base_layout": "L25",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/32",
                "tag": "infographic",
                "accepts": ["infographic"],
                "required": True,
                "default_text": "Infographic Area",
                "description": "Infographic placeholder area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "C5-diagram": {
        "id": "C5-diagram",
        "name": "Single Diagram",
        "category": "content",
        "series": "C",
        "description": "Slide with one diagram",
        "base_layout": "L25",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/32",
                "tag": "diagram",
                "accepts": ["diagram"],
                "required": True,
                "default_text": "Diagram Area",
                "description": "Diagram placeholder area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    # ========================================
    # VISUAL + TEXT TEMPLATES (V Series)
    # ========================================

    "V1-image-text": {
        "id": "V1-image-text",
        "name": "Image + Text",
        "category": "visual",
        "series": "V",
        "description": "Image on left, text insights on right",
        "base_layout": "L02",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content_left": {
                "grid_row": "4/18",
                "grid_column": "2/20",
                "tag": "image",
                "accepts": ["image"],
                "description": "Image area (1080x840px)"
            },
            "content_right": {
                "grid_row": "4/18",
                "grid_column": "20/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "default_text": "Key Insights",
                "description": "Text/observations (720x840px)"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    "V2-chart-text": {
        "id": "V2-chart-text",
        "name": "Chart + Text",
        "category": "visual",
        "series": "V",
        "description": "Chart on left, text insights on right",
        "base_layout": "L02",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content_left": {
                "grid_row": "4/18",
                "grid_column": "2/20",
                "tag": "chart",
                "accepts": ["chart"],
                "description": "Chart area (1080x840px)"
            },
            "content_right": {
                "grid_row": "4/18",
                "grid_column": "20/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "default_text": "Key Insights",
                "description": "Text/observations (720x840px)"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    "V3-diagram-text": {
        "id": "V3-diagram-text",
        "name": "Diagram + Text",
        "category": "visual",
        "series": "V",
        "description": "Diagram on left, text insights on right",
        "base_layout": "L02",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content_left": {
                "grid_row": "4/18",
                "grid_column": "2/20",
                "tag": "diagram",
                "accepts": ["diagram"],
                "description": "Diagram area (1080x840px)"
            },
            "content_right": {
                "grid_row": "4/18",
                "grid_column": "20/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "default_text": "Key Insights",
                "description": "Text/observations (720x840px)"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    "V4-infographic-text": {
        "id": "V4-infographic-text",
        "name": "Infographic + Text",
        "category": "visual",
        "series": "V",
        "description": "Infographic on left, text insights on right",
        "base_layout": "L02",
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content_left": {
                "grid_row": "4/18",
                "grid_column": "2/20",
                "tag": "infographic",
                "accepts": ["infographic"],
                "description": "Infographic area (1080x840px)"
            },
            "content_right": {
                "grid_row": "4/18",
                "grid_column": "20/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "default_text": "Key Insights",
                "description": "Text/observations (720x840px)"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    # ========================================
    # IMAGE SPLIT TEMPLATES (I Series)
    # ========================================

    "I1-image-left": {
        "id": "I1-image-left",
        "name": "Image Left (Wide)",
        "category": "image",
        "series": "I",
        "description": "Full-height image on left (12 cols), content on right",
        "base_layout": None,  # L27 decommissioned
        "theming_enabled": True,
        "slots": {
            "image": {
                "grid_row": "1/19",
                "grid_column": "1/12",
                "tag": "image",
                "accepts": ["image"],
                "description": "Full-height image (660x1080px)"
            },
            "title": {
                "grid_row": "1/3",
                "grid_column": "12/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "12/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "12/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "description": "Main content area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "12/17",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "I2-image-right": {
        "id": "I2-image-right",
        "name": "Image Right (Wide)",
        "category": "image",
        "series": "I",
        "description": "Full-height image on right (12 cols), content on left",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "image": {
                "grid_row": "1/19",
                "grid_column": "21/33",
                "tag": "image",
                "accepts": ["image"],
                "description": "Full-height image (660x1080px)"
            },
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/21",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/21",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/21",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "description": "Main content area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "18/20",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "I3-image-left-narrow": {
        "id": "I3-image-left-narrow",
        "name": "Image Left (Narrow)",
        "category": "image",
        "series": "I",
        "description": "Full-height narrow image on left (6 cols), content on right",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "image": {
                "grid_row": "1/19",
                "grid_column": "1/7",
                "tag": "image",
                "accepts": ["image"],
                "description": "Full-height narrow image (360x1080px)"
            },
            "title": {
                "grid_row": "1/3",
                "grid_column": "7/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "7/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "7/32",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "description": "Main content area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "7/12",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    "I4-image-right-narrow": {
        "id": "I4-image-right-narrow",
        "name": "Image Right (Narrow)",
        "category": "image",
        "series": "I",
        "description": "Full-height narrow image on right (6 cols), content on left",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "image": {
                "grid_row": "1/19",
                "grid_column": "26/33",
                "tag": "image",
                "accepts": ["image"],
                "description": "Full-height narrow image (360x1080px)"
            },
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/26",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/26",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "4/18",
                "grid_column": "2/26",
                "tag": "body",
                "accepts": ["body", "table", "html"],
                "description": "Main content area"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "23/25",
                "tag": "logo",
                "accepts": ["image", "emoji"],
                "default_text": "Logo"
            }
        },
        "defaults": {}
    },

    # ========================================
    # SPLIT TEMPLATES (S Series)
    # ========================================

    "S3-two-visuals": {
        "id": "S3-two-visuals",
        "name": "Two Visuals",
        "category": "split",
        "series": "S",
        "description": "Two charts/diagrams/infographics side by side",
        "base_layout": None,  # L03 decommissioned
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content_left": {
                "grid_row": "4/14",
                "grid_column": "2/17",
                "tag": "visual",
                "accepts": ["chart", "infographic", "diagram", "image"],
                "description": "Left visual (900x600px)"
            },
            "content_right": {
                "grid_row": "4/14",
                "grid_column": "17/32",
                "tag": "visual",
                "accepts": ["chart", "infographic", "diagram", "image"],
                "description": "Right visual (900x600px)"
            },
            "caption_left": {
                "grid_row": "14/18",
                "grid_column": "2/17",
                "tag": "body",
                "accepts": ["text", "html"],
                "default_text": "Key Insights 1",
                "description": "Left caption/description"
            },
            "caption_right": {
                "grid_row": "14/18",
                "grid_column": "17/32",
                "tag": "body",
                "accepts": ["text", "html"],
                "default_text": "Key Insights 2",
                "description": "Right caption/description"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    "S4-comparison": {
        "id": "S4-comparison",
        "name": "Comparison",
        "category": "split",
        "series": "S",
        "description": "Two columns for comparing items (before/after, pros/cons)",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "1/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "required": True,
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "header_left": {
                "grid_row": "4/5",
                "grid_column": "2/17",
                "tag": "header",
                "accepts": ["text"],
                "default_text": "Option A",
                "description": "Left column header"
            },
            "header_right": {
                "grid_row": "4/5",
                "grid_column": "17/32",
                "tag": "header",
                "accepts": ["text"],
                "default_text": "Option B",
                "description": "Right column header"
            },
            "content_left": {
                "grid_row": "5/18",
                "grid_column": "2/17",
                "tag": "body",
                "accepts": ["body", "table", "html", "image", "chart"],
                "default_text": "Content 1",
                "description": "Left column content"
            },
            "content_right": {
                "grid_row": "5/18",
                "grid_column": "17/32",
                "tag": "body",
                "accepts": ["body", "table", "html", "image", "chart"],
                "default_text": "Content 2",
                "description": "Right column content"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"],
                "default_text": "Footer"
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {}
    },

    # ========================================
    # BLANK TEMPLATE (B Series)
    # ========================================

    "B1-blank": {
        "id": "B1-blank",
        "name": "Blank Canvas",
        "category": "blank",
        "series": "B",
        "description": "Empty slide - add elements freely using the toolbar",
        "base_layout": None,
        "theming_enabled": False,
        "slots": {},  # No pre-defined slots
        "defaults": {}
    },

    # ========================================
    # BACKEND LAYOUTS (L Series)
    # Note: L01, L03, L27 have been decommissioned
    # Only L02, L25, L29 are active
    # ========================================

    "L02": {
        "id": "L02",
        "name": "Left Diagram with Text Right",
        "category": "backend",
        "series": "L",
        "description": "Diagram/chart on left, observations/text on right",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "2/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"]
            },
            "diagram": {
                "grid_row": "5/17",
                "grid_column": "2/23",
                "tag": "content",
                "accepts": ["content", "diagram", "chart", "html"],
                "description": "Diagram/chart area (1260x720px)",
                "format_owner": "analytics_service"
            },
            "text": {
                "grid_row": "5/17",
                "grid_column": "23/32",
                "tag": "body",
                "accepts": ["text", "body", "html"],
                "description": "Observations/text area (540x720px)"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"]
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {
            "background_color": "#ffffff"
        }
    },

    "L25": {
        "id": "L25",
        "name": "Main Content Shell",
        "category": "backend",
        "series": "L",
        "description": "Standard content slide with title, subtitle, and rich content area (Text Service)",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "title": {
                "grid_row": "2/3",
                "grid_column": "2/32",
                "tag": "title",
                "accepts": ["text"],
                "default_text": "Slide Title"
            },
            "subtitle": {
                "grid_row": "3/4",
                "grid_column": "2/32",
                "tag": "subtitle",
                "accepts": ["text"],
                "default_text": "Subtitle"
            },
            "content": {
                "grid_row": "5/17",
                "grid_column": "2/32",
                "tag": "content",
                "accepts": ["content", "html"],
                "description": "Main content area (1800x720px)",
                "format_owner": "text_service"
            },
            "footer": {
                "grid_row": "18/19",
                "grid_column": "2/7",
                "tag": "footer",
                "accepts": ["text"]
            },
            "logo": {
                "grid_row": "17/19",
                "grid_column": "30/32",
                "tag": "logo",
                "accepts": ["image", "emoji"]
            }
        },
        "defaults": {
            "background_color": "#ffffff"
        }
    },

    "L29": {
        "id": "L29",
        "name": "Hero Full-Bleed",
        "category": "backend",
        "series": "L",
        "description": "Full-bleed hero slide for title/section/closing (Text Service)",
        "base_layout": None,
        "theming_enabled": True,
        "slots": {
            "hero": {
                "grid_row": "1/19",
                "grid_column": "1/33",
                "tag": "content",
                "accepts": ["content", "html", "hero_content"],
                "description": "Full-slide hero content (1920x1080px)",
                "format_owner": "text_service"
            }
        },
        "defaults": {
            "background_color": "#1e3a5f"
        }
    }
}


# ============================================
# TEMPLATE CATEGORIES
# ============================================

TEMPLATE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "hero": {
        "name": "Hero Slides",
        "description": "Full-bleed title, section, and closing slides",
        "templates": ["H1-generated", "H1-structured", "H2-section", "H3-closing"]
    },
    "content": {
        "name": "Content Slides",
        "description": "Single content area slides",
        "templates": ["C1-text", "C3-chart", "C4-infographic", "C5-diagram"]
    },
    "visual": {
        "name": "Visual + Text",
        "description": "Visual element on left with text insights on right",
        "templates": ["V1-image-text", "V2-chart-text", "V3-diagram-text", "V4-infographic-text"]
    },
    "image": {
        "name": "Image Split",
        "description": "Full-height image with content area",
        "templates": ["I1-image-left", "I2-image-right", "I3-image-left-narrow", "I4-image-right-narrow"]
    },
    "split": {
        "name": "Split Layouts",
        "description": "Two-column and multi-element layouts",
        "templates": ["S3-two-visuals", "S4-comparison"]
    },
    "blank": {
        "name": "Blank",
        "description": "Start from scratch",
        "templates": ["B1-blank"]
    },
    "backend": {
        "name": "Backend Layouts",
        "description": "Core backend layouts for Director/Text Service",
        "templates": ["L02", "L25", "L29"]
    },
    "dynamic": {
        "name": "Dynamic Layouts",
        "description": "X-series layouts with dynamically generated content zones",
        "templates": []  # Populated dynamically from ls_dynamic_layouts table
    }
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """Get template definition by ID."""
    return TEMPLATE_REGISTRY.get(template_id)


def get_template_with_pixels(template_id: str) -> Optional[Dict[str, Any]]:
    """Get template with all slots enriched with pixel dimensions."""
    template = TEMPLATE_REGISTRY.get(template_id)
    if not template:
        return None

    result = template.copy()
    result["slots"] = {}
    for slot_name, slot_def in template.get("slots", {}).items():
        result["slots"][slot_name] = get_slot_with_pixels(slot_def)

    return result


def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all templates in a category."""
    category_def = TEMPLATE_CATEGORIES.get(category)
    if not category_def:
        return []
    return [TEMPLATE_REGISTRY[tid] for tid in category_def["templates"] if tid in TEMPLATE_REGISTRY]


def get_all_template_ids() -> List[str]:
    """Get all template IDs."""
    return list(TEMPLATE_REGISTRY.keys())


def slot_accepts(template_id: str, slot_name: str, content_type: str) -> bool:
    """Check if a slot accepts a given content type."""
    template = TEMPLATE_REGISTRY.get(template_id)
    if not template or slot_name not in template.get("slots", {}):
        return False
    accepts = template["slots"][slot_name].get("accepts", [])
    return content_type in accepts or "any" in accepts


def get_main_content_slots(template_id: str) -> List[Dict[str, Any]]:
    """Get the main content slots (not title/footer/logo) with pixel dimensions."""
    template = TEMPLATE_REGISTRY.get(template_id)
    if not template:
        return []

    main_slots = []
    for slot_name, slot_def in template.get("slots", {}).items():
        # Skip structural slots
        if slot_def.get("tag") in ["title", "subtitle", "footer", "logo", "background"]:
            continue
        enriched = get_slot_with_pixels(slot_def)
        enriched["slot_name"] = slot_name
        main_slots.append(enriched)

    return main_slots


def count_slots_accepting(template_id: str, content_type: str) -> int:
    """Count how many slots in a template accept a specific content type."""
    template = TEMPLATE_REGISTRY.get(template_id)
    if not template:
        return 0

    count = 0
    for slot_def in template.get("slots", {}).values():
        if content_type in slot_def.get("accepts", []):
            count += 1
    return count


# ============================================
# X-SERIES: DYNAMIC LAYOUT SUPPORT
# ============================================
# X-series layouts dynamically split the content area of base templates
# into sub-zones based on content analysis.
#
# Mapping:
# X1 → C1-text (1800×840px content area)
# X2 → I1-image-left (1200×840px content area)
# X3 → I2-image-right (1140×840px content area)
# X4 → I3-image-left-narrow (1500×840px content area)
# X5 → I4-image-right-narrow (1440×840px content area)

import hashlib
from typing import Tuple

# Content area definitions for each base layout
# These define the exact pixel bounds of the main content area that can be split
CONTENT_AREAS: Dict[str, Dict[str, Any]] = {
    "C1-text": {
        "grid_row": "4/18",      # rows 4-17 (14 rows)
        "grid_column": "2/32",   # cols 2-31 (30 cols)
        "pixels": {
            "x": 60,            # (2-1) * 60
            "y": 180,           # (4-1) * 60
            "width": 1800,      # 30 * 60
            "height": 840       # 14 * 60
        }
    },
    "I1-image-left": {
        "grid_row": "4/18",      # rows 4-17 (14 rows)
        "grid_column": "12/32",  # cols 12-31 (20 cols)
        "pixels": {
            "x": 660,           # (12-1) * 60
            "y": 180,           # (4-1) * 60
            "width": 1200,      # 20 * 60
            "height": 840       # 14 * 60
        }
    },
    "I2-image-right": {
        "grid_row": "4/18",      # rows 4-17 (14 rows)
        "grid_column": "2/21",   # cols 2-20 (19 cols)
        "pixels": {
            "x": 60,            # (2-1) * 60
            "y": 180,           # (4-1) * 60
            "width": 1140,      # 19 * 60
            "height": 840       # 14 * 60
        }
    },
    "I3-image-left-narrow": {
        "grid_row": "4/18",      # rows 4-17 (14 rows)
        "grid_column": "7/32",   # cols 7-31 (25 cols)
        "pixels": {
            "x": 360,           # (7-1) * 60
            "y": 180,           # (4-1) * 60
            "width": 1500,      # 25 * 60
            "height": 840       # 14 * 60
        }
    },
    "I4-image-right-narrow": {
        "grid_row": "4/18",      # rows 4-17 (14 rows)
        "grid_column": "2/26",   # cols 2-25 (24 cols)
        "pixels": {
            "x": 60,            # (2-1) * 60
            "y": 180,           # (4-1) * 60
            "width": 1440,      # 24 * 60
            "height": 840       # 14 * 60
        }
    }
}

# X-series mapping: base layout → X series number
X_SERIES_MAP: Dict[str, int] = {
    "C1-text": 1,
    "I1-image-left": 2,
    "I2-image-right": 3,
    "I3-image-left-narrow": 4,
    "I4-image-right-narrow": 5
}


# ============================================
# PRECONFIGURED SPLIT PATTERNS
# ============================================
# Patterns define how to split a content area into zones
# Each pattern specifies:
# - direction: horizontal, vertical, or grid
# - ratios: list of proportions for each zone (must sum to 1.0)
# - zone_count: number of zones created
# - labels: default labels for each zone
# - content_hints: suggested content types per zone

SPLIT_PATTERNS: Dict[str, Dict[str, Any]] = {
    # ========== HORIZONTAL SPLITS (rows) ==========
    "agenda-3-item": {
        "direction": "horizontal",
        "zone_count": 3,
        "ratios": [0.35, 0.35, 0.30],  # 3 rows: highlight, item, item
        "labels": ["Main Goal", "Key Point 1", "Key Point 2"],
        "content_hints": ["heading", "bullets", "bullets"],
        "description": "3 horizontal zones for agenda slides"
    },
    "agenda-5-item": {
        "direction": "horizontal",
        "zone_count": 5,
        "ratios": [0.25, 0.20, 0.20, 0.18, 0.17],
        "labels": ["Overview", "Item 1", "Item 2", "Item 3", "Item 4"],
        "content_hints": ["heading", "bullets", "bullets", "bullets", "bullets"],
        "description": "5 horizontal zones for detailed agenda"
    },
    "use-case-3row": {
        "direction": "horizontal",
        "zone_count": 3,
        "ratios": [0.25, 0.50, 0.25],  # Problem, Solution, Benefits
        "labels": ["Problem", "Solution", "Benefits"],
        "content_hints": ["paragraph", "bullets", "highlights"],
        "description": "Problem-Solution-Benefits structure"
    },
    "timeline-4row": {
        "direction": "horizontal",
        "zone_count": 4,
        "ratios": [0.25, 0.25, 0.25, 0.25],
        "labels": ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
        "content_hints": ["timeline_item", "timeline_item", "timeline_item", "timeline_item"],
        "description": "4 equal rows for timeline/process"
    },

    # ========== VERTICAL SPLITS (columns) ==========
    "comparison-2col": {
        "direction": "vertical",
        "zone_count": 2,
        "ratios": [0.50, 0.50],
        "labels": ["Option A", "Option B"],
        "content_hints": ["comparison_item", "comparison_item"],
        "description": "Side-by-side comparison"
    },
    "feature-3col": {
        "direction": "vertical",
        "zone_count": 3,
        "ratios": [0.33, 0.34, 0.33],
        "labels": ["Feature 1", "Feature 2", "Feature 3"],
        "content_hints": ["feature_card", "feature_card", "feature_card"],
        "description": "3 equal columns for features"
    },

    # ========== GRID SPLITS ==========
    "grid-2x2": {
        "direction": "grid",
        "zone_count": 4,
        "grid_layout": [2, 2],  # 2 rows × 2 columns
        "ratios": [0.25, 0.25, 0.25, 0.25],  # Equal distribution
        "labels": ["Quadrant 1", "Quadrant 2", "Quadrant 3", "Quadrant 4"],
        "content_hints": ["card", "card", "card", "card"],
        "description": "2×2 grid layout"
    },
    "grid-2x3": {
        "direction": "grid",
        "zone_count": 6,
        "grid_layout": [2, 3],  # 2 rows × 3 columns
        "ratios": [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],  # Equal distribution
        "labels": ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"],
        "content_hints": ["card", "card", "card", "card", "card", "card"],
        "description": "2×3 grid for 6 items"
    },

    # ========== I-SERIES SPECIFIC (narrow content areas) ==========
    "image-split-2row": {
        "direction": "horizontal",
        "zone_count": 2,
        "ratios": [0.50, 0.50],
        "labels": ["Key Point", "Details"],
        "content_hints": ["heading", "bullets"],
        "description": "2 rows for image + text layouts"
    },
    "image-split-3row": {
        "direction": "horizontal",
        "zone_count": 3,
        "ratios": [0.33, 0.34, 0.33],
        "labels": ["Point 1", "Point 2", "Point 3"],
        "content_hints": ["bullets", "bullets", "bullets"],
        "description": "3 rows for image + text layouts"
    }
}


# ============================================
# X-SERIES HELPER FUNCTIONS
# ============================================

def generate_layout_id(base_layout: str, zone_config: Dict[str, Any]) -> str:
    """
    Generate a unique layout ID for an X-series layout.

    Format: X{series}-{hash8}
    Example: X1-a3f7e8c2

    Args:
        base_layout: Base layout ID (C1-text, I1-image-left, etc.)
        zone_config: Zone configuration dictionary to hash

    Returns:
        Unique layout ID string
    """
    series = X_SERIES_MAP.get(base_layout, 1)
    # Create a deterministic hash from the zone configuration
    config_str = str(sorted(zone_config.items()))
    hash_digest = hashlib.sha256(config_str.encode()).hexdigest()[:8]
    return f"X{series}-{hash_digest}"


def get_content_area(base_layout: str) -> Optional[Dict[str, Any]]:
    """
    Get the content area definition for a base layout.

    Args:
        base_layout: Base layout ID (C1-text, I1-image-left, etc.)

    Returns:
        Content area dict with grid_row, grid_column, and pixels
    """
    return CONTENT_AREAS.get(base_layout)


def get_x_series_number(base_layout: str) -> int:
    """
    Get the X-series number for a base layout.

    Args:
        base_layout: Base layout ID

    Returns:
        X-series number (1-5)
    """
    return X_SERIES_MAP.get(base_layout, 1)


def get_split_pattern(pattern_name: str) -> Optional[Dict[str, Any]]:
    """
    Get a split pattern by name.

    Args:
        pattern_name: Pattern name (e.g., "agenda-3-item")

    Returns:
        Pattern definition dict
    """
    return SPLIT_PATTERNS.get(pattern_name)


def list_split_patterns() -> List[str]:
    """Get all available split pattern names."""
    return list(SPLIT_PATTERNS.keys())


def suggest_pattern_for_content_type(content_type: str, zone_count: int = 3) -> Optional[str]:
    """
    Suggest a split pattern based on content type and zone count.

    Args:
        content_type: Content type (agenda, use_case, comparison, etc.)
        zone_count: Desired number of zones

    Returns:
        Pattern name or None if no match
    """
    # Content type to pattern mapping
    suggestions = {
        ("agenda", 3): "agenda-3-item",
        ("agenda", 5): "agenda-5-item",
        ("use_case", 3): "use-case-3row",
        ("use_cases", 3): "use-case-3row",
        ("comparison", 2): "comparison-2col",
        ("compare", 2): "comparison-2col",
        ("features", 3): "feature-3col",
        ("feature", 3): "feature-3col",
        ("timeline", 4): "timeline-4row",
        ("process", 4): "timeline-4row",
        ("grid", 4): "grid-2x2",
        ("grid", 6): "grid-2x3",
    }

    # Check for exact match
    key = (content_type.lower(), zone_count)
    if key in suggestions:
        return suggestions[key]

    # Check for content type match with any zone count
    for (ct, zc), pattern in suggestions.items():
        if ct == content_type.lower():
            return pattern

    return None


def create_zones_from_pattern(
    base_layout: str,
    pattern_name: str,
    zone_labels: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Create zone definitions by splitting a content area using a pattern.

    Args:
        base_layout: Base layout ID (C1-text, I1-image-left, etc.)
        pattern_name: Split pattern name (e.g., "agenda-3-item")
        zone_labels: Optional custom labels for zones

    Returns:
        List of zone definitions with grid and pixel coordinates
    """
    content_area = CONTENT_AREAS.get(base_layout)
    if not content_area:
        raise ValueError(f"Unknown base layout: {base_layout}")

    pattern = SPLIT_PATTERNS.get(pattern_name)
    if not pattern:
        raise ValueError(f"Unknown split pattern: {pattern_name}")

    # Parse content area grid coordinates
    row_start, row_end = map(int, content_area["grid_row"].split('/'))
    col_start, col_end = map(int, content_area["grid_column"].split('/'))

    total_rows = row_end - row_start
    total_cols = col_end - col_start

    pixels = content_area["pixels"]
    direction = pattern["direction"]
    ratios = pattern["ratios"]
    labels = zone_labels or pattern.get("labels", [])
    content_hints = pattern.get("content_hints", [])

    zones = []

    if direction == "horizontal":
        # Split by rows
        current_row = row_start
        current_y = pixels["y"]

        for i, ratio in enumerate(ratios):
            row_span = int(total_rows * ratio)
            # Ensure at least 1 row per zone
            row_span = max(1, row_span)

            zone_height = int(pixels["height"] * ratio)

            zone = {
                "zone_id": f"zone_{i+1}",
                "label": labels[i] if i < len(labels) else f"Zone {i+1}",
                "grid_row": f"{current_row}/{current_row + row_span}",
                "grid_column": content_area["grid_column"],
                "pixels": {
                    "x": pixels["x"],
                    "y": current_y,
                    "width": pixels["width"],
                    "height": zone_height
                },
                "content_type_hint": content_hints[i] if i < len(content_hints) else None,
                "z_index": 100 + i
            }
            zones.append(zone)

            current_row += row_span
            current_y += zone_height

    elif direction == "vertical":
        # Split by columns
        current_col = col_start
        current_x = pixels["x"]

        for i, ratio in enumerate(ratios):
            col_span = int(total_cols * ratio)
            # Ensure at least 1 col per zone
            col_span = max(1, col_span)

            zone_width = int(pixels["width"] * ratio)

            zone = {
                "zone_id": f"zone_{i+1}",
                "label": labels[i] if i < len(labels) else f"Zone {i+1}",
                "grid_row": content_area["grid_row"],
                "grid_column": f"{current_col}/{current_col + col_span}",
                "pixels": {
                    "x": current_x,
                    "y": pixels["y"],
                    "width": zone_width,
                    "height": pixels["height"]
                },
                "content_type_hint": content_hints[i] if i < len(content_hints) else None,
                "z_index": 100 + i
            }
            zones.append(zone)

            current_col += col_span
            current_x += zone_width

    elif direction == "grid":
        # Grid layout (rows × cols)
        grid_layout = pattern.get("grid_layout", [2, 2])
        grid_rows, grid_cols = grid_layout

        rows_per_zone = total_rows // grid_rows
        cols_per_zone = total_cols // grid_cols
        zone_height = pixels["height"] // grid_rows
        zone_width = pixels["width"] // grid_cols

        zone_idx = 0
        for r in range(grid_rows):
            for c in range(grid_cols):
                zone = {
                    "zone_id": f"zone_{zone_idx+1}",
                    "label": labels[zone_idx] if zone_idx < len(labels) else f"Zone {zone_idx+1}",
                    "grid_row": f"{row_start + r * rows_per_zone}/{row_start + (r+1) * rows_per_zone}",
                    "grid_column": f"{col_start + c * cols_per_zone}/{col_start + (c+1) * cols_per_zone}",
                    "pixels": {
                        "x": pixels["x"] + c * zone_width,
                        "y": pixels["y"] + r * zone_height,
                        "width": zone_width,
                        "height": zone_height
                    },
                    "content_type_hint": content_hints[zone_idx] if zone_idx < len(content_hints) else None,
                    "z_index": 100 + zone_idx
                }
                zones.append(zone)
                zone_idx += 1

    return zones


def create_custom_zones(
    base_layout: str,
    direction: str,
    ratios: List[float],
    zone_labels: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Create zone definitions with custom ratios.

    Args:
        base_layout: Base layout ID
        direction: "horizontal", "vertical", or "grid"
        ratios: List of proportions (must sum to 1.0)
        zone_labels: Optional labels for zones

    Returns:
        List of zone definitions
    """
    # Validate ratios sum to 1.0
    if abs(sum(ratios) - 1.0) > 0.01:
        raise ValueError("Ratios must sum to 1.0")

    # Create a temporary pattern
    temp_pattern = {
        "direction": direction,
        "zone_count": len(ratios),
        "ratios": ratios,
        "labels": zone_labels or [f"Zone {i+1}" for i in range(len(ratios))],
        "content_hints": []
    }

    # Add temporary pattern to registry
    temp_name = f"_custom_{len(ratios)}_{direction}"
    SPLIT_PATTERNS[temp_name] = temp_pattern

    try:
        zones = create_zones_from_pattern(base_layout, temp_name)
    finally:
        # Clean up temporary pattern
        del SPLIT_PATTERNS[temp_name]

    return zones
