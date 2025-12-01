# Image Service Requirements for Layout Builder v7.5

This document specifies the API requirements for Image Service to integrate with Layout Builder's image insertion features.

## Overview

Layout Builder needs Image Service to provide:
1. **AI-generated images** at specified aspect ratios
2. **Image URLs** for insertion via `insertImage` API
3. **Multiple size variants** for responsive display
4. **Theme-aligned imagery** matching presentation aesthetics

---

## API 1: Generate Image

### Purpose
Generate an AI image based on a prompt with specified dimensions.

### Endpoint Suggestion
```
POST /api/image/generate
```

### Request Format
```typescript
{
  presentationId: string,
  prompt: string,              // Image generation prompt
  negativePrompt?: string,     // What to avoid
  dimensions: {
    width: number,             // Pixels (e.g., 1280)
    height: number,            // Pixels (e.g., 720)
    aspectRatio: string        // e.g., '16:9', '4:3', '1:1', '9:16'
  },
  style?: {
    type: 'photorealistic' | 'illustration' | 'abstract' | 'minimalist' | 'corporate' | '3d-render',
    mood?: 'professional' | 'creative' | 'energetic' | 'calm' | 'dramatic',
    colorScheme?: {
      dominant?: string,       // Hex color
      accent?: string,         // Hex color
      palette?: string[]       // Color palette to incorporate
    }
  },
  context?: {
    slideTitle?: string,       // Current slide title
    presentationTopic?: string,// Overall topic
    industry?: string          // Industry context
  },
  options?: {
    format: 'png' | 'jpeg' | 'webp',
    quality: number,           // 1-100
    transparent?: boolean      // PNG only
  }
}
```

### Response Format
```typescript
{
  success: boolean,
  imageUrl: string,            // CDN URL to generated image
  thumbnailUrl?: string,       // Smaller preview version
  dimensions: {
    width: number,
    height: number,
    aspectRatio: string
  },
  metadata: {
    format: string,
    fileSize: number,          // Bytes
    generationTime: number     // Milliseconds
  },
  expiresAt?: string,          // ISO timestamp (if URL is temporary)
  error?: string
}
```

---

## API 2: Generate Image Variants

### Purpose
Generate multiple size variants of an image for responsive use.

### Endpoint Suggestion
```
POST /api/image/generate-variants
```

### Request Format
```typescript
{
  // ... same as generate
  variants: Array<{
    name: string,              // e.g., 'large', 'medium', 'thumbnail'
    width: number,
    height: number
  }>
}
```

### Response Format
```typescript
{
  success: boolean,
  variants: Array<{
    name: string,
    imageUrl: string,
    dimensions: { width, height }
  }>,
  error?: string
}
```

---

## API 3: Search Stock Images

### Purpose
Search for stock/royalty-free images matching criteria.

### Endpoint Suggestion
```
GET /api/image/search
```

### Request Parameters
```typescript
{
  query: string,               // Search query
  aspectRatio?: string,        // Filter by aspect ratio
  color?: string,              // Dominant color filter
  style?: string,              // Style filter
  page?: number,
  limit?: number               // Max 50
}
```

### Response Format
```typescript
{
  success: boolean,
  images: Array<{
    id: string,
    previewUrl: string,        // Low-res preview
    fullUrl: string,           // Full resolution
    dimensions: { width, height },
    attribution?: string       // Credit if required
  }>,
  pagination: {
    page: number,
    totalPages: number,
    totalResults: number
  }
}
```

---

## Common Aspect Ratios for Slides

Layout Builder uses a 32×18 grid (1920×1080 base). Common image zones:

| Use Case | Aspect Ratio | Recommended Size | Grid Position |
|----------|--------------|------------------|---------------|
| Hero full-bleed | 16:9 | 1920×1080 | Full slide |
| Left half (L27) | 9:16 | 720×1080 | cols 1-12, rows 1-18 |
| Content image | 16:9 | 1280×720 | cols 2-20, rows 5-13 |
| Square icon | 1:1 | 400×400 | 6×6 grid cells |
| Tall portrait | 3:4 | 600×800 | cols 2-10, rows 4-16 |
| Wide banner | 21:9 | 1680×720 | cols 2-30, rows 3-10 |

---

## Image Quality Requirements

### Resolution Guidelines
| Display Size | Min Resolution | Recommended |
|--------------|----------------|-------------|
| Thumbnail | 200×150 | 400×300 |
| Medium | 800×600 | 1280×960 |
| Full slide | 1920×1080 | 2560×1440 |

### File Size Limits
- **Thumbnail**: < 50KB
- **Medium**: < 200KB
- **Full resolution**: < 1MB
- **Hero image**: < 2MB

### Format Recommendations
| Use Case | Format | Quality |
|----------|--------|---------|
| Photos | JPEG | 85% |
| Graphics/logos | PNG | - |
| Animations | GIF/WebP | - |
| General web | WebP | 80% |

---

## Layout Builder Integration

### How Layout Builder Will Use These APIs

1. **insertImage** postMessage handler:
   ```javascript
   {
     action: 'insertImage',
     params: {
       slideIndex: 0,
       position: { gridRow: '4/14', gridColumn: '3/20' },
       imageUrl: 'https://...',  // From Image Service
       alt: 'Description',
       objectFit: 'cover',
       draggable: true
     }
   }
   ```

2. **Image rendering**:
   - Layout Builder creates `<img>` element
   - Positions in CSS grid
   - Handles `object-fit` styling
   - Enables drag-drop repositioning

3. **Image HTML output**:
   ```html
   <div id="img-abc123" class="dynamic-element inserted-image"
        style="grid-row: 4/14; grid-column: 3/20;">
     <img src="https://..."
          alt="Description"
          style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">
   </div>
   ```

---

## Theme Integration

### Color-Matched Images

Image Service should consider theme colors when generating:

```typescript
// Request includes theme context
{
  style: {
    colorScheme: {
      dominant: '#1e40af',     // Blue theme
      accent: '#f59e0b'        // Orange accent
    }
  }
}
```

### Style Matching

| Presentation Style | Image Style |
|-------------------|-------------|
| Corporate/Professional | photorealistic, minimalist |
| Creative/Startup | illustration, 3d-render |
| Technical/Data | abstract, minimalist |
| Marketing | energetic, colorful |

---

## Caching & Performance

### CDN Requirements
- Images served via CDN (CloudFront, Cloudflare, etc.)
- Cache headers for browser caching
- WebP with JPEG fallback

### Response Time Expectations
| Operation | Expected | Max |
|-----------|----------|-----|
| Stock search | < 500ms | 2s |
| Generate (small) | < 5s | 15s |
| Generate (large) | < 10s | 30s |
| Fetch existing | < 200ms | 1s |

### URL Persistence
- Generated images should have stable URLs (not expiring)
- Or if temporary, provide `expiresAt` and refresh endpoint

---

## Error Handling

### Error Codes
| Code | Meaning |
|------|---------|
| `INVALID_DIMENSIONS` | Invalid width/height |
| `INVALID_ASPECT_RATIO` | Unsupported aspect ratio |
| `GENERATION_FAILED` | AI generation failed |
| `CONTENT_POLICY` | Content policy violation |
| `RATE_LIMITED` | Too many requests |
| `NOT_FOUND` | Image not found |

### Fallback Behavior
Return a placeholder image URL:
```
https://images.deckster.xyz/placeholder/{width}x{height}?text=Image+Unavailable
```

---

## Security Considerations

1. **Content Safety**: Filter inappropriate content in AI generation
2. **URL Validation**: Only serve images from approved domains
3. **Rate Limiting**: Limit generation requests per user/presentation
4. **Copyright**: Ensure stock images are properly licensed

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial specification |

---

## Contact

For questions about these requirements, contact the Layout Builder team.
