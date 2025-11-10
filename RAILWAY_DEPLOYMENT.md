# Railway Deployment Guide - v7.5-main

## Overview

This guide covers deploying v7.5-main (with download endpoints) to Railway.

---

## ✅ Deployment Compatibility

### Feature Branch → Railway

**YES, the `feature/download-endpoints` branch is 100% compatible with Railway deployment!**

- ✅ **Backward Compatible**: All existing endpoints work exactly the same
- ✅ **Additive Changes Only**: Only adds new `/download/pdf` and `/download/pptx` endpoints
- ✅ **Director Compatible**: Director will continue to work without any changes
- ✅ **No Breaking Changes**: Zero modifications to existing CRUD operations

---

## 🚀 Deployment Steps

### Option 1: Switch Branch in Railway Dashboard (Recommended)

1. **Go to Railway Dashboard**
   - Navigate to your v7.5-main service
   - Click on "Settings" tab

2. **Change Branch**
   - Find "Source" section
   - Change branch from `main` to `feature/download-endpoints`
   - Click "Update"

3. **Trigger Deployment**
   - Railway will automatically detect the change
   - New deployment will start
   - Wait for build to complete (~5-10 minutes)

4. **Verify Deployment**
   ```bash
   # Test existing endpoints (should work as before)
   curl https://your-railway-url.up.railway.app/

   # Test new download endpoints
   curl "https://your-railway-url.up.railway.app/api/presentations/{id}/download/pdf"
   ```

### Option 2: Deploy via Railway CLI

```bash
# Install Railway CLI if not installed
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Switch to feature branch locally
git checkout feature/download-endpoints

# Deploy
railway up
```

---

## 📦 What Gets Deployed

### New Files in Feature Branch:
```
converters/                    # PDF/PPTX conversion modules
├── __init__.py
├── base.py                   # Screenshot capture
├── pdf_converter.py          # PDF generation
└── pptx_converter.py         # PPTX generation

tests/                        # Test infrastructure
docs/API_REFERENCE.md         # API documentation
test_downloads_manual.py      # Testing script
nixpacks.toml                 # Railway build config
Procfile                      # Railway start command
```

### Updated Files:
```
requirements.txt              # Added playwright, python-pptx, Pillow
server.py                     # Added 2 new endpoints
models.py                     # Added download models
README.md                     # Updated documentation
```

---

## 🔧 Railway Configuration

### Environment Variables

**Required**:
- `PORT` - Automatically set by Railway (usually 8080 or 8000)

**Optional** (already configured in code):
- `ALLOWED_ORIGINS` - CORS origins (default: "*")

**No changes needed** - The feature branch uses the same environment variables as main.

### Build Configuration

Railway will automatically:
1. Detect Python project
2. Install dependencies from `requirements.txt`
3. Install Playwright browsers (via `nixpacks.toml`)
4. Start server with `uvicorn`

### Build Process

The `nixpacks.toml` file ensures:
```toml
[phases.install]
cmds = [
  "pip install -r requirements.txt",
  "playwright install chromium",      # Install browser
  "playwright install-deps chromium"  # Install system dependencies
]
```

---

## ⚙️ Director Integration

### Zero Configuration Needed

Your director is configured to connect to:
```python
DECK_BUILDER_API_URL = "http://localhost:8504"  # Local
# OR
DECK_BUILDER_API_URL = "https://your-railway-url.up.railway.app"  # Production
```

**After deploying feature branch**:
- ✅ Director continues working exactly the same
- ✅ All existing endpoints respond identically
- ✅ New download endpoints available (director can optionally use them)
- ✅ No director code changes required

---

## 📊 API Compatibility Matrix

| Endpoint | Main Branch | Feature Branch | Breaking? |
|----------|-------------|----------------|-----------|
| `POST /api/presentations` | ✅ | ✅ | No |
| `GET /api/presentations/{id}` | ✅ | ✅ | No |
| `GET /api/presentations` | ✅ | ✅ | No |
| `DELETE /api/presentations/{id}` | ✅ | ✅ | No |
| `GET /p/{id}` | ✅ | ✅ | No |
| `GET /api/presentations/{id}/download/pdf` | ❌ | ✅ | **NEW** |
| `GET /api/presentations/{id}/download/pptx` | ❌ | ✅ | **NEW** |

**Verdict**: ✅ 100% Backward Compatible

---

## 🧪 Testing After Deployment

### 1. Health Check
```bash
curl https://your-railway-url.up.railway.app/
```

Expected:
```json
{
  "message": "v7.5-main: Simplified Layout Builder API",
  "version": "7.5.0",
  "layouts": ["L25", "L29"],
  "endpoints": {
    "create_presentation": "POST /api/presentations",
    "download_pdf": "GET /api/presentations/{id}/download/pdf",
    "download_pptx": "GET /api/presentations/{id}/download/pptx",
    ...
  }
}
```

### 2. Test Existing Functionality
```bash
# Create a presentation (existing endpoint)
curl -X POST https://your-railway-url.up.railway.app/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "slides": [{"layout": "L29", "content": {"hero_content": "<div>Test</div>"}}]
  }'
```

### 3. Test New Download Endpoints
```bash
# Get presentation ID from step 2
PRES_ID="<id-from-response>"

# Download PDF
curl "https://your-railway-url.up.railway.app/api/presentations/$PRES_ID/download/pdf" \
  -o test.pdf

# Download PPTX
curl "https://your-railway-url.up.railway.app/api/presentations/$PRES_ID/download/pptx" \
  -o test.pptx
```

### 4. Test with Director
```bash
# Your director should continue working without any changes
cd director_agent/v3.4
python main.py
```

---

## 🐛 Troubleshooting

### Issue: Playwright Installation Fails

**Symptom**: Build fails with Playwright-related errors

**Solution**: Railway might need additional system dependencies

Add to `nixpacks.toml`:
```toml
[phases.setup]
aptPkgs = ["chromium", "chromium-driver", "fonts-liberation"]
```

### Issue: Download Endpoints Return 500

**Symptom**: `/download/pdf` or `/download/pptx` returns internal server error

**Check**:
1. Railway logs: `railway logs`
2. Verify Playwright installed: Check build logs for "playwright install chromium"
3. Verify memory limits: Downloads need ~512MB RAM minimum

**Solution**: Increase Railway service memory if needed

### Issue: Port Configuration

**Symptom**: Service doesn't start or is unreachable

**Check**: Railway automatically sets `PORT` environment variable
- The app uses: `port = int(os.getenv("PORT", "8009"))`
- Railway will override with its own PORT value

**Solution**: No action needed - port is auto-configured

---

## 📈 Performance Considerations

### Resource Usage

**Main Branch**:
- Memory: ~200-300MB
- CPU: Low
- Build time: ~2-3 minutes

**Feature Branch**:
- Memory: ~400-600MB (Playwright + browsers)
- CPU: Moderate (PDF/PPTX generation)
- Build time: ~5-7 minutes (includes browser installation)

### Recommendations

For Railway deployment:
- **Minimum**: 512MB RAM, 0.5 vCPU
- **Recommended**: 1GB RAM, 1 vCPU
- **Storage**: ~500MB (for Chromium browser)

---

## 🔄 Rollback Plan

If issues arise, rollback is simple:

### Via Railway Dashboard
1. Go to "Deployments" tab
2. Find previous deployment (main branch)
3. Click "Redeploy"

### Via Branch Switch
1. Change source branch back to `main`
2. Railway will automatically redeploy

**Rollback Time**: ~2-3 minutes

---

## ✅ Pre-Deployment Checklist

Before switching Railway to feature branch:

- [ ] Verify feature branch is up to date
- [ ] Review Railway resource limits (512MB RAM minimum)
- [ ] Backup current Railway URL for rollback
- [ ] Test feature branch locally first
- [ ] Notify team of deployment window
- [ ] Have rollback plan ready

---

## 🎯 Summary

### Will It Work?

**YES! 100%** ✅

The feature branch:
- ✅ Contains all commits from main
- ✅ Adds new functionality without breaking existing features
- ✅ Is fully backward compatible
- ✅ Works with director without any changes
- ✅ Includes Railway deployment configuration

### Deployment Confidence: HIGH

**Risk Level**: ⬜ Low
- Additive changes only
- No breaking changes
- Easy rollback
- Well-tested locally

### Recommendation

**Proceed with deployment!** Switch Railway from `main` to `feature/download-endpoints`.

Your director will continue working exactly as before, with the bonus of having PDF and PPTX download capabilities available.

---

## 📞 Support

If deployment issues occur:
1. Check Railway logs: `railway logs`
2. Review build logs in Railway dashboard
3. Test endpoints with curl commands above
4. Rollback to main if needed

---

**Ready to deploy!** 🚀

Last updated: 2025-11-09
