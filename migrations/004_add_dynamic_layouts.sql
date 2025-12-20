-- Migration: 004_add_dynamic_layouts
-- Description: Add dynamic layouts table for X-series dynamic layout generation
-- Version: 7.5.7
-- Date: 2024-12-17

-- ==================== Dynamic Layouts Table ====================
-- Stores dynamically generated X-series layouts that split content areas
-- into multiple zones based on content analysis.
--
-- X-Series Mapping:
-- X1 → C1-text (1800×840px content area)
-- X2 → I1-image-left (1200×840px content area)
-- X3 → I2-image-right (1140×840px content area)
-- X4 → I3-image-left-narrow (1500×840px content area)
-- X5 → I4-image-right-narrow (1440×840px content area)

CREATE TABLE IF NOT EXISTS ls_dynamic_layouts (
    -- Primary key: layout_id follows pattern X{series}-{hash8}
    -- Example: X1-a3f7e8c2
    layout_id VARCHAR(20) PRIMARY KEY,

    -- Base layout reference
    base_layout VARCHAR(30) NOT NULL,

    -- Layout metadata
    name VARCHAR(100) NOT NULL,
    description TEXT,
    content_type VARCHAR(50) NOT NULL,

    -- Split configuration
    split_pattern VARCHAR(50) NOT NULL,
    split_direction VARCHAR(20) NOT NULL DEFAULT 'horizontal',
    zone_count INTEGER NOT NULL,

    -- Zone definitions (JSONB array)
    -- Structure:
    -- [
    --   {
    --     "zone_id": "zone_1",
    --     "label": "Highlight",
    --     "grid_row": "4/9",
    --     "grid_column": "2/32",
    --     "pixels": {"x": 60, "y": 180, "width": 1800, "height": 300},
    --     "content_type_hint": "heading",
    --     "z_index": 100
    --   },
    --   ...
    -- ]
    zones JSONB NOT NULL,

    -- Content area dimensions (original area that was split)
    content_area JSONB NOT NULL,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP WITH TIME ZONE,

    -- Visibility (public layouts can be reused)
    is_public BOOLEAN DEFAULT TRUE,

    -- Optional: track who created (NULL for system-generated)
    created_by UUID,

    -- Constraints
    CONSTRAINT ls_dynamic_layouts_zone_count CHECK (zone_count >= 2 AND zone_count <= 8),
    CONSTRAINT ls_dynamic_layouts_split_direction CHECK (
        split_direction IN ('horizontal', 'vertical', 'grid')
    ),
    CONSTRAINT ls_dynamic_layouts_base_layout CHECK (
        base_layout IN ('C1-text', 'I1-image-left', 'I2-image-right', 'I3-image-left-narrow', 'I4-image-right-narrow')
    )
);

-- ==================== Indexes ====================

-- Index for fast lookups by base layout
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_base
ON ls_dynamic_layouts(base_layout);

-- Index for content type filtering
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_content_type
ON ls_dynamic_layouts(content_type);

-- Index for pattern lookups (finding existing patterns)
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_pattern
ON ls_dynamic_layouts(split_pattern);

-- Index for public layouts (reusable gallery)
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_public
ON ls_dynamic_layouts(is_public)
WHERE is_public = TRUE;

-- Composite index for common query: find layout by base + content type
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_base_content
ON ls_dynamic_layouts(base_layout, content_type);

-- Index for usage tracking (popular layouts)
CREATE INDEX IF NOT EXISTS idx_ls_dynamic_layouts_usage
ON ls_dynamic_layouts(usage_count DESC);

-- ==================== Trigger for updated_at ====================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_ls_dynamic_layouts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update updated_at on row changes
DROP TRIGGER IF EXISTS ls_dynamic_layouts_updated_at_trigger ON ls_dynamic_layouts;
CREATE TRIGGER ls_dynamic_layouts_updated_at_trigger
    BEFORE UPDATE ON ls_dynamic_layouts
    FOR EACH ROW
    EXECUTE FUNCTION update_ls_dynamic_layouts_updated_at();

-- ==================== Function to Increment Usage ====================

-- Function to increment usage count when a layout is used
CREATE OR REPLACE FUNCTION increment_dynamic_layout_usage(p_layout_id VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    UPDATE ls_dynamic_layouts
    SET usage_count = usage_count + 1,
        last_used_at = NOW()
    WHERE layout_id = p_layout_id;
END;
$$ LANGUAGE plpgsql;

-- ==================== Comments ====================

COMMENT ON TABLE ls_dynamic_layouts IS 'Dynamically generated X-series layouts that split content areas into multiple zones. These layouts are created based on content analysis and can be reused.';
COMMENT ON COLUMN ls_dynamic_layouts.layout_id IS 'Unique identifier following pattern X{series}-{hash8}, e.g., X1-a3f7e8c2';
COMMENT ON COLUMN ls_dynamic_layouts.base_layout IS 'Base template: C1-text for X1, I1-I4 for X2-X5';
COMMENT ON COLUMN ls_dynamic_layouts.split_pattern IS 'Named pattern used: agenda-3-item, comparison-2col, custom, etc.';
COMMENT ON COLUMN ls_dynamic_layouts.zones IS 'JSON array of ZoneDefinition objects with grid and pixel coordinates';
COMMENT ON COLUMN ls_dynamic_layouts.content_area IS 'Original content area dimensions that was split into zones';
COMMENT ON COLUMN ls_dynamic_layouts.usage_count IS 'Number of times this layout has been used for content generation';
