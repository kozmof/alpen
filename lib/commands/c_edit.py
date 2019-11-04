import subprocess
from typing import List
from .core.custom_types import Config
from .core.configure import load_config
from .core.record import record_edited_file
from .core.command_registry import register_edit_command


def c_edit(arg):
    config: Config = load_config()
    editor: str = config["editor"]
    record_edited_file(arg)
    command: List[str] = register_edit_command(editor, arg)
    subprocess.run(command)