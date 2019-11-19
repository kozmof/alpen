import os
import json
from typing import Optional, List
from .configure import load_config
from .dir_ops import get_dir_path
from .metadata import (init_metadata, 
                      version_check,
                      recover_missing_keys,
                      update_metadata_file,
                      f2t,
                      METADATA_FILE,
                      CURENT_FORMAT_VERSION)
from .custom_types import Config
from .consistency import doc_file_exists

TAG_FILE = "tags.json"


def t2f(tag_name: str, config: Config) -> Optional[List[str]]:
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r") as fpt:
            tag_data = json.load(fpt)
            if tag_name in tag_data:
                return tag_data[tag_name]


def add_tag(file_name, tag_name):
    config: Config = load_config()
    if not doc_file_exists(file_name):
        print(f"{doc_path} does not exist.")
        return

    update_tag_file("ADD_TAG", file_name, config, tag_name=tag_name)
    update_metadata_file("ADD_TAG", file_name, config, tag_name=tag_name)


def arg_check_t(action_type: str):
    if action_type == "ADD_TAG":
        if tag_name is None and new_file_name:
            raise Exception("Pass only tag_name")
    elif action_type == "REMOVE_TAG":
        if tag_name is None and new_file_name:
            raise Exception("Pass only tag_name")
    elif action_type == "RENAME_FILE":
        if new_file_name is None and tag_name:
            raise Exception("Pass only new_file_name")
    else:
        raise Exception(f"No such action type: {action_type}")


def get_tag_data(config: Config):
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r") as fpt:
            tag_data = json.load(fpt)
            return tag_data


def update_json(tag_data, config: Config):
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "w") as fpt:
            json.dump(tag_data, fpt)


def update_tag_file(action_type: str, file_name: str, config: Config, tag_name: Optional[str] = None, new_file_name: Optional[str] = None):
    arg_check_t(action_type)
    if action_type == "ADD_TAG":
        tag_data = get_tag_data(config)
        if tag_data:
            if tag_name in tag_data:
                if file_name not in tag_data[tag_name]:
                    tag_data[tag_name].append(file_name)
            else:
                tag_data[tag_name] = [file_name]

            update_json(tag_data, config)
        else:
            tag_data = {}
            tag_data[tag_name] = [file_name]
            update_json(tag_data, config)

    elif action_type == "REMOVE_TAG":
        tag_data = get_tag_data(config)
        if tag_data:
            if tag_name in tag_data:
                if file_name in tag_data[tag_name]:
                    tag_data[tag_name].remove(file_name)
                    update_json(tag_data, config)

    elif action_type == "RENAME_FILE":
        tag_names = f2t(file_name, config)
        if tag_names:
            tag_data = get_tag_data(config)
            if tag_data:
                for tag_name in tag_names:
                    tag_data[tag_name].remove(file_name)
                    tag_data[tag_name].append(new_file_name)

                update_json(tag_data, config)
    else:
        raise Exception("No such action type: {action_type}")