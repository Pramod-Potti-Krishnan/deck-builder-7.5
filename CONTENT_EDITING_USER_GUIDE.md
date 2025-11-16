# Content Editing User Guide

Complete guide to using the content editing feature in v7.5-main.

---

## 🚀 Quick Start

### 1. Start the Server
```bash
cd agents/layout_builder_main/v7.5-main
python3 server.py
```

Server will start on: http://localhost:8504

### 2. Create a Test Presentation
```bash
# In another terminal
python3 test_editing_api.py
```

This creates a sample presentation and tests all API endpoints.

### 3. Open Presentation in Browser
```
http://localhost:8504/p/{presentation-id}
```

---

## ✏️ Using Edit Mode

### Entering Edit Mode

**Method 1: Click Button**
- Look for the blue "✏️ Edit Mode" button (top-right corner)
- Click it to activate editing

**Method 2: Keyboard Shortcut**
- Press the **E** key

### When Edit Mode is Active

You'll see:
- ✅ Red "EDIT MODE ACTIVE" banner at top
- ✅ Edit Mode button turns red
- ✅ Edit controls panel appears (top-right)
- ✅ Keyboard shortcuts guide (bottom-right)
- ✅ Dashed outlines appear when hovering over text

### Editing Content

1. **Hover over any text** - You'll see a dashed blue outline
2. **Click the text** - Outline becomes solid, cursor appears
3. **Type your changes** - Edit like any text editor
4. **Click outside** - Saves your edits to local state

**Editable Fields:**
- ✅ Slide titles
- ✅ Subtitles
- ✅ Body text
- ✅ Rich content areas
- ✅ Hero content (L29 slides)

**NOT Editable:**
- ❌ Charts and diagrams
- ❌ Company logos
- ❌ Footer presentation names

---

## 💾 Saving Changes

### Method 1: Click Save Button
- Click "💾 Save Changes" in the control panel

### Method 2: Keyboard Shortcut
- Press **Ctrl+S** (Windows/Linux) or **Cmd+S** (Mac)

### What Happens When You Save
1. All slide content is extracted
2. Each slide is updated via API
3. A version backup is created automatically
4. You see a success notification
5. Edit mode automatically exits
6. Page stays on current slide

**Success Message:**
```
✅ All changes saved! (3 slides updated)
```

---

## ❌ Canceling Edits

### Method 1: Click Cancel Button
- Click "❌ Cancel" in the control panel

### Method 2: Keyboard Shortcut
- Press **ESC** key

### What Happens When You Cancel
1. All changes are discarded
2. Original content is restored
3. Edit mode exits
4. No API calls are made
5. No version is created

**Cancel Message:**
```
❌ Changes discarded
```

---

## 📜 Version History

### Opening Version History

**Method 1: Click Button**
- Click "📜 Version History" in the control panel

**Method 2: API**
```
GET http://localhost:8504/api/presentations/{id}/versions
```

### Version History Modal

Shows all versions with:
- Version number (newest first)
- Creation date and time
- Creator (user, director_agent, system)
- Change summary
- Restore button

### Restoring a Version

1. Click "↺ Restore" button on any version
2. Confirm the action (popup appears)
3. Current state is backed up automatically
4. Selected version is restored
5. Page reloads to show restored content

**Restore Message:**
```
✅ Version restored! Reloading...
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **E** | Toggle Edit Mode on/off |
| **Ctrl+S** or **Cmd+S** | Save all changes |
| **ESC** | Cancel edits and exit |
| **?** | Show general help overlay |

---

## 🔔 Notifications

### Notification Types

**Info (Blue)** 📘
- Edit mode activated
- Version history loading
- General information

**Success (Green)** ✅
- Changes saved successfully
- Version restored

**Warning (Orange)** ⚠️
- Partial save (some slides failed)
- Non-critical issues

**Error (Red)** ❌
- Save failed
- API errors
- Version restore failed

### Notification Behavior
- Auto-hide after 3 seconds (except errors)
- Errors require click to dismiss
- Positioned at bottom-center
- Maximum 500px width

---

## 🧪 Testing the Feature

### Complete Test Workflow

1. **Start Server**
   ```bash
   python3 server.py
   ```

2. **Run Test Script**
   ```bash
   python3 test_editing_api.py
   ```

   This will output a presentation ID.

3. **Open in Browser**
   ```
   http://localhost:8504/p/{presentation-id}
   ```

4. **Test Edit Mode**
   - Press **E** to enter edit mode
   - Click slide title and change text
   - Click subtitle and change text
   - Press **Ctrl+S** to save
   - Verify changes persisted

5. **Test Version History**
   - Make another edit
   - Save again
   - Click "Version History"
   - Verify 2+ versions appear
   - Restore version 1
   - Verify content reverted

6. **Test Cancel**
   - Enter edit mode
   - Make changes (don't save)
   - Press **ESC**
   - Verify changes discarded

---

## 🛠️ API Testing (Advanced)

### Using FastAPI Docs

1. Open: http://localhost:8504/docs
2. Try these endpoints:

**Update Presentation Title**
```
PUT /api/presentations/{id}
Body: {"title": "New Title"}
```

**Update Slide Content**
```
PUT /api/presentations/{id}/slides/0
Body: {
  "slide_title": "Updated Title",
  "rich_content": "<div>Updated Content</div>"
}
```

**Get Version History**
```
GET /api/presentations/{id}/versions
```

**Restore Version**
```
POST /api/presentations/{id}/restore/{version_id}
Body: {"create_backup": true}
```

### Using cURL

**Update Slide 1 Title**
```bash
curl -X PUT "http://localhost:8504/api/presentations/{id}/slides/0" \
  -H "Content-Type: application/json" \
  -d '{"slide_title": "API Updated Title"}'
```

**Get Version History**
```bash
curl "http://localhost:8504/api/presentations/{id}/versions"
```

---

## 🐛 Troubleshooting

### Edit Mode Button Not Appearing
- **Check**: Server running on port 8504?
- **Check**: Browser console for JavaScript errors
- **Fix**: Hard refresh (Ctrl+Shift+R)

### Can't Edit Text
- **Check**: Is Edit Mode active? (Red banner at top)
- **Check**: Are you clicking on text fields?
- **Fix**: Press **E** to toggle edit mode

### Save Button Not Working
- **Check**: Browser console for network errors
- **Check**: Server logs for API errors
- **Fix**: Ensure server is running and accessible

### Version History Empty
- **Reason**: No edits have been saved yet
- **Fix**: Make an edit and save it
- **Note**: Version history is created on first save

### Page Not Reloading After Restore
- **Check**: Browser console for errors
- **Check**: Pop-up blockers enabled?
- **Fix**: Manually refresh the page

---

## 📊 What Gets Saved

### Text Content (Saved)
- ✅ Slide titles
- ✅ Subtitles
- ✅ Body text paragraphs
- ✅ Rich HTML content
- ✅ Hero slide content

### Non-Text Content (Not Saved via Edit Mode)
- ❌ Charts (requires regeneration via Analytics service)
- ❌ Diagrams (requires regeneration via Diagram service)
- ❌ Company logos (static assets)
- ❌ Layout structure (managed by Layout Builder)

**Note**: To update charts/diagrams, use the Director Agent or respective microservices.

---

## 🔒 Version History Details

### What's Stored
- Complete presentation state
- Timestamp (ISO format)
- Creator (user, director_agent, system)
- Change summary
- All slide content

### Storage Location
```
storage/versions/{presentation_id}/
  ├── index.json (version metadata)
  ├── v_20251116_141523_abc123.json (version 1)
  ├── v_20251116_142018_def456.json (version 2)
  └── ...
```

### Version Retention
- ✅ All versions kept indefinitely
- ✅ No automatic cleanup
- ✅ Manual cleanup via file system if needed

---

## 🚨 Important Notes

### Concurrency
- ⚠️ No real-time collaboration yet
- ⚠️ Last save wins (no conflict resolution)
- ✅ Recommendation: One editor at a time

### Data Persistence
- ✅ Changes saved to disk (JSON files)
- ✅ Survives server restarts
- ❌ Not in database (file-based for now)

### Browser Compatibility
- ✅ Chrome 88+ (tested)
- ✅ Firefox 78+ (tested)
- ✅ Safari 14+ (should work)
- ✅ Edge 88+ (should work)

---

## 📞 Support

### Check Logs
**Browser Console:**
- Press F12 → Console tab
- Look for errors or warnings

**Server Logs:**
- Check terminal where server is running
- Look for API errors or exceptions

### Common Error Messages

**"Presentation not found"**
- Invalid presentation ID in URL
- Presentation was deleted

**"Failed to update slide"**
- Server not running
- Network error
- Check server logs

**"Error loading version history"**
- Version history file corrupted
- Permissions issue
- Check storage/versions/ directory

---

## 🎯 Next Steps

### Phase 3 (Future Enhancements)

**Rich Text Editing**
- Formatting toolbar (bold, italic, lists)
- WYSIWYG editor integration
- Image upload

**Collaboration**
- Real-time multi-user editing
- Conflict resolution
- User cursors

**Templates**
- Pre-built slide templates
- Quick insert components
- Style library

**Advanced Version Control**
- Diff view between versions
- Branching/merging
- Comments on versions

---

## 📝 Example Workflow

### Complete Editing Session

1. **Start**: Open presentation
   ```
   http://localhost:8504/p/abc123
   ```

2. **Edit**: Press **E**, update slide 1 title to "Q4 Results"

3. **Save**: Press **Ctrl+S**
   - Notification: "✅ All changes saved!"
   - Version created automatically

4. **More Edits**: Update slide 2 subtitle to "Key Metrics"

5. **Save Again**: Press **Ctrl+S**
   - Another version created

6. **Check History**: Click "Version History"
   - See 2 versions listed

7. **Undo**: Restore version 1
   - Slide 2 subtitle reverts
   - Slide 1 title stays "Q4 Results"

8. **Exit**: Press **E** to view final presentation

---

**End of Guide**

For questions or issues, check:
- API Documentation: http://localhost:8504/docs
- Server logs: Terminal output
- Browser console: F12 → Console

Happy Editing! ✨
