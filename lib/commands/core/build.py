import json
from .configure import load_config
from .dir_ops import get_dir_path
from .custom_types import Config
from .metadata import METADATA_FILE
from .tag import TAG_FILE


def extract(file_names, tagged_files):
    return [tagged_file for tagged_file in taggedfiles if tagged_file in file_names]


def make_build_config(file_names):
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    history_dir = get_dir_path("HISTORY", config)

    metadata_dir = get_dir_path("METADATA", config)
    metadata_file_path = f"{metadata_dir}/{METADATA_FILE}"
    with open(metadata_file_path, "r") as f:
        metadata = json.load(f)

    tag_dir = get_dir_path("TAG", config)
    tag_file_path = f"{tag_dir}/{TAG_FILE}"
    with open(tag_file_path, "r") as f:
        tag_data = json.load(f)

    build_config = {
        "pages": {
            file_name: {
                "doc": f"{doc_dir}/{file_name}",
                "history": f"{history_dir}/{file_name}",
                "tag": metadata[file_name]
            } for file_name in file_names
        },

        "tags" {tag: extract(file_names, tagged_files) for tag, tagged_files in tag_data.items()}
    }

    return build_config