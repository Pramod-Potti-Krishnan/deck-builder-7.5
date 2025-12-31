/**
 * L27 - Image Left with Content Right
 * Typography matches L25 best practices
 */

function renderL27(content, slide = {}, slideIndex = 0) {
  // Extract background settings from slide object
  const backgroundColor = slide?.background_color || '';
  const backgroundImage = slide?.background_image || '';

  // Build background style
  let backgroundStyle = '';
  if (backgroundImage) {
    backgroundStyle = `background-image: url('${backgroundImage}'); background-size: cover; background-position: center; background-repeat: no-repeat;`;
    if (backgroundColor) {
      backgroundStyle += ` background-color: ${backgroundColor};`; // Fallback color
    }
  } else if (backgroundColor) {
    backgroundStyle = `background-color: ${backgroundColor};`;
  }

  return `
    <section data-layout="L27" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Left: Full-height Image (columns 1-12) -->
      <div class="image-container"
           data-section-id="slide-${slideIndex}-section-image"
           data-section-type="image"
           data-slot-name="image"
           data-slide-index="${slideIndex}"
           style="grid-row: 1/19; grid-column: 1/12;">
        ${content.image_url || ''}
      </div>

      <!-- Right: Title (42px bold, matching L25) -->
      <div class="slide-title"
           data-section-id="slide-${slideIndex}-section-title"
           data-section-type="title"
           data-slot-name="title"
           data-slide-index="${slideIndex}"
           style="grid-row: 2/3; grid-column: 13/32; font-size: 42px; font-weight: bold; color: #1f2937; line-height: 1.2;">
        ${content.slide_title || ''}
      </div>

      <!-- Right: Subtitle (24px, matching L25) -->
      <div class="subtitle"
           data-section-id="slide-${slideIndex}-section-subtitle"
           data-section-type="subtitle"
           data-slot-name="subtitle"
           data-slide-index="${slideIndex}"
           style="grid-row: 3/4; grid-column: 13/32; font-size: 24px; color: #6b7280; line-height: 1.4; margin-top: 8px;">
        ${content.element_1 || ''}
      </div>

      <!-- Right: Main Content Body -->
      <div class="text-content"
           data-section-id="slide-${slideIndex}-section-text"
           data-section-type="text"
           data-slot-name="text"
           data-slide-index="${slideIndex}"
           style="grid-row: 5/17; grid-column: 13/32; font-size: 20px; color: #374151; line-height: 1.6; overflow-y: auto;">
        ${content.main_content || ''}
      </div>

      <!-- Footer: Presentation Name (18px, matching L25) -->
      ${content.presentation_name ? `
      <div class="footer-presentation-name" data-slot-name="footer" style="grid-row: 18/19; grid-column: 12/30; padding: 8px 14px; font-size: 18px; color: #1f2937; font-weight: 500; display: flex; align-items: center; height: 100%;">
        ${content.presentation_name}
      </div>
      ` : ''}

      <!-- Logo (top-right corner, 2×2 grid) -->
      ${(content.logo || content.company_logo) ? `
      <div class="logo-container" data-slot-name="logo" style="grid-row: 1/3; grid-column: 31/33; display: flex; align-items: center; justify-content: center; padding: 4px;">
        <div style="max-width: 100%; max-height: 100%; display: flex; align-items: center; justify-content: center;">
          ${content.logo || content.company_logo}
        </div>
      </div>
      ` : ''}
    </section>
  `;
}

// Export for v7.5
if (typeof window !== 'undefined') {
  window.renderL27 = renderL27;
}
