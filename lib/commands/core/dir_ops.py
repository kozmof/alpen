import os
from .custom_types import Config


def get_dir_name(dir_type: str) -> str
    if dir_type == "DOCUMENT":
        return ".doc"
    elif dir_type == "HISTORY":
        return ".history"
    elif dir_type == "TODO":
        return ".todo"
    elif dir_type == "TAG":
        return ".tags"
    elif dir_type == "METADATA":
        return ".metadata"
    else:
        raise Exception(f"No such dir_type: {dir_type}")


def get_dir_path(dir_type: str, config: Config) -> str:
    dir_name = get_dir_name(dir_type)
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    doc_dir = f"{root_path}/{dir_name}/{uuid}"
    return doc_dir


def make_directory(dir_type: str, config: Config) -> None:
    dir_path = get_dir_path(dir_type, config)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)