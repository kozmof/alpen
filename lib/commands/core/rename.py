import re
from typing import Tuple, Optional

from lib.commands.core.tag import update_tag_file
from lib.commands.core.metadata import update_metadata_file
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config

def arg_to_names(arg) -> Tuple[Optional[str], Optional[str]]:
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


def apply_rename(file_name, new_file_name, config: Config):
    update_tag_file("RENAME_FILE", config, file_name=file_name, new_file_name=new_file_name)
    update_metadata_file("RENAME_FILE", config, file_name=file_name, new_file_name=new_file_name)