#!/bin/bash
# Test script for C4-infographic and C5-diagram content rendering
# Usage: ./test_infographic_diagram.sh [BASE_URL]
# Default: http://localhost:8000

BASE_URL="${1:-http://localhost:8000}"
echo "=============================================="
echo "Testing Infographic & Diagram Content Rendering"
echo "Base URL: $BASE_URL"
echo "=============================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Create a presentation with C4-infographic slide
echo -e "\n${YELLOW}Test 1: Creating presentation with C4-infographic${NC}"

RESPONSE=$(curl -s -X POST "$BASE_URL/api/presentations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Infographic Test",
    "slides": [{
      "layout": "C4-infographic",
      "content": {
        "slide_title": "Test Infographic Slide",
        "subtitle": "Testing HTML content rendering",
        "infographic_html": "<div style=\"background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 8px;\"><div style=\"text-align: center; color: white;\"><h2 style=\"font-size: 2em; margin-bottom: 10px;\">📊 Infographic Content</h2><p style=\"font-size: 1.2em;\">This is real HTML content, not a placeholder!</p></div></div>"
      }
    }]
  }')

PRES_ID=$(echo $RESPONSE | jq -r '.id // .presentation_id // empty')

if [ -n "$PRES_ID" ] && [ "$PRES_ID" != "null" ]; then
  echo -e "${GREEN}✓ Created presentation: $PRES_ID${NC}"

  # Check if infographic_html was stored
  GET_RESPONSE=$(curl -s "$BASE_URL/api/presentations/$PRES_ID")
  INFOGRAPHIC_HTML=$(echo $GET_RESPONSE | jq -r '.slides[0].content.infographic_html // empty')

  if [ -n "$INFOGRAPHIC_HTML" ] && [ "$INFOGRAPHIC_HTML" != "null" ]; then
    echo -e "${GREEN}✓ infographic_html stored (${#INFOGRAPHIC_HTML} chars)${NC}"
  else
    echo -e "${RED}✗ infographic_html NOT stored in response${NC}"
  fi

  # Open in browser for visual verification
  VIEWER_URL="$BASE_URL/viewer/presentation-viewer.html?id=$PRES_ID"
  echo -e "${YELLOW}→ View presentation: $VIEWER_URL${NC}"

  INFOGRAPHIC_PRES_ID=$PRES_ID
else
  echo -e "${RED}✗ Failed to create presentation${NC}"
  echo "Response: $RESPONSE"
fi

# Test 2: Create a presentation with C5-diagram slide
echo -e "\n${YELLOW}Test 2: Creating presentation with C5-diagram${NC}"

RESPONSE=$(curl -s -X POST "$BASE_URL/api/presentations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Diagram Test",
    "slides": [{
      "layout": "C5-diagram",
      "content": {
        "slide_title": "Test Diagram Slide",
        "subtitle": "Testing diagram HTML content",
        "diagram_html": "<div style=\"background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); height: 100%; display: flex; align-items: center; justify-content: center; border-radius: 8px;\"><div style=\"text-align: center; color: white;\"><h2 style=\"font-size: 2em; margin-bottom: 10px;\">🔷 Diagram Content</h2><p style=\"font-size: 1.2em;\">This is real diagram HTML, not a placeholder!</p><div style=\"margin-top: 20px; display: flex; justify-content: center; gap: 20px;\"><div style=\"width: 60px; height: 60px; background: rgba(255,255,255,0.3); border-radius: 50%;\"></div><div style=\"width: 60px; height: 60px; background: rgba(255,255,255,0.3); border-radius: 50%;\"></div><div style=\"width: 60px; height: 60px; background: rgba(255,255,255,0.3); border-radius: 50%;\"></div></div></div></div>"
      }
    }]
  }')

PRES_ID=$(echo $RESPONSE | jq -r '.id // .presentation_id // empty')

if [ -n "$PRES_ID" ] && [ "$PRES_ID" != "null" ]; then
  echo -e "${GREEN}✓ Created presentation: $PRES_ID${NC}"

  # Check if diagram_html was stored
  GET_RESPONSE=$(curl -s "$BASE_URL/api/presentations/$PRES_ID")
  DIAGRAM_HTML=$(echo $GET_RESPONSE | jq -r '.slides[0].content.diagram_html // empty')

  if [ -n "$DIAGRAM_HTML" ] && [ "$DIAGRAM_HTML" != "null" ]; then
    echo -e "${GREEN}✓ diagram_html stored (${#DIAGRAM_HTML} chars)${NC}"
  else
    echo -e "${RED}✗ diagram_html NOT stored in response${NC}"
  fi

  # Open in browser for visual verification
  VIEWER_URL="$BASE_URL/viewer/presentation-viewer.html?id=$PRES_ID"
  echo -e "${YELLOW}→ View presentation: $VIEWER_URL${NC}"

  DIAGRAM_PRES_ID=$PRES_ID
else
  echo -e "${RED}✗ Failed to create presentation${NC}"
  echo "Response: $RESPONSE"
fi

# Test 3: Combined test with both layouts
echo -e "\n${YELLOW}Test 3: Creating presentation with both C4 and C5 slides${NC}"

RESPONSE=$(curl -s -X POST "$BASE_URL/api/presentations" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Combined Infographic & Diagram Test",
    "slides": [
      {
        "layout": "C4-infographic",
        "content": {
          "slide_title": "Infographic Slide",
          "infographic_html": "<div style=\"background: #4A90A4; height: 100%; padding: 20px; box-sizing: border-box;\"><h3 style=\"color: white;\">📈 Real Infographic</h3><p style=\"color: white;\">Content mode working!</p></div>"
        }
      },
      {
        "layout": "C5-diagram",
        "content": {
          "slide_title": "Diagram Slide",
          "diagram_html": "<div style=\"background: #6B4A8A; height: 100%; padding: 20px; box-sizing: border-box;\"><h3 style=\"color: white;\">🔷 Real Diagram</h3><p style=\"color: white;\">Content mode working!</p></div>"
        }
      }
    ]
  }')

PRES_ID=$(echo $RESPONSE | jq -r '.id // .presentation_id // empty')

if [ -n "$PRES_ID" ] && [ "$PRES_ID" != "null" ]; then
  echo -e "${GREEN}✓ Created combined presentation: $PRES_ID${NC}"
  VIEWER_URL="$BASE_URL/viewer/presentation-viewer.html?id=$PRES_ID"
  echo -e "${YELLOW}→ View presentation: $VIEWER_URL${NC}"
else
  echo -e "${RED}✗ Failed to create combined presentation${NC}"
  echo "Response: $RESPONSE"
fi

# Summary
echo -e "\n=============================================="
echo -e "${YELLOW}VERIFICATION STEPS:${NC}"
echo "=============================================="
echo "1. Open the viewer URLs above in a browser"
echo "2. Open DevTools (F12) → Console tab"
echo "3. Look for these logs:"
echo "   - 'Created Infographic (content): ...' ← SUCCESS"
echo "   - 'Created Infographic (placeholder): ...' ← PROBLEM"
echo ""
echo "4. Check that slides show:"
echo "   - Gradient backgrounds with text"
echo "   - NOT gray placeholder boxes"
echo ""
echo "5. If you see (placeholder) or gray boxes:"
echo "   - Clear browser cache: Cmd+Shift+R / Ctrl+Shift+R"
echo "   - Check Railway deployment status"
echo "=============================================="
