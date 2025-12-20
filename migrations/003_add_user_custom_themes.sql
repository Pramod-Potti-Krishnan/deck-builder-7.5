-- Migration: 003_add_user_custom_themes
-- Description: Add user custom themes table for theme customization system
-- Version: 7.5.4
-- Date: 2024-12-08

-- ==================== User Custom Themes Table ====================
-- Stores user-created custom themes that can be reused across presentations

CREATE TABLE IF NOT EXISTS ls_user_themes (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- User ownership (required for multi-tenant)
    user_id UUID NOT NULL,

    -- Theme identification
    name VARCHAR(100) NOT NULL,
    description TEXT,

    -- Base theme inheritance (NULL for fully custom themes)
    -- If set, this theme inherits from the predefined theme and overrides specific properties
    base_theme_id VARCHAR(50),

    -- Full theme configuration (JSONB for flexibility)
    -- Structure:
    -- {
    --   "colors": { "primary": "#...", "background": "#...", ... },
    --   "typography": { "font_family": "...", "title_size": "...", ... },
    --   "spacing": { "slide_padding": "...", "element_gap": "...", ... },
    --   "effects": { "border_radius": "...", "shadow_small": "...", ... },
    --   "content_styles": { "h1": {...}, "h2": {...}, ... }
    -- }
    theme_config JSONB NOT NULL,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Sharing settings
    is_public BOOLEAN DEFAULT FALSE,

    -- Constraints
    CONSTRAINT ls_user_themes_name_length CHECK (char_length(name) >= 1)
);

-- ==================== Indexes ====================

-- Index for fast user theme lookups
CREATE INDEX IF NOT EXISTS idx_ls_user_themes_user_id
ON ls_user_themes(user_id);

-- Index for public theme gallery queries
CREATE INDEX IF NOT EXISTS idx_ls_user_themes_public
ON ls_user_themes(is_public)
WHERE is_public = TRUE;

-- Index for searching by base theme
CREATE INDEX IF NOT EXISTS idx_ls_user_themes_base
ON ls_user_themes(base_theme_id)
WHERE base_theme_id IS NOT NULL;

-- ==================== Row Level Security ====================

-- Enable RLS
ALTER TABLE ls_user_themes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own themes
CREATE POLICY ls_user_themes_select_own ON ls_user_themes
    FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can view public themes
CREATE POLICY ls_user_themes_select_public ON ls_user_themes
    FOR SELECT
    USING (is_public = TRUE);

-- Policy: Users can insert their own themes
CREATE POLICY ls_user_themes_insert_own ON ls_user_themes
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own themes
CREATE POLICY ls_user_themes_update_own ON ls_user_themes
    FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can delete their own themes
CREATE POLICY ls_user_themes_delete_own ON ls_user_themes
    FOR DELETE
    USING (auth.uid() = user_id);

-- ==================== Trigger for updated_at ====================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_ls_user_themes_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at on row changes
DROP TRIGGER IF EXISTS ls_user_themes_updated_at_trigger ON ls_user_themes;
CREATE TRIGGER ls_user_themes_updated_at_trigger
    BEFORE UPDATE ON ls_user_themes
    FOR EACH ROW
    EXECUTE FUNCTION update_ls_user_themes_updated_at();

-- ==================== Comments ====================

COMMENT ON TABLE ls_user_themes IS 'User-created custom themes for presentations. Supports full customization of colors, typography, spacing, and effects.';
COMMENT ON COLUMN ls_user_themes.base_theme_id IS 'If set, this theme inherits from a predefined theme (e.g., corporate-blue, minimal-gray). NULL means fully custom.';
COMMENT ON COLUMN ls_user_themes.theme_config IS 'Full theme configuration including colors, typography, spacing, effects, and content_styles as JSONB.';
COMMENT ON COLUMN ls_user_themes.is_public IS 'If TRUE, theme is visible in public theme gallery for all users to use.';
