# File Downloader CLI

A simple and efficient Python command-line tool to download files (images, videos, documents, etc.) from URLs.

## Features

- Download any file type (images, videos, PDFs, etc.)
- Progress bar showing download status
- Support for multiple URLs in a single command
- Custom output directory
- Custom filename for downloads
- Automatic filename detection from URL or server headers
- File size display
- Overwrite protection

## Installation

1. Clone this repository or download the files

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests tqdm
```

3. Make the script executable (optional, for Unix/Linux/Mac):
```bash
chmod +x downloader.py
```

## Usage

### Basic Usage

Download a single file:
```bash
python downloader.py https://example.com/image.jpg
```

### Download with Custom Filename

```bash
python downloader.py https://example.com/video.mp4 -o my_video.mp4
```

### Download to Custom Directory

```bash
python downloader.py https://example.com/file.pdf -d ./my_downloads
```

### Download Multiple Files

```bash
python downloader.py https://example.com/image1.jpg https://example.com/image2.jpg https://example.com/video.mp4
```

## Command-Line Options

```
usage: downloader.py [-h] [-o OUTPUT] [-d DIRECTORY] urls [urls ...]

Download files from URLs (images, videos, etc.)

positional arguments:
  urls                  URL(s) to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filename (only works with single URL)
  -d DIRECTORY, --directory DIRECTORY
                        Output directory (default: downloads)
```

## Examples

### Download an image:
```bash
python downloader.py https://example.com/photo.jpg
```

### Download a video with custom name:
```bash
python downloader.py https://example.com/video.mp4 -o vacation_2024.mp4
```

### Download multiple files:
```bash
python downloader.py \
  https://example.com/image1.png \
  https://example.com/image2.png \
  https://example.com/document.pdf
```

### Download to a specific folder:
```bash
python downloader.py https://example.com/report.pdf -d ~/Documents/Reports
```

## Supported File Types

This tool can download any file type accessible via HTTP/HTTPS, including:

- Images: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`, etc.
- Videos: `.mp4`, `.avi`, `.mkv`, `.mov`, `.webm`, etc.
- Audio: `.mp3`, `.wav`, `.flac`, `.m4a`, etc.
- Documents: `.pdf`, `.doc`, `.docx`, `.txt`, etc.
- Archives: `.zip`, `.tar`, `.gz`, `.rar`, etc.
- And any other file type accessible via URL

## Requirements

- Python 3.6 or higher
- `requests` library
- `tqdm` library

## License

MIT License - Feel free to use and modify as needed.

## Troubleshooting

### Downloads folder not found
The tool automatically creates a `downloads` folder in the current directory if it doesn't exist.

### File already exists
If a file with the same name exists, the tool will ask if you want to overwrite it.

### Network errors
Make sure you have an active internet connection and the URL is accessible.

### Permission errors
Ensure you have write permissions in the output directory.

## Contributing

Feel free to submit issues or pull requests to improve this tool!
