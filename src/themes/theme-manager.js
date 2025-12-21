/**
 * Theme Manager
 *
 * Handles theme injection and application via CSS custom properties.
 * Works with theme-variables.css to provide dynamic theming.
 *
 * Enhanced in v7.5.4 to support:
 * - Full theme overrides (colors, typography, spacing, effects)
 * - Custom user themes
 * - Granular property updates
 *
 * Usage:
 *   ThemeManager.injectThemeStyles(themeConfig);
 *   ThemeManager.injectThemeStyles(themeConfig, overrides);
 *   ThemeManager.injectFullTheme(fullConfig);  // NEW
 *
 * @module ThemeManager
 */

const ThemeManager = (function() {
    'use strict';

    const STYLE_ELEMENT_ID = 'presentation-theme-styles';

    /**
     * Convert camelCase to kebab-case for CSS property names
     * @param {string} str - camelCase string
     * @returns {string} kebab-case string
     */
    function toKebabCase(str) {
        return str.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
    }

    /**
     * Map theme color keys to CSS variable names
     */
    const colorToCssVar = {
        primary: '--theme-primary',
        primaryLight: '--theme-primary-light',
        primary_light: '--theme-primary-light',
        primaryDark: '--theme-primary-dark',
        primary_dark: '--theme-primary-dark',
        accent: '--theme-accent',
        background: '--theme-bg',
        backgroundAlt: '--theme-bg-alt',
        background_alt: '--theme-bg-alt',
        textPrimary: '--theme-text-primary',
        text_primary: '--theme-text-primary',
        textSecondary: '--theme-text-secondary',
        text_secondary: '--theme-text-secondary',
        textBody: '--theme-text-body',
        text_body: '--theme-text-body',
        heroTextPrimary: '--theme-hero-text-primary',
        hero_text_primary: '--theme-hero-text-primary',
        heroTextSecondary: '--theme-hero-text-secondary',
        hero_text_secondary: '--theme-hero-text-secondary',
        heroBackground: '--theme-hero-bg',
        hero_background: '--theme-hero-bg',
        footerText: '--theme-footer-text',
        footer_text: '--theme-footer-text',
        border: '--theme-border',
        // Tertiary colors (v7.5.5)
        tertiary1: '--theme-tertiary-1',
        tertiary_1: '--theme-tertiary-1',
        tertiary2: '--theme-tertiary-2',
        tertiary_2: '--theme-tertiary-2',
        tertiary3: '--theme-tertiary-3',
        tertiary_3: '--theme-tertiary-3',
        // Chart colors (v7.5.5)
        chart1: '--theme-chart-1',
        chart_1: '--theme-chart-1',
        chart2: '--theme-chart-2',
        chart_2: '--theme-chart-2',
        chart3: '--theme-chart-3',
        chart_3: '--theme-chart-3',
        chart4: '--theme-chart-4',
        chart_4: '--theme-chart-4',
        chart5: '--theme-chart-5',
        chart_5: '--theme-chart-5',
        chart6: '--theme-chart-6',
        chart_6: '--theme-chart-6'
    };

    /**
     * Map spacing keys to CSS variable names (v7.5.4)
     */
    const spacingToCssVar = {
        slide_padding: '--theme-slide-padding',
        slidePadding: '--theme-slide-padding',
        element_gap: '--theme-element-gap',
        elementGap: '--theme-element-gap',
        section_gap: '--theme-section-gap',
        sectionGap: '--theme-section-gap'
    };

    /**
     * Map effects keys to CSS variable names (v7.5.4)
     */
    const effectsToCssVar = {
        border_radius: '--theme-border-radius',
        borderRadius: '--theme-border-radius',
        shadow_small: '--theme-shadow-small',
        shadowSmall: '--theme-shadow-small',
        shadow_medium: '--theme-shadow-medium',
        shadowMedium: '--theme-shadow-medium',
        shadow_large: '--theme-shadow-large',
        shadowLarge: '--theme-shadow-large'
    };

    /**
     * Get or create the theme style element
     * @returns {HTMLStyleElement}
     */
    function getStyleElement() {
        let styleEl = document.getElementById(STYLE_ELEMENT_ID);
        if (!styleEl) {
            styleEl = document.createElement('style');
            styleEl.id = STYLE_ELEMENT_ID;
            document.head.appendChild(styleEl);
        }
        return styleEl;
    }

    /**
     * Generate CSS variable declarations from theme colors
     * @param {Object} colors - Theme colors object
     * @param {Object} overrides - Optional color overrides
     * @returns {string} CSS declarations
     */
    function generateColorCss(colors, overrides = {}) {
        const mergedColors = { ...colors, ...overrides };
        const declarations = [];

        for (const [key, value] of Object.entries(mergedColors)) {
            const cssVar = colorToCssVar[key];
            if (cssVar && value) {
                declarations.push(`${cssVar}: ${value};`);
            }
        }

        return declarations.join('\n      ');
    }

    /**
     * Generate CSS variable declarations from typography settings
     * @param {Object} typography - Theme typography object
     * @returns {string} CSS declarations
     */
    function generateTypographyCss(typography) {
        if (!typography) return '';

        const declarations = [];

        // Font family
        if (typography.fontFamily) {
            declarations.push(`--theme-font-family: ${typography.fontFamily};`);
        }
        if (typography.font_family) {
            declarations.push(`--theme-font-family: ${typography.font_family};`);
        }

        // Font family for headings (v7.5.4)
        if (typography.fontFamilyHeading || typography.font_family_heading) {
            declarations.push(`--theme-font-family-heading: ${typography.fontFamilyHeading || typography.font_family_heading};`);
        }

        // Standard profile typography
        if (typography.standard) {
            const std = typography.standard;
            if (std.title) {
                if (std.title.fontSize) declarations.push(`--theme-title-size: ${std.title.fontSize};`);
                if (std.title.fontWeight) declarations.push(`--theme-title-weight: ${std.title.fontWeight};`);
                if (std.title.lineHeight) declarations.push(`--theme-title-line-height: ${std.title.lineHeight};`);
            }
            if (std.subtitle) {
                if (std.subtitle.fontSize) declarations.push(`--theme-subtitle-size: ${std.subtitle.fontSize};`);
                if (std.subtitle.fontWeight) declarations.push(`--theme-subtitle-weight: ${std.subtitle.fontWeight};`);
                if (std.subtitle.lineHeight) declarations.push(`--theme-subtitle-line-height: ${std.subtitle.lineHeight};`);
            }
            if (std.body) {
                if (std.body.fontSize) declarations.push(`--theme-body-size: ${std.body.fontSize};`);
                if (std.body.lineHeight) declarations.push(`--theme-body-line-height: ${std.body.lineHeight};`);
            }
            if (std.footer) {
                if (std.footer.fontSize) declarations.push(`--theme-footer-size: ${std.footer.fontSize};`);
                if (std.footer.fontWeight) declarations.push(`--theme-footer-weight: ${std.footer.fontWeight};`);
            }
        }

        // Hero profile typography
        if (typography.hero) {
            const hero = typography.hero;
            if (hero.title) {
                if (hero.title.fontSize) declarations.push(`--theme-hero-title-size: ${hero.title.fontSize};`);
                if (hero.title.fontWeight) declarations.push(`--theme-hero-title-weight: ${hero.title.fontWeight};`);
                if (hero.title.textShadow) declarations.push(`--theme-hero-title-shadow: ${hero.title.textShadow};`);
            }
            if (hero.subtitle) {
                if (hero.subtitle.fontSize) declarations.push(`--theme-hero-subtitle-size: ${hero.subtitle.fontSize};`);
                if (hero.subtitle.fontWeight) declarations.push(`--theme-hero-subtitle-weight: ${hero.subtitle.fontWeight};`);
            }
        }

        return declarations.join('\n      ');
    }

    /**
     * Generate CSS variable declarations from spacing settings (v7.5.4)
     * @param {Object} spacing - Theme spacing object
     * @returns {string} CSS declarations
     */
    function generateSpacingCss(spacing) {
        if (!spacing) return '';

        const declarations = [];

        for (const [key, value] of Object.entries(spacing)) {
            const cssVar = spacingToCssVar[key];
            if (cssVar && value) {
                declarations.push(`${cssVar}: ${value};`);
            }
        }

        return declarations.join('\n      ');
    }

    /**
     * Generate CSS variable declarations from effects settings (v7.5.4)
     * @param {Object} effects - Theme effects object
     * @returns {string} CSS declarations
     */
    function generateEffectsCss(effects) {
        if (!effects) return '';

        const declarations = [];

        for (const [key, value] of Object.entries(effects)) {
            const cssVar = effectsToCssVar[key];
            if (cssVar && value) {
                declarations.push(`${cssVar}: ${value};`);
            }
        }

        return declarations.join('\n      ');
    }

    /**
     * Inject theme styles into the document
     *
     * @param {Object} themeConfig - Full theme configuration object
     * @param {Object} colorOverrides - Optional color overrides (legacy, use overrides.colors instead)
     */
    function injectThemeStyles(themeConfig, colorOverrides = {}) {
        if (!themeConfig) {
            console.warn('[ThemeManager] No theme config provided');
            return;
        }

        const styleEl = getStyleElement();

        // Generate CSS for all theme sections
        const colorCss = generateColorCss(themeConfig.colors || {}, colorOverrides);
        const typographyCss = generateTypographyCss(themeConfig.typography);
        const spacingCss = generateSpacingCss(themeConfig.spacing);
        const effectsCss = generateEffectsCss(themeConfig.effects);

        // Build complete CSS
        styleEl.textContent = `
    /* Theme: ${themeConfig.name || themeConfig.id || 'Custom'} */
    :root {
      ${colorCss}
      ${typographyCss}
      ${spacingCss}
      ${effectsCss}
    }
    `;

        // Handle dark mode class
        if (themeConfig.id === 'dark-mode') {
            document.documentElement.classList.add('theme-dark-mode');
        } else {
            document.documentElement.classList.remove('theme-dark-mode');
        }

        console.log(`[ThemeManager] Applied theme: ${themeConfig.name || themeConfig.id}`);
    }

    /**
     * Inject full theme with granular overrides (v7.5.4)
     *
     * @param {Object} themeConfig - Base theme configuration
     * @param {Object} overrides - Granular overrides: {colors, typography, spacing, effects}
     */
    function injectFullTheme(themeConfig, overrides = {}) {
        if (!themeConfig) {
            console.warn('[ThemeManager] No theme config provided');
            return;
        }

        const styleEl = getStyleElement();

        // Merge base config with overrides
        const mergedColors = { ...(themeConfig.colors || {}), ...(overrides.colors || {}) };
        const mergedTypography = overrides.typography
            ? { ...(themeConfig.typography || {}), ...overrides.typography }
            : themeConfig.typography;
        const mergedSpacing = overrides.spacing
            ? { ...(themeConfig.spacing || {}), ...overrides.spacing }
            : themeConfig.spacing;
        const mergedEffects = overrides.effects
            ? { ...(themeConfig.effects || {}), ...overrides.effects }
            : themeConfig.effects;

        // Generate CSS for all sections
        const colorCss = generateColorCss(mergedColors, {});
        const typographyCss = generateTypographyCss(mergedTypography);
        const spacingCss = generateSpacingCss(mergedSpacing);
        const effectsCss = generateEffectsCss(mergedEffects);

        // Build complete CSS
        styleEl.textContent = `
    /* Theme: ${themeConfig.name || themeConfig.id || 'Custom'} (with overrides) */
    :root {
      ${colorCss}
      ${typographyCss}
      ${spacingCss}
      ${effectsCss}
    }
    `;

        // Handle dark mode
        const isDarkMode = mergedColors.background && isColorDark(mergedColors.background);
        if (themeConfig.id === 'dark-mode' || isDarkMode) {
            document.documentElement.classList.add('theme-dark-mode');
        } else {
            document.documentElement.classList.remove('theme-dark-mode');
        }

        console.log(`[ThemeManager] Applied full theme with overrides:`, {
            colors: Object.keys(overrides.colors || {}).length,
            typography: !!overrides.typography,
            spacing: !!overrides.spacing,
            effects: !!overrides.effects
        });
    }

    /**
     * Check if a color is "dark" (for auto dark-mode detection)
     * @param {string} color - Hex color string
     * @returns {boolean}
     */
    function isColorDark(color) {
        if (!color || !color.startsWith('#')) return false;
        const hex = color.replace('#', '');
        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);
        // Using luminance formula
        const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
        return luminance < 0.5;
    }

    /**
     * Apply CSS variables directly from a dictionary (v7.5.4)
     * Used with the /theme/css-variables API endpoint
     *
     * @param {Object} cssVariables - Dictionary of CSS var name -> value
     */
    function applyCssVariables(cssVariables) {
        if (!cssVariables || typeof cssVariables !== 'object') {
            console.warn('[ThemeManager] Invalid CSS variables object');
            return;
        }

        const styleEl = getStyleElement();
        const declarations = [];

        for (const [varName, value] of Object.entries(cssVariables)) {
            if (varName.startsWith('--') && value) {
                declarations.push(`${varName}: ${value};`);
            }
        }

        styleEl.textContent = `
    /* Theme: Applied via CSS Variables */
    :root {
      ${declarations.join('\n      ')}
    }
    `;

        console.log(`[ThemeManager] Applied ${declarations.length} CSS variables`);
    }

    /**
     * Remove injected theme styles (revert to defaults)
     */
    function clearThemeStyles() {
        const styleEl = document.getElementById(STYLE_ELEMENT_ID);
        if (styleEl) {
            styleEl.remove();
        }
        document.documentElement.classList.remove('theme-dark-mode');
        console.log('[ThemeManager] Theme styles cleared');
    }

    /**
     * Get current theme CSS variables as an object
     * @returns {Object} Current CSS variable values
     */
    function getCurrentThemeValues() {
        const computedStyle = getComputedStyle(document.documentElement);
        const values = {};

        for (const cssVar of Object.values(colorToCssVar)) {
            const value = computedStyle.getPropertyValue(cssVar).trim();
            if (value) {
                values[cssVar] = value;
            }
        }

        return values;
    }

    /**
     * Set a single CSS variable
     * @param {string} varName - CSS variable name (e.g., '--theme-primary')
     * @param {string} value - CSS value
     */
    function setCssVariable(varName, value) {
        document.documentElement.style.setProperty(varName, value);
    }

    /**
     * Generate CSS for deckster typography classes (v7.5.5)
     * Used by Text Service when styling_mode is "css_classes"
     *
     * @param {string} themeId - Theme identifier
     * @param {Object} theme - Theme configuration from THEME_REGISTRY
     * @returns {string} CSS string with .deckster-* class definitions
     */
    function generateDecksterClasses(themeId, theme) {
        const colors = theme.colors || {};
        const contentStyles = theme.contentStyles || {};

        return `
/* Theme: ${themeId} - Deckster Typography Classes (v7.5.5) */
/* Generated for Text Service CSS class-based styling */

.theme-${themeId} .deckster-t1 {
    font-size: ${contentStyles.h1?.fontSize || '36px'};
    font-weight: ${contentStyles.h1?.fontWeight || 'bold'};
    color: ${colors.textPrimary || '#1f2937'};
    margin-bottom: ${contentStyles.h1?.marginBottom || '16px'};
}

.theme-${themeId} .deckster-t2 {
    font-size: ${contentStyles.h2?.fontSize || '28px'};
    font-weight: ${contentStyles.h2?.fontWeight || '600'};
    color: ${colors.textPrimary || '#1f2937'};
    margin-bottom: ${contentStyles.h2?.marginBottom || '12px'};
}

.theme-${themeId} .deckster-t3 {
    font-size: ${contentStyles.h3?.fontSize || '22px'};
    font-weight: ${contentStyles.h3?.fontWeight || '600'};
    color: ${colors.textSecondary || '#6b7280'};
    margin-bottom: ${contentStyles.h3?.marginBottom || '8px'};
}

.theme-${themeId} .deckster-t4 {
    font-size: ${contentStyles.p?.fontSize || '20px'};
    font-weight: 400;
    color: ${colors.textBody || '#374151'};
    line-height: ${contentStyles.p?.lineHeight || '1.6'};
    margin-bottom: ${contentStyles.p?.marginBottom || '12px'};
}

.theme-${themeId} .deckster-emphasis {
    color: ${colors.accent || '#f59e0b'};
    font-weight: 600;
}

.theme-${themeId} .deckster-bullets {
    padding-left: ${contentStyles.ul?.paddingLeft || '24px'};
    list-style-type: disc;
    margin-bottom: ${contentStyles.ul?.marginBottom || '12px'};
}

.theme-${themeId} .deckster-bullet-item {
    margin-bottom: ${contentStyles.li?.marginBottom || '6px'};
    color: ${colors.textBody || '#374151'};
}

.theme-${themeId} .deckster-bullets .deckster-bullet-item::marker {
    color: ${colors.primary || '#1e40af'};
}
`;
    }

    /**
     * Inject deckster classes for all registered themes
     * @returns {string} Combined CSS for all themes
     */
    function generateAllDecksterClasses() {
        const THEME_REGISTRY = window.THEME_REGISTRY || {};
        let css = '';

        for (const [themeId, theme] of Object.entries(THEME_REGISTRY)) {
            css += generateDecksterClasses(themeId, theme);
        }

        return css;
    }

    /**
     * Inject deckster classes into the document
     */
    function injectDecksterClasses() {
        const css = generateAllDecksterClasses();
        let styleEl = document.getElementById('deckster-typography-styles');

        if (!styleEl) {
            styleEl = document.createElement('style');
            styleEl.id = 'deckster-typography-styles';
            document.head.appendChild(styleEl);
        }

        styleEl.textContent = css;
        console.log('[ThemeManager] Deckster typography classes injected');
    }

    // Public API
    return {
        injectThemeStyles,
        injectFullTheme,
        applyCssVariables,
        clearThemeStyles,
        getCurrentThemeValues,
        setCssVariable,
        colorToCssVar,
        spacingToCssVar,
        effectsToCssVar,
        // v7.5.5: Deckster typography classes for Text Service
        generateDecksterClasses,
        generateAllDecksterClasses,
        injectDecksterClasses
    };
})();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.ThemeManager = ThemeManager;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
