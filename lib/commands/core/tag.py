import os
import json
from configure import load_config
from dir_ops import get_dir_path
from metadata import (init_metadata, 
                      version_check,
                      recover_missing_keys,
                      METADATA_FILE,
                      CURENT_FORMAT_VERSION)
from custom_types import Config

TAG_FILE = "tags.json"

def add_tag(file_name, tag_name):
    config: Config = load_config()

    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"

    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"

    if os.path.isfile(tag_file_path):
        with open(tag_file_path, "r+") as fpt:
            tag_data = json.load(fpt)

            if tag_name in tag_data:
                if file_name not in tag_data[tag_name]:
                    tag_data[tag_name].append(file_name)
            else:
                tag_data[tag_name] = [file_name]

            json.dump(tag_data, fpt)
    else:
        tags = {}
        tags[tag_name] = [file_name]
        with open(tag_file_path, "w") as fpt:
            json.dump(tags, fpt)

    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path, "r") as fpm:
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