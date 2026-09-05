from __future__ import annotations

import sys
from pathlib import Path

from module.update.check_update import GITHUB_UPDATE_OWNER, GITHUB_UPDATE_REPO, resolve_update_check_source
from module.user_data import migrate_legacy_user_data, user_data_dir


def test_source_mode_keeps_config_in_cwd(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delattr(sys, "frozen", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))

    assert user_data_dir() == tmp_path
    assert not (tmp_path / "Roaming" / "AALC").exists()


def test_frozen_mode_uses_appdata(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    appdata = tmp_path / "Roaming"
    install_dir = tmp_path / "install"
    install_dir.mkdir()
    monkeypatch.setenv("APPDATA", str(appdata))
    monkeypatch.chdir(install_dir)

    assert user_data_dir() == appdata / "AALC"


def test_migrate_copies_config_from_sibling_install(tmp_path: Path) -> None:
    old_install = tmp_path / "AALC_v1.5.3" / "AALC"
    new_install = tmp_path / "AALC_v1.5.4" / "AALC"
    dest = tmp_path / "Roaming" / "AALC"
    old_install.mkdir(parents=True)
    new_install.mkdir(parents=True)
    dest.mkdir(parents=True)
    (old_install / "config.yaml").write_text("background_click: true\nset_win_size: 900\n", encoding="utf-8")
    (old_install / "theme_pack_list.yaml").write_text("pack: 1\n", encoding="utf-8")
    backup = old_install / "config_backup"
    backup.mkdir()
    (backup / "config.yaml").write_text("backup: true\n", encoding="utf-8")
    weights = old_install / "theme_pack_weight"
    weights.mkdir()
    (weights / "theme_pack_weight_team_1.yaml").write_text("team: 1\n", encoding="utf-8")

    assert migrate_legacy_user_data(dest_dir=dest, install_dir=new_install) is True
    assert (dest / "config.yaml").read_text(encoding="utf-8") == "background_click: true\nset_win_size: 900\n"
    assert (dest / "theme_pack_list.yaml").read_text(encoding="utf-8") == "pack: 1\n"
    assert (dest / "config_backup" / "config.yaml").read_text(encoding="utf-8") == "backup: true\n"
    assert (dest / "theme_pack_weight" / "theme_pack_weight_team_1.yaml").read_text(encoding="utf-8") == "team: 1\n"


def test_migrate_ignores_unrelated_sibling_config(tmp_path: Path) -> None:
    unrelated = tmp_path / "OtherApp"
    new_install = tmp_path / "AALC_v1.5.4" / "AALC"
    dest = tmp_path / "Roaming" / "AALC"
    unrelated.mkdir(parents=True)
    new_install.mkdir(parents=True)
    dest.mkdir(parents=True)
    (unrelated / "config.yaml").write_text("other: true\n", encoding="utf-8")

    assert migrate_legacy_user_data(dest_dir=dest, install_dir=new_install) is False
    assert not (dest / "config.yaml").exists()


def test_migrate_does_not_overwrite_existing_appdata_config(tmp_path: Path) -> None:
    old_install = tmp_path / "AALC_v1.5.3" / "AALC"
    new_install = tmp_path / "AALC_v1.5.4" / "AALC"
    dest = tmp_path / "Roaming" / "AALC"
    old_install.mkdir(parents=True)
    new_install.mkdir(parents=True)
    dest.mkdir(parents=True)
    (old_install / "config.yaml").write_text("old: true\n", encoding="utf-8")
    (dest / "config.yaml").write_text("kept: true\n", encoding="utf-8")

    assert migrate_legacy_user_data(dest_dir=dest, install_dir=new_install) is False
    assert (dest / "config.yaml").read_text(encoding="utf-8") == "kept: true\n"


def test_update_source_auto_and_github_use_fork() -> None:
    assert GITHUB_UPDATE_OWNER == "galact-byte"
    assert GITHUB_UPDATE_REPO == "AhabAssistantLimbusCompany"
    assert resolve_update_check_source("Auto") == "github"
    assert resolve_update_check_source("GitHub") == "github"
    assert resolve_update_check_source("MirrorChyan") == "mirrorchyan"
