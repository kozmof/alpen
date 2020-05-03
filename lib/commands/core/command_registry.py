import re
from typing import List
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path

def register_edit_command(editor: str, user_input: str, use_todo_dir: bool = False) -> List[str]:
    config: Config = load_config()
    elements = list(filter(lambda x:x, user_input.split(" ")))
    if use_todo_dir:
        dir_path = get_dir_path("TODO", config)
    else:
        dir_path = get_dir_path("DOCUMENT", config)
    command = [editor] + list(
        map(
            lambda x: dir_path + "/" + x if not re.match(
                "{plus}|{minus}".format(
                    plus=r"\+",
                    minus=r"\-"),
                    x
                ) else x, elements
            )
    )
    return command