# Supabase Storage Migration Guide

**Version**: v7.5.2
**Date**: November 16, 2025
**Status**: Production-Ready
**Author**: Layout Builder Team

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Why Supabase?](#why-supabase)
4. [Migration Strategy](#migration-strategy)
5. [Data Flow](#data-flow)
6. [Schema Design](#schema-design)
7. [Caching Strategy](#caching-strategy)
8. [Rollback Plan](#rollback-plan)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Guide](#deployment-guide)

---

## Overview

### The Problem

**Before Migration**:
- Layout Builder stored presentations in local filesystem (`storage/presentations/`)
- Railway containers are ephemeral (stateless)
- Every restart/deployment wiped all presentations
- **Result**: All presentation links became invalid ❌

**After Migration**:
- Presentations stored in Supabase PostgreSQL + Storage
- Railway restarts have zero impact on data
- Presentation links persist indefinitely
- **Result**: Production-grade reliability ✅

---

## Architecture

### 2-Tier Storage Architecture

```
┌─────────────────────────────────────────────────┐
│         Layout Builder Service (Railway)        │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │    Hybrid Storage Manager                 │ │
│  │                                           │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  Tier 1: Supabase (Primary)         │ │ │
│  │  │  ├── PostgreSQL (metadata + JSON)   │ │ │
│  │  │  └── Storage Buckets (backup)       │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  │              ▼          ▲                 │ │
│  │  ┌─────────────────────────────────────┐ │ │
│  │  │  Tier 2: Local Cache (Speed)        │ │ │
│  │  │  ├── Memory Cache (hot data)        │ │ │
│  │  │  └── Filesystem Cache (cold data)   │ │ │
│  │  └─────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │      Supabase Cloud        │
        │                            │
        │  ┌──────────────────────┐  │
        │  │  PostgreSQL Database │  │
        │  │  • presentations     │  │
        │  │  • versions          │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │  Storage Buckets     │  │
        │  │  • presentation-data │  │
        │  └──────────────────────┘  │
        └────────────────────────────┘
             PERSISTENT STORAGE
```

---

## Why Supabase?

### Comparison of Storage Options

| Feature | Filesystem | Railway Volume | Supabase Pro |
|---------|-----------|----------------|--------------|
| **Survives Restarts** | ❌ No | ✅ Yes | ✅ Yes |
| **Multi-Region** | ❌ No | ❌ No | ✅ Yes |
| **Automatic Backups** | ❌ No | ⚠️ Manual | ✅ Daily |
| **Scalability** | ❌ Limited | ⚠️ Volume size | ✅ Unlimited |
| **Query Performance** | ⚠️ File scan | ⚠️ File scan | ✅ Indexed SQL |
| **Cost (10GB)** | ✅ Free | ~$2.50/mo | ✅ Included ($25/mo) |
| **Portability** | ❌ No | ❌ Railway-locked | ✅ Postgres standard |
| **JSONB Support** | ❌ No | ❌ No | ✅ Native |
| **Version Control** | ⚠️ Manual | ⚠️ Manual | ✅ Built-in |

**Decision**: Supabase Pro provides production-grade features already included in your subscription.

---

## Migration Strategy

### Phase 1: Fresh Start (Current Approach)

**Status**: ✅ **CHOSEN APPROACH**

**Strategy**:
- Accept loss of existing test presentations
- Deploy Supabase integration
- Start fresh with persistent storage
- All future presentations永久 preserved

**Pros**:
- ✅ Clean migration (no data compatibility issues)
- ✅ Faster implementation (no migration script)
- ✅ Zero risk of data corruption

**Cons**:
- ⚠️ Existing presentation links break (test data only)

**Decision Rationale**:
- Current presentations are test/demo data
- Production launch hasn't happened yet
- Clean start ensures data integrity

---

### Phase 2: Gradual Migration (Future Option)

**Status**: 📅 Available if needed

**Strategy**:
```python
# migration_script.py
def migrate_filesystem_to_supabase():
    """Migrate existing filesystem presentations to Supabase"""

    # 1. Load all filesystem presentations
    filesystem = FilesystemPresentationStorage()
    presentation_ids = filesystem.list_all()

    # 2. Initialize Supabase
    supabase = SupabasePresentationStorage()

    # 3. Migrate each presentation (preserving IDs)
    for pres_id in presentation_ids:
        presentation = filesystem.load(pres_id)
        if presentation:
            # Preserve original ID and timestamps
            supabase.save_with_id(pres_id, presentation)
            print(f"✅ Migrated: {pres_id}")

    print(f"✅ Migration complete: {len(presentation_ids)} presentations")
```

**Use Case**: If production presentations exist before migration

---

## Data Flow

### Create Presentation Flow

```
1. API Request: POST /api/presentations
   ↓
2. Validate presentation data (Pydantic)
   ↓
3. Generate UUID
   ↓
4. INSERT INTO presentations (PostgreSQL)
   │  - id, title, slides (JSONB), created_at
   ↓
5. UPLOAD to Storage Bucket (async backup)
   │  - presentations/{uuid}.json
   ↓
6. Cache in memory (optional)
   │  - memory_cache[uuid] = presentation_data
   ↓
7. Return presentation_id to client
```

**Performance**: ~100-200ms (PostgreSQL insert + async upload)

---

### Read Presentation Flow

```
1. API Request: GET /api/presentations/{id}
   ↓
2. Check memory cache → HIT?
   │  YES: Return cached data (5ms)
   │  NO: Continue ↓
   ↓
3. SELECT FROM presentations WHERE id={id}
   │  - PostgreSQL query (10-50ms)
   ↓
4. Found? → Cache + Return
   │  Not Found? → Check Storage Bucket (fallback)
   ↓
5. DOWNLOAD from Storage Bucket
   │  - presentations/{uuid}.json
   ↓
6. Return presentation_data
```

**Performance**:
- Cache HIT: ~5ms ✅
- PostgreSQL: ~10-50ms ✅
- Storage fallback: ~100-200ms ⚠️

---

### Update Presentation Flow

```
1. API Request: PUT /api/presentations/{id}
   ↓
2. Load current presentation (PostgreSQL)
   ↓
3. Create version snapshot
   │  INSERT INTO presentation_versions
   │  - version_id, presentation_id, version_data (JSONB)
   │  - created_by, change_summary
   ↓
4. UPDATE presentations SET ...
   │  - slides, updated_at, updated_by
   ↓
5. UPLOAD to Storage Bucket (async)
   │  - presentations/{uuid}.json
   │  - versions/{uuid}/{version_id}.json
   ↓
6. Invalidate cache
   │  - del memory_cache[uuid]
   ↓
7. Return updated presentation
```

**Performance**: ~150-300ms (version insert + update + async upload)

---

### Version History Flow

```
1. API Request: GET /api/presentations/{id}/versions
   ↓
2. SELECT FROM presentation_versions
   │  WHERE presentation_id={id}
   │  ORDER BY created_at DESC
   ↓
3. Return version metadata list
   │  [{version_id, created_at, created_by, change_summary}, ...]
```

**Performance**: ~20-50ms (indexed query)

---

## Schema Design

### PostgreSQL Tables

#### Table 1: `presentations`

**Purpose**: Store current presentation state

```sql
CREATE TABLE presentations (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Presentation Data
    title VARCHAR(200) NOT NULL,
    slides JSONB NOT NULL,  -- Full slides array with layout + content

    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    updated_by VARCHAR(100),
    restored_from VARCHAR(100),  -- version_id if restored from history
    metadata JSONB,  -- Additional metadata (future use)

    -- Indexes
    INDEX idx_presentations_created_at (created_at DESC),
    INDEX idx_presentations_updated_at (updated_at DESC)
);
```

**Example Row**:
```json
{
  "id": "9d54c1e8-f939-436a-aae7-73e11275ec63",
  "title": "Quarterly Revenue Growth",
  "slides": [
    {
      "layout": "L02",
      "content": {
        "slide_title": "Quarterly Revenue Growth",
        "element_1": "FY 2024 Performance",
        "element_3": "<div>...chart HTML...</div>",
        "element_2": "<div>...insights HTML...</div>"
      }
    }
  ],
  "created_at": "2025-11-16T10:30:00Z",
  "updated_at": "2025-11-16T11:45:00Z",
  "updated_by": "director_agent",
  "restored_from": null,
  "metadata": null
}
```

---

#### Table 2: `presentation_versions`

**Purpose**: Store version history for undo/restore

```sql
CREATE TABLE presentation_versions (
    -- Primary Key
    id SERIAL PRIMARY KEY,

    -- Foreign Key (cascade delete when presentation deleted)
    presentation_id UUID NOT NULL REFERENCES presentations(id) ON DELETE CASCADE,

    -- Version Identity
    version_id VARCHAR(100) NOT NULL,  -- v_20251116_120000_abc123

    -- Version Data
    version_data JSONB NOT NULL,  -- Complete presentation snapshot at this version

    -- Version Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by VARCHAR(100) NOT NULL,
    change_summary TEXT,

    -- Constraints
    UNIQUE(presentation_id, version_id),

    -- Indexes
    INDEX idx_versions_presentation (presentation_id, created_at DESC),
    INDEX idx_versions_version_id (version_id)
);
```

**Example Row**:
```json
{
  "id": 1,
  "presentation_id": "9d54c1e8-f939-436a-aae7-73e11275ec63",
  "version_id": "v_20251116_114500_abc123",
  "version_data": {
    "id": "9d54c1e8-f939-436a-aae7-73e11275ec63",
    "title": "Quarterly Revenue Growth",
    "slides": [...]  // Complete presentation at this point in time
  },
  "created_at": "2025-11-16T11:45:00Z",
  "created_by": "user",
  "change_summary": "Updated slide 1 content"
}
```

---

### Supabase Storage Buckets

#### Bucket: `presentation-data`

**Purpose**: Backup storage + disaster recovery

**Configuration**:
- **Privacy**: Private (requires authentication)
- **Access**: Service key only (server-side access)
- **Max File Size**: 50MB (default)
- **MIME Types**: application/json

**Folder Structure**:
```
presentation-data/
├── presentations/
│   ├── 9d54c1e8-f939-436a-aae7-73e11275ec63.json
│   ├── a1b2c3d4-e5f6-4789-0abc-def012345678.json
│   └── ...
└── versions/
    ├── 9d54c1e8-f939-436a-aae7-73e11275ec63/
    │   ├── v_20251116_114500_abc123.json
    │   ├── v_20251116_120000_def456.json
    │   └── ...
    └── ...
```

**Upload Strategy**:
- **Async**: Upload happens after PostgreSQL insert (non-blocking)
- **Fire-and-forget**: Upload failures don't block API response
- **Redundancy**: PostgreSQL is authoritative, Storage is backup

**Recovery Scenario**:
```python
# If PostgreSQL data corrupted/lost
def recover_from_storage():
    """Restore PostgreSQL from Storage bucket backup"""

    # 1. List all files in bucket
    files = supabase.storage.from_('presentation-data').list('presentations/')

    # 2. Download and restore each presentation
    for file in files:
        json_data = supabase.storage.from_('presentation-data').download(
            f'presentations/{file.name}'
        )
        presentation = json.loads(json_data)

        # 3. Insert into PostgreSQL
        supabase.table('presentations').insert(presentation).execute()
```

---

## Caching Strategy

### Tier 2: Local Cache Architecture

**Purpose**: Reduce Supabase queries, improve read performance

#### Memory Cache (Hot Data)

**Implementation**: Simple Python dictionary

```python
class SupabasePresentationStorage:
    def __init__(self):
        self.memory_cache = {}  # {presentation_id: presentation_data}
        self.cache_ttl = 3600   # 1 hour TTL
        self.cache_timestamps = {}  # {presentation_id: timestamp}
```

**Cache Operations**:

```python
# READ: Cache-first strategy
def load(self, presentation_id):
    # 1. Check memory cache
    if presentation_id in self.memory_cache:
        if not self._is_cache_expired(presentation_id):
            return self.memory_cache[presentation_id]  # FAST: ~1ms

    # 2. Cache MISS: Query PostgreSQL
    presentation = self._query_postgresql(presentation_id)  # ~10-50ms

    # 3. Populate cache
    if presentation:
        self.memory_cache[presentation_id] = presentation
        self.cache_timestamps[presentation_id] = time.time()

    return presentation

# WRITE: Write-through + invalidate
def update(self, presentation_id, updates):
    # 1. Invalidate cache immediately
    if presentation_id in self.memory_cache:
        del self.memory_cache[presentation_id]
        del self.cache_timestamps[presentation_id]

    # 2. Write to PostgreSQL
    updated = self._update_postgresql(presentation_id, updates)

    # 3. Don't cache yet (let next read populate)
    return updated
```

**Cache Metrics**:
- **Hit Rate Target**: >70% for active presentations
- **Memory Usage**: ~1KB per presentation × 1000 = ~1MB
- **TTL**: 1 hour (configurable via `CACHE_TTL_SECONDS`)

---

### Cache Invalidation Rules

**Scenarios**:

1. **Presentation Updated** → Invalidate cache immediately
2. **Presentation Deleted** → Remove from cache
3. **Version Restored** → Invalidate cache (new content)
4. **TTL Expired** → Remove on next access
5. **Memory Pressure** → LRU eviction (future enhancement)

**No Cache Stampede**:
- Single-threaded Python (no concurrent reads)
- If needed: Use locks or async queue for concurrent environments

---

## Rollback Plan

### Immediate Rollback (< 1 minute)

**Scenario**: Supabase integration breaks after deployment

**Action**:
```bash
# Railway Dashboard → Environment Variables
ENABLE_SUPABASE=false

# Service automatically falls back to filesystem
# Next restart uses FilesystemPresentationStorage
```

**Result**:
- Service continues running
- New presentations saved to filesystem (ephemeral)
- Existing Supabase data preserved for recovery

---

### Full Rollback (< 5 minutes)

**Scenario**: Need to revert codebase changes

**Action**:
```bash
# 1. Revert git commits
git checkout feature/content-editing
git log  # Find commit before Supabase migration
git revert <commit-hash>

# 2. Push revert
git push origin feature/content-editing

# 3. Railway redeploys automatically
# Previous filesystem-only code restored
```

**Result**:
- Codebase back to pre-migration state
- Supabase data preserved (can re-migrate later)
- No data loss

---

### Partial Rollback (Hybrid Mode)

**Scenario**: Keep Supabase but disable some features

**Options**:
```bash
# Disable cache only
ENABLE_LOCAL_CACHE=false

# Read from Supabase, fallback to filesystem
SUPABASE_FALLBACK_ENABLED=true

# Use Supabase for reads only (filesystem for writes)
SUPABASE_READ_ONLY=true
```

---

## Testing Strategy

### Unit Tests (`tests/test_supabase_storage.py`)

**Mock Supabase Client**:
```python
import pytest
from unittest.mock import Mock, patch
from storage_supabase import SupabasePresentationStorage

@pytest.fixture
def mock_supabase():
    with patch('storage_supabase.create_client') as mock:
        yield mock

def test_save_presentation(mock_supabase):
    """Test saving presentation to Supabase"""
    storage = SupabasePresentationStorage()

    presentation_data = {
        "title": "Test Presentation",
        "slides": [{"layout": "L25", "content": {...}}]
    }

    # Mock PostgreSQL insert
    mock_supabase.table().insert().execute.return_value = {
        "data": [{"id": "test-uuid"}]
    }

    presentation_id = storage.save(presentation_data)

    assert presentation_id == "test-uuid"
    mock_supabase.table().insert.assert_called_once()
```

**Coverage Target**: >90% for all storage methods

---

### Integration Tests (`tests/test_supabase_integration.py`)

**Real Supabase Connection** (test project):

```python
import pytest
from storage_supabase import SupabasePresentationStorage
import os

@pytest.fixture
def supabase_storage():
    # Use test Supabase project
    os.environ['SUPABASE_URL'] = 'https://test-project.supabase.co'
    os.environ['SUPABASE_KEY'] = 'test-key'
    return SupabasePresentationStorage()

def test_full_crud_workflow(supabase_storage):
    """Test create → read → update → delete flow"""

    # 1. Create
    presentation_data = {...}
    pres_id = supabase_storage.save(presentation_data)
    assert pres_id is not None

    # 2. Read
    loaded = supabase_storage.load(pres_id)
    assert loaded["title"] == presentation_data["title"]

    # 3. Update
    updates = {"title": "Updated Title"}
    updated = supabase_storage.update(pres_id, updates, create_version=True)
    assert updated["title"] == "Updated Title"

    # 4. Version History
    history = supabase_storage.get_version_history(pres_id)
    assert len(history["versions"]) == 1

    # 5. Delete
    success = supabase_storage.delete(pres_id)
    assert success == True

    # 6. Verify deleted
    deleted = supabase_storage.load(pres_id)
    assert deleted is None
```

---

### Manual Testing Checklist

**Pre-deployment**:
- [ ] Create presentation locally → verify in Supabase dashboard
- [ ] Update presentation → verify version created
- [ ] Restore version → verify content reverted
- [ ] Delete presentation → verify cascade delete
- [ ] Restart local server → verify presentations persist
- [ ] Disable Supabase → verify fallback to filesystem
- [ ] Load test: Create 100 presentations → verify performance

**Post-deployment (Railway)**:
- [ ] Create presentation via Railway API → verify in Supabase
- [ ] Restart Railway service → verify presentation still accessible
- [ ] Test version history endpoints
- [ ] Monitor error logs for 1 hour
- [ ] Verify cache hit rates in logs

---

## Deployment Guide

### Pre-Deployment Checklist

- [ ] Supabase project created
- [ ] PostgreSQL schema created (presentations + presentation_versions tables)
- [ ] Storage bucket created (presentation-data)
- [ ] API credentials obtained (URL, anon key, service key)
- [ ] Railway environment variables configured
- [ ] All tests passing locally
- [ ] Documentation reviewed and accurate

---

### Deployment Steps

**Step 1: Configure Railway Environment Variables**

```bash
# Railway Dashboard → v7.5-main service → Variables
SUPABASE_URL=https://eshvntffcestlfuofwhv.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_BUCKET=presentation-data
ENABLE_SUPABASE=true
ENABLE_LOCAL_CACHE=true
CACHE_TTL_SECONDS=3600
```

**Step 2: Deploy Code**

```bash
# Commit all changes
git add -A
git commit -m "feat: Add Supabase persistent storage with 2-tier cache"

# Push to deployment branch
git push origin feature/supabase-persistent-storage

# Merge to feature/content-editing (deployment branch)
git checkout feature/content-editing
git merge feature/supabase-persistent-storage
git push origin feature/content-editing
```

**Step 3: Monitor Deployment**

```bash
# Railway auto-deploys on push

# Watch logs
railway logs -f

# Look for:
# ✅ "Supabase client initialized successfully"
# ✅ "Storage bucket 'presentation-data' ready"
# ✅ "Server started on port 8504"
```

**Step 4: Verify Health**

```bash
# Test API health
curl https://web-production-f0d13.up.railway.app/

# Expected response:
{
  "message": "v7.5-main: Simplified Layout Builder API with Content Editing",
  "version": "7.5.2",
  "storage": "supabase",
  "cache_enabled": true
}
```

**Step 5: Create Test Presentation**

```bash
curl -X POST https://web-production-f0d13.up.railway.app/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Supabase Migration Test",
    "slides": [{
      "layout": "L25",
      "content": {
        "slide_title": "Test Slide",
        "subtitle": "Verifying Supabase Storage",
        "rich_content": "<div>If you can see this after a Railway restart, Supabase is working!</div>"
      }
    }]
  }'

# Save the returned presentation_id
# Example: 9d54c1e8-f939-436a-aae7-73e11275ec63
```

**Step 6: Restart Railway & Verify Persistence**

```bash
# Railway Dashboard → v7.5-main → Restart

# After restart (30s), test if presentation still exists:
curl https://web-production-f0d13.up.railway.app/api/presentations/{id}

# Should return full presentation JSON ✅
```

---

### Post-Deployment Monitoring

**Metrics to Watch** (first 24 hours):

1. **Error Rate**: Should be <1% (check Railway logs)
2. **Response Times**:
   - Create: <300ms
   - Read (cache hit): <50ms
   - Read (cache miss): <200ms
3. **Cache Hit Rate**: Target >60% (log metrics)
4. **Supabase Usage**: Monitor Supabase dashboard
   - Database size
   - API requests
   - Storage bandwidth

**Alerts**:
- Set up Railway alerts for:
  - Error rate >5%
  - Response time >1s
  - Memory usage >80%

---

## Troubleshooting

### Issue: Presentations not persisting

**Symptoms**: Presentation lost after Railway restart

**Diagnosis**:
```bash
# Check Railway logs
railway logs | grep "SUPABASE"

# Look for:
# ❌ "Supabase client initialization failed"
# ❌ "SUPABASE_URL not set"
```

**Solution**:
```bash
# Verify environment variables
railway variables

# Ensure all Supabase variables are set:
# - SUPABASE_URL
# - SUPABASE_SERVICE_KEY
# - ENABLE_SUPABASE=true
```

---

### Issue: Slow response times

**Symptoms**: API responses taking >1s

**Diagnosis**:
```bash
# Check cache hit rate in logs
railway logs | grep "cache"

# Look for:
# ❌ "Cache MISS rate: 95%"  (bad)
# ✅ "Cache HIT rate: 75%"   (good)
```

**Solution**:
```bash
# Increase cache TTL
railway variables set CACHE_TTL_SECONDS=7200  # 2 hours

# Or disable cache temporarily to isolate issue
railway variables set ENABLE_LOCAL_CACHE=false
```

---

### Issue: Supabase quota exceeded

**Symptoms**: "Rate limit exceeded" errors

**Diagnosis**:
```bash
# Check Supabase dashboard
# Project Settings → Usage

# Look for:
# - Database size > 8GB
# - API requests > daily limit
# - Bandwidth > 250GB/month
```

**Solution**:
```bash
# Short-term: Increase Supabase plan
# Long-term: Optimize queries, add caching, archive old data
```

---

## Summary

### Key Benefits

✅ **Data Persistence**: Presentations survive all Railway restarts
✅ **Production-Ready**: Built on Supabase Pro (enterprise-grade)
✅ **Fast Performance**: 2-tier cache reduces latency
✅ **Version Control**: Full history with restore capabilities
✅ **Scalable**: Handles 100K+ presentations
✅ **Rollback Ready**: Multiple fallback options

### Migration Checklist

- [ ] Documentation reviewed
- [ ] Supabase project configured
- [ ] PostgreSQL schema created
- [ ] Storage bucket created
- [ ] Railway variables set
- [ ] Code deployed
- [ ] Tests passing
- [ ] Presentations persisting
- [ ] Monitoring active
- [ ] Team notified

---

**For questions or issues, refer to**:
- [SUPABASE_SETUP.md](./SUPABASE_SETUP.md) - Setup instructions
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Deployment procedures

**End of Migration Guide**
