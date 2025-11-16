/**
 * L02 - Left Diagram with Text Box on Right
 * Typography matches L25 best practices
 *
 * v7.5.1: Enhanced HTML support for element_2 and element_3
 * - Supports both HTML and plain text content
 * - Auto-detects content type and applies appropriate styling
 * - Grid dimensions: element_3 (1260×720px), element_2 (540×720px)
 */

function renderL02(content) {
  // Helper function to detect if content contains HTML
  const isHTML = (str) => str && str.includes('<');

  // Detect content types
  const element3IsHTML = isHTML(content.element_3);
  const element2IsHTML = isHTML(content.element_2);

  // Build element_3 (diagram/chart) content
  // Grid: row 5/17 (720px), column 2/23 (1260px)
  const element3Content = element3IsHTML
    ? content.element_3 || ''  // HTML: render as-is
    : `<div style="font-size: 20px; color: #374151; line-height: 1.6;">${content.element_3 || ''}</div>`;  // Plain text: wrap with styling

  // Build element_2 (observations/text) content
  // Grid: row 5/17 (720px), column 23/32 (540px) - adjusted from 24/32 to match Analytics expectations
  const element2Content = element2IsHTML
    ? content.element_2 || ''  // HTML: render as-is
    : `<div style="font-size: 20px; color: #374151; line-height: 1.6;">${content.element_2 || ''}</div>`;  // Plain text: wrap with styling

  return `
    <section data-layout="L02" class="content-slide grid-container">
      <!-- Title (42px bold, matching L25) -->
      <div class="slide-title" style="grid-row: 2/3; grid-column: 2/32; font-size: 42px; font-weight: bold; color: #1f2937; line-height: 1.2;">
        ${content.slide_title || ''}
      </div>

      <!-- Subtitle (24px, matching L25) -->
      <div class="subtitle" style="grid-row: 3/4; grid-column: 2/32; font-size: 24px; color: #6b7280; line-height: 1.4; margin-top: 8px;">
        ${content.element_1 || ''}
      </div>

      <!-- Left: Diagram/Chart Container (1260px × 720px) -->
      <div class="diagram-container" style="grid-row: 5/17; grid-column: 2/23; width: 100%; height: 100%; overflow: hidden;">
        ${element3Content}
      </div>

      <!-- Right: Observations/Text Container (540px × 720px) -->
      <div class="body-primary" style="grid-row: 5/17; grid-column: 23/32; width: 100%; height: 100%; overflow: auto;">
        ${element2Content}
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
  window.renderL02 = renderL02;
}
