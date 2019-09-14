import os
import json
from typing import Dict, List, Union, NewType
Config = NewType("Config", Dict[str, Union[str, List[str]]])


INITIAL_CONFIG: Config = {
    "root_path": "",
    "targets": [],
    "stops": [],
    "mask": [".md"],
    "enable_mask": True
}

"""
1. stops
2. mask
3. targets 
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


def save_root_path() -> None:
    config : Config = load_config()
    with open(CONFIG_PATH, "w") as f:
        config["root_path"]: Config = os.path.dirname(os.path.realpath(__file__))
        json.dump(config, f)


if __name__ == "__main__":
    save_root_path()