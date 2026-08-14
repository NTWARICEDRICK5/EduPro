#!/usr/bin/env python3
"""Safely organize the direct files in a directory by filename extension."""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".odt"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov"},
    "Audio": {".mp3", ".wav", ".flac", ".aac"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c"},
}


@dataclass
class Results:
    """Counts returned after an organization run."""

    processed: int = 0
    moved: int = 0
    skipped: int = 0
    errors: int = 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organize direct files in a directory.")
    parser.add_argument("directory", type=Path, help="Directory whose files will be organized")
    parser.add_argument("--dry-run", action="store_true", help="Show planned moves without changing files")
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Also organize names beginning with a dot",
    )
    parser.add_argument("--log-file", type=Path, help="Optional file for detailed logs")
    return parser.parse_args(argv)


def configure_logging(log_file: Path | None = None) -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file is not None:
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=handlers,
        force=True,
    )


def validate_directory(directory: Path) -> Path:
    """Return an absolute target directory or raise a helpful exception."""
    directory = directory.expanduser()
    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")
    return directory.resolve()


def scan_files(directory: Path, include_hidden: bool = False) -> list[Path]:
    """List direct, non-directory children, optionally excluding hidden names."""
    try:
        entries = directory.iterdir()
        return sorted(
            (entry for entry in entries if entry.is_file() and (include_hidden or not entry.name.startswith("."))),
            key=lambda entry: entry.name.lower(),
        )
    except PermissionError as error:
        raise PermissionError(f"Cannot read directory: {directory}") from error
    except OSError as error:
        raise OSError(f"Cannot scan directory {directory}: {error}") from error


def get_category(file_path: Path) -> str:
    """Classify a file by its final suffix. Unknown and suffixless files are Others."""
    suffix = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def ensure_category_directory(directory: Path, category: str, dry_run: bool = False) -> Path:
    destination_directory = directory / category
    if not dry_run:
        destination_directory.mkdir(exist_ok=True)
    return destination_directory


def get_available_destination(destination_directory: Path, filename: str) -> Path:
    """Return a non-existing name, preserving a suffix such as '.jpg'."""
    proposed = destination_directory / filename
    if not proposed.exists():
        return proposed

    source_name = Path(filename)
    stem, suffix = source_name.stem, source_name.suffix
    index = 1
    while True:
        candidate = destination_directory / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            logging.warning("Name collision for %s; using %s", filename, candidate.name)
            return candidate
        index += 1


def move_file(source: Path, destination: Path, dry_run: bool = False) -> None:
    """Move one file unless dry-run mode is selected."""
    if dry_run:
        return
    try:
        shutil.move(str(source), str(destination))
    except PermissionError as error:
        raise PermissionError(f"Permission denied moving {source.name}: {error}") from error
    except OSError as error:
        raise OSError(f"Could not move {source.name}: {error}") from error


def organize(directory: Path, *, dry_run: bool = False, include_hidden: bool = False) -> Results:
    """Organize direct files and print each planned or completed move."""
    results = Results()
    files = scan_files(directory, include_hidden=include_hidden)
    if not files:
        print("No eligible files found.")
        return results

    for source in files:
        results.processed += 1
        category = get_category(source)
        try:
            destination_directory = ensure_category_directory(directory, category, dry_run=dry_run)
            destination = get_available_destination(destination_directory, source.name)
            move_file(source, destination, dry_run=dry_run)
        except OSError as error:
            results.errors += 1
            logging.error("%s", error)
            print(f"[!] {source.name}  → {category}/ (error)")
            continue

        if not dry_run:
            results.moved += 1
        logging.info("%s: %s -> %s", "Planned" if dry_run else "Moved", source, destination)
        print(f"[+] {source.name}  → {category}/")
    return results


def display_summary(results: Results, dry_run: bool) -> None:
    print("\nNo files were moved." if dry_run else "\nOrganization complete.")
    print(f"Files processed: {results.processed}")
    print(f"Files moved:     {results.moved}")
    print(f"Errors:          {results.errors}")
    if results.skipped:
        print(f"Files skipped:   {results.skipped}")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.log_file)
    try:
        directory = validate_directory(args.directory)
        print("Python File Organizer\n---------------------")
        print(f"\nTarget directory: {directory}")
        print("\nDRY RUN" if args.dry_run else "\nScanning files...")
        results = organize(directory, dry_run=args.dry_run, include_hidden=args.include_hidden)
        display_summary(results, args.dry_run)
        return 1 if results.errors else 0
    except (FileNotFoundError, NotADirectoryError, PermissionError, OSError) as error:
        logging.error("%s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
