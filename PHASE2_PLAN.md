# Phase 2: Section Selection & Review Mode - Implementation Plan

**Branch**: `feature/world-class-editor-phase2`
**Started**: 2025-01-24
**Status**: In Progress
**Goal**: Enable intelligent section-based selection and AI-powered regeneration

---

## Overview

Phase 2 introduces the **critical foundation** for transforming v7.5-main into a world-class AI-powered presentation editor. This phase enables users to:

1. **Select specific sections** within slides (not just entire slides)
2. **Enter Review Mode** to visually identify and select sections
3. **Provide AI instructions** for selected sections
4. **Regenerate content** using Director Service integration
5. **Preview and apply** AI-generated improvements

This is the **killer feature** that makes our editor unique compared to Google Slides.

---

## Architecture Overview

```
User Flow:
1. Toggle Review Mode (new button)
2. Click to select sections (blue highlight)
3. Enter AI instruction ("Make it more engaging")
4. Click "Regenerate with AI"
5. Preview side-by-side comparison
6. Accept/Reject/Retry
7. Apply changes with version tracking
```

**Section ID System**:
- Format: `slide-{slideIndex}-section-{sectionType}`
- Examples:
  - `slide-0-section-title`
  - `slide-0-section-subtitle`
  - `slide-0-section-content`
  - `slide-1-section-chart`

**Data Attributes**:
- `data-section-id`: Unique identifier
- `data-section-type`: Type (title, subtitle, content, chart, diagram, text, body, hero)
- `data-slide-index`: Slide position (0-indexed)

---

## Section Mappings by Layout

### L01: Centered Chart with Text Below
- `title` → slide_title (element)
- `subtitle` → element_1
- `chart` → element_4 (chart/diagram container)
- `body` → element_3 (text below chart)

### L02: Left Diagram with Right Text
- `title` → slide_title
- `subtitle` → element_1
- `diagram` → element_3 (left side, 1260×720px)
- `text` → element_2 (right side, 540×720px)

### L03: Dual Charts with Bottom Text
- `title` → slide_title
- `subtitle` → element_1
- `chart1` → element_5 (left chart)
- `chart2` → element_6 (right chart)
- `body` → element_3 (text below charts)

### L25: Main Content Shell
- `title` → slide_title
- `subtitle` → subtitle/element_1
- `content` → rich_content (main content area, 1800×720px)

### L27: Image with Side Text
- `title` → slide_title
- `subtitle` → subtitle
- `image` → element_4 (image container)
- `text` → element_3 (side text)

### L29: Hero/Title Slide
- `hero` → hero_content (full-slide content)

---

## Progress Tracking

### ✅ Completed (Commit: e42fa02)

1. **Layout Renderers - Section IDs Added**
   - ✅ L01.js (title, subtitle, chart, body)
   - ✅ L02.js (title, subtitle, diagram, text)
   - ✅ L25.js (title, subtitle, content)

2. **Function Signature Updates**
   - ✅ All completed renderers now accept `slideIndex` parameter
   - ✅ Section IDs generated dynamically based on slide position

### 🔄 In Progress

3. **Layout Renderers - Remaining**
   - ⏳ L03.js (title, subtitle, chart1, chart2, body)
   - ⏳ L27.js (title, subtitle, image, text)
   - ⏳ L29.js (hero)

### 📝 Pending

4. **Viewer Integration**
   - ⏳ Update `presentation-viewer.html` rendering loop to pass `slideIndex`
   - ⏳ Add Review Mode toggle button to UI
   - ⏳ Add section selection indicator (floating badge)

5. **Review Mode System**
   - ⏳ Create `src/utils/review-mode.js`
     - Enter/exit review mode functions
     - Make sections selectable
     - Handle section click events
     - Visual feedback (hover, selected states)

6. **Section Selection Manager**
   - ⏳ Create `src/utils/section-selection.js`
     - Track selected sections (Set data structure)
     - Extract section content and metadata
     - Build API request payloads
     - Multi-select support (Ctrl+Click)

7. **AI Regeneration Panel**
   - ⏳ Create `src/components/regeneration-panel.js`
     - Floating panel when sections selected
     - Text input for user instructions
     - "Regenerate with AI" button
     - Loading states and error handling

8. **CSS Styling**
   - ⏳ Create `src/styles/review-mode.css`
     - Selectable section styles (.selectable)
     - Selected section highlight (.selected)
     - Hover effects
     - Review mode indicators
   - ⏳ Create `src/styles/regeneration-panel.css`
     - Panel positioning and styling
     - Button styles
     - Responsive design

9. **Backend Data Models**
   - ⏳ Update `models.py` with:
     - `SectionRegenerationRequest`
     - `SectionRegenerationResponse`
     - `RegenerationHistoryEntry`

10. **API Endpoints**
    - ⏳ Add `POST /api/presentations/{id}/regenerate-section`
    - ⏳ Add `GET /api/presentations/{id}/sections` (section metadata)
    - ⏳ Add `GET /api/presentations/{id}/sections/{section_id}/history`

11. **Testing**
    - ⏳ Manual testing of section selection
    - ⏳ Verify section IDs are correct
    - ⏳ Test review mode toggle
    - ⏳ Test regeneration panel appearance

---

## Implementation Steps

### Step 1: Complete Layout Renderers (Next) ⭐

**Files to Modify**:
- `src/renderers/L03.js`
- `src/renderers/L27.js`
- `src/renderers/L29.js`

**Changes**:
1. Add `slideIndex = 0` parameter to function signature
2. Add `data-section-id`, `data-section-type`, `data-slide-index` to each editable section
3. Follow same pattern as L01, L02, L25

**Example for L03**:
```javascript
function renderL03(content, slide = {}, slideIndex = 0) {
  // ...
  return `
    <section data-layout="L03" class="content-slide grid-container">
      <div class="slide-title"
           data-section-id="slide-${slideIndex}-section-title"
           data-section-type="title"
           data-slide-index="${slideIndex}">
        ${content.slide_title}
      </div>
      <!-- Additional sections... -->
    </section>
  `;
}
```

### Step 2: Update Viewer to Pass slideIndex

**File**: `viewer/presentation-viewer.html`

**Find** (around line 185):
```javascript
const slideHTML = renderer(content, slide);
```

**Replace with**:
```javascript
const slideHTML = renderer(content, slide, slideIndex);
```

### Step 3: Create Review Mode System

**File**: `src/utils/review-mode.js` (NEW)

```javascript
/**
 * Review Mode for Section Selection
 * Enables visual selection of slide sections for AI regeneration
 */

let reviewModeActive = false;
const selectedSections = new Set();

/**
 * Enter Review Mode - makes sections selectable
 */
function enterReviewMode() {
  reviewModeActive = true;
  document.body.dataset.mode = 'review';

  console.log('📋 Entering Review Mode...');

  // Find all sections with section IDs
  const sections = document.querySelectorAll('[data-section-id]');
  console.log(`Found ${sections.length} selectable sections`);

  // Make sections selectable
  sections.forEach(section => {
    section.classList.add('selectable');
    section.addEventListener('click', handleSectionClick);
  });

  // Show selection indicator
  showSelectionIndicator();
  showNotification('📋 Review Mode Active - Click sections to select', 'info');
}

/**
 * Exit Review Mode - restore normal view
 */
function exitReviewMode() {
  reviewModeActive = false;
  document.body.dataset.mode = 'view';

  // Remove selectable state
  const sections = document.querySelectorAll('[data-section-id]');
  sections.forEach(section => {
    section.classList.remove('selectable', 'selected');
    section.removeEventListener('click', handleSectionClick);
  });

  // Clear selection
  clearSelection();
  hideSelectionIndicator();
  showNotification('Review Mode Exited', 'info');
}

/**
 * Toggle Review Mode on/off
 */
function toggleReviewMode() {
  if (reviewModeActive) {
    exitReviewMode();
  } else {
    enterReviewMode();
  }
}

/**
 * Handle section click in review mode
 */
function handleSectionClick(event) {
  if (!reviewModeActive) return;

  event.stopPropagation();
  const sectionId = event.currentTarget.dataset.sectionId;

  if (event.ctrlKey || event.metaKey) {
    // Multi-select with Ctrl/Cmd
    toggleSectionSelection(sectionId);
  } else {
    // Single select - clear others first
    clearSelection();
    selectSection(sectionId);
  }
}

/**
 * Select a section
 */
function selectSection(sectionId) {
  selectedSections.add(sectionId);
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (element) {
    element.classList.add('selected');
  }
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log(`✅ Selected: ${sectionId}`);
}

/**
 * Deselect a section
 */
function deselectSection(sectionId) {
  selectedSections.delete(sectionId);
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (element) {
    element.classList.remove('selected');
  }
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log(`❌ Deselected: ${sectionId}`);
}

/**
 * Toggle section selection
 */
function toggleSectionSelection(sectionId) {
  if (selectedSections.has(sectionId)) {
    deselectSection(sectionId);
  } else {
    selectSection(sectionId);
  }
}

/**
 * Clear all selections
 */
function clearSelection() {
  selectedSections.forEach(sectionId => {
    const element = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (element) {
      element.classList.remove('selected');
    }
  });
  selectedSections.clear();
  updateSelectionIndicator();
  updateRegenerationPanel();

  console.log('🧹 Selection cleared');
}

/**
 * Get selected sections with metadata
 */
function getSelectedSections() {
  const sections = [];

  selectedSections.forEach(sectionId => {
    const element = document.querySelector(`[data-section-id="${sectionId}"]`);
    if (element) {
      sections.push({
        sectionId: element.dataset.sectionId,
        sectionType: element.dataset.sectionType,
        slideIndex: parseInt(element.dataset.slideIndex),
        content: element.innerHTML,
        layout: element.closest('[data-layout]')?.dataset.layout || 'unknown'
      });
    }
  });

  return sections;
}

/**
 * Show selection indicator (floating badge)
 */
function showSelectionIndicator() {
  let indicator = document.getElementById('selection-indicator');
  if (!indicator) {
    indicator = document.createElement('div');
    indicator.id = 'selection-indicator';
    indicator.className = 'selection-indicator';
    document.body.appendChild(indicator);
  }
  updateSelectionIndicator();
}

/**
 * Update selection indicator count
 */
function updateSelectionIndicator() {
  const indicator = document.getElementById('selection-indicator');
  if (indicator) {
    const count = selectedSections.size;
    indicator.textContent = `${count} section${count !== 1 ? 's' : ''} selected`;
    indicator.style.display = count > 0 ? 'block' : 'none';
  }
}

/**
 * Hide selection indicator
 */
function hideSelectionIndicator() {
  const indicator = document.getElementById('selection-indicator');
  if (indicator) {
    indicator.style.display = 'none';
  }
}

/**
 * Show/hide regeneration panel based on selection
 */
function updateRegenerationPanel() {
  const panel = document.getElementById('regeneration-panel');
  if (panel) {
    panel.style.display = selectedSections.size > 0 ? 'block' : 'none';
  }
}

// Export functions
if (typeof window !== 'undefined') {
  window.enterReviewMode = enterReviewMode;
  window.exitReviewMode = exitReviewMode;
  window.toggleReviewMode = toggleReviewMode;
  window.getSelectedSections = getSelectedSections;
  window.clearSelection = clearSelection;
}
```

### Step 4: Create Section Selection Manager

**File**: `src/utils/section-selection.js` (NEW)

Simple state manager - most logic is in review-mode.js. This file can be minimal or merged into review-mode.js.

### Step 5: Create AI Regeneration Panel Component

**File**: `src/components/regeneration-panel.js` (NEW)

```javascript
/**
 * AI Regeneration Panel
 * Appears when sections are selected in review mode
 */

/**
 * Regenerate selected sections with AI
 */
async function regenerateSelectedSections() {
  const sections = getSelectedSections();

  if (sections.length === 0) {
    showNotification('No sections selected', 'warning');
    return;
  }

  const instruction = document.getElementById('ai-instruction-input')?.value;
  if (!instruction || instruction.trim() === '') {
    showNotification('Please enter an instruction for the AI', 'warning');
    return;
  }

  console.log(`🤖 Regenerating ${sections.length} section(s) with AI...`);
  showNotification('🤖 Regenerating with AI...', 'info');

  try {
    for (const section of sections) {
      console.log(`Processing: ${section.sectionId}`);

      const response = await fetch(
        `/api/presentations/${PRESENTATION_DATA.id || 'current'}/regenerate-section`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            slide_index: section.slideIndex,
            section_id: section.sectionId,
            section_type: section.sectionType,
            user_instruction: instruction.trim(),
            current_content: section.content,
            layout: section.layout
          })
        }
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();

      if (data.success) {
        // Update section in DOM
        updateSectionInDOM(section.sectionId, data.updated_content);
        console.log(`✅ Updated: ${section.sectionId}`);
      } else {
        throw new Error(data.message || 'Regeneration failed');
      }
    }

    showNotification(`✅ ${sections.length} section(s) regenerated successfully!`, 'success');
    clearSelection();

    // Clear instruction input
    const input = document.getElementById('ai-instruction-input');
    if (input) input.value = '';

  } catch (error) {
    console.error('Regeneration error:', error);
    showNotification(`❌ Error: ${error.message}`, 'error');
  }
}

/**
 * Update section content in DOM with animation
 */
function updateSectionInDOM(sectionId, newContent) {
  const element = document.querySelector(`[data-section-id="${sectionId}"]`);
  if (!element) {
    console.warn(`Section not found: ${sectionId}`);
    return;
  }

  // Fade out animation
  element.style.transition = 'opacity 0.3s ease';
  element.style.opacity = '0.3';

  setTimeout(() => {
    // Update content
    element.innerHTML = newContent;

    // Fade in animation
    element.style.opacity = '1';

    // Highlight briefly
    element.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
    setTimeout(() => {
      element.style.backgroundColor = '';
    }, 2000);
  }, 300);
}

// Export functions
if (typeof window !== 'undefined') {
  window.regenerateSelectedSections = regenerateSelectedSections;
}
```

### Step 6: Add CSS Styles

**File**: `src/styles/review-mode.css` (NEW)

```css
/**
 * Review Mode Styles for Section Selection
 */

/* Review Mode Indicator */
body[data-mode="review"]::after {
  content: "📋 REVIEW MODE - Click sections to select";
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background: #3b82f6;
  color: white;
  padding: 8px 24px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  z-index: 9999;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* Selectable Sections */
.selectable {
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.selectable:hover {
  outline: 2px dashed #3b82f6;
  outline-offset: 4px;
  background-color: rgba(59, 130, 246, 0.05);
}

/* Selected Sections */
.selectable.selected {
  outline: 3px solid #3b82f6;
  outline-offset: 4px;
  background-color: rgba(59, 130, 246, 0.1);
}

/* Selection Indicator Badge */
.selection-indicator {
  position: fixed;
  top: 60px;
  right: 20px;
  background: #3b82f6;
  color: white;
  padding: 12px 20px;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 600;
  z-index: 10001;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  display: none;
}

/* Review Mode Toggle Button */
#toggle-review-mode {
  position: fixed;
  top: 20px;
  left: 20px;
  padding: 12px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  z-index: 10000;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: all 0.2s ease;
}

#toggle-review-mode:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

#toggle-review-mode.active {
  background: #10b981;
}

#toggle-review-mode.active:hover {
  background: #059669;
}
```

**File**: `src/styles/regeneration-panel.css` (NEW)

```css
/**
 * AI Regeneration Panel Styles
 */

#regeneration-panel {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 20px 24px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  z-index: 10001;
  display: none;
  min-width: 500px;
  max-width: 700px;
}

#regeneration-panel h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #1f2937;
  font-weight: 600;
}

#regeneration-panel .input-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

#ai-instruction-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s ease;
}

#ai-instruction-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

#regenerate-btn {
  padding: 12px 24px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

#regenerate-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

#regenerate-btn:active {
  transform: translateY(0);
}

#cancel-selection-btn {
  padding: 12px 24px;
  background: #6b7280;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

#cancel-selection-btn:hover {
  background: #4b5563;
}

@media (max-width: 768px) {
  #regeneration-panel {
    min-width: 90%;
    bottom: 20px;
  }

  #regeneration-panel .input-group {
    flex-direction: column;
  }

  #regenerate-btn,
  #cancel-selection-btn {
    width: 100%;
  }
}
```

### Step 7: Update Viewer HTML

**File**: `viewer/presentation-viewer.html`

Add after line 74 (after edit-shortcuts div):

```html
<!-- Review Mode Toggle Button -->
<button id="toggle-review-mode" onclick="toggleReviewMode()">📋 Review Mode</button>

<!-- Selection Indicator -->
<div id="selection-indicator" class="selection-indicator"></div>

<!-- AI Regeneration Panel -->
<div id="regeneration-panel">
  <h3>🤖 AI Regeneration</h3>
  <div class="input-group">
    <input
      type="text"
      id="ai-instruction-input"
      placeholder="Enter instruction (e.g., Make it more engaging with examples)"
    />
    <button id="regenerate-btn" onclick="regenerateSelectedSections()">
      Regenerate with AI
    </button>
    <button id="cancel-selection-btn" onclick="clearSelection()">
      Cancel
    </button>
  </div>
</div>
```

Add in `<head>` section:
```html
<!-- Review Mode & Regeneration Styles -->
<link rel="stylesheet" href="/src/styles/review-mode.css">
<link rel="stylesheet" href="/src/styles/regeneration-panel.css">
```

Add before closing `</body>`:
```html
<!-- Review Mode & Section Selection -->
<script src="/src/utils/review-mode.js"></script>
<script src="/src/components/regeneration-panel.js"></script>
```

Update rendering loop (around line 185):
```javascript
// OLD:
const slideHTML = renderer(content, slide);

// NEW:
const slideHTML = renderer(content, slide, slideIndex);
```

### Step 8: Backend Data Models

**File**: `models.py`

Add these new models:

```python
class SectionRegenerationRequest(BaseModel):
    """Request to regenerate a specific section with AI"""
    slide_index: int = Field(..., description="Zero-based slide index")
    section_id: str = Field(..., description="Section ID (e.g., slide-0-section-title)")
    section_type: str = Field(..., description="Section type (title, subtitle, content, etc.)")
    user_instruction: str = Field(..., description="User's instruction for AI regeneration")
    current_content: str = Field(..., description="Current HTML content of the section")
    layout: str = Field(..., description="Layout ID (L01, L02, etc.)")

class SectionRegenerationResponse(BaseModel):
    """Response from section regeneration"""
    success: bool
    section_id: str
    updated_content: str
    message: str = "Section regenerated successfully"

class RegenerationHistoryEntry(BaseModel):
    """History entry for section regeneration"""
    id: str
    section_id: str
    slide_index: int
    timestamp: str
    user_instruction: str
    original_content: str
    regenerated_content: str
    accepted: bool
    created_by: str = "user"
```

### Step 9: API Endpoint

**File**: `server.py`

Add new endpoint:

```python
@app.post("/api/presentations/{presentation_id}/regenerate-section")
async def regenerate_section(
    presentation_id: str,
    request: SectionRegenerationRequest
):
    """
    Regenerate a specific section using Director Service AI

    This is a PLACEHOLDER implementation that returns mock data.
    TODO: Integrate with actual Director Service API
    """
    try:
        # Load presentation
        presentation = await storage.load(presentation_id)
        if not presentation:
            raise HTTPException(status_code=404, detail="Presentation not found")

        # Validate slide index
        if request.slide_index < 0 or request.slide_index >= len(presentation["slides"]):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid slide index {request.slide_index}"
            )

        # TODO: Call Director Service API here
        # For now, return mock enhanced content

        # Mock AI regeneration (simple transformation for testing)
        enhanced_content = f"""
        <div style="padding: 20px; background: rgba(59, 130, 246, 0.05); border-left: 4px solid #3b82f6;">
            <p style="margin: 0 0 10px 0; color: #3b82f6; font-weight: bold;">
                ✨ AI Enhanced (Mock)
            </p>
            <div>{request.current_content}</div>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #6b7280; font-style: italic;">
                Instruction: "{request.user_instruction}"
            </p>
        </div>
        """

        # TODO: Update actual slide content in storage
        # For now, just return the enhanced content without saving

        return SectionRegenerationResponse(
            success=True,
            section_id=request.section_id,
            updated_content=enhanced_content,
            message=f"Section {request.section_type} regenerated (mock)"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error regenerating section: {str(e)}"
        )
```

---

## Testing Plan

### Manual Testing Checklist

1. **Section IDs**
   - [ ] All layouts render section IDs correctly
   - [ ] Section IDs follow naming convention
   - [ ] Data attributes present on all sections

2. **Review Mode**
   - [ ] Toggle button appears and works
   - [ ] Sections become selectable in review mode
   - [ ] Hover highlights sections
   - [ ] Click selects section (blue outline)
   - [ ] Ctrl+Click multi-selects
   - [ ] Selection indicator shows count

3. **Regeneration Panel**
   - [ ] Panel appears when sections selected
   - [ ] Input accepts user instructions
   - [ ] Regenerate button triggers API call
   - [ ] Loading state shows during regeneration
   - [ ] Success notification appears
   - [ ] Content updates in DOM with animation

4. **Edge Cases**
   - [ ] Works with all 6 layouts
   - [ ] Handles empty sections
   - [ ] API errors show user-friendly messages
   - [ ] Multiple selections work correctly
   - [ ] Clear selection works

---

## Next Phase Preview

### Phase 3: AI Integration & Director Service
- Real Director Service API integration
- Preview mode (side-by-side comparison)
- Accept/Reject/Retry workflow
- Regeneration history tracking
- Smart context preservation
- Batch regeneration

---

## Notes & Decisions

**Why Section IDs at Runtime?**
- No database migration required
- Works with existing presentations
- IDs generated fresh on each render
- Slide index determines uniqueness

**Why Review Mode vs. Always Selectable?**
- Cleaner user experience
- No accidental selections during presentation
- Clear separation: View → Review → Edit modes

**Mock API for Phase 2?**
- YES - allows frontend development without Director dependency
- Mock returns simple enhanced content
- Real integration in Phase 3

---

**Last Updated**: 2025-01-24
**Next Commit**: Complete L03, L27, L29 + Viewer integration + Review mode UI
