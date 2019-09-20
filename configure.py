import os
import json
from typing import Dict, List, Union, NewType
Config = NewType("Config", Dict[str, Union[str, List[str]]])


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

CONFIG_PATH: str = "config.json"


def init() -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(INITIAL_CONFIG, f)


def load_config() -> Config:
    if os.path.isfile(CONFIG_PATH):
        with open("config.json", "r") as f:
            return json.load(f)
    else:     
        raise Exception("config.json not found")


def update_config(key: str, value: any) -> None:
    if os.path.isfile(CONFIG_PATH):
        config : Config = load_config()
        with open(CONFIG_PATH, "w") as f:
            config[key]: Config = value
            json.dump(config, f)
    else:     
        raise Exception("config.json not found")


def save_root_path() -> None:
    root_path: str = os.path.dirname(os.path.realpath(__file__))
    update_config("root_path", root_path)


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

if __name__ == "__main__":
    save_root_path()
    config_editor("vim")