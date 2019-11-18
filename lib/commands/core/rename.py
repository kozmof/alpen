from tag import update_tag_file
from metadata import update_metadata_file
from custom_types import Config


def apply_rename(config: Config):
    update_tag_file("RENAME", file_name, config, new_file_name=new_file_name)
    update_metadata_file("RENAME", file_name, config, new_file_name=new_file_name)