/**
 * Theme Registry
 *
 * Client-side theme definitions that mirror the backend predefined themes.
 * Used for instant preview without API calls and for style cascade calculations.
 *
 * This should be kept in sync with PREDEFINED_THEMES in server.py
 *
 * @module ThemeRegistry
 */

const THEME_REGISTRY = {
    'corporate-blue': {
        id: 'corporate-blue',
        name: 'Corporate Blue',
        description: 'Professional blue theme for business presentations',

        colors: {
            primary: '#1e40af',
            primaryLight: '#3b82f6',
            primaryDark: '#1e3a8a',
            accent: '#f59e0b',
            background: '#ffffff',
            backgroundAlt: '#f8fafc',
            textPrimary: '#1f2937',
            textSecondary: '#6b7280',
            textBody: '#374151',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#e5e7eb',
            heroBackground: '#1e3a5f',
            footerText: '#6b7280',
            border: '#e5e7eb',
            // Tertiary colors
            tertiary1: '#f8fafc',
            tertiary2: '#e2e8f0',
            tertiary3: '#94a3b8',
            // Chart colors
            chart1: '#3b82f6',
            chart2: '#10b981',
            chart3: '#f59e0b',
            chart4: '#ef4444',
            chart5: '#8b5cf6',
            chart6: '#ec4899'
        },

        typography: {
            fontFamily: 'Poppins, sans-serif',
            standard: {
                title: { fontSize: '42px', fontWeight: 'bold', lineHeight: '1.2' },
                subtitle: { fontSize: '24px', fontWeight: 'normal', lineHeight: '1.4' },
                body: { fontSize: '20px', lineHeight: '1.6' },
                footer: { fontSize: '18px', fontWeight: '500' }
            },
            hero: {
                title: { fontSize: '72px', fontWeight: 'bold', textShadow: '0 2px 4px rgba(0,0,0,0.3)' },
                subtitle: { fontSize: '32px', fontWeight: 'normal' },
                footer: { fontSize: '18px' }
            }
        },

        contentStyles: {
            h1: { fontSize: '36px', fontWeight: 'bold', marginBottom: '16px' },
            h2: { fontSize: '28px', fontWeight: '600', marginBottom: '12px' },
            h3: { fontSize: '22px', fontWeight: '600', marginBottom: '8px' },
            p: { fontSize: '20px', lineHeight: '1.6', marginBottom: '12px' },
            ul: { paddingLeft: '24px', marginBottom: '12px' },
            li: { marginBottom: '6px' }
        }
    },

    'elegant-emerald': {
        id: 'elegant-emerald',
        name: 'Elegant Emerald',
        description: 'Sophisticated theme with nature-inspired elegance',

        colors: {
            primary: '#059669',
            primaryLight: '#10b981',
            primaryDark: '#047857',
            accent: '#fbbf24',
            background: '#f0fdf4',
            backgroundAlt: '#ecfdf5',
            textPrimary: '#064e3b',
            textSecondary: '#047857',
            textBody: '#065f46',
            heroTextPrimary: '#ecfdf5',
            heroTextSecondary: '#a7f3d0',
            heroBackground: '#064e3b',
            footerText: '#059669',
            border: '#d1fae5',
            // Tertiary colors
            tertiary1: '#ecfdf5',
            tertiary2: '#a7f3d0',
            tertiary3: '#6ee7b7',
            // Chart colors
            chart1: '#10b981',
            chart2: '#3b82f6',
            chart3: '#f59e0b',
            chart4: '#ef4444',
            chart5: '#8b5cf6',
            chart6: '#ec4899'
        },

        typography: {
            fontFamily: 'Lato, sans-serif',
            fontFamilyHeading: 'Playfair Display, serif',
            standard: {
                title: { fontSize: '46px', fontWeight: '700', lineHeight: '1.2' },
                subtitle: { fontSize: '22px', fontWeight: 'normal', lineHeight: '1.4' },
                body: { fontSize: '20px', lineHeight: '1.6' },
                footer: { fontSize: '16px', fontWeight: '500' }
            },
            hero: {
                title: { fontSize: '70px', fontWeight: '700', textShadow: '0 2px 4px rgba(0,0,0,0.2)' },
                subtitle: { fontSize: '28px', fontWeight: 'normal' },
                footer: { fontSize: '16px' }
            }
        },

        contentStyles: {
            h1: { fontSize: '38px', fontWeight: '700', marginBottom: '16px' },
            h2: { fontSize: '30px', fontWeight: '600', marginBottom: '12px' },
            h3: { fontSize: '24px', fontWeight: '600', marginBottom: '8px' },
            p: { fontSize: '20px', lineHeight: '1.6', marginBottom: '12px' },
            ul: { paddingLeft: '24px', marginBottom: '12px' },
            li: { marginBottom: '6px' }
        }
    },

    'vibrant-orange': {
        id: 'vibrant-orange',
        name: 'Vibrant Orange',
        description: 'Energetic, bold theme for creative presentations',

        colors: {
            primary: '#ea580c',
            primaryLight: '#f97316',
            primaryDark: '#c2410c',
            accent: '#0891b2',
            background: '#fff7ed',  // Warm cream instead of white
            backgroundAlt: '#ffedd5',
            textPrimary: '#7c2d12',  // Dark brown-orange
            textSecondary: '#9a3412',  // Rust
            textBody: '#78350f',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#fed7aa',  // Peach
            heroBackground: '#c2410c',  // Burnt orange
            footerText: '#a8a29e',
            border: '#fdba74',
            // Tertiary colors
            tertiary1: '#fff7ed',
            tertiary2: '#fed7aa',
            tertiary3: '#fdba74',
            // Chart colors
            chart1: '#f97316',
            chart2: '#3b82f6',
            chart3: '#10b981',
            chart4: '#ef4444',
            chart5: '#8b5cf6',
            chart6: '#ec4899'
        },

        typography: {
            fontFamily: 'Montserrat, sans-serif',
            standard: {
                title: { fontSize: '44px', fontWeight: '700', lineHeight: '1.2' },
                subtitle: { fontSize: '26px', fontWeight: '500', lineHeight: '1.4' },
                body: { fontSize: '20px', lineHeight: '1.6' },
                footer: { fontSize: '18px', fontWeight: '500' }
            },
            hero: {
                title: { fontSize: '76px', fontWeight: '800', textShadow: '0 3px 6px rgba(0,0,0,0.4)' },
                subtitle: { fontSize: '34px', fontWeight: '500' },
                footer: { fontSize: '18px' }
            }
        },

        contentStyles: {
            h1: { fontSize: '40px', fontWeight: '700', marginBottom: '16px' },
            h2: { fontSize: '32px', fontWeight: '600', marginBottom: '12px' },
            h3: { fontSize: '26px', fontWeight: '600', marginBottom: '8px' },
            p: { fontSize: '20px', lineHeight: '1.6', marginBottom: '12px' },
            ul: { paddingLeft: '24px', marginBottom: '12px' },
            li: { marginBottom: '6px' }
        }
    },

    'dark-mode': {
        id: 'dark-mode',
        name: 'Dark Mode',
        description: 'Modern, elegant dark theme with dramatic contrast',

        colors: {
            primary: '#60a5fa',
            primaryLight: '#93c5fd',
            primaryDark: '#3b82f6',
            accent: '#fbbf24',  // Amber accent
            background: '#111827',  // Charcoal
            backgroundAlt: '#1f2937',
            textPrimary: '#f9fafb',  // Near white
            textSecondary: '#d1d5db',  // Light gray
            textBody: '#e5e7eb',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#9ca3af',  // Muted gray
            heroBackground: '#030712',  // Near black
            footerText: '#6b7280',
            border: '#374151',
            // Tertiary colors
            tertiary1: '#374151',
            tertiary2: '#4b5563',
            tertiary3: '#6b7280',
            // Chart colors (brighter for dark background)
            chart1: '#60a5fa',
            chart2: '#34d399',
            chart3: '#fbbf24',
            chart4: '#f87171',
            chart5: '#a78bfa',
            chart6: '#f472b6'
        },

        typography: {
            fontFamily: 'Inter, sans-serif',
            standard: {
                title: { fontSize: '40px', fontWeight: '600', lineHeight: '1.2' },
                subtitle: { fontSize: '22px', fontWeight: 'normal', lineHeight: '1.4' },
                body: { fontSize: '20px', lineHeight: '1.6' },
                footer: { fontSize: '16px', fontWeight: '500' }
            },
            hero: {
                title: { fontSize: '68px', fontWeight: '600', textShadow: '0 4px 8px rgba(0,0,0,0.6)' },
                subtitle: { fontSize: '30px', fontWeight: 'normal' },
                footer: { fontSize: '16px' }
            }
        },

        contentStyles: {
            h1: { fontSize: '36px', fontWeight: '600', marginBottom: '16px' },
            h2: { fontSize: '28px', fontWeight: '500', marginBottom: '12px' },
            h3: { fontSize: '22px', fontWeight: '500', marginBottom: '8px' },
            p: { fontSize: '20px', lineHeight: '1.6', marginBottom: '12px' },
            ul: { paddingLeft: '24px', marginBottom: '12px' },
            li: { marginBottom: '6px' }
        }
    }
};

/**
 * Default theme ID
 */
const DEFAULT_THEME_ID = 'corporate-blue';

/**
 * Get a theme by ID
 * @param {string} themeId - Theme identifier
 * @returns {Object|null} Theme configuration or null if not found
 */
function getTheme(themeId) {
    return THEME_REGISTRY[themeId] || null;
}

/**
 * Get the default theme
 * @returns {Object} Default theme configuration
 */
function getDefaultTheme() {
    return THEME_REGISTRY[DEFAULT_THEME_ID];
}

/**
 * List all available theme IDs
 * @returns {string[]} Array of theme IDs
 */
function listThemeIds() {
    return Object.keys(THEME_REGISTRY);
}

/**
 * Get theme colors with optional overrides applied
 * @param {string} themeId - Theme identifier
 * @param {Object} colorOverrides - Optional color overrides
 * @returns {Object} Merged colors
 */
function getThemeColors(themeId, colorOverrides = {}) {
    const theme = THEME_REGISTRY[themeId] || THEME_REGISTRY[DEFAULT_THEME_ID];
    return { ...theme.colors, ...colorOverrides };
}

/**
 * Check if a template ID is a hero template
 * @param {string} templateId - Template identifier
 * @returns {boolean} True if hero template
 */
function isHeroTemplate(templateId) {
    return /^H[123]/.test(templateId);
}

/**
 * Get style profile for a template (standard or hero)
 * @param {string} templateId - Template identifier
 * @returns {string} 'hero' or 'standard'
 */
function getStyleProfile(templateId) {
    return isHeroTemplate(templateId) ? 'hero' : 'standard';
}

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.THEME_REGISTRY = THEME_REGISTRY;
    window.DEFAULT_THEME_ID = DEFAULT_THEME_ID;
    window.getTheme = getTheme;
    window.getDefaultTheme = getDefaultTheme;
    window.listThemeIds = listThemeIds;
    window.getThemeColors = getThemeColors;
    window.isHeroTemplate = isHeroTemplate;
    window.getStyleProfile = getStyleProfile;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        THEME_REGISTRY,
        DEFAULT_THEME_ID,
        getTheme,
        getDefaultTheme,
        listThemeIds,
        getThemeColors,
        isHeroTemplate,
        getStyleProfile
    };
}
