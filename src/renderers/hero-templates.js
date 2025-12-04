/**
 * Hero Template Renderers for Frontend Slide Templates
 *
 * These renderers use buildSlotStyle() to apply styles from TEMPLATE_REGISTRY.
 * This ensures templates render exactly as designed in the Template Builder.
 *
 * Hero Templates:
 * - H1-generated: Full-bleed AI-generated content
 * - H1-structured: Manual title/subtitle with customizable background
 * - H2-section: Section divider slide
 * - H3-closing: Closing/thank you slide
 */

// ===========================================
// H1-GENERATED: AI-Generated Hero
// ===========================================

/**
 * H1-generated - Full-bleed hero slide (AI generates everything)
 * Used when AI generates the entire title slide design.
 */
function renderH1Generated(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H1-generated'));

  return `
    <section data-layout="H1-generated" data-template="H1-generated" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Hero Content Area (full-bleed) -->
      <div class="hero-content-area"
           ${buildSlotAttributes('hero', slideIndex)}
           style="${buildSlotStyle('H1-generated', 'hero', {
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
 * Uses template-registry styles for elegant, centered design.
 */
function renderH1Structured(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H1-structured'));

  return `
    <section data-layout="H1-structured" data-template="H1-structured" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Image Layer -->
      <div class="background-hero"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Title -->
      <div class="title-hero"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'title', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      <div class="subtitle-hero"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'subtitle', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Footer -->
      ${(content.presentation_name || content.footer_text || content.footer) ? `
      <div class="footer-hero"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'footer', {
             'display': 'flex',
             'align-items': 'center'
           })}">
        ${content.presentation_name || content.footer_text || content.footer || ''}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo-hero"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'logo', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        <div style="max-width: 100%; max-height: 100%; display: flex; align-items: center; justify-content: center; font-size: 48px;">
          ${content.company_logo}
        </div>
      </div>
      ` : ''}
    </section>
  `;
}

// ===========================================
// H2-SECTION: Section Divider
// ===========================================

/**
 * H2-section - Section divider slide
 * Features section number and title with elegant styling.
 */
function renderH2Section(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H2-section'));

  return `
    <section data-layout="H2-section" data-template="H2-section" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Layer -->
      <div class="background-hero"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H2-section', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Section Number -->
      <div class="section-number-hero"
           ${buildSlotAttributes('section_number', slideIndex)}
           style="${buildSlotStyle('H2-section', 'section_number', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.section_number || ''}
      </div>

      <!-- Title -->
      <div class="title-hero"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H2-section', 'title', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || ''}
      </div>

      <!-- Subtitle -->
      ${content.subtitle ? `
      <div class="subtitle-hero"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('H2-section', 'subtitle', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.subtitle}
      </div>
      ` : ''}
    </section>
  `;
}

// ===========================================
// H3-CLOSING: Closing/Thank You Slide
// ===========================================

/**
 * H3-closing - Closing slide with contact info
 * Elegant centered design for thank you slides.
 */
function renderH3Closing(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H3-closing'));

  return `
    <section data-layout="H3-closing" data-template="H3-closing" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Layer -->
      <div class="background-hero"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Title -->
      <div class="title-hero"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'title', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.slide_title || content.title || 'Thank You'}
      </div>

      <!-- Subtitle -->
      <div class="subtitle-hero"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'subtitle', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.subtitle || ''}
      </div>

      <!-- Contact Information -->
      ${content.contact_info ? `
      <div class="contact-hero"
           ${buildSlotAttributes('contact', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'contact_info', {
             'display': 'flex',
             'flex-direction': 'column',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        ${content.contact_info}
      </div>
      ` : ''}

      <!-- Logo -->
      ${content.company_logo ? `
      <div class="logo-hero"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'logo', {
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'
           })}">
        <div style="max-width: 100%; max-height: 100%; display: flex; align-items: center; justify-content: center; font-size: 48px;">
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
