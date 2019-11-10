import re
import os
import subprocess
from typing import List
from .core.custom_types import Config
from .core.configure import load_config
from .core.record import record_edited_file
from .core.command_registry import register_edit_command
from .core.dir_ops import document_dir


def c_edit(arg):
    config: Config = load_config()
    editor: str = config["editor"]
    record_edited_file(arg)
    doc_dir = document_dir(config)
    doc_files: List = [f for f in os.listdir(doc_dir) if os.path.isfile(os.path.join(doc_dir, f))]
    is_editable = False
    is_new_name = True

    for f in doc_files:
        body, _ = os.path.splitext(f)
        m_body = re.search(body, arg)
        if m_body:
            m_full = re.search(f, arg)
            if m_full and m_body.start() and m_full.start():
                is_editable = True
                break
            else:
                is_new_name = False

    if is_editable or is_new_name:
        command: List[str] = register_edit_command(editor, arg)
        subprocess.run(command)
    else:
        print("Using a same name with different extensions are not allowed.")