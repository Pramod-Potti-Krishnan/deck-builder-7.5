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
            border: '#e5e7eb'
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

    'minimal-gray': {
        id: 'minimal-gray',
        name: 'Minimal Gray',
        description: 'Clean, minimalist gray theme for modern presentations',

        colors: {
            primary: '#374151',
            primaryLight: '#6b7280',
            primaryDark: '#1f2937',
            accent: '#10b981',
            background: '#ffffff',
            backgroundAlt: '#f9fafb',
            textPrimary: '#111827',
            textSecondary: '#6b7280',
            textBody: '#374151',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#d1d5db',
            heroBackground: '#1f2937',
            footerText: '#9ca3af',
            border: '#e5e7eb'
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
        }
    },

    'vibrant-orange': {
        id: 'vibrant-orange',
        name: 'Vibrant Orange',
        description: 'Energetic orange theme for creative presentations',

        colors: {
            primary: '#ea580c',
            primaryLight: '#f97316',
            primaryDark: '#c2410c',
            accent: '#0891b2',
            background: '#ffffff',
            backgroundAlt: '#fff7ed',
            textPrimary: '#1c1917',
            textSecondary: '#78716c',
            textBody: '#44403c',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#fed7aa',
            heroBackground: '#9a3412',
            footerText: '#a8a29e',
            border: '#e7e5e4'
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
        }
    },

    'dark-mode': {
        id: 'dark-mode',
        name: 'Dark Mode',
        description: 'Dark theme for low-light environments',

        colors: {
            primary: '#60a5fa',
            primaryLight: '#93c5fd',
            primaryDark: '#3b82f6',
            accent: '#fbbf24',
            background: '#111827',
            backgroundAlt: '#1f2937',
            textPrimary: '#f9fafb',
            textSecondary: '#d1d5db',
            textBody: '#e5e7eb',
            heroTextPrimary: '#ffffff',
            heroTextSecondary: '#9ca3af',
            heroBackground: '#030712',
            footerText: '#6b7280',
            border: '#374151'
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
                title: { fontSize: '72px', fontWeight: 'bold', textShadow: '0 2px 4px rgba(0,0,0,0.5)' },
                subtitle: { fontSize: '32px', fontWeight: 'normal' },
                footer: { fontSize: '18px' }
            }
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
