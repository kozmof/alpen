"""Directory ops
"""

import os
from typing import Optional
from lib.commands.core.custom_types import Config


def get_dir_name(dir_type: str) -> str:
    """Get a specific directory name

    Args:
        dir_type (str): A type of directory

    Returns:
        str: A name of directory
    """
    if dir_type == "DOCUMENT":
        return ".docs"
    elif dir_type == "HISTORY":
        return ".histories"
    elif dir_type == "TODO":
        return ".todo"
    elif dir_type == "MEMO":
        return ".memo"
    elif dir_type == "TAG":
        return ".tags"
    elif dir_type == "DOMAIN":
        return ".domains"
    elif dir_type == "METADATA":
        return ".metadata"
    else:
        raise Exception(f"No such dir_type: {dir_type}")


def get_dir_path(dir_type: str, config: Config) -> Optional[str]:
    """Get an absolute path of directory

    Args:
        dir_type (str): A directory type
        config (Config): Config data

    Returns:
        Optional[str]: A path
    """
    dir_name = get_dir_name(dir_type)
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    if root_path and uuid:
        doc_dir = f"{root_path}/{dir_name}/{uuid}"
        return doc_dir
    else:
        return None


def make_directory(dir_type: str, config: Config) -> None:
    """Make a specific directory if it doesn't exist

    Args:
        dir_type (str): A directory type
        config (Config): Config data
    """
    dir_path = get_dir_path(dir_type, config),
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)