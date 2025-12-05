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
 * Uses template-registry styles for LEFT-aligned, LEFT HALF design.
 *
 * Slot elements have:
 * - Unique IDs for targeting by slot-converter.js
 * - slot-convertible class for conversion tracking
 * - data-element-target for specifying target Element Type
 */
function renderH1Structured(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H1-structured'));
  const template = TEMPLATE_REGISTRY['H1-structured'];

  return `
    <section data-layout="H1-structured" data-template="H1-structured" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Image Layer -->
      <div class="background-hero slot-convertible"
           id="slide-${slideIndex}-slot-background"
           data-element-target="image"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Title (LEFT-aligned, BOTTOM-aligned, LEFT HALF) -->
      <div class="title-hero slot-convertible"
           id="slide-${slideIndex}-slot-title"
           data-element-target="textbox"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'title')}">
        ${content.slide_title || content.title || template.slots.title.defaultText || ''}
      </div>

      <!-- Subtitle (LEFT-aligned, LEFT HALF) -->
      <div class="subtitle-hero slot-convertible"
           id="slide-${slideIndex}-slot-subtitle"
           data-element-target="textbox"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'subtitle')}">
        ${content.subtitle || template.slots.subtitle.defaultText || ''}
      </div>

      <!-- Footer (LEFT, UPPERCASE, BOLD) -->
      <div class="footer-hero slot-convertible"
           id="slide-${slideIndex}-slot-footer"
           data-element-target="textbox"
           ${buildSlotAttributes('footer', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'footer')}">
        ${content.presentation_name || content.footer_text || content.footer || template.slots.footer.defaultText || ''}
      </div>

      <!-- Logo (BOTTOM RIGHT) -->
      <div class="logo-hero slot-convertible"
           id="slide-${slideIndex}-slot-logo"
           data-element-target="image"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('H1-structured', 'logo')}">
        ${content.company_logo || template.slots.logo.defaultText || ''}
      </div>
    </section>
  `;
}

// ===========================================
// H2-SECTION: Section Divider
// ===========================================

/**
 * H2-section - Section divider slide
 * Features section number and title with elegant styling.
 * Uses template-registry styles - NO subtitle slot in this template.
 */
function renderH2Section(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H2-section'));
  const template = TEMPLATE_REGISTRY['H2-section'];

  return `
    <section data-layout="H2-section" data-template="H2-section" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Layer -->
      <div class="background-hero"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H2-section', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Section Number (centered, large) -->
      <div class="section-number-hero"
           ${buildSlotAttributes('section_number', slideIndex)}
           style="${buildSlotStyle('H2-section', 'section_number')}">
        ${content.section_number || template.slots.section_number.defaultText || ''}
      </div>

      <!-- Title (centered below section number) -->
      <div class="title-hero"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H2-section', 'title')}">
        ${content.slide_title || content.title || template.slots.title.defaultText || ''}
      </div>
    </section>
  `;
}

// ===========================================
// H3-CLOSING: Closing/Thank You Slide
// ===========================================

/**
 * H3-closing - Closing slide with contact info
 * Elegant centered design for thank you slides.
 * Uses template-registry styles for all slots.
 */
function renderH3Closing(content, slide = {}, slideIndex = 0) {
  const backgroundStyle = buildBackgroundStyle(slide, content, getTemplateDefaultBackground('H3-closing'));
  const template = TEMPLATE_REGISTRY['H3-closing'];

  return `
    <section data-layout="H3-closing" data-template="H3-closing" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Background Layer -->
      <div class="background-hero"
           ${buildSlotAttributes('background', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'background')}">
        ${content.background_image ? `<img src="${content.background_image}" style="width: 100%; height: 100%; object-fit: cover;">` : ''}
      </div>

      <!-- Title (centered) -->
      <div class="title-hero"
           ${buildSlotAttributes('title', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'title')}">
        ${content.slide_title || content.title || template.slots.title.defaultText || ''}
      </div>

      <!-- Subtitle (centered below title) -->
      <div class="subtitle-hero"
           ${buildSlotAttributes('subtitle', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'subtitle')}">
        ${content.subtitle || template.slots.subtitle.defaultText || ''}
      </div>

      <!-- Contact Information -->
      <div class="contact-hero"
           ${buildSlotAttributes('contact_info', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'contact_info')}">
        ${content.contact_info || template.slots.contact_info.defaultText || ''}
      </div>

      <!-- Logo (bottom right) -->
      <div class="logo-hero"
           ${buildSlotAttributes('logo', slideIndex)}
           style="${buildSlotStyle('H3-closing', 'logo')}">
        ${content.company_logo || template.slots.logo.defaultText || ''}
      </div>
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
