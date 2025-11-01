/**
 * RevealJS Configuration
 *
 * Forces full viewport coverage and disables default RevealJS scaling.
 * Prevents V5's viewport cramping issues.
 *
 * Critical Settings:
 * - width/height: 100vw/100vh (full viewport)
 * - margin: 0 (no margins)
 * - minScale/maxScale: 1 (disable scaling)
 * - center: false (no auto-centering)
 * - disableLayout: true (prevent RevealJS layout interference)
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
  document.body.classList.toggle('highlight-borders');
  const isHighlighted = document.body.classList.contains('highlight-borders');
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
 * Toggle overlay badges (system indicator, completion badge, help text)
 */
function toggleOverlays() {
  const systemIndicator = document.getElementById('system-indicator');
  const completionBadge = document.getElementById('completion-badge');
  const helpText = document.getElementById('help-text');

  if (systemIndicator) systemIndicator.classList.toggle('overlay-hidden');
  if (completionBadge) completionBadge.classList.toggle('overlay-hidden');
  if (helpText) helpText.classList.toggle('overlay-hidden');

  const isHidden = systemIndicator ? systemIndicator.classList.contains('overlay-hidden') : true;
  console.log(`Overlays: ${isHidden ? 'HIDDEN' : 'VISIBLE'}`);
}

// ===== REVEAL.JS CONFIGURATION =====

const RevealConfig = {
  // ===== Viewport Settings (CRITICAL) =====
  // Reference dimensions at 16:9 ratio (Full HD)
  width: 1920,
  height: 1080,
  margin: 0,

  // Enable RevealJS scaling for responsive display
  minScale: 0.1,
  maxScale: 3.0,

  // Enable auto-centering for scaled slides
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
    16: () => { toggleOverlays(); },        // 'Shift' - Toggle overlay badges
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
  plugins: []
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
  console.log('   - Base dimensions: 1920 x 1080 (16:9 ratio)');
  console.log('   - Scaling: enabled (0.1 - 3.0)');
  console.log('   - Responsive: automatic scaling to viewport');
  console.log('   - Keyboard shortcuts: G=Grid, B=Borders, C=Controls');

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
  console.log(`   - Current slide: ${event.indexh + 1}`);

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
  console.log(`Slide changed: ${event.indexh + 1} / ${Reveal.getTotalSlides()}`);

  // Update slide number in footer if it exists
  const footer = document.querySelector('.footer');
  if (footer) {
    const slideNumber = footer.querySelector('.slide-number');
    if (slideNumber) {
      slideNumber.textContent = `${event.indexh + 1} / ${Reveal.getTotalSlides()}`;
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
    index: indices.h + 1,
    total: Reveal.getTotalSlides(),
    element: currentSlide,
    layoutId: currentSlide.dataset.layout || 'unknown'
  };
}

/**
 * Navigate to specific slide
 */
function goToSlide(index) {
  Reveal.slide(index - 1); // Convert 1-based to 0-based
}

// Make functions globally available
if (typeof window !== 'undefined') {
  window.RevealConfig = RevealConfig;
  window.initReveal = initReveal;
  window.toggleGridOverlay = toggleGridOverlay;
  window.toggleBorderHighlight = toggleBorderHighlight;
  window.toggleControlsPanel = toggleControlsPanel;
  window.toggleOverlays = toggleOverlays;
  window.getCurrentSlideInfo = getCurrentSlideInfo;
  window.goToSlide = goToSlide;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    RevealConfig,
    initReveal,
    toggleGridOverlay,
    toggleBorderHighlight,
    toggleControlsPanel,
    toggleOverlays,
    getCurrentSlideInfo,
    goToSlide
  };
}
