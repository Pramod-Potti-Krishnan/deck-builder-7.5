/**
 * Dynamic Template Renderers for X-Series Layouts
 *
 * X-series layouts dynamically split the content area of base templates
 * (C1, I1-I4) into sub-zones based on content analysis.
 *
 * X-Series Mapping:
 * - X1 → C1-text (1800×840px content area)
 * - X2 → I1-image-left (1200×840px content area)
 * - X3 → I2-image-right (1140×840px content area)
 * - X4 → I3-image-left-narrow (1500×840px content area)
 * - X5 → I4-image-right-narrow (1440×840px content area)
 *
 * What stays the same: Title, subtitle, footer, logo, image (for I-series)
 * What changes: Content area is split into multiple sub-zones
 */

(function() {
  'use strict';

  // Cache for fetched dynamic layouts
  const dynamicLayoutCache = new Map();

  // X-series to base layout mapping
  const X_SERIES_BASE_LAYOUTS = {
    1: 'C1-text',
    2: 'I1-image-left',
    3: 'I2-image-right',
    4: 'I3-image-left-narrow',
    5: 'I4-image-right-narrow'
  };

  // Base layout slot definitions (structural slots only)
  // These stay the same regardless of content area splits
  const BASE_STRUCTURAL_SLOTS = {
    'C1-text': {
      title: { gridRow: '1/3', gridColumn: '2/32' },
      subtitle: { gridRow: '3/4', gridColumn: '2/32' },
      footer: { gridRow: '18/19', gridColumn: '2/7' },
      logo: { gridRow: '17/19', gridColumn: '30/32' }
    },
    'I1-image-left': {
      image: { gridRow: '1/19', gridColumn: '1/12' },
      title: { gridRow: '1/3', gridColumn: '12/32' },
      subtitle: { gridRow: '3/4', gridColumn: '12/32' },
      footer: { gridRow: '18/19', gridColumn: '12/17' },
      logo: { gridRow: '17/19', gridColumn: '30/32' }
    },
    'I2-image-right': {
      image: { gridRow: '1/19', gridColumn: '21/33' },
      title: { gridRow: '1/3', gridColumn: '2/21' },
      subtitle: { gridRow: '3/4', gridColumn: '2/21' },
      footer: { gridRow: '18/19', gridColumn: '2/7' },
      logo: { gridRow: '17/19', gridColumn: '18/20' }
    },
    'I3-image-left-narrow': {
      image: { gridRow: '1/19', gridColumn: '1/7' },
      title: { gridRow: '1/3', gridColumn: '7/32' },
      subtitle: { gridRow: '3/4', gridColumn: '7/32' },
      footer: { gridRow: '18/19', gridColumn: '7/12' },
      logo: { gridRow: '17/19', gridColumn: '30/32' }
    },
    'I4-image-right-narrow': {
      image: { gridRow: '1/19', gridColumn: '26/33' },
      title: { gridRow: '1/3', gridColumn: '2/26' },
      subtitle: { gridRow: '3/4', gridColumn: '2/26' },
      footer: { gridRow: '18/19', gridColumn: '2/7' },
      logo: { gridRow: '17/19', gridColumn: '23/25' }
    }
  };

  /**
   * Check if a layout ID is an X-series dynamic layout
   * Pattern: X{1-5}-{8 hex characters}
   */
  function isXSeriesLayout(layoutId) {
    return /^X[1-5]-[a-f0-9]{8}$/.test(layoutId);
  }

  /**
   * Extract X-series number from layout ID
   */
  function getXSeriesNumber(layoutId) {
    const match = layoutId.match(/^X(\d)/);
    return match ? parseInt(match[1], 10) : null;
  }

  /**
   * Get base layout for an X-series layout ID
   */
  function getBaseLayout(layoutId) {
    const series = getXSeriesNumber(layoutId);
    return series ? X_SERIES_BASE_LAYOUTS[series] : null;
  }

  /**
   * Fetch dynamic layout from the API
   * Returns cached version if available
   */
  async function fetchDynamicLayout(layoutId) {
    // Check cache first
    if (dynamicLayoutCache.has(layoutId)) {
      return dynamicLayoutCache.get(layoutId);
    }

    try {
      const response = await fetch(`/api/dynamic-layouts/${layoutId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch layout ${layoutId}: ${response.status}`);
      }
      const layoutData = await response.json();

      // Cache the result
      dynamicLayoutCache.set(layoutId, layoutData);
      return layoutData;
    } catch (error) {
      console.error(`[DynamicTemplates] Error fetching layout ${layoutId}:`, error);
      return null;
    }
  }

  /**
   * Clear the layout cache (useful after layout updates)
   */
  function clearLayoutCache(layoutId = null) {
    if (layoutId) {
      dynamicLayoutCache.delete(layoutId);
    } else {
      dynamicLayoutCache.clear();
    }
  }

  /**
   * Build background style for a slide
   */
  function buildDynamicBackgroundStyle(slide, content, defaultColor) {
    // Delegate to global function if available
    if (typeof window.buildBackgroundStyle === 'function') {
      return window.buildBackgroundStyle(slide, content, defaultColor);
    }

    const bgColor = content?.background_color || slide?.background_color || defaultColor;
    return `background-color: ${bgColor};`;
  }

  /**
   * Render an X-series dynamic layout
   *
   * This function:
   * 1. Renders a blank grid container with structural slots
   * 2. Adds zone containers for the dynamically split content area
   * 3. DirectElementCreator will populate elements after render
   *
   * @param {string} layoutId - X-series layout ID (e.g., "X1-a3f7e8c2")
   * @param {Object} content - Content object from slide data
   * @param {Object} slide - Slide data object
   * @param {number} slideIndex - 0-based slide index
   * @param {Object} layoutData - Optional pre-fetched layout data (for sync rendering)
   * @returns {string} HTML string for the slide
   */
  function renderXSeriesLayout(layoutId, content, slide = {}, slideIndex = 0, layoutData = null) {
    const series = getXSeriesNumber(layoutId);
    const baseLayout = getBaseLayout(layoutId);

    if (!series || !baseLayout) {
      console.error(`[DynamicTemplates] Invalid X-series layout ID: ${layoutId}`);
      return renderFallbackSlide(layoutId, slideIndex);
    }

    const backgroundStyle = buildDynamicBackgroundStyle(slide, content, 'var(--theme-bg, #ffffff)');

    // Build zone containers HTML if layout data is available
    let zonesHtml = '';
    if (layoutData && layoutData.zones) {
      zonesHtml = layoutData.zones.map((zone, idx) => {
        return `
          <div class="dynamic-zone"
               data-zone-id="${zone.zone_id}"
               data-zone-index="${idx}"
               data-zone-label="${zone.label || ''}"
               data-content-type-hint="${zone.content_type_hint || ''}"
               style="
                 grid-row: ${zone.grid_row};
                 grid-column: ${zone.grid_column};
                 position: relative;
                 z-index: ${zone.z_index || (100 + idx)};
               ">
          </div>
        `;
      }).join('');
    }

    return `
      <section data-layout="${layoutId}"
               data-template="${layoutId}"
               data-base-layout="${baseLayout}"
               data-x-series="${series}"
               class="dynamic-slide x-series-slide grid-container"
               data-slide-index="${slideIndex}"
               data-direct-elements="true"
               data-dynamic-layout="true"
               style="${backgroundStyle}">
        ${zonesHtml}
      </section>
    `;
  }

  /**
   * Render a fallback slide when layout fetch fails
   */
  function renderFallbackSlide(layoutId, slideIndex) {
    return `
      <section data-layout="${layoutId}"
               data-template="${layoutId}"
               class="content-slide grid-container error-slide"
               data-slide-index="${slideIndex}"
               style="background-color: #fef2f2;">
        <div style="
          grid-row: 8/11;
          grid-column: 4/30;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          color: #dc2626;
          font-family: Poppins, sans-serif;
        ">
          <div style="font-size: 24px; font-weight: bold; margin-bottom: 8px;">
            Layout Not Found
          </div>
          <div style="font-size: 16px; color: #9ca3af;">
            Dynamic layout "${layoutId}" could not be loaded.
          </div>
        </div>
      </section>
    `;
  }

  /**
   * Async render function that fetches layout data first
   * Use this when layout data is not pre-cached
   */
  async function renderXSeriesLayoutAsync(layoutId, content, slide = {}, slideIndex = 0) {
    const layoutData = await fetchDynamicLayout(layoutId);
    return renderXSeriesLayout(layoutId, content, slide, slideIndex, layoutData);
  }

  /**
   * Get structural slots for an X-series layout
   * These are the slots that stay the same (title, subtitle, footer, logo, image)
   */
  function getStructuralSlots(layoutId) {
    const baseLayout = getBaseLayout(layoutId);
    return baseLayout ? BASE_STRUCTURAL_SLOTS[baseLayout] : null;
  }

  /**
   * Convert zones to TEMPLATE_REGISTRY-compatible slot format
   * This allows DirectElementCreator to create elements for zones
   */
  function zonesToSlots(zones, baseLayout) {
    const slots = {};

    zones.forEach((zone, idx) => {
      slots[zone.zone_id] = {
        gridRow: zone.grid_row,
        gridColumn: zone.grid_column,
        tag: 'body',  // Default to body text type
        accepts: ['body', 'html', 'text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '10px'
        },
        defaultText: zone.label || `Zone ${idx + 1}`,
        description: zone.label || `Dynamic zone ${idx + 1}`,
        isDynamicZone: true,
        contentTypeHint: zone.content_type_hint
      };
    });

    return slots;
  }

  /**
   * Create a virtual template entry for an X-series layout
   * This can be added to TEMPLATE_REGISTRY dynamically
   */
  function createVirtualTemplate(layoutId, layoutData) {
    const baseLayout = layoutData.base_layout;
    const structuralSlots = BASE_STRUCTURAL_SLOTS[baseLayout] || {};
    const zoneSlots = zonesToSlots(layoutData.zones, baseLayout);

    // Build template slot definitions from structural + zones
    const slots = {};

    // Add structural slots with full style definitions
    const baseTemplate = typeof TEMPLATE_REGISTRY !== 'undefined'
      ? TEMPLATE_REGISTRY[baseLayout]
      : null;

    if (baseTemplate && baseTemplate.slots) {
      // Copy structural slots from base template
      for (const [slotName, slotPos] of Object.entries(structuralSlots)) {
        if (baseTemplate.slots[slotName]) {
          slots[slotName] = {
            ...baseTemplate.slots[slotName],
            gridRow: slotPos.gridRow,
            gridColumn: slotPos.gridColumn
          };
        }
      }
    }

    // Add zone slots (these replace the 'content' slot)
    Object.assign(slots, zoneSlots);

    return {
      id: layoutId,
      name: layoutData.name,
      category: 'dynamic',
      series: 'X',
      description: layoutData.description || `Dynamic layout based on ${baseLayout}`,
      baseLayout: baseLayout,
      themingEnabled: true,
      isDynamic: true,
      contentType: layoutData.content_type,
      splitPattern: layoutData.split_pattern,
      splitDirection: layoutData.split_direction,
      zoneCount: layoutData.zone_count,
      zones: layoutData.zones,
      contentArea: layoutData.content_area,
      slots: slots,
      defaults: {}
    };
  }

  /**
   * Register a dynamic layout in TEMPLATE_REGISTRY
   * This allows the layout to be used like any other template
   */
  function registerDynamicLayout(layoutId, layoutData) {
    if (typeof TEMPLATE_REGISTRY === 'undefined') {
      console.warn('[DynamicTemplates] TEMPLATE_REGISTRY not available');
      return null;
    }

    const virtualTemplate = createVirtualTemplate(layoutId, layoutData);
    TEMPLATE_REGISTRY[layoutId] = virtualTemplate;

    // Also add to TEMPLATE_CATEGORIES.dynamic
    if (typeof TEMPLATE_CATEGORIES !== 'undefined') {
      if (!TEMPLATE_CATEGORIES.dynamic.templates.includes(layoutId)) {
        TEMPLATE_CATEGORIES.dynamic.templates.push(layoutId);
      }
    }

    console.log(`[DynamicTemplates] Registered dynamic layout: ${layoutId}`);
    return virtualTemplate;
  }

  /**
   * Fetch and register a dynamic layout
   * Convenience function that does both operations
   */
  async function loadAndRegisterDynamicLayout(layoutId) {
    const layoutData = await fetchDynamicLayout(layoutId);
    if (layoutData) {
      return registerDynamicLayout(layoutId, layoutData);
    }
    return null;
  }

  // ===== EXPORTS =====

  // Export to window
  window.DynamicTemplates = {
    // Core functions
    isXSeriesLayout,
    getXSeriesNumber,
    getBaseLayout,
    getStructuralSlots,

    // Rendering
    renderXSeriesLayout,
    renderXSeriesLayoutAsync,

    // Layout management
    fetchDynamicLayout,
    clearLayoutCache,
    registerDynamicLayout,
    loadAndRegisterDynamicLayout,
    createVirtualTemplate,
    zonesToSlots,

    // Constants
    X_SERIES_BASE_LAYOUTS,
    BASE_STRUCTURAL_SLOTS
  };

  // Also expose key functions directly
  window.isXSeriesLayout = isXSeriesLayout;
  window.renderXSeriesLayout = renderXSeriesLayout;
  window.fetchDynamicLayout = fetchDynamicLayout;

  console.log('[DynamicTemplates] Module loaded. Use DynamicTemplates.* for X-series layout support.');

})();
