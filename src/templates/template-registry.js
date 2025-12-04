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
    baseLayout: null, // New renderer
    slots: {
      background: {
        gridRow: '1/19',
        gridColumn: '1/33',
        tag: 'background',
        accepts: ['image', 'color', 'gradient'],
        description: 'Background image or color'
      },
      title: {
        gridRow: '7/10',
        gridColumn: '3/31',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '72px',
          fontWeight: 'bold',
          color: '#ffffff',
          textAlign: 'center',
          textShadow: '0 2px 4px rgba(0,0,0,0.3)'
        },
        description: 'Main presentation title'
      },
      subtitle: {
        gridRow: '10/12',
        gridColumn: '5/29',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '32px',
          fontWeight: 'normal',
          color: '#e5e7eb',
          textAlign: 'center'
        },
        description: 'Subtitle or tagline'
      },
      footer: {
        gridRow: '16/18',
        gridColumn: '3/15',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          color: '#d1d5db'
        },
        description: 'Date, presenter name, or other info'
      },
      logo: {
        gridRow: '16/18',
        gridColumn: '28/31',
        tag: 'logo',
        accepts: ['image', 'emoji'],
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
        accepts: ['image', 'color', 'gradient']
      },
      section_number: {
        gridRow: '6/8',
        gridColumn: '3/31',
        tag: 'section_number',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          fontWeight: '600',
          color: '#9ca3af',
          textAlign: 'center',
          textTransform: 'uppercase',
          letterSpacing: '4px'
        },
        description: 'Section number (e.g., "SECTION 01")'
      },
      title: {
        gridRow: '8/11',
        gridColumn: '3/31',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '56px',
          fontWeight: 'bold',
          color: '#ffffff',
          textAlign: 'center'
        },
        description: 'Section title'
      },
      subtitle: {
        gridRow: '11/13',
        gridColumn: '5/29',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#d1d5db',
          textAlign: 'center'
        },
        description: 'Optional section description'
      }
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
        accepts: ['image', 'color', 'gradient']
      },
      title: {
        gridRow: '6/9',
        gridColumn: '3/31',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '64px',
          fontWeight: 'bold',
          color: '#ffffff',
          textAlign: 'center'
        },
        description: 'Closing message (e.g., "Thank You")'
      },
      subtitle: {
        gridRow: '9/11',
        gridColumn: '5/29',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          color: '#e5e7eb',
          textAlign: 'center'
        },
        description: 'Additional message or call to action'
      },
      contact_info: {
        gridRow: '13/16',
        gridColumn: '8/26',
        tag: 'contact',
        accepts: ['text', 'html'],
        style: {
          fontSize: '20px',
          color: '#d1d5db',
          textAlign: 'center',
          lineHeight: '1.8'
        },
        description: 'Contact details, website, social links'
      },
      logo: {
        gridRow: '16/18',
        gridColumn: '14/20',
        tag: 'logo',
        accepts: ['image', 'emoji'],
        style: {
          textAlign: 'center'
        },
        description: 'Company logo (centered)'
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937',
          lineHeight: '1.2'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280',
          lineHeight: '1.4',
          marginTop: '8px'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'body',
        accepts: ['body', 'html'],
        style: {
          fontSize: '20px',
          color: '#374151',
          lineHeight: '1.6'
        },
        description: 'Main text content area (1800x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
      }
    },
    defaults: {},
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'table',
        accepts: ['table', 'html'],
        description: 'Table content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
      }
    },
    defaults: {},
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'chart',
        accepts: ['chart'],
        description: 'Chart placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'infographic',
        accepts: ['infographic'],
        description: 'Infographic placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
    slots: {
      title: {
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'diagram',
        accepts: ['diagram'],
        description: 'Diagram placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
      }
    },
    defaults: {},
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '2/32',
        tag: 'image',
        accepts: ['image'],
        description: 'Image placeholder area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
      }
    },
    defaults: {},
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content_left: {
        gridRow: '5/17',
        gridColumn: '2/17',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        description: 'Visual element (900x720px)'
      },
      content_right: {
        gridRow: '5/17',
        gridColumn: '18/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: '20px',
          color: '#374151',
          lineHeight: '1.6'
        },
        description: 'Text/observations (840x720px)'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
        description: 'Full-height image (660x1080px)'
      },
      title: {
        gridRow: '2/3',
        gridColumn: '13/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '13/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content: {
        gridRow: '5/17',
        gridColumn: '13/32',
        tag: 'body',
        accepts: ['body', 'table', 'html'],
        style: {
          fontSize: '20px',
          color: '#374151',
          lineHeight: '1.6'
        },
        description: 'Main content area'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '13/18',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      content_left: {
        gridRow: '5/14',
        gridColumn: '2/16',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        description: 'Left visual (840x540px)'
      },
      content_right: {
        gridRow: '5/14',
        gridColumn: '17/31',
        tag: 'visual',
        accepts: ['chart', 'infographic', 'diagram', 'image'],
        description: 'Right visual (840x540px)'
      },
      caption_left: {
        gridRow: '14/17',
        gridColumn: '2/16',
        tag: 'body',
        accepts: ['text', 'html'],
        style: {
          fontSize: '18px',
          color: '#374151'
        },
        description: 'Left caption/description'
      },
      caption_right: {
        gridRow: '14/17',
        gridColumn: '17/31',
        tag: 'body',
        accepts: ['text', 'html'],
        style: {
          fontSize: '18px',
          color: '#374151'
        },
        description: 'Right caption/description'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        }
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        }
      },
      header_left: {
        gridRow: '5/6',
        gridColumn: '2/16',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontWeight: '600',
          color: '#1f2937',
          textAlign: 'center'
        },
        description: 'Left column header (e.g., "Before", "Option A")'
      },
      header_right: {
        gridRow: '5/6',
        gridColumn: '17/31',
        tag: 'header',
        accepts: ['text'],
        style: {
          fontSize: '28px',
          fontWeight: '600',
          color: '#1f2937',
          textAlign: 'center'
        },
        description: 'Right column header (e.g., "After", "Option B")'
      },
      content_left: {
        gridRow: '6/17',
        gridColumn: '2/16',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        description: 'Left column content'
      },
      content_right: {
        gridRow: '6/17',
        gridColumn: '17/31',
        tag: 'body',
        accepts: ['body', 'table', 'html', 'image', 'chart'],
        description: 'Right column content'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        }
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji']
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
        gridRow: '2/3',
        gridColumn: '2/32',
        tag: 'title',
        accepts: ['text'],
        style: {
          fontSize: '42px',
          fontWeight: 'bold',
          color: '#1f2937'
        },
        optional: true
      },
      subtitle: {
        gridRow: '3/4',
        gridColumn: '2/32',
        tag: 'subtitle',
        accepts: ['text'],
        style: {
          fontSize: '24px',
          color: '#6b7280'
        },
        optional: true
      },
      canvas: {
        gridRow: '4/18',
        gridColumn: '1/33',
        tag: 'canvas',
        accepts: ['any'],
        description: 'Freeform content area - insert elements anywhere'
      },
      footer: {
        gridRow: '18/19',
        gridColumn: '2/7',
        tag: 'footer',
        accepts: ['text'],
        style: {
          fontSize: '18px',
          fontWeight: '500',
          color: '#1f2937'
        },
        optional: true
      },
      logo: {
        gridRow: '17/19',
        gridColumn: '30/32',
        tag: 'logo',
        accepts: ['image', 'emoji'],
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
