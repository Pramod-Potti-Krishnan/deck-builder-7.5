#!/bin/bash
# Quick verification that the fix is deployed
# Usage: ./verify_deployment.sh [BASE_URL]

BASE_URL="${1:-http://localhost:8000}"
echo "Checking deployment at: $BASE_URL"
echo ""

# Fetch the direct-element-creator.js and check for the fix
JS_URL="$BASE_URL/src/utils/direct-element-creator.js"

echo "Fetching: $JS_URL"
CONTENT=$(curl -s "$JS_URL" 2>/dev/null)

if [ -z "$CONTENT" ]; then
  echo "❌ Could not fetch JavaScript file"
  exit 1
fi

# Check for v7.5.2 version string
if echo "$CONTENT" | grep -q "v7.5.2"; then
  echo "✅ Version v7.5.2 detected - LATEST DEPLOYED"
else
  echo "⚠️  Version v7.5.2 NOT found - may be stale deployment"
fi

# Check for the mode indicator in console log
if echo "$CONTENT" | grep -q '(content)'; then
  echo "✅ Content mode indicator found - FIX IS DEPLOYED"
else
  echo "❌ Content mode indicator NOT found - FIX NOT DEPLOYED"
fi

# Check for getInfographicContent function
if echo "$CONTENT" | grep -q "getInfographicContent"; then
  echo "✅ getInfographicContent() helper found"
else
  echo "❌ getInfographicContent() helper NOT found"
fi

# Check for getDiagramContent function
if echo "$CONTENT" | grep -q "getDiagramContent"; then
  echo "✅ getDiagramContent() helper found"
else
  echo "❌ getDiagramContent() helper NOT found"
fi

echo ""
echo "If any ❌ markers above, the fix is NOT deployed."
echo "Wait for Railway to complete redeploy, then run again."
