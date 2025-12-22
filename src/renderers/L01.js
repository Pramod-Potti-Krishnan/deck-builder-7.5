/**
 * L01 - Centered Chart or Diagram with 2-line text below
 * Typography matches L25 best practices
 */

function renderL01(content, slide = {}, slideIndex = 0) {
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
    <section data-layout="L01" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Title (42px bold, matching L25) -->
      <div class="slide-title"
           data-section-id="slide-${slideIndex}-section-title"
           data-section-type="title"
           data-slot-name="title"
           data-slide-index="${slideIndex}"
           style="grid-row: 2/3; grid-column: 2/32; font-size: 42px; font-weight: bold; color: #1f2937; line-height: 1.2;">
        ${content.slide_title || ''}
      </div>

      <!-- Subtitle (24px, matching L25) -->
      <div class="subtitle"
           data-section-id="slide-${slideIndex}-section-subtitle"
           data-section-type="subtitle"
           data-slot-name="subtitle"
           data-slide-index="${slideIndex}"
           style="grid-row: 3/4; grid-column: 2/32; font-size: 24px; color: #6b7280; line-height: 1.4; margin-top: 8px;">
        ${content.element_1 || ''}
      </div>

      <!-- Chart/Diagram Container -->
      <div class="chart-container"
           data-section-id="slide-${slideIndex}-section-chart"
           data-section-type="chart"
           data-slot-name="chart"
           data-slide-index="${slideIndex}"
           data-format-owner="analytics_service"
           style="grid-row: 5/15; grid-column: 2/32;">
        ${content.element_4 || ''}
      </div>

      <!-- Body Text Below Chart -->
      <div class="body-primary"
           data-section-id="slide-${slideIndex}-section-body"
           data-section-type="body"
           data-slot-name="body"
           data-slide-index="${slideIndex}"
           style="grid-row: 15/17; grid-column: 2/32; font-size: 20px; color: #374151; line-height: 1.6;">
        ${content.element_3 || ''}
      </div>

      <!-- Footer: Presentation Name (18px, matching L25) -->
      ${content.presentation_name ? `
      <div class="footer-presentation-name" data-slot-name="footer" style="grid-row: 18/19; grid-column: 2/20; padding: 8px 14px; font-size: 18px; color: #1f2937; font-weight: 500; display: flex; align-items: center; height: 100%;">
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
  window.renderL01 = renderL01;
}
