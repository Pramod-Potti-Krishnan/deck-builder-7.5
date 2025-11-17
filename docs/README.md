# Documentation Organization

**Last Updated**: November 16, 2025

This directory contains all documentation for v7.5-main Layout Builder, organized by importance and recency.

---

## 📁 Directory Structure

```
docs/
├── README.md                           # This file (documentation index)
├── ARCHITECTURE.md                     # System architecture (CRITICAL)
├── CONTENT_GENERATION_GUIDE.md         # Text Service integration guide (CRITICAL)
├── CONTENT_EDITING_USER_GUIDE.md       # Content editing features guide (CRITICAL)
├── L02_DIRECTOR_INTEGRATION_GUIDE.md   # Director Agent integration (CRITICAL)
├── LAYOUT_SPECIFICATIONS.md            # Layout specifications reference (CRITICAL)
├── recent/                             # Recent fixes and updates
│   ├── ANALYTICS_CHARTJS_ERROR.md
│   ├── APEXCHARTS_FIX_SUMMARY.md
│   └── CHART_RENDERING_FIX_COMPLETE.md
└── archive/                            # Archived/reference documentation
    └── REVEALJS_CAPABILITIES.md
```

---

## 📖 Critical Documentation (docs/)

These documents are essential for understanding and working with v7.5-main:

### **ARCHITECTURE.md**
- Complete system architecture documentation
- Component diagrams and data flow
- Format ownership model
- Grid system specifications
- Technology stack details

**Audience**: Developers, architects, integrators

---

### **LAYOUT_SPECIFICATIONS.md**
- Comprehensive specifications for all 6 layouts (L01, L02, L03, L25, L27, L29)
- Grid positioning and dimensions
- Content field definitions
- Format ownership per layout
- Chart/diagram interchangeability rules

**Audience**: Text Service developers, Director Agent developers, frontend developers

---

### **L02_DIRECTOR_INTEGRATION_GUIDE.md**
- L02 layout integration guide for Director Agent
- HTML vs plain text content handling
- Analytics Service integration patterns
- Troubleshooting blank screen issues
- Viewport requirements and best practices

**Audience**: Director Agent developers, Analytics Service integrators

---

### **CONTENT_GENERATION_GUIDE.md**
- HTML content generation guidelines for Text Service
- Layout-specific content requirements
- Inline styling best practices
- Content area dimensions and constraints

**Audience**: Text Service developers, AI content generators

---

### **CONTENT_EDITING_USER_GUIDE.md**
- User guide for content editing features
- Version history and restore functionality
- Slide-level content updates
- API usage examples

**Audience**: End users, application developers, integrators

---

## 🕒 Recent Documentation (docs/recent/)

Recent fixes, updates, and issue resolutions. These documents provide historical context for recent changes:

### **ANALYTICS_CHARTJS_ERROR.md**
- Error documentation for Analytics + Chart.js integration
- Blank screen issue diagnosis
- Resolution steps

### **APEXCHARTS_FIX_SUMMARY.md**
- Summary of ApexCharts integration fixes
- Configuration updates
- Testing results

### **CHART_RENDERING_FIX_COMPLETE.md**
- Complete documentation of chart rendering fixes
- Before/after comparisons
- Implementation details

**Note**: These documents are useful for understanding recent changes but may be archived once fixes are stable and well-tested.

---

## 🗄️ Archived Documentation (docs/archive/)

Reference material and outdated documentation:

### **REVEALJS_CAPABILITIES.md**
- Reveal.js framework capabilities reference
- May be outdated or superseded by official Reveal.js docs
- Kept for historical reference

---

## 🎯 Quick Reference Guide

### For Text Service Developers
1. Start with **CONTENT_GENERATION_GUIDE.md**
2. Reference **LAYOUT_SPECIFICATIONS.md** for dimensions
3. Check **ARCHITECTURE.md** for format ownership rules

### For Director Agent Developers
1. Start with **L02_DIRECTOR_INTEGRATION_GUIDE.md** (if using L02)
2. Reference **LAYOUT_SPECIFICATIONS.md** for all layouts
3. Check **ARCHITECTURE.md** for integration patterns

### For System Architects
1. Start with **ARCHITECTURE.md**
2. Review **LAYOUT_SPECIFICATIONS.md** for layout details
3. Check recent/ folder for latest fixes and updates

### For End Users
1. Start with **CONTENT_EDITING_USER_GUIDE.md**
2. Reference main **README.md** (in project root) for quick start

---

## 📝 Documentation Maintenance

### When to Update Documentation

**Critical docs/** - Update when:
- System architecture changes
- New layouts are added or removed
- Integration patterns change
- Format ownership model changes

**Recent docs/recent/** - Add when:
- Fixing bugs or issues
- Implementing new features
- Resolving integration problems

**Archive docs/archive/** - Move to archive when:
- Documentation becomes outdated
- Features are deprecated
- Content is superseded by newer docs

### Moving Documents Between Folders

**Promote from recent/ to docs/** when:
- A recent fix becomes a permanent feature
- Integration pattern becomes standard
- Content needs to be referenced frequently

**Archive from docs/ to archive/** when:
- Feature is deprecated
- Documentation is superseded
- Content is rarely accessed

**Archive from recent/ to archive/** when:
- Fix is stable and well-understood (6+ months)
- Issue is no longer relevant
- Content is superseded by newer documentation

---

## 🔗 Related Documentation

- **Main README.md**: Project overview, quick start, API reference (in project root)
- **API Documentation**: Auto-generated at `/docs` endpoint (FastAPI)
- **Test Files**: `test_*.json` in project root for API testing examples

---

## ✅ Document Status

| Document | Status | Last Updated | Next Review |
|----------|--------|--------------|-------------|
| ARCHITECTURE.md | ✅ Current | 2025-01-01 | 2025-04-01 |
| LAYOUT_SPECIFICATIONS.md | ✅ Current | 2025-01-16 | 2025-04-01 |
| CONTENT_GENERATION_GUIDE.md | ✅ Current | 2025-01-01 | 2025-04-01 |
| L02_DIRECTOR_INTEGRATION_GUIDE.md | ✅ Current | 2025-01-16 | 2025-04-01 |
| CONTENT_EDITING_USER_GUIDE.md | ✅ Current | 2025-01-16 | 2025-04-01 |
| recent/* | 📅 Recent | 2025-01-15 | 2025-07-01 |
| archive/* | 🗄️ Archived | Various | N/A |

---

**End of Documentation Index**
