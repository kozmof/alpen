import re
import os
import subprocess
from typing import List
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.command_registry import register_edit_command
from lib.commands.core.dir_ops import get_dir_path


def c_edit(arg, use_todo_dir=False, use_memo_dir=False):
    config: Config = load_config()
    editor: str = config["editor"]
    file_pos: str = config["editor_file_pos"]
    try:
        file_name = arg.split(" ")[file_pos]
    except IndexError:
        print("Invalid file input")
        return
    command: List[str] = register_edit_command(
        editor=editor,
        file_name=file_name,
        user_input=arg,
        use_todo_dir=use_todo_dir,
        use_memo_dir=use_memo_dir
        )
    subprocess.run(command)