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
    command: List[str] = register_edit_command(
        editor,
        arg,
        use_todo_dir=use_todo_dir,
        use_memo_dir=use_memo_dir
        )
    subprocess.run(command)