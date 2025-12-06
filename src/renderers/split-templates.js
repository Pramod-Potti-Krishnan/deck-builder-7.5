/**
 * Split Template Renderers for Frontend Slide Templates
 *
 * These renderers use the NEW Direct Element Creation approach:
 * - Render blank grid container only
 * - Elements are created after render by DirectElementCreator using ElementManager
 * - All styles come from TEMPLATE_REGISTRY
 *
 * Split Templates (S1-S4) + Blank (B1):
 * - S1: Visual + Text (chart/infographic/diagram on left, text on right)
 * - S2: Image + Content (full-height image on left, content on right)
 * - S3: Two Visuals (side by side charts/diagrams)
 * - S4: Comparison (two columns for compare/contrast)
 * - B1: Blank Canvas
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
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

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
  const backgroundStyle = buildBackgroundStyle(slide, content, '#ffffff');

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
  window.renderS1VisualText = renderS1VisualText;
  window.renderS2ImageContent = renderS2ImageContent;
  window.renderS3TwoVisuals = renderS3TwoVisuals;
  window.renderS4Comparison = renderS4Comparison;
  window.renderB1Blank = renderB1Blank;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    renderS1VisualText,
    renderS2ImageContent,
    renderS3TwoVisuals,
    renderS4Comparison,
    renderB1Blank
  };
}
