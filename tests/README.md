# Test Files - v7.5-main Layout Builder

**Last Updated**: November 16, 2025

This directory contains test files and test scripts for v7.5-main Layout Builder.

---

## 📁 Directory Structure

```
tests/
├── README.md                           # This file (test documentation)
├── test_editing_api.py                 # Content editing API tests (RECENT)
├── test_l02_html_support.py            # L02 HTML support tests (RECENT)
├── test_real_apexcharts.json           # ApexCharts integration test (RECENT)
├── test_analytics_apexcharts.json      # Analytics + ApexCharts test (RECENT)
├── test_all_6_layouts_fixed.json       # All 6 layouts test suite (RECENT)
└── archive/                            # Older/deprecated test files
    ├── test_all_6_layouts.json
    ├── test_borders_demo.json
    ├── test_logo_positioning.json
    └── test-presentation.json
```

---

## 🧪 Recent Test Files (tests/)

### **test_editing_api.py**
**Purpose**: Test content editing API endpoints
**Created**: November 16, 2025
**Type**: Python test script (pytest/unittest)

**Tests**:
- Slide content updates (PUT /api/presentations/{id}/slides/{index})
- Presentation metadata updates
- Version history functionality
- Restore version functionality

**Run**:
```bash
python test_editing_api.py
# or
pytest test_editing_api.py
```

---

### **test_l02_html_support.py**
**Purpose**: Test L02 layout HTML rendering support
**Created**: November 16, 2025
**Type**: Python test script

**Tests**:
- HTML content rendering in element_2 and element_3
- Plain text backward compatibility
- Analytics chart integration
- Chart.js script execution
- Blank screen issue resolution

**Run**:
```bash
python test_l02_html_support.py
```

---

### **test_real_apexcharts.json**
**Purpose**: Test real-world ApexCharts integration
**Created**: November 16, 2025
**Type**: JSON test data

**Tests**:
- ApexCharts rendering in L02 layout
- Chart configuration and options
- Responsive chart behavior
- Real chart data visualization

**Usage**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_real_apexcharts.json
```

---

### **test_analytics_apexcharts.json**
**Purpose**: Test Analytics Service integration with ApexCharts
**Created**: November 15, 2025
**Type**: JSON test data

**Tests**:
- Analytics Service response format
- ApexCharts configuration from Analytics
- element_2 and element_3 HTML rendering
- Chart + observations layout

**Usage**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_analytics_apexcharts.json
```

---

### **test_all_6_layouts_fixed.json**
**Purpose**: Comprehensive test of all 6 layouts (L01-L29)
**Created**: November 13, 2025
**Type**: JSON test data

**Tests**:
- L01: Centered Chart/Diagram
- L02: Diagram Left + Text Right
- L03: Two Charts Side-by-Side
- L25: Rich Content Shell
- L27: Image Left + Content Right
- L29: Hero Full-Bleed

**Usage**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_all_6_layouts_fixed.json
```

---

## 🗄️ Archived Test Files (tests/archive/)

### **test_all_6_layouts.json**
**Purpose**: Original all-layouts test (superseded by test_all_6_layouts_fixed.json)
**Created**: November 13, 2025
**Status**: Archived - replaced by fixed version

---

### **test_borders_demo.json**
**Purpose**: Test border toggle functionality
**Created**: November 13, 2025
**Status**: Archived - feature stable

---

### **test_logo_positioning.json**
**Purpose**: Test company logo positioning in footer
**Created**: November 13, 2025
**Status**: Archived - feature stable

---

### **test-presentation.json**
**Purpose**: Original basic presentation test
**Created**: November 10, 2025
**Status**: Archived - superseded by newer tests

---

## 🚀 Quick Start

### Running Python Tests

```bash
# Run all Python tests
python -m pytest tests/

# Run specific test file
python tests/test_editing_api.py

# Run with verbose output
pytest tests/ -v
```

### Testing with JSON Files

```bash
# Start the server first
python server.py

# In another terminal, test with JSON
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_all_6_layouts_fixed.json

# Response will include presentation URL like:
# {"id": "uuid", "url": "/p/uuid", "message": "..."}

# Open in browser
open http://localhost:8504/p/{uuid}
```

### Testing Specific Features

**Content Editing**:
```bash
python tests/test_editing_api.py
```

**L02 HTML Support**:
```bash
python tests/test_l02_html_support.py
```

**Analytics Integration**:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @tests/test_analytics_apexcharts.json
```

---

## 📝 Test Coverage

### API Endpoints
- ✅ `POST /api/presentations` - Create presentation
- ✅ `GET /api/presentations/{id}` - Get presentation
- ✅ `PUT /api/presentations/{id}` - Update metadata
- ✅ `PUT /api/presentations/{id}/slides/{index}` - Update slide
- ✅ `GET /api/presentations/{id}/versions` - Version history
- ✅ `POST /api/presentations/{id}/restore/{version_id}` - Restore version
- ✅ `GET /p/{id}` - View presentation
- ✅ `DELETE /api/presentations/{id}` - Delete presentation

### Layout Coverage
- ✅ L01: Centered Chart/Diagram
- ✅ L02: Diagram Left + Text Right (HTML support)
- ✅ L03: Two Charts Side-by-Side
- ✅ L25: Rich Content Shell
- ✅ L27: Image Left + Content Right
- ✅ L29: Hero Full-Bleed

### Feature Coverage
- ✅ Content editing
- ✅ Version history
- ✅ Restore versions
- ✅ HTML rendering in L02
- ✅ Chart integration (Chart.js, ApexCharts)
- ✅ Analytics Service integration
- ✅ Footer components (presentation name, logo)
- ✅ Grid system
- ✅ Border toggle

---

## 🔧 Writing New Tests

### Python Test Template

```python
"""
Test: [Feature Name]
Purpose: [What this tests]
"""

import requests

BASE_URL = "http://localhost:8504"

def test_feature_name():
    """Test description"""
    # Arrange
    test_data = {
        "title": "Test Presentation",
        "slides": [...]
    }

    # Act
    response = requests.post(
        f"{BASE_URL}/api/presentations",
        json=test_data
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "url" in data

    print(f"✅ Test passed: {data['url']}")

if __name__ == "__main__":
    test_feature_name()
```

### JSON Test Template

```json
{
  "title": "Test: [Feature Name]",
  "slides": [
    {
      "layout": "L25",
      "content": {
        "slide_title": "Test Slide",
        "subtitle": "Testing [feature]",
        "rich_content": "<div>Test content</div>"
      }
    }
  ]
}
```

---

## 📊 Test Maintenance

### When to Add New Tests

**Add to tests/ (recent)** when:
- Testing new features
- Verifying bug fixes
- Validating integration changes
- Testing edge cases

**Move to archive/** when:
- Test is superseded by newer version
- Feature is stable and well-tested (6+ months)
- Test data is outdated
- Test is no longer relevant

### Test File Naming

- **Python scripts**: `test_[feature_name].py`
- **JSON data**: `test_[feature_name].json`
- Use descriptive names that indicate what is being tested

### Version Control

All test files are tracked in git. Use meaningful commit messages:
```bash
git add tests/test_new_feature.py
git commit -m "test: Add tests for new feature X"
```

---

## 🐛 Troubleshooting

### Server Not Running
```bash
# Error: Connection refused
# Solution: Start the server
python server.py
```

### Port Already in Use
```bash
# Error: Port 8504 already in use
# Solution: Kill existing process or use different port
lsof -i :8504
kill -9 [PID]
# Or set PORT environment variable
PORT=8505 python server.py
```

### JSON Validation Error
```bash
# Error: 422 Unprocessable Entity
# Solution: Validate JSON structure matches Pydantic models
# Check: models.py for required fields and types
```

### Chart Not Rendering
```bash
# Check browser console (F12) for errors
# Verify Chart.js/ApexCharts loaded in presentation-viewer.html
# Ensure chart container has explicit dimensions
```

---

## 📚 Related Documentation

- **API Documentation**: http://localhost:8504/docs (FastAPI auto-docs)
- **Layout Specifications**: `../docs/LAYOUT_SPECIFICATIONS.md`
- **Architecture**: `../docs/ARCHITECTURE.md`
- **Integration Guides**: `../docs/L02_DIRECTOR_INTEGRATION_GUIDE.md`

---

## ✅ Test Status Summary

| Test File | Status | Last Run | Next Review |
|-----------|--------|----------|-------------|
| test_editing_api.py | ✅ Active | 2025-11-16 | 2025-12-16 |
| test_l02_html_support.py | ✅ Active | 2025-11-16 | 2025-12-16 |
| test_real_apexcharts.json | ✅ Active | 2025-11-16 | 2025-12-16 |
| test_analytics_apexcharts.json | ✅ Active | 2025-11-15 | 2025-12-15 |
| test_all_6_layouts_fixed.json | ✅ Active | 2025-11-13 | 2026-05-13 |
| archive/* | 🗄️ Archived | Various | N/A |

---

**End of Test Documentation**
