# Text Service Requirements for Layout Builder v7.5

This document specifies the API requirements for Text Service to integrate with Layout Builder's world-class editor features.

## Overview

Layout Builder needs Text Service to provide:
1. **AI-generated rich text content** for slide sections (updateSectionContent API)
2. **Theme-aligned HTML tables** for insertion (insertTable API)
3. **Formatted text blocks** for various layout zones

---

## API 1: Generate Section Content

### Purpose
Generate or regenerate text content for a specific slide section based on AI prompts.

### Endpoint Suggestion
```
POST /api/text/generate-section
```

### Request Format
```typescript
{
  presentationId: string,
  slideIndex: number,
  sectionId: string,           // e.g., 'slide-0-section-content'
  sectionType: 'title' | 'subtitle' | 'content' | 'hero' | 'bullet_list' | 'numbered_list',
  prompt: string,              // User prompt or AI instruction
  context?: {
    slideTitle?: string,       // Current slide title for context
    presentationTheme?: string,// Overall theme
    previousContent?: string,  // Existing content to improve/replace
    tone?: 'professional' | 'casual' | 'technical' | 'creative',
    maxLength?: number         // Character limit
  },
  theme: {
    primaryColor: string,      // e.g., '#1e40af'
    secondaryColor: string,
    fontFamily: string,        // e.g., 'Inter, sans-serif'
    fontSize: {
      title: string,           // e.g., '42px'
      subtitle: string,
      body: string,
      caption: string
    }
  }
}
```

### Response Format
```typescript
{
  success: boolean,
  content: string,             // HTML content ready to inject
  contentType: 'html',
  metadata?: {
    wordCount: number,
    characterCount: number,
    estimatedReadTime: string  // e.g., '30 seconds'
  },
  error?: string
}
```

### HTML Output Requirements

**Content must be:**
1. **Self-contained HTML** - No external CSS dependencies
2. **Inline-styled** - All styles via `style` attribute
3. **Theme-aligned** - Use provided color/font values
4. **Sanitized** - No script tags or event handlers
5. **Responsive** - Use relative units (%, em, rem) where appropriate

**Example Output:**
```html
<div style="font-family: Inter, sans-serif; color: #1f2937;">
  <h3 style="font-size: 24px; font-weight: 600; color: #1e40af; margin-bottom: 16px;">
    Key Insights
  </h3>
  <ul style="font-size: 18px; line-height: 1.6; padding-left: 24px;">
    <li style="margin-bottom: 12px;">First insight point</li>
    <li style="margin-bottom: 12px;">Second insight point</li>
    <li style="margin-bottom: 12px;">Third insight point</li>
  </ul>
</div>
```

---

## API 2: Generate Table HTML

### Purpose
Generate theme-aligned HTML tables for insertion into slides.

### Endpoint Suggestion
```
POST /api/text/generate-table
```

### Request Format
```typescript
{
  presentationId: string,
  tableSpec: {
    rows: number,              // 1-20
    cols: number,              // 1-10
    headerRow: boolean,        // First row is header
    data?: string[][],         // Optional initial data
    prompt?: string            // AI prompt to generate data (if data not provided)
  },
  dimensions: {
    width: string,             // e.g., '100%', '800px'
    maxHeight?: string         // e.g., '400px' (scrollable if exceeded)
  },
  theme: {
    primaryColor: string,
    secondaryColor: string,
    fontFamily: string,
    headerBackground: string,  // e.g., '#1e40af'
    headerTextColor: string,   // e.g., '#ffffff'
    rowBackground: string,     // e.g., '#ffffff'
    alternateRowBackground?: string, // e.g., '#f9fafb'
    borderColor: string,       // e.g., '#e5e7eb'
    fontSize: string           // e.g., '16px'
  },
  options?: {
    striped: boolean,          // Alternate row colors
    hoverable: boolean,        // Hover effect (CSS :hover)
    compact: boolean,          // Reduced padding
    editable: boolean          // Add contenteditable to cells
  }
}
```

### Response Format
```typescript
{
  success: boolean,
  tableHtml: string,           // Complete HTML table
  tableId: string,             // Unique ID for the table
  dimensions: {
    rows: number,
    cols: number,
    estimatedHeight: string    // e.g., '320px'
  },
  error?: string
}
```

### HTML Output Requirements

**Table HTML must:**
1. Use `<table>` element with `border-collapse: collapse`
2. Include `<thead>` and `<tbody>` if headerRow is true
3. Use `<th>` for header cells, `<td>` for data cells
4. Apply all styles inline
5. Be responsive (use `width: 100%` by default)
6. Support `contenteditable="true"` if editable option is true

**Example Output:**
```html
<table id="table-abc123" style="width: 100%; border-collapse: collapse; font-family: Inter, sans-serif; font-size: 16px;">
  <thead>
    <tr>
      <th style="background: #1e40af; color: #ffffff; padding: 12px 16px; text-align: left; font-weight: 600; border: 1px solid #e5e7eb;">
        Quarter
      </th>
      <th style="background: #1e40af; color: #ffffff; padding: 12px 16px; text-align: left; font-weight: 600; border: 1px solid #e5e7eb;">
        Revenue
      </th>
      <th style="background: #1e40af; color: #ffffff; padding: 12px 16px; text-align: left; font-weight: 600; border: 1px solid #e5e7eb;">
        Growth
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td contenteditable="true" style="background: #ffffff; padding: 12px 16px; border: 1px solid #e5e7eb;">Q1 2024</td>
      <td contenteditable="true" style="background: #ffffff; padding: 12px 16px; border: 1px solid #e5e7eb;">$2.4M</td>
      <td contenteditable="true" style="background: #ffffff; padding: 12px 16px; border: 1px solid #e5e7eb;">+15%</td>
    </tr>
    <tr>
      <td contenteditable="true" style="background: #f9fafb; padding: 12px 16px; border: 1px solid #e5e7eb;">Q2 2024</td>
      <td contenteditable="true" style="background: #f9fafb; padding: 12px 16px; border: 1px solid #e5e7eb;">$2.8M</td>
      <td contenteditable="true" style="background: #f9fafb; padding: 12px 16px; border: 1px solid #e5e7eb;">+17%</td>
    </tr>
  </tbody>
</table>
```

---

## API 3: Improve/Rewrite Content

### Purpose
Improve, expand, or rewrite existing text content.

### Endpoint Suggestion
```
POST /api/text/improve
```

### Request Format
```typescript
{
  content: string,             // Existing content (HTML or plain text)
  contentType: 'html' | 'text',
  action: 'improve' | 'expand' | 'simplify' | 'formalize' | 'casualize' | 'summarize' | 'bulletize',
  instructions?: string,       // Additional instructions
  theme: { /* same as above */ }
}
```

### Response Format
```typescript
{
  success: boolean,
  content: string,             // Improved HTML content
  changes: string[],           // List of changes made
  error?: string
}
```

---

## Layout Builder Integration

### How Layout Builder Will Use These APIs

1. **updateSectionContent** postMessage handler:
   - Frontend calls `updateSectionContent` with sectionId and content
   - Content comes from Text Service `generate-section` API
   - Layout Builder injects HTML into the section's innerHTML

2. **insertTable** postMessage handler:
   - Frontend calls `insertTable` with position and tableHtml
   - tableHtml comes from Text Service `generate-table` API
   - Layout Builder creates positioned container and injects table

3. **AI Regeneration Panel** (existing feature):
   - Uses `improve` API to regenerate selected sections
   - Calls Layout Builder's `updateSectionContent` to inject result

### Response Time Expectations

| API | Expected Response Time | Max Response Time |
|-----|----------------------|-------------------|
| generate-section | < 3s | 10s |
| generate-table | < 2s | 5s |
| improve | < 3s | 10s |

---

## Theme Integration

### Layout Builder Theme Data

Layout Builder will provide theme data in requests. The theme object structure:

```typescript
interface Theme {
  primaryColor: string;        // Main brand color
  secondaryColor: string;      // Accent color
  backgroundColor: string;     // Slide background
  textColor: string;           // Primary text color
  fontFamily: string;          // Font stack
  fontSize: {
    title: string;             // 42px default
    subtitle: string;          // 28px default
    body: string;              // 18px default
    caption: string;           // 14px default
  };
  spacing: {
    paragraph: string;         // 16px default
    section: string;           // 32px default
  };
}
```

### Color Format
- All colors in hex format: `#RRGGBB` or `#RRGGBBAA`
- No named colors (red, blue, etc.)
- No RGB/HSL formats

---

## Error Handling

### Error Response Format
```typescript
{
  success: false,
  error: string,               // Human-readable error message
  errorCode: string,           // Machine-readable code
  details?: object             // Additional debug info
}
```

### Error Codes
| Code | Meaning |
|------|---------|
| `INVALID_REQUEST` | Request validation failed |
| `GENERATION_FAILED` | AI generation failed |
| `RATE_LIMITED` | Too many requests |
| `CONTENT_TOO_LONG` | Generated content exceeds limits |
| `INVALID_THEME` | Theme object malformed |

---

## Security Considerations

1. **HTML Sanitization**: All generated HTML must be sanitized
   - No `<script>` tags
   - No `on*` event handlers
   - No `javascript:` URLs
   - No `<iframe>` or `<object>` tags

2. **Content Validation**: Validate all user-provided content before processing

3. **Rate Limiting**: Implement rate limiting per presentation/user

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial specification |

---

## Contact

For questions about these requirements, contact the Layout Builder team.
