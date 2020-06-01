import os
import json
from uuid import uuid4
from typing import Optional, List
from lib.commands.core.custom_types import Config
from lib.commands.core.dir_ops import get_dir_path

METADATA_FILE = "metadata.json"
CURENT_FORMAT_VERSION = "1.0"

FORMAT = {
  "tag": [],
  "domain": [],
  "first_finish": "",
  "revise": "",
  "uuid": "",
  "version": CURENT_FORMAT_VERSION
}


def init_metadata(file_name):
    key = file_name
    val = FORMAT
    uuid = str(uuid4())
    print(uuid)
    val["uuid"] =  uuid
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
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            if file_name in metadata:
                return metadata[file_name]["tag"]

k
def f2d(file_name: str, config: Config) -> Optional[List[str]]:
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            if file_name in metadata:
                return metadata[file_name]["domain"]


def load_metadata(config: Config):
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            return metadata


def dump_metadata_json(metadata, config: Config):
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if not os.path.isdir(metadata_dir):
        os.makedirs(metadata_dir)

    with open(metadata_file_path, "w") as f:
        json.dump(metadata, f, indent=4, sort_keys=True)


def update_metadata_file(action_type: str, config: Config,
                         file_name: Optional[str] = None,
                         tag_name: Optional[str] = None, new_tag_name: Optional[str] = None,
                         domain_name: Optional[str] = None, new_domain_name: Optional[str] = None,
                         new_file_name: Optional[str] = None):
    metadata = load_metadata(config)
    if not metadata:
        metadata = {}
        key, data = init_metadata(file_name)
        metadata[key] = data
        metadata[key]["tag"].append(tag_name)

    if action_type == "ADD_TAG":
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

        dump_metadata_json(metadata, config)

    elif action_type == "REMOVE_TAG":
        if file_name in metadata:
            if tag_name in metadata[file_name]["tag"]:
                metadata[file_name]["tag"].remove(tag_name)
                dump_metadata_json(metadata, config)

    elif action_type == "RENAME_TAG":
        for file_name, data in metadata.items():
            if tag_name in data["tag"]:
                metadata[file_name]["tag"].remove(tag_name)
                metadata[file_name]["tag"].append(new_tag_name)
        dump_metadata_json(metadata, config)

    elif action_type == "ADD_DOMAIN":
        if file_name in metadata:
            is_consistent = version_check(metadata[file_name])
            if not is_consistent:
                recover_missing_keys(metadata)

            if domain_name not in metadata[file_name]["domain"]:
                metadata[file_name]["domain"].append(domain_name)
        else:
            key, data = init_metadata(file_name)
            metadata[key] = data
            metadata[key]["domain"].append(domain_name)

        dump_metadata_json(metadata, config)

    elif action_type == "REMOVE_DOMAIN":
        if file_name in metadata:
            if domain_name in metadata[file_name]["domain"]:
                metadata[file_name]["domain"].remove(domain_name)
                dump_metadata_json(metadata, config)

    elif action_type == "RENAME_DOMAIN":
        for file_name, data in metadata.items():
            if domain_name in data["domain"]:
                metadata[file_name]["domain"].remove(domain_name)
                metadata[file_name]["domain"].append(new_domain_name)
        dump_metadata_json(metadata, config)

    elif action_type == "RENAME_FILE":
        if file_name in metadata:
            metadata[new_file_name] = metadata[file_name]
            del metadata[file_name]
            dump_metadata_json(metadata, config)
    else:
        raise Exception(f"No such action type: {action_type}")