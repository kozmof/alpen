import re
import os
from lib.commands.core.configure import load_config, has_config
from lib.commands.core.dir_ops import get_dir_path 

def memo_dir_path():
    return get_dir_path('MEMO', load_config())


def get_memo() -> str:
    MEMO_DIR_PATH = memo_dir_path()
    if not os.path.isdir(MEMO_DIR_PATH):
        os.makedirs(MEMO_DIR_PATH)

    if MEMO_DIR_PATH:
        memo_file_path = f"{MEMO_DIR_PATH}/memo.md"
    else:
        return ""
    if os.path.isfile(memo_file_path):
        with open(memo_file_path, "r") as f:
            text: str = f.read()
            return text
    else:
        init_text = "welcome !"
        with open(memo_file_path, "w") as f:
            f.write(init_text)

        return init_text
