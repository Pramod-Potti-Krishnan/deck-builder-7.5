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
// SHARED HELPER: Build Content Slide Structure
// ===========================================

/**
 * Builds the standard content slide structure with title, subtitle, content, footer, logo
 * All C1-C6 templates share this structure, only the content slot differs.
 */
function buildContentSlide(templateId, content, slide, slideIndex, contentSlotName, contentHtml) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  return `
    <section data-layout="${templateId}" data-template="${templateId}" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle(templateId, 'title', {
             'display': 'flex',
             'align-items': 'flex-end'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle(templateId, 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start'
           })}">
        ${content.subtitle || content.element_1 || ''}
      </div>

      <!-- Main Content Area -->
      <div class="content-area"
           ${buildSlotAttributes(contentSlotName, slideIndex)}
           style="${buildSlotStyle(templateId, 'content', {
             'overflow-y': 'auto',
             'overflow-x': 'hidden'
           })}"
           data-content-width="1800px"
           data-content-height="720px">
        ${contentHtml}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle(templateId, 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Company Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle(templateId, 'logo', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        <div style="max-width: 80%; max-height: 80%; display: flex; align-items: center; justify-content: center; font-size: 36px;">
          ${content.company_logo}
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
 * Uses template-registry styles for elegant typography.
 */
function renderC1Text(content, slide = {}, slideIndex = 0) {
  const contentHtml = content.rich_content || content.body || '';
  return buildContentSlide('C1-text', content, slide, slideIndex, 'body', contentHtml);
}

// ===========================================
// C2-TABLE: Table Slide
// ===========================================

/**
 * C2-table - Slide with data table
 * Uses template-registry styles for proper table presentation.
 */
function renderC2Table(content, slide = {}, slideIndex = 0) {
  const contentHtml = content.table_html || content.table || '';
  return buildContentSlide('C2-table', content, slide, slideIndex, 'table', contentHtml);
}

// ===========================================
// C3-CHART: Single Chart Slide
// ===========================================

/**
 * C3-chart - Slide with one chart visualization
 * Uses template-registry styles for chart container.
 */
function renderC3Chart(content, slide = {}, slideIndex = 0) {
  const contentHtml = content.chart_html || content.chart || '';
  return buildContentSlide('C3-chart', content, slide, slideIndex, 'chart', contentHtml);
}

// ===========================================
// C4-INFOGRAPHIC: Single Infographic Slide
// ===========================================

/**
 * C4-infographic - Slide with one infographic
 * Uses template-registry styles for infographic container.
 */
function renderC4Infographic(content, slide = {}, slideIndex = 0) {
  const contentHtml = content.infographic_svg || content.infographic || '';
  return buildContentSlide('C4-infographic', content, slide, slideIndex, 'infographic', contentHtml);
}

// ===========================================
// C5-DIAGRAM: Single Diagram Slide
// ===========================================

/**
 * C5-diagram - Slide with one diagram
 * Uses template-registry styles for diagram container.
 */
function renderC5Diagram(content, slide = {}, slideIndex = 0) {
  const contentHtml = content.diagram_svg || content.diagram || '';
  return buildContentSlide('C5-diagram', content, slide, slideIndex, 'diagram', contentHtml);
}

// ===========================================
// C6-IMAGE: Single Image Slide
// ===========================================

/**
 * C6-image - Slide with one image and optional caption
 * Uses template-registry styles for image container.
 */
function renderC6Image(content, slide = {}, slideIndex = 0) {
  let contentHtml = '';
  if (content.image_url) {
    if (content.image_url.startsWith('<')) {
      // Already HTML
      contentHtml = content.image_url;
    } else {
      // URL - wrap in img tag
      contentHtml = `<img src="${content.image_url}" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="${content.slide_title || 'Image'}">`;
    }
  } else if (content.image) {
    contentHtml = content.image;
  }
  return buildContentSlide('C6-image', content, slide, slideIndex, 'image', contentHtml);
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
