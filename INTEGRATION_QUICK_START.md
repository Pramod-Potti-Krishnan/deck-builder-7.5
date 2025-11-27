# Layout Service Integration Quick Start

**Railway Deployment**: https://web-production-f0d13.up.railway.app
**Version**: 7.5.0 (6-Layout System + AI Section Regeneration)
**Last Updated**: 2025-01-24

---

## 🚀 Complete Documentation Paths

### **Primary Integration Documents**

#### 1. Complete Features Reference
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/FEATURES.md`

**What's Inside**:
- All 6 layouts (L01, L02, L03, L25, L27, L29) with specifications
- Content editing features (version history, restore)
- AI-powered section regeneration (Phase 2)
- Chart & visualization support
- Complete API reference
- Integration patterns
- Developer features

**Use For**: Complete feature overview and API reference

---

#### 2. Director Service Integration Spec (Section Regeneration)
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/DIRECTOR_SECTION_REGENERATION_SPEC.md`

**What's Inside**:
- API endpoint specification for section regeneration
- Complete request/response schemas
- Section types by layout
- Real-world regeneration scenarios
- Chart regeneration patterns
- Content constraints and guidelines
- Error handling
- Performance requirements
- Complete integration examples

**Use For**: Implementing AI section regeneration in Director Service

---

#### 3. Phase 2 Implementation Plan
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/PHASE2_PLAN.md`

**What's Inside**:
- Section regeneration architecture
- Implementation roadmap
- Frontend and backend integration
- Testing checklist
- Step-by-step implementation guide

**Use For**: Understanding section regeneration implementation

---

### **Core Documentation (docs/ directory)**

#### 4. System Architecture
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/ARCHITECTURE.md`

**Use For**: Understanding system design, format ownership model

---

#### 5. Layout Specifications
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/LAYOUT_SPECIFICATIONS.md`

**Use For**: Detailed layout grid specs, content field definitions

---

#### 6. Content Generation Guide
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/CONTENT_GENERATION_GUIDE.md`

**Use For**: Text Service HTML content generation guidelines

---

#### 7. Frontend Integration Guide
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/FRONTEND_INTEGRATION_GUIDE.md`

**Use For**: Iframe embedding, postMessage bridge, frontend integration

---

#### 8. L02 Director Integration
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/L02_DIRECTOR_INTEGRATION_GUIDE.md`

**Use For**: L02 layout integration with Director Agent

---

#### 9. Content Editing User Guide
**Path**: `/Users/pk1980/Documents/Software/deckster-backend/deckster-w-content-strategist/agents/layout_builder_main/v7.5-main/docs/CONTENT_EDITING_USER_GUIDE.md`

**Use For**: Version history, restore functionality, editing features

---

## 🌐 Railway Deployment Information

### **Base URL**
```
https://web-production-f0d13.up.railway.app
```

### **API Endpoints**

#### Core Endpoints:
- **API Root**: `GET https://web-production-f0d13.up.railway.app/`
- **Interactive Docs**: `GET https://web-production-f0d13.up.railway.app/docs`
- **Create Presentation**: `POST https://web-production-f0d13.up.railway.app/api/presentations`
- **View Presentation**: `GET https://web-production-f0d13.up.railway.app/p/{id}`
- **List Presentations**: `GET https://web-production-f0d13.up.railway.app/api/presentations`

#### Edit Endpoints:
- **Update Slide**: `PUT https://web-production-f0d13.up.railway.app/api/presentations/{id}/slides/{index}`
- **Version History**: `GET https://web-production-f0d13.up.railway.app/api/presentations/{id}/versions`
- **Restore Version**: `POST https://web-production-f0d13.up.railway.app/api/presentations/{id}/restore/{version_id}`

#### AI Endpoints (Phase 2):
- **Regenerate Section**: `POST https://web-production-f0d13.up.railway.app/api/presentations/{id}/regenerate-section`

---

## 🔧 CORS Configuration

### **Allowed Origins** (Already Configured)

The service accepts requests from:
- ✅ `localhost:*` (development)
- ✅ `127.0.0.1:*` (local)
- ✅ `*.up.railway.app` (Railway deployments) **← Your deployment**
- ✅ `*.vercel.app` (Vercel deployments)
- ✅ `*.netlify.app` (Netlify deployments)
- ✅ `deckster.xyz` (production)
- ✅ `www.deckster.xyz` (production)

**Configuration Location**:
- Backend CORS: `server.py` (uses `ALLOWED_ORIGINS` env variable)
- PostMessage Security: `viewer/presentation-viewer.html` (line 313)

**Your Railway URL is already whitelisted** ✅

---

## 📝 Quick Integration Examples

### **1. Create Presentation**

```bash
curl -X POST https://web-production-f0d13.up.railway.app/api/presentations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Presentation",
    "slides": [
      {
        "layout": "L25",
        "content": {
          "slide_title": "Welcome",
          "subtitle": "Integration Test",
          "rich_content": "<div style=\"padding: 40px;\"><h2>Hello from Railway!</h2></div>"
        }
      }
    ]
  }'
```

**Response**:
```json
{
  "id": "abc123...",
  "url": "/p/abc123...",
  "message": "Presentation created successfully"
}
```

**View**: `https://web-production-f0d13.up.railway.app/p/abc123...`

---

### **2. Regenerate Section with AI**

```bash
curl -X POST https://web-production-f0d13.up.railway.app/api/presentations/{id}/regenerate-section \
  -H "Content-Type: application/json" \
  -d '{
    "slide_index": 0,
    "section_id": "slide-0-section-title",
    "section_type": "title",
    "user_instruction": "Make this more engaging",
    "current_content": "Welcome",
    "layout": "L25"
  }'
```

**Response**:
```json
{
  "success": true,
  "updated_content": "<enhanced content>",
  "section_id": "slide-0-section-title",
  "message": "Section regenerated successfully"
}
```

---

### **3. Iframe Embedding**

```html
<!-- Frontend application -->
<iframe
  id="presentation-iframe"
  src="https://web-production-f0d13.up.railway.app/p/{presentation_id}"
  width="100%"
  height="600px"
  frameborder="0"
></iframe>

<script>
  const iframe = document.getElementById('presentation-iframe');

  // Send command to presentation
  iframe.contentWindow.postMessage({
    action: 'nextSlide'
  }, 'https://web-production-f0d13.up.railway.app');

  // Listen for response
  window.addEventListener('message', (event) => {
    if (event.origin === 'https://web-production-f0d13.up.railway.app') {
      console.log('Response:', event.data);
    }
  });
</script>
```

**Available Commands**:
- `nextSlide`, `prevSlide`, `goToSlide`
- `toggleEditMode`, `saveAllChanges`, `cancelEdits`
- `toggleOverview`, `getCurrentSlideInfo`

---

## 🎯 Integration Checklist

### **For Director Service Integration**:
- [ ] Read: `DIRECTOR_SECTION_REGENERATION_SPEC.md`
- [ ] Implement: `POST /api/regenerate-section` endpoint
- [ ] Test: Section regeneration with mock data
- [ ] Verify: Response format matches specification

### **For Frontend Integration**:
- [ ] Read: `docs/FRONTEND_INTEGRATION_GUIDE.md`
- [ ] Implement: Iframe embedding with postMessage
- [ ] Test: Cross-origin communication
- [ ] Verify: All commands working

### **For Text Service Integration**:
- [ ] Read: `docs/CONTENT_GENERATION_GUIDE.md`
- [ ] Implement: HTML content generation
- [ ] Test: All 6 layouts
- [ ] Verify: Content area dimensions

---

## 🔍 Testing the Deployment

### **1. Verify API is Running**
```bash
curl https://web-production-f0d13.up.railway.app/
```

**Expected**: JSON response with API info

### **2. Access Interactive Docs**
Visit: https://web-production-f0d13.up.railway.app/docs

**Expected**: FastAPI Swagger UI

### **3. Test Presentation Creation**
Use the curl example above or the Swagger UI

---

## 📚 Documentation Priority Order

**For Quick Integration** (read in this order):
1. **FEATURES.md** - Overview of all capabilities
2. **DIRECTOR_SECTION_REGENERATION_SPEC.md** - If integrating with Director
3. **docs/FRONTEND_INTEGRATION_GUIDE.md** - If embedding in frontend
4. **docs/CONTENT_GENERATION_GUIDE.md** - If generating content

**For Deep Understanding**:
5. **docs/ARCHITECTURE.md** - System design
6. **docs/LAYOUT_SPECIFICATIONS.md** - Layout details
7. **PHASE2_PLAN.md** - Implementation details

---

## 🆘 Common Integration Issues

### **Issue 1: CORS Errors**
**Solution**: Railway domain (`*.up.railway.app`) is already whitelisted

### **Issue 2: Section Regeneration Returns Mock Data**
**Reason**: Phase 2 uses mock AI (for testing)
**Solution**: Integrate real Director Service API (see DIRECTOR_SECTION_REGENERATION_SPEC.md)

### **Issue 3: Charts Not Rendering**
**Solution**: Ensure chart HTML includes complete `<script>` tags
**Reference**: `docs/CONTENT_GENERATION_GUIDE.md`

### **Issue 4: PostMessage Not Working**
**Solution**: Verify origin matches exactly: `https://web-production-f0d13.up.railway.app`
**Reference**: `docs/FRONTEND_INTEGRATION_GUIDE.md`

---

## 📞 Support

### **API Documentation**:
- Live Docs: https://web-production-f0d13.up.railway.app/docs
- Root Endpoint: https://web-production-f0d13.up.railway.app/

### **Code Repository**:
- GitHub: https://github.com/Pramod-Potti-Krishnan/deck-builder-7.5
- Branch: `feature/world-class-editor-phase2`

---

## ✅ Summary

**Railway Deployment**: ✅ Live and ready
**CORS Configuration**: ✅ Already includes Railway domain
**Documentation**: ✅ Complete and up-to-date
**API Endpoints**: ✅ All functional
**AI Features**: ✅ Phase 2 implemented (mock AI)

**Next Step**: Choose your integration path and read the corresponding documentation!

---

**Last Updated**: 2025-01-24
**Deployment**: https://web-production-f0d13.up.railway.app
