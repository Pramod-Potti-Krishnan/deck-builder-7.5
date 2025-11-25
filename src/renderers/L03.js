/**
 * L03 - Two Charts in Columns with Text Below
 * Typography matches L25 best practices
 */

function renderL03(content, slide = {}, slideIndex = 0) {
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
    <section data-layout="L03" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Title (42px bold, matching L25) -->
      <div class="slide-title"
           data-section-id="slide-${slideIndex}-section-title"
           data-section-type="title"
           data-slide-index="${slideIndex}"
           style="grid-row: 2/3; grid-column: 2/32; font-size: 42px; font-weight: bold; color: #1f2937; line-height: 1.2;">
        ${content.slide_title || ''}
      </div>

      <!-- Subtitle (24px, matching L25) -->
      <div class="subtitle"
           data-section-id="slide-${slideIndex}-section-subtitle"
           data-section-type="subtitle"
           data-slide-index="${slideIndex}"
           style="grid-row: 3/4; grid-column: 2/32; font-size: 24px; color: #6b7280; line-height: 1.4; margin-top: 8px;">
        ${content.element_1 || ''}
      </div>

      <!-- Left Chart -->
      <div class="chart-container"
           data-section-id="slide-${slideIndex}-section-chart1"
           data-section-type="chart1"
           data-slide-index="${slideIndex}"
           style="grid-row: 5/14; grid-column: 2/16;">
        ${content.element_4 || ''}
      </div>

      <!-- Right Chart -->
      <div class="chart-container"
           data-section-id="slide-${slideIndex}-section-chart2"
           data-section-type="chart2"
           data-slide-index="${slideIndex}"
           style="grid-row: 5/14; grid-column: 17/31;">
        ${content.element_2 || ''}
      </div>

      <!-- Left Body Text Below Chart -->
      <div class="body-primary"
           data-section-id="slide-${slideIndex}-section-body-left"
           data-section-type="body-left"
           data-slide-index="${slideIndex}"
           style="grid-row: 14/17; grid-column: 2/16; font-size: 20px; color: #374151; line-height: 1.6;">
        ${content.element_3 || ''}
      </div>

      <!-- Right Body Text Below Chart -->
      <div class="body-primary"
           data-section-id="slide-${slideIndex}-section-body-right"
           data-section-type="body-right"
           data-slide-index="${slideIndex}"
           style="grid-row: 14/17; grid-column: 17/31; font-size: 20px; color: #374151; line-height: 1.6;">
        ${content.element_5 || ''}
      </div>

      <!-- Footer: Presentation Name (18px, matching L25) -->
      ${content.presentation_name ? `
      <div class="footer-presentation-name" style="grid-row: 18/19; grid-column: 2/7; padding: 8px 14px; font-size: 18px; color: #1f2937; font-weight: 500; display: flex; align-items: center; height: 100%;">
        ${content.presentation_name}
      </div>
      ` : ''}

      <!-- Footer: Company Logo (bottom-right, matching L27) -->
      ${content.company_logo ? `
      <div class="footer-company-logo" style="grid-row: 17/19; grid-column: 30/32; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <div style="max-width: 50%; max-height: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px;">
          ${content.company_logo}
        </div>
      </div>
      ` : ''}
    </section>
  `;
}

// Export for v7.5
if (typeof window !== 'undefined') {
  window.renderL03 = renderL03;
}
