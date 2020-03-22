from lib.commands.core.configure import load_config
from lib.commands.core.tag import update_tag_file
from lib.commands.core.metadata import update_metadata_file
from lib.commands.core.consistency import doc_file_exists
from lib.commands.core.custom_types import Config


def add_tag(file_name, tag_name):
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        update_tag_file("ADD_TAG", config, file_name=file_name, tag_name=tag_name)
        update_metadata_file("ADD_TAG", config, file_name=file_name, tag_name=tag_name)
        print(f"{tag_name} added to {file_name}")


def remove_tag(file_name, tag_name):
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        update_tag_file("REMOVE_TAG", config, file_name=file_name, tag_name=tag_name)
        update_metadata_file("REMOVE_TAG", config, file_name=file_name, tag_name=tag_name)
        print(f"{tag_name} removed from {file_name}")


def rename_tag(tag_name, new_tag_name):
    config: Config = load_config()
    update_tag_file("RENAME_TAG", config, tag_name=tag_name, new_tag_name=new_tag_name)
    update_metadata_file("RENAME_TAG", config, tag_name=tag_name, new_tag_name=new_tag_name)
    print(f"{tag_name} renamed to {new_tag_name}")


def search_tag(tag_name):
    config: Config = load_config()
    update_tag_file("SEARCH_TAG", config, tag_name=tag_name)


def show_all():
    config: Config = load_config()
    update_tag_file("SHOW_ALL", config)

    