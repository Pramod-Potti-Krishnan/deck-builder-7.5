/**
 * Split, Visual, and Image Template Renderers for Frontend Slide Templates
 *
 * These renderers use the NEW Direct Element Creation approach:
 * - Render blank grid container only
 * - Elements are created after render by DirectElementCreator using ElementManager
 * - All styles come from TEMPLATE_REGISTRY
 *
 * Visual + Text Templates (V1-V4):
 * - V1: Image + Text (image on left, text insights on right)
 * - V2: Chart + Text (chart on left, text insights on right)
 * - V3: Diagram + Text (diagram on left, text insights on right)
 * - V4: Infographic + Text (infographic on left, text insights on right)
 *
 * Image Split Templates (I1-I4):
 * - I1: Image Left Wide (12 cols image left, content right)
 * - I2: Image Right Wide (12 cols image right, content left)
 * - I3: Image Left Narrow (6 cols image left, content right)
 * - I4: Image Right Narrow (6 cols image right, content left)
 *
 * Split Templates (S3-S4):
 * - S3: Two Visuals (side by side charts/diagrams)
 * - S4: Comparison (two columns for compare/contrast)
 *
 * Blank:
 * - B1: Blank Canvas
 *
 * Legacy (kept for backward compatibility):
 * - S1: Visual + Text (replaced by V1-V4)
 * - S2: Image + Content (replaced by I1-I4)
 */

// ===========================================
// SHARED HELPER: Build Blank Split Slide
// ===========================================

/**
 * Builds a blank grid container for direct element creation.
 * Elements are added after render by DirectElementCreator.
 *
 * NEW SIMPLIFIED APPROACH:
 * - Renderer outputs blank grid container only
 * - DirectElementCreator adds elements using ElementManager
 * - No slot HTML, no slot conversion, no race conditions
 */
function buildBlankSplitSlide(templateId, content, slide, slideIndex) {
  // Use CSS variable for theming
  const backgroundStyle = window.buildBackgroundStyle(slide, content, 'var(--theme-bg, #ffffff)');

  return `
    <section data-layout="${templateId}" data-template="${templateId}"
             class="split-slide grid-container"
             data-slide-index="${slideIndex}"
             data-direct-elements="true"
             style="${backgroundStyle}">
    </section>
  `;
}

// ===========================================
// S1-VISUAL-TEXT: Visual + Text Split
// ===========================================

/**
 * S1-visual-text - Visual element on left, text content on right
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderS1VisualText(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('S1-visual-text', content, slide, slideIndex);
}

// ===========================================
// S2-IMAGE-CONTENT: Image + Content Split
// ===========================================

/**
 * S2-image-content - Full-height image on left, content on right
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderS2ImageContent(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('S2-image-content', content, slide, slideIndex);
}

// ===========================================
// V1-IMAGE-TEXT: Image + Text Insights
// ===========================================

/**
 * V1-image-text - Image on left, text insights on right
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderV1ImageText(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('V1-image-text', content, slide, slideIndex);
}

// ===========================================
// V2-CHART-TEXT: Chart + Text Insights
// ===========================================

/**
 * V2-chart-text - Chart on left, text insights on right
 */
function renderV2ChartText(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('V2-chart-text', content, slide, slideIndex);
}

// ===========================================
// V3-DIAGRAM-TEXT: Diagram + Text Insights
// ===========================================

/**
 * V3-diagram-text - Diagram on left, text insights on right
 */
function renderV3DiagramText(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('V3-diagram-text', content, slide, slideIndex);
}

// ===========================================
// V4-INFOGRAPHIC-TEXT: Infographic + Text Insights
// ===========================================

/**
 * V4-infographic-text - Infographic on left, text insights on right
 */
function renderV4InfographicText(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('V4-infographic-text', content, slide, slideIndex);
}

// ===========================================
// I1-IMAGE-LEFT: Wide Image Left
// ===========================================

/**
 * I1-image-left - Full-height wide image on left (12 cols), content on right
 */
function renderI1ImageLeft(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('I1-image-left', content, slide, slideIndex);
}

// ===========================================
// I2-IMAGE-RIGHT: Wide Image Right
// ===========================================

/**
 * I2-image-right - Full-height wide image on right (12 cols), content on left
 */
function renderI2ImageRight(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('I2-image-right', content, slide, slideIndex);
}

// ===========================================
// I3-IMAGE-LEFT-NARROW: Narrow Image Left
// ===========================================

/**
 * I3-image-left-narrow - Full-height narrow image on left (6 cols), content on right
 */
function renderI3ImageLeftNarrow(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('I3-image-left-narrow', content, slide, slideIndex);
}

// ===========================================
// I4-IMAGE-RIGHT-NARROW: Narrow Image Right
// ===========================================

/**
 * I4-image-right-narrow - Full-height narrow image on right (6 cols), content on left
 */
function renderI4ImageRightNarrow(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('I4-image-right-narrow', content, slide, slideIndex);
}

// ===========================================
// S3-TWO-VISUALS: Two Visuals Side by Side
// ===========================================

/**
 * S3-two-visuals - Two visual elements side by side with captions
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderS3TwoVisuals(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('S3-two-visuals', content, slide, slideIndex);
}

// ===========================================
// S4-COMPARISON: Comparison Layout
// ===========================================

/**
 * S4-comparison - Two columns for comparing items
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderS4Comparison(content, slide = {}, slideIndex = 0) {
  return buildBlankSplitSlide('S4-comparison', content, slide, slideIndex);
}

// ===========================================
// B1-BLANK: Blank Canvas
// ===========================================

/**
 * B1-blank - Truly blank canvas for freeform content
 * No pre-defined elements - users add elements manually via the toolbar.
 */
function renderB1Blank(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = window.buildBackgroundStyle(slide, content, '#ffffff');

  return `
    <section data-layout="B1-blank" data-template="B1-blank"
             class="blank-slide grid-container"
             data-slide-index="${slideIndex}"
             style="${backgroundStyle}">
      <!-- Truly blank - no pre-defined elements -->
    </section>
  `;
}

// ===========================================
// EXPORTS
// ===========================================

// Export for browser
if (typeof window !== 'undefined') {
  // V Series (Visual + Text)
  window.renderV1ImageText = renderV1ImageText;
  window.renderV2ChartText = renderV2ChartText;
  window.renderV3DiagramText = renderV3DiagramText;
  window.renderV4InfographicText = renderV4InfographicText;

  // I Series (Image Split)
  window.renderI1ImageLeft = renderI1ImageLeft;
  window.renderI2ImageRight = renderI2ImageRight;
  window.renderI3ImageLeftNarrow = renderI3ImageLeftNarrow;
  window.renderI4ImageRightNarrow = renderI4ImageRightNarrow;

  // S Series (Split)
  window.renderS3TwoVisuals = renderS3TwoVisuals;
  window.renderS4Comparison = renderS4Comparison;

  // B Series (Blank)
  window.renderB1Blank = renderB1Blank;

  // Legacy (kept for backward compatibility)
  window.renderS1VisualText = renderS1VisualText;
  window.renderS2ImageContent = renderS2ImageContent;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    // V Series
    renderV1ImageText,
    renderV2ChartText,
    renderV3DiagramText,
    renderV4InfographicText,
    // I Series
    renderI1ImageLeft,
    renderI2ImageRight,
    renderI3ImageLeftNarrow,
    renderI4ImageRightNarrow,
    // S Series
    renderS3TwoVisuals,
    renderS4Comparison,
    // B Series
    renderB1Blank,
    // Legacy
    renderS1VisualText,
    renderS2ImageContent
  };
}
