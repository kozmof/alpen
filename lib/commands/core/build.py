import os
import json
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.custom_types import Config
from lib.commands.core.metadata import load_metadata, METADATA_FILE
from lib.commands.core.tag import load_tag_data, TAG_FILE

BUILD_PAYLOAD_FILE = "build.payload.json"


def extract(file_names, tagged_files):
    return [tagged_file for tagged_file in tagged_files if tagged_file in file_names]


def load(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    else:
        return ""


def load_json(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return json.load(f)


def make_build_config_file(file_names):
    print(type(file_names))
    config: Config = load_config()
    root_dir = config["root_path"]
    doc_dir = get_dir_path("DOCUMENT", config)
    history_dir = get_dir_path("HISTORY", config)

    metadata = load_metadata(config) or []
    tag_data = load_tag_data(config) or {}

    build_config = {
        "pages": {
            file_name: {
                "doc": load(f"{doc_dir}/{file_name}"),
                "history": load_json(
                    f"{history_dir}/{os.path.splitext(file_name)[0]}-{os.path.splitext(file_name)[1]}.json"
                    ),
                "tag": metadata[file_name].get("tag", []) if file_name in metadata else []
            } for file_name in file_names
        },
        "tags": {
            tag: extract(file_names, tagged_files) for tag, tagged_files in tag_data.items()
            }
    }

    save_path = "{root_dir}/publish/{build_file}".format(
        root_dir=root_dir,
        build_file=BUILD_PAYLOAD_FILE
        )

    with open(save_path, "w") as f:
        json.dump(build_config, f, indent=4, sort_keys=True)