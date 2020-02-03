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

from typing import Optional, List, Dict, Callable
from .commands.core.gprint import grid_text
from .commands.core.todo import get_todo
from .commands.core.custom_types import Shorthand
from .commands.core.configure import load_shorthand


class DSKShell(cmd.Cmd):
    shorthand: Shorthand = load_shorthand()
    description = "commands\n"\
                  " build ({build_short}): build texts\n"\
                  " list ({list_short}): list all documents\n"\
                  " edit ({edit_short}): edit documents\n"\
                  " tag ({tag_short}): tag documents\n"\
                  " rename ({rename_short}): raname a document\n"\
                  " save_history ({save_history_short}): save diffs\n"\
                  " todo ({todo_short}): edit todo list\n"\
                  " diff ({diff_short}): show diff (before stage)\n"\
                  " clear ({clear_short}): clear\n"\
                  " quit ({quit_short}): quit".format(build_short=shorthand["build"],
                                                      list_short=shorthand["list"],
                                                      edit_short=shorthand["edit"],
                                                      tag_short=shorthand["tag"],
                                                      rename_short=shorthand["rename"],
                                                      save_history_short=shorthand["save_history"],
                                                      todo_short=shorthand["todo"],
                                                      diff_short=shorthand["diff"],
                                                      clear_short=shorthand["clear"],
                                                      quit_short=shorthand["quit"])

    grid_0 = description
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
        c_clear(self.description, show_grid=show_grid)

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
          "quit": cls.do_quit
        }
        for key, value in shorthand.items():
            setattr(cls, f"do_{value}", mmapper[key])