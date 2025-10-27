#!/usr/bin/env python3
"""
File Downloader CLI Tool
A professional command-line tool to download files (images, videos, etc.) from URLs
Built with Typer for a modern CLI experience
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse, unquote

import typer
import requests
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TextColumn,
)
from rich.table import Table
from rich.panel import Panel

# Initialize Typer app and Rich console
app = typer.Typer(
    name="downloader",
    help="📥 Professional file downloader CLI - Download files from URLs with style!",
    add_completion=True,
)
console = Console()

# Version info
__version__ = "2.0.0"


class FileDownloader:
    """Enhanced file downloader with progress tracking"""

    def __init__(self, output_dir: Path = Path("downloads")):
        """Initialize the file downloader with an output directory"""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_filename_from_url(self, url: str) -> str:
        """Extract filename from URL"""
        parsed_url = urlparse(url)
        filename = unquote(os.path.basename(parsed_url.path))

        # If no filename in URL, use a default name
        if not filename or filename == "/" or filename == "":
            filename = "downloaded_file"

        return filename

    def get_filename_from_headers(self, response: requests.Response) -> Optional[str]:
        """Try to get filename from Content-Disposition header"""
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition and "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[1].strip('"\'')
            return unquote(filename)
        return None

    def download(
        self,
        url: str,
        output_filename: Optional[str] = None,
        force: bool = False,
        chunk_size: int = 8192,
    ) -> Optional[Path]:
        """
        Download a file from the given URL with Rich progress bar

        Args:
            url: URL to download from
            output_filename: Custom filename for the downloaded file
            force: Force overwrite if file exists
            chunk_size: Size of chunks to download at a time

        Returns:
            Path to the downloaded file or None if failed
        """
        try:
            console.print(f"[cyan]🔍 Fetching:[/cyan] {url}")

            # Send HEAD request first to get file info
            head_response = requests.head(url, allow_redirects=True, timeout=10)
            head_response.raise_for_status()

            # Get file size if available
            file_size = int(head_response.headers.get("content-length", 0))

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
            if output_path.exists() and not force:
                if not typer.confirm(
                    f"File '{filename}' already exists. Overwrite?", default=False
                ):
                    console.print("[yellow]⚠️  Download cancelled.[/yellow]")
                    return None

            # Download the file
            console.print(f"[green]📥 Downloading to:[/green] {output_path}")

            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Update file size from actual response if not available from HEAD
            if file_size == 0:
                file_size = int(response.headers.get("content-length", 0))

            # Download with Rich progress bar
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(
                    f"[cyan]{filename}", total=file_size if file_size > 0 else None
                )

                with open(output_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            file.write(chunk)
                            progress.update(task, advance=len(chunk))

            # Success message
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            console.print(
                f"[bold green]✓ Successfully downloaded:[/bold green] {output_path}"
            )
            console.print(f"[dim]File size: {file_size_mb:.2f} MB[/dim]")
            return output_path

        except requests.exceptions.HTTPError as e:
            console.print(f"[bold red]✗ HTTP Error:[/bold red] {e}", style="red")
            return None
        except requests.exceptions.ConnectionError:
            console.print(
                "[bold red]✗ Connection Error:[/bold red] Unable to connect to the server",
                style="red",
            )
            return None
        except requests.exceptions.Timeout:
            console.print(
                "[bold red]✗ Timeout Error:[/bold red] Request timed out", style="red"
            )
            return None
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]✗ Error downloading file:[/bold red] {e}")
            return None
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️  Download cancelled by user[/yellow]")
            # Clean up partial download
            if output_path and output_path.exists():
                output_path.unlink()
                console.print("[dim]Cleaned up partial download[/dim]")
            return None
        except Exception as e:
            console.print(f"[bold red]✗ Unexpected error:[/bold red] {e}")
            return None


@app.command()
def download(
    urls: List[str] = typer.Argument(
        ..., help="URL(s) to download. Can specify multiple URLs separated by space."
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output filename (only works with single URL)",
    ),
    directory: str = typer.Option(
        "downloads",
        "--directory",
        "-d",
        help="Output directory for downloaded files",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force overwrite existing files without confirmation",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Minimal output mode",
    ),
):
    """
    📥 Download files from URLs (images, videos, documents, etc.)

    Examples:

        $ downloader download https://example.com/image.jpg

        $ downloader download https://example.com/video.mp4 -o myvideo.mp4

        $ downloader download https://site.com/file1.jpg https://site.com/file2.jpg

        $ downloader download https://example.com/doc.pdf -d ~/Documents -f
    """
    # Validate arguments
    if len(urls) > 1 and output:
        console.print(
            "[bold red]Error:[/bold red] Cannot use --output with multiple URLs",
            style="red",
        )
        raise typer.Exit(1)

    # Create downloader
    output_dir = Path(directory)
    downloader = FileDownloader(output_dir=output_dir)

    if not quiet:
        console.print(
            Panel(
                f"[bold cyan]Output Directory:[/bold cyan] {output_dir.absolute()}\n"
                f"[bold cyan]Files to Download:[/bold cyan] {len(urls)}",
                title="📥 File Downloader",
                border_style="cyan",
            )
        )
        console.print()

    # Download files
    successful = 0
    failed = 0
    results = []

    for url in urls:
        result = downloader.download(url, output_filename=output, force=force)
        if result:
            successful += 1
            results.append((url, result, "✓"))
        else:
            failed += 1
            results.append((url, None, "✗"))

        # Add spacing between downloads if multiple URLs
        if len(urls) > 1 and not quiet:
            console.print()

    # Print summary if multiple downloads
    if len(urls) > 1 and not quiet:
        console.rule("[bold cyan]Summary[/bold cyan]")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Status", style="dim", width=6)
        table.add_column("URL")
        table.add_column("Saved To")

        for url, path, status in results:
            status_color = "green" if status == "✓" else "red"
            table.add_row(
                f"[{status_color}]{status}[/{status_color}]",
                url[:60] + "..." if len(url) > 60 else url,
                str(path) if path else "[red]Failed[/red]",
            )

        console.print(table)
        console.print(
            f"\n[bold green]✓ Successful:[/bold green] {successful} | "
            f"[bold red]✗ Failed:[/bold red] {failed}"
        )

    # Exit with appropriate code
    raise typer.Exit(0 if failed == 0 else 1)


@app.command()
def version():
    """Show version information"""
    console.print(
        Panel(
            f"[bold cyan]File Downloader CLI[/bold cyan]\n"
            f"Version: [green]{__version__}[/green]\n"
            f"Built with [magenta]Typer[/magenta] and [magenta]Rich[/magenta]",
            title="📥 Downloader Info",
            border_style="cyan",
        )
    )


@app.command()
def info():
    """Show information about the tool and supported features"""
    info_text = """
[bold cyan]Supported Features:[/bold cyan]

• Download any file type (images, videos, documents, archives, etc.)
• Beautiful progress bars with transfer speed and ETA
• Multiple file downloads in one command
• Custom output directory and filename
• Automatic filename detection from URL or server headers
• File overwrite protection with confirmation
• Force overwrite mode for automation
• Quiet mode for scripts
• Colored output for better readability
• Error handling for network issues

[bold cyan]Supported Protocols:[/bold cyan]

• HTTP/HTTPS

[bold cyan]Common File Types:[/bold cyan]

• Images: .jpg, .png, .gif, .webp, .svg, etc.
• Videos: .mp4, .avi, .mkv, .mov, .webm, etc.
• Audio: .mp3, .wav, .flac, .m4a, etc.
• Documents: .pdf, .doc, .docx, .txt, etc.
• Archives: .zip, .tar, .gz, .rar, etc.
    """
    console.print(
        Panel(info_text, title="📥 File Downloader Info", border_style="cyan")
    )


def main():
    """Main entry point"""
    app()


if __name__ == "__main__":
    main()
