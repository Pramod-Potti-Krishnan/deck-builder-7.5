/**
 * Template Registry for Frontend Slide Templates
 *
 * This is a NEW system for frontend-driven slide creation.
 * It does NOT modify existing L25/L02/L29 backend-generated content.
 *
 * Templates define:
 * - Slot positions and sizes (consistent title/subtitle/footer across all)
 * - What content types each slot accepts
 * - Default styling per slot type
 */

const TEMPLATE_REGISTRY = {
  // ===========================================
  // HERO TEMPLATES (Full-bleed slides)
  // ===========================================

  'H1-generated': {
    id: 'H1-generated',
    name: 'Title Slide (AI Generated)',
    category: 'hero',
    description: 'Full-bleed title slide - AI generates entire design',
    renderer: 'renderH1Generated',
    baseLayout: 'L29',
    themingEnabled: true,
    slots: {
      hero: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'hero_content',
        accepts: ['hero_content'],
        description: 'Full slide canvas for AI-generated content'
      }
    },
    defaults: {
      background_color: 'var(--theme-text-primary, #1f2937)'
    },
    thumbnail: 'hero-generated.svg'
  },

  'H1-structured': {
    id: 'H1-structured',
    name: 'Title Slide (Manual)',
    category: 'hero',
    description: 'Structured title slide with editable title, subtitle, and customizable background',
    renderer: 'renderH1Structured',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      background: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'background',
        accepts: ['image', 'color', 'gradient'],
        style: { zIndex: -1 },
        defaultText: null,
        description: 'Background image or color'
      },
      title: {
        gridRow: '7/10',
        gridColumn: '3/17',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-hero-title-size, 48px)',
          fontWeight: 'var(--theme-hero-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',    // LEFT (horizontal cross-axis)
          justifyContent: 'flex-end',  // BOTTOM (vertical main-axis)
          textAlign: 'left'
        },
        defaultText: 'Presentation Title',
        description: 'Main presentation title'
      },
      subtitle: {
        gridRow: '10/12',
        gridColumn: '3/17',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-hero-subtitle-size, 32px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-secondary, #94a3b8)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',    // LEFT (horizontal cross-axis)
          justifyContent: 'flex-start', // TOP (vertical main-axis)
          textAlign: 'left'
        },
        defaultText: 'Presentation Subtitle',
        description: 'Subtitle or tagline'
      },
      author_info: {
        gridRow: '16/18',
        gridColumn: '3/17',
        tag: 'author_info',
        accepts: ['text'],
        style: {
          fontSize: '26px',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          textTransform: 'uppercase'
        },
        defaultText: 'AUTHOR | DATE',
        description: 'Presenter name, date, or other info'
      },
      logo: {
        gridRow: '16/18',
        gridColumn: '28/31',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          textTransform: 'capitalize'
        },
        defaultText: 'Logo',
        description: 'Company logo'
      }
    },
    defaults: {
      background_color: '#1e3a5f',
      background_image: null
    },
    thumbnail: 'hero-structured.svg'
  },

  'H2-section': {
    id: 'H2-section',
    name: 'Section Divider',
    category: 'hero',
    description: 'Chapter/section break slide',
    renderer: 'renderH2Section',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      background: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'background',
        accepts: ['image', 'color', 'gradient'],
        style: { zIndex: -1 },
        defaultText: null,
        description: 'Background image or color'
      },
      section_number: {
        gridRow: '6/11',
        gridColumn: '11/17',  // Large number on left side
        tag: 'section_number',
        accepts: ['text'],
        style: {
          fontSize: '180px',  // Large section number - decorative, not themed
          fontWeight: 'var(--theme-hero-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',      // CENTER (horizontal)
          justifyContent: 'center',  // CENTER (vertical)
          textAlign: 'center'
        },
        defaultText: '#',
        description: 'Section number placeholder'
      },
      title: {
        gridRow: '6/11',
        gridColumn: '17/31',  // Title on right side next to number
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-hero-title-size, 64px)',
          fontWeight: 'var(--theme-hero-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',    // LEFT (horizontal)
          justifyContent: 'center',    // CENTER (vertical)
          textAlign: 'left',
          textTransform: 'capitalize'
        },
        defaultText: 'Section Title',
        description: 'Section title'
      }
      // NOTE: No subtitle in Template Builder design for H2-section
    },
    defaults: {
      background_color: 'var(--theme-text-body, #374151)'
    },
    thumbnail: 'section-divider.svg'
  },

  'H3-closing': {
    id: 'H3-closing',
    name: 'Closing Slide',
    category: 'hero',
    description: 'Thank you / closing slide with contact info',
    renderer: 'renderH3Closing',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      background: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'background',
        accepts: ['image', 'color', 'gradient'],
        style: { zIndex: -1 },
        defaultText: null,
        description: 'Background image or color'
      },
      title: {
        gridRow: '6/9',
        gridColumn: '3/31',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-hero-title-size, 48px)',
          fontWeight: 'var(--theme-hero-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',        // CENTER (horizontal)
          justifyContent: 'flex-end',  // BOTTOM (vertical)
          textAlign: 'center'
        },
        defaultText: 'Thank You',
        description: 'Closing message (e.g., "Thank You")'
      },
      subtitle: {
        gridRow: '9/11',
        gridColumn: '5/29',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-hero-subtitle-size, 32px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-secondary, #94a3b8)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',        // CENTER (horizontal)
          justifyContent: 'flex-start', // TOP (vertical)
          textAlign: 'center'
        },
        defaultText: 'We appreciate your time',
        description: 'Additional message or call to action'
      },
      contact_info: {
        gridRow: '12/15',
        gridColumn: '8/26',
        tag: 'contact',
        accepts: ['text', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-hero-text-primary, #ffffff)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',        // CENTER (horizontal)
          justifyContent: 'flex-start', // TOP (vertical)
          textAlign: 'center',
          textTransform: 'none'
        },
        defaultText: 'email@company.com | www.company.com',
        description: 'Contact details, website, social links'
      },
      logo: {
        gridRow: '16/18',
        gridColumn: '26/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo',
        description: 'Company logo'
      }
    },
    defaults: {
      background_color: '#1e3a5f'
    },
    thumbnail: 'closing-slide.svg'
  },

  // ===========================================
  // SINGLE CONTENT TEMPLATES
  // ===========================================

  'C1-text': {
    id: 'C1-text',
    name: 'Text Content',
    category: 'content',
    description: 'Standard slide with body text (paragraphs, bullets)',
    renderer: 'renderC1Text',
    baseLayout: 'L25',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',           // Dark for content slides
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',           // Medium gray for subtitle
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-start', // TOP align (vertical) - sits right below title
          textAlign: 'left',
          padding: '0',
          paddingTop: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/32',
        tag: 'body',
        accepts: ['body', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)',           // Body text gray
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Content Area',
        description: 'Main text content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',           // Light gray for footer
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'content-text.svg'
  },

  // C2-table REMOVED - merged into C1-text (tables are hypertext)

  'C3-chart': {
    id: 'C3-chart',
    name: 'Single Chart',
    category: 'content',
    description: 'Slide with one chart visualization',
    renderer: 'renderC3Chart',
    baseLayout: 'L25',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-start', // TOP align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingTop: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/32',
        tag: 'chart',
        accepts: ['chart'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Chart Area',
        description: 'Chart placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'content-chart.svg'
  },

  'C4-infographic': {
    id: 'C4-infographic',
    name: 'Single Infographic',
    category: 'content',
    description: 'Slide with one infographic',
    renderer: 'renderC4Infographic',
    baseLayout: 'L25',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-start', // TOP align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingTop: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/32',
        tag: 'infographic',
        accepts: ['infographic'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Infographic Area',
        description: 'Infographic placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'content-infographic.svg'
  },

  'C5-diagram': {
    id: 'C5-diagram',
    name: 'Single Diagram',
    category: 'content',
    description: 'Slide with one diagram',
    renderer: 'renderC5Diagram',
    baseLayout: 'L25',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-start', // TOP align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingTop: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/32',
        tag: 'diagram',
        accepts: ['diagram'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Diagram Area',
        description: 'Diagram placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'content-diagram.svg'
  },

  // C6-image REMOVED - use I series for image layouts

  // ===========================================
  // VISUAL + TEXT TEMPLATES (V Series)
  // Visual element LEFT, text insights RIGHT
  // ===========================================

  'V1-image-text': {
    id: 'V1-image-text',
    name: 'Image + Text',
    category: 'visual',
    description: 'Image on left, text insights on right',
    renderer: 'renderV1ImageText',
    baseLayout: 'L02',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '0',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content_left: {
        gridRow: '4/18',
        gridColumn: '2/20',
        tag: 'image',
        accepts: ['image'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingLeft: '5px'
        },
        defaultText: null,
        description: 'Image area (900x720px)'
      },
      content_right: {
        gridRow: '4/18',
        gridColumn: '20/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '20px 25px 20px 10px'
        },
        defaultText: 'Key Insights',
        description: 'Text/observations (600x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'visual-image-text.svg'
  },

  'V2-chart-text': {
    id: 'V2-chart-text',
    name: 'Chart + Text',
    category: 'visual',
    description: 'Chart on left, text insights on right',
    renderer: 'renderV2ChartText',
    baseLayout: 'L02',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '0',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content_left: {
        gridRow: '4/18',
        gridColumn: '2/20',
        tag: 'chart',
        accepts: ['chart'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingLeft: '5px'
        },
        defaultText: null,
        description: 'Chart area (900x720px)'
      },
      content_right: {
        gridRow: '4/18',
        gridColumn: '20/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '20px 25px 20px 10px'
        },
        defaultText: 'Key Insights',
        description: 'Text/observations (600x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'visual-chart-text.svg'
  },

  'V3-diagram-text': {
    id: 'V3-diagram-text',
    name: 'Diagram + Text',
    category: 'visual',
    description: 'Diagram on left, text insights on right',
    renderer: 'renderV3DiagramText',
    baseLayout: 'L02',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '0',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content_left: {
        gridRow: '4/18',
        gridColumn: '2/20',
        tag: 'diagram',
        accepts: ['diagram'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingLeft: '5px'
        },
        defaultText: null,
        description: 'Diagram area (900x720px)'
      },
      content_right: {
        gridRow: '4/18',
        gridColumn: '20/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '20px 25px 20px 10px'
        },
        defaultText: 'Key Insights',
        description: 'Text/observations (600x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'visual-diagram-text.svg'
  },

  'V4-infographic-text': {
    id: 'V4-infographic-text',
    name: 'Infographic + Text',
    category: 'visual',
    description: 'Infographic on left, text insights on right',
    renderer: 'renderV4InfographicText',
    baseLayout: 'L02',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '0',
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content_left: {
        gridRow: '4/18',
        gridColumn: '2/20',
        tag: 'infographic',
        accepts: ['infographic'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingLeft: '5px'
        },
        defaultText: null,
        description: 'Infographic area (900x720px)'
      },
      content_right: {
        gridRow: '4/18',
        gridColumn: '20/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '20px 25px 20px 10px'
        },
        defaultText: 'Key Insights',
        description: 'Text/observations (600x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)',
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'visual-infographic-text.svg'
  },

  // ===========================================
  // IMAGE SPLIT TEMPLATES (I Series)
  // Full-height image with content
  // ===========================================

  'I1-image-left': {
    id: 'I1-image-left',
    name: 'Image Left (Wide)',
    category: 'image',
    description: 'Full-height image on left (12 cols), content on right',
    renderer: 'renderI1ImageLeft',
    baseLayout: 'L27',
    themingEnabled: true,
    slots: {
      image: {
        gridRow: '1/19',
        gridColumn: '1/12',
        tag: 'image',
        accepts: ['image'],
        style: {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Full-height image (660x1080px)'
      },
      title: {
        gridRow: '1/3',
        gridColumn: '12/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0px 25px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '12/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          padding: '0px 25px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '12/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '25px 25px'
        },
        defaultText: null,
        description: 'Main content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '12/17',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'image-left-wide.svg'
  },

  'I2-image-right': {
    id: 'I2-image-right',
    name: 'Image Right (Wide)',
    category: 'image',
    description: 'Full-height image on right (12 cols), content on left',
    renderer: 'renderI2ImageRight',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      image: {
        gridRow: '1/19',
        gridColumn: '21/33',
        tag: 'image',
        accepts: ['image'],
        style: {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Full-height image (660x1080px)'
      },
      title: {
        gridRow: '1/3',
        gridColumn: '2/21',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0px 25px 0px 4px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/21',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          padding: '0px 25px 0px 4px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/21',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '25px 25px 25px 4px'
        },
        defaultText: null,
        description: 'Main content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '18/20',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'image-right-wide.svg'
  },

  'I3-image-left-narrow': {
    id: 'I3-image-left-narrow',
    name: 'Image Left (Narrow)',
    category: 'image',
    description: 'Full-height narrow image on left (6 cols), content on right',
    renderer: 'renderI3ImageLeftNarrow',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      image: {
        gridRow: '1/19',
        gridColumn: '1/7',
        tag: 'image',
        accepts: ['image'],
        style: {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Full-height narrow image (330x1080px)'
      },
      title: {
        gridRow: '1/3',
        gridColumn: '7/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0px 25px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '7/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          padding: '0px 25px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '7/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '25px 25px'
        },
        defaultText: null,
        description: 'Main content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '7/12',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'image-left-narrow.svg'
  },

  'I4-image-right-narrow': {
    id: 'I4-image-right-narrow',
    name: 'Image Right (Narrow)',
    category: 'image',
    description: 'Full-height narrow image on right (6 cols), content on left',
    renderer: 'renderI4ImageRightNarrow',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      image: {
        gridRow: '1/19',
        gridColumn: '26/33',
        tag: 'image',
        accepts: ['image'],
        style: {
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Full-height narrow image (330x1080px)'
      },
      title: {
        gridRow: '1/3',
        gridColumn: '2/26',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #111827)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left',
          padding: '0px 25px 0px 4px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/26',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-secondary, #4b5563)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left',
          padding: '0px 25px 0px 4px'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/18',
        gridColumn: '2/26',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '25px 25px 25px 4px'
        },
        defaultText: null,
        description: 'Main content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 14px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '23/25',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'image-right-narrow.svg'
  },

  // ===========================================
  // SPLIT CONTENT TEMPLATES (S Series)
  // ===========================================

  // S1-visual-text REMOVED - replaced by V series (V1-V4)
  // S2-image-content REMOVED - replaced by I series (I1-I4)

  'S3-two-visuals': {
    id: 'S3-two-visuals',
    name: 'Two Visuals',
    category: 'split',
    description: 'Two charts/diagrams/infographics side by side',
    renderer: 'renderS3TwoVisuals',
    baseLayout: 'L03',
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',       // Minimal bottom padding (matches C1)
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'center',   // MIDDLE align (vertical)
          textAlign: 'left',
          padding: '0',               // Reset default 16px to 0
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      content_left: {
        gridRow: '4/14',
        gridColumn: '2/17',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          paddingLeft: '5px'
        },
        defaultText: null,
        description: 'Left visual (840x540px)'
      },
      content_right: {
        gridRow: '4/14',
        gridColumn: '17/32',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Right visual (840x540px)'
      },
      caption_left: {
        gridRow: '14/18',
        gridColumn: '2/17',
        tag: 'body',
        accepts: ['text', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Key Insights 1',
        description: 'Left caption/description'
      },
      caption_right: {
        gridRow: '14/18',
        gridColumn: '17/32',
        tag: 'body',
        accepts: ['text', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          padding: '0',
          paddingTop: '20px',
          paddingLeft: '5px'
        },
        defaultText: 'Key Insights 2',
        description: 'Right caption/description'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'split-two-visuals.svg'
  },

  'S4-comparison': {
    id: 'S4-comparison',
    name: 'Comparison',
    category: 'split',
    description: 'Two columns for comparing items (before/after, pros/cons)',
    renderer: 'renderS4Comparison',
    baseLayout: null,
    themingEnabled: true,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 48px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'flex-end', // BOTTOM align (vertical)
          textAlign: 'left',
          padding: '0',
          paddingBottom: '4px',       // Minimal bottom padding (matches C1)
          paddingLeft: '5px'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-subtitle-size, 32px)',
          fontWeight: 'var(--theme-subtitle-weight, normal)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align (horizontal)
          justifyContent: 'center',   // MIDDLE align (vertical)
          textAlign: 'left',
          padding: '0',               // Reset default 16px to 0
          paddingLeft: '5px'
        },
        defaultText: 'Subtitle'
      },
      header_left: {
        gridRow: '4/5',
        gridColumn: '2/17',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textTransform: 'uppercase',
          paddingLeft: '5px'
        },
        defaultText: 'Option A',
        description: 'Left column header (e.g., "Before", "Option A")'
      },
      header_right: {
        gridRow: '4/5',
        gridColumn: '17/32',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textTransform: 'uppercase',
          paddingLeft: '5px'
        },
        defaultText: 'Option B',
        description: 'Right column header (e.g., "After", "Option B")'
      },
      content_left: {
        gridRow: '5/18',
        gridColumn: '2/17',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Content 1',
        description: 'Left column content'
      },
      content_right: {
        gridRow: '5/18',
        gridColumn: '17/32',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          textAlign: 'left',
          paddingLeft: '5px'
        },
        defaultText: 'Content 2',
        description: 'Right column content'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          paddingLeft: '5px'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)'
        },
        defaultText: null
      }
    },
    defaults: {},
    thumbnail: 'split-comparison.svg'
  },

  // ===========================================
  // BLANK/FREEFORM TEMPLATE
  // ===========================================

  'B1-blank': {
    id: 'B1-blank',
    name: 'Blank Canvas',
    category: 'blank',
    description: 'Empty slide - add elements freely using the toolbar',
    renderer: 'renderB1Blank',
    baseLayout: null,
    slots: {},  // No pre-defined slots - truly blank canvas
    defaults: {},
    thumbnail: 'blank-canvas.svg'
  },

  // ===========================================
  // L-SERIES BACKEND LAYOUTS (Director Service)
  // Added for v7.5.1 UUID Architecture - Element Mapping
  // These layouts are created by the Director Agent and Text Service
  // ===========================================

  'L25': {
    id: 'L25',
    name: 'Main Content Shell',
    category: 'backend',
    description: 'Standard content slide with title, subtitle, and rich content area (Text Service)',
    renderer: 'renderL25',
    baseLayout: null,
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 42px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'content',
        accepts: ['content', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Main content area (Text Service owns)',
        formatOwner: 'text_service'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 18px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: ''
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: ''
      }
    },
    defaults: {
      background_color: 'var(--theme-hero-text-primary, #ffffff)'
    }
  },

  'L29': {
    id: 'L29',
    name: 'Hero Full-Bleed',
    category: 'backend',
    description: 'Full-bleed hero slide for title/section/closing (Text Service)',
    renderer: 'renderL29',
    baseLayout: null,
    slots: {
      hero: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'content',
        accepts: ['content', 'html', 'hero_content'],
        style: {},
        defaultText: '',
        description: 'Full-slide hero content (Text Service owns)',
        formatOwner: 'text_service'
      }
    },
    defaults: {
      background_color: '#1e3a5f'
    }
  },

  'L27': {
    id: 'L27',
    name: 'Image Left with Content Right',
    category: 'backend',
    description: 'Full-height image on left, text content on right',
    renderer: 'renderL27',
    baseLayout: null,
    slots: {
      image: {
        gridRow: '1/19',
        gridColumn: '1/12',
        tag: 'image',
        accepts: ['image'],
        style: {},
        defaultText: '',
        description: 'Full-height image area'
      },
      title: {
        gridRow: '2/3',
        gridColumn: '13/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 42px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '13/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: ''
      },
      text: {
        gridRow: '5/17',
        gridColumn: '13/32',
        tag: 'body',
        accepts: ['text', 'body', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Main text content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '13/18',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 18px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: ''
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: ''
      }
    },
    defaults: {
      background_color: 'var(--theme-hero-text-primary, #ffffff)'
    }
  },

  'L01': {
    id: 'L01',
    name: 'Centered Chart with Text Below',
    category: 'backend',
    description: 'Chart/diagram centered with text below',
    renderer: 'renderL01',
    baseLayout: null,
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 42px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: ''
      },
      chart: {
        gridRow: '5/15',
        gridColumn: '2/32',
        tag: 'content',
        accepts: ['content', 'chart', 'html'],
        style: {},
        defaultText: '',
        description: 'Chart/diagram area (Analytics Service)',
        formatOwner: 'analytics_service'
      },
      body: {
        gridRow: '15/17',
        gridColumn: '2/32',
        tag: 'body',
        accepts: ['text', 'body'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Text below chart'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 18px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: ''
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: ''
      }
    },
    defaults: {
      background_color: 'var(--theme-hero-text-primary, #ffffff)'
    }
  },

  'L02': {
    id: 'L02',
    name: 'Left Diagram with Text Right',
    category: 'backend',
    description: 'Diagram/chart on left, observations/text on right',
    renderer: 'renderL02',
    baseLayout: null,
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 42px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: ''
      },
      diagram: {
        gridRow: '5/17',
        gridColumn: '2/23',
        tag: 'content',
        accepts: ['content', 'diagram', 'chart', 'html'],
        style: {},
        defaultText: '',
        description: 'Diagram/chart area (1260x720px)',
        formatOwner: 'analytics_service'
      },
      text: {
        gridRow: '5/17',
        gridColumn: '23/32',
        tag: 'body',
        accepts: ['text', 'body', 'html'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Observations/text area (540x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 18px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: ''
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: ''
      }
    },
    defaults: {
      background_color: 'var(--theme-hero-text-primary, #ffffff)'
    }
  },

  'L03': {
    id: 'L03',
    name: 'Two Charts in Columns',
    category: 'backend',
    description: 'Two charts side by side with text below each',
    renderer: 'renderL03',
    baseLayout: null,
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-title-size, 42px)',
          fontWeight: 'var(--theme-title-weight, bold)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-body-size, 24px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-footer-text, #6b7280)'
        },
        defaultText: ''
      },
      chart1: {
        gridRow: '5/14',
        gridColumn: '2/16',
        tag: 'content',
        accepts: ['content', 'chart', 'html'],
        style: {},
        defaultText: '',
        description: 'Left chart area',
        formatOwner: 'analytics_service'
      },
      chart2: {
        gridRow: '5/14',
        gridColumn: '17/31',
        tag: 'content',
        accepts: ['content', 'chart', 'html'],
        style: {},
        defaultText: '',
        description: 'Right chart area',
        formatOwner: 'analytics_service'
      },
      body_left: {
        gridRow: '14/17',
        gridColumn: '2/16',
        tag: 'body',
        accepts: ['text', 'body'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Left text below chart'
      },
      body_right: {
        gridRow: '14/17',
        gridColumn: '17/31',
        tag: 'body',
        accepts: ['text', 'body'],
        style: {
          fontSize: 'var(--theme-body-size, 20px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-body, #374151)'
        },
        defaultText: '',
        description: 'Right text below chart'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: 'var(--theme-footer-size, 18px)',
          fontFamily: 'var(--theme-font-family, Poppins, sans-serif)',
          color: 'var(--theme-text-primary, #1f2937)'
        },
        defaultText: ''
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {},
        defaultText: ''
      }
    },
    defaults: {
      background_color: 'var(--theme-hero-text-primary, #ffffff)'
    }
  }
};

// ===========================================
// TEMPLATE CATEGORIES FOR UI
// ===========================================

const TEMPLATE_CATEGORIES = {
  hero: {
    name: 'Hero Slides',
    description: 'Full-bleed title, section, and closing slides',
    templates: ['H1-generated', 'H1-structured', 'H2-section', 'H3-closing']
  },
  content: {
    name: 'Content Slides',
    description: 'Single content area slides',
    templates: ['C1-text', 'C3-chart', 'C4-infographic', 'C5-diagram']
  },
  visual: {
    name: 'Visual + Text',
    description: 'Visual element on left with text insights on right',
    templates: ['V1-image-text', 'V2-chart-text', 'V3-diagram-text', 'V4-infographic-text']
  },
  image: {
    name: 'Image Split',
    description: 'Full-height image with content area',
    templates: ['I1-image-left', 'I2-image-right', 'I3-image-left-narrow', 'I4-image-right-narrow']
  },
  split: {
    name: 'Split Layout Slides',
    description: 'Two-column and multi-element layouts',
    templates: ['S3-two-visuals', 'S4-comparison']
  },
  blank: {
    name: 'Blank',
    description: 'Start from scratch',
    templates: ['B1-blank']
  }
};

// ===========================================
// HELPER FUNCTIONS
// ===========================================

/**
 * Get template definition by ID
 */
function getTemplate(templateId) {
  return TEMPLATE_REGISTRY[templateId] || null;
}

/**
 * Get all templates in a category
 */
function getTemplatesByCategory(category) {
  const categoryDef = TEMPLATE_CATEGORIES[category];
  if (!categoryDef) return [];
  return categoryDef.templates.map(id => TEMPLATE_REGISTRY[id]).filter(Boolean);
}

/**
 * Get all template IDs
 */
function getAllTemplateIds() {
  return Object.keys(TEMPLATE_REGISTRY);
}

/**
 * Check if a slot accepts a given content type
 */
function slotAccepts(templateId, slotName, contentType) {
  const template = TEMPLATE_REGISTRY[templateId];
  if (!template || !template.slots[slotName]) return false;
  const accepts = template.slots[slotName].accepts;
  return accepts.includes(contentType) || accepts.includes('any');
}

// Export for browser
if (typeof window !== 'undefined') {
  window.TEMPLATE_REGISTRY = TEMPLATE_REGISTRY;
  window.TEMPLATE_CATEGORIES = TEMPLATE_CATEGORIES;
  window.getTemplate = getTemplate;
  window.getTemplatesByCategory = getTemplatesByCategory;
  window.getAllTemplateIds = getAllTemplateIds;
  window.slotAccepts = slotAccepts;
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    TEMPLATE_REGISTRY,
    TEMPLATE_CATEGORIES,
    getTemplate,
    getTemplatesByCategory,
    getAllTemplateIds,
    slotAccepts
  };
}
