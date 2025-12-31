/**
 * L25: Main Content Shell
 *
 * Structure:
 * - Row 2: slide_title (layout_builder formats)
 * - Row 3: subtitle (layout_builder formats)
 * - Rows 5-16: rich_content (text_service owns - full creative control)
 * - Row 18: footer
 *
 * Content Area Dimensions:
 * - Grid: 12 rows × 30 columns
 * - Pixels: ~1800px × ~720px (at 1920×1080 resolution)
 *
 * Format Ownership:
 * - slide_title, subtitle: layout_builder (plain text → HTML)
 * - rich_content: text_service (receives HTML, renders as-is)
 */

function renderL25(content, slide = {}, slideIndex = 0) {
  // Extract background settings from slide object
  // v7.5.4: Use theme background as default
  const backgroundColor = slide?.background_color || 'var(--theme-bg, #ffffff)';
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

  // Use FormatOwnership utility if available, otherwise render as-is
  const richContentHTML = window.FormatOwnership
    ? window.FormatOwnership.renderWithOwnership(content.rich_content, content, 'rich_content')
    : content.rich_content;

  return `
    <section data-layout="L25" class="content-slide grid-container" style="${backgroundStyle}">
      <!-- Title (layout_builder formats) - v7.5.4: Uses theme CSS variables -->
      <div class="slide-title"
           data-section-id="slide-${slideIndex}-section-title"
           data-section-type="title"
           data-slot-name="title"
           data-slide-index="${slideIndex}"
           style="grid-row: 2/3; grid-column: 2/32; font-size: var(--theme-title-size, 42px); font-weight: var(--theme-title-weight, bold); font-family: var(--theme-font-family, Poppins, sans-serif); color: var(--theme-text-primary, #1f2937); line-height: var(--theme-title-line-height, 1.2);">
        ${content.slide_title}
      </div>

      <!-- Subtitle (layout_builder formats) - v7.5.4: Uses theme CSS variables -->
      ${(content.subtitle || content.element_1) ? `
      <div class="subtitle"
           data-section-id="slide-${slideIndex}-section-subtitle"
           data-section-type="subtitle"
           data-slot-name="subtitle"
           data-slide-index="${slideIndex}"
           style="grid-row: 3/4; grid-column: 2/32; font-size: var(--theme-subtitle-size, 24px); font-family: var(--theme-font-family, Poppins, sans-serif); color: var(--theme-text-secondary, #6b7280); line-height: var(--theme-subtitle-line-height, 1.4); margin-top: 8px;">
        ${content.subtitle || content.element_1}
      </div>
      ` : ''}

      <!-- Rich Content Area (text_service owns) -->
      <!-- Content Area: 1800px wide × 720px tall -->
      <!-- Text Service has full creative control -->
      <div class="rich-content-area"
           data-section-id="slide-${slideIndex}-section-content"
           data-section-type="content"
           data-slot-name="content"
           data-slide-index="${slideIndex}"
           style="grid-row: 5/17; grid-column: 2/32; overflow-y: auto; overflow-x: hidden;"
           data-format-owner="text_service"
           data-content-width="1800px"
           data-content-height="720px">
        ${richContentHTML}
      </div>

      <!-- Footer with 3 sections -->
      <div class="footer-container" style="grid-row: 18/19; grid-column: 1/33; display: grid; grid-template-columns: repeat(32, 1fr); align-items: center;">
        <!-- Left Section: Presentation Name (columns 2-20, 18 grids) - v7.5.4: Uses theme CSS variables -->
        ${content.presentation_name ? `
        <div class="footer-presentation-name" data-slot-name="footer" style="grid-column: 2/20; padding: 8px 14px; font-size: var(--theme-footer-size, 18px); font-family: var(--theme-font-family, Poppins, sans-serif); color: var(--theme-text-primary, #1f2937); font-weight: var(--theme-footer-weight, 500); display: flex; align-items: center; height: 100%;">
          ${content.presentation_name}
        </div>
        ` : ''}

        <!-- Middle Section: Empty (columns 20-31) -->
      </div>

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

// Export for browser
if (typeof window !== 'undefined') {
  window.renderL25 = renderL25;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = renderL25;
}
