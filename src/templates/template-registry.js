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
      background_color: '#1f2937'
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
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',
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
          fontSize: '32px',
          fontFamily: 'Poppins, sans-serif',
          color: '#94a3b8',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',    // LEFT (horizontal cross-axis)
          justifyContent: 'flex-start', // TOP (vertical main-axis)
          textAlign: 'left'
        },
        defaultText: 'Presentation Subtitle',
        description: 'Subtitle or tagline'
      },
      footer: {
        gridRow: '16/18',
        gridColumn: '3/17',  // LEFT HALF (was 3/15)
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '26px',  // (was 18px)
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',              // White text for hero slide
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',      // LEFT (horizontal)
          justifyContent: 'flex-start',  // TOP (vertical)
          textAlign: 'left',
          textTransform: 'uppercase'
        },
        defaultText: 'AUTHOR | DATE',
        description: 'Date, presenter name, or other info'
      },
      logo: {
        gridRow: '16/18',
        gridColumn: '28/31',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          fontWeight: 'bold',
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
          fontSize: '180px',  // Large section number
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',
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
          fontSize: '64px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',
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
      background_color: '#374151'
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
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',
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
          fontSize: '32px',
          fontFamily: 'Poppins, sans-serif',
          color: '#94a3b8',
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
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#ffffff',
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
          fontSize: '20px',
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
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',           // Dark for content slides
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align
          justifyContent: 'flex-end', // BOTTOM align
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',           // Medium gray for subtitle
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',   // LEFT align
          justifyContent: 'flex-start', // TOP align
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'body',
        accepts: ['body', 'html'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',           // Body text gray
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '20px 0px'
        },
        defaultText: 'Content Area',
        description: 'Main text content area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',           // Light gray for footer
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-text.svg'
  },

  'C2-table': {
    id: 'C2-table',
    name: 'Table Slide',
    category: 'content',
    description: 'Slide with data table',
    renderer: 'renderC2Table',
    baseLayout: 'L25',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'table',
        accepts: ['table', 'html'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left',
          padding: '20px 0px'
        },
        defaultText: 'Table Area',
        description: 'Table content area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-table.svg'
  },

  'C3-chart': {
    id: 'C3-chart',
    name: 'Single Chart',
    category: 'content',
    description: 'Slide with one chart visualization',
    renderer: 'renderC3Chart',
    baseLayout: 'L25',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'chart',
        accepts: ['chart'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '20px 0px'
        },
        defaultText: 'Chart Area',
        description: 'Chart placeholder area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-chart.svg'
  },

  'C4-infographic': {
    id: 'C4-infographic',
    name: 'Single Infographic',
    category: 'content',
    description: 'Slide with one infographic',
    renderer: 'renderC4Infographic',
    baseLayout: 'L25',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'infographic',
        accepts: ['infographic'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '20px 0px'
        },
        defaultText: 'Infographic Area',
        description: 'Infographic placeholder area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-infographic.svg'
  },

  'C5-diagram': {
    id: 'C5-diagram',
    name: 'Single Diagram',
    category: 'content',
    description: 'Slide with one diagram',
    renderer: 'renderC5Diagram',
    baseLayout: 'L25',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'diagram',
        accepts: ['diagram'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '20px 0px'
        },
        defaultText: 'Diagram Area',
        description: 'Diagram placeholder area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-diagram.svg'
  },

  'C6-image': {
    id: 'C6-image',
    name: 'Single Image',
    category: 'content',
    description: 'Slide with one image and optional caption',
    renderer: 'renderC6Image',
    baseLayout: 'L25',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontWeight: 'bold',
          fontFamily: 'Poppins, sans-serif',
          color: '#111827',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-end',
          textAlign: 'left'
        },
        defaultText: 'Slide Title'
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontFamily: 'Poppins, sans-serif',
          color: '#4b5563',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'flex-start',
          textAlign: 'left'
        },
        defaultText: 'Subtitle'
      },
      content: {
        gridRow: '4/17',
        gridColumn: '2/32',
        tag: 'image',
        accepts: ['image'],
        style: {
          fontSize: '24px',
          fontFamily: 'Poppins, sans-serif',
          color: '#374151',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '20px 0px'
        },
        defaultText: 'Image Area',
        description: 'Image placeholder area'
      },
      footer: {
        gridRow: '17/19',
        gridColumn: '2/10',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '14px',
          fontFamily: 'Poppins, sans-serif',
          color: '#6b7280',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          justifyContent: 'center',
          textAlign: 'left'
        },
        defaultText: 'Footer'
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {
      background_color: '#ffffff'
    },
    thumbnail: 'content-image.svg'
  },

  // ===========================================
  // SPLIT CONTENT TEMPLATES
  // ===========================================

  'S1-visual-text': {
    id: 'S1-visual-text',
    name: 'Visual + Text',
    category: 'split',
    description: 'Chart/Infographic/Diagram on left, text on right',
    renderer: 'renderS1VisualText',
    baseLayout: 'L02',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      content_left: {
        gridRow: '4/18',
        gridColumn: '2/20',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        style: {
          fontSize: '24px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Visual element (900x720px)'
      },
      content_right: {
        gridRow: '4/18',
        gridColumn: '20/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: '24px',
          textAlign: 'left',
          padding: '25px 25px'
        },
        defaultText: 'Key Insights',
        description: 'Text/observations (840x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {},
        defaultText: null
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
    thumbnail: 'split-visual-text.svg'
  },

  'S2-image-content': {
    id: 'S2-image-content',
    name: 'Image + Content',
    category: 'split',
    description: 'Full-height image on left, content on right',
    renderer: 'renderS2ImageContent',
    baseLayout: 'L27',
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
          fontSize: '48px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          justifyContent: 'flex-start',
          padding: '0px 25px'
        },
        defaultText: null
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '12/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start',
          padding: '0px 25px'
        },
        defaultText: null
      },
      content: {
        gridRow: '4/18',
        gridColumn: '12/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: '24px',
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
        style: {},
        defaultText: null
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px'
        },
        defaultText: 'Logo'
      }
    },
    defaults: {},
    thumbnail: 'split-image-content.svg'
  },

  'S3-two-visuals': {
    id: 'S3-two-visuals',
    name: 'Two Visuals',
    category: 'split',
    description: 'Two charts/diagrams/infographics side by side',
    renderer: 'renderS3TwoVisuals',
    baseLayout: 'L03',
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      content_left: {
        gridRow: '4/14',
        gridColumn: '2/17',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        style: {
          fontSize: '24px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
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
          fontSize: '24px',
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
          fontSize: '24px',
          textAlign: 'left',
          padding: '10px 10px'
        },
        defaultText: null,
        description: 'Left caption/description'
      },
      caption_right: {
        gridRow: '14/18',
        gridColumn: '17/32',
        tag: 'body',
        accepts: ['text', 'html'],
        style: {
          fontSize: '24px',
          textAlign: 'left',
          padding: '10px 10px'
        },
        defaultText: null,
        description: 'Right caption/description'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {},
        defaultText: null
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
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null
      },
      header_left: {
        gridRow: '4/5',
        gridColumn: '2/17',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          textTransform: 'uppercase'
        },
        defaultText: null,
        description: 'Left column header (e.g., "Before", "Option A")'
      },
      header_right: {
        gridRow: '4/5',
        gridColumn: '17/32',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          textTransform: 'uppercase'
        },
        defaultText: null,
        description: 'Right column header (e.g., "After", "Option B")'
      },
      content_left: {
        gridRow: '5/18',
        gridColumn: '2/17',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        style: {
          fontSize: '24px',
          textAlign: 'left'
        },
        defaultText: null,
        description: 'Left column content'
      },
      content_right: {
        gridRow: '5/18',
        gridColumn: '17/32',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        style: {
          fontSize: '24px',
          textAlign: 'left'
        },
        defaultText: null,
        description: 'Right column content'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {},
        defaultText: null
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px'
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
    description: 'Empty slide - place elements freely',
    renderer: 'renderB1Blank',
    baseLayout: null,
    slots: {
      title: {
        gridRow: '1/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '48px',
          fontFamily: 'Poppins, sans-serif',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null,
        optional: true
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'flex-start'
        },
        defaultText: null,
        optional: true
      },
      canvas: {
        gridRow: '4/18',
        gridColumn: '2/32',
        tag: 'canvas',
        accepts: ['any'],
        style: {
          fontSize: '24px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center'
        },
        defaultText: null,
        description: 'Freeform content area - insert elements anywhere'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {},
        defaultText: null,
        optional: true
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          fontSize: '20px'
        },
        defaultText: 'Logo',
        optional: true
      }
    },
    defaults: {},
    thumbnail: 'blank-canvas.svg'
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
    templates: ['C1-text', 'C2-table', 'C3-chart', 'C4-infographic', 'C5-diagram', 'C6-image']
  },
  split: {
    name: 'Split Layout Slides',
    description: 'Two-column and multi-element layouts',
    templates: ['S1-visual-text', 'S2-image-content', 'S3-two-visuals', 'S4-comparison']
  },
  blank: {
    name: 'Blank',
    description: 'Start from scratch',
    templates: ['B1-blank']
  }
};

// ===========================================
// SLOT STYLE DEFAULTS (for theming)
// ===========================================

const SLOT_STYLE_DEFAULTS = {
  // Standard slide styles
  standard: {
    title: {
      fontSize: '42px',
      fontWeight: 'bold',
      color: '#1f2937',
      lineHeight: '1.2'
    },
    subtitle: {
      fontSize: '24px',
      fontWeight: 'normal',
      color: '#6b7280',
      lineHeight: '1.4'
    },
    body: {
      fontSize: '20px',
      color: '#374151',
      lineHeight: '1.6'
    },
    footer: {
      fontSize: '18px',
      fontWeight: '500',
      color: '#1f2937'
    }
  },
  // Hero slide styles (larger, usually light text on dark)
  hero: {
    title: {
      fontSize: '72px',
      fontWeight: 'bold',
      color: '#ffffff',
      textShadow: '0 2px 4px rgba(0,0,0,0.3)'
    },
    subtitle: {
      fontSize: '32px',
      fontWeight: 'normal',
      color: '#e5e7eb'
    },
    footer: {
      fontSize: '18px',
      color: '#d1d5db'
    }
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
  window.SLOT_STYLE_DEFAULTS = SLOT_STYLE_DEFAULTS;
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
    SLOT_STYLE_DEFAULTS,
    getTemplate,
    getTemplatesByCategory,
    getAllTemplateIds,
    slotAccepts
  };
}
