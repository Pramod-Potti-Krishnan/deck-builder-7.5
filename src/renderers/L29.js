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

function renderL29(content, slide = {}, slideIndex = 0) {
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

  // Use FormatOwnership utility if available, otherwise render as-is
  const heroHTML = window.FormatOwnership
    ? window.FormatOwnership.renderWithOwnership(content.hero_content, content, 'hero_content')
    : content.hero_content;

  return `
    <section data-layout="L29" class="hero-slide grid-container" style="${backgroundStyle}">
      <!-- Hero Content Area (full-bleed) -->
      <!-- Full Slide: 1920px × 1080px -->
      <!-- Text Service has complete creative control -->
      <div class="hero-content-area"
           data-section-id="slide-${slideIndex}-section-hero"
           data-section-type="hero"
           data-slot-name="hero"
           data-slide-index="${slideIndex}"
           style="grid-row: 1/19; grid-column: 1/33; overflow: hidden; width: 100%; height: 100%;"
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
