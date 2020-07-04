"""Renaming utilities
"""
import re
from typing import Tuple, Optional

from lib.commands.core.tag import manipulate_tag_data
from lib.commands.core.domain import manipulate_domain_data
from lib.commands.core.metadata import manipulate_metadata
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config

def arg_to_names(arg: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse arguments and get an original name and a new name

    Args:
        arg (str): rename <rename_from> <rename_to>

    Returns:
        Tuple[Optional[str], Optional[str]]: An original name and a new name
    """
    result_1 = list(re.findall("\'", arg))
    result_2 = list(re.findall('\"', arg))
    original_name = None
    new_name = None

    if len(result_1) == 4:
        result = result_1
    elif len(result_2) == 4:
        result = result_2
    else:
        result = None

    if not result:
        names = arg.split(" ")

    if not result and len(names) != 2:
        print("Invalid syntax. rename <rename_from> <rename_to>")
        return None, None
    else:
        if len(names) == 2:
            original_name = names[0]
            new_name = names[1]
        elif result:
            original_name = arg[result[0].end():result[1].start()]
            new_name = arg[result[2].end():result[3].start()]
        else:
            raise Exception("logical error")

    return original_name, new_name


def apply_rename(file_name: str, new_file_name: str, config: Config) -> None:
    """Rename a file and change related data

    Args:
        file_name (str): A file name
        new_file_name (str): A new file name
        config (Config): Config data
    """
    manipulate_tag_data("RENAME_FILE", config, file_name=file_name, new_file_name=new_file_name)
    manipulate_domain_data("RENAME_FILE", config, file_name=file_name, new_file_name=new_file_name)
    manipulate_metadata("RENAME_FILE", config, file_name=file_name, new_file_name=new_file_name)