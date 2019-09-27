import os
import cmd
import subprocess
from pprint import pprint
from gprint import grid_text
from color import color
from parser import color_diff
from git_stamp import combine_stamp
from typing import List, Callable
from command_registry import register_edit_command 
from dir_ops import document_dir
from custom_types import Config, Shorthand
from configure import load_config, load_shorthand
from record import record_edited_file, read_edited_file_record


def ascii_art():
    config: Config = load_config()
    if config["enable_ascii_art"]:
        art = " _____     ______     __  __ \n/\  __-.  /\  ___\   /\ \/ / \n\ \ \/\ \ \ \___  \  \ \  _\"-. \n \ \____-  \/\_____\  \ \_\ \_\ \n  \/____/   \/_____/   \/_/\/_/"
        return art + "\n\n"
    else:
        return ""


def change_log() -> str:
    return f"recently edited\n{read_edited_file_record()}" 


class DSKShell(cmd.Cmd):
    shorthand: Shorthand = load_shorthand()
    description = "commands\n"\
                  " build ({build_short}): build texts\n"\
                  " list ({list_short}): list all documents\n"\
                  " edit ({edit_short}): edit documents\n"\
                  " diff ({diff_short}): show diff (before commit)\n"\
                  " clear ({clear_short}): clear\n"\
                  " quit ({quit_short}): quit".format(build_short=shorthand["build"],
                                                      list_short=shorthand["list"],
                                                      edit_short=shorthand["edit"],
                                                      diff_short=shorthand["diff"],
                                                      clear_short=shorthand["clear"],
                                                      quit_short=shorthand["quit"])

    left_side = f"{ascii_art()}{description}"
    right_side = change_log()
    intro = grid_text(left_side, right_side, margin=5)
    prompt = "|> "

    def do_build(self, arg):
        pass

    def do_list(self, arg):
        config: Config = load_config()
        doc_dir = document_dir(config)
        for file_name in sorted(os.listdir(doc_dir)):
            print(file_name)

    def do_tag(self, arg):
        if arg == "add":
            print("DEBUG ADD")
        elif arg == "delete":
            print("DEBUG DELETE")
        elif arg == "search":
            print("DEBUG SEARCH")

    def do_diff(self, arg):
        for file_name, diff_text in combine_stamp(enable_time_stamp=False).items():
            print(color(file_name, color_type="green"))
            print(color_diff(diff_text))

    def do_edit(self, arg):
        config: Config = load_config()
        editor: str = config["editor"]
        record_edited_file(arg)
        command: List[str] = register_edit_command(editor, arg)
        subprocess.run(command)

    def complete_edit(self, text: str, linei: str, start_index: int, end_index: int) -> List[str]:
        return ["complete test"]

    def do_clear(self, arg):
        subprocess.run(["clear"])
        print(self.intro)

    def do_quit(self, arg):
        return True

    @classmethod
    def set_shorthand(cls):
        shorthand: Shorthand = load_shorthand()
        mmapper: Dict[str, Callable] = {
          "build": cls.do_build,
          "list": cls.do_list,
          "edit": cls.do_edit,
          "diff": cls.do_diff,
          "clear": cls.do_clear,
          "quit": cls.do_quit
        }
        for key, value in shorthand.items():
            setattr(cls, f"do_{value}", mmapper[key])