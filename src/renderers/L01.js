/**
 * L01 - Centered Chart or Diagram with 2-line text below
 * Typography matches L25 best practices
 */

function renderL01(content) {
  return `
    <section data-layout="L01" class="content-slide grid-container">
      <!-- Title (42px bold, matching L25) -->
      <div class="slide-title" style="grid-row: 2/3; grid-column: 2/32; font-size: 42px; font-weight: bold; color: #1f2937; line-height: 1.2;">
        ${content.slide_title || ''}
      </div>

      <!-- Subtitle (24px, matching L25) -->
      <div class="subtitle" style="grid-row: 3/4; grid-column: 2/32; font-size: 24px; color: #6b7280; line-height: 1.4; margin-top: 8px;">
        ${content.element_1 || ''}
      </div>

      <!-- Chart/Diagram Container -->
      <div class="chart-container" style="grid-row: 5/15; grid-column: 2/32; overflow: visible; display: block; height: 100%;">
        ${content.element_4 || ''}
      </div>

      <!-- Body Text Below Chart -->
      <div class="body-primary" style="grid-row: 15/17; grid-column: 2/32; font-size: 20px; color: #374151; line-height: 1.6;">
        ${content.element_3 || ''}
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
  window.renderL01 = renderL01;
}
