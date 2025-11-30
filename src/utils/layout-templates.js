/**
 * Layout Templates - Default Content for Presentation Layouts
 *
 * Provides default content templates for each layout type,
 * used when adding new slides or switching layouts.
 *
 * Layouts:
 * - L01: Centered Chart with Text Below
 * - L02: Left Diagram with Text on Right
 * - L03: Two Charts in Columns with Text Below
 * - L25: Main Content Shell (rich content area)
 * - L27: Image Left with Content Right
 * - L29: Full-Bleed Hero Slides
 */

(function() {
  'use strict';

  // Layout metadata and templates
  const LAYOUTS = {
    L01: {
      name: 'Centered Chart',
      description: 'Chart centered with text below',
      icon: '📊',
      thumbnail: '/static/thumbnails/L01.png',
      defaultContent: {
        slide_title: 'Chart Title',
        subtitle: 'Subtitle goes here',
        element_1: '<div class="chart-placeholder" style="width:100%;height:300px;background:#374151;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Chart Placeholder</div>',
        element_2: '<p>Add your analysis or key insights about the chart here.</p>'
      }
    },

    L02: {
      name: 'Diagram Left',
      description: 'Diagram on left, text on right',
      icon: '🔲',
      thumbnail: '/static/thumbnails/L02.png',
      defaultContent: {
        slide_title: 'Diagram Title',
        subtitle: 'Process or concept overview',
        element_1: '<div class="diagram-placeholder" style="width:100%;height:400px;background:#374151;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Diagram Placeholder</div>',
        element_2: '<h3>Key Points</h3><ul><li>Point one explanation</li><li>Point two explanation</li><li>Point three explanation</li></ul>'
      }
    },

    L03: {
      name: 'Two Charts',
      description: 'Two charts side by side with text below',
      icon: '📈',
      thumbnail: '/static/thumbnails/L03.png',
      defaultContent: {
        slide_title: 'Comparison Title',
        subtitle: 'Comparing two data sets',
        element_1: '<div class="chart-placeholder" style="width:100%;height:250px;background:#374151;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Chart 1</div>',
        element_2: '<div class="chart-placeholder" style="width:100%;height:250px;background:#374151;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Chart 2</div>',
        element_3: '<p><strong>Chart 1:</strong> Description of first chart. <strong>Chart 2:</strong> Description of second chart.</p>'
      }
    },

    L25: {
      name: 'Content Shell',
      description: 'Rich content area for flexible layouts',
      icon: '📝',
      thumbnail: '/static/thumbnails/L25.png',
      defaultContent: {
        slide_title: 'Content Title',
        subtitle: 'Section subtitle',
        rich_content: `
          <div class="content-section">
            <h3>Section Header</h3>
            <p>This is a content shell layout designed for rich, flexible content. You can add:</p>
            <ul>
              <li>Bulleted lists with key points</li>
              <li>Formatted text with <strong>bold</strong> and <em>italic</em> styles</li>
              <li>Multiple paragraphs and sections</li>
            </ul>
            <p>The content area provides 1800px × 720px of space for your content.</p>
          </div>
        `
      }
    },

    L27: {
      name: 'Image Left',
      description: 'Image on left, content on right',
      icon: '🖼️',
      thumbnail: '/static/thumbnails/L27.png',
      defaultContent: {
        slide_title: 'Image with Content',
        subtitle: 'Visual storytelling layout',
        element_1: '<div class="image-placeholder" style="width:100%;height:100%;min-height:400px;background:linear-gradient(135deg,#374151,#1f2937);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#9ca3af;">Image Placeholder</div>',
        element_2: '<h3>Content Area</h3><p>This layout pairs an image with supporting content. Great for:</p><ul><li>Product showcases</li><li>Team introductions</li><li>Feature highlights</li></ul>'
      }
    },

    L29: {
      name: 'Full-Bleed Hero',
      description: 'Full-screen hero slide',
      icon: '🎯',
      thumbnail: '/static/thumbnails/L29.png',
      defaultContent: {
        hero_content: `
          <div class="hero-slide" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:linear-gradient(135deg,#1e3a8a,#3730a3);color:white;padding:60px;">
            <h1 style="font-size:72px;font-weight:700;margin:0 0 20px 0;text-shadow:0 4px 20px rgba(0,0,0,0.3);">Hero Title</h1>
            <p style="font-size:28px;opacity:0.9;max-width:800px;margin:0;">Supporting text that provides context or a call to action for your audience.</p>
          </div>
        `
      }
    }
  };

  /**
   * Get layout information
   * @param {string} layoutId - Layout ID (L01, L02, etc.)
   * @returns {Object} Layout metadata
   */
  function getLayout(layoutId) {
    return LAYOUTS[layoutId] || null;
  }

  /**
   * Get all layouts
   * @returns {Object} All layout definitions
   */
  function getAllLayouts() {
    return { ...LAYOUTS };
  }

  /**
   * Get layout options for dropdown/picker
   * @returns {Array} Array of layout options for UI
   */
  function getLayoutOptions() {
    return Object.entries(LAYOUTS).map(([id, layout]) => ({
      id,
      name: layout.name,
      description: layout.description,
      icon: layout.icon,
      thumbnail: layout.thumbnail
    }));
  }

  /**
   * Get default content for a layout
   * @param {string} layoutId - Layout ID
   * @returns {Object} Default content object
   */
  function getDefaultContent(layoutId) {
    const layout = LAYOUTS[layoutId];
    if (!layout) {
      console.warn(`Unknown layout: ${layoutId}`);
      return LAYOUTS.L25.defaultContent; // Fallback to L25
    }
    return { ...layout.defaultContent };
  }

  /**
   * Map content from one layout to another
   * @param {Object} content - Source content
   * @param {string} fromLayout - Source layout ID
   * @param {string} toLayout - Target layout ID
   * @returns {Object} Mapped content
   */
  function mapContent(content, fromLayout, toLayout) {
    const targetDefault = getDefaultContent(toLayout);
    const mapped = { ...targetDefault };

    // Common field mappings
    if (content.slide_title) mapped.slide_title = content.slide_title;
    if (content.subtitle) mapped.subtitle = content.subtitle;

    // Layout-specific mappings
    if (fromLayout === 'L29' && toLayout !== 'L29') {
      // Converting from hero to standard layout
      if (content.hero_content) {
        mapped.rich_content = content.hero_content;
      }
    } else if (fromLayout !== 'L29' && toLayout === 'L29') {
      // Converting from standard to hero layout
      const title = content.slide_title || 'Hero Title';
      const subtitle = content.subtitle || 'Add your message here';
      mapped.hero_content = `
        <div class="hero-slide" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:linear-gradient(135deg,#1e3a8a,#3730a3);color:white;padding:60px;">
          <h1 style="font-size:72px;font-weight:700;margin:0 0 20px 0;">${title}</h1>
          <p style="font-size:28px;opacity:0.9;">${subtitle}</p>
        </div>
      `;
    } else {
      // Standard to standard layout mapping
      if (content.rich_content) mapped.rich_content = content.rich_content;
      if (content.element_1) mapped.element_1 = content.element_1;
      if (content.element_2) mapped.element_2 = content.element_2;
      if (content.element_3) mapped.element_3 = content.element_3;
    }

    return mapped;
  }

  /**
   * Create slide picker HTML
   * @returns {string} HTML for layout picker UI
   */
  function createLayoutPickerHTML() {
    const options = getLayoutOptions();

    return `
      <div class="layout-picker">
        <div class="layout-picker-header">
          <h3>Choose a Layout</h3>
          <button class="layout-picker-close" onclick="closeLayoutPicker()">&times;</button>
        </div>
        <div class="layout-picker-grid">
          ${options.map(opt => `
            <div class="layout-option" data-layout="${opt.id}" onclick="selectLayout('${opt.id}')">
              <div class="layout-thumbnail">
                <span class="layout-icon">${opt.icon}</span>
              </div>
              <div class="layout-info">
                <span class="layout-name">${opt.name}</span>
                <span class="layout-desc">${opt.description}</span>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  /**
   * Create layout dropdown HTML
   * @param {string} selectedLayout - Currently selected layout
   * @returns {string} HTML for layout dropdown
   */
  function createLayoutDropdownHTML(selectedLayout = '') {
    const options = getLayoutOptions();

    return `
      <select class="layout-dropdown" onchange="handleLayoutChange(this.value)">
        <option value="">Select Layout...</option>
        ${options.map(opt => `
          <option value="${opt.id}" ${opt.id === selectedLayout ? 'selected' : ''}>
            ${opt.icon} ${opt.name}
          </option>
        `).join('')}
      </select>
    `;
  }

  // Expose functions globally
  window.LayoutTemplates = {
    getLayout,
    getAllLayouts,
    getLayoutOptions,
    getDefaultContent,
    mapContent,
    createLayoutPickerHTML,
    createLayoutDropdownHTML,
    LAYOUTS
  };

})();
