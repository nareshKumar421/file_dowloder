#!/usr/bin/env python3
"""
File Downloader CLI Tool
A simple command-line tool to download files (images, videos, etc.) from URLs
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
from tqdm import tqdm


class FileDownloader:
    def __init__(self, output_dir="downloads"):
        """Initialize the file downloader with an output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_filename_from_url(self, url):
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))

        # If no filename in URL, use a default name
        if not filename or filename == '/':
            filename = 'downloaded_file'

        return filename

    def get_filename_from_headers(self, response):
        """Try to get filename from Content-Disposition header"""
        content_disposition = response.headers.get('Content-Disposition')
        if content_disposition:
            # Try to extract filename from Content-Disposition header
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')
                return unquote(filename)
        return None

    def download(self, url, output_filename=None, chunk_size=8192):
        """
        Download a file from the given URL

        Args:
            url: URL to download from
            output_filename: Custom filename for the downloaded file
            chunk_size: Size of chunks to download at a time

        Returns:
            Path to the downloaded file or None if failed
        """
        try:
            print(f"Fetching: {url}")

            # Send HEAD request first to get file info
            head_response = requests.head(url, allow_redirects=True, timeout=10)

            # Get file size if available
            file_size = int(head_response.headers.get('content-length', 0))

            # Determine filename
            if output_filename:
                filename = output_filename
            else:
                # Try to get filename from headers first
                filename = self.get_filename_from_headers(head_response)
                if not filename:
                    # Fall back to extracting from URL
                    filename = self.get_filename_from_url(url)

            output_path = self.output_dir / filename

            # Check if file already exists
            if output_path.exists():
                response = input(f"File '{filename}' already exists. Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print("Download cancelled.")
                    return None

            # Download the file
            print(f"Downloading to: {output_path}")

            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Update file size from actual response if not available from HEAD
            if file_size == 0:
                file_size = int(response.headers.get('content-length', 0))

            # Download with progress bar
            with open(output_path, 'wb') as file:
                if file_size > 0:
                    # Show progress bar with known file size
                    with tqdm(
                        total=file_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                        desc=filename
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))
                else:
                    # Download without progress bar if size unknown
                    print("Downloading... (size unknown)")
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)

            print(f"✓ Successfully downloaded: {output_path}")
            print(f"File size: {output_path.stat().st_size:,} bytes")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"✗ Error downloading file: {e}", file=sys.stderr)
            return None
        except KeyboardInterrupt:
            print("\n✗ Download cancelled by user")
            # Clean up partial download
            if output_path.exists():
                output_path.unlink()
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}", file=sys.stderr)
            return None


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Download files from URLs (images, videos, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://example.com/image.jpg
  %(prog)s https://example.com/video.mp4 -o my_video.mp4
  %(prog)s https://example.com/file.pdf -d ./my_downloads
  %(prog)s https://example.com/image.png https://example.com/video.mp4
        """
    )

    parser.add_argument(
        'urls',
        nargs='+',
        help='URL(s) to download'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output filename (only works with single URL)'
    )

    parser.add_argument(
        '-d', '--directory',
        default='downloads',
        help='Output directory (default: downloads)'
    )

    args = parser.parse_args()

    # Validate arguments
    if len(args.urls) > 1 and args.output:
        parser.error("Cannot use --output with multiple URLs")

    # Create downloader
    downloader = FileDownloader(output_dir=args.directory)

    print(f"Output directory: {downloader.output_dir.absolute()}\n")

    # Download files
    successful = 0
    failed = 0

    for url in args.urls:
        result = downloader.download(url, output_filename=args.output)
        if result:
            successful += 1
        else:
            failed += 1

        # Add spacing between downloads if multiple URLs
        if len(args.urls) > 1:
            print()

    # Print summary if multiple downloads
    if len(args.urls) > 1:
        print("-" * 50)
        print(f"Summary: {successful} successful, {failed} failed")

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
