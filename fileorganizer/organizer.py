"""Organize files into extension-based folders, with collision-safe moves."""
from pathlib import Path
import shutil
from typing import Dict, List, Tuple

CATEGORIES: Dict[str, set] = {
    "Imagens": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tif", ".tiff"},
    "Documentos": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".md"},
    "Audio": {".mp3", ".wav", ".aac", ".m4a", ".ogg", ".flac", ".wma"},
    "Videos": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".mpeg", ".mpg"},
    "Compactados": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"},
}


def category_for(path: Path) -> str:
    """Return a category name based on a file's extension."""
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Outros"


def plan_organization(directory: Path) -> List[Tuple[Path, Path]]:
    """Build (source, destination) pairs for files directly inside directory."""
    directory = Path(directory).expanduser()
    if not directory.exists():
        raise FileNotFoundError("A pasta informada não existe.")
    if not directory.is_dir():
        raise NotADirectoryError("O caminho informado não é uma pasta.")

    plan = []
    for source in sorted(directory.iterdir(), key=lambda item: item.name.lower()):
        if source.is_file():
            destination = directory / category_for(source) / source.name
            plan.append((source, destination))
    return plan


def _available_destination(destination: Path) -> Path:
    """Choose a non-conflicting filename without overwriting existing data."""
    if not destination.exists():
        return destination
    counter = 1
    while True:
        candidate = destination.with_name(
            "{}_{}{}".format(destination.stem, counter, destination.suffix)
        )
        if not candidate.exists():
            return candidate
        counter += 1


def organize_files(directory: Path) -> List[Tuple[Path, Path]]:
    """Move planned files and return the actual (source, destination) pairs."""
    completed = []
    for source, planned_destination in plan_organization(directory):
        planned_destination.parent.mkdir(parents=True, exist_ok=True)
        destination = _available_destination(planned_destination)
        shutil.move(str(source), str(destination))
        completed.append((source, destination))
    return completed
