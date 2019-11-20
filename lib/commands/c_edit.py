import re
import os
import subprocess
from typing import List
from .core.custom_types import Config
from .core.configure import load_config
from .core.record import record_edited_file
from .core.command_registry import register_edit_command
from .core.dir_ops import get_dir_path


def c_edit(arg, use_todo_dir=False):
    config: Config = load_config()
    editor: str = config["editor"]

    if use_todo_dir:
        dir_path = get_dir_path("TODO", config)
    else:
        record_edited_file(arg)
        dir_path = get_dir_path("DOCUMENT", config)

    doc_files: List = [file for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file))]
    is_editable = False
    is_new_name = True

    for file_name in doc_files:
        body, _ = os.path.splitext(file_name)
        m_body = re.search(body, arg)
        if m_body:
            m_full = re.search(file_name, arg)
            if m_full and (m_body.start() == m_full.start()):
                is_editable = True
                break
            else:
                is_new_name = False

    if is_editable or is_new_name:
        command: List[str] = register_edit_command(editor, arg, use_todo_dir=use_todo_dir)
        subprocess.run(command)
    else:
        print("Using a same name with different extensions are not allowed.")