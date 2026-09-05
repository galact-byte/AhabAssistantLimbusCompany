import sys
from pathlib import Path

from .user_data import is_frozen, migrate_legacy_user_data, user_data_dir

VERSION_PATH = "./assets/config/version.txt"
EXAMPLE_PATH = "./assets/config/config.example.yaml"
THEME_PACK_LIST_EXAMPLE_PATH = "./assets/config/theme_pack_list.example.yaml"

if is_frozen():
    _data_dir = user_data_dir()
    migrate_legacy_user_data(
        dest_dir=_data_dir,
        install_dir=Path(sys.executable).resolve().parent,
    )
    CONFIG_PATH = str(_data_dir / "config.yaml")
    THEME_PACK_LIST_PATH = str(_data_dir / "theme_pack_list.yaml")
    THEME_PACK_WEIGHT_PATH = str(_data_dir / "theme_pack_weight")
    CONFIG_BACKUP_PATH = str(_data_dir / "config_backup")
else:
    CONFIG_PATH = "./config.yaml"
    THEME_PACK_LIST_PATH = "./theme_pack_list.yaml"
    THEME_PACK_WEIGHT_PATH = "./theme_pack_weight"
    CONFIG_BACKUP_PATH = "config_backup"
