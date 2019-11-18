import json
from typing import Optional, List
from custom_types import Config

METADATA_FILE = "metadata.json"
CURENT_FORMAT_VERSION = "1.0"

FORMAT = {
  "tag": [],
  "version": CURENT_FORMAT_VERSION
}


def init_metadata(file_name):
    key = file_name
    val = FORMAT[CURENT_FORMAT_VERSION]
    return key, val


def version_check(metadata):
    if metadata["version"] == CURENT_FORMAT_VERSION:
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
            metadta = json.load(fpm)
            if file_name in metadta:
                return metadta[file_name]["tag"]


def arg_check_m(action_type: str):
    if action_type == "ADD_TAG":
        if tag_name is None and new_file_name:
            raise Exception("Pass only tag_name")
    elif action_type == "RENAME":
        if new_file_name is None and tag_name:
            raise Exception("Pass only new_file_name")
    else:
        raise Exception(f"No such action type: {action_type}")


def update_metadata_file(action_type: str, file_name: str, config: Config, tag_name: Optional[str] = None, new_file_name: Optional[str] = None):
    arg_check_m(config)
    if action_type == "ADD_TAG":
        metadata_dir = get_dir_path("METADATA", config)
        metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

        if os.path.isfile(metadata_file_path):
            with open(metadata_file_path, "r+") as fpm:
                metadata = json.load(fpm)

                if file_name in metadata:

                    is_consistent = version_check(metadata):
                    if not is_consistent:
                        recover_missing_keys(metadata)

                    if tag_name not in metadata[file_name]["tag"]:
                        metadata[file_name]["tag"].append(tag)
                else:
                    key, data = init(file_name)
                    metadata[key] = data
                    metadata[key]["tag"].append(tag_name)

                json.dump(metadata, fpm)
        else:
            metadata = {}
            key, data = init_metadata(file_name)
            metadata[key] = data
            metadata[key]["tag"].append(tag_name)

            with open(metadata_file_path, "w") as fpm:
                json.dump(metadata, fpm)

    elif action_type == "RENAME":
        metadata_dir = get_dir_path("METADATA", config)
        metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

        if os.path.isfile(metadata_file_path):
            with open(metaedata_file_path, "r+", as fpm):
                metadata = json.load(fpm)
                if file_name in metadta:
                    metadata[new_file_name] = metadata[file_name]
                    del metadata[file_name]

                json.dump(metatdata, fpm)
    else:
        raise Exception(f"No such action type: {action_type}")