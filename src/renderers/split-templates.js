/**
 * Split Template Renderers for Frontend Slide Templates
 *
 * These renderers use buildSlotStyle() to apply styles from TEMPLATE_REGISTRY.
 * This ensures templates render exactly as designed in the Template Builder.
 *
 * Split Templates (S1-S4) + Blank (B1):
 * - S1: Visual + Text (chart/infographic/diagram on left, text on right)
 * - S2: Image + Content (full-height image on left, content on right)
 * - S3: Two Visuals (side by side charts/diagrams)
 * - S4: Comparison (two columns for compare/contrast)
 * - B1: Blank Canvas
 */

// ===========================================
// S1-VISUAL-TEXT: Visual + Text Split
// ===========================================

/**
 * S1-visual-text - Visual element on left, text content on right
 * Uses template-registry styles for proper split layout.
 */
function renderS1VisualText(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  return `
    <section data-layout="S1-visual-text" data-template="S1-visual-text" class="split-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'title', {
             'display': 'flex',
             'align-items': 'flex-end'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Left Content (Visual) -->
      <div class="content-left"
           ${buildSlotAttributes('visual', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'content_left', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.visual_content || content.chart_html || content.diagram_svg || content.infographic_svg || ''}
      </div>

      <!-- Right Content (Text) -->
      <div class="content-right"
           ${buildSlotAttributes('body', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'content_right', {
             'overflow-y': 'auto'
           })}">
        ${content.rich_content || content.body || content.content_right || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('S1-visual-text', 'logo', {
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
// S2-IMAGE-CONTENT: Image + Content Split
// ===========================================

/**
 * S2-image-content - Full-height image on left, content on right
 * Uses template-registry styles for proper split layout.
 */
function renderS2ImageContent(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  // Handle image content
  let imageHtml = '';
  if (content.image_url) {
    if (content.image_url.startsWith('<')) {
      imageHtml = content.image_url;
    } else {
      imageHtml = `<img src="${content.image_url}" style="width: 100%; height: 100%; object-fit: cover;" alt="${content.slide_title || 'Image'}">`;
    }
  } else if (content.image) {
    imageHtml = content.image;
  }

  return `
    <section data-layout="S2-image-content" data-template="S2-image-content" class="split-slide grid-container" style="${backgroundStyle}">
      <!-- Image (full-height left) -->
      <div class="image-area"
           ${buildSlotAttributes('image', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'image', {
             'overflow': 'hidden'
           })}">
        ${imageHtml}
      </div>

      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'title', {
             'display': 'flex',
             'align-items': 'flex-end'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Content Area -->
      <div class="content-area"
           ${buildSlotAttributes('body', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'content', {
             'overflow-y': 'auto'
           })}">
        ${content.rich_content || content.body || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('S2-image-content', 'logo', {
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
// S3-TWO-VISUALS: Two Visuals Side by Side
// ===========================================

/**
 * S3-two-visuals - Two visual elements side by side with captions
 * Uses template-registry styles for proper split layout.
 */
function renderS3TwoVisuals(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  return `
    <section data-layout="S3-two-visuals" data-template="S3-two-visuals" class="split-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'title', {
             'display': 'flex',
             'align-items': 'flex-end',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start',
             'justify-content': 'center'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Left Visual -->
      <div class="content-left"
           ${buildSlotAttributes('visual_left', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'content_left', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.visual_left || content.chart_html_1 || ''}
      </div>

      <!-- Right Visual -->
      <div class="content-right"
           ${buildSlotAttributes('visual_right', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'content_right', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.visual_right || content.chart_html_2 || ''}
      </div>

      <!-- Left Caption -->
      <div class="caption-left"
           ${buildSlotAttributes('caption_left', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'caption_left')}">
        ${content.caption_left || ''}
      </div>

      <!-- Right Caption -->
      <div class="caption-right"
           ${buildSlotAttributes('caption_right', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'caption_right')}">
        ${content.caption_right || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('S3-two-visuals', 'logo', {
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
// S4-COMPARISON: Comparison Layout
// ===========================================

/**
 * S4-comparison - Two columns for comparing items
 * Uses template-registry styles for proper comparison layout.
 */
function renderS4Comparison(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  return `
    <section data-layout="S4-comparison" data-template="S4-comparison" class="split-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'title', {
             'display': 'flex',
             'align-items': 'flex-end',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start',
             'justify-content': 'center'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Left Header -->
      <div class="header-left"
           ${buildSlotAttributes('header_left', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'header_left', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.header_left || content.left_header || ''}
      </div>

      <!-- Right Header -->
      <div class="header-right"
           ${buildSlotAttributes('header_right', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'header_right', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.header_right || content.right_header || ''}
      </div>

      <!-- Left Content -->
      <div class="content-left"
           ${buildSlotAttributes('content_left', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'content_left', {
             'overflow-y': 'auto'
           })}">
        ${content.content_left || content.left_content || ''}
      </div>

      <!-- Right Content -->
      <div class="content-right"
           ${buildSlotAttributes('content_right', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'content_right', {
             'overflow-y': 'auto'
           })}">
        ${content.content_right || content.right_content || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('S4-comparison', 'logo', {
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
// B1-BLANK: Blank Canvas
// ===========================================

/**
 * B1-blank - Empty canvas for freeform content
 * Uses template-registry styles for proper layout.
 */
function renderB1Blank(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, '');

  return `
    <section data-layout="B1-blank" data-template="B1-blank" class="blank-slide grid-container" style="${backgroundStyle}">
      <!-- Title -->
      <div class="slide-title"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('B1-blank', 'title', {
             'display': 'flex',
             'align-items': 'flex-end',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('B1-blank', 'subtitle', {
             'display': 'flex',
             'align-items': 'flex-start',
             'justify-content': 'center'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Canvas -->
      <div class="canvas"
           ${buildSlotAttributes('canvas', slideIndex)}
           style="${buildSlotStyle('B1-blank', 'canvas', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.canvas_content || content.canvas || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('B1-blank', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('B1-blank', 'logo', {
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
