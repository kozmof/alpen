"""Tag operations
"""
from typing import List
from lib.commands.core.configure import load_config
from lib.commands.core.tag import manipulate_tag_data
from lib.commands.core.metadata import manipulate_metadata
from lib.commands.core.consistency import doc_file_exists
from lib.commands.core.custom_types import Config


def add_tag(file_name: str, tag_name: str) -> None:
    """Add a tag

    Args:
        file_name (str): A file name to add a tag
        tag_name (str): A tag name
    """
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        manipulate_tag_data("ADD_TAG", config, file_name=file_name, tag_name=tag_name)
        manipulate_metadata("ADD_TAG", config, file_name=file_name, tag_name=tag_name)
        print(f"{tag_name} added to {file_name}")


def remove_tag(file_name: str, tag_name: str) -> None:
    """Remove a tag

    Args:
        file_name (str): A file name to remove a tag
        tag_name (str): A tag name
    """
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        manipulate_tag_data("REMOVE_TAG", config, file_name=file_name, tag_name=tag_name)
        manipulate_metadata("REMOVE_TAG", config, file_name=file_name, tag_name=tag_name)
        print(f"{tag_name} removed from {file_name}")


def rename_tag(tag_name: str, new_tag_name: str) -> None:
    """Rename a tag

    Args:
        tag_name (str): A tag name to be renamed
        new_tag_name (str): A new tag name
    """
    config: Config = load_config()
    manipulate_tag_data("RENAME_TAG", config, tag_name=tag_name, new_tag_name=new_tag_name)
    manipulate_metadata("RENAME_TAG", config, tag_name=tag_name, new_tag_name=new_tag_name)
    print(f"{tag_name} renamed to {new_tag_name}")


def search_tag(tag_name: str) -> None:
    """Search a tag and print related file names

    Args:
        tag_name (str): A tag to search
    """
    config: Config = load_config()
    manipulate_tag_data("SEARCH_TAG", config, tag_name=tag_name)


def show_all() -> None:
    """Show all tag data
    """
    config: Config = load_config()
    manipulate_tag_data("SHOW_ALL", config)