# Testing the File Downloader CLI

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `requests` - HTTP library
- `typer` - CLI framework
- `rich` - Beautiful terminal output

### 2. Basic Tests

#### Test 1: Display Help
```bash
python downloader.py --help
python downloader.py download --help
```

#### Test 2: Show Version
```bash
python downloader.py version
```

#### Test 3: Show Tool Information
```bash
python downloader.py info
```

#### Test 4: Download a Small File
```bash
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
```

#### Test 5: Download with Custom Filename
```bash
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o my_gitignore.txt
```

#### Test 6: Download to a Custom Directory
```bash
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -d test_downloads
```

#### Test 7: Download Multiple Files
```bash
python downloader.py download \
  https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore \
  https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore
```

#### Test 8: Force Overwrite Mode
```bash
# Download the same file twice with force flag
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -f
```

#### Test 9: Quiet Mode
```bash
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -q
```

## Public Test URLs

Here are some publicly accessible URLs you can use for testing:

### Small Text Files (Fast Downloads)
```bash
# Python gitignore
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# JavaScript gitignore
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Java gitignore
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Java.gitignore
```

### Images (Replace with actual public URLs)
```bash
# You can use any publicly accessible image URL
python downloader.py download https://your-public-image-url.com/image.jpg
```

### Multiple Files Test
```bash
python downloader.py download \
  https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore \
  https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore \
  https://raw.githubusercontent.com/github/gitignore/main/Go.gitignore
```

## Expected Output Examples

### Successful Single Download

```
╭──────────────── 📥 File Downloader ────────────────╮
│ Output Directory: /path/to/downloads               │
│ Files to Download: 1                               │
╰────────────────────────────────────────────────────╯

🔍 Fetching: https://example.com/file.txt
📥 Downloading to: downloads/file.txt
⠋ file.txt ━━━━━━━━━━━━━━━━ 100% 13.3 kB 1.2 MB/s 0:00:00
✓ Successfully downloaded: downloads/file.txt
File size: 0.01 MB
```

### Successful Multiple Downloads with Summary

```
╭──────────────── 📥 File Downloader ────────────────╮
│ Output Directory: /path/to/downloads               │
│ Files to Download: 3                               │
╰────────────────────────────────────────────────────╯

🔍 Fetching: https://example.com/file1.txt
📥 Downloading to: downloads/file1.txt
⠋ file1.txt ━━━━━━━━━━━━━━ 100% 1.2 kB 500 kB/s 0:00:00
✓ Successfully downloaded: downloads/file1.txt
File size: 0.00 MB

🔍 Fetching: https://example.com/file2.txt
📥 Downloading to: downloads/file2.txt
⠋ file2.txt ━━━━━━━━━━━━━━ 100% 2.5 kB 800 kB/s 0:00:00
✓ Successfully downloaded: downloads/file2.txt
File size: 0.00 MB

🔍 Fetching: https://example.com/file3.txt
📥 Downloading to: downloads/file3.txt
⠋ file3.txt ━━━━━━━━━━━━━━ 100% 3.1 kB 950 kB/s 0:00:00
✓ Successfully downloaded: downloads/file3.txt
File size: 0.00 MB

───────────────────────── Summary ─────────────────────────
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Status ┃ URL                     ┃ Saved To             ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ ✓      │ https://example.com/... │ downloads/file1.txt  │
│ ✓      │ https://example.com/... │ downloads/file2.txt  │
│ ✓      │ https://example.com/... │ downloads/file3.txt  │
└────────┴─────────────────────────┴──────────────────────┘

✓ Successful: 3 | ✗ Failed: 0
```

### File Already Exists (Without Force)

```
🔍 Fetching: https://example.com/file.txt
File 'file.txt' already exists. Overwrite? [y/N]: n
⚠️  Download cancelled.
```

### Error - HTTP 404

```
🔍 Fetching: https://example.com/nonexistent.txt
✗ HTTP Error: 404 Client Error: Not Found for url: ...
```

### Error - Connection Error

```
🔍 Fetching: https://invalid-domain-that-does-not-exist.com/file.txt
✗ Connection Error: Unable to connect to the server
```

## Manual Testing Checklist

### Basic Functionality
- [ ] Help command works (`--help`)
- [ ] Version command works (`version`)
- [ ] Info command works (`info`)
- [ ] Single file download works
- [ ] File is actually saved to disk
- [ ] File size matches expected size
- [ ] Progress bar displays correctly

### Options Testing
- [ ] Custom filename (`-o`) works
- [ ] Custom directory (`-d`) works
- [ ] Force overwrite (`-f`) bypasses confirmation
- [ ] Quiet mode (`-q`) minimizes output
- [ ] Multiple URLs work together

### Error Handling
- [ ] Invalid URL shows error
- [ ] Network error handled gracefully
- [ ] 404 error shows appropriate message
- [ ] Ctrl+C cancels download cleanly
- [ ] Partial downloads are cleaned up on cancel

### Edge Cases
- [ ] URL without filename works (uses default)
- [ ] Overwrite prompt works correctly
- [ ] Large file download works
- [ ] Multiple simultaneous downloads work
- [ ] Summary table displays correctly

## Automated Testing

### Run All Basic Tests
Create a test script:

```bash
#!/bin/bash

echo "Test 1: Help"
python downloader.py --help

echo -e "\n\nTest 2: Version"
python downloader.py version

echo -e "\n\nTest 3: Info"
python downloader.py info

echo -e "\n\nTest 4: Single Download"
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

echo -e "\n\nTest 5: Custom Name"
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore -o node_test.txt

echo -e "\n\nTest 6: Custom Directory"
python downloader.py download https://raw.githubusercontent.com/github/gitignore/main/Go.gitignore -d test_dir

echo -e "\n\nTest 7: Multiple Downloads"
python downloader.py download \
  https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore \
  https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

echo -e "\n\nAll tests completed!"
```

## Performance Testing

### Test Download Speed
```bash
# Download a larger file to test progress bar and speed display
python downloader.py download <URL-to-large-file>
```

### Test Multiple Downloads
```bash
# Test with 5+ URLs to see summary table
python downloader.py download URL1 URL2 URL3 URL4 URL5
```

## Cleanup After Testing

Remove test downloads:
```bash
rm -rf downloads/
rm -rf test_downloads/
rm -rf test_dir/
```

## Troubleshooting Test Issues

### Module Not Found
**Issue**: `ModuleNotFoundError: No module named 'typer'` or `'rich'`

**Solution**:
```bash
pip install -r requirements.txt
```

### Permission Denied
**Issue**: Cannot create downloads directory

**Solution**: Check write permissions or use a different directory:
```bash
python downloader.py download URL -d ~/Downloads
```

### Color Output Not Showing
**Issue**: Colors don't display in terminal

**Solution**: Rich automatically detects terminal capabilities. If colors don't show:
- Use a modern terminal (iTerm2, Windows Terminal, etc.)
- Check if `TERM` environment variable is set
- Colors may not work in some CI/CD environments

### Progress Bar Issues
**Issue**: Progress bar not displaying correctly

**Solution**:
- Ensure terminal width is sufficient (at least 80 characters)
- Some terminals don't support progress bars
- Try quiet mode (`-q`) if progress bars cause issues

## Using Your Own URLs

Test with your own files:
```bash
# Your own image
python downloader.py download https://yoursite.com/image.jpg

# Your own video
python downloader.py download https://yoursite.com/video.mp4 -d ~/Videos

# Your own document
python downloader.py download https://yoursite.com/doc.pdf -o important.pdf
```

## Integration Testing

### Test in Scripts
```bash
#!/bin/bash
# Download multiple files for a project

python downloader.py download \
  https://example.com/file1.jpg \
  https://example.com/file2.jpg \
  -d project_assets \
  -f

if [ $? -eq 0 ]; then
    echo "All files downloaded successfully!"
else
    echo "Some downloads failed!"
    exit 1
fi
```

### Test with Quiet Mode for Logs
```bash
# Good for automation and logging
python downloader.py download URL -q >> download.log 2>&1
```

## Advanced Testing

### Test with Different File Types
```bash
# Test image
python downloader.py download <image-url>

# Test video
python downloader.py download <video-url>

# Test PDF
python downloader.py download <pdf-url>

# Test ZIP
python downloader.py download <zip-url>
```

### Stress Test
```bash
# Download many files at once
python downloader.py download URL1 URL2 URL3 ... URL10
```

## Reporting Issues

When reporting issues, include:
1. Command you ran
2. Error message (full output)
3. Python version (`python --version`)
4. OS and terminal type
5. Output of `pip list | grep -E "(typer|rich|requests)"`

---

**Happy Testing! 🚀**
