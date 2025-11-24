# Content Generation Guide for v7.5-main

**Version**: 7.5.0
**Date**: 2025-01-01
**Audience**: Text Service developers

---

## Overview

v7.5-main simplifies presentation layouts to **only 2 layouts**, giving Text Service **full creative control** over content areas. This guide explains how to generate HTML content that renders beautifully within the allocated content areas.

---

## Architecture Philosophy

### Format Ownership Model

**Layout Builder owns**:
- Structural elements (titles, subtitles, footers)
- Grid positioning
- Slide backgrounds
- Layout scaffolding

**Text Service owns**:
- Content creation and formatting
- HTML structure within content areas
- Styling (colors, fonts, sizes)
- Layout within allocated space

### Key Principle
> Text Service receives dimensions → Generates HTML that fits → Layout Builder renders as-is

---

## The 2 Layouts

### L29: Full-Bleed Slides
**Purpose**: Title slides, section dividers, ending slides, AND hero moments
**Format Ownership**: Text Service owns hero_content field (complete creative control)
**Text Service Role**: Generate complete HTML for entire 1920×1080px slide

**Use Cases**:
- **Title slides**: Opening slide with presenter info
- **Section dividers**: Section break slides
- **Ending slides**: Closing slides with CTA
- **Hero moments**: High-impact full-bleed visuals

**Content to Generate**:
```json
{
  "hero_content": "Full HTML (1920px × 1080px) - Text Service has complete control"
}
```

**Note**: Text Service generates ALL HTML for L29 slides. Layout Builder renders as-is.

---

### L25: Main Content Shell
**Purpose**: 80% of your slides
**Format Ownership**: Text Service owns `rich_content` field
**Content Area Dimensions**:
- **Grid**: Rows 5-16, Columns 2-31 (12 rows × 30 columns)
- **Pixels**: ~1800px wide × ~720px tall (at 1920×1080)
- **Aspect Ratio**: 2.5:1 (horizontal)
- **Overflow**: Vertical scroll enabled

**Structure**:
```
Row 1: margin
Row 2: slide_title (layout_builder formats)
Row 3: subtitle (layout_builder formats)
Row 4: spacing
Rows 5-16: RICH_CONTENT (text_service owns) ← 1800×720px
Row 17: spacing
Row 18: footer
```

**Content to Generate**:
```json
{
  "slide_title": "Plain text (max 80 chars)",
  "subtitle": "Plain text (max 120 chars)",
  "rich_content": "<div>HTML with full styling (1800px × 720px)</div>",
  "presentation_name": "Q4 Business Review (optional)",
  "company_logo": "<img src='logo.png' style='height: 20px;'> (optional)"
}
```

**Text Service Responsibilities**:
1. Generate complete HTML for `rich_content` field
2. Include all styling inline (no external CSS classes)
3. Ensure content fits within 1800px × 720px
4. Design layout: cards, columns, tables, etc.
5. Optionally provide `presentation_name` and `company_logo` for footer

**Footer Customization** (Optional):
- **presentation_name**: Text displayed in footer left section (5 grids, columns 2-6)
  - Plain text or simple HTML
  - Example: `"Q4 Business Review"` or `"Client Proposal - Acme Corp"`
- **company_logo**: HTML/image displayed in footer right section (3 grids, columns 29-31)
  - Can be image tag, SVG, or simple HTML
  - Example: `"<img src='logo.png' style='height: 20px;'>"` or `"<span style='font-weight: bold;'>ACME</span>"`
  - Keep height around 20px for best fit

---

### L29: Hero Full-Bleed
**Purpose**: High-impact opening/closing slides
**Format Ownership**: Text Service owns `hero_content` field
**Content Area Dimensions**:
- **Grid**: Rows 1-18, Columns 1-32 (entire slide)
- **Pixels**: 1920px wide × 1080px tall (full HD)
- **Aspect Ratio**: 16:9
- **Overflow**: Hidden (no scrolling)

**Structure**:
```
Full slide: HERO_CONTENT (text_service owns) ← 1920×1080px
No title, no subtitle, no footer
```

**Content to Generate**:
```json
{
  "hero_content": "<div>Full-bleed HTML (1920px × 1080px)</div>"
}
```

**Text Service Responsibilities**:
1. Generate complete HTML for entire slide
2. Include all styling inline
3. Ensure content fits EXACTLY 1920×1080px (no overflow)
4. Handle backgrounds, overlays, text positioning

---

## Background Customization

**NEW FEATURE**: All slides now support optional backgrounds (color and/or image).

### When to Use Backgrounds

**Background Color**:
- Brand-aligned slides matching corporate colors
- Section dividers with thematic colors
- Visual hierarchy and categorization
- Improved readability with subtle tints

**Background Image**:
- Hero slides (L29) with impactful imagery
- Branded backdrops for title slides
- Thematic backgrounds for section breaks
- Full-bleed visuals for engagement

### Adding Backgrounds to Slides

#### Background Color Only

```json
{
  "layout": "L25",
  "background_color": "#f0f9ff",
  "content": {
    "slide_title": "Revenue Growth Strategy",
    "subtitle": "Q4 2024 Results",
    "rich_content": "<div>Your HTML content here</div>"
  }
}
```

#### Background Image Only

```json
{
  "layout": "L29",
  "background_image": "https://images.example.com/hero-background.jpg",
  "content": {
    "hero_content": "<div style='color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.8);'>Hero Content</div>"
  }
}
```

#### Both (Image with Color Fallback)

```json
{
  "layout": "L29",
  "background_image": "https://images.example.com/background.jpg",
  "background_color": "#1a1a2e",
  "content": {
    "hero_content": "<div>Content with safe fallback color</div>"
  }
}
```

### Background Best Practices

1. **Contrast for Readability**
   - Use light backgrounds (#f0f9ff, #fef3c7) with dark text
   - Use dark backgrounds (#1a1a2e, #0f4c75) with light text
   - Add text shadows for text over images: `text-shadow: 2px 2px 8px rgba(0,0,0,0.8);`

2. **Image Specifications**
   - **Resolution**: 1920×1080 or higher for crisp display
   - **Format**: JPG for photos, PNG for graphics with transparency
   - **Size**: Keep under 1MB for fast loading
   - **Positioning**: Images use `background-size: cover` (fills entire slide)

3. **Color Selection**
   - Use hex format: `#FF5733` (6 digits) or `#f8f9fa` (case insensitive)
   - Stick to brand colors for consistency
   - Test contrast ratios for accessibility (WCAG AA: 4.5:1 minimum)

4. **Fallback Strategy**
   - Always provide `background_color` when using `background_image`
   - Fallback color shows if image fails to load or during loading
   - Choose fallback color that matches image dominant color

### Content Visibility on Backgrounds

When generating HTML content for slides with backgrounds:

**For Light Backgrounds** (#f0f9ff, #fff7ed, etc.):
```html
<div style="color: #1f2937; /* Dark text for readability */">
  <h2 style="color: #111827;">Dark headings on light background</h2>
  <p>Body text remains readable</p>
</div>
```

**For Dark Backgrounds** (#1a1a2e, #0f4c75, etc.):
```html
<div style="color: #f9fafb; /* Light text for readability */">
  <h2 style="color: #ffffff;">White headings on dark background</h2>
  <p>Light body text for contrast</p>
</div>
```

**For Image Backgrounds**:
```html
<div style="
  color: white;
  text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
  background: rgba(0,0,0,0.3);
  padding: 20px;
  border-radius: 8px;
">
  <h2>Text with shadow and semi-transparent background</h2>
  <p>Ensures readability over any image</p>
</div>
```

### Director Service Integration

When generating slides, the Director Service can specify backgrounds:

```python
# Example: Director Service generating slide with background
slide = {
    "layout": "L25",
    "background_color": "#f0f9ff",  # Light blue for brand consistency
    "content": {
        "slide_title": "Market Analysis",
        "subtitle": "Q4 2024",
        "rich_content": text_service.generate_html(data)
    }
}
```

**Decision Flow for Director Service**:
1. Title/Hero slides → Use `background_image` for impact
2. Section dividers → Use `background_color` matching theme
3. Data/Analytics slides → Light `background_color` (#f8f9fa, #f0f9ff)
4. Standard content → No background (white default) or subtle tint

---

## HTML Generation Patterns

### Pattern 1: Card-Based Layout (L25)

**Use Case**: Metrics, features, benefits
**Recommended For**: 3-4 key points with visual emphasis

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; padding: 32px; height: 100%; align-items: center;">
  <!-- Card 1 -->
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 48px; border-radius: 16px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
    <div style="font-size: 64px; font-weight: bold; color: white; margin-bottom: 24px;">25%</div>
    <h3 style="font-size: 28px; color: white; margin-bottom: 16px; font-weight: 600;">Cost Savings</h3>
    <p style="font-size: 18px; color: rgba(255,255,255,0.9); line-height: 1.6;">Reduction in operational costs through AI automation</p>
  </div>

  <!-- Card 2 -->
  <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 48px; border-radius: 16px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
    <div style="font-size: 64px; font-weight: bold; color: white; margin-bottom: 24px;">40%</div>
    <h3 style="font-size: 28px; color: white; margin-bottom: 16px; font-weight: 600;">Efficiency Gain</h3>
    <p style="font-size: 18px; color: rgba(255,255,255,0.9); line-height: 1.6;">Faster processing with intelligent workflows</p>
  </div>

  <!-- Card 3 -->
  <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 48px; border-radius: 16px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
    <div style="font-size: 64px; font-weight: bold; color: white; margin-bottom: 24px;">95%</div>
    <h3 style="font-size: 28px; color: white; margin-bottom: 16px; font-weight: 600;">Accuracy</h3>
    <p style="font-size: 18px; color: rgba(255,255,255,0.9); line-height: 1.6;">Diagnostic accuracy with machine learning</p>
  </div>
</div>
```

**Dimensions**: Fits perfectly in 1800×720px content area

---

### Pattern 2: Two-Column Layout (L25)

**Use Case**: Benefits vs Implementation, Before vs After
**Recommended For**: Comparative content, balanced information

```html
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; padding: 32px; height: 100%;">
  <!-- Left Column -->
  <div style="padding: 24px;">
    <h2 style="font-size: 36px; margin-bottom: 32px; color: #1f2937; font-weight: 700; border-bottom: 4px solid #3b82f6; padding-bottom: 16px;">Key Benefits</h2>
    <ul style="font-size: 20px; line-height: 2; color: #374151; list-style: none; padding: 0;">
      <li style="margin-bottom: 24px; padding-left: 40px; position: relative;">
        <span style="position: absolute; left: 0; top: 0; color: #3b82f6; font-size: 28px;">✓</span>
        <strong style="color: #1f2937;">300% ROI</strong> - Full return within 12 months
      </li>
      <li style="margin-bottom: 24px; padding-left: 40px; position: relative;">
        <span style="position: absolute; left: 0; top: 0; color: #3b82f6; font-size: 28px;">✓</span>
        <strong style="color: #1f2937;">20 Hours/Week Saved</strong> - Automation at scale
      </li>
      <li style="margin-bottom: 24px; padding-left: 40px; position: relative;">
        <span style="position: absolute; left: 0; top: 0; color: #3b82f6; font-size: 28px;">✓</span>
        <strong style="color: #1f2937;">10x Scale</strong> - Handle 10x current volume
      </li>
    </ul>
  </div>

  <!-- Right Column -->
  <div style="padding: 24px;">
    <h2 style="font-size: 36px; margin-bottom: 32px; color: #1f2937; font-weight: 700; border-bottom: 4px solid #10b981; padding-bottom: 16px;">Implementation</h2>
    <ol style="font-size: 20px; line-height: 2; color: #374151; padding-left: 40px;">
      <li style="margin-bottom: 24px;">
        <strong style="color: #1f2937;">Phase 1:</strong> Data migration<br>
        <span style="font-size: 16px; color: #6b7280;">Timeline: 2 weeks</span>
      </li>
      <li style="margin-bottom: 24px;">
        <strong style="color: #1f2937;">Phase 2:</strong> User training<br>
        <span style="font-size: 16px; color: #6b7280;">Timeline: 1 week</span>
      </li>
      <li style="margin-bottom: 24px;">
        <strong style="color: #1f2937;">Phase 3:</strong> Go-live & support<br>
        <span style="font-size: 16px; color: #6b7280;">Timeline: 1 day</span>
      </li>
    </ol>
  </div>
</div>
```

**Dimensions**: Fits perfectly in 1800×720px content area

---

### Pattern 3: Table Layout (L25)

**Use Case**: Comparison tables, feature matrices
**Recommended For**: Detailed data presentation

```html
<div style="padding: 24px; height: 100%; overflow: auto;">
  <table style="width: 100%; border-collapse: collapse; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <thead>
      <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
        <th style="padding: 20px; text-align: left; font-weight: 600;">Feature</th>
        <th style="padding: 20px; text-align: center; font-weight: 600;">Current State</th>
        <th style="padding: 20px; text-align: center; font-weight: 600;">With AI</th>
        <th style="padding: 20px; text-align: center; font-weight: 600;">Impact</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom: 1px solid #e5e7eb; background: #f9fafb;">
        <td style="padding: 20px; font-weight: 600; color: #1f2937;">Processing Time</td>
        <td style="padding: 20px; text-align: center; color: #6b7280;">45 min</td>
        <td style="padding: 20px; text-align: center; color: #3b82f6; font-weight: 700;">5 min</td>
        <td style="padding: 20px; text-align: center; color: #10b981; font-weight: 700;">89% faster</td>
      </tr>
      <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 20px; font-weight: 600; color: #1f2937;">Error Rate</td>
        <td style="padding: 20px; text-align: center; color: #6b7280;">12%</td>
        <td style="padding: 20px; text-align: center; color: #3b82f6; font-weight: 700;">1%</td>
        <td style="padding: 20px; text-align: center; color: #10b981; font-weight: 700;">92% reduction</td>
      </tr>
      <tr style="border-bottom: 1px solid #e5e7eb; background: #f9fafb;">
        <td style="padding: 20px; font-weight: 600; color: #1f2937;">Cost per Transaction</td>
        <td style="padding: 20px; text-align: center; color: #6b7280;">$15</td>
        <td style="padding: 20px; text-align: center; color: #3b82f6; font-weight: 700;">$4</td>
        <td style="padding: 20px; text-align: center; color: #10b981; font-weight: 700;">73% savings</td>
      </tr>
      <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 20px; font-weight: 600; color: #1f2937;">Customer Satisfaction</td>
        <td style="padding: 20px; text-align: center; color: #6b7280;">72%</td>
        <td style="padding: 20px; text-align: center; color: #3b82f6; font-weight: 700;">94%</td>
        <td style="padding: 20px; text-align: center; color: #10b981; font-weight: 700;">+22 points</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Dimensions**: Fits in 1800×720px with scrolling if needed

---

### Pattern 4: Hero Image + Text Overlay (L29)

**Use Case**: Opening slides, brand moments
**Recommended For**: High-impact visual statements

```html
<div style="width: 100%; height: 100%; position: relative; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px;">
  <!-- Main Heading -->
  <h1 style="font-size: 96px; color: white; margin-bottom: 48px; text-align: center; font-weight: 900; line-height: 1.1; text-shadow: 0 4px 12px rgba(0,0,0,0.3);">
    Transform Your Business
  </h1>

  <!-- Subheading -->
  <p style="font-size: 42px; color: rgba(255,255,255,0.95); text-align: center; max-width: 1400px; line-height: 1.5; margin-bottom: 64px; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">
    Unlock the power of AI to drive innovation, efficiency, and sustainable growth across your organization
  </p>

  <!-- Call to Action Button -->
  <button style="padding: 28px 64px; font-size: 32px; background: white; color: #667eea; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; box-shadow: 0 8px 24px rgba(0,0,0,0.3); transition: all 0.3s;">
    Get Started Today
  </button>

  <!-- Optional: Bottom Badge -->
  <div style="position: absolute; bottom: 40px; right: 40px; background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); padding: 16px 32px; border-radius: 8px; color: white; font-size: 18px;">
    Trusted by 500+ companies
  </div>
</div>
```

**Dimensions**: Exactly 1920×1080px (full slide)

---

### Pattern 5: Grid of Small Cards (L25)

**Use Case**: Feature lists, service offerings
**Recommended For**: 6-9 items with equal importance

```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(2, 1fr); gap: 24px; padding: 24px; height: 100%;">
  <!-- Card 1 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #3b82f6;">
    <div style="font-size: 48px; margin-bottom: 16px;">🚀</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">Fast Deployment</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">Go live in 2 weeks with our rapid implementation framework</p>
  </div>

  <!-- Card 2 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #10b981;">
    <div style="font-size: 48px; margin-bottom: 16px;">🔒</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">Enterprise Security</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">SOC 2 Type II certified with bank-level encryption</p>
  </div>

  <!-- Card 3 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #f59e0b;">
    <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">Real-Time Analytics</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">Live dashboards and insights powered by AI</p>
  </div>

  <!-- Card 4 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #8b5cf6;">
    <div style="font-size: 48px; margin-bottom: 16px;">🤝</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">24/7 Support</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">Dedicated team available around the clock</p>
  </div>

  <!-- Card 5 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #ec4899;">
    <div style="font-size: 48px; margin-bottom: 16px;">⚡</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">Scalable Platform</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">Handle millions of transactions effortlessly</p>
  </div>

  <!-- Card 6 -->
  <div style="background: #f3f4f6; padding: 32px; border-radius: 12px; border-left: 6px solid #06b6d4;">
    <div style="font-size: 48px; margin-bottom: 16px;">🎯</div>
    <h3 style="font-size: 24px; color: #1f2937; margin-bottom: 12px; font-weight: 600;">Easy Integration</h3>
    <p style="font-size: 16px; color: #6b7280; line-height: 1.6;">Works with your existing systems seamlessly</p>
  </div>
</div>
```

**Dimensions**: Fits perfectly in 1800×720px content area

---

## Best Practices

### Styling Guidelines

1. **Use inline styles only** - No external CSS classes
2. **Specify all dimensions** - Use px, %, fr, or vw/vh units
3. **Include fallback fonts** - `font-family: -apple-system, BlinkMacSystemFont, ...`
4. **Use standard color formats** - Hex codes (#3b82f6) or rgb(59, 130, 246)
5. **Prefer CSS Grid/Flexbox** - Better control than floats

### Dimension Constraints

**L25 (Rich Content)**:
- Max width: 1800px
- Max height: 720px
- Overflow: Vertical scroll enabled (use sparingly)
- Test at 1920×1080 resolution

**L29 (Hero)**:
- Exact size: 1920×1080px
- Overflow: Hidden (content MUST fit)
- No scrolling allowed

### Responsive Design

While presentations are typically displayed at 1920×1080, consider:
- Use percentage widths for flexibility
- Test content scaling at different zoom levels
- Ensure minimum font sizes (16px+) for readability

### Performance

1. **Minimize DOM complexity** - Max 50 elements per content area
2. **Optimize images** - Use appropriate sizes, compress well
3. **Avoid heavy animations** - CSS transitions only
4. **Limit nested structures** - Keep HTML hierarchy shallow

---

## Content Validation

### Text Service Should Validate

**Before sending to Layout Builder**:

```python
def validate_l25_content(html: str) -> bool:
    """Validate L25 rich_content fits constraints"""
    # Estimated height check (rough calculation)
    # Complex: parse HTML, estimate rendered height
    # Simple: character/line count heuristics

    # Check for dangerous tags
    dangerous = ['<script', '<iframe', '<object', '<embed']
    if any(tag in html.lower() for tag in dangerous):
        return False

    # Check width (ensure no fixed widths > 1800px)
    if 'width: 2000px' in html:  # Example check
        return False

    return True

def validate_l29_content(html: str) -> bool:
    """Validate L29 hero_content fits exactly 1920×1080px"""
    # Must fit without scrolling
    # Check for overflow: hidden compatibility
    # Validate full-bleed design

    return True
```

### Validation Checklist

- [ ] No `<script>` tags (security risk)
- [ ] No `<iframe>` tags (security risk)
- [ ] All styles are inline (no external classes)
- [ ] Content width ≤ 1800px (L25) or 1920px (L29)
- [ ] Content height ≤ 720px (L25) or 1080px (L29)
- [ ] Well-formed HTML (valid tags, proper nesting)
- [ ] Accessible colors (sufficient contrast)
- [ ] Readable font sizes (16px minimum)

---

## Integration with Director

### What Director Sends to Text Service

```json
{
  "layout_id": "L25",
  "layout_name": "Main Content Shell",
  "field_specifications": {
    "slide_title": {
      "format_type": "plain_text",
      "format_owner": "layout_builder",
      "max_chars": 80
    },
    "subtitle": {
      "format_type": "plain_text",
      "format_owner": "layout_builder",
      "max_chars": 120
    },
    "rich_content": {
      "format_type": "html",
      "format_owner": "text_service",
      "content_area": {
        "grid": {
          "rows": [5, 16],
          "columns": [2, 31]
        },
        "pixels": {
          "width": 1800,
          "height": 720
        }
      }
    }
  },
  "content_guidance": {
    "title": "Key Benefits",
    "narrative": "Focus on ROI, efficiency, and accuracy",
    "key_points": ["300% ROI", "20 hours saved", "95% accuracy"]
  }
}
```

### What Text Service Returns

```json
{
  "slide_title": "Key Benefits of AI Implementation",
  "subtitle": "Measurable Impact in 90 Days",
  "rich_content": "<div style=\"display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px;\">...</div>"
}
```

---

## Common Mistakes to Avoid

### ❌ Don't Do This

**1. Using external CSS classes**
```html
<!-- WRONG -->
<div class="card primary-color">...</div>
```

**2. Exceeding content area dimensions**
```html
<!-- WRONG for L25 -->
<div style="width: 2000px; height: 900px;">...</div>
```

**3. Hardcoding slide numbers or layout info**
```html
<!-- WRONG -->
<div>Slide 5 of 20</div>
```

**4. Using relative units without context**
```html
<!-- RISKY -->
<div style="width: 50em;">...</div>
```

### ✅ Do This Instead

**1. Use inline styles**
```html
<!-- CORRECT -->
<div style="background: #3b82f6; padding: 24px; border-radius: 12px;">...</div>
```

**2. Stay within content area**
```html
<!-- CORRECT for L25 -->
<div style="max-width: 1800px; max-height: 720px; overflow: auto;">...</div>
```

**3. Let Layout Builder handle metadata**
```html
<!-- CORRECT -->
<!-- Footer handles slide numbers automatically -->
```

**4. Use px or % units**
```html
<!-- CORRECT -->
<div style="width: 600px; padding: 24px;">...</div>
```

---

## Testing Your Generated Content

### Manual Testing

1. **Create test presentation** via API:
```bash
curl -X POST http://localhost:8504/api/presentations \
  -H "Content-Type: application/json" \
  -d @test-presentation.json
```

2. **View in browser** at returned URL

3. **Check content area fit**:
   - Press 'C' to toggle content area debug mode
   - Verify no overflow (unless intended)
   - Test at different zoom levels

### Automated Testing

```python
def test_content_generation():
    # Generate content
    content = text_service.generate_l25_content(...)

    # Validate
    assert validate_l25_content(content['rich_content'])

    # Test rendering (headless browser)
    presentation = {
        "title": "Test",
        "slides": [{"layout": "L25", "content": content}]
    }

    # Check for errors
    result = layout_builder.render(presentation)
    assert result.success
```

---

## Summary

### Quick Reference

| Layout | Text Service Role | Content Area Size | Overflow |
|--------|------------------|-------------------|----------|
| L25 | Generate rich HTML | 1800×720px | Vertical scroll |
| L29 | Generate full-bleed HTML (title/section/ending/hero) | 1920×1080px | No (hidden) |

### Key Takeaways

1. ✅ Text Service owns content creation, not structure
2. ✅ Use inline styles exclusively
3. ✅ Respect content area dimensions
4. ✅ Validate HTML before sending
5. ✅ Test at 1920×1080 resolution
6. ✅ Design for 16:9 aspect ratio
7. ✅ Keep DOM complexity low
8. ✅ Use semantic HTML where possible

---

**Questions?** See `/docs/ARCHITECTURE.md` or contact the Layout Builder team.

**Version History**:
- v7.5.0 (2025-01-01): Initial release with 2-layout system
