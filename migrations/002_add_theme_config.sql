-- Migration: Add theme_config column to ls_presentations
-- Date: 2024-12-08
-- Description: Adds support for presentation-level theme configuration
--
-- Theme config allows each presentation to specify a theme and optional
-- color overrides for customization.
--
-- Run this SQL in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/YOUR_PROJECT/sql/new

-- Add theme_config column (JSONB for flexible structure)
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS theme_config JSONB;

-- Add comment describing the column structure
COMMENT ON COLUMN ls_presentations.theme_config IS
'Presentation theme configuration. Structure:
{
  "theme_id": "corporate-blue",  // Reference to predefined theme
  "color_overrides": {           // Optional color customizations
    "primary": "#custom-color",
    "accent": "#custom-accent"
  }
}

Available predefined themes:
- corporate-blue: Professional blue theme for business presentations
- minimal-gray: Clean, minimalist gray theme
- vibrant-orange: Energetic orange theme for creative presentations
- dark-mode: Dark theme for low-light environments';

-- Optional: Create index for faster queries by theme
-- (Useful if you need to find all presentations using a specific theme)
-- CREATE INDEX IF NOT EXISTS idx_ls_presentations_theme
-- ON ls_presentations ((theme_config->>'theme_id'));
