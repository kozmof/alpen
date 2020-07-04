"""Metadata Utilities
"""
import os
import json
from uuid import uuid4
from typing import Optional, List, Tuple
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
  "lang": "",
  "version": CURENT_FORMAT_VERSION
}


def init_metadata(file_name: str) -> Tuple[str, dict]:
    """Initialize metadata

    Args:
        file_name (str): A file name

    Returns:
        Tuple[str, dict]: A key and initialized metadata. Currently key is a file name
    """
    key = file_name
    val = FORMAT.copy()
    uuid = str(uuid4())
    val["uuid"] =  uuid
    return key, val


def version_check(file_metadata: dict) -> bool:
    """Check a version of format of metadata

    Args:
        file_metadata (dict): file specific metadata

    Returns:
        bool: True if it is an valid version
    """
    if file_metadata["version"] == CURENT_FORMAT_VERSION:
        return True
    else:
        return False


def recover_missing_keys(metadata: dict) -> dict:
    """Recover missing keys in a current format

    Args:
        metadata (dict): metadata

    Returns:
        dict: Recovered metadata
    """
    for key in FORMAT.keys():
        if key not in metadata:
            metadata[key] = FORMAT[key]
    for key in metadata.keys():
        if key not in FORMAT:
            del metadata[key]
    return metadata


def f2t(file_name: str, config: Config) -> Optional[List[str]]:
    """A file name to tags

    Args:
        file_name (str): A file name
        config (Config): Config data

    Returns:
        Optional[List[str]]: Tags related to given a file
    """
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            if file_name in metadata:
                return metadata[file_name]["tag"]


def f2d(file_name: str, config: Config) -> Optional[List[str]]:
    """A file name to domains

    Args:
        file_name (str): A file name
        config (Config): Config data

    Returns:
        Optional[List[str]]: Domains related to given a file
    """
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            if file_name in metadata:
                return metadata[file_name]["domain"]


def load_metadata(config: Config) -> dict:
    """Load metadata

    Args:
        config (Config): Config data

    Returns:
        dict: Metadata
    """
    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as f:
            metadata = json.load(f)
            return metadata


def dump_metadata_json(metadata: dict, config: Config) -> None:
    """Dump metadata to JSON

    Args:
        metadata (dict): Metadata
        config (Config): Config data
    """
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
    """Update metadata file

        - ADD_TAG: Add a new tag
        - REMOVE_TAG: Remove a tag
        - RENAME_TAG: Rename a tag
        - ADD_DOMAIN: Add a new domain
        - REMOVE_DOMAIN: Remove a domain
        - RENAME_DOMAIN: Rename a domain
        - RENAME_FILE: Rename a file

    Arg Patterns:
        - ADD_TAG:        file_name, tag_name
        - REMOVE_TAG:     file_name, tag_name
        - RENAME_TAG:     tag_name, new_tag_name
        - ADD_DOMAIN:     file_name, domain_name
        - REMOVE_DOMAIN:  file_name, domain_name
        - RENAME_DOMAIN:  domain_name, new_domain_name
        - RENAME_FILE:  file_name, new_file_name

    Args:
        action_type (str):                          ADD_TAG, REMOVE_TAG, RENAME_TAG, ADD_DOMAIN, REMOVE_DOMAIN, RENAME_DOMAIN,RENAME_FILE
        config (Config):                            Config file
        file_name (Optional[str], optional):        Use in ADD_TAG, REMOVE_TAG, RENAME_TAG, ADD_DOMAIN, REMOVE_DOMAIN, RENAME_DOMAIN, RENAME_FILE. Defaults to None.
        new_file_name (Optional[str], optional):    Use in RENAME_FILE. Defaults to None.
        tag_name (Optional[str], optional):         Use in ADD_TAG, REMOVE_TAG, Defaults to None.
        new_tag_name (Optional[str], optional):     Use in RENAME_TAG. Defaults to None.
        domain_name (Optional[str], optional):      Use in ADD_DOMAIN, REMOVE_DOMAIN, Defaults to None.
        new_domain_name (Optional[str], optional):  Use in RENAME_DOMAIN. Defaults to None.
    """
    metadata = load_metadata(config)
    if not metadata:
        metadata = {}
        key, data = init_metadata(file_name)
        metadata[key] = data
        metadata[key]["tag"].append(tag_name)
    else:
        key = file_name
    new_key = new_file_name
    # -------------------------------------------------------
    # ADD_TAG 
    if action_type == "ADD_TAG":
        if key in metadata:
            is_consistent = version_check(metadata[key])
            if not is_consistent:
                recover_missing_keys(metadata)

            if tag_name not in metadata[key]["tag"]:
                metadata[key]["tag"].append(tag_name)
        else:
            key, data = init_metadata(file_name)
            metadata[key] = data
            metadata[key]["tag"].append(tag_name)

        dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # REMOVE_TAG
    elif action_type == "REMOVE_TAG":
        if key in metadata:
            if tag_name in metadata[key]["tag"]:
                metadata[key]["tag"].remove(tag_name)
                dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # RENAME_TAG
    elif action_type == "RENAME_TAG":
        for key, data in metadata.items():
            if tag_name in data["tag"]:
                metadata[key]["tag"].remove(tag_name)
                metadata[key]["tag"].append(new_tag_name)
        dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # ADD_DOMAIN
    elif action_type == "ADD_DOMAIN":
        if key in metadata:
            is_consistent = version_check(metadata[key])
            if not is_consistent:
                recover_missing_keys(metadata)

            if domain_name not in metadata[key]["domain"]:
                metadata[key]["domain"].append(domain_name)
        else:
            key, data = init_metadata(file_name)
            metadata[key] = data
            metadata[key]["domain"].append(domain_name)

        dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # REMOVE_DOMAIN
    elif action_type == "REMOVE_DOMAIN":
        if key in metadata:
            if domain_name in metadata[key]["domain"]:
                metadata[key]["domain"].remove(domain_name)
                dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # RENAME_DOMAIN
    elif action_type == "RENAME_DOMAIN":
        for key, data in metadata.items():
            if domain_name in data["domain"]:
                metadata[key]["domain"].remove(domain_name)
                metadata[key]["domain"].append(new_domain_name)
        dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    # RENAME_FILE
    elif action_type == "RENAME_FILE":
        if key in metadata:
            metadata[new_key] = metadata[key]
            del metadata[key]
            dump_metadata_json(metadata, config)
    # -------------------------------------------------------
    else:
        raise Exception(f"No such action type: {action_type}")