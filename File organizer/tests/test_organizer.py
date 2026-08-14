from pathlib import Path

import pytest

from organizer import (
    get_available_destination,
    get_category,
    organize,
    scan_files,
    validate_directory,
)


@pytest.mark.parametrize(
    ("filename", "category"),
    [
        ("photo.JPG", "Images"),
        ("report.pdf", "Documents"),
        ("backup.tar.gz", "Archives"),
        ("script.py", "Code"),
        ("README", "Others"),
        ("file.unknown", "Others"),
    ],
)
def test_get_category(filename: str, category: str) -> None:
    assert get_category(Path(filename)) == category


def test_collision_gets_numbered_name(tmp_path: Path) -> None:
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "photo_1.jpg").touch()
    assert get_available_destination(tmp_path, "photo.jpg").name == "photo_2.jpg"


def test_validate_nonexistent_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        validate_directory(tmp_path / "missing")


def test_dry_run_does_not_move_or_create_directories(tmp_path: Path) -> None:
    source = tmp_path / "photo.jpg"
    source.write_text("image placeholder")
    results = organize(tmp_path, dry_run=True)
    assert source.exists()
    assert not (tmp_path / "Images").exists()
    assert results.processed == 1
    assert results.moved == 0


def test_organize_moves_files_and_protects_duplicate_names(tmp_path: Path) -> None:
    source = tmp_path / "photo.jpg"
    source.write_text("new photo")
    images = tmp_path / "Images"
    images.mkdir()
    (images / "photo.jpg").write_text("old photo")

    results = organize(tmp_path)
    assert not source.exists()
    assert (images / "photo.jpg").read_text() == "old photo"
    assert (images / "photo_1.jpg").read_text() == "new photo"
    assert results.moved == 1


def test_scan_files_excludes_directories_and_hidden_files_by_default(tmp_path: Path) -> None:
    (tmp_path / "visible.txt").touch()
    (tmp_path / ".env").touch()
    (tmp_path / "folder").mkdir()
    assert [file.name for file in scan_files(tmp_path)] == ["visible.txt"]
    assert {file.name for file in scan_files(tmp_path, include_hidden=True)} == {"visible.txt", ".env"}
