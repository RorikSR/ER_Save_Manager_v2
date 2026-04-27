from __future__ import annotations

import shutil
import time
from datetime import datetime
from pathlib import Path
from app_paths import DATA_DIR, ensure_runtime_data


ensure_runtime_data()
REPO_ROOT = Path(__file__).resolve().parent
BACKUP_ROOT = DATA_DIR / "backups"
SAVE_FILENAMES = ("ER0000.sl2", "ER0000.co2")
LAST_BACKUP_BY_PATH = {}


def preferred_save_filename(seamless_coop_enabled: bool) -> str:
    return "ER0000.co2" if seamless_coop_enabled else "ER0000.sl2"


def alternate_save_filename(filename: str) -> str:
    if filename.endswith(".co2"):
        return "ER0000.sl2"
    return "ER0000.co2"


def resolve_save_path(directory: str | Path, preferred_filename: str | None = None) -> Path:
    directory = Path(directory)
    preferred_filename = preferred_filename or "ER0000.sl2"
    preferred_path = directory / preferred_filename
    if preferred_path.exists():
        return preferred_path

    alternate_path = directory / alternate_save_filename(preferred_filename)
    if alternate_path.exists():
        return alternate_path

    for filename in SAVE_FILENAMES:
        candidate = directory / filename
        if candidate.exists():
            return candidate

    return preferred_path


def copy_save_to_directory(source_file: str | Path, destination_directory: str | Path, target_filename: str | None = None) -> Path:
    source_file = Path(source_file)
    destination_directory = Path(destination_directory)
    destination_directory.mkdir(parents=True, exist_ok=True)
    destination_path = destination_directory / (target_filename or source_file.name)
    shutil.copy2(source_file, destination_path)
    return destination_path


def convert_save_file(source_file: str | Path, target_extension: str, destination_directory: str | Path | None = None) -> Path:
    source_file = Path(source_file)
    if not target_extension.startswith("."):
        target_extension = f".{target_extension}"

    destination_directory = Path(destination_directory) if destination_directory else source_file.parent
    destination_directory.mkdir(parents=True, exist_ok=True)
    destination_path = destination_directory / f"{source_file.stem}{target_extension}"
    shutil.copy2(source_file, destination_path)
    return destination_path


def create_timestamped_backup(file_path: str | Path, label: str = "auto") -> Path | None:
    file_path = Path(file_path)
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    safe_label = "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in label).strip("_") or "auto"
    backup_dir = BACKUP_ROOT / file_path.stem
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{timestamp}__{safe_label}{file_path.suffix}"
    shutil.copy2(file_path, backup_path)
    return backup_path


def prepare_for_write(file_path: str | Path, label: str = "auto", throttle_seconds: float = 1.0) -> Path | None:
    file_path = Path(file_path).resolve()
    now = time.time()
    last_backup_time = LAST_BACKUP_BY_PATH.get(str(file_path))
    if last_backup_time is not None and now - last_backup_time < throttle_seconds:
        return None

    backup_path = create_timestamped_backup(file_path, label=label)
    LAST_BACKUP_BY_PATH[str(file_path)] = now
    return backup_path
