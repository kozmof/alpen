import os
from lib.commands.c_edit import c_edit
from lib.commands.core.todo import toggle_check, TODO_DIR_PATH


def c_todo(self, option):
    if not option:
        if os.path.isdir(TODO_DIR_PATH):
            c_edit("todo.md", use_todo_dir=True)
        else:
            os.makedirs(TODO_DIR_PATH)
            c_edit("todo.md", use_todo_dir=True)
    else:
        elems = option.split(" ")
        if elems[0] == "t":
            try:
                for possibly_num in elems[1:]:
                    toggle_check(int(possibly_num))
            except ValueError:
                pass

    self.do_clear(None)              