/**
 * L29: Hero Full-Bleed Layout
 *
 * Structure:
 * - Rows 1-18, Columns 1-32: Full slide (hero_content)
 * - No title, no subtitle, no footer
 * - Text Service has complete control
 *
 * Content Area Dimensions:
 * - Grid: 18 rows × 32 columns (entire slide)
 * - Pixels: 1920px × 1080px (full HD)
 *
 * Format Ownership:
 * - hero_content: text_service (complete HTML with full styling)
 *
 * Use Cases:
 * - Opening hero images with overlaid text
 * - Full-screen calls to action
 * - Immersive brand experiences
 * - Video backgrounds with text overlays
 */

function renderL29(content) {
  // Use FormatOwnership utility if available, otherwise render as-is
  const heroHTML = window.FormatOwnership
    ? window.FormatOwnership.renderWithOwnership(content.hero_content, content, 'hero_content')
    : content.hero_content;

  return `
    <section data-layout="L29" class="hero-slide grid-container">
      <!-- Hero Content Area (full-bleed) -->
      <!-- Full Slide: 1920px × 1080px -->
      <!-- Text Service has complete creative control -->
      <div class="hero-content-area"
           style="grid-row: 1/19; grid-column: 1/33;
                  display: flex;
                  flex-direction: column;
                  justify-content: center;
                  align-items: center;
                  text-align: center;
                  width: 100%; height: 100%;"
           data-format-owner="text_service"
           data-content-width="1920px"
           data-content-height="1080px">
        ${heroHTML}
      </div>
    </section>
  `;
}

// Export for browser
if (typeof window !== 'undefined') {
  window.renderL29 = renderL29;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = renderL29;
}
