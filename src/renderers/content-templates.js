/**
 * Content Template Renderers for Frontend Slide Templates
 *
 * These renderers use buildSlotStyle() to apply styles from TEMPLATE_REGISTRY.
 * This ensures templates render exactly as designed in the Template Builder.
 *
 * Content Templates (C1-C6):
 * - C1: Text Content (body paragraphs, bullets)
 * - C2: Table Slide
 * - C3: Single Chart
 * - C4: Single Infographic
 * - C5: Single Diagram
 * - C6: Single Image
 */

// ===========================================
// SHARED HELPER: Build Blank Grid Container
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
function buildBlankContentSlide(templateId, content, slide, slideIndex) {
  // Use CSS variable for theming
  const backgroundStyle = window.buildBackgroundStyle(slide, content, 'var(--theme-bg, #ffffff)');

  return `
    <section data-layout="${templateId}" data-template="${templateId}"
             class="content-slide grid-container"
             data-slide-index="${slideIndex}"
             data-direct-elements="true"
             style="${backgroundStyle}">
    </section>
  `;
}

// ===========================================
// SHARED HELPER: Build Content Slide Structure
// ===========================================

/**
 * Builds the standard content slide structure with title, subtitle, content, footer, logo
 * All C1-C6 templates share this structure, only the content slot differs.
 * Uses defaultText from TEMPLATE_REGISTRY when no content provided.
 *
 * NOTE: This is the OLD approach using slot HTML elements.
 * For NEW approach using direct element creation, use buildBlankContentSlide().
 */
function buildContentSlide(templateId, content, slide, slideIndex, contentSlotName, contentHtml) {
  const backgroundStyle = window.buildBackgroundStyle(slide, content, '');
  const template = TEMPLATE_REGISTRY[templateId];

  return `
    <section data-layout="${templateId}" data-template="${templateId}" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${window.buildSlotAttributes('title', slideIndex)}
           style="${window.buildSlotStyle(templateId, 'title')}">
        ${content.slide_title || content.title || (template?.slots?.title?.defaultText || '')}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${window.buildSlotAttributes('subtitle', slideIndex)}
           style="${window.buildSlotStyle(templateId, 'subtitle')}">
        ${content.subtitle || content.element_1 || (template?.slots?.subtitle?.defaultText || '')}
      </div>

      <!-- Main Content Area -->
      <div class="content-area"
           ${window.buildSlotAttributes(contentSlotName, slideIndex)}
           style="${window.buildSlotStyle(templateId, 'content', {
             'overflow-y': 'auto',
             'overflow-x': 'hidden'
           })}"
           data-content-width="1800px"
           data-content-height="720px">
        ${contentHtml || (template?.slots?.content?.defaultText || '')}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer || template?.slots?.footer?.defaultText) ? `
      <div class="footer"
           ${window.buildSlotAttributes('footer', slideIndex)}
           style="${window.buildSlotStyle(templateId, 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || (template?.slots?.footer?.defaultText || '')}
      </div>
      ` : ''}

      <!-- Company Logo -->
      ${(content.company_logo || template?.slots?.logo?.defaultText) ? `
      <div class="logo"
           ${window.buildSlotAttributes('logo', slideIndex)}
           style="${window.buildSlotStyle(templateId, 'logo', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        <div style="max-width: 80%; max-height: 80%; display: flex; align-items: center; justify-content: center; font-size: 36px;">
          ${content.company_logo || (template?.slots?.logo?.defaultText || '')}
        </div>
      </div>
      ` : ''}
    </section>
  `;
}

// ===========================================
// C1-TEXT: Text Content Slide
// ===========================================

/**
 * C1-text - Standard slide with body text
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements (title, subtitle, body, footer, logo) are created after render
 *   by DirectElementCreator using ElementManager
 */
function renderC1Text(content, slide = {}, slideIndex = 0) {
  return buildBlankContentSlide('C1-text', content, slide, slideIndex);
}

// ===========================================
// C2-TABLE: Table Slide
// ===========================================

/**
 * C2-table - Slide with data table
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderC2Table(content, slide = {}, slideIndex = 0) {
  return buildBlankContentSlide('C2-table', content, slide, slideIndex);
}

// ===========================================
// C3-CHART: Single Chart Slide
// ===========================================

/**
 * C3-chart - Slide with one chart visualization
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderC3Chart(content, slide = {}, slideIndex = 0) {
  return buildBlankContentSlide('C3-chart', content, slide, slideIndex);
}

// ===========================================
// C4-INFOGRAPHIC: Single Infographic Slide
// ===========================================

/**
 * C4-infographic - Slide with one infographic
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderC4Infographic(content, slide = {}, slideIndex = 0) {
  return buildBlankContentSlide('C4-infographic', content, slide, slideIndex);
}

// ===========================================
// C5-DIAGRAM: Single Diagram Slide
// ===========================================

/**
 * C5-diagram - Slide with one diagram
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements created by DirectElementCreator
 */
function renderC5Diagram(content, slide = {}, slideIndex = 0) {
  return buildBlankContentSlide('C5-diagram', content, slide, slideIndex);
}

// ===========================================
// C6-IMAGE: Single Image Slide
// ===========================================

/**
 * C6-image - Slide with one image and optional caption
 *
 * NEW SIMPLIFIED APPROACH:
 * - Outputs blank grid container only
 * - Elements (title, subtitle, image, footer, logo) are created after render
 *   by DirectElementCreator using ElementManager
 * - No slot HTML, no slot conversion, no race conditions
 */
function renderC6Image(content, slide = {}, slideIndex = 0) {
  // Just return blank container - elements added by DirectElementCreator
  return buildBlankContentSlide('C6-image', content, slide, slideIndex);
}

// ===========================================
// EXPORTS
// ===========================================

// Export for browser
if (typeof window !== 'undefined') {
  window.renderC1Text = renderC1Text;
  window.renderC2Table = renderC2Table;
  window.renderC3Chart = renderC3Chart;
  window.renderC4Infographic = renderC4Infographic;
  window.renderC5Diagram = renderC5Diagram;
  window.renderC6Image = renderC6Image;
  window.buildContentSlide = buildContentSlide;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    renderC1Text,
    renderC2Table,
    renderC3Chart,
    renderC4Infographic,
    renderC5Diagram,
    renderC6Image,
    buildContentSlide
  };
}
