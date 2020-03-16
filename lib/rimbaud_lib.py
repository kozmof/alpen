import cmd

from .commands.c_build import c_build
from .commands.c_list import c_list
from .commands.c_tag import c_tag
from .commands.c_diff import c_diff
from .commands.c_edit import c_edit
from .commands.c_rename import c_rename
from .commands.c_save_history import c_save_history
from .commands.c_todo import c_todo
from .commands.c_clear import c_clear, change_log
from .commands.c_tutorial import c_tutorial

from typing import Optional, List, Dict, Callable
from .commands.core.gprint import grid_text
from .commands.core.todo import get_todo
from .commands.core.custom_types import Shorthand
from .commands.core.configure import load_shorthand


class RimbaudShell(cmd.Cmd):
    grid_0 = "Welcome back hacker"
    grid_1 = change_log()
    grid_2 = get_todo()
    intro = grid_text(grid_0, grid_1, grid_2, margin=5)
    prompt = "|> "

    def do_build(self, _):
        c_build()

    def do_list(self, _):
        c_list()

    def do_tag(self, arg):
        c_tag(arg)

    def do_diff(self, _):
        c_diff()

    def do_edit(self, arg):
        c_edit(arg)

    def do_rename(self, arg):
        c_rename(arg)

    def do_save_history(self, _):
        c_save_history()

    def do_todo(self, option):
        c_todo(self, option)

    # TODO implement
    def complete_edit(self, text: str, linei: str, start_index: int, end_index: int) -> List[str]:
        return ["complete test"]

    def do_clear(self, option):
        if option == "s":
            show_grid = True
        else:
            show_grid = False
        c_clear(show_grid=show_grid)

    def do_tutorial(self, _):
        c_tutorial()

    def do_quit(self, _):
        return True

    @classmethod
    def set_shorthand(cls):
        shorthand: Shorthand = load_shorthand()
        mmapper: Dict[str, Callable] = {
          "build": cls.do_build,
          "list": cls.do_list,
          "edit": cls.do_edit,
          "tag": cls.do_tag,
          "rename": cls.do_rename,
          "save_history": cls.do_save_history,
          "todo": cls.do_todo,
          "diff": cls.do_diff,
          "clear": cls.do_clear,
          "tutorial": cls.do_tutorial,
          "quit": cls.do_quit
        }
        for key, value in shorthand.items():
            setattr(cls, f"do_{value}", mmapper[key])