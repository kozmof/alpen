import os
from lib.commands.c_edit import c_edit
from lib.commands.core.memo import memo_dir_path


def c_memo(self):
    MEMO_DIR_PATH = memo_dir_path()

    if os.path.isdir(MEMO_DIR_PATH):
        c_edit("todo.md", use_todo_dir=True)
    else:
        os.makedirs(MEMO_DIR_PATH)
        c_edit("todo.md", use_todo_dir=True)

    self.do_clear(None)              