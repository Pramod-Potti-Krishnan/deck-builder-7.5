-- Migration: Add derivative_elements column to ls_presentations
-- Date: 2024-12-08
-- Description: Adds support for presentation-level footer and logo configuration
--
-- Derivative elements are presentation-level settings that apply to all slides:
-- - footer: Template with variables like {title}, {page}, {date}, {author}
-- - logo: Image URL to display on all slides
--
-- Run this SQL in the Supabase SQL Editor:
-- https://supabase.com/dashboard/project/YOUR_PROJECT/sql/new

-- Add derivative_elements column (JSONB for flexible structure)
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS derivative_elements JSONB;

-- Add comment describing the column structure
COMMENT ON COLUMN ls_presentations.derivative_elements IS
'Presentation-level elements that appear on all slides. Structure:
{
  "footer": {
    "template": "{title} | Page {page}",  // Template with variables
    "values": {                           // Variable values
      "title": "My Presentation",
      "date": "December 2024",
      "author": "John Smith"
    },
    "style": {                            // Optional style overrides
      "color": "#6b7280",
      "fontSize": "14px"
    }
  },
  "logo": {
    "image_url": "https://...",           // Logo image URL
    "alt_text": "Company Logo"            // Alt text for accessibility
  }
}';

-- Optional: Create index for faster queries on derivative_elements
-- (Useful if you need to query presentations by footer/logo config)
-- CREATE INDEX IF NOT EXISTS idx_ls_presentations_derivative_elements
-- ON ls_presentations USING GIN (derivative_elements);
