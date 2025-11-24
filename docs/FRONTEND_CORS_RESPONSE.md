# Response to Frontend Team: Cross-Origin Iframe Access Solution

**Date**: 2025-01-24
**From**: Backend Team (v7.5-main)
**To**: Frontend Team
**Re**: CORS Request for Presentation Viewer Integration

---

## Executive Summary

We've implemented a **postMessage bridge** to enable cross-origin control of the presentation viewer. The solution is now **production-ready** and deployed.

**Status**: ✅ SOLVED - Ready for frontend integration

---

## What Was Wrong

### The Original Issue

Your BACKEND_CORS_REQUEST.md suggested that CORS headers would solve the iframe.contentWindow access problem. **This was based on incorrect information** in our integration guide.

### The Real Problem

**CORS headers do NOT enable cross-origin iframe access** - they only control HTTP requests (fetch, XHR).

When you try:
```javascript
const iframeWindow = iframe.contentWindow;
iframeWindow.Reveal.next(); // ❌ SecurityError
```

The browser blocks this due to the **Same-Origin Policy**, which is a security feature that **no HTTP headers can bypass**.

---

## The Solution: postMessage API

We've implemented a **postMessage bridge** in the viewer that allows cross-origin communication.

### How It Works

1. **Frontend sends commands** via `postMessage`
2. **Viewer receives and executes** the command
3. **Viewer sends response** back to frontend

### Implementation (Frontend Side)

Replace your direct `iframe.contentWindow` calls with `postMessage`:

#### ❌ Old Code (Doesn't Work Cross-Origin)
```javascript
// This fails cross-origin
const iframeWindow = iframe.contentWindow;
iframeWindow.Reveal.next();
```

#### ✅ New Code (Works Cross-Origin)
```javascript
// This works!
const iframe = document.getElementById('presentation-iframe');
iframe.contentWindow.postMessage(
  { action: 'nextSlide' },
  'https://web-production-f0d13.up.railway.app'
);
```

---

## Complete Integration Guide

### Step 1: Create Helper Function

Add this to your `/components/presentation-viewer.tsx`:

```typescript
const VIEWER_ORIGIN = 'https://web-production-f0d13.up.railway.app';

// Helper to send commands to the iframe
function sendCommand(
  iframe: HTMLIFrameElement,
  action: string,
  params?: Record<string, any>
): Promise<any> {
  return new Promise((resolve, reject) => {
    const handler = (event: MessageEvent) => {
      // Only accept messages from viewer origin
      if (event.origin !== VIEWER_ORIGIN) return;

      if (event.data.action === action) {
        window.removeEventListener('message', handler);

        if (event.data.success) {
          resolve(event.data);
        } else {
          reject(new Error(event.data.error || 'Command failed'));
        }
      }
    };

    window.addEventListener('message', handler);

    // Timeout after 5 seconds
    setTimeout(() => {
      window.removeEventListener('message', handler);
      reject(new Error('Command timeout'));
    }, 5000);

    iframe.contentWindow?.postMessage({ action, params }, VIEWER_ORIGIN);
  });
}
```

### Step 2: Update Your Button Handlers

Replace all button handlers with postMessage calls:

```typescript
// Previous slide
const handlePrevSlide = async () => {
  try {
    await sendCommand(iframeRef.current, 'prevSlide');
    console.log('⬅️ Previous slide');
  } catch (error) {
    console.error('Failed to navigate:', error);
  }
};

// Next slide
const handleNextSlide = async () => {
  try {
    await sendCommand(iframeRef.current, 'nextSlide');
    console.log('➡️ Next slide');
  } catch (error) {
    console.error('Failed to navigate:', error);
  }
};

// Toggle overview mode
const handleToggleOverview = async () => {
  try {
    const result = await sendCommand(iframeRef.current, 'toggleOverview');
    console.log('📊 Overview:', result.isOverview ? 'ON' : 'OFF');
  } catch (error) {
    console.error('Failed to toggle overview:', error);
  }
};

// Toggle edit mode
const handleToggleEdit = async () => {
  try {
    const result = await sendCommand(iframeRef.current, 'toggleEditMode');
    const isEditing = result.isEditing;
    console.log('✏️ Edit mode:', isEditing ? 'ON' : 'OFF');
    // Update your UI based on isEditing
  } catch (error) {
    console.error('Failed to toggle edit:', error);
  }
};

// Save changes
const handleSaveChanges = async () => {
  try {
    await sendCommand(iframeRef.current, 'saveAllChanges');
    console.log('💾 Changes saved');
  } catch (error) {
    console.error('Failed to save:', error);
  }
};

// Get current slide info (for counter)
const updateSlideCounter = async () => {
  try {
    const result = await sendCommand(iframeRef.current, 'getCurrentSlideInfo');
    const { index, total } = result.data;
    setSlideInfo(`${index} / ${total}`);
  } catch (error) {
    console.error('Failed to get slide info:', error);
  }
};
```

### Step 3: Update Slide Counter Polling

Replace your polling logic:

```typescript
useEffect(() => {
  const interval = setInterval(() => {
    if (iframeRef.current) {
      updateSlideCounter();
    }
  }, 500);

  return () => clearInterval(interval);
}, []);
```

---

## Available Commands

All commands from your original implementation are supported:

| Command | Description | Parameters | Response |
|---------|-------------|------------|----------|
| `nextSlide` | Navigate to next slide | None | `{ success: true }` |
| `prevSlide` | Navigate to previous slide | None | `{ success: true }` |
| `goToSlide` | Go to specific slide | `{ index: number }` | `{ success: true, slideIndex: number }` |
| `getCurrentSlideInfo` | Get current slide info | None | `{ success: true, data: { index, total, layoutId } }` |
| `toggleEditMode` | Toggle edit mode | None | `{ success: true, isEditing: boolean }` |
| `saveAllChanges` | Save all edits | None | `{ success: true }` |
| `cancelEdits` | Cancel edits | None | `{ success: true }` |
| `toggleOverview` | Toggle grid view | None | `{ success: true, isOverview: boolean }` |
| `isOverviewActive` | Check if overview active | None | `{ success: true, data: boolean }` |

---

## Security

The viewer validates message origins before executing commands. Only these origins are allowed:

- ✅ `localhost:*` (development)
- ✅ `127.0.0.1:*` (development)
- ✅ `*.up.railway.app` (Railway deployments)
- ✅ `*.vercel.app` (Vercel deployments)
- ✅ `*.netlify.app` (Netlify deployments)

Unauthorized origins are rejected with console warnings.

---

## Testing

### Quick Test

1. Update your button handlers with postMessage calls
2. Load a presentation in your frontend
3. Click "Next" button
4. Check browser console for: `📨 postMessage received: nextSlide`
5. Verify slide navigates

### Debugging

Open browser DevTools console in the iframe:
- Should see: `✅ postMessage bridge initialized`
- On each command: `📨 postMessage received: [action]`
- On each response: `📤 postMessage response sent`

---

## Migration Checklist

- [ ] Add `sendCommand` helper function to your codebase
- [ ] Update "Previous" button handler
- [ ] Update "Next" button handler
- [ ] Update "Grid/Overview" button handler
- [ ] Update "Edit" button handler
- [ ] Update "Save" button handler (if visible)
- [ ] Update slide counter polling logic
- [ ] Test all buttons work correctly
- [ ] Verify slide counter updates
- [ ] Check browser console for errors

---

## Updated Documentation

The integration guide has been updated with correct postMessage examples:

**Path**: `/agents/layout_builder_main/v7.5-main/docs/FRONTEND_INTEGRATION_GUIDE.md`
**Section**: "Cross-Origin Issues - postMessage Required" (lines 371-470)

All the incorrect CORS header suggestions have been removed and replaced with working postMessage examples.

---

## What Changed on Backend

### 1. postMessage Bridge (viewer/presentation-viewer.html)
- Added event listener for cross-origin messages
- Validates origin for security
- Executes commands and sends responses
- Logs all activity for debugging

### 2. Iframe Headers (server.py)
- Added `Content-Security-Policy: frame-ancestors *`
- Added `X-Frame-Options: ALLOWALL`
- These allow iframe embedding but don't affect JavaScript access

### 3. Documentation (FRONTEND_INTEGRATION_GUIDE.md)
- Removed misleading CORS section
- Added comprehensive postMessage documentation
- Included complete working examples

---

## Why This is Better

**Before** (Direct Access - Same-Origin Only):
```javascript
// ❌ Only works if frontend and viewer are same domain
iframeWindow.Reveal.next();
```

**After** (postMessage - Works Everywhere):
```javascript
// ✅ Works across any origin combination
sendCommand(iframe, 'nextSlide');
```

### Benefits:
- ✅ Works cross-origin (production setup)
- ✅ Works same-origin (development)
- ✅ Secure (origin validation)
- ✅ Standard browser API
- ✅ Promise-based (easier error handling)
- ✅ Future-proof architecture

---

## Deployment Status

**Status**: ✅ DEPLOYED to Railway Production

The postMessage bridge is live on:
```
https://web-production-f0d13.up.railway.app/p/{id}
```

You can start testing immediately.

---

## Need Help?

If you encounter any issues during migration:

1. Check browser console for postMessage logs
2. Verify iframe src URL is correct (`/p/{id}` not `/viewer/{id}`)
3. Confirm targetOrigin matches production URL
4. Review updated integration guide for examples

**Contact**: Backend Team
**Reference Docs**: `/docs/FRONTEND_INTEGRATION_GUIDE.md`

---

## Timeline

- **Implemented**: 2025-01-24
- **Deployed**: 2025-01-24
- **Ready for Integration**: NOW

---

**Thank you for reporting this issue! The updated implementation is much more robust and follows web security best practices.**
