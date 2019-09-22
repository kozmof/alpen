import os
import json
from time import time
from uuid import uuid4
from typing import Dict, List, Union, NewType
Config = NewType("Config", Dict[str, Union[str, List[str]]])
ConfigBackup = NewType("ConfigBackup", Dict[str, Config])

INITIAL_CONFIG: Config = {
    "root_path": "",
    "targets": [],
    "stops": [],
    "masks": [".md"],
    "enable_mask": True
}

"""
PRIORITY
1. stops
2. masks / targets
"""


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH: str = ROOT_DIR + "/" + "config.json"
CONFIG_BACKUP_PATH: str = ROOT_DIR + "/" + ".backup_config.json"


def init() -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(INITIAL_CONFIG, f)


def load_config(backup=False) -> Union[Config, ConfigBackup]:
    if not backup: 
        cpath = CONFIG_PATH
    else:
        cpath = CONFIG_BACKUP_PATH

    if os.path.isfile(cpath):
        with open(cpath, "r") as f:
            return json.load(f)
    else:     
        raise Exception("{} not found".format(cpath))


def update_config(key: str, value: any, halt_if_exists: bool = False, backup_limit=10) -> None:
    if os.path.isfile(CONFIG_PATH):
        config : Config = load_config()
        update: bool = False
        if halt_if_exists:
            if key not in config:
                update = True
        else:
            update = True

        if update:
            with open(CONFIG_PATH, "w") as f:
                config[key]: Config = value
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


def save_uuid() -> None:
    uuid: str = str(uuid4())
    update_config("uuid", uuid, halt_if_exists=True)


def save_root_path() -> None:
    update_config("root_path", ROOT_DIR, halt_if_exists=True)


def config_editor(editor: str) -> None:
    update_config("editor", editor)


def is_active_file(file_naem: str) -> bool:
    config: Config = load_config()
    stops: List[str] = config["stops"]
    masks: List[str] = config["masks"]
    targets: List[str] = config["targets"]

    if file_naem in stops:
        return False
    elif file_name in targets:
        return True
    else:
        for mask in masks:
            if re.match(".*" + mask + "$", file_naem):
                return True
        return False


def document_dir():
    config: Config = load_config()
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    doc_dir = "{}/docs/{}".format(root_path, uuid)
    return doc_dir


def make_doc_directory():
    doc_dir = document_dir()
    if not os.path.isdir(doc_dir):
        os.makedirs(doc_dir)


if __name__ == "__main__":
    save_root_path()
    save_uuid()
    config_editor("vim")
    make_doc_directory()
