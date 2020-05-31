import os
import json
from pprint import pprint
from typing import Optional, List
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.metadata import (update_metadata_file,
                      f2t)
from lib.commands.core.custom_types import Config

TAG_FILE = "tags.json"


def t2f(tag_name: str, config: Config) -> Optional[List[str]]:
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r") as fpt:
            tag_data = json.load(fpt)
            if tag_name in tag_data:
                return tag_data[tag_name]


def load_tag_data(config: Config):
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r") as fpt:
            tag_data = json.load(fpt)
            return tag_data


def dump_tag_json(tag_data, config: Config):
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if not os.path.isdir(tag_dir):
        os.makedirs(tag_dir)

    with open(tag_file_path, "w") as fpt:
        json.dump(tag_data, fpt, indent=4, sort_keys=True)


def update_tag_file(action_type: str, config: Config,
                    file_name: Optional[str] = None, new_file_name: Optional[str] = None,
                    tag_name: Optional[str] = None, new_tag_name: Optional[str] = None):

    if action_type == "ADD_TAG":
        tag_data = load_tag_data(config)

        if tag_data:
            if tag_name in tag_data:
                if file_name not in tag_data[tag_name]:
                    tag_data[tag_name].append(file_name)
            else:
                tag_data[tag_name] = [file_name]

        else:
            tag_data = {}
            tag_data[tag_name] = [file_name]

        dump_tag_json(tag_data, config)

    elif action_type == "REMOVE_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            if file_name in tag_data[tag_name]:
                tag_data[tag_name].remove(file_name)
                if not tag_data[tag_name]:
                    del tag_data[tag_name]
                dump_tag_json(tag_data, config)

    elif action_type == "RENAME_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            tag_data[new_tag_name] = tag_data[tag_name]
            del tag_data[tag_name]
            dump_tag_json(tag_data, config)

    elif action_type == "SEARCH_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            pprint(tag_data[tag_name])

    elif action_type == "SHOW_ALL":
        tag_data = load_tag_data(config)
        pprint(tag_data)

    elif action_type == "RENAME_FILE":
        tag_names = f2t(file_name, config)
        tag_data = load_tag_data(config)
        if tag_names and tag_data:
            for tag_name in tag_names:
                tag_data[tag_name].remove(file_name)
                tag_data[tag_name].append(new_file_name)

            dump_tag_json(tag_data, config)
    else:
        raise Exception("No such action type: {action_type}")