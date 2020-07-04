"""Configure utilities
"""
import re
import os
import json
from time import time
from uuid import uuid4
from typing import List, Union
from lib.commands.core.custom_types import Config, Shorthand, ConfigBackup
from lib.commands.core.dir_ops import make_directory


INITIAL_CONFIG: Config = {
    "root_path": "",
    "user": "",
    "editor": "",
    "editor_file_pos": 0,
    "uuid": "",
    "commit_header": "[alpen-manual-commit]"
}


INITIAL_SHORTHAND: Shorthand = {
    "build": "b",
    "list": "l",
    "edit": "e",
    "tag": "ta",
    "tutorial": "tu",
    "rename": "r",
    "save_history": "s",
    "todo": "to",
    "memo": "m",
    "diff": "d",
    "clear": "c",
    "quit": "q"
}


ROOT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, *([".."] * 3))))
CONFIG_PATH: str = ROOT_DIR + "/" + "config.json"
CONFIG_BACKUP_PATH: str = ROOT_DIR + "/" + ".backup_config.json"
SHORTHAND_PATH = ROOT_DIR + "/" + "shorthand.json"


def init() -> None:
    """Initialize config data
    """
    with open(CONFIG_PATH, "w") as f:
        json.dump(INITIAL_CONFIG, f, indent=4, sort_keys=True)

    with open(SHORTHAND_PATH, "w") as f:
        json.dump(INITIAL_SHORTHAND, f, indent=4, sort_keys=True)


class ConfigError(Exception):
    """Custom Exception for missing a config file
    """
    pass


def load_config(backup=False) -> Union[Config, ConfigBackup]:
    """Load config data

    Args:
        backup (bool, optional): Load backup config data. Defaults to False.

    Returns:
        Union[Config, ConfigBackup]: Config data or backup config data
    """
    if not backup: 
        cpath = CONFIG_PATH
    else:
        cpath = CONFIG_BACKUP_PATH

    if os.path.isfile(cpath):
        with open(cpath, "r") as f:
            return json.load(f)
    elif backup:
        backup_config = INITIAL_CONFIG.copy()
        return backup_config
    else:     
        raise ConfigError(f"{cpath} not found")


def has_config() -> bool:
    """Check whether a config file exists or not

    Returns:
        bool: True if a config file exists
    """
    cpath = CONFIG_PATH
    if os.path.isfile(cpath):
        return True
    else:
        return False


def update_config(key: str, value: any, halt_if_exists: bool=False, backup_limit: int=10) -> None:
    """Update config data

    Args:
        key (str): A key to update data
        value (any): A value to be updated
        halt_if_exists (bool, optional): Don't update if a key exists. Defaults to False.
        backup_limit (int, optional): An amount of backup data. Defaults to 10.
    """
    if os.path.isfile(CONFIG_PATH):
        config : Config = load_config()
        update: bool = False
        if halt_if_exists:
            if key not in config:
                update = True

            elif not config[key]:
                update = True

        else:
            update = True

        if update:
            with open(CONFIG_PATH, "w") as f:
                config[key] = value
                json.dump(config, f, indent=4, sort_keys=True)

            config_backup: ConfigBackup = load_config(backup=True)

            if len(config_backup) > backup_limit:
                old_key: str = str(min([int(timestamp) for timestamp in config_backup.keys()]))
                del config_backup[old_key]

            with open(CONFIG_BACKUP_PATH, "w") as fb:
                backup_key: str = str(int(time()))
                config_backup[backup_key] = config
                json.dump(config_backup, fb, indent=4, sort_keys=True)

    else:     
        raise Exception("config.json not found")


def load_shorthand() -> Shorthand:
    """Load command shorthands
    Returns:
        Shorthand: Command shorthands
    """
    spath: str = SHORTHAND_PATH

    if os.path.isfile(spath):
        with open(spath, "r") as f:
            return json.load(f)
    else:     
        raise Exception(f"{spath} not found")


def update_shorthand(config: Config, key: str, value: str) -> None:
    """Updata shorthand data

    Args:
        config (Config): Config data
        key (str): An command name
        value (str): A shorthand
    """
    if os.path.isfile(SHORTHAND_PATH):
        shorthand: Shorthand = load_shorthand()
        with open(SHORTHAND_PATH, "w") as f:
            shorthand[key] = value
            json.dump(shorthand, f, indent=4, sort_keys=True)


def save_uuid() -> None:
    """Save an uuid if it doesn't exist
    """
    uuid: str = str(uuid4())
    update_config("uuid", uuid, halt_if_exists=True)


def save_root_path() -> None:
    """Save an absolute path of root if it doesn't exist
    """
    update_config("root_path", ROOT_DIR, halt_if_exists=True)


def config_editor(editor: str) -> None:
    """Configure an editor 

    Args:
        editor (str): An editor command in CLI
    """
    update_config("editor", editor)


def config_user(user: str) -> None:
    """Configure an user name

    Args:
        user (str): An user name
    """
    update_config("user", user)


def config_editor_file_pos(pos: int) -> None:
    """Configure a file position to be openend by an editor

    Args:
        pos (int): A position statrts from 0
    """
    update_config("editor_file_pos", pos)


def config_deploy_path(path: str) -> None:
    """Configure a path to save a built data

    Args:
        path (str): A path 
    """
    update_config("deploy_path", path)
