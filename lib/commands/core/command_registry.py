import re
from typing import List
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.record import record_edited_file


def register_edit_command(editor: str, file_name: str, user_input: str, use_todo_dir: bool = False, use_memo_dir: bool = False) -> List[str]:
    config: Config = load_config()
    elements = list(filter(lambda x:x, user_input.split(" ")))
    if use_todo_dir:
        dir_path = get_dir_path("TODO", config)
    elif use_memo_dir:
        dir_path = get_dir_path("MEMO", config)
    else:
        dir_path = get_dir_path("DOCUMENT", config)
    record_edited_file(file_name=file_name)
    command = [editor] + [dir_path + "/" + x if x == file_name else x for x in elements]
    return command