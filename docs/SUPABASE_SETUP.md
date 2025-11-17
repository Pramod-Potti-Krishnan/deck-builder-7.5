# Supabase Setup Guide

**Version**: v7.5.2
**Date**: November 16, 2025
**Purpose**: Step-by-step guide for configuring Supabase for Layout Builder
**Audience**: DevOps, Backend Engineers

---

## 📋 Prerequisites

Before starting, ensure you have:

- [x] Supabase Pro account active
- [x] Access to Supabase dashboard (https://supabase.com/dashboard)
- [x] Railway account with v7.5-main service deployed
- [x] PostgreSQL client installed (optional, for local testing)

---

## Step 1: Access Supabase Project

### 1.1 Log in to Supabase Dashboard

```
URL: https://supabase.com/dashboard
```

### 1.2 Select Existing Project

**Project Details**:
- **Project ID**: `eshvntffcestlfuofwhv`
- **Project Name**: (Your project name)
- **Region**: (Your selected region)
- **Plan**: Supabase Pro

If you don't see your project, create a new one:
1. Click "New Project"
2. Choose organization
3. Name: `layout-builder-prod`
4. Database Password: (Generate strong password)
5. Region: Choose closest to your users (e.g., `us-east-1`)
6. Plan: Pro ($25/month)
7. Click "Create new project"

**Wait**: 2-3 minutes for project provisioning

---

## Step 2: Create PostgreSQL Schema

### 2.1 Navigate to SQL Editor

1. In Supabase dashboard, click **SQL Editor** (left sidebar)
2. Click **"New Query"**

### 2.2 Create Tables

**Copy and paste this entire SQL script**:

```sql
-- ============================================
-- Layout Builder v7.5-main Storage Schema
-- ============================================

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Table 1: presentations
-- Purpose: Store current presentation state
-- ============================================

CREATE TABLE presentations (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Presentation Data
    title VARCHAR(200) NOT NULL,
    slides JSONB NOT NULL,  -- Full slides array with layout + content

    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    updated_by VARCHAR(100),
    restored_from VARCHAR(100),  -- version_id if restored from history
    metadata JSONB  -- Additional metadata for future use
);

-- Indexes for fast queries
CREATE INDEX idx_presentations_created_at ON presentations(created_at DESC);
CREATE INDEX idx_presentations_updated_at ON presentations(updated_at DESC);
CREATE INDEX idx_presentations_title ON presentations USING gin(to_tsvector('english', title));

-- ============================================
-- Table 2: presentation_versions
-- Purpose: Store version history for undo/restore
-- ============================================

CREATE TABLE presentation_versions (
    -- Primary Key
    id SERIAL PRIMARY KEY,

    -- Foreign Key (cascade delete when presentation deleted)
    presentation_id UUID NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,

    -- Version Identity
    version_id VARCHAR(100) NOT NULL,  -- Format: v_20251116_120000_abc123

    -- Version Data
    version_data JSONB NOT NULL,  -- Complete presentation snapshot at this version

    -- Version Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100) NOT NULL,
    change_summary TEXT,

    -- Constraints
    CONSTRAINT unique_presentation_version UNIQUE(presentation_id, version_id)
);

-- Indexes for fast version queries
CREATE INDEX idx_versions_presentation ON presentation_versions(presentation_id, created_at DESC);
CREATE INDEX idx_versions_version_id ON presentation_versions(version_id);

-- ============================================
-- Grant Permissions (if using RLS)
-- ============================================

-- Allow service role to access all tables
GRANT ALL ON presentations TO service_role;
GRANT ALL ON presentation_versions TO service_role;

-- ============================================
-- Success Verification Query
-- ============================================

-- Verify tables created successfully
SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE tablename IN ('presentations', 'presentation_versions')
ORDER BY tablename;

-- Expected Output:
-- schemaname | tablename              | tableowner
-- -----------|------------------------|------------
-- public     | presentations          | postgres
-- public     | presentation_versions  | postgres
```

### 2.3 Execute SQL

1. Click **"Run"** button (or press Ctrl+Enter / Cmd+Enter)
2. Wait for execution (~2-3 seconds)
3. Verify output shows 2 rows (both tables created)

**Expected Output**:
```
schemaname | tablename              | tableowner
-----------|------------------------|------------
public     | presentations          | postgres
public     | presentation_versions  | postgres

Query executed successfully. 2 rows returned.
```

---

## Step 3: Create Storage Bucket

### 3.1 Navigate to Storage

1. In Supabase dashboard, click **Storage** (left sidebar)
2. Click **"New Bucket"**

### 3.2 Configure Bucket

**Bucket Settings**:

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `presentation-data` | Must match code exactly |
| **Public** | ❌ No (unchecked) | Private bucket for security |
| **Allowed MIME types** | `application/json` | JSON files only |
| **File size limit** | `50 MB` | Default is fine |

3. Click **"Create bucket"**

**Result**: Bucket `presentation-data` created ✅

### 3.3 Configure Bucket Policies (Optional)

**Note**: If using `service_role` key, RLS policies are bypassed. This is optional.

If you want to enable RLS for additional security:

1. Click on `presentation-data` bucket
2. Navigate to **"Policies"** tab
3. Click **"New Policy"**

**Policy 1: Allow Service Role Full Access**

```sql
CREATE POLICY "Service role has full access"
ON storage.objects
FOR ALL
TO service_role
USING (bucket_id = 'presentation-data')
WITH CHECK (bucket_id = 'presentation-data');
```

---

## Step 4: Get API Credentials

### 4.1 Navigate to API Settings

1. Click **Project Settings** (gear icon, bottom left)
2. Click **API** (left sidebar)

### 4.2 Copy Credentials

**Copy the following values** (you'll need these for Railway):

| Credential | Field Name | Example | Usage |
|------------|-----------|---------|-------|
| **URL** | `URL` | `https://eshvntffcestlfuofwhv.supabase.co` | SUPABASE_URL |
| **anon (public)** | `anon public` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | SUPABASE_ANON_KEY |
| **service_role (secret)** | `service_role secret` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | SUPABASE_SERVICE_KEY |

⚠️ **IMPORTANT**: The `service_role` key is **secret**. Never commit to git or expose in client-side code.

**Save these credentials securely** (e.g., password manager, env vault)

---

## Step 5: Configure Railway Environment Variables

### 5.1 Navigate to Railway Dashboard

```
URL: https://railway.app/dashboard
```

### 5.2 Select v7.5-main Service

1. Find your project (e.g., `deck-builder-7.5`)
2. Click on `v7.5-main` service

### 5.3 Add Environment Variables

1. Click **"Variables"** tab
2. Click **"Add Variable"** for each:

**Required Variables**:

```bash
SUPABASE_URL=https://eshvntffcestlfuofwhv.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Your anon key
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...  # Your service_role key
SUPABASE_BUCKET=presentation-data
ENABLE_SUPABASE=true
```

**Optional Variables** (with defaults):

```bash
ENABLE_LOCAL_CACHE=true
CACHE_TTL_SECONDS=3600
```

### 5.4 Save and Redeploy

1. Click **"Save"** (Railway may auto-redeploy)
2. If not, click **"Restart"** to apply new variables

---

## Step 6: Verify Setup

### 6.1 Check Railway Logs

```bash
# View deployment logs
railway logs -f

# Or via Railway Dashboard → Deployments → View Logs
```

**Look for success messages**:
```
✅ Supabase client initialized successfully
✅ Connected to project: eshvntffcestlfuofwhv
✅ Storage bucket 'presentation-data' ready
✅ PostgreSQL tables verified: presentations, presentation_versions
✅ Server started on port 8504
```

**If you see errors**:
```
❌ SUPABASE_URL not set → Check Railway variables
❌ Invalid API key → Verify SUPABASE_SERVICE_KEY is correct
❌ Bucket not found → Ensure bucket named 'presentation-data'
```

---

### 6.2 Test API Connection

**Create a test presentation**:

```bash
curl -X POST https://web-production-f0d13.up.railway.app/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Supabase Setup Test",
    "slides": [{
      "layout": "L25",
      "content": {
        "slide_title": "Setup Verification",
        "subtitle": "Testing Supabase Integration",
        "rich_content": "<div style=\"padding: 20px; font-size: 18px;\">If you can see this, Supabase is configured correctly! ✅</div>"
      }
    }]
  }'
```

**Expected Response**:
```json
{
  "id": "9d54c1e8-f939-436a-aae7-73e11275ec63",
  "url": "/p/9d54c1e8-f939-436a-aae7-73e11275ec63",
  "message": "Presentation 'Supabase Setup Test' created successfully"
}
```

**Verify in Supabase**:
1. Go to Supabase Dashboard → **Table Editor**
2. Select `presentations` table
3. You should see 1 row with your test presentation ✅

**Verify in Storage**:
1. Go to Supabase Dashboard → **Storage**
2. Click `presentation-data` bucket
3. Navigate to `presentations/` folder
4. You should see `{uuid}.json` file ✅

---

### 6.3 Test Persistence (Critical!)

**Restart Railway service**:
```bash
# Railway Dashboard → v7.5-main → Restart
```

**After restart (~30 seconds), load the presentation**:
```bash
curl https://web-production-f0d13.up.railway.app/api/presentations/9d54c1e8-f939-436a-aae7-73e11275ec63
```

**Expected**: Full presentation JSON returned ✅

**If this fails** → Supabase not configured correctly, presentations are still ephemeral ❌

---

## Step 7: Enable Monitoring (Optional but Recommended)

### 7.1 Supabase Dashboard Metrics

1. Navigate to **Project Settings** → **Usage**
2. Monitor:
   - Database size (should grow as presentations added)
   - API requests (should show activity)
   - Bandwidth (Storage uploads/downloads)

### 7.2 Set Up Alerts

1. **Supabase Alerts**:
   - Project Settings → Alerts
   - Enable:
     - Database size > 7GB (80% of Pro limit)
     - API requests approaching limit

2. **Railway Alerts**:
   - Service Settings → Alerts
   - Enable:
     - Error rate > 5%
     - Memory usage > 80%

---

## Troubleshooting

### Issue 1: "Supabase client initialization failed"

**Possible Causes**:
- ❌ `SUPABASE_URL` not set
- ❌ `SUPABASE_SERVICE_KEY` not set
- ❌ Invalid API key

**Solution**:
```bash
# Verify variables in Railway
railway variables

# Should show:
# SUPABASE_URL=https://...
# SUPABASE_SERVICE_KEY=eyJ...
```

---

### Issue 2: "Bucket 'presentation-data' not found"

**Possible Causes**:
- ❌ Bucket not created
- ❌ Bucket named incorrectly (typo)

**Solution**:
1. Go to Supabase Dashboard → Storage
2. Verify bucket exists: `presentation-data` (exact match)
3. If not, create it (Step 3)

---

### Issue 3: "Table 'presentations' does not exist"

**Possible Causes**:
- ❌ SQL script not executed
- ❌ SQL error during execution

**Solution**:
1. Go to Supabase Dashboard → SQL Editor
2. Run verification query:
```sql
SELECT tablename FROM pg_tables
WHERE tablename IN ('presentations', 'presentation_versions');
```
3. If no results, re-run schema creation SQL (Step 2.2)

---

### Issue 4: "Permission denied for table presentations"

**Possible Causes**:
- ❌ Using `anon` key instead of `service_role` key
- ❌ RLS policies blocking access

**Solution**:
```bash
# Ensure using service_role key in Railway
railway variables set SUPABASE_SERVICE_KEY=eyJ...  # service_role key, not anon key

# Or disable RLS temporarily for debugging
```

```sql
-- In Supabase SQL Editor
ALTER TABLE presentations DISABLE ROW LEVEL SECURITY;
ALTER TABLE presentation_versions DISABLE ROW LEVEL SECURITY;
```

---

### Issue 5: Presentations not persisting after Railway restart

**Possible Causes**:
- ❌ `ENABLE_SUPABASE=false` (still using filesystem)
- ❌ Supabase write failing silently

**Diagnosis**:
```bash
# Check Railway logs during presentation creation
railway logs | grep -i "supabase\|storage"

# Look for:
# ✅ "Saved presentation to Supabase: {uuid}"
# ❌ "Falling back to filesystem storage"
```

**Solution**:
```bash
# Ensure Supabase enabled
railway variables set ENABLE_SUPABASE=true

# Restart service
railway restart
```

---

## Quick Reference

### Environment Variables Checklist

```bash
# Required
✅ SUPABASE_URL
✅ SUPABASE_SERVICE_KEY
✅ SUPABASE_BUCKET
✅ ENABLE_SUPABASE

# Optional (with defaults)
⚪ ENABLE_LOCAL_CACHE (default: true)
⚪ CACHE_TTL_SECONDS (default: 3600)
```

### Supabase Configuration Checklist

```bash
✅ Project created (Pro plan)
✅ PostgreSQL tables created:
   - presentations
   - presentation_versions
✅ Storage bucket created:
   - presentation-data (private)
✅ API credentials copied:
   - URL
   - anon key
   - service_role key
✅ Railway variables configured
✅ Test presentation created
✅ Persistence verified (restart test)
```

---

## Next Steps

After completing this setup:

1. ✅ [Deploy code changes](./DEPLOYMENT_GUIDE.md)
2. ✅ [Run tests](../tests/README.md)
3. ✅ [Monitor Supabase usage](https://supabase.com/dashboard/project/eshvntffcestlfuofwhv/usage)
4. ✅ [Review migration guide](./SUPABASE_MIGRATION_GUIDE.md)

---

## Support

**Supabase Issues**:
- Supabase Documentation: https://supabase.com/docs
- Support: https://supabase.com/support

**Railway Issues**:
- Railway Documentation: https://docs.railway.app
- Support: https://railway.app/support

**Layout Builder Issues**:
- See: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- GitHub Issues: (your repo)

---

**Setup Complete!** 🎉

Your Supabase integration is now configured and ready for production use. Presentations will persist across all Railway restarts and deployments.

**End of Setup Guide**
