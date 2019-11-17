import re
import os
import json
from time import time
from uuid import uuid4
from typing import List, Union
from .custom_types import Config, Shorthand, ConfigBackup
from .dir_ops import make_directory


INITIAL_CONFIG: Config = {
    "root_path": "",
    "targets": [],
    "stops": [],
    "masks": ["md", "txt"],
    "enable_mask": True,
    "commit_header": "[DSK-manual-commit]"
}


INITIAL_SHORTHAND: Shorthand = {
    "build": "b",
    "list": "l",
    "edit": "e",
    "rename": "r",
    "save_history": "sh",
    "todo": "t",
    "diff": "d",
    "clear": "c",
    "quit": "q"
}


"""
PRIORITY
1. stops
2. masks / targets
"""


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH: str = ROOT_DIR + "/" + "config.json"
CONFIG_BACKUP_PATH: str = ROOT_DIR + "/" + ".backup_config.json"
SHORTHAND_PATH = ROOT_DIR + "/" + "shorthand.json"


def init() -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(INITIAL_CONFIG, f)

    with open(SHORTHAND_PATH, "w") as f:
        json.dump(INITIAL_SHORTHAND, f)


def load_config(backup=False) -> Union[Config, ConfigBackup]:
    if not backup: 
        cpath = CONFIG_PATH
    else:
        cpath = CONFIG_BACKUP_PATH

    if os.path.isfile(cpath):
        with open(cpath, "r") as f:
            return json.load(f)
    else:     
        raise Exception(f"{cpath} not found")


def update_config(key: str, value: any, halt_if_exists: bool = False, backup_limit=10) -> None:
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
                json.dump(config, f)

            config_backup: ConfigBackup = load_config(backup=True)

            if len(config_backup) > backup_limit:
                old_key: str = str(min([int(timestamp) for timestamp in config_backup.keys()]))
                del config_backup[old_key]

            with open(CONFIG_BACKUP_PATH, "w") as fb:
                backup_key: str = str(int(time()))
                config_backup[backup_key] = config
                json.dump(config_backup, fb)

    else:     
        raise Exception("config.json not found")


def load_shorthand() -> Shorthand:
    spath: str = SHORTHAND_PATH

    if os.path.isfile(spath):
        with open(spath, "r") as f:
            return json.load(f)
    else:     
        raise Exception(f"{spath} not found")


def update_shorthand(key: str, value: str) -> None:
    if os.path.isfile(SHORTHAND_PATH):
        shorthand: shorthand = load_shorthand()
        with open(SHORTHAND_PATH, "w") as f:
            shorthand[key] = value
            json.dump(config, f)


def save_uuid() -> None:
    uuid: str = str(uuid4())
    update_config("uuid", uuid, halt_if_exists=True)


def save_root_path() -> None:
    update_config("root_path", ROOT_DIR, halt_if_exists=True)


def config_editor(editor: str) -> None:
    update_config("editor", editor)


def is_active_file(file_name: str) -> bool:
    config: Config = load_config()
    stops: List[str] = config["stops"]
    masks: List[str] = config["masks"]
    targets: List[str] = config["targets"]

    if file_name in stops:
        return False
    elif file_name in targets:
        return True
    else:
        for mask in masks:
            if re.match(f".*\.{mask}$", file_name):
                return True
        return False


if __name__ == "__main__":
    # init()
    # save_root_path()
    # save_uuid()
    # config_editor("code")
    config = load_config()
    # make_directory("DOCUMENT", config)
    make_directory("HISTORY", config)
