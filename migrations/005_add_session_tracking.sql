-- Migration: 005_add_session_tracking.sql
-- Purpose: Add session_id column for presentation persistence
-- Run: Execute in Supabase SQL Editor
-- Author: Claude Code
-- Date: 2025-01-25

-- Add session_id column to enable presentation recovery after browser refresh
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS session_id VARCHAR(100);

-- Add index for fast session-based lookups
CREATE INDEX IF NOT EXISTS idx_ls_presentations_session_id
ON ls_presentations(session_id);

-- Composite index for session + created_at queries (sorted by most recent)
CREATE INDEX IF NOT EXISTS idx_ls_presentations_session_created
ON ls_presentations(session_id, created_at DESC);

-- Add column documentation
COMMENT ON COLUMN ls_presentations.session_id IS
'Session ID for tracking presentations. Enables retrieval by session for persistence across browser refresh.';
