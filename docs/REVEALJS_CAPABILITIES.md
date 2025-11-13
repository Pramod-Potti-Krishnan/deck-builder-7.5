# Reveal.js Capabilities Guide for v7.5-main

**Version**: Reveal.js 4.5.0
**Last Updated**: November 2025
**Purpose**: Comprehensive guide to Reveal.js features available for v7.5-main presentation viewer

---

## Table of Contents

1. [Overview](#overview)
2. [Current v7.5-main Implementation](#current-v75-main-implementation)
3. [⭐ Slide Overview Mode (Thumbnail Grid)](#-slide-overview-mode-thumbnail-grid)
4. [Speaker Notes & Presenter View](#speaker-notes--presenter-view)
5. [Fragments (Step-by-Step Reveals)](#fragments-step-by-step-reveals)
6. [Backgrounds](#backgrounds)
7. [Auto-Animate](#auto-animate)
8. [Vertical Slides](#vertical-slides)
9. [Available Plugins](#available-plugins)
10. [JavaScript API Reference](#javascript-api-reference)
11. [Event System](#event-system)
12. [Configuration Options](#configuration-options)
13. [Keyboard Shortcuts](#keyboard-shortcuts)
14. [Frontend Integration Examples](#frontend-integration-examples)
15. [Implementation Recommendations](#implementation-recommendations)
16. [Code Examples](#code-examples)

---

## Overview

Reveal.js is a powerful HTML presentation framework that v7.5-main uses to display presentations. Currently, we're only using a small fraction of its capabilities. This guide documents all available features and how to implement them in your frontend.

**Current Usage**: ~20% of Reveal.js capabilities
**Available Features**: 50+ additional features ready to use

---

## Current v7.5-main Implementation

### What's Already Working

**Reveal.js Version**: 4.5.0 (loaded from CDN)

**Enabled Features**:
```javascript
{
  controls: true,           // Navigation arrows
  progress: true,           // Progress bar at bottom
  slideNumber: true,        // Slide numbers
  hash: true,              // URL hash for deep linking
  history: true,           // Browser history
  keyboard: true,          // Keyboard navigation
  overview: true,          // Overview mode (ESC/O key)
  center: false,           // Don't center slides vertically
  transition: 'slide',     // Slide transition effect
  width: 1920,            // Base width
  height: 1080,           // Base height
  margin: 0,              // No margins
  minScale: 1,            // No downscaling
  maxScale: 1             // No upscaling
}
```

**Custom Keyboard Shortcuts** (in viewer.html):
- **G key**: Toggle grid view
- **B key**: Toggle borders
- **C key**: Toggle controls

**Layouts Supported**:
- **L25**: Content shell with header/footer
- **L29**: Full-bleed hero layout

---

## ⭐ Slide Overview Mode (Thumbnail Grid)

### **YES - This Feature EXISTS and is Already Enabled!**

Reveal.js has a built-in overview mode that shows all slides as clickable thumbnails in a grid layout.

### How to Access

**Keyboard Shortcuts**:
- Press **ESC** to toggle overview mode
- Press **O** (letter O) to toggle overview mode

**Programmatic Access**:
```javascript
// Toggle overview mode
Reveal.toggleOverview();

// Explicitly show overview
Reveal.toggleOverview(true);

// Explicitly hide overview
Reveal.toggleOverview(false);

// Check if overview is active
const isInOverview = Reveal.isOverview();
```

### Features of Overview Mode

1. **Thumbnail Grid**: All slides displayed as miniatures
2. **Click Navigation**: Click any slide to jump directly to it
3. **Keyboard Navigation**: Arrow keys still work to move between slides
4. **Maintains State**: Remembers your current slide when exiting overview
5. **Responsive**: Adapts to browser window size

### Events

Listen for overview mode changes:

```javascript
Reveal.on('overviewshown', function() {
  console.log('Overview mode opened');
  // Update your UI, show "Grid View" indicator, etc.
});

Reveal.on('overviewhidden', function() {
  console.log('Overview mode closed');
  // Update your UI, show "Slide View" indicator, etc.
});
```

### Frontend Integration Example

**Add Overview Button to UI**:

```html
<!-- React Component -->
function OverviewButton() {
  const [isOverview, setIsOverview] = useState(false);

  useEffect(() => {
    const handleOverviewShown = () => setIsOverview(true);
    const handleOverviewHidden = () => setIsOverview(false);

    Reveal.on('overviewshown', handleOverviewShown);
    Reveal.on('overviewhidden', handleOverviewHidden);

    return () => {
      Reveal.off('overviewshown', handleOverviewShown);
      Reveal.off('overviewhidden', handleOverviewHidden);
    };
  }, []);

  return (
    <button onClick={() => Reveal.toggleOverview()}>
      {isOverview ? '📋 Slide View' : '🔲 Grid View'}
    </button>
  );
}
```

**Vanilla JavaScript**:

```javascript
// Add button to page
const overviewBtn = document.createElement('button');
overviewBtn.textContent = 'Show All Slides';
overviewBtn.style.position = 'fixed';
overviewBtn.style.top = '20px';
overviewBtn.style.right = '20px';
overviewBtn.style.zIndex = '1000';

overviewBtn.addEventListener('click', () => {
  Reveal.toggleOverview();
});

document.body.appendChild(overviewBtn);

// Update button text based on state
Reveal.on('overviewshown', () => {
  overviewBtn.textContent = 'Hide Grid';
});

Reveal.on('overviewhidden', () => {
  overviewBtn.textContent = 'Show All Slides';
});
```

### Styling Overview Mode

Customize the appearance with CSS:

```css
/* Override default overview styling */
.reveal.overview .slides section {
  border: 2px solid #ccc;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.reveal.overview .slides section.present {
  border-color: #007bff;
  box-shadow: 0 6px 12px rgba(0,123,255,0.3);
}

.reveal.overview .slides section:hover {
  border-color: #0056b3;
  cursor: pointer;
}
```

---

## Speaker Notes & Presenter View

### Overview

Reveal.js includes a powerful **Speaker View** that shows:
- Current slide
- Next slide preview
- Speaker notes (hidden from audience)
- Elapsed time and current time
- Slide navigation controls

### Setup

**1. Include the Notes Plugin**:

```html
<!-- Add to viewer.html -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>

<script>
  Reveal.initialize({
    // ... existing config ...
    plugins: [ RevealNotes ]
  });
</script>
```

**2. Add Notes to Slides**:

**Method 1: Using `<aside>` element**:
```html
<section>
  <h1>Slide Title</h1>
  <p>Slide content...</p>

  <aside class="notes">
    These are speaker notes. Only visible in presenter view.
    - Remember to mention the Q3 results
    - Emphasize the 40% growth
    - Transition smoothly to next slide
  </aside>
</section>
```

**Method 2: Using `data-notes` attribute**:
```html
<section data-notes="Quick reminder: mention the deadline">
  <h1>Project Timeline</h1>
</section>
```

### Accessing Speaker View

**Keyboard Shortcut**: Press **S** key

**Programmatic Access**:
```javascript
// Open speaker view
Reveal.getPlugin('notes').open();
```

### Speaker View Features

- **Dual monitors**: Show presentation on one screen, notes on another
- **Synchronized**: Notes window stays in sync with main presentation
- **Timer**: Shows elapsed time and current time
- **Next slide preview**: See what's coming up
- **Slide thumbnails**: Quick navigation

### Frontend Integration

**Add Speaker Mode Button**:

```javascript
function SpeakerNotesButton() {
  const openSpeakerView = () => {
    const notesPlugin = Reveal.getPlugin('notes');
    if (notesPlugin) {
      notesPlugin.open();
    } else {
      alert('Speaker notes plugin not loaded');
    }
  };

  return (
    <button onClick={openSpeakerView}>
      🎤 Open Speaker View
    </button>
  );
}
```

### Generating Notes from Content

For v7.5-main, you could automatically generate speaker notes from slide metadata:

```javascript
// When rendering slides, add notes based on content
function addSpeakerNotes(slideElement, slideData) {
  const notes = document.createElement('aside');
  notes.className = 'notes';

  // Generate notes from slide metadata
  let noteText = `Slide ${slideData.slideNumber}:\n`;
  if (slideData.title) {
    noteText += `Title: ${slideData.title}\n`;
  }
  if (slideData.talking_points) {
    noteText += `\nKey Points:\n${slideData.talking_points.join('\n')}`;
  }

  notes.textContent = noteText;
  slideElement.appendChild(notes);
}
```

---

## Fragments (Step-by-Step Reveals)

### Overview

Fragments allow content to appear step-by-step on the same slide, perfect for:
- Revealing bullet points one at a time
- Building charts progressively
- Highlighting specific elements
- Creating step-by-step tutorials

### Basic Usage

```html
<section>
  <h2>Key Points</h2>
  <ul>
    <li class="fragment">First point appears</li>
    <li class="fragment">Then second point</li>
    <li class="fragment">Finally third point</li>
  </ul>
</section>
```

### Fragment Styles

```html
<!-- Fade in (default) -->
<p class="fragment">Fades in</p>

<!-- Fade out -->
<p class="fragment fade-out">Fades out</p>

<!-- Fade up -->
<p class="fragment fade-up">Slides up and fades in</p>

<!-- Fade down -->
<p class="fragment fade-down">Slides down and fades in</p>

<!-- Fade left/right -->
<p class="fragment fade-left">Slides from left</p>
<p class="fragment fade-right">Slides from right</p>

<!-- Grow/Shrink -->
<p class="fragment grow">Grows</p>
<p class="fragment shrink">Shrinks</p>

<!-- Highlight -->
<p class="fragment highlight-red">Highlights in red</p>
<p class="fragment highlight-blue">Highlights in blue</p>
<p class="fragment highlight-green">Highlights in green</p>

<!-- Strike through -->
<p class="fragment strike">Gets struck through</p>

<!-- Fade in then out -->
<p class="fragment fade-in-then-out">Appears then disappears</p>

<!-- Fade in then semi-out -->
<p class="fragment fade-in-then-semi-out">Appears then dims</p>
```

### Fragment Order

Control the order with `data-fragment-index`:

```html
<section>
  <p class="fragment" data-fragment-index="3">Appears third</p>
  <p class="fragment" data-fragment-index="1">Appears first</p>
  <p class="fragment" data-fragment-index="2">Appears second</p>
</section>
```

### Multiple Effects

Apply multiple fragment effects:

```html
<p class="fragment fade-up highlight-red">
  Slides up AND highlights red
</p>
```

### JavaScript API

```javascript
// Navigate fragments
Reveal.nextFragment();      // Show next fragment
Reveal.prevFragment();      // Show previous fragment

// Get fragment state
const fragments = Reveal.availableFragments();
// Returns: { prev: boolean, next: boolean }

// Check current fragments
const currentFragments = Reveal.getCurrentSlide().querySelectorAll('.fragment');
```

### Events

```javascript
Reveal.on('fragmentshown', function(event) {
  console.log('Fragment shown:', event.fragment);
  // event.fragment = the DOM element
  // event.index = fragment index
});

Reveal.on('fragmenthidden', function(event) {
  console.log('Fragment hidden:', event.fragment);
});
```

### v7.5-main Integration

When generating slides in your renderers, add fragment classes:

```javascript
// Example: Render bullet points with fragments
function renderBulletList(items) {
  return `
    <ul>
      ${items.map(item => `
        <li class="fragment fade-up">${item}</li>
      `).join('')}
    </ul>
  `;
}
```

---

## Backgrounds

### Overview

Reveal.js supports multiple background types for slides:
- Solid colors
- Gradients
- Images
- Videos
- Iframes (embedded web pages)

### Color Backgrounds

```html
<!-- Solid color -->
<section data-background-color="#ff0000">
  <h2>Red Background</h2>
</section>

<!-- CSS color names -->
<section data-background-color="aquamarine">
  <h2>Aquamarine Background</h2>
</section>

<!-- Gradient -->
<section data-background-gradient="linear-gradient(to bottom, #283b95, #17b2c3)">
  <h2>Gradient Background</h2>
</section>
```

### Image Backgrounds

```html
<!-- Basic image -->
<section data-background-image="https://example.com/image.jpg">
  <h2>Image Background</h2>
</section>

<!-- With sizing -->
<section
  data-background-image="https://example.com/logo.png"
  data-background-size="200px"
  data-background-position="center"
  data-background-repeat="no-repeat">
  <h2>Sized Image</h2>
</section>

<!-- Cover entire slide -->
<section
  data-background-image="https://example.com/hero.jpg"
  data-background-size="cover">
  <h2>Full Cover Image</h2>
</section>

<!-- With opacity -->
<section
  data-background-image="https://example.com/texture.jpg"
  data-background-opacity="0.3">
  <h2>Semi-transparent Background</h2>
</section>
```

### Video Backgrounds

```html
<!-- Auto-playing video -->
<section
  data-background-video="https://example.com/video.mp4"
  data-background-video-loop
  data-background-video-muted>
  <h2>Video Background</h2>
</section>

<!-- Multiple formats for browser compatibility -->
<section
  data-background-video="video.mp4,video.webm"
  data-background-video-loop
  data-background-video-muted>
  <h2>Multi-format Video</h2>
</section>
```

### Iframe Backgrounds

```html
<!-- Embed a webpage as background -->
<section
  data-background-iframe="https://example.com"
  data-background-interactive>
  <h2>Interactive Web Background</h2>
</section>
```

### Background Transitions

```html
<!-- Custom transition for this slide's background -->
<section data-background-transition="zoom">
  <h2>Zoom Background Transition</h2>
</section>
```

**Available transitions**: none, fade, slide, convex, concave, zoom

### v7.5-main Integration

Add background support to your layout renderers:

```javascript
// In L25 or L29 renderer
function renderSlide(slideData) {
  const backgroundAttrs = [];

  if (slideData.background) {
    if (slideData.background.type === 'color') {
      backgroundAttrs.push(`data-background-color="${slideData.background.value}"`);
    } else if (slideData.background.type === 'image') {
      backgroundAttrs.push(`data-background-image="${slideData.background.url}"`);
      if (slideData.background.size) {
        backgroundAttrs.push(`data-background-size="${slideData.background.size}"`);
      }
      if (slideData.background.opacity) {
        backgroundAttrs.push(`data-background-opacity="${slideData.background.opacity}"`);
      }
    } else if (slideData.background.type === 'video') {
      backgroundAttrs.push(`data-background-video="${slideData.background.url}"`);
      backgroundAttrs.push(`data-background-video-loop`);
      backgroundAttrs.push(`data-background-video-muted`);
    }
  }

  return `<section ${backgroundAttrs.join(' ')}>
    <!-- Slide content -->
  </section>`;
}
```

---

## Auto-Animate

### Overview

Auto-Animate automatically animates elements that change between slides. Reveal.js matches elements and smoothly transitions:
- Position
- Size
- Color
- Opacity
- Padding/margins

### Basic Usage

```html
<!-- Slide 1 -->
<section data-auto-animate>
  <h1>Auto-Animate</h1>
</section>

<!-- Slide 2 -->
<section data-auto-animate>
  <h1 style="margin-top: 100px; color: red;">Auto-Animate</h1>
</section>
```

Result: The h1 smoothly moves down and changes color.

### Matching Elements

**By default**: Matched by text content

```html
<!-- Slide 1 -->
<section data-auto-animate>
  <div>Box</div>
</section>

<!-- Slide 2 -->
<section data-auto-animate>
  <div style="width: 200px;">Box</div>
</section>
```

**Using data-id**: More explicit matching

```html
<!-- Slide 1 -->
<section data-auto-animate>
  <div data-id="box">Box</div>
</section>

<!-- Slide 2 -->
<section data-auto-animate>
  <div data-id="box" style="transform: rotate(45deg);">Box</div>
</section>
```

### Configuration

```html
<!-- Custom easing -->
<section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">

<!-- Custom duration -->
<section data-auto-animate data-auto-animate-duration="2.0">

<!-- Delay animations -->
<section data-auto-animate data-auto-animate-delay="0.5">

<!-- Disable unmatched elements -->
<section data-auto-animate data-auto-animate-unmatched="false">
```

### Advanced Examples

**Code Evolution**:

```html
<!-- Slide 1 -->
<section data-auto-animate>
  <pre><code data-id="code">
    let x = 5;
  </code></pre>
</section>

<!-- Slide 2 -->
<section data-auto-animate>
  <pre><code data-id="code">
    let x = 5;
    let y = 10;
  </code></pre>
</section>

<!-- Slide 3 -->
<section data-auto-animate>
  <pre><code data-id="code">
    let x = 5;
    let y = 10;
    console.log(x + y);
  </code></pre>
</section>
```

**Chart Building**:

```html
<!-- Slide 1: Empty chart -->
<section data-auto-animate>
  <div data-id="chart" style="width: 400px; height: 300px; border: 1px solid #ccc;">
  </div>
</section>

<!-- Slide 2: Add first bar -->
<section data-auto-animate>
  <div data-id="chart" style="width: 400px; height: 300px; border: 1px solid #ccc;">
    <div data-id="bar1" style="width: 60%; height: 50px; background: blue;"></div>
  </div>
</section>

<!-- Slide 3: Add second bar -->
<section data-auto-animate>
  <div data-id="chart" style="width: 400px; height: 300px; border: 1px solid #ccc;">
    <div data-id="bar1" style="width: 60%; height: 50px; background: blue;"></div>
    <div data-id="bar2" style="width: 80%; height: 50px; background: green;"></div>
  </div>
</section>
```

### v7.5-main Integration

Enable auto-animate for related slides:

```javascript
// Mark related slides with data-auto-animate
function renderAnimatedSequence(slides) {
  return slides.map(slide => `
    <section data-auto-animate>
      ${renderSlideContent(slide)}
    </section>
  `).join('');
}
```

---

## Vertical Slides

### Overview

Create hierarchical presentations with main topics (horizontal) and subtopics (vertical).

```
Home → Topic 1 → Topic 2 → Topic 3
           ↓         ↓        ↓
       Subtopic  Subtopic  Subtopic
           ↓         ↓        ↓
       Details   Details   Details
```

### Basic Structure

```html
<div class="slides">
  <!-- Horizontal slide 1 -->
  <section>
    <h1>Topic 1</h1>
  </section>

  <!-- Horizontal slide 2 with vertical slides -->
  <section>
    <section>
      <h1>Topic 2</h1>
      <p>Press down arrow for details</p>
    </section>
    <section>
      <h2>Subtopic 2.1</h2>
    </section>
    <section>
      <h2>Subtopic 2.2</h2>
    </section>
  </section>

  <!-- Horizontal slide 3 -->
  <section>
    <h1>Topic 3</h1>
  </section>
</div>
```

### Navigation

- **Left/Right arrows**: Navigate horizontally
- **Up/Down arrows**: Navigate vertically
- **Space**: Navigate to next slide (right or down)

### Navigation Modes

Configure how vertical slides behave:

```javascript
Reveal.initialize({
  navigationMode: 'default',  // Free navigation in all directions
  // OR
  navigationMode: 'linear',   // Left/right through all slides sequentially
  // OR
  navigationMode: 'grid'      // Restrict to grid navigation
});
```

### Vertical Slide Indicators

Show dots indicating vertical slides:

```javascript
Reveal.initialize({
  showSlideNumber: 'all',     // Show numbers like "2.3" for vertical slides
  controls: true,             // Show arrow controls
  controlsTutorial: true,     // Show pulsing arrows on first view
});
```

### JavaScript API

```javascript
// Check if vertical slide
Reveal.isVerticalSlide();        // Returns true if on vertical slide

// Navigate vertically
Reveal.up();                     // Go up one vertical slide
Reveal.down();                   // Go down one vertical slide

// Get slide indices
const indices = Reveal.getIndices();
// Returns: { h: 2, v: 1, f: 0 }
// h = horizontal, v = vertical, f = fragment

// Navigate to specific slide
Reveal.slide(2, 1);             // Go to slide 2, vertical slide 1
```

### v7.5-main Consideration

Vertical slides might be complex for v7.5-main's current architecture. Consider:
- Keep presentations flat (horizontal only) for simplicity
- OR allow optional vertical structure for advanced users
- Update slide count logic to handle h×v slides

---

## Available Plugins

### Core Plugins (Included with Reveal.js)

#### 1. **RevealNotes** - Speaker Notes
```javascript
import RevealNotes from 'reveal.js/plugin/notes/notes.js';

Reveal.initialize({
  plugins: [ RevealNotes ]
});
```

#### 2. **RevealHighlight** - Code Syntax Highlighting
```javascript
import RevealHighlight from 'reveal.js/plugin/highlight/highlight.js';

Reveal.initialize({
  plugins: [ RevealHighlight ]
});
```

```html
<section>
  <pre><code class="javascript">
    function hello() {
      console.log('Hello World!');
    }
  </code></pre>
</section>
```

#### 3. **RevealMarkdown** - Markdown Content
```javascript
import RevealMarkdown from 'reveal.js/plugin/markdown/markdown.js';

Reveal.initialize({
  plugins: [ RevealMarkdown ]
});
```

```html
<section data-markdown>
  ## Slide Title
  - Bullet 1
  - Bullet 2
</section>
```

#### 4. **RevealSearch** - Full-Text Search
```javascript
import RevealSearch from 'reveal.js/plugin/search/search.js';

Reveal.initialize({
  plugins: [ RevealSearch ]
});
```

**Usage**: Press **CTRL+Shift+F** to search

#### 5. **RevealZoom** - Element Zoom
```javascript
import RevealZoom from 'reveal.js/plugin/zoom/zoom.js';

Reveal.initialize({
  plugins: [ RevealZoom ]
});
```

**Usage**: **Alt+Click** on any element to zoom in

#### 6. **RevealMath** - Mathematical Equations
```javascript
import RevealMath from 'reveal.js/plugin/math/math.js';

Reveal.initialize({
  plugins: [ RevealMath ]
});
```

```html
<section>
  <p>Inline: $E = mc^2$</p>
  <p>Block: $$\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$</p>
</section>
```

### Plugin Loading Example

```html
<script type="module">
  import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.esm.js';
  import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.esm.js';
  import RevealSearch from 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/search/search.esm.js';
  import RevealHighlight from 'https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.esm.js';

  Reveal.initialize({
    plugins: [ RevealNotes, RevealSearch, RevealHighlight ]
  });
</script>
```

---

## JavaScript API Reference

### Navigation Methods

```javascript
// Basic navigation
Reveal.next();                   // Next slide (right or down)
Reveal.prev();                   // Previous slide (left or up)
Reveal.right();                  // Next horizontal slide
Reveal.left();                   // Previous horizontal slide
Reveal.up();                     // Previous vertical slide
Reveal.down();                   // Next vertical slide

// Direct navigation
Reveal.slide(h, v, f);          // Go to slide (horizontal, vertical, fragment)
Reveal.slide(2);                // Go to horizontal slide 2
Reveal.slide(2, 1);             // Go to slide 2, vertical slide 1

// Fragment navigation
Reveal.nextFragment();          // Show next fragment
Reveal.prevFragment();          // Show previous fragment

// Special navigation
Reveal.navigateNext();          // Smart next (considers fragments)
Reveal.navigatePrev();          // Smart previous (considers fragments)
Reveal.navigateLeft();          // Navigate left
Reveal.navigateRight();         // Navigate right
Reveal.navigateUp();            // Navigate up
Reveal.navigateDown();          // Navigate down
```

### State Methods

```javascript
// Slide information
Reveal.getTotalSlides();        // Total number of slides
Reveal.getCurrentSlide();       // Current slide DOM element
Reveal.getSlides();             // Array of all slide elements
Reveal.getIndices();            // { h: 0, v: 0, f: -1 }
Reveal.getProgress();           // 0-1 representing progress
Reveal.getScale();              // Current scale factor

// Slide state checks
Reveal.isFirstSlide();          // Is this the first slide?
Reveal.isLastSlide();           // Is this the last slide?
Reveal.isVerticalSlide();       // Is this a vertical slide?

// Navigation state
Reveal.availableRoutes();       // { left: false, right: true, up: false, down: true }
Reveal.availableFragments();   // { prev: false, next: true }

// Mode checks
Reveal.isOverview();            // Is overview mode active?
Reveal.isPaused();              // Is presentation paused?
Reveal.isAutoSliding();         // Is auto-slide active?

// Configuration
Reveal.getConfig();             // Get all configuration
Reveal.configure({              // Update configuration
  controls: false
});
```

### Control Methods

```javascript
// View modes
Reveal.toggleOverview();        // Toggle overview mode
Reveal.toggleOverview(true);    // Show overview
Reveal.toggleOverview(false);   // Hide overview
Reveal.togglePause();           // Toggle pause mode
Reveal.toggleHelp();            // Toggle help overlay

// Presentation controls
Reveal.sync();                  // Force sync of state
Reveal.syncSlide();             // Sync current slide
Reveal.syncFragments();         // Sync fragments

// Layout
Reveal.layout();                // Force layout recalculation
Reveal.shuffle();               // Randomize slide order
```

### Plugin Methods

```javascript
// Plugin access
Reveal.getPlugin('notes');      // Get notes plugin instance
Reveal.getPlugins();            // Get all loaded plugins
Reveal.hasPlugin('search');     // Check if plugin loaded
```

---

## Event System

### Available Events

```javascript
// Lifecycle events
Reveal.on('ready', function(event) {
  // Fired when Reveal.js finishes loading
  console.log('Reveal.js ready');
});

// Slide change events
Reveal.on('slidechanged', function(event) {
  // event.previousSlide, event.currentSlide, event.indexh, event.indexv
  console.log('Slide changed to:', event.indexh, event.indexv);
});

Reveal.on('slidetransitionend', function(event) {
  // Fired after slide transition animation completes
});

// Fragment events
Reveal.on('fragmentshown', function(event) {
  // event.fragment = DOM element
  console.log('Fragment shown:', event.fragment);
});

Reveal.on('fragmenthidden', function(event) {
  console.log('Fragment hidden:', event.fragment);
});

// Overview events
Reveal.on('overviewshown', function() {
  console.log('Overview mode activated');
});

Reveal.on('overviewhidden', function() {
  console.log('Overview mode deactivated');
});

// Auto-slide events
Reveal.on('autoslidepaused', function() {});
Reveal.on('autoslideresumed', function() {});

// Other events
Reveal.on('paused', function() {});
Reveal.on('resumed', function() {});
Reveal.on('resize', function() {});
```

### Event Handler Methods

```javascript
// Add event listener
Reveal.on('slidechanged', function(event) {
  // Handle event
});

// Remove event listener
const handler = function(event) { /* ... */ };
Reveal.on('slidechanged', handler);
Reveal.off('slidechanged', handler);

// One-time event listener
Reveal.once('ready', function() {
  // Only fires once
});
```

### Practical Examples

**Track Slide Views**:

```javascript
Reveal.on('slidechanged', function(event) {
  analytics.track('Slide Viewed', {
    slide: event.indexh,
    vertical: event.indexv,
    title: event.currentSlide.querySelector('h1, h2')?.textContent
  });
});
```

**Update URL Hash**:

```javascript
Reveal.on('slidechanged', function(event) {
  window.location.hash = `/${event.indexh}/${event.indexv}`;
});
```

**Show Progress**:

```javascript
Reveal.on('slidechanged', function() {
  const progress = Reveal.getProgress() * 100;
  document.getElementById('progress').textContent = `${Math.round(progress)}%`;
});
```

**Lazy Load Content**:

```javascript
Reveal.on('slidechanged', function(event) {
  // Load images for current and next slide only
  const currentSlide = event.currentSlide;
  const nextSlide = currentSlide.nextElementSibling;

  [currentSlide, nextSlide].forEach(slide => {
    if (slide) {
      slide.querySelectorAll('[data-src]').forEach(img => {
        img.src = img.dataset.src;
      });
    }
  });
});
```

---

## Configuration Options

### Complete Configuration Reference

```javascript
Reveal.initialize({
  // Presentation size
  width: 1920,                    // Base width
  height: 1080,                   // Base height
  margin: 0.04,                   // Margin as fraction of width/height
  minScale: 0.2,                  // Minimum scale (zoom out)
  maxScale: 2.0,                  // Maximum scale (zoom in)

  // Display
  controls: true,                 // Show navigation arrows
  controlsLayout: 'bottom-right', // Position: edges | bottom-right
  controlsBackArrows: 'faded',    // Visibility: faded | hidden | visible
  progress: true,                 // Show progress bar
  slideNumber: false,             // Show slide numbers
  showSlideNumber: 'all',         // When to show: all | speaker | print
  hashOneBasedIndex: false,       // Use 1-based slide numbers in URL
  hash: false,                    // Enable URL hash
  respondToHashChanges: true,     // Respond to URL hash changes

  // Navigation
  history: false,                 // Browser history
  keyboard: true,                 // Keyboard shortcuts
  keyboardCondition: null,        // Condition for keyboard: null | 'focused'
  disableLayout: false,           // Disable responsive layout
  overview: true,                 // Enable overview mode
  center: true,                   // Vertical centering
  touch: true,                    // Touch navigation
  loop: false,                    // Loop presentation
  rtl: false,                     // Right-to-left text direction
  navigationMode: 'default',      // Navigation: default | linear | grid
  shuffle: false,                 // Randomize slide order
  fragments: true,                // Enable fragments
  fragmentInURL: true,            // Fragments in URL
  embedded: false,                // Is embedded in iframe?
  help: true,                     // Show help overlay (? key)
  pause: true,                    // Enable pause (B or . key)
  showNotes: false,               // Show speaker notes
  autoPlayMedia: null,            // Auto-play media: null | true | false
  preloadIframes: null,           // Preload iframes: null | true | false
  autoAnimate: true,              // Enable auto-animate
  autoAnimateMatcher: null,       // Custom element matching function
  autoAnimateEasing: 'ease',      // Default easing
  autoAnimateDuration: 1.0,       // Default duration (seconds)
  autoAnimateUnmatched: true,     // Animate unmatched elements

  // Auto-slide
  autoSlide: 0,                   // Auto-advance interval (ms), 0 = disabled
  autoSlideStoppable: true,       // Stop on user input
  autoSlideMethod: null,          // Custom navigation method
  defaultTiming: null,            // Default slide duration

  // Mouse
  mouseWheel: false,              // Mouse wheel navigation
  rollingLinks: false,            // 3D link rolling effect
  hideInactiveCursor: true,       // Hide cursor after delay
  hideCursorTime: 5000,           // Delay before hiding cursor (ms)

  // Transitions
  transition: 'slide',            // Transition: none | fade | slide | convex | concave | zoom
  transitionSpeed: 'default',     // Speed: default | fast | slow
  backgroundTransition: 'fade',   // Background transition style

  // Parallax
  parallaxBackgroundImage: '',    // Parallax background image URL
  parallaxBackgroundSize: '',     // Background size (CSS syntax)
  parallaxBackgroundRepeat: '',   // Repeat: repeat | no-repeat
  parallaxBackgroundPosition: '', // Position: center | top left | etc.
  parallaxBackgroundHorizontal: null,  // Horizontal movement amount
  parallaxBackgroundVertical: null,    // Vertical movement amount

  // Presentation mode
  display: 'block',               // Display mode for slides
  hideAddressBar: true,           // Hide address bar on mobile

  // PDF export
  pdfMaxPagesPerSlide: Number.POSITIVE_INFINITY,  // Slide splitting
  pdfSeparateFragments: true,     // Export fragments as separate pages
  pdfPageHeightOffset: -1,        // Page height adjustment

  // Plugins
  plugins: []                     // Array of plugin instances
});
```

### Commonly Used Configurations

**Basic Presentation**:
```javascript
Reveal.initialize({
  controls: true,
  progress: true,
  history: true,
  center: true,
  transition: 'slide'
});
```

**Full-Screen Presentation** (v7.5-main style):
```javascript
Reveal.initialize({
  width: 1920,
  height: 1080,
  margin: 0,
  minScale: 1,
  maxScale: 1,
  controls: true,
  progress: true,
  slideNumber: true,
  hash: true,
  center: false,
  transition: 'slide'
});
```

**Auto-Playing Presentation**:
```javascript
Reveal.initialize({
  autoSlide: 5000,           // 5 seconds per slide
  loop: true,                // Loop forever
  autoSlideStoppable: true,  // Stop on user input
  transition: 'fade'
});
```

**Kiosk Mode** (no controls):
```javascript
Reveal.initialize({
  controls: false,
  progress: false,
  keyboard: false,
  touch: false,
  autoSlide: 3000,
  loop: true
});
```

---

## Keyboard Shortcuts

### Default Shortcuts

**Navigation**:
- **← / ↑**: Previous slide
- **→ / ↓**: Next slide
- **Space**: Next slide
- **Shift+Space**: Previous slide
- **Home**: First slide
- **End**: Last slide

**View Modes**:
- **ESC / O**: Toggle overview mode
- **F**: Toggle fullscreen
- **S**: Open speaker notes (if plugin loaded)
- **B / .**: Toggle pause/blackout
- **?: Show help overlay

**Fragments**:
- **← / ↑**: Previous fragment
- **→ / ↓**: Next fragment

**Search**:
- **CTRL+Shift+F**: Open search (if plugin loaded)

**Zoom**:
- **ALT+Click**: Zoom to element (if plugin loaded)

### v7.5-main Custom Shortcuts

(Already implemented in viewer.html):
- **G**: Toggle grid borders
- **B**: Toggle section borders
- **C**: Toggle controls

### Adding Custom Shortcuts

```javascript
// Add custom keyboard bindings
Reveal.addKeyBinding(
  { keyCode: 84, key: 'T', description: 'Toggle Theme' },
  function() {
    // Toggle between themes
    const themes = ['white', 'black', 'league'];
    const current = Reveal.getConfig().theme || 'white';
    const next = themes[(themes.indexOf(current) + 1) % themes.length];

    document.getElementById('theme').setAttribute('href', `theme-${next}.css`);
  }
);

// Add shortcut with modifier keys
Reveal.addKeyBinding(
  { keyCode: 80, key: 'P', description: 'Print' },
  function() {
    window.print();
  }
);

// Remove a default key binding
Reveal.removeKeyBinding(32); // Remove space bar binding
```

### Disabling Keyboard Navigation

```javascript
// Disable all keyboard shortcuts
Reveal.initialize({
  keyboard: false
});

// Disable specific shortcuts
Reveal.initialize({
  keyboard: {
    27: null,  // Disable ESC (overview toggle)
    32: null   // Disable space (next slide)
  }
});

// Custom key handlers
Reveal.initialize({
  keyboard: {
    39: 'next',           // Right arrow: next slide
    37: 'prev',           // Left arrow: previous slide
    40: function() {      // Down arrow: custom function
      console.log('Custom down handler');
    }
  }
});
```

---

## Frontend Integration Examples

### React Integration

**Complete React Component**:

```typescript
import React, { useEffect, useState, useRef } from 'react';

interface RevealControlsProps {
  presentationId: string;
}

export function RevealControls({ presentationId }: RevealControlsProps) {
  const [isOverview, setIsOverview] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [currentSlide, setCurrentSlide] = useState({ h: 0, v: 0 });
  const [totalSlides, setTotalSlides] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Wait for Reveal to be ready
    const initializeControls = () => {
      if (typeof Reveal === 'undefined') {
        setTimeout(initializeControls, 100);
        return;
      }

      // Set initial state
      setTotalSlides(Reveal.getTotalSlides());
      const indices = Reveal.getIndices();
      setCurrentSlide({ h: indices.h, v: indices.v });
      setProgress(Reveal.getProgress());

      // Event listeners
      Reveal.on('slidechanged', handleSlideChanged);
      Reveal.on('overviewshown', () => setIsOverview(true));
      Reveal.on('overviewhidden', () => setIsOverview(false));
      Reveal.on('paused', () => setIsPaused(true));
      Reveal.on('resumed', () => setIsPaused(false));
    };

    initializeControls();

    return () => {
      if (typeof Reveal !== 'undefined') {
        Reveal.off('slidechanged', handleSlideChanged);
        Reveal.off('overviewshown');
        Reveal.off('overviewhidden');
        Reveal.off('paused');
        Reveal.off('resumed');
      }
    };
  }, []);

  const handleSlideChanged = (event: any) => {
    setCurrentSlide({ h: event.indexh, v: event.indexv });
    setProgress(Reveal.getProgress());
  };

  const toggleOverview = () => {
    if (typeof Reveal !== 'undefined') {
      Reveal.toggleOverview();
    }
  };

  const togglePause = () => {
    if (typeof Reveal !== 'undefined') {
      Reveal.togglePause();
    }
  };

  const openSpeakerView = () => {
    if (typeof Reveal !== 'undefined') {
      const notesPlugin = Reveal.getPlugin('notes');
      if (notesPlugin) {
        notesPlugin.open();
      } else {
        alert('Speaker notes plugin not loaded');
      }
    }
  };

  const navigateTo = (direction: 'left' | 'right' | 'up' | 'down') => {
    if (typeof Reveal !== 'undefined') {
      Reveal[direction]();
    }
  };

  return (
    <div className="reveal-controls">
      {/* Navigation */}
      <div className="nav-controls">
        <button onClick={() => navigateTo('left')} title="Previous">
          ←
        </button>
        <button onClick={() => navigateTo('up')} title="Up">
          ↑
        </button>
        <button onClick={() => navigateTo('down')} title="Down">
          ↓
        </button>
        <button onClick={() => navigateTo('right')} title="Next">
          →
        </button>
      </div>

      {/* View Controls */}
      <div className="view-controls">
        <button onClick={toggleOverview}>
          {isOverview ? '📋 Slide View' : '🔲 Grid View'}
        </button>
        <button onClick={togglePause}>
          {isPaused ? '▶️ Resume' : '⏸️ Pause'}
        </button>
        <button onClick={openSpeakerView}>
          🎤 Speaker View
        </button>
      </div>

      {/* Progress Info */}
      <div className="progress-info">
        <span>
          Slide {currentSlide.h + 1}
          {currentSlide.v > 0 && `.${currentSlide.v + 1}`} of {totalSlides}
        </span>
        <span>{Math.round(progress * 100)}%</span>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress * 100}%` }}
        />
      </div>
    </div>
  );
}
```

### Vue 3 Integration

```vue
<template>
  <div class="reveal-controls">
    <button @click="toggleOverview">
      {{ isOverview ? '📋 Slide View' : '🔲 Grid View' }}
    </button>
    <button @click="togglePause">
      {{ isPaused ? '▶️ Resume' : '⏸️ Pause' }}
    </button>
    <button @click="openSpeakerView">
      🎤 Speaker View
    </button>

    <div class="slide-info">
      Slide {{ currentSlide.h + 1 }} of {{ totalSlides }}
      ({{ Math.round(progress * 100) }}%)
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const isOverview = ref(false);
const isPaused = ref(false);
const currentSlide = ref({ h: 0, v: 0 });
const totalSlides = ref(0);
const progress = ref(0);

const handleSlideChanged = (event: any) => {
  currentSlide.value = { h: event.indexh, v: event.indexv };
  progress.value = (window as any).Reveal.getProgress();
};

const toggleOverview = () => {
  (window as any).Reveal?.toggleOverview();
};

const togglePause = () => {
  (window as any).Reveal?.togglePause();
};

const openSpeakerView = () => {
  const Reveal = (window as any).Reveal;
  const notesPlugin = Reveal?.getPlugin('notes');
  if (notesPlugin) {
    notesPlugin.open();
  }
};

onMounted(() => {
  const Reveal = (window as any).Reveal;
  if (Reveal) {
    totalSlides.value = Reveal.getTotalSlides();
    const indices = Reveal.getIndices();
    currentSlide.value = { h: indices.h, v: indices.v };

    Reveal.on('slidechanged', handleSlideChanged);
    Reveal.on('overviewshown', () => (isOverview.value = true));
    Reveal.on('overviewhidden', () => (isOverview.value = false));
    Reveal.on('paused', () => (isPaused.value = true));
    Reveal.on('resumed', () => (isPaused.value = false));
  }
});

onUnmounted(() => {
  const Reveal = (window as any).Reveal;
  if (Reveal) {
    Reveal.off('slidechanged', handleSlideChanged);
  }
});
</script>
```

### Vanilla JavaScript Integration

```javascript
// Presentation Controller Class
class PresentationController {
  constructor() {
    this.state = {
      isOverview: false,
      isPaused: false,
      currentSlide: { h: 0, v: 0 },
      totalSlides: 0,
      progress: 0
    };

    this.initialize();
  }

  initialize() {
    if (typeof Reveal === 'undefined') {
      setTimeout(() => this.initialize(), 100);
      return;
    }

    this.state.totalSlides = Reveal.getTotalSlides();
    this.updateState();
    this.attachEventListeners();
    this.createUI();
  }

  attachEventListeners() {
    Reveal.on('slidechanged', (event) => {
      this.state.currentSlide = { h: event.indexh, v: event.indexv };
      this.state.progress = Reveal.getProgress();
      this.updateUI();
    });

    Reveal.on('overviewshown', () => {
      this.state.isOverview = true;
      this.updateUI();
    });

    Reveal.on('overviewhidden', () => {
      this.state.isOverview = false;
      this.updateUI();
    });
  }

  createUI() {
    const container = document.createElement('div');
    container.className = 'presentation-controls';
    container.innerHTML = `
      <button id="overview-btn">Grid View</button>
      <button id="speaker-btn">Speaker View</button>
      <div id="slide-info"></div>
      <div class="progress-bar">
        <div id="progress-fill"></div>
      </div>
    `;

    document.body.appendChild(container);

    document.getElementById('overview-btn').addEventListener('click', () => {
      Reveal.toggleOverview();
    });

    document.getElementById('speaker-btn').addEventListener('click', () => {
      const notesPlugin = Reveal.getPlugin('notes');
      if (notesPlugin) notesPlugin.open();
    });

    this.updateUI();
  }

  updateUI() {
    const overviewBtn = document.getElementById('overview-btn');
    if (overviewBtn) {
      overviewBtn.textContent = this.state.isOverview ? 'Slide View' : 'Grid View';
    }

    const slideInfo = document.getElementById('slide-info');
    if (slideInfo) {
      slideInfo.textContent = `Slide ${this.state.currentSlide.h + 1} of ${this.state.totalSlides}`;
    }

    const progressFill = document.getElementById('progress-fill');
    if (progressFill) {
      progressFill.style.width = `${this.state.progress * 100}%`;
    }
  }

  updateState() {
    const indices = Reveal.getIndices();
    this.state.currentSlide = { h: indices.h, v: indices.v };
    this.state.progress = Reveal.getProgress();
  }
}

// Initialize controller when page loads
window.addEventListener('load', () => {
  new PresentationController();
});
```

---

## Implementation Recommendations

### Quick Wins (High Value, Easy to Implement)

#### 1. **Document Overview Mode** ⭐⭐⭐⭐⭐
**Effort**: 5 minutes
**Value**: High - Users likely don't know this exists

**Action Items**:
- Add "Grid View" button to UI
- Show tooltip: "Press ESC or O for grid view"
- Update documentation

**Code**:
```javascript
<button onClick={() => Reveal.toggleOverview()} title="Press ESC or O">
  🔲 Grid View
</button>
```

#### 2. **Enable Speaker Notes** ⭐⭐⭐⭐⭐
**Effort**: 30 minutes
**Value**: High - Essential for presenters

**Action Items**:
- Add RevealNotes plugin to viewer.html
- Generate speaker notes from slide metadata
- Add "Speaker View" button

**Implementation**: See [Speaker Notes section](#speaker-notes--presenter-view)

#### 3. **Add Search Plugin** ⭐⭐⭐⭐
**Effort**: 15 minutes
**Value**: High - Quick slide finding

**Action Items**:
- Add RevealSearch plugin
- Document CTRL+Shift+F shortcut
- Consider adding search button in UI

#### 4. **Fragment Support** ⭐⭐⭐⭐
**Effort**: 1-2 hours
**Value**: Medium-High - Better storytelling

**Action Items**:
- Update renderers to support fragment classes
- Add UI to control fragment behavior
- Test with bullet points and charts

---

### Medium Priority (Moderate Effort, Good Value)

#### 5. **Background Support** ⭐⭐⭐
**Effort**: 2-3 hours
**Value**: Medium - Visual enhancement

**Action Items**:
- Extend slide model to include background options
- Update renderers to generate background attributes
- Add color/image/gradient support

#### 6. **Auto-Animate** ⭐⭐⭐
**Effort**: 3-4 hours
**Value**: Medium - Smooth transitions

**Action Items**:
- Identify slide sequences that should animate
- Add data-auto-animate attributes
- Test with code examples and charts

#### 7. **Custom Keyboard Shortcuts** ⭐⭐⭐
**Effort**: 1 hour
**Value**: Medium - Better navigation

**Action Items**:
- Add shortcuts for common actions
- Create help overlay (? key)
- Document all shortcuts

---

### Advanced Features (Higher Effort)

#### 8. **Code Highlighting** ⭐⭐
**Effort**: 2-3 hours
**Value**: Low-Medium - Only if technical presentations needed

**Condition**: Only if users create technical presentations

#### 9. **Math Support** ⭐⭐
**Effort**: 2-3 hours
**Value**: Low - Only if equations needed

**Condition**: Only if users create scientific/mathematical presentations

#### 10. **Vertical Slides** ⭐
**Effort**: 5+ hours
**Value**: Low-Medium - Adds complexity

**Consideration**: May complicate v7.5-main's architecture. Consider for v8 only.

---

## Code Examples

### Complete Integration Example

**Enhanced viewer.html with all recommended features**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>v7.5 Presentation Viewer</title>

  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/white.css">

  <!-- Plugin CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/monokai.css">

  <style>
    /* Custom controls */
    .custom-controls {
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 100;
      display: flex;
      gap: 10px;
    }

    .custom-controls button {
      padding: 10px 15px;
      background: rgba(0, 0, 0, 0.7);
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 14px;
    }

    .custom-controls button:hover {
      background: rgba(0, 0, 0, 0.9);
    }

    /* Progress indicator */
    .slide-progress {
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.7);
      color: white;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 14px;
      z-index: 100;
    }
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides" id="presentation-slides">
      <!-- Slides will be inserted here -->
    </div>
  </div>

  <!-- Custom UI -->
  <div class="custom-controls">
    <button id="overview-btn" title="Press ESC or O">🔲 Grid View</button>
    <button id="speaker-btn" title="Press S">🎤 Speaker View</button>
    <button id="help-btn" title="Press ?">❓ Help</button>
  </div>

  <div class="slide-progress" id="slide-progress">
    Slide 1 of 1
  </div>

  <!-- Reveal.js and Plugins -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/search/search.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>

  <script>
    // Initialize Reveal.js
    Reveal.initialize({
      // Display
      controls: true,
      progress: true,
      slideNumber: true,
      hash: true,
      history: true,

      // Navigation
      keyboard: true,
      overview: true,
      center: false,

      // Presentation size
      width: 1920,
      height: 1080,
      margin: 0,
      minScale: 1,
      maxScale: 1,

      // Transitions
      transition: 'slide',

      // Fragments
      fragments: true,
      fragmentInURL: true,

      // Auto-animate
      autoAnimate: true,
      autoAnimateDuration: 1.0,

      // Plugins
      plugins: [
        RevealNotes,
        RevealSearch,
        RevealHighlight
      ]
    }).then(() => {
      console.log('Reveal.js initialized');
      setupCustomControls();
      loadPresentation();
    });

    // Custom controls
    function setupCustomControls() {
      // Overview button
      document.getElementById('overview-btn').addEventListener('click', () => {
        Reveal.toggleOverview();
      });

      // Speaker view button
      document.getElementById('speaker-btn').addEventListener('click', () => {
        const notesPlugin = Reveal.getPlugin('notes');
        if (notesPlugin) {
          notesPlugin.open();
        } else {
          alert('Speaker notes plugin not loaded');
        }
      });

      // Help button
      document.getElementById('help-btn').addEventListener('click', () => {
        Reveal.toggleHelp();
      });

      // Update progress
      Reveal.on('slidechanged', updateProgress);
      Reveal.on('overviewshown', () => {
        document.getElementById('overview-btn').textContent = '📋 Slide View';
      });
      Reveal.on('overviewhidden', () => {
        document.getElementById('overview-btn').textContent = '🔲 Grid View';
      });

      updateProgress();
    }

    function updateProgress() {
      const indices = Reveal.getIndices();
      const total = Reveal.getTotalSlides();
      const progress = Math.round(Reveal.getProgress() * 100);

      document.getElementById('slide-progress').textContent =         `Slide ${indices.h + 1} of ${total} (${progress}%)`;
    }

    // Load presentation from API
    async function loadPresentation() {
      const presentationId = window.location.pathname.split('/p/')[1];

      try {
        const response = await fetch(`/api/presentations/${presentationId}`);
        const data = await response.json();

        // Render slides
        const slidesHTML = data.slides.map(slide => renderSlide(slide)).join('');
        document.getElementById('presentation-slides').innerHTML = slidesHTML;

        // Sync Reveal.js
        Reveal.sync();
        updateProgress();

      } catch (error) {
        console.error('Failed to load presentation:', error);
      }
    }

    function renderSlide(slideData) {
      // Generate slide HTML based on layout
      // Add fragments, backgrounds, etc.
      return `<section>${slideData.html}</section>`;
    }
  </script>
</body>
</html>
```

---

## Summary

### Current State
- v7.5-main uses ~20% of Reveal.js capabilities
- Basic navigation and display features enabled
- Huge untapped potential

### Key Discoveries

1. **⭐ Slide Overview/Sorter EXISTS** - Already enabled, just needs UI button
2. **Speaker Notes** - Powerful presenter view available
3. **Fragments** - Step-by-step reveals for better storytelling
4. **Rich API** - 50+ JavaScript methods for custom features
5. **Plugin System** - Search, highlighting, math support ready to use

### Recommended Next Steps

**Phase 1: Quick Wins (Week 1)**
1. Add "Grid View" button for overview mode
2. Enable speaker notes plugin
3. Add search plugin
4. Document keyboard shortcuts

**Phase 2: Enhancement (Week 2-3)**
5. Implement fragment support in renderers
6. Add background support (color/image)
7. Create custom keyboard shortcuts
8. Add progress indicators

**Phase 3: Advanced (Future)**
9. Auto-animate for smooth transitions
10. Code highlighting (if needed)
11. Math support (if needed)
12. Vertical slides (v8 consideration)

### Resources

- **Reveal.js Documentation**: https://revealjs.com/
- **API Reference**: https://revealjs.com/api/
- **Plugins**: https://revealjs.com/plugins/
- **Examples**: https://revealjs.com/demo/

---

**End of Guide**

For questions or clarifications about implementing these features in v7.5-main, consult this guide or the official Reveal.js documentation.
