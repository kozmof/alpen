"""Tag Utilities
"""
import os
import json
from pprint import pprint
from typing import Optional, List, Dict
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.metadata import (
    manipulate_metadata,
    f2t
    )
from lib.commands.core.custom_types import Config

TAG_FILE = "tags.json"


def load_tag_data(config: Config) -> Dict:
    """Load all tag data

    Structure:
        tag_data:
            {
                [tag_name: str]:  List # file names
            }

    Args:
        config (Config): Config data

    Returns:
        Dict: Tag data
    """
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r") as f:
            tag_data = json.load(f)
            return tag_data


def dump_tag_json(tag_data, config: Config) -> None:
    """Dump tag data

    Args:
        tag_data (Dict): Tag data
        config (Config): Config data
    """
    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    if not os.path.isdir(tag_dir):
        os.makedirs(tag_dir)

    with open(tag_file_path, "w") as f:
        json.dump(tag_data, f, indent=4, sort_keys=True)


def manipulate_tag_data(action_type: str, config: Config,
                    file_name: Optional[str] = None, new_file_name: Optional[str] = None,
                    tag_name: Optional[str] = None, new_tag_name: Optional[str] = None) -> None:
    """Update tag file

        - ADD_TAG: Add a new tag
        - REMOVE_TAG: Remove a tag
        - RENAME_TAG: Rename a tag
        - SEARCH_TAG: Search a tag and print linked files
        - SHOW_ALL: Print all tag data
        - RENAME_FILE: Rename a file which links to tags

    Arg Patterns:
        - ADD_TAG:      file_name, tag_name
        - REMOVE_TAG:   file_name, tag_name
        - RENAME_TAG:   tag_name, new_tag_name
        - SEARCH_TAG:   tag_name
        - SHOW_ALL:     none
        - RENAME_FILE:  file_name, new_file_name

    Args:
        action_type (str):                          ADD_TAG, REMOVE_TAG, RENAME_TAG, SEARCH_TAG, SHOW_ALL, RENAME_FILE
        config (Config):                            Config file
        file_name (Optional[str], optional):        Use in ADD_TAG, REMOVE_TAG, RENAME_TAG, RENAME_FILE. Defaults to None.
        new_file_name (Optional[str], optional):    Use in RENAME_FILE. Defaults to None.
        tag_name (Optional[str], optional):         Use in ADD_TAG, REMOVE_TAG, SEARCH_TAG.  Defaults to None.
        new_tag_name (Optional[str], optional):     Use in RENAME_TAG. Defaults to None.
    """
    # -------------------------------------------------------
    # ADD_TAG 
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
    # -------------------------------------------------------
    # REMOVE_TAG
    elif action_type == "REMOVE_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            if file_name in tag_data[tag_name]:
                tag_data[tag_name].remove(file_name)
                if not tag_data[tag_name]:
                    del tag_data[tag_name]
                dump_tag_json(tag_data, config)
    # -------------------------------------------------------
    # RENAME_TAG
    elif action_type == "RENAME_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            tag_data[new_tag_name] = tag_data[tag_name]
            del tag_data[tag_name]
            dump_tag_json(tag_data, config)
    # -------------------------------------------------------
    # SEARCH_TAG
    elif action_type == "SEARCH_TAG":
        tag_data = load_tag_data(config)
        if tag_data and tag_name in tag_data:
            pprint(tag_data[tag_name])
    # -------------------------------------------------------
    # SHOW_ALL
    elif action_type == "SHOW_ALL":
        tag_data = load_tag_data(config)
        pprint(tag_data)
    # -------------------------------------------------------
    # RENAME_FILE
    elif action_type == "RENAME_FILE":
        tag_names = f2t(file_name, config)
        tag_data = load_tag_data(config)
        if tag_names and tag_data:
            for tag_name in tag_names:
                tag_data[tag_name].remove(file_name)
                tag_data[tag_name].append(new_file_name)

            dump_tag_json(tag_data, config)
    # -------------------------------------------------------
    else:
        raise Exception(f"No such action type: {action_type}")