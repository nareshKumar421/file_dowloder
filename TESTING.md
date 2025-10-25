# Testing the File Downloader

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Simple Tests

#### Test 1: Display Help
```bash
python downloader.py --help
```

#### Test 2: Download a Small PDF File
```bash
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
```

#### Test 3: Download with Custom Filename
```bash
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -o my_document.pdf
```

#### Test 4: Download to a Custom Directory
```bash
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -d test_downloads
```

#### Test 5: Download Multiple Files
```bash
python downloader.py \
  https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf \
  https://filesamples.com/samples/document/txt/sample1.txt
```

## Public Test URLs

Here are some publicly accessible URLs you can use for testing:

### Small Files (Fast Downloads)
- **Text File**: `https://filesamples.com/samples/document/txt/sample1.txt`
- **PDF File**: `https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf`
- **JSON File**: `https://jsonplaceholder.typicode.com/posts/1`

### Images
- **Sample Image 1**: `https://via.placeholder.com/600/92c952`
- **Sample Image 2**: `https://via.placeholder.com/600/771796`

### Larger Files (for Progress Bar Testing)
You can use any publicly accessible image, video, or file URL you have.

## What to Check

### After Each Test:
1. **Check the downloads folder**: `ls -lh downloads/` or `dir downloads`
2. **Verify file was downloaded**: The file should exist in the output directory
3. **Check file size**: Make sure the file isn't empty or corrupted
4. **Progress bar**: Did the progress bar display correctly?

### Expected Behavior:

✓ **Successful Download**:
```
Output directory: /path/to/file_dowloder/downloads

Fetching: https://example.com/file.pdf
Downloading to: downloads/file.pdf
file.pdf: 100%|███████████| 13.3k/13.3k [00:00<00:00, 1.20MB/s]
✓ Successfully downloaded: downloads/file.pdf
File size: 13,264 bytes
```

✓ **File Already Exists**:
```
File 'file.pdf' already exists. Overwrite? (y/n):
```

✓ **Error Handling**:
```
✗ Error downloading file: 404 Client Error: Not Found for url: ...
```

## Manual Testing Steps

### Step-by-Step:

1. **Test Help Command**
   ```bash
   python downloader.py --help
   ```
   Expected: Should show usage instructions

2. **Test Simple Download**
   ```bash
   python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
   ```
   Expected: Downloads to `downloads/dummy.pdf`

3. **Test Custom Name**
   ```bash
   python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -o renamed.pdf
   ```
   Expected: Downloads to `downloads/renamed.pdf`

4. **Test Custom Directory**
   ```bash
   python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -d my_files
   ```
   Expected: Downloads to `my_files/dummy.pdf`

5. **Test Overwrite Protection**
   - Download the same file twice
   - Second time should ask: "File 'dummy.pdf' already exists. Overwrite? (y/n):"

6. **Test Multiple Downloads**
   ```bash
   python downloader.py \
     https://via.placeholder.com/300 \
     https://via.placeholder.com/400
   ```
   Expected: Both files download with progress bars

7. **Test Invalid URL**
   ```bash
   python downloader.py https://invalid-url-that-does-not-exist.com/file.pdf
   ```
   Expected: Should show error message

## Using Your Own URLs

You can test with any publicly accessible URL:

```bash
# Your own image
python downloader.py https://yourwebsite.com/image.jpg

# Your own video
python downloader.py https://yourwebsite.com/video.mp4

# Your own document
python downloader.py https://yourwebsite.com/document.pdf
```

## Cleanup After Testing

Remove test downloads:
```bash
rm -rf downloads/
rm -rf test_downloads/
```

## Troubleshooting

### Issue: Module not found
**Solution**: Run `pip install -r requirements.txt`

### Issue: Permission denied
**Solution**: Make sure you have write permissions in the current directory

### Issue: SSL certificate errors
**Solution**: Your Python installation might need updated certificates

### Issue: 403 or 404 errors
**Solution**: The URL might be blocking automated downloads or doesn't exist
