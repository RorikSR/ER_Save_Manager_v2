from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path


FROZEN = getattr(sys, "frozen", False)
BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
APP_DIR = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent
BUNDLED_DATA_DIR = BUNDLE_DIR / "data"
DATA_DIR = APP_DIR / "data"

MUTABLE_DATA_PATHS = {
    Path("archive"),
    Path("backup"),
    Path("backups"),
    Path("config.json"),
    Path("GameSaveDir.txt"),
    Path("post.update"),
    Path("recovered"),
    Path("reports"),
    Path("save-files"),
    Path("save-files-pre-V1.5-BACKUP"),
    Path("temp"),
    Path("updates"),
}


def _is_mutable_path(relative_path: Path) -> bool:
    return any(
        relative_path == mutable_path or mutable_path in relative_path.parents
        for mutable_path in MUTABLE_DATA_PATHS
    )


def ensure_runtime_data() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if BUNDLED_DATA_DIR.exists() and BUNDLED_DATA_DIR.resolve() != DATA_DIR.resolve():
        for source_path in BUNDLED_DATA_DIR.rglob("*"):
            relative_path = source_path.relative_to(BUNDLED_DATA_DIR)
            target_path = DATA_DIR / relative_path

            if source_path.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue

            target_path.parent.mkdir(parents=True, exist_ok=True)
            if target_path.exists() and _is_mutable_path(relative_path):
                continue
            shutil.copy2(source_path, target_path)

    for directory_name in (
        "archive",
        "backup",
        "backups",
        "recovered",
        "reports",
        "save-files",
        "temp",
        "updates",
    ):
        (DATA_DIR / directory_name).mkdir(parents=True, exist_ok=True)

    return DATA_DIR


def data_path(*parts: str) -> Path:
    return DATA_DIR.joinpath(*parts)


def data_dir(*parts: str) -> str:
    return str(data_path(*parts)) + os.sep
