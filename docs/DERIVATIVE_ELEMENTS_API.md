# Derivative Elements API - Frontend Integration Guide

## Overview

**Derivative Elements** are presentation-level elements that appear consistently across all slides:
- **Footer**: Template-based text with variables like `{title}`, `{page}`, `{date}`
- **Logo**: Single image that displays on all slides in the logo slot

Unlike regular slide content, derivative elements are:
- **Set once, applied everywhere** - edit on any slide updates all slides
- **Presentation-level** - stored at the presentation level, not per-slide
- **Auto-synced** - changes instantly reflect across all slides

---

## Data Models

### DerivativeElements
```typescript
interface DerivativeElements {
  footer?: FooterConfig | null;
  logo?: LogoConfig | null;
}
```

### FooterConfig
```typescript
interface FooterConfig {
  template: string;       // Template with variables: "{title} | Page {page}"
  values: {               // Variable values
    title?: string;       // e.g., "Q4 Business Review"
    date?: string;        // e.g., "December 2024"
    author?: string;      // e.g., "John Smith"
  };
  style?: {               // Optional style overrides
    color?: string;
    fontSize?: string;
    fontFamily?: string;
    // ... any CSS properties
  } | null;
}
```

**Supported Template Variables:**
| Variable | Source | Description |
|----------|--------|-------------|
| `{title}` | `values.title` | Presentation title |
| `{page}` | Auto-calculated | Current slide number (1-based) |
| `{total}` | Auto-calculated | Total slide count |
| `{date}` | `values.date` | Date string |
| `{author}` | `values.author` | Author name |

### LogoConfig
```typescript
interface LogoConfig {
  image_url: string | null;  // Logo image URL
  alt_text?: string;         // Alt text (default: "Logo")
}
```

---

## PostMessage API Reference

All commands follow the standard postMessage pattern:

```javascript
// Send command
iframe.contentWindow.postMessage({
  action: 'commandName',
  params: { /* parameters */ }
}, iframeOrigin);

// Receive response
window.addEventListener('message', (event) => {
  const { success, action, error, ...data } = event.data;
  // Handle response
});
```

---

### 1. Get Derivative Elements

Get the current footer and logo configuration.

**Action:** `getDerivativeElements`

**Parameters:** None

**Response:**
```javascript
{
  success: true,
  action: 'getDerivativeElements',
  derivativeElements: {
    footer: { template: "...", values: {...}, style: {...} } | null,
    logo: { image_url: "...", alt_text: "..." } | null
  } | null,
  message?: 'No derivative elements configured'
}
```

**Example:**
```javascript
iframe.contentWindow.postMessage({
  action: 'getDerivativeElements'
}, iframeOrigin);
```

---

### 2. Update Derivative Elements

Update footer and/or logo configuration. Changes are persisted to the database and synced across all slides.

**Action:** `updateDerivativeElements`

**Parameters:**
```typescript
{
  presentationId?: string;  // Optional, uses current if not provided
  footer?: FooterConfig | null;  // Set to null to clear footer
  logo?: LogoConfig | null;      // Set to null to clear logo
}
```

**Response:**
```javascript
{
  success: true,
  action: 'updateDerivativeElements',
  derivativeElements: { /* updated config */ },
  message: 'Derivative elements updated and synced across all slides'
}
```

**Examples:**

```javascript
// Set footer only
iframe.contentWindow.postMessage({
  action: 'updateDerivativeElements',
  params: {
    footer: {
      template: '{title} | Page {page} of {total}',
      values: {
        title: 'Q4 Business Review'
      }
    }
  }
}, iframeOrigin);

// Set logo only
iframe.contentWindow.postMessage({
  action: 'updateDerivativeElements',
  params: {
    logo: {
      image_url: 'https://storage.example.com/logo.png',
      alt_text: 'Company Logo'
    }
  }
}, iframeOrigin);

// Set both footer and logo
iframe.contentWindow.postMessage({
  action: 'updateDerivativeElements',
  params: {
    footer: {
      template: '{title} | {date}',
      values: {
        title: 'Annual Report',
        date: 'December 2024'
      },
      style: {
        color: '#6b7280',
        fontSize: '14px'
      }
    },
    logo: {
      image_url: 'https://storage.example.com/company-logo.png'
    }
  }
}, iframeOrigin);

// Clear footer (keep logo)
iframe.contentWindow.postMessage({
  action: 'updateDerivativeElements',
  params: {
    footer: null
  }
}, iframeOrigin);
```

---

### 3. Clear Derivative Elements

Remove footer and/or logo configuration entirely.

**Action:** `clearDerivativeElements`

**Parameters:**
```typescript
{
  presentationId?: string;  // Optional, uses current if not provided
  clearFooter?: boolean;    // Default: true
  clearLogo?: boolean;      // Default: true
}
```

**Response:**
```javascript
{
  success: true,
  action: 'clearDerivativeElements',
  derivativeElements: null | { /* remaining config */ },
  message?: 'Derivative elements cleared'
}
```

**Examples:**

```javascript
// Clear both footer and logo
iframe.contentWindow.postMessage({
  action: 'clearDerivativeElements'
}, iframeOrigin);

// Clear only footer
iframe.contentWindow.postMessage({
  action: 'clearDerivativeElements',
  params: {
    clearFooter: true,
    clearLogo: false
  }
}, iframeOrigin);

// Clear only logo
iframe.contentWindow.postMessage({
  action: 'clearDerivativeElements',
  params: {
    clearFooter: false,
    clearLogo: true
  }
}, iframeOrigin);
```

---

### 4. Sync Derivative Elements

Re-render footer/logo slots across all slides without making an API call. Useful after local changes or when you want to refresh the display.

**Action:** `syncDerivativeElements`

**Parameters:** None

**Response:**
```javascript
{
  success: true,
  action: 'syncDerivativeElements',
  message: 'Synced derivative elements across 12 slides',
  derivativeElements: { /* current config */ }
}
```

**Example:**
```javascript
iframe.contentWindow.postMessage({
  action: 'syncDerivativeElements'
}, iframeOrigin);
```

---

### 5. Preview Footer

Preview what a footer template would render as without saving changes. Useful for live preview in a settings UI.

**Action:** `previewFooter`

**Parameters:**
```typescript
{
  footer: FooterConfig;    // Footer config to preview
  slideIndex: number;      // 0-based slide index for {page} variable
}
```

**Response:**
```javascript
{
  success: true,
  action: 'previewFooter',
  previewText: 'Q4 Business Review | Page 3 of 12',
  slideIndex: 2,
  totalSlides: 12
}
```

**Example:**
```javascript
// Preview footer for slide 3 (0-based index = 2)
iframe.contentWindow.postMessage({
  action: 'previewFooter',
  params: {
    footer: {
      template: '{title} | Page {page} of {total}',
      values: {
        title: 'Q4 Business Review'
      }
    },
    slideIndex: 2
  }
}, iframeOrigin);
```

---

## REST API Endpoints

In addition to postMessage, you can call these REST endpoints directly:

### PUT /api/presentations/{id}/derivative-elements
Update derivative elements configuration.

```bash
curl -X PUT "http://localhost:8504/api/presentations/{id}/derivative-elements" \
  -H "Content-Type: application/json" \
  -d '{
    "footer": {
      "template": "{title} | Page {page}",
      "values": { "title": "My Presentation" }
    },
    "logo": {
      "image_url": "https://example.com/logo.png"
    }
  }'
```

### GET /api/presentations/{id}/derivative-elements
Get current derivative elements configuration.

```bash
curl "http://localhost:8504/api/presentations/{id}/derivative-elements"
```

### DELETE /api/presentations/{id}/derivative-elements
Clear all derivative elements.

```bash
curl -X DELETE "http://localhost:8504/api/presentations/{id}/derivative-elements"
```

---

## Frontend Implementation Guide

### Presentation Settings Panel

Recommended UI for managing derivative elements:

```
+--------------------------------------------------+
|  Presentation Settings                      [X]  |
+--------------------------------------------------+
|                                                  |
|  FOOTER                                          |
|  +--------------------------------------------+  |
|  | Template: [____________________________]  |  |
|  | Preview: "Q4 Review | Page 1 of 12"       |  |
|  +--------------------------------------------+  |
|                                                  |
|  Variables:                                      |
|  Title:  [Q4 Business Review______________]     |
|  Date:   [December 2024___________________]     |
|  Author: [John Smith______________________]     |
|                                                  |
+--------------------------------------------------+
|                                                  |
|  LOGO                                            |
|  +------------+                                  |
|  |   [img]    |  company-logo.png                |
|  +------------+  [Upload] [Remove]               |
|                                                  |
+--------------------------------------------------+
|                              [Cancel]  [Save]    |
+--------------------------------------------------+
```

### Implementation Steps

1. **Get initial state** when opening settings:
```javascript
iframe.contentWindow.postMessage({ action: 'getDerivativeElements' }, origin);
```

2. **Live preview** as user types (debounced):
```javascript
iframe.contentWindow.postMessage({
  action: 'previewFooter',
  params: {
    footer: currentFooterConfig,
    slideIndex: 0  // Preview for first slide
  }
}, origin);
```

3. **Save changes** when user clicks Save:
```javascript
iframe.contentWindow.postMessage({
  action: 'updateDerivativeElements',
  params: {
    footer: finalFooterConfig,
    logo: finalLogoConfig
  }
}, origin);
```

4. **Handle response** and close panel on success:
```javascript
window.addEventListener('message', (event) => {
  if (event.data.action === 'updateDerivativeElements') {
    if (event.data.success) {
      showToast('Settings saved!');
      closeSettingsPanel();
    } else {
      showError(event.data.error);
    }
  }
});
```

---

## Common Footer Templates

| Use Case | Template |
|----------|----------|
| Simple page number | `Page {page}` |
| Page X of Y | `Page {page} of {total}` |
| Title + page | `{title} \| Page {page}` |
| Full professional | `{title} \| Page {page} of {total} \| {date}` |
| Author credit | `{title} \| {author} \| {date}` |
| Confidential | `CONFIDENTIAL \| {title} \| Page {page}` |

---

## Error Handling

All postMessage responses include `success` and `error` fields:

```javascript
// Success
{
  success: true,
  action: 'updateDerivativeElements',
  derivativeElements: { ... }
}

// Error
{
  success: false,
  action: 'updateDerivativeElements',
  error: 'No presentation ID available'
}
```

Common errors:
- `No presentation ID available` - Presentation not loaded
- `Failed to update derivative elements` - API error
- `syncDerivativeElements function not available` - Script not loaded

---

## Database Migration

Before using derivative elements, ensure the database column exists:

```sql
ALTER TABLE ls_presentations
ADD COLUMN IF NOT EXISTS derivative_elements JSONB;
```

Run this migration in Supabase SQL Editor:
`migrations/001_add_derivative_elements.sql`

---

## Version

- **API Version**: 1.0
- **Document Date**: December 2024
- **Layout Service**: v7.5-main
