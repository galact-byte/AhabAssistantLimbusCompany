from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_DATA_NAME = "AALC"
LEGACY_USER_FILES = ("config.yaml", "theme_pack_list.yaml")
LEGACY_USER_DIRS = ("config_backup", "theme_pack_weight")


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def user_data_dir() -> Path:
    if not is_frozen():
        return Path.cwd()
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return Path.cwd()
    dest = Path(appdata) / APP_DATA_NAME
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def _looks_like_aalc_dir(path: Path) -> bool:
    name = path.name.casefold()
    return "aalc" in name or name.startswith("ahab")


def _candidate_legacy_dirs(install_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path) -> None:
        try:
            resolved = path.resolve()
        except OSError:
            return
        if resolved in seen or not path.is_dir():
            return
        seen.add(resolved)
        candidates.append(path)

    add(install_dir)
    parent = install_dir.parent
    if parent.exists():
        for child in parent.iterdir():
            if child.is_dir() and _looks_like_aalc_dir(child):
                add(child)
    grandparent = parent.parent
    if grandparent.exists() and grandparent != parent:
        for child in grandparent.iterdir():
            if not child.is_dir() or not _looks_like_aalc_dir(child):
                continue
            add(child)
            add(child / "AALC")
    return candidates


def migrate_legacy_user_data(*, dest_dir: Path, install_dir: Path) -> bool:
    dest_dir.mkdir(parents=True, exist_ok=True)
    if (dest_dir / "config.yaml").exists():
        return False

    dest_resolved = dest_dir.resolve()
    best: Path | None = None
    best_mtime = -1.0
    for candidate in _candidate_legacy_dirs(install_dir):
        try:
            if candidate.resolve() == dest_resolved:
                continue
        except OSError:
            continue
        config_path = candidate / "config.yaml"
        if not config_path.is_file():
            continue
        mtime = config_path.stat().st_mtime
        if mtime > best_mtime:
            best = candidate
            best_mtime = mtime
    if best is None:
        return False

    for name in LEGACY_USER_FILES:
        src = best / name
        dest = dest_dir / name
        if src.is_file() and not dest.exists():
            shutil.copy2(src, dest)
    for name in LEGACY_USER_DIRS:
        src = best / name
        dest = dest_dir / name
        if src.is_dir() and not dest.exists():
            shutil.copytree(src, dest)
    return (dest_dir / "config.yaml").exists()
