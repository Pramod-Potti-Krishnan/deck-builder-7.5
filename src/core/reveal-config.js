/**
 * RevealJS Configuration
 *
 * Uses fixed 1920×1080px base for consistent grid layout rendering.
 * Required for L02 and other layouts with fixed pixel dimensions.
 *
 * Critical Settings:
 * - width/height: 1920×1080 (fixed base dimensions)
 * - margin: 0 (no margins)
 * - minScale: 0.1 (allow downscaling to fit smaller viewports)
 * - maxScale: 1.0 (prevent upscaling beyond 1920×1080)
 * - center: true (center presentation in viewport)
 *
 * v7.5.1: Changed from percentage-based to fixed dimensions
 * Reason: Grid system assumes 1920×1080 base for element sizing
 * Allows downscaling so content fits in viewports smaller than 1920×1080
 */

// ===== HELPER FUNCTIONS (must be defined before RevealConfig) =====

/**
 * Toggle grid overlay
 */
function toggleGridOverlay() {
  let overlay = document.getElementById('grid-overlay');

  if (overlay) {
    // Remove existing overlay
    overlay.remove();
    console.log('Grid overlay: OFF');
  } else {
    // Create overlay
    overlay = document.createElement('div');
    overlay.id = 'grid-overlay';
    overlay.className = 'grid-overlay';
    document.body.appendChild(overlay);
    console.log('Grid overlay: ON');
  }
}

/**
 * Toggle border highlighting
 */
function toggleBorderHighlight() {
  document.body.classList.toggle('show-borders');
  const isHighlighted = document.body.classList.contains('show-borders');
  console.log(`Border highlight: ${isHighlighted ? 'ON' : 'OFF'}`);
}

/**
 * Toggle controls panel
 */
function toggleControlsPanel() {
  const panel = document.getElementById('controls-panel');
  if (panel) {
    panel.classList.toggle('visible');
    const isVisible = panel.classList.contains('visible');
    console.log(`Controls panel: ${isVisible ? 'VISIBLE' : 'HIDDEN'}`);
  }
}

/**
 * Toggle help text overlay
 */
function toggleHelpText() {
  const helpText = document.getElementById('help-text');
  if (helpText) {
    helpText.classList.toggle('show');
    const isVisible = helpText.classList.contains('show');
    console.log(`Help text: ${isVisible ? 'VISIBLE' : 'HIDDEN'}`);
  }
}

// ===== REVEAL.JS CONFIGURATION =====

const RevealConfig = {
  // ===== Viewport Settings (CRITICAL) =====
  // Use fixed 1920×1080px base for grid system compatibility
  // Grid layouts (L02, etc.) depend on these exact dimensions
  width: 1920,
  height: 1080,
  margin: 0,

  // Allow downscaling to fit smaller viewports, prevent upscaling
  // v7.5.1: minScale allows fitting in smaller screens, maxScale prevents enlargement
  minScale: 0.1,
  maxScale: 1.0,

  // Center presentation in viewport
  center: true,

  // ===== Layout Control =====
  // Let RevealJS handle layout scaling
  // disableLayout removed to allow proper scaling

  // ===== Navigation =====
  controls: true,
  controlsLayout: 'bottom-right',
  controlsBackArrows: 'faded',
  progress: true,
  slideNumber: 'c/t', // Current/Total

  // ===== Keyboard Shortcuts =====
  keyboard: {
    // Standard navigation
    37: 'prev', // Left arrow
    39: 'next', // Right arrow
    38: 'prev', // Up arrow
    40: 'next', // Down arrow

    // Custom shortcuts (functions defined above)
    71: () => { toggleGridOverlay(); },  // 'G' - Toggle grid overlay
    66: () => { toggleBorderHighlight(); }, // 'B' - Toggle border highlight
    67: () => { toggleControlsPanel(); },   // 'C' - Toggle controls panel
    72: () => { toggleHelpText(); },        // 'H' - Toggle help text
  },

  // ===== Behavior =====
  loop: false,
  rtl: false,
  navigationMode: 'default',
  shuffle: false,

  // ===== Fragments =====
  fragments: true,
  fragmentInURL: true,

  // ===== Overview Mode =====
  overview: true,

  // ===== Help Overlay =====
  help: true,

  // ===== Presentation Mode =====
  showNotes: false,

  // ===== Auto-slide (disabled) =====
  autoSlide: 0,

  // ===== Transitions =====
  transition: 'slide', // none/fade/slide/convex/concave/zoom
  transitionSpeed: 'default', // default/fast/slow

  // ===== Background Transition =====
  backgroundTransition: 'fade',

  // ===== Parallax (disabled) =====
  parallaxBackgroundImage: '',
  parallaxBackgroundSize: '',

  // ===== Performance =====
  preloadIframes: true,
  autoPlayMedia: null,

  // ===== Hash =====
  hash: true,
  respondToHashChanges: true,

  // ===== History =====
  history: true,

  // ===== PDF Export =====
  pdfMaxPagesPerSlide: 1,
  pdfSeparateFragments: true,
  pdfPageHeightOffset: -1,

  // ===== Plugins =====
  plugins: [RevealChart],

  // ===== Chart.js Configuration =====
  chart: {
    defaults: {
      color: 'lightgray',
      font: {
        family: 'Inter, system-ui, sans-serif',
        size: 14
      }
    }
  }
};

// ===== INITIALIZATION FUNCTIONS =====

/**
 * Initialize Reveal.js with our configuration
 */
function initReveal() {
  if (typeof Reveal === 'undefined') {
    console.error('Reveal.js not loaded. Make sure reveal.js is included before reveal-config.js');
    return;
  }

  // Initialize Reveal
  Reveal.initialize(RevealConfig);

  // Log initialization
  console.log('✅ Reveal.js initialized with custom config');
  console.log('   - Base dimensions: 1920×1080px (fixed)');
  console.log('   - Scaling: down-only (0.1 - 1.0) - fits smaller viewports');
  console.log('   - Grid system: Fixed pixel layout for L02/L25/etc.');
  console.log('   - Keyboard shortcuts: G=Grid, B=Borders, C=Controls, H=Help');

  // Add event listeners
  Reveal.on('ready', onRevealReady);
  Reveal.on('slidechanged', onSlideChanged);
}

/**
 * Called when Reveal is ready
 */
function onRevealReady(event) {
  console.log('✅ Reveal.js ready');
  console.log(`   - Total slides: ${Reveal.getTotalSlides()}`);
  console.log(`   - Current slide: ${event.indexh}`);

  // Verify viewport size
  const slideElement = document.querySelector('.reveal .slides section');
  if (slideElement) {
    const bounds = slideElement.getBoundingClientRect();
    console.log(`   - Slide dimensions: ${Math.round(bounds.width)}px × ${Math.round(bounds.height)}px`);

    // Warn if slide doesn't fill viewport
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    if (Math.abs(bounds.width - viewportWidth) > 10 || Math.abs(bounds.height - viewportHeight) > 10) {
      console.warn('⚠️  Slide not filling viewport!');
      console.warn(`   Expected: ${viewportWidth}px × ${viewportHeight}px`);
      console.warn(`   Actual: ${Math.round(bounds.width)}px × ${Math.round(bounds.height)}px`);
    }
  }
}

/**
 * Called when slide changes
 */
function onSlideChanged(event) {
  console.log(`Slide changed: ${event.indexh} / ${Reveal.getTotalSlides()}`);

  // Update slide number in footer if it exists (0-based display)
  const footer = document.querySelector('.footer');
  if (footer) {
    const slideNumber = footer.querySelector('.slide-number');
    if (slideNumber) {
      slideNumber.textContent = `${event.indexh} / ${Reveal.getTotalSlides()}`;
    }
  }
}

// ===== UTILITY FUNCTIONS =====

/**
 * Get current slide info
 */
function getCurrentSlideInfo() {
  const indices = Reveal.getIndices();
  const currentSlide = Reveal.getCurrentSlide();

  return {
    index: indices.h,  // 0-based (frontend adds 1 for display)
    total: Reveal.getTotalSlides(),
    layoutId: currentSlide ? currentSlide.dataset.layout : 'unknown'
  };
}

/**
 * Navigate to specific slide (0-based index)
 */
function goToSlide(index) {
  Reveal.slide(index);  // Now expects 0-based index
}

/**
 * Toggle overview mode (grid view of all slides)
 * Called by ESC key or from parent window
 */
function toggleOverview() {
  if (typeof Reveal !== 'undefined') {
    Reveal.toggleOverview();
    console.log(`Overview mode: ${Reveal.isOverview() ? 'ON' : 'OFF'}`);
  }
}

/**
 * Check if overview mode is active
 */
function isOverviewActive() {
  return typeof Reveal !== 'undefined' ? Reveal.isOverview() : false;
}

// Make functions globally available
if (typeof window !== 'undefined') {
  window.RevealConfig = RevealConfig;
  window.initReveal = initReveal;
  window.toggleGridOverlay = toggleGridOverlay;
  window.toggleBorderHighlight = toggleBorderHighlight;
  window.toggleControlsPanel = toggleControlsPanel;
  window.toggleHelpText = toggleHelpText;
  window.getCurrentSlideInfo = getCurrentSlideInfo;
  window.goToSlide = goToSlide;
  window.toggleOverview = toggleOverview; // Expose for parent window
  window.isOverviewActive = isOverviewActive; // Expose for parent window
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    RevealConfig,
    initReveal,
    toggleGridOverlay,
    toggleBorderHighlight,
    toggleControlsPanel,
    toggleHelpText,
    getCurrentSlideInfo,
    goToSlide,
    toggleOverview,
    isOverviewActive
  };
}
