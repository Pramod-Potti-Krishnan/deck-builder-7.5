/**
 * Hero Template Renderers for Frontend Slide Templates
 *
 * These renderers use the NEW Direct Element Creation approach:
 * - Render blank grid container only
 * - Elements are created after render by DirectElementCreator using ElementManager
 * - All styles come from TEMPLATE_REGISTRY
 *
 * Hero Templates:
 * - H1-generated: Full-bleed AI-generated content (LEGACY - not using direct elements)
 * - H1-structured: Manual title/subtitle with customizable background
 * - H2-section: Section divider slide
 * - H3-closing: Closing/thank you slide
 */

// ===========================================
// SHARED HELPER: Build Blank Hero Slide
// ===========================================

/**
 * Builds a blank grid container for direct element creation.
 * Elements are added after render by DirectElementCreator.
 *
 * Hero slides use dark backgrounds by default.
 */
function buildBlankHeroSlide(templateId, content, slide, slideIndex) {
  // Hero slides default to dark background
  const defaultBg = templateId === 'H2-section' ? '#374151' : '#1e3a5f';
  const backgroundStyle = window.buildBackgroundStyle(slide, content, defaultBg);

  return `
    <section data-layout="${templateId}" data-template="${templateId}"
             class="hero-slide grid-container"
             data-slide-index="${slideIndex}"
             data-direct-elements="true"
             style="${backgroundStyle}">
    </section>
  `;
}

// ===========================================
// H1-GENERATED: AI-Generated Hero
// ===========================================

/**
 * H1-generated - Full-bleed hero slide (AI generates everything)
 * Used when AI generates the entire title slide design.
 * NOTE: This template uses LEGACY approach (not direct element creation)
 * because AI generates the complete hero_content HTML.
 */
function renderH1Generated(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = window.buildBackgroundStyle(slide, content, window.getTemplateDefaultBackground('H1-generated'));

  return `
    <section data-layout="H1-generated" data-template="H1-generated" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Hero Content Area (full-bleed) -->
      <div class="hero-content-area"
           ${window.buildSlotAttributes('hero', slideIndex)}
           style="${window.buildSlotStyle('H1-generated', 'hero', {
             'overflow': 'hidden',
             'width': '100%',
             'height': '100%'
           })}"
           data-content-width="1920px"
           data-content-height="1080px">
        ${content.hero_content || ''}
      </div>
    </section>
  `;
}

// ===========================================
// H1-STRUCTURED: Manual Title Slide
// ===========================================

/**
 * H1-structured - Manual title slide with editable elements
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements (background, title, subtitle, footer, logo) are created after render
 *   by DirectElementCreator using ElementManager
 */
function renderH1Structured(content, slide = {}, slideIndex = 0) {
  return buildBlankHeroSlide('H1-structured', content, slide, slideIndex);
}

// ===========================================
// H2-SECTION: Section Divider
// ===========================================

/**
 * H2-section - Section divider slide
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements (background, section_number, title) are created after render
 *   by DirectElementCreator using ElementManager
 * - NOTE: This template has NO subtitle slot
 */
function renderH2Section(content, slide = {}, slideIndex = 0) {
  return buildBlankHeroSlide('H2-section', content, slide, slideIndex);
}

// ===========================================
// H3-CLOSING: Closing/Thank You Slide
// ===========================================

/**
 * H3-closing - Closing slide with contact info
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements (background, title, subtitle, contact_info, logo) are created after render
 *   by DirectElementCreator using ElementManager
 */
function renderH3Closing(content, slide = {}, slideIndex = 0) {
  return buildBlankHeroSlide('H3-closing', content, slide, slideIndex);
}

// ===========================================
// EXPORTS
// ===========================================

// Export for browser
if (typeof window !== 'undefined') {
  window.renderH1Generated = renderH1Generated;
  window.renderH1Structured = renderH1Structured;
  window.renderH2Section = renderH2Section;
  window.renderH3Closing = renderH3Closing;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    renderH1Generated,
    renderH1Structured,
    renderH2Section,
    renderH3Closing
  };
}
