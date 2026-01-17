"""
FastAPI server for v7.5-main: Simplified Layout Architecture

Port: 8504
Backend Layouts: L02, L25, L29 (L01, L03, L27 decommissioned)
Frontend Templates: H1-generated, H1-structured, H2-section, H3-closing,
                   C1-text, C3-chart, C4-infographic, C5-diagram,
                   V1-image-text, V2-chart-text, V3-diagram-text, V4-infographic-text,
                   I1-image-left, I2-image-right, I3-image-left-narrow, I4-image-right-narrow,
                   S3-two-visuals, S4-comparison, B1-blank
"""

import os
import json
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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
    # Image Element CRUD models
    ImageElement,
    ImageCreateRequest,
    ImageUpdateRequest,
    ImageResponse,
    ImageListResponse,
    # Chart Element CRUD models
    ChartElement,
    ChartCreateRequest,
    ChartUpdateRequest,
    ChartResponse,
    ChartListResponse,
    # Diagram Element CRUD models
    DiagramElement,
    DiagramCreateRequest,
    DiagramUpdateRequest,
    DiagramResponse,
    DiagramListResponse,
    # Infographic Element CRUD models
    InfographicElement,
    InfographicCreateRequest,
    InfographicUpdateRequest,
    InfographicResponse,
    InfographicListResponse,
    # Content Element CRUD models
    ContentElement,
    ContentCreateRequest,
    ContentUpdateRequest,
    ContentResponse,
    ContentListResponse,
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
    UserCustomThemeListResponse,
    # Director Service Integration models (v7.5.5)
    LayoutSummary,
    LayoutDetailResponse,
    LayoutListResponse,
    LayoutRecommendationRequest,
    LayoutRecommendationResponse,
    LayoutRecommendation,
    CanFitRequest,
    CanFitResponse,
    CapabilitiesResponse,
    SlotDefinition,
    SlotPixels,
    # X-Series Dynamic Layout models (v7.5.7)
    DynamicLayoutRequest,
    DynamicLayoutResponse,
    DynamicLayoutListResponse,
    ZoneDefinition,
    ZonePixels,
    # Grid Element API models (v7.5.9)
    AddElementRequest,
    AddElementResponse
)
from storage import storage
from src.layout_registry import (
    TEMPLATE_REGISTRY,
    TEMPLATE_CATEGORIES,
    get_template,
    get_template_with_pixels,
    get_templates_by_category,
    get_all_template_ids,
    get_main_content_slots,
    count_slots_accepting,
    grid_to_pixels,
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    # X-Series Dynamic Layout support (v7.5.7)
    CONTENT_AREAS,
    SPLIT_PATTERNS,
    X_SERIES_MAP,
    generate_layout_id,
    get_content_area,
    get_x_series_number,
    get_split_pattern,
    list_split_patterns,
    suggest_pattern_for_content_type,
    create_zones_from_pattern,
    create_custom_zones
)
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
            border="#e5e7eb",
            # Tertiary colors
            tertiary_1="#f8fafc",
            tertiary_2="#e2e8f0",
            tertiary_3="#94a3b8",
            # Chart colors
            chart_1="#3b82f6",
            chart_2="#10b981",
            chart_3="#f59e0b",
            chart_4="#ef4444",
            chart_5="#8b5cf6",
            chart_6="#ec4899"
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
            border="#d1fae5",
            # Tertiary colors
            tertiary_1="#ecfdf5",
            tertiary_2="#a7f3d0",
            tertiary_3="#6ee7b7",
            # Chart colors
            chart_1="#10b981",
            chart_2="#3b82f6",
            chart_3="#f59e0b",
            chart_4="#ef4444",
            chart_5="#8b5cf6",
            chart_6="#ec4899"
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
            border="#fdba74",
            # Tertiary colors
            tertiary_1="#fff7ed",
            tertiary_2="#fed7aa",
            tertiary_3="#fdba74",
            # Chart colors
            chart_1="#f97316",
            chart_2="#3b82f6",
            chart_3="#10b981",
            chart_4="#ef4444",
            chart_5="#8b5cf6",
            chart_6="#ec4899"
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
            border="#374151",
            # Tertiary colors
            tertiary_1="#374151",
            tertiary_2="#4b5563",
            tertiary_3="#6b7280",
            # Chart colors (brighter for dark background)
            chart_1="#60a5fa",
            chart_2="#34d399",
            chart_3="#fbbf24",
            chart_4="#f87171",
            chart_5="#a78bfa",
            chart_6="#f472b6"
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

# Character width ratios for common fonts (used by Text Service)
# These ratios represent: average character width / font size
FONT_CHAR_WIDTH_RATIOS: dict[str, float] = {
    "Poppins": 0.50,
    "Inter": 0.48,
    "Roboto": 0.47,
    "Open Sans": 0.49,
    "Montserrat": 0.52,
    "Lato": 0.47,
    "Playfair Display": 0.45,
    "default": 0.50
}


def get_char_width_ratio(font_family: str) -> float:
    """
    Get character width ratio for a font family.

    Args:
        font_family: CSS font-family string (e.g., "Poppins, sans-serif")

    Returns:
        Float ratio (0.45-0.55 typical range)
    """
    # Extract primary font name from CSS font-family
    primary_font = font_family.split(",")[0].strip().strip("'\"")
    return FONT_CHAR_WIDTH_RATIOS.get(primary_font, FONT_CHAR_WIDTH_RATIOS["default"])


def build_typography_response(theme: ThemeConfig) -> dict:
    """
    Transform ThemeConfig into ThemeTypographyResponse format.

    Extracts and normalizes typography data from theme configuration
    into the format required by Text Service.

    Args:
        theme: ThemeConfig object (predefined or custom)

    Returns:
        Dictionary matching ThemeTypographyResponse schema
    """
    colors = theme.colors
    typography = theme.typography or {}
    content_styles = theme.content_styles or {}
    effects = theme.effects

    # Extract font families
    font_family = typography.get("fontFamily", "Poppins, sans-serif")
    font_family_heading = typography.get("fontFamilyHeading") or font_family

    # Helper to parse fontSize string to int
    def parse_size(size_str: str, default: int = 20) -> int:
        if not size_str:
            return default
        try:
            return int(str(size_str).replace("px", "").strip())
        except (ValueError, AttributeError):
            return default

    # Helper to parse fontWeight to int
    def parse_weight(weight_str, default: int = 400) -> int:
        if not weight_str:
            return default
        weight_map = {"normal": 400, "bold": 700, "light": 300}
        if isinstance(weight_str, int):
            return weight_str
        if isinstance(weight_str, str):
            if weight_str in weight_map:
                return weight_map[weight_str]
            try:
                return int(weight_str)
            except ValueError:
                return default
        return default

    # Helper to parse lineHeight to float
    def parse_line_height(lh_str, default: float = 1.4) -> float:
        if not lh_str:
            return default
        try:
            return float(lh_str)
        except (ValueError, TypeError):
            return default

    # Build h1 token - from hero title (largest) for presentation titles
    hero_title = typography.get("hero", {}).get("title", {})
    h1_size = parse_size(hero_title.get("fontSize"), 72)
    h1_token = {
        "size": h1_size,
        "size_px": f"{h1_size}px",
        "weight": parse_weight(hero_title.get("fontWeight"), 700),
        "line_height": 1.2,
        "letter_spacing": "-0.02em",
        "color": colors.text_primary,
        "text_transform": "none"
    }

    # Build h2 token - from standard title (slide titles)
    standard_title = typography.get("standard", {}).get("title", {})
    content_h2 = content_styles.get("h2", {})
    h2_size = parse_size(standard_title.get("fontSize") or content_h2.get("fontSize"), 42)
    h2_token = {
        "size": h2_size,
        "size_px": f"{h2_size}px",
        "weight": parse_weight(standard_title.get("fontWeight") or content_h2.get("fontWeight"), 600),
        "line_height": 1.3,
        "letter_spacing": "-0.01em",
        "color": colors.text_primary,
        "text_transform": "none"
    }

    # Build h3 token - from content_styles.h3 (subsection headings)
    content_h3 = content_styles.get("h3", {})
    h3_size = parse_size(content_h3.get("fontSize"), 22)
    h3_token = {
        "size": h3_size,
        "size_px": f"{h3_size}px",
        "weight": parse_weight(content_h3.get("fontWeight"), 600),
        "line_height": 1.4,
        "letter_spacing": "0",
        "color": colors.text_primary,
        "text_transform": "none"
    }

    # Build h4 token - derived from h3 pattern (smaller)
    h4_size = max(h3_size - 4, 18)  # h4 is typically 4px smaller than h3
    h4_token = {
        "size": h4_size,
        "size_px": f"{h4_size}px",
        "weight": 600,
        "line_height": 1.4,
        "letter_spacing": "0",
        "color": colors.text_body,
        "text_transform": "none"
    }

    # Build body token - from standard body or content_styles.p
    standard_body = typography.get("standard", {}).get("body", {})
    content_p = content_styles.get("p", {})
    body_size = parse_size(standard_body.get("fontSize") or content_p.get("fontSize"), 20)
    body_token = {
        "size": body_size,
        "size_px": f"{body_size}px",
        "weight": 400,
        "line_height": parse_line_height(standard_body.get("lineHeight") or content_p.get("lineHeight"), 1.6),
        "letter_spacing": "0",
        "color": colors.text_body
    }

    # Build subtitle token - from standard subtitle
    standard_subtitle = typography.get("standard", {}).get("subtitle", {})
    subtitle_size = parse_size(standard_subtitle.get("fontSize"), 24)
    subtitle_token = {
        "size": subtitle_size,
        "size_px": f"{subtitle_size}px",
        "weight": parse_weight(standard_subtitle.get("fontWeight"), 400),
        "line_height": 1.5,
        "letter_spacing": "0",
        "color": colors.text_secondary,
        "text_transform": "none"
    }

    # Build caption token - derived from body pattern (smaller)
    caption_size = max(body_size - 4, 14)  # Caption is smaller than body
    caption_token = {
        "size": caption_size,
        "size_px": f"{caption_size}px",
        "weight": 400,
        "line_height": 1.4,
        "letter_spacing": "0.01em",
        "color": colors.text_secondary
    }

    # Build emphasis token
    emphasis_token = {
        "weight": 600,
        "color": colors.text_primary,
        "style": "normal"
    }

    # Build list_styles - from ul/li content_styles + primary color
    content_ul = content_styles.get("ul", {})
    content_li = content_styles.get("li", {})
    list_styles = {
        "bullet_type": "disc",
        "bullet_color": colors.primary,
        "bullet_size": "0.4em",
        "list_indent": content_ul.get("paddingLeft", "1.5em"),
        "item_spacing": content_li.get("marginBottom", "0.5em"),
        "numbered_style": "decimal",
        "nested_indent": "1.5em"
    }

    # Build textbox_defaults - from effects or defaults
    border_radius = "8px"
    if effects:
        border_radius = effects.border_radius
    textbox_defaults = {
        "background": "transparent",
        "background_gradient": None,
        "border_width": "0px",
        "border_color": "transparent",
        "border_radius": border_radius,
        "padding": "16px",
        "box_shadow": "none"
    }

    # Get char_width_ratio
    char_width_ratio = get_char_width_ratio(font_family)

    return {
        "theme_id": theme.id,
        "font_family": font_family,
        "font_family_heading": font_family_heading,
        "tokens": {
            "h1": h1_token,
            "h2": h2_token,
            "h3": h3_token,
            "h4": h4_token,
            "body": body_token,
            "subtitle": subtitle_token,
            "caption": caption_token,
            "emphasis": emphasis_token
        },
        "list_styles": list_styles,
        "textbox_defaults": textbox_defaults,
        "char_width_ratio": char_width_ratio
    }


# ==================== Helper Functions ====================

def get_default_content(layout: str) -> dict:
    """
    Get default content template for a layout type.

    These defaults provide a starting point for new slides.
    Supports both backend layouts (L02, L25, L29) and frontend templates (H1, C1, S1, B1).
    """
    defaults = {
        # ========== BACKEND LAYOUTS (L01, L03, L27 decommissioned) ==========
        "L02": {
            "slide_title": "Diagram Title",
            "element_1": "Diagram Label",
            "element_4": "<div style='width:100%;height:500px;display:flex;align-items:center;justify-content:center;background:#f8fafc;border:2px dashed #cbd5e1;border-radius:8px;'><span style='color:#64748b;'>Diagram placeholder</span></div>",
            "element_2": "<ul><li>Key point one</li><li>Key point two</li><li>Key point three</li></ul>"
        },
        "L25": {
            "slide_title": "Slide Title",
            "subtitle": "Subtitle goes here",
            "rich_content": "<div style='padding: 20px;'><h2 style='color: #1f2937; margin-bottom: 16px;'>Content Heading</h2><p style='color: #374151; line-height: 1.6;'>Add your content here. This layout provides a large content area for rich text, lists, and formatted content.</p><ul style='margin-top: 16px; color: #374151;'><li>First point</li><li>Second point</li><li>Third point</li></ul></div>"
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
        if field in old_content and new_layout in ["L02"]:
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
            "backend": ["L02", "L25", "L29"],
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

    Supports blank presentation creation (v7.5.4):
    When blank=true, creates a single C1-text slide with "Untitled Presentation" title.
    Used for immediate presentation creation on builder page load.

    Request body (standard):
    {
        "title": "My Presentation",
        "slides": [
            {
                "layout": "L29",
                "content": {
                    "hero_content": "<div style='...'>Title Slide with Presenter Info</div>"
                }
            }
        ]
    }

    Request body (blank presentation):
    {
        "blank": true,
        "session_id": "uuid",  // optional
        "user_id": "string"    // optional
    }

    Returns:
    {
        "id": "uuid",
        "url": "/p/uuid",
        "message": "Presentation created successfully",
        "slide_count": 1,      // for blank presentations
        "layout": "C1-text"    // for blank presentations
    }
    """
    try:
        from uuid import uuid4

        # Handle blank presentation shortcut (v7.5.4)
        if request.blank:
            slide_id = f"slide_{uuid4().hex[:12]}"
            presentation_data = {
                "title": request.title if request.title != "Untitled Presentation" or not request.blank else "Untitled Presentation",
                "slides": [{
                    "slide_id": slide_id,
                    "layout": "C1-text",
                    "content": get_default_content("C1-text"),
                    "background_color": None,
                    "background_image": None,
                    "text_boxes": [],
                    "images": [],
                    "charts": [],
                    "infographics": [],
                    "diagrams": [],
                    "contents": []
                }],
                "derivative_elements": None,
                "theme_config": None,
                "is_blank": True,  # Track for cleanup
                "session_id": request.session_id,
                "user_id": request.user_id
            }

            # Save to storage
            presentation_id = await storage.save(presentation_data)

            # Build response with additional blank presentation fields
            return PresentationResponse(
                id=presentation_id,
                url=f"/p/{presentation_id}",
                message=f"Presentation '{presentation_data['title']}' created successfully",
                slide_count=1,
                layout="C1-text"
            )

        # Standard flow: Convert request to dict
        presentation_data = request.model_dump()

        # Validate layouts (backend + frontend templates)
        valid_layouts = [
            # Backend layouts (L01, L03, L27 decommissioned)
            "L02", "L25", "L29",
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


# NOTE: This sync endpoint must come BEFORE the general /{theme_id} route
@app.get("/api/themes/sync")
async def sync_themes():
    """
    Bulk sync endpoint for Text Service and Director.

    Returns all predefined themes in a single response with version tracking.
    Text Service calls this on startup to cache theme definitions.

    Response format (snake_case for Python/Pydantic compatibility):
    {
        "themes": {
            "corporate-blue": {"typography": {...}, "colors": {...}},
            ...
        },
        "version": "1.0.0",
        "last_updated": "2024-12-20T00:00:00Z"
    }
    """
    from datetime import datetime

    themes_data = {}
    for theme_id, theme in PREDEFINED_THEMES.items():
        themes_data[theme_id] = {
            "typography": theme.typography,
            "colors": theme.colors.model_dump(),  # Returns snake_case
            "content_styles": theme.content_styles
        }

    return {
        "themes": themes_data,
        "version": "1.0.0",
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }


# NOTE: This typography endpoint must come BEFORE the general /{theme_id} route
@app.get("/api/themes/{theme_id}/typography")
async def get_theme_typography(theme_id: str):
    """
    Get typography tokens for a theme.

    Returns complete typography configuration optimized for Text Service
    character constraint calculations and theme-aware text generation.

    Path Parameters:
    - theme_id: Theme identifier (predefined ID like 'corporate-blue' or custom theme UUID)

    Returns:
    - font_family: Primary font family
    - font_family_heading: Heading font family
    - tokens: Typography tokens for h1-h4, body, subtitle, caption, emphasis
    - list_styles: Bullet and list styling tokens
    - textbox_defaults: Default text container styling
    - char_width_ratio: Font character width ratio for constraint calculations

    Example:
    ```json
    {
        "theme_id": "corporate-blue",
        "font_family": "Poppins, sans-serif",
        "tokens": {
            "h1": {"size": 72, "size_px": "72px", "weight": 700, ...},
            "body": {"size": 20, "size_px": "20px", "weight": 400, ...}
        },
        "list_styles": {"bullet_type": "disc", "bullet_color": "#1e40af", ...},
        "char_width_ratio": 0.5
    }
    ```
    """
    # First, check if it's a predefined theme
    theme = PREDEFINED_THEMES.get(theme_id)

    if theme:
        # Build typography response from predefined theme
        response = build_typography_response(theme)
        return JSONResponse(content=response)

    # If not predefined, check for custom user theme (UUID format)
    if hasattr(storage, 'supabase') and storage.supabase:
        try:
            result = storage.supabase.client.table("ls_user_themes").select("*").eq(
                "id", theme_id
            ).execute()

            if result.data:
                custom_theme_data = result.data[0]
                theme_config = custom_theme_data.get("theme_config", {})
                base_theme_id = custom_theme_data.get("base_theme_id")

                # Start with base theme if specified
                if base_theme_id and base_theme_id in PREDEFINED_THEMES:
                    base = PREDEFINED_THEMES[base_theme_id]
                    # Create merged theme
                    merged_colors = base.colors.model_dump()
                    if "colors" in theme_config:
                        merged_colors.update(theme_config["colors"])

                    merged_typography = base.typography.copy() if base.typography else {}
                    if "typography" in theme_config:
                        merged_typography.update(theme_config["typography"])

                    merged_content_styles = base.content_styles.copy() if base.content_styles else {}
                    if "content_styles" in theme_config:
                        merged_content_styles.update(theme_config["content_styles"])

                    merged_effects = base.effects

                    # Create a synthetic ThemeConfig for the helper
                    synthetic_theme = ThemeConfig(
                        id=theme_id,
                        name=custom_theme_data.get("name", "Custom Theme"),
                        colors=ThemeColors(**merged_colors),
                        typography=merged_typography,
                        content_styles=merged_content_styles,
                        effects=merged_effects,
                        is_custom=True
                    )
                    response = build_typography_response(synthetic_theme)
                    return JSONResponse(content=response)
                else:
                    # Fully custom theme without base
                    colors_data = theme_config.get("colors", ThemeColors().model_dump())
                    synthetic_theme = ThemeConfig(
                        id=theme_id,
                        name=custom_theme_data.get("name", "Custom Theme"),
                        colors=ThemeColors(**colors_data),
                        typography=theme_config.get("typography"),
                        content_styles=theme_config.get("content_styles"),
                        is_custom=True
                    )
                    response = build_typography_response(synthetic_theme)
                    return JSONResponse(content=response)
        except Exception as e:
            # Log error but continue to 404
            print(f"[ThemeTypography] Error fetching custom theme {theme_id}: {e}")

    # Theme not found
    raise HTTPException(
        status_code=404,
        detail=f"Theme '{theme_id}' not found. Available predefined themes: {list(PREDEFINED_THEMES.keys())}"
    )


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
    - layout: Layout type (L02, L25, L29)

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
    - layout: Layout type (L02, L25, L29)
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
            "L02", "L25", "L29",
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
    - new_layout: New layout type (L02, L25, L29)
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
            "L02", "L25", "L29",
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


# ==================== Generic Element CRUD Helpers ====================

def get_next_element_z_index(elements: list, base_z: int = 100) -> int:
    """Get the next available z-index for a new element."""
    if not elements:
        return base_z
    max_z = max(elem.get('z_index', base_z) for elem in elements)
    return max_z + 1


def find_element_by_id(elements: list, element_id: str):
    """Find an element by ID in a list. Returns (index, element) or (None, None)."""
    for idx, elem in enumerate(elements):
        if elem.get("id") == element_id:
            return idx, elem
    return None, None


# ==================== Image Element CRUD Endpoints ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/images", response_model=ImageResponse)
async def create_image(
    presentation_id: str,
    slide_index: int,
    request: ImageCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Create a new image element on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        images = presentation["slides"][slide_index]["images"]

        if len(images) >= 20:
            raise HTTPException(status_code=400, detail="Maximum 20 images per slide")

        # Get parent slide ID for cascade delete support
        parent_slide_id = presentation["slides"][slide_index].get("slide_id")

        new_image = ImageElement(
            parent_slide_id=parent_slide_id,
            position=request.position,
            image_url=request.image_url,
            alt_text=request.alt_text,
            object_fit=request.object_fit or "cover",
            z_index=request.z_index or get_next_element_z_index(images, 100)
        )

        images.append(new_image.model_dump())

        summary = change_summary or f"Added image to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ImageResponse(
            success=True,
            image=new_image,
            message=f"Image created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating image: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/images", response_model=ImageListResponse)
async def list_images(presentation_id: str, slide_index: int):
    """Get all images on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        images = slide.get("images", [])

        return ImageListResponse(
            success=True,
            slide_index=slide_index,
            images=[ImageElement(**img) for img in images],
            count=len(images)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing images: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}", response_model=ImageResponse)
async def get_image(presentation_id: str, slide_index: int, image_id: str):
    """Get a specific image element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        images = slide.get("images", [])

        _, image = find_element_by_id(images, image_id)
        if image is None:
            raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")

        return ImageResponse(
            success=True,
            image=ImageElement(**image),
            message="Image found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting image: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}", response_model=ImageResponse)
async def update_image(
    presentation_id: str,
    slide_index: int,
    image_id: str,
    request: ImageUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Update an existing image element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        images = presentation["slides"][slide_index]["images"]

        image_idx, image = find_element_by_id(images, image_id)
        if image_idx is None:
            raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")

        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    image["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    image[key] = value

        summary = change_summary or f"Updated image on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ImageResponse(
            success=True,
            image=ImageElement(**image),
            message="Image updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating image: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/images/{image_id}")
async def delete_image(
    presentation_id: str,
    slide_index: int,
    image_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete an image from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        images = presentation["slides"][slide_index]["images"]

        original_count = len(images)
        images[:] = [img for img in images if img.get("id") != image_id]

        if len(images) == original_count:
            raise HTTPException(status_code=404, detail=f"Image not found: {image_id}")

        summary = change_summary or f"Deleted image from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Image deleted",
            "image_id": image_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting image: {str(e)}")


# ==================== Chart Element CRUD Endpoints ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/charts", response_model=ChartResponse)
async def create_chart(
    presentation_id: str,
    slide_index: int,
    request: ChartCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Create a new chart element on a slide."""
    try:
        logger.debug(f"Creating chart on presentation {presentation_id}, slide {slide_index}")

        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        charts = presentation["slides"][slide_index]["charts"]

        if len(charts) >= 10:
            raise HTTPException(status_code=400, detail="Maximum 10 charts per slide")

        parent_slide_id = presentation["slides"][slide_index].get("slide_id")

        new_chart = ChartElement(
            parent_slide_id=parent_slide_id,
            position=request.position,
            chart_type=request.chart_type,
            chart_config=request.chart_config,
            chart_html=request.chart_html,
            z_index=request.z_index or get_next_element_z_index(charts, 100)
        )

        charts.append(new_chart.model_dump())

        summary = change_summary or f"Added chart to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ChartResponse(
            success=True,
            chart=new_chart,
            message=f"Chart created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chart: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/charts", response_model=ChartListResponse)
async def list_charts(presentation_id: str, slide_index: int):
    """Get all charts on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        charts = slide.get("charts", [])

        return ChartListResponse(
            success=True,
            slide_index=slide_index,
            charts=[ChartElement(**c) for c in charts],
            count=len(charts)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing charts: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}", response_model=ChartResponse)
async def get_chart(presentation_id: str, slide_index: int, chart_id: str):
    """Get a specific chart element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        charts = slide.get("charts", [])

        _, chart = find_element_by_id(charts, chart_id)
        if chart is None:
            raise HTTPException(status_code=404, detail=f"Chart not found: {chart_id}")

        return ChartResponse(
            success=True,
            chart=ChartElement(**chart),
            message="Chart found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chart: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}", response_model=ChartResponse)
async def update_chart(
    presentation_id: str,
    slide_index: int,
    chart_id: str,
    request: ChartUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Update an existing chart element."""
    try:
        logger.debug(f"Updating chart {chart_id} on presentation {presentation_id}, slide {slide_index}")

        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        charts = presentation["slides"][slide_index]["charts"]

        chart_idx, chart = find_element_by_id(charts, chart_id)
        if chart_idx is None:
            raise HTTPException(status_code=404, detail=f"Chart not found: {chart_id}")

        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    chart["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    chart[key] = value

        summary = change_summary or f"Updated chart on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ChartResponse(
            success=True,
            chart=ChartElement(**chart),
            message="Chart updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating chart: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/charts/{chart_id}")
async def delete_chart(
    presentation_id: str,
    slide_index: int,
    chart_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete a chart from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        charts = presentation["slides"][slide_index]["charts"]

        original_count = len(charts)
        charts[:] = [c for c in charts if c.get("id") != chart_id]

        if len(charts) == original_count:
            raise HTTPException(status_code=404, detail=f"Chart not found: {chart_id}")

        summary = change_summary or f"Deleted chart from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Chart deleted",
            "chart_id": chart_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chart: {str(e)}")


# ==================== Diagram Element CRUD Endpoints ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/diagrams", response_model=DiagramResponse)
async def create_diagram(
    presentation_id: str,
    slide_index: int,
    request: DiagramCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Create a new diagram element on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        diagrams = presentation["slides"][slide_index]["diagrams"]

        if len(diagrams) >= 10:
            raise HTTPException(status_code=400, detail="Maximum 10 diagrams per slide")

        parent_slide_id = presentation["slides"][slide_index].get("slide_id")

        new_diagram = DiagramElement(
            parent_slide_id=parent_slide_id,
            position=request.position,
            diagram_type=request.diagram_type,
            mermaid_code=request.mermaid_code,
            svg_content=request.svg_content,
            html_content=request.html_content,
            direction=request.direction or "TB",
            theme=request.theme or "default",
            z_index=request.z_index or get_next_element_z_index(diagrams, 100)
        )

        diagrams.append(new_diagram.model_dump())

        summary = change_summary or f"Added diagram to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return DiagramResponse(
            success=True,
            diagram=new_diagram,
            message=f"Diagram created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating diagram: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/diagrams", response_model=DiagramListResponse)
async def list_diagrams(presentation_id: str, slide_index: int):
    """Get all diagrams on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        diagrams = slide.get("diagrams", [])

        return DiagramListResponse(
            success=True,
            slide_index=slide_index,
            diagrams=[DiagramElement(**d) for d in diagrams],
            count=len(diagrams)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing diagrams: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}", response_model=DiagramResponse)
async def get_diagram(presentation_id: str, slide_index: int, diagram_id: str):
    """Get a specific diagram element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        diagrams = slide.get("diagrams", [])

        _, diagram = find_element_by_id(diagrams, diagram_id)
        if diagram is None:
            raise HTTPException(status_code=404, detail=f"Diagram not found: {diagram_id}")

        return DiagramResponse(
            success=True,
            diagram=DiagramElement(**diagram),
            message="Diagram found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting diagram: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}", response_model=DiagramResponse)
async def update_diagram(
    presentation_id: str,
    slide_index: int,
    diagram_id: str,
    request: DiagramUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Update an existing diagram element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        diagrams = presentation["slides"][slide_index]["diagrams"]

        diagram_idx, diagram = find_element_by_id(diagrams, diagram_id)
        if diagram_idx is None:
            raise HTTPException(status_code=404, detail=f"Diagram not found: {diagram_id}")

        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    diagram["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    diagram[key] = value

        summary = change_summary or f"Updated diagram on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return DiagramResponse(
            success=True,
            diagram=DiagramElement(**diagram),
            message="Diagram updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating diagram: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/diagrams/{diagram_id}")
async def delete_diagram(
    presentation_id: str,
    slide_index: int,
    diagram_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete a diagram from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        diagrams = presentation["slides"][slide_index]["diagrams"]

        original_count = len(diagrams)
        diagrams[:] = [d for d in diagrams if d.get("id") != diagram_id]

        if len(diagrams) == original_count:
            raise HTTPException(status_code=404, detail=f"Diagram not found: {diagram_id}")

        summary = change_summary or f"Deleted diagram from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Diagram deleted",
            "diagram_id": diagram_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting diagram: {str(e)}")


# ==================== Infographic Element CRUD Endpoints ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/infographics", response_model=InfographicResponse)
async def create_infographic(
    presentation_id: str,
    slide_index: int,
    request: InfographicCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Create a new infographic element on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        infographics = presentation["slides"][slide_index]["infographics"]

        if len(infographics) >= 10:
            raise HTTPException(status_code=400, detail="Maximum 10 infographics per slide")

        parent_slide_id = presentation["slides"][slide_index].get("slide_id")

        new_infographic = InfographicElement(
            parent_slide_id=parent_slide_id,
            position=request.position,
            infographic_type=request.infographic_type,
            svg_content=request.svg_content,
            html_content=request.html_content,
            items=request.items,
            z_index=request.z_index or get_next_element_z_index(infographics, 100)
        )

        infographics.append(new_infographic.model_dump())

        summary = change_summary or f"Added infographic to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return InfographicResponse(
            success=True,
            infographic=new_infographic,
            message=f"Infographic created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating infographic: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/infographics", response_model=InfographicListResponse)
async def list_infographics(presentation_id: str, slide_index: int):
    """Get all infographics on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        infographics = slide.get("infographics", [])

        return InfographicListResponse(
            success=True,
            slide_index=slide_index,
            infographics=[InfographicElement(**i) for i in infographics],
            count=len(infographics)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing infographics: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}", response_model=InfographicResponse)
async def get_infographic(presentation_id: str, slide_index: int, infographic_id: str):
    """Get a specific infographic element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        infographics = slide.get("infographics", [])

        _, infographic = find_element_by_id(infographics, infographic_id)
        if infographic is None:
            raise HTTPException(status_code=404, detail=f"Infographic not found: {infographic_id}")

        return InfographicResponse(
            success=True,
            infographic=InfographicElement(**infographic),
            message="Infographic found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting infographic: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}", response_model=InfographicResponse)
async def update_infographic(
    presentation_id: str,
    slide_index: int,
    infographic_id: str,
    request: InfographicUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Update an existing infographic element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        infographics = presentation["slides"][slide_index]["infographics"]

        infographic_idx, infographic = find_element_by_id(infographics, infographic_id)
        if infographic_idx is None:
            raise HTTPException(status_code=404, detail=f"Infographic not found: {infographic_id}")

        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    infographic["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    infographic[key] = value

        summary = change_summary or f"Updated infographic on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return InfographicResponse(
            success=True,
            infographic=InfographicElement(**infographic),
            message="Infographic updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating infographic: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/infographics/{infographic_id}")
async def delete_infographic(
    presentation_id: str,
    slide_index: int,
    infographic_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete an infographic from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])
        infographics = presentation["slides"][slide_index]["infographics"]

        original_count = len(infographics)
        infographics[:] = [i for i in infographics if i.get("id") != infographic_id]

        if len(infographics) == original_count:
            raise HTTPException(status_code=404, detail=f"Infographic not found: {infographic_id}")

        summary = change_summary or f"Deleted infographic from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Infographic deleted",
            "infographic_id": infographic_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting infographic: {str(e)}")


# ==================== Content Element CRUD Endpoints ====================

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/contents", response_model=ContentResponse)
async def create_content(
    presentation_id: str,
    slide_index: int,
    request: ContentCreateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Create a new content element on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])

        # Ensure contents array exists
        if 'contents' not in presentation["slides"][slide_index]:
            presentation["slides"][slide_index]["contents"] = []
        contents = presentation["slides"][slide_index]["contents"]

        if len(contents) >= 5:
            raise HTTPException(status_code=400, detail="Maximum 5 content elements per slide")

        parent_slide_id = presentation["slides"][slide_index].get("slide_id")

        new_content = ContentElement(
            parent_slide_id=parent_slide_id,
            slot_name=request.slot_name,
            position=request.position,
            content_html=request.content_html or "",
            content_type=request.content_type or "html",
            format_owner=request.format_owner or "text_service",
            z_index=request.z_index or get_next_element_z_index(contents, 100)
        )

        contents.append(new_content.model_dump())

        summary = change_summary or f"Added content element to slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ContentResponse(
            success=True,
            content=new_content,
            message=f"Content element created on slide {slide_index + 1}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating content element: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/contents", response_model=ContentListResponse)
async def list_contents(presentation_id: str, slide_index: int):
    """Get all content elements on a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        contents = slide.get("contents", [])

        return ContentListResponse(
            success=True,
            slide_index=slide_index,
            contents=[ContentElement(**c) for c in contents],
            count=len(contents)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing content elements: {str(e)}")


@app.get("/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}", response_model=ContentResponse)
async def get_content(presentation_id: str, slide_index: int, content_id: str):
    """Get a specific content element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        slide = ensure_slide_elements(presentation["slides"][slide_index])
        contents = slide.get("contents", [])

        _, content = find_element_by_id(contents, content_id)
        if content is None:
            raise HTTPException(status_code=404, detail=f"Content element not found: {content_id}")

        return ContentResponse(
            success=True,
            content=ContentElement(**content),
            message="Content element found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting content element: {str(e)}")


@app.put("/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}", response_model=ContentResponse)
async def update_content(
    presentation_id: str,
    slide_index: int,
    content_id: str,
    request: ContentUpdateRequest,
    created_by: str = "user",
    change_summary: str = None
):
    """Update an existing content element."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])

        if 'contents' not in presentation["slides"][slide_index]:
            presentation["slides"][slide_index]["contents"] = []
        contents = presentation["slides"][slide_index]["contents"]

        content_idx, content = find_element_by_id(contents, content_id)
        if content_idx is None:
            raise HTTPException(status_code=404, detail=f"Content element not found: {content_id}")

        update_data = request.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                if key == "position":
                    content["position"] = value.model_dump() if hasattr(value, 'model_dump') else value
                else:
                    content[key] = value

        summary = change_summary or f"Updated content element on slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return ContentResponse(
            success=True,
            content=ContentElement(**content),
            message="Content element updated"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating content element: {str(e)}")


@app.delete("/api/presentations/{presentation_id}/slides/{slide_index}/contents/{content_id}")
async def delete_content(
    presentation_id: str,
    slide_index: int,
    content_id: str,
    created_by: str = "user",
    change_summary: str = None
):
    """Delete a content element from a slide."""
    try:
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        presentation["slides"][slide_index] = ensure_slide_elements(presentation["slides"][slide_index])

        if 'contents' not in presentation["slides"][slide_index]:
            presentation["slides"][slide_index]["contents"] = []
        contents = presentation["slides"][slide_index]["contents"]

        original_count = len(contents)
        contents[:] = [c for c in contents if c.get("id") != content_id]

        if len(contents) == original_count:
            raise HTTPException(status_code=404, detail=f"Content element not found: {content_id}")

        summary = change_summary or f"Deleted content element from slide {slide_index + 1}"
        await storage.update(
            presentation_id,
            {"slides": presentation["slides"]},
            created_by=created_by,
            change_summary=summary,
            create_version=True
        )

        return JSONResponse(content={
            "success": True,
            "message": "Content element deleted",
            "content_id": content_id
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting content element: {str(e)}")


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


# ==================== Director Service Coordination Endpoints (v7.5.5) ====================
# These endpoints enable the Director Service to coordinate with the Layout Service
# for content-to-layout mapping based on grid dimensions.


@app.get("/capabilities", response_model=CapabilitiesResponse, tags=["Director Integration"])
async def get_capabilities():
    """
    Get Layout Service capabilities for Director coordination.

    Returns service capabilities including:
    - Supported template series (H, C, V, I, S, B, L)
    - Total template count
    - Standard zone definitions
    - Available endpoints
    """
    return {
        "service": "layout-service",
        "version": "7.5.5",
        "status": "healthy",
        "capabilities": {
            "template_series": ["H", "C", "V", "I", "S", "B", "L"],
            "total_templates": len(TEMPLATE_REGISTRY),
            "supports_themes": True,
            "theme_count": len(PREDEFINED_THEMES),
            "exposes_grid_size": True,
            "grid_system": {
                "columns": 32,
                "rows": 18,
                "slide_width": SLIDE_WIDTH,
                "slide_height": SLIDE_HEIGHT
            }
        },
        "template_series": {
            "H": {
                "name": "Hero Series",
                "description": "Full-bleed title, section, and closing slides",
                "count": len(TEMPLATE_CATEGORIES["hero"]["templates"]),
                "use_for": ["title_slides", "section_dividers", "closing_slides"]
            },
            "C": {
                "name": "Content Series",
                "description": "Single content area slides",
                "count": len(TEMPLATE_CATEGORIES["content"]["templates"]),
                "use_for": ["text_content", "single_chart", "single_diagram", "infographic"]
            },
            "V": {
                "name": "Visual + Text Series",
                "description": "Visual element with text insights",
                "count": len(TEMPLATE_CATEGORIES["visual"]["templates"]),
                "use_for": ["chart_analysis", "diagram_explanation", "image_description"]
            },
            "I": {
                "name": "Image Split Series",
                "description": "Full-height image with content",
                "count": len(TEMPLATE_CATEGORIES["image"]["templates"]),
                "use_for": ["image_heavy_content", "photo_stories"]
            },
            "S": {
                "name": "Split Series",
                "description": "Two-column layouts",
                "count": len(TEMPLATE_CATEGORIES["split"]["templates"]),
                "use_for": ["comparisons", "before_after", "two_charts"]
            },
            "B": {
                "name": "Blank Series",
                "description": "Empty canvas",
                "count": len(TEMPLATE_CATEGORIES["blank"]["templates"]),
                "use_for": ["custom_layouts", "freeform"]
            },
            "L": {
                "name": "Backend Layout Series",
                "description": "Core backend layouts for Director/Text Service",
                "count": len(TEMPLATE_CATEGORIES["backend"]["templates"]),
                "use_for": ["director_generated", "text_service", "analytics_service"]
            }
        },
        "standard_zones": {
            "title": {"required": True, "description": "Slide title area"},
            "subtitle": {"required": False, "description": "Optional subtitle"},
            "content": {"required": True, "description": "Primary content area"},
            "footer": {"required": False, "description": "Footer area"},
            "logo": {"required": False, "description": "Company logo area"}
        },
        "endpoints": {
            "capabilities": "GET /capabilities",
            "list_layouts": "GET /api/layouts",
            "get_layout": "GET /api/layouts/{layout_id}",
            "recommend_layout": "POST /api/recommend-layout",
            "can_fit": "POST /api/can-fit"
        }
    }


@app.get("/api/layouts", response_model=LayoutListResponse, tags=["Director Integration"])
async def list_layouts(category: str = None):
    """
    List all available layouts/templates with metadata.

    Query Parameters:
    - category: Filter by category (hero, content, visual, image, split, blank, backend)

    Returns all 26 templates with:
    - Basic metadata (id, name, series, category)
    - Primary content types
    - Main content dimensions
    """
    layouts = []

    template_ids = get_all_template_ids()
    if category:
        category_def = TEMPLATE_CATEGORIES.get(category)
        if category_def:
            template_ids = category_def["templates"]

    for template_id in template_ids:
        template = TEMPLATE_REGISTRY.get(template_id)
        if not template:
            continue

        # Get main content slot dimensions
        main_slots = get_main_content_slots(template_id)
        main_dimensions = None
        primary_content_types = []

        if main_slots:
            # Use the first main content slot for dimensions
            first_slot = main_slots[0]
            if "pixels" in first_slot:
                main_dimensions = SlotPixels(
                    x=first_slot["pixels"]["x"],
                    y=first_slot["pixels"]["y"],
                    width=first_slot["pixels"]["width"],
                    height=first_slot["pixels"]["height"]
                )
            # Collect content types from all main slots
            for slot in main_slots:
                primary_content_types.extend(slot.get("accepts", []))
            primary_content_types = list(set(primary_content_types))

        layouts.append(LayoutSummary(
            layout_id=template_id,
            name=template["name"],
            series=template["series"],
            category=template["category"],
            description=template["description"],
            theming_enabled=template.get("theming_enabled", True),
            base_layout=template.get("base_layout"),
            primary_content_types=primary_content_types,
            main_content_dimensions=main_dimensions
        ))

    # Build categories dict
    categories = {}
    for cat_name, cat_def in TEMPLATE_CATEGORIES.items():
        categories[cat_name] = cat_def["templates"]

    return LayoutListResponse(
        layouts=layouts,
        total=len(layouts),
        categories=categories
    )


@app.get("/api/layouts/{layout_id}", response_model=LayoutDetailResponse, tags=["Director Integration"])
async def get_layout_details(layout_id: str):
    """
    Get detailed layout specification with exact content zone dimensions.

    This is the CRITICAL endpoint for Director Service - returns:
    - Full slot definitions with grid positions
    - Pixel dimensions for each slot
    - Content type constraints
    - Format ownership information

    Path Parameters:
    - layout_id: Layout/template ID (e.g., L25, C1-text, H1-structured)
    """
    template = get_template_with_pixels(layout_id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Layout '{layout_id}' not found. Valid layouts: {get_all_template_ids()}"
        )

    # Convert slots to SlotDefinition format
    slots_dict = {}
    for slot_name, slot_def in template.get("slots", {}).items():
        slot_data = {
            "grid_row": slot_def.get("grid_row", "1/19"),
            "grid_column": slot_def.get("grid_column", "1/33"),
            "tag": slot_def.get("tag", "content"),
            "accepts": slot_def.get("accepts", ["content"]),
            "required": slot_def.get("required", False),
            "description": slot_def.get("description"),
            "default_text": slot_def.get("default_text"),
            "format_owner": slot_def.get("format_owner")
        }
        # Add pixel dimensions if available
        if "pixels" in slot_def:
            slot_data["pixels"] = SlotPixels(
                x=slot_def["pixels"]["x"],
                y=slot_def["pixels"]["y"],
                width=slot_def["pixels"]["width"],
                height=slot_def["pixels"]["height"]
            )
        slots_dict[slot_name] = slot_data

    return LayoutDetailResponse(
        layout_id=layout_id,
        name=template["name"],
        series=template["series"],
        category=template["category"],
        description=template["description"],
        theming_enabled=template.get("theming_enabled", True),
        base_layout=template.get("base_layout"),
        slide_dimensions={
            "width": SLIDE_WIDTH,
            "height": SLIDE_HEIGHT,
            "unit": "pixels"
        },
        slots=slots_dict,
        defaults=template.get("defaults", {})
    )


@app.post("/api/recommend-layout", response_model=LayoutRecommendationResponse, tags=["Director Integration"])
async def recommend_layout(request: LayoutRecommendationRequest):
    """
    Recommend best layout for given content type and requirements.

    Request Body:
    - content_type: Type of content (chart, diagram, text, hero, comparison, image, infographic)
    - topic_count: Number of topics/items to display (1-10)
    - service: Requesting service (director, text-service, analytics-service)
    - variant: Content variant (single, split, comparison, etc.)
    - preferences: Additional preferences

    Returns ranked layout recommendations with confidence scores.
    """
    recommendations = []

    # Hero content
    if request.content_type == "hero":
        recommendations.append(LayoutRecommendation(
            layout_id="H1-structured",
            confidence=0.95,
            reason="Structured hero slide with title, subtitle, and author info",
            main_content_slots=get_main_content_slots("H1-structured")
        ))
        recommendations.append(LayoutRecommendation(
            layout_id="L29",
            confidence=0.90,
            reason="Full-bleed hero canvas for AI-generated content",
            main_content_slots=get_main_content_slots("L29")
        ))

    # Section divider
    elif request.content_type == "section":
        recommendations.append(LayoutRecommendation(
            layout_id="H2-section",
            confidence=0.95,
            reason="Section divider with large number and title",
            main_content_slots=get_main_content_slots("H2-section")
        ))

    # Closing slide
    elif request.content_type == "closing":
        recommendations.append(LayoutRecommendation(
            layout_id="H3-closing",
            confidence=0.95,
            reason="Thank you slide with contact info",
            main_content_slots=get_main_content_slots("H3-closing")
        ))

    # Chart content
    elif request.content_type == "chart":
        if request.topic_count == 1:
            recommendations.append(LayoutRecommendation(
                layout_id="C3-chart",
                confidence=0.95,
                reason="Single chart with full-width content area",
                main_content_slots=get_main_content_slots("C3-chart")
            ))
        elif request.topic_count == 2:
            recommendations.append(LayoutRecommendation(
                layout_id="S3-two-visuals",
                confidence=0.95,
                reason="Two charts side-by-side with captions",
                main_content_slots=get_main_content_slots("S3-two-visuals")
            ))
        # Chart with analysis text
        if request.variant == "with_analysis":
            recommendations.insert(0, LayoutRecommendation(
                layout_id="V2-chart-text",
                confidence=0.98,
                reason="Chart on left with text insights on right",
                main_content_slots=get_main_content_slots("V2-chart-text")
            ))

    # Diagram content
    elif request.content_type == "diagram":
        if request.variant == "with_analysis":
            recommendations.append(LayoutRecommendation(
                layout_id="V3-diagram-text",
                confidence=0.95,
                reason="Diagram on left with text insights on right",
                main_content_slots=get_main_content_slots("V3-diagram-text")
            ))
        else:
            recommendations.append(LayoutRecommendation(
                layout_id="C5-diagram",
                confidence=0.95,
                reason="Full-width diagram area",
                main_content_slots=get_main_content_slots("C5-diagram")
            ))
            recommendations.append(LayoutRecommendation(
                layout_id="L02",
                confidence=0.85,
                reason="Diagram left with text right (backend layout)",
                main_content_slots=get_main_content_slots("L02")
            ))

    # Text content
    elif request.content_type == "text":
        recommendations.append(LayoutRecommendation(
            layout_id="C1-text",
            confidence=0.95,
            reason="Full-width text content area with title and subtitle",
            main_content_slots=get_main_content_slots("C1-text")
        ))
        recommendations.append(LayoutRecommendation(
            layout_id="L25",
            confidence=0.90,
            reason="Main content shell (backend layout for Text Service)",
            main_content_slots=get_main_content_slots("L25")
        ))

    # Infographic content
    elif request.content_type == "infographic":
        if request.variant == "with_analysis":
            recommendations.append(LayoutRecommendation(
                layout_id="V4-infographic-text",
                confidence=0.95,
                reason="Infographic on left with text insights on right",
                main_content_slots=get_main_content_slots("V4-infographic-text")
            ))
        else:
            recommendations.append(LayoutRecommendation(
                layout_id="C4-infographic",
                confidence=0.95,
                reason="Full-width infographic area",
                main_content_slots=get_main_content_slots("C4-infographic")
            ))

    # Image content
    elif request.content_type == "image":
        image_position = request.preferences.get("image_position", "left") if request.preferences else "left"
        if image_position == "left":
            recommendations.append(LayoutRecommendation(
                layout_id="I1-image-left",
                confidence=0.95,
                reason="Full-height image on left with content on right",
                main_content_slots=get_main_content_slots("I1-image-left")
            ))
        else:
            recommendations.append(LayoutRecommendation(
                layout_id="I2-image-right",
                confidence=0.95,
                reason="Full-height image on right with content on left",
                main_content_slots=get_main_content_slots("I2-image-right")
            ))
        # Also suggest with analysis
        recommendations.append(LayoutRecommendation(
            layout_id="V1-image-text",
            confidence=0.85,
            reason="Image with text insights (smaller image area)",
            main_content_slots=get_main_content_slots("V1-image-text")
        ))

    # Comparison content
    elif request.content_type == "comparison":
        recommendations.append(LayoutRecommendation(
            layout_id="S4-comparison",
            confidence=0.95,
            reason="Two-column comparison layout with headers",
            main_content_slots=get_main_content_slots("S4-comparison")
        ))
        recommendations.append(LayoutRecommendation(
            layout_id="S3-two-visuals",
            confidence=0.85,
            reason="Two visuals side-by-side (for visual comparison)",
            main_content_slots=get_main_content_slots("S3-two-visuals")
        ))

    # Default fallback
    if not recommendations:
        recommendations.append(LayoutRecommendation(
            layout_id="L25",
            confidence=0.70,
            reason="Universal fallback - main content shell",
            main_content_slots=get_main_content_slots("L25")
        ))

    return LayoutRecommendationResponse(
        recommended_layouts=recommendations,
        fallback="L25",
        request_summary={
            "content_type": request.content_type,
            "topic_count": request.topic_count,
            "service": request.service,
            "variant": request.variant
        }
    )


@app.post("/api/can-fit", response_model=CanFitResponse, tags=["Director Integration"])
async def can_fit(request: CanFitRequest):
    """
    Validate if content can fit in the specified layout.

    Request Body:
    - layout_id: Layout to check
    - content_zones_needed: Number of content zones required
    - content_type: Type of content (text, chart, diagram, image, etc.)

    Returns whether the content fits and suggests alternatives if not.
    """
    template = get_template(request.layout_id)
    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Layout '{request.layout_id}' not found. Valid layouts: {get_all_template_ids()}"
        )

    # Count available zones that accept the content type
    available_zones = count_slots_accepting(request.layout_id, request.content_type)

    can_fit = available_zones >= request.content_zones_needed

    # Suggest alternative if doesn't fit
    suggested_layout = None
    if not can_fit:
        # Find a layout that can accommodate the content
        if request.content_zones_needed >= 2:
            # Need multiple zones - suggest split layouts
            if request.content_type in ["chart", "diagram", "infographic", "image"]:
                suggested_layout = "S3-two-visuals"
            else:
                suggested_layout = "S4-comparison"
        else:
            # Single zone needed - suggest based on content type
            content_to_layout = {
                "chart": "C3-chart",
                "diagram": "C5-diagram",
                "infographic": "C4-infographic",
                "image": "I1-image-left",
                "text": "C1-text",
                "body": "C1-text",
                "html": "L25"
            }
            suggested_layout = content_to_layout.get(request.content_type, "L25")

    return CanFitResponse(
        can_fit=can_fit,
        layout_id=request.layout_id,
        content_zones_available=available_zones,
        content_zones_needed=request.content_zones_needed,
        suggested_layout=suggested_layout,
        reason=f"Layout '{request.layout_id}' has {available_zones} zone(s) accepting '{request.content_type}', need {request.content_zones_needed}"
    )


# ==================== X-Series Dynamic Layout Endpoints ====================
# v7.5.7: Dynamic layout generation for intelligent content area splitting
#
# X-Series Mapping:
# X1 → C1-text (1800×840px content area)
# X2 → I1-image-left (1200×840px content area)
# X3 → I2-image-right (1140×840px content area)
# X4 → I3-image-left-narrow (1500×840px content area)
# X5 → I4-image-right-narrow (1440×840px content area)

# In-memory cache for dynamic layouts (fallback when Supabase unavailable)
_dynamic_layouts_cache: dict[str, dict] = {}


def _get_supabase_client():
    """Get Supabase client if available, otherwise return None."""
    try:
        from supabase import create_client
        from config import get_settings
        settings = get_settings()
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception:
        pass
    return None


async def _save_dynamic_layout(layout_data: dict) -> bool:
    """Save dynamic layout to Supabase or memory cache."""
    layout_id = layout_data["layout_id"]

    # Try Supabase first
    client = _get_supabase_client()
    if client:
        try:
            # Convert to database format
            db_record = {
                "layout_id": layout_id,
                "base_layout": layout_data["base_layout"],
                "name": layout_data["name"],
                "description": layout_data.get("description"),
                "content_type": layout_data["content_type"],
                "split_pattern": layout_data["split_pattern"],
                "split_direction": layout_data["split_direction"],
                "zone_count": len(layout_data["zones"]),
                "zones": layout_data["zones"],
                "content_area": layout_data["content_area"],
                "is_public": layout_data.get("reusable", True)
            }
            client.table("ls_dynamic_layouts").upsert(db_record).execute()
            return True
        except Exception as e:
            print(f"Supabase save failed: {e}, using memory cache")

    # Fallback to memory cache
    _dynamic_layouts_cache[layout_id] = layout_data
    return True


async def _get_dynamic_layout(layout_id: str) -> dict | None:
    """Get dynamic layout from Supabase or memory cache."""
    # Try Supabase first
    client = _get_supabase_client()
    if client:
        try:
            result = client.table("ls_dynamic_layouts").select("*").eq("layout_id", layout_id).execute()
            if result.data:
                db_record = result.data[0]
                # Convert from database format
                return {
                    "layout_id": db_record["layout_id"],
                    "base_layout": db_record["base_layout"],
                    "name": db_record["name"],
                    "description": db_record.get("description"),
                    "content_type": db_record["content_type"],
                    "zones": db_record["zones"],
                    "split_pattern": db_record["split_pattern"],
                    "split_direction": db_record["split_direction"],
                    "content_area": db_record["content_area"],
                    "reusable": db_record.get("is_public", True),
                    "created_at": db_record.get("created_at")
                }
        except Exception as e:
            print(f"Supabase get failed: {e}, using memory cache")

    # Fallback to memory cache
    return _dynamic_layouts_cache.get(layout_id)


async def _list_dynamic_layouts(base_layout: str = None, content_type: str = None) -> list[dict]:
    """List all dynamic layouts with optional filters."""
    layouts = []

    # Try Supabase first
    client = _get_supabase_client()
    if client:
        try:
            query = client.table("ls_dynamic_layouts").select("*")
            if base_layout:
                query = query.eq("base_layout", base_layout)
            if content_type:
                query = query.eq("content_type", content_type)
            result = query.execute()

            for db_record in result.data:
                layouts.append({
                    "layout_id": db_record["layout_id"],
                    "base_layout": db_record["base_layout"],
                    "name": db_record["name"],
                    "description": db_record.get("description"),
                    "content_type": db_record["content_type"],
                    "zones": db_record["zones"],
                    "split_pattern": db_record["split_pattern"],
                    "split_direction": db_record["split_direction"],
                    "content_area": db_record["content_area"],
                    "reusable": db_record.get("is_public", True),
                    "created_at": db_record.get("created_at")
                })
            return layouts
        except Exception as e:
            print(f"Supabase list failed: {e}, using memory cache")

    # Fallback to memory cache
    for layout_data in _dynamic_layouts_cache.values():
        if base_layout and layout_data.get("base_layout") != base_layout:
            continue
        if content_type and layout_data.get("content_type") != content_type:
            continue
        layouts.append(layout_data)

    return layouts


async def _delete_dynamic_layout(layout_id: str) -> bool:
    """Delete a dynamic layout."""
    # Try Supabase first
    client = _get_supabase_client()
    if client:
        try:
            client.table("ls_dynamic_layouts").delete().eq("layout_id", layout_id).execute()
        except Exception as e:
            print(f"Supabase delete failed: {e}")

    # Also remove from memory cache
    if layout_id in _dynamic_layouts_cache:
        del _dynamic_layouts_cache[layout_id]
        return True

    return True


@app.post("/api/dynamic-layouts/generate", response_model=DynamicLayoutResponse, tags=["X-Series Dynamic Layouts"])
async def generate_dynamic_layout(request: DynamicLayoutRequest):
    """
    Generate a dynamic X-series layout by splitting the content area into zones.

    This endpoint creates a new dynamic layout based on:
    - base_layout: The template to split (C1-text, I1-I4)
    - content_type: Type of content (agenda, use_case, comparison, features, etc.)
    - zone_count: Number of zones to create (2-8)
    - split_pattern: Named pattern or custom

    The generated layout can be used like any other template for content generation.

    Request Body:
    - base_layout: Base template ID (C1-text, I1-I4)
    - content_type: Content type for pattern suggestion
    - zone_count: Number of zones (2-8)
    - split_direction: Optional preferred direction
    - split_pattern: Optional named pattern
    - zone_labels: Optional custom labels
    - custom_ratios: Optional custom split ratios

    Returns:
    - layout_id: Unique ID (e.g., X1-a3f7e8c2)
    - zones: List of zone definitions with coordinates
    - split_pattern: Pattern used
    """
    # Get content area for base layout
    content_area = get_content_area(request.base_layout)
    if not content_area:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid base layout: {request.base_layout}. Valid options: {list(CONTENT_AREAS.keys())}"
        )

    # Determine split pattern
    pattern_name = request.split_pattern
    if not pattern_name:
        # Try to suggest based on content type
        pattern_name = suggest_pattern_for_content_type(request.content_type, request.zone_count)

    # Generate zones
    zones_data = []
    if pattern_name and get_split_pattern(pattern_name):
        # Use preconfigured pattern
        zones_data = create_zones_from_pattern(
            request.base_layout,
            pattern_name,
            request.zone_labels
        )
    elif request.custom_ratios:
        # Use custom ratios
        direction = request.split_direction or "horizontal"
        zones_data = create_custom_zones(
            request.base_layout,
            direction,
            request.custom_ratios,
            request.zone_labels
        )
        pattern_name = "custom"
    else:
        # Default: equal split in preferred direction
        direction = request.split_direction or "horizontal"
        equal_ratios = [1.0 / request.zone_count] * request.zone_count
        zones_data = create_custom_zones(
            request.base_layout,
            direction,
            equal_ratios,
            request.zone_labels
        )
        pattern_name = f"equal-{request.zone_count}-{direction}"

    # Create zone config for hash generation
    zone_config = {
        "base": request.base_layout,
        "pattern": pattern_name,
        "zones": len(zones_data),
        "direction": request.split_direction or "horizontal"
    }

    # Generate unique layout ID
    layout_id = generate_layout_id(request.base_layout, zone_config)

    # Check if this layout already exists
    existing = await _get_dynamic_layout(layout_id)
    if existing:
        # Return existing layout
        zones = [ZoneDefinition(
            zone_id=z["zone_id"],
            label=z.get("label"),
            grid_row=z["grid_row"],
            grid_column=z["grid_column"],
            pixels=ZonePixels(**z["pixels"]),
            content_type_hint=z.get("content_type_hint"),
            z_index=z.get("z_index", 100)
        ) for z in existing["zones"]]

        return DynamicLayoutResponse(
            layout_id=layout_id,
            base_layout=request.base_layout,
            name=existing["name"],
            description=existing.get("description"),
            content_type=existing["content_type"],
            zones=zones,
            split_pattern=existing["split_pattern"],
            split_direction=existing["split_direction"],
            content_area=ZonePixels(**existing["content_area"]),
            reusable=True,
            created_at=existing.get("created_at")
        )

    # Build zone definitions
    zones = [ZoneDefinition(
        zone_id=z["zone_id"],
        label=z.get("label"),
        grid_row=z["grid_row"],
        grid_column=z["grid_column"],
        pixels=ZonePixels(**z["pixels"]),
        content_type_hint=z.get("content_type_hint"),
        z_index=z.get("z_index", 100)
    ) for z in zones_data]

    # Create layout name
    x_series = get_x_series_number(request.base_layout)
    layout_name = f"X{x_series} {request.content_type.title()} ({len(zones)} zones)"

    # Get split direction
    split_direction = request.split_direction
    if not split_direction and pattern_name:
        pattern = get_split_pattern(pattern_name)
        if pattern:
            split_direction = pattern.get("direction", "horizontal")
    split_direction = split_direction or "horizontal"

    # Create response
    response = DynamicLayoutResponse(
        layout_id=layout_id,
        base_layout=request.base_layout,
        name=layout_name,
        description=f"Dynamic {request.content_type} layout based on {request.base_layout}",
        content_type=request.content_type,
        zones=zones,
        split_pattern=pattern_name,
        split_direction=split_direction,
        content_area=ZonePixels(**content_area["pixels"]),
        reusable=True,
        created_at=datetime.utcnow().isoformat()
    )

    # Save to storage
    layout_data = {
        "layout_id": layout_id,
        "base_layout": request.base_layout,
        "name": layout_name,
        "description": response.description,
        "content_type": request.content_type,
        "zones": zones_data,
        "split_pattern": pattern_name,
        "split_direction": split_direction,
        "content_area": content_area["pixels"],
        "reusable": True,
        "created_at": response.created_at
    }
    await _save_dynamic_layout(layout_data)

    return response


# NOTE: These specific routes must come BEFORE the parameterized /{layout_id} route
@app.get("/api/dynamic-layouts/patterns", tags=["X-Series Dynamic Layouts"])
async def list_split_patterns_endpoint():
    """
    List all available preconfigured split patterns.

    Returns a dictionary of pattern names with their configurations:
    - direction: horizontal, vertical, or grid
    - zone_count: Number of zones created
    - ratios: Split ratios
    - labels: Default zone labels
    - description: Pattern description
    """
    return {
        "patterns": SPLIT_PATTERNS,
        "total": len(SPLIT_PATTERNS),
        "by_direction": {
            "horizontal": [p for p, d in SPLIT_PATTERNS.items() if d["direction"] == "horizontal"],
            "vertical": [p for p, d in SPLIT_PATTERNS.items() if d["direction"] == "vertical"],
            "grid": [p for p, d in SPLIT_PATTERNS.items() if d["direction"] == "grid"]
        }
    }


@app.get("/api/dynamic-layouts/base-layouts", tags=["X-Series Dynamic Layouts"])
async def list_base_layouts():
    """
    List all available base layouts for X-series dynamic layout generation.

    Returns information about each base layout including:
    - Content area dimensions
    - X-series mapping
    - Grid coordinates
    """
    base_layouts = []
    for base_id, content_area in CONTENT_AREAS.items():
        base_layouts.append({
            "base_layout": base_id,
            "x_series": f"X{X_SERIES_MAP.get(base_id, 0)}",
            "content_area": {
                "grid_row": content_area["grid_row"],
                "grid_column": content_area["grid_column"],
                "pixels": content_area["pixels"]
            },
            "description": TEMPLATE_REGISTRY.get(base_id, {}).get("description", "")
        })

    return {
        "base_layouts": base_layouts,
        "total": len(base_layouts),
        "x_series_mapping": X_SERIES_MAP
    }


@app.get("/api/dynamic-layouts/{layout_id}", response_model=DynamicLayoutResponse, tags=["X-Series Dynamic Layouts"])
async def get_dynamic_layout_details(layout_id: str):
    """
    Get details of a specific dynamic X-series layout.

    Path Parameters:
    - layout_id: Dynamic layout ID (e.g., X1-a3f7e8c2)

    Returns the full layout specification including:
    - Zone definitions with grid and pixel coordinates
    - Split pattern used
    - Content area dimensions
    """
    layout_data = await _get_dynamic_layout(layout_id)

    if not layout_data:
        raise HTTPException(
            status_code=404,
            detail=f"Dynamic layout '{layout_id}' not found"
        )

    # Convert zones to ZoneDefinition models
    zones = [ZoneDefinition(
        zone_id=z["zone_id"],
        label=z.get("label"),
        grid_row=z["grid_row"],
        grid_column=z["grid_column"],
        pixels=ZonePixels(**z["pixels"]),
        content_type_hint=z.get("content_type_hint"),
        z_index=z.get("z_index", 100)
    ) for z in layout_data["zones"]]

    return DynamicLayoutResponse(
        layout_id=layout_data["layout_id"],
        base_layout=layout_data["base_layout"],
        name=layout_data["name"],
        description=layout_data.get("description"),
        content_type=layout_data["content_type"],
        zones=zones,
        split_pattern=layout_data["split_pattern"],
        split_direction=layout_data["split_direction"],
        content_area=ZonePixels(**layout_data["content_area"]),
        reusable=layout_data.get("reusable", True),
        created_at=layout_data.get("created_at")
    )


@app.get("/api/dynamic-layouts", response_model=DynamicLayoutListResponse, tags=["X-Series Dynamic Layouts"])
async def list_dynamic_layouts(
    base_layout: str = None,
    content_type: str = None
):
    """
    List all dynamic X-series layouts with optional filters.

    Query Parameters:
    - base_layout: Filter by base template (C1-text, I1-I4)
    - content_type: Filter by content type (agenda, use_case, etc.)

    Returns:
    - layouts: List of dynamic layouts
    - total: Total count
    - by_base: Counts grouped by base template
    - by_content_type: Counts grouped by content type
    """
    layouts_data = await _list_dynamic_layouts(base_layout, content_type)

    # Convert to response models
    layouts = []
    by_base: dict[str, int] = {}
    by_content_type: dict[str, int] = {}

    for data in layouts_data:
        zones = [ZoneDefinition(
            zone_id=z["zone_id"],
            label=z.get("label"),
            grid_row=z["grid_row"],
            grid_column=z["grid_column"],
            pixels=ZonePixels(**z["pixels"]),
            content_type_hint=z.get("content_type_hint"),
            z_index=z.get("z_index", 100)
        ) for z in data["zones"]]

        layouts.append(DynamicLayoutResponse(
            layout_id=data["layout_id"],
            base_layout=data["base_layout"],
            name=data["name"],
            description=data.get("description"),
            content_type=data["content_type"],
            zones=zones,
            split_pattern=data["split_pattern"],
            split_direction=data["split_direction"],
            content_area=ZonePixels(**data["content_area"]),
            reusable=data.get("reusable", True),
            created_at=data.get("created_at")
        ))

        # Count by base layout
        base = data["base_layout"]
        by_base[base] = by_base.get(base, 0) + 1

        # Count by content type
        ct = data["content_type"]
        by_content_type[ct] = by_content_type.get(ct, 0) + 1

    return DynamicLayoutListResponse(
        layouts=layouts,
        total=len(layouts),
        by_base=by_base,
        by_content_type=by_content_type
    )


@app.delete("/api/dynamic-layouts/{layout_id}", tags=["X-Series Dynamic Layouts"])
async def delete_dynamic_layout(layout_id: str):
    """
    Delete a dynamic X-series layout.

    Path Parameters:
    - layout_id: Dynamic layout ID to delete (e.g., X1-a3f7e8c2)

    Note: This only deletes from storage. Slides already using this layout
    will continue to work but the layout cannot be reused.
    """
    # Check if layout exists
    layout_data = await _get_dynamic_layout(layout_id)
    if not layout_data:
        raise HTTPException(
            status_code=404,
            detail=f"Dynamic layout '{layout_id}' not found"
        )

    # Delete
    await _delete_dynamic_layout(layout_id)

    return {
        "success": True,
        "message": f"Dynamic layout '{layout_id}' deleted",
        "deleted_layout": layout_id
    }


# ==================== Grid Element API (v7.5.9) ====================
# Simplified API for adding positioned elements using start_row/start_col/width/height format

@app.post("/api/presentations/{presentation_id}/slides/{slide_index}/elements", response_model=AddElementResponse, tags=["Grid Element API"])
async def add_positioned_element(
    presentation_id: str,
    slide_index: int,
    request: AddElementRequest,
    created_by: str = "api",
    change_summary: str = None
):
    """
    Add an element at specific grid coordinates.

    This endpoint provides a simplified interface for adding positioned elements
    using start_row/start_col/width/height format instead of grid_row/grid_column strings.

    Grid System: 32 columns x 18 rows (60px cells on 1920x1080)
    Content Safe Zone: rows 4-17, columns 2-31

    Request body:
    - element_type: TEXT_BOX, IMAGE, or CHART
    - html: HTML content for the element
    - start_row: Top-left row position (1-18)
    - start_col: Top-left column position (1-32)
    - width: Width in grid cells (1-32)
    - height: Height in grid cells (1-18)
    - draggable: Whether user can drag to reposition (default: true)
    - resizable: Whether user can resize (default: true)
    - z_index: Layer order, higher = on top (default: 100)

    Example:
    ```json
    {
        "element_type": "TEXT_BOX",
        "html": "<div style='padding: 16px;'>Content here</div>",
        "start_row": 4,
        "start_col": 2,
        "width": 9,
        "height": 5,
        "draggable": true,
        "resizable": true,
        "z_index": 100
    }
    ```
    This creates a text box at rows 4-8, columns 2-10.
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if slide_index < 0 or slide_index >= len(presentation.get("slides", [])):
            raise HTTPException(status_code=400, detail=f"Invalid slide index: {slide_index}")

        # Convert to grid position
        grid_pos = request.to_grid_position()
        grid_row = grid_pos["grid_row"]
        grid_column = grid_pos["grid_column"]

        # Handle different element types
        if request.element_type.upper() == "TEXT_BOX":
            # Ensure text_boxes array exists
            presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
            text_boxes = presentation["slides"][slide_index]["text_boxes"]

            # Check limit
            if len(text_boxes) >= 20:
                raise HTTPException(status_code=400, detail="Maximum 20 text boxes per slide")

            # Create text box with grid position
            new_textbox = TextBox(
                position=TextBoxPosition(
                    grid_row=grid_row,
                    grid_column=grid_column
                ),
                content=request.html,
                style=TextBoxStyle(
                    background_color="transparent",
                    border_color="transparent",
                    border_width=0
                ),
                z_index=request.z_index,
                draggable=request.draggable,
                resizable=request.resizable
            )

            # Add to slide
            text_boxes.append(new_textbox.model_dump())
            element_id = new_textbox.id

            # Save with version tracking
            summary = change_summary or f"Added text box to slide {slide_index + 1} at grid position {grid_row}, {grid_column}"
            await storage.update(
                presentation_id,
                {"slides": presentation["slides"]},
                created_by=created_by,
                change_summary=summary,
                create_version=True
            )

            return AddElementResponse(
                success=True,
                element_id=element_id,
                element_type="TEXT_BOX",
                grid_row=grid_row,
                grid_column=grid_column,
                message=f"Text box created at grid position {grid_row}, {grid_column}"
            )

        elif request.element_type.upper() == "IMAGE":
            # Handle image element creation
            # For now, treat images as text boxes with HTML content
            presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
            text_boxes = presentation["slides"][slide_index]["text_boxes"]

            if len(text_boxes) >= 20:
                raise HTTPException(status_code=400, detail="Maximum 20 elements per slide")

            new_textbox = TextBox(
                position=TextBoxPosition(
                    grid_row=grid_row,
                    grid_column=grid_column
                ),
                content=request.html,
                style=TextBoxStyle(
                    background_color="transparent",
                    border_color="transparent",
                    border_width=0
                ),
                z_index=request.z_index,
                draggable=request.draggable,
                resizable=request.resizable
            )

            text_boxes.append(new_textbox.model_dump())
            element_id = new_textbox.id

            summary = change_summary or f"Added image to slide {slide_index + 1} at grid position {grid_row}, {grid_column}"
            await storage.update(
                presentation_id,
                {"slides": presentation["slides"]},
                created_by=created_by,
                change_summary=summary,
                create_version=True
            )

            return AddElementResponse(
                success=True,
                element_id=element_id,
                element_type="IMAGE",
                grid_row=grid_row,
                grid_column=grid_column,
                message=f"Image element created at grid position {grid_row}, {grid_column}"
            )

        elif request.element_type.upper() == "CHART":
            # Handle chart element creation
            presentation["slides"][slide_index] = ensure_slide_text_boxes(presentation["slides"][slide_index])
            text_boxes = presentation["slides"][slide_index]["text_boxes"]

            if len(text_boxes) >= 20:
                raise HTTPException(status_code=400, detail="Maximum 20 elements per slide")

            new_textbox = TextBox(
                position=TextBoxPosition(
                    grid_row=grid_row,
                    grid_column=grid_column
                ),
                content=request.html,
                style=TextBoxStyle(
                    background_color="transparent",
                    border_color="transparent",
                    border_width=0
                ),
                z_index=request.z_index,
                draggable=request.draggable,
                resizable=request.resizable
            )

            text_boxes.append(new_textbox.model_dump())
            element_id = new_textbox.id

            summary = change_summary or f"Added chart to slide {slide_index + 1} at grid position {grid_row}, {grid_column}"
            await storage.update(
                presentation_id,
                {"slides": presentation["slides"]},
                created_by=created_by,
                change_summary=summary,
                create_version=True
            )

            return AddElementResponse(
                success=True,
                element_id=element_id,
                element_type="CHART",
                grid_row=grid_row,
                grid_column=grid_column,
                message=f"Chart element created at grid position {grid_row}, {grid_column}"
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported element type: {request.element_type}. Use TEXT_BOX, IMAGE, or CHART."
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding positioned element: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding element: {str(e)}")


@app.post("/api/presentations/{presentation_id}/grid-overlay", tags=["Grid Element API"])
async def toggle_grid_overlay(presentation_id: str, show: bool = True):
    """
    Toggle grid overlay visibility for visual debugging.

    Note: The grid overlay is controlled client-side via postMessage.
    This endpoint provides a REST interface for backend-to-backend communication.

    Existing postMessage commands (for frontend reference):
    - {action: 'showGridOverlay'} - Turn grid ON
    - {action: 'hideGridOverlay'} - Turn grid OFF
    - {action: 'toggleGridOverlay'} - Toggle
    - {action: 'isGridOverlayActive'} - Check status
    """
    # This is primarily a notification/documentation endpoint
    # The actual grid overlay is controlled client-side
    return {
        "success": True,
        "presentation_id": presentation_id,
        "grid_overlay": "show" if show else "hide",
        "message": f"Grid overlay {'enabled' if show else 'disabled'}. Use postMessage for client-side control."
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8504))
    uvicorn.run(app, host="0.0.0.0", port=port)
