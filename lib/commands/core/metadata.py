import os
import json
from typing import Optional, List
from .custom_types import Config
from .dir_ops import get_dir_path

METADATA_FILE = "metadata.json"
CURENT_FORMAT_VERSION = "1.0"

FORMAT = {
  "tag": [],
  "version": CURENT_FORMAT_VERSION
}


def init_metadata(file_name):
    key = file_name
    val = FORMAT
    return key, val


def version_check(file_metadata):
    if file_metadata["version"] == CURENT_FORMAT_VERSION:
        return True
    else:
        return False


def recover_missing_keys(metadata):
    for key in FORMAT.keys():
        if key not in metadata:
            metadata[key] = FORMAT[key]

    for key in metadata.keys:
        if key not in FORMAT:
            del metadata[key]

    return metadata


def f2t(file_name: str, config: Config) -> Optional[List[str]]:
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as fpm:
            metadata = json.load(fpm)
            if file_name in metadata:
                return metadata[file_name]["tag"]


def arg_check_metadata(action_type: str,
                       file_name: Optional[str], new_file_name: Optional[str],
                       tag_name: Optional[str], new_tag_name: Optional[str]):

    if action_type == "ADD_TAG":
        if tag_name is None and (new_tag_name or new_file_name):
            raise Exception("Pass only tag_name")

    elif action_type == "REMOVE_TAG":
        if tag_name is None and (new_tag_name or new_file_name):
            raise Exception("Pass only tag_name")

    elif action_type == "RENAME_TAG":
        if (tag_name is None or new_tag_name is None) and new_file_name:
            raise Exception("Pasa only tag_name and new_tag_name")

    elif action_type == "RENAME_FILE":
        if new_file_name is None and (tag_name or new_tag_name):
            raise Exception("Pass only new_file_name")
    else:
        raise Exception(f"No such action type: {action_type}")


def load_metadata(config: Config):
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as fpm:
            metadata = json.load(fpm)
            return metadata


def dump_metadata_json(metadata, config: Config):
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if not os.path.isdir(metadata_dir):
        os.makedirs(metadata_dir)

    with open(metadata_file_path, "w") as fpm:
        json.dump(metadata, fpm)


def update_metadata_file(action_type: str, config: Config,
                         file_name: Optional[str] = None,
                         tag_name: Optional[str] = None, new_tag_name: Optional[str] = None,
                         new_file_name: Optional[str] = None):

    arg_check_metadata(action_type=action_type,
                       file_name=file_name,
                       new_file_name=new_file_name,
                       tag_name=tag_name,
                       new_tag_name=new_tag_name)

    if action_type == "ADD_TAG":
        metadata = load_metadata(config)
        if metadata:
            if file_name in metadata:
                is_consistent = version_check(metadata[file_name])
                if not is_consistent:
                    recover_missing_keys(metadata)

                if tag_name not in metadata[file_name]["tag"]:
                    metadata[file_name]["tag"].append(tag_name)
            else:
                key, data = init_metadata(file_name)
                metadata[key] = data
                metadata[key]["tag"].append(tag_name)

        else:
            metadata = {}
            key, data = init_metadata(file_name)
            metadata[key] = data
            metadata[key]["tag"].append(tag_name)

        dump_metadata_json(metadata, config)

    elif action_type == "REMOVE_TAG":
        metadata = load_metadata(config)
        if metadata and file_name in metadata:
            if tag_name in metadata[file_name]["tag"]:
                metadata[file_name]["tag"].remove(tag_name)
                dump_metadata_json(metadata, config)

    elif action_type == "RENAME_TAG":
        metadata = load_metadata(config)
        if metadata: 
            for file_name, data in metadata.items():
                if tag_name in data["tag"]:
                    metadata[file_name]["tag"].remove(tag_name)
                    metadata[file_name]["tag"].append(new_tag_name)
            dump_metadata_json(metadata, config)

    elif action_type == "RENAME_FILE":
        metadata = load_metadata(config)
        if metadata and file_name in metadata:
            metadata[new_file_name] = metadata[file_name]
            del metadata[file_name]
            dump_metadata_json(metada, config)
    else:
        raise Exception(f"No such action type: {action_type}")