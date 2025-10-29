# GUI Testing Guide - Chrome-Inspired Modern Design

Complete testing checklist for the upgraded File Downloader GUI v2.1.0

## Installation & Setup

### Install Dependencies
```bash
pip install -r requirements-gui.txt
```

### Launch GUI
```bash
python launch_gui.py
```

## Visual Design Testing

### 🎨 Chrome-Inspired Design Elements

**Expected:** Modern, clean interface inspired by Chrome's design language

Test checklist:
- [ ] Header with large icon and title
- [ ] Rounded corners on all cards (12px radius)
- [ ] Proper spacing and padding
- [ ] Card-based layout (elevated appearance)
- [ ] Modern color scheme
- [ ] Clean typography with proper font weights
- [ ] Smooth color transitions
- [ ] Professional status bar at bottom

## Feature Testing

### 1. Header Section

**Elements to test:**
- [ ] Large file downloader icon (📥) displays correctly
- [ ] "File Downloader" title is bold and prominent
- [ ] Theme toggle button works (☀️ Light / 🌙 Dark)
- [ ] About button shows dialog with app info
- [ ] Header has appropriate background color

**Test theme toggle:**
1. Click "☀️ Light" button
2. Verify interface changes to light mode
3. Verify button text changes to "🌙 Dark"
4. Click again to return to dark mode
5. Verify smooth color transition

**Test about dialog:**
1. Click "ℹ️ About" button
2. Verify dialog shows version 2.1.0
3. Verify features list is displayed
4. Close dialog and verify app continues working

### 2. URL Input Card

**Design elements:**
- [ ] Card has rounded corners and elevated appearance
- [ ] "Enter URLs" label is bold
- [ ] Helper text shows "One URL per line • Supports HTTP/HTTPS"
- [ ] Textbox has border and proper styling
- [ ] Clear and Validate buttons are styled correctly

**Test URL input:**
1. Click in URL textbox
2. Verify placeholder text clears automatically
3. Paste multiple URLs (one per line)
4. Verify text wraps properly
5. Verify scrolling works for many URLs

**Test Clear button:**
1. Add some URLs
2. Click "🗑️ Clear" button
3. Verify all URLs are removed
4. Verify status bar shows "URLs cleared"

**Test Validate button:**
1. Add mix of valid and invalid URLs:
   ```
   https://example.com/file.jpg
   invalid-url
   https://test.com/image.png
   not-a-url
   ```
2. Click "✓ Validate URLs" button
3. Verify dialog shows count of valid/invalid URLs
4. Verify invalid URLs are listed
5. Verify status bar updates

### 3. Output Directory Card

**Design elements:**
- [ ] Card with folder icon (📁)
- [ ] "Save to:" label
- [ ] Entry field shows current directory
- [ ] "Browse" button is prominent
- [ ] "📂 Open" button to open folder

**Test Browse:**
1. Click "Browse" button
2. Navigate to a different folder
3. Select folder
4. Verify path updates in entry field
5. Verify status bar confirms change

**Test Open Folder:**
1. Click "📂 Open" button
2. Verify file manager opens
3. Verify correct folder opens
4. Test with non-existent folder (should show warning)

### 4. Download Button

**Visual states to test:**

**Normal state:**
- [ ] Blue background (#1f6aa5 dark, #144870 darker)
- [ ] Text: "⬇ Start Download"
- [ ] Height: 45px
- [ ] Rounded corners (10px)
- [ ] Bold text
- [ ] Hover effect (slightly darker)

**Downloading state:**
- [ ] Gray background
- [ ] Text: "⏳ Downloading..."
- [ ] Disabled (no hover)

**Test functionality:**
1. Without URLs - should show warning
2. With URLs - should start download
3. While downloading - should be disabled
4. After complete - should re-enable

### 5. Downloads List Section

**Header elements:**
- [ ] "Downloads" label (bold, size 15)
- [ ] "⏸ Stop All" button (initially disabled)
- [ ] "🗑 Clear List" button (always enabled)

**Empty state:**
- [ ] Large download icon (📥, size 48)
- [ ] "No downloads yet" message (bold, gray)
- [ ] Hint text: "Add URLs above..."
- [ ] Centered in scrollable area

**Test Stop All button:**
1. Start multiple downloads
2. Click "⏸ Stop All"
3. Verify all active downloads are cancelled
4. Verify status bar updates
5. Verify button disables when no active downloads

**Test Clear List button:**
1. Complete some downloads
2. Click "🗑 Clear List"
3. Verify only completed/failed items removed
4. Verify active downloads remain
5. Verify empty state shows if all cleared
6. Test with no items (should show info dialog)

### 6. Download Item Cards

**Modern card design:**
- [ ] White background (light) / Gray20 (dark)
- [ ] Rounded corners (10px)
- [ ] Proper padding (15px)
- [ ] File icon (📄, size 20)
- [ ] URL/filename bold at top
- [ ] Progress bar in middle (height 8px, rounded)
- [ ] Status text at bottom
- [ ] Cancel button (✕) on right

**Progress states to test:**

**Waiting:**
```
📄 https://example.com/file.jpg     ✕
   ▱▱▱▱▱▱▱▱▱▱ 0%
   ⏳ Waiting...
```

**Connecting:**
```
📄 https://example.com/file.jpg     ✕
   ▱▱▱▱▱▱▱▱▱▱ 0%
   🔍 Connecting...
```

**Downloading:**
```
📄 file.jpg                         ✕
   ▓▓▓▓▓▓▱▱▱▱ 65%
   ⬇ 1.3 MB / 2.0 MB • 2.5 MB/s
```

**Complete:**
```
📄 file.jpg                         ✓
   ▓▓▓▓▓▓▓▓▓▓ 100%
   ✓ Complete • 2.00 MB • 1.2s
```

**Failed:**
```
📄 file.jpg                         ✕
   ▱▱▱▱▱▱▱▱▱▱ 0%
   ✗ HTTP Error: 404
```

**Cancelled:**
```
📄 file.jpg                         ✕
   ▓▓▱▱▱▱▱▱▱▱ 30%
   ✕ Cancelled
```

**Test cancel individual download:**
1. Start a download
2. Click ✕ button while downloading
3. Verify download stops
4. Verify status shows "✕ Cancelled"
5. Verify button becomes disabled
6. Verify stats update (failed count)

### 7. Status Bar

**Elements:**
- [ ] Colored status indicator (●)
- [ ] Status text (left-aligned)
- [ ] Statistics (right-aligned): "Total: X • Success: Y • Failed: Z"
- [ ] Height: 45px
- [ ] Bottom of window

**Status colors to test:**
- [ ] Green: Ready, successful completion
- [ ] Blue: Downloading, validating
- [ ] Orange: Warnings, partial failures
- [ ] Red: Errors
- [ ] Gray: Neutral messages

**Messages to verify:**
- [ ] "Ready to download" (green) - initial state
- [ ] "Downloading X file(s)..." (blue) - during download
- [ ] "URLs cleared" (gray) - after clearing URLs
- [ ] "Output directory: ..." (blue) - after browsing
- [ ] "Validated: X valid, Y invalid" (blue) - after validation
- [ ] "✓ All X file(s) downloaded successfully!" (green) - all success
- [ ] "Download complete: X succeeded, Y failed" (orange) - mixed results
- [ ] "Stopping all downloads..." (orange) - when stopping
- [ ] "Cleared X item(s)" (gray) - after clearing list

**Test stats counter:**
1. Start fresh (0 • 0 • 0)
2. Download 3 files (3 • 3 • 0)
3. Fail 1 download (4 • 3 • 1)
4. Cancel 1 download (5 • 3 • 2)
5. Verify counters are accurate

## Functional Testing

### Test Case 1: Single File Download

**Steps:**
1. Launch GUI
2. Clear URL field
3. Paste valid URL: `https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore`
4. Keep default download directory
5. Click "⬇ Start Download"

**Expected:**
- [ ] Empty state disappears
- [ ] Download card appears
- [ ] Status: Connecting → Downloading → Complete
- [ ] Progress bar fills from 0% to 100%
- [ ] Download speed shows (MB/s)
- [ ] File size shows correctly
- [ ] Completion time displays
- [ ] Success message appears
- [ ] Stats update (Total: 1, Success: 1, Failed: 0)
- [ ] Download button re-enables

### Test Case 2: Multiple File Downloads

**Steps:**
1. Clear URL field
2. Add 3 valid URLs (one per line)
3. Click "⬇ Start Download"

**Expected:**
- [ ] All 3 cards appear immediately
- [ ] Downloads start sequentially
- [ ] Each shows individual progress
- [ ] Status updates independently for each
- [ ] Completion message shows total statistics
- [ ] All progress bars reach 100%

### Test Case 3: Error Handling - Invalid URL

**Steps:**
1. Enter: `https://httpbin.org/status/404`
2. Start download

**Expected:**
- [ ] Connection attempt shows
- [ ] Error status appears: "✗ HTTP Error: 404"
- [ ] Progress bar stays at 0%
- [ ] Status text is red
- [ ] Cancel button remains enabled
- [ ] Failed counter increments
- [ ] Warning dialog appears at end

### Test Case 4: Error Handling - Connection Error

**Steps:**
1. Enter invalid domain: `https://invalid-domain-xyz-123.com/file.jpg`
2. Start download

**Expected:**
- [ ] Shows "🔍 Connecting..."
- [ ] After timeout: "✗ Connection failed"
- [ ] Status text is red
- [ ] Failed counter increments

### Test Case 5: Cancel During Download

**Steps:**
1. Start downloading a large file
2. While progress is at ~30%, click ✕ button

**Expected:**
- [ ] Download stops immediately
- [ ] Status: "✕ Cancelled" (orange)
- [ ] Progress bar shows partial progress
- [ ] Partial file is deleted
- [ ] Failed counter increments
- [ ] Cancel button disables

### Test Case 6: Stop All Downloads

**Steps:**
1. Start 5 downloads
2. Let 2 complete
3. Click "⏸ Stop All"

**Expected:**
- [ ] 3 active downloads cancelled
- [ ] 2 completed downloads unaffected
- [ ] Status: "Stopping all downloads..."
- [ ] All cancel buttons disable
- [ ] Failed counter increases by 3

### Test Case 7: Clear Completed Downloads

**Steps:**
1. Have mix of completed, failed, and active downloads
2. Click "🗑 Clear List"

**Expected:**
- [ ] Only completed/failed items removed
- [ ] Active downloads remain
- [ ] If all cleared, empty state shows
- [ ] Status confirms clearing

### Test Case 8: Theme Toggle

**Steps:**
1. Start with dark mode
2. Toggle to light mode during a download
3. Toggle back to dark

**Expected:**
- [ ] All colors change smoothly
- [ ] Download continues uninterrupted
- [ ] All text remains readable
- [ ] Progress bars visible in both themes
- [ ] Status indicators clear in both themes

### Test Case 9: Custom Output Directory

**Steps:**
1. Click Browse
2. Select Desktop (or another folder)
3. Download a file
4. Click "📂 Open" to verify

**Expected:**
- [ ] Path updates in entry
- [ ] File downloads to selected location
- [ ] Folder opens correctly
- [ ] Path persists for session

### Test Case 10: URL Validation

**Steps:**
1. Enter mix of valid and invalid URLs:
```
https://example.com/valid1.jpg
not-a-url-at-all
https://test.com/valid2.png
ftp://unsupported.com/file.zip
http://valid3.com/file.pdf
just-some-text
```
2. Click "✓ Validate URLs"

**Expected:**
- [ ] Dialog shows: "Found 3 invalid URL(s)"
- [ ] Lists invalid URLs
- [ ] Shows valid count
- [ ] Status bar confirms validation

## User Experience Testing

### Responsiveness

**Test window resizing:**
1. Resize to minimum (900x650)
2. Verify all elements visible
3. Resize to large (1920x1080)
4. Verify layout scales properly
5. Verify scrolling works for long download lists

### Performance

**Test with many downloads:**
1. Add 20 URLs
2. Start download
3. Monitor GUI responsiveness

**Expected:**
- [ ] GUI remains responsive
- [ ] Progress updates smooth
- [ ] No lag in scrolling
- [ ] Stats update correctly
- [ ] Memory usage reasonable

### Edge Cases

**Test empty URL field:**
- [ ] Shows warning dialog
- [ ] Download doesn't start

**Test whitespace-only URLs:**
- [ ] Ignored/filtered out
- [ ] No empty cards created

**Test very long URL:**
- [ ] Truncates in display (adds ...)
- [ ] Full URL used for download
- [ ] Tooltip could show full URL

**Test special characters in URL:**
- [ ] Properly encoded/decoded
- [ ] Filename extracted correctly

**Test simultaneous actions:**
- [ ] Can't start download while one running
- [ ] Theme toggle works during download
- [ ] Can browse directory during download
- [ ] Can clear list while downloading

## Accessibility Testing

**Keyboard navigation:**
- [ ] Tab moves between fields
- [ ] Enter in URL field doesn't close window
- [ ] Buttons accessible via keyboard

**Visual clarity:**
- [ ] All text readable in both themes
- [ ] Sufficient contrast ratios
- [ ] Icons clear and meaningful
- [ ] Status colors distinguishable

## Bug Checklist

Common issues to test for:
- [ ] No memory leaks during long sessions
- [ ] Progress bar animates smoothly
- [ ] No UI freezing during downloads
- [ ] Dialogs don't block unnecessarily
- [ ] Empty state shows/hides correctly
- [ ] Stats counter never goes negative
- [ ] Download directory creation works
- [ ] File overwrite handling (if file exists)
- [ ] Cancel cleans up partial files
- [ ] Error messages are helpful
- [ ] No crashes on invalid input

## Final Checklist

**Visual polish:**
- [ ] All spacing consistent
- [ ] All corners properly rounded
- [ ] All colors appropriate
- [ ] All fonts properly weighted
- [ ] All icons aligned

**Functionality:**
- [ ] All buttons work
- [ ] All features tested
- [ ] No console errors
- [ ] Clean error handling
- [ ] Proper state management

**User experience:**
- [ ] Intuitive workflow
- [ ] Clear feedback for all actions
- [ ] No confusing states
- [ ] Helpful error messages
- [ ] Professional appearance

## Test Scenarios Summary

| Scenario | Status | Notes |
|----------|--------|-------|
| Single download | ⬜ | Test with small file |
| Multiple downloads | ⬜ | Test with 3-5 files |
| Invalid URL | ⬜ | Should show clear error |
| Network error | ⬜ | Connection timeout |
| Cancel download | ⬜ | Should cleanup |
| Stop all | ⬜ | Bulk cancellation |
| Clear list | ⬜ | Remove completed |
| Theme toggle | ⬜ | Both themes work |
| Custom directory | ⬜ | Browse and save |
| URL validation | ⬜ | Detect invalid |
| Empty state | ⬜ | Shows correctly |
| Status updates | ⬜ | All messages clear |
| Progress tracking | ⬜ | Accurate percentages |
| Open folder | ⬜ | Opens correctly |
| About dialog | ⬜ | Shows info |

## Reporting Issues

When reporting issues, include:
1. Python version: `python --version`
2. OS and version
3. Steps to reproduce
4. Expected vs actual behavior
5. Screenshots if visual issue
6. Console output if error

## Test Environment

- **OS:** Windows / macOS / Linux
- **Python:** 3.7+
- **CustomTkinter:** 5.2.0+
- **Screen Resolution:** Note for responsive testing
- **Theme Tested:** Dark / Light / Both

---

**Testing completed:** [ ] Yes [ ] No
**Date:** _____________
**Tester:** _____________
**Issues found:** _____________
**All features working:** [ ] Yes [ ] No

