import os
import cmd
import subprocess
from pprint import pprint
from gprint import grid_text
from color import color
from todo import TODO_DIR_PATH, get_todo, toggle_check
from parser import color_diff
from git_stamp import combine_stamp
from typing import List, Callable
from command_registry import register_edit_command 
from dir_ops import document_dir, history_dir
from custom_types import Config, Shorthand
from configure import load_config, load_shorthand
from record import record_edited_file, read_edited_file_record
from shell import fixed_path_shell


def change_log() -> str:
    return f"recently edited\n{read_edited_file_record()}" 


class DSKShell(cmd.Cmd):
    shorthand: Shorthand = load_shorthand()
    description = "commands\n"\
                  " build ({build_short}): build texts\n"\
                  " list ({list_short}): list all documents\n"\
                  " edit ({edit_short}): edit documents\n"\
                  " rename({rename_short}): raname a document\n"\
                  " recover_history({recover_history_short}): recover a missing history file\n"\
                  " todo ({todo_short}): edit todo list\n"\
                  " diff ({diff_short}): show diff (before commit)\n"\
                  " clear ({clear_short}): clear\n"\
                  " quit ({quit_short}): quit".format(build_short=shorthand["build"],
                                                      list_short=shorthand["list"],
                                                      edit_short=shorthand["edit"],
                                                      rename_short=shorthand["rename"],
                                                      recover_history_short=shorthand["recover_history"],
                                                      todo_short=shorthand["todo"],
                                                      diff_short=shorthand["diff"],
                                                      clear_short=shorthand["clear"],
                                                      quit_short=shorthand["quit"])

    grid_0 = description
    grid_1 = change_log()
    grid_2 = get_todo()
    intro = grid_text(grid_0, grid_1, grid_2, margin=5)
    prompt = "|> "

    # TODO implement
    def do_build(self, arg):
        pass

    def do_list(self, arg):
        config: Config = load_config()
        doc_dir = document_dir(config)
        for file_name in sorted(os.listdir(doc_dir)):
            print(file_name)

    # TODO implement
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

    def do_rename(self, arg):
        names = arg.split(" ")
        if len(names) != 2:
            print("Invalid syntax. rename <rename_from> <rename_to>")
        else:
            original_name = names[0]
            new_name = names[1]

            doc_dir = document_dir()
            original_path = f"{doc_dir}/{original_name}"
            new_path = f"{doc_dir}/{new_name}"

            hist_dir = history_dir()
            original_hist_path = f"{hist_dir}/{original_name}"
            new_hist_path = f"{hist_dir}/{new_name}"

            if os.path.isfile(original_path):
                if os.path.isfile(new_path):
                    print(f"{new_name} is already existing. Choose another name")
                else:
                    command = f"mv {original_path} {new_path}"
                    fixed_path_shell(command)
                    if os.path.isfile(original_hist_path):
                        command = f"mv {original_hist_path} {new_hist_path}"
                        fixed_path_shell(command)
                    else:
                        print(f"History file not found: {original_hist_path}")
            else:
                print(f"No such a file: {original_name}")

    def do_todo(self, option):
        if not option:
            if os.path.isdir(TODO_DIR_PATH):
                self.do_edit("todo/todo.md")
            else:
                os.makedirs(TODO_DIR_PATH)
                self.do_edit("todo/todo.md")
        else:
            elems = option.split(" ")
            if elems[0] == "t":
                try:
                    for possibly_num in elems[1:]:
                        toggle_check(int(possibly_num))
                except ValueError:
                    pass

        self.do_clear(None)              

    # TODO implement
    def complete_edit(self, text: str, linei: str, start_index: int, end_index: int) -> List[str]:
        return ["complete test"]

    def do_clear(self, _):
        subprocess.run(["clear"])
        grid_0 = self.description
        grid_1 = change_log()
        grid_2 = get_todo()
        intro = grid_text(grid_0, grid_1, grid_2, margin=5)
        print(intro)

    def do_quit(self, _):
        return True

    @classmethod
    def set_shorthand(cls):
        shorthand: Shorthand = load_shorthand()
        mmapper: Dict[str, Callable] = {
          "build": cls.do_build,
          "list": cls.do_list,
          "edit": cls.do_edit,
          "rename": cls.do_rename,
          "recover_history": cls.do_recover_history,
          "todo": cls.do_todo,
          "diff": cls.do_diff,
          "clear": cls.do_clear,
          "quit": cls.do_quit
        }
        for key, value in shorthand.items():
            setattr(cls, f"do_{value}", mmapper[key])