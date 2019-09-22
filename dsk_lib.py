import os
import cmd
import subprocess
from pprint import pprint
from git_stamp import git_diff
from configure import load_config, Config
from command_registry import register_command 
from configure import document_dir
from typing import List


class DSKShell(cmd.Cmd):
    ascii_art = " _____     ______     __  __ \n/\  __-.  /\  ___\   /\ \/ / \n\ \ \/\ \ \ \___  \  \ \  _\"-. \n \ \____-  \/\_____\  \ \_\ \_\ \n  \/____/   \/_____/   \/_/\/_/"
    description = "commands\n"\
                  " build: build texts\n"\
                  " list: list all documents\n"\
                  " edit: edit documents\n"\
                  " exit: exit"

    intro = "{}\n{}".format(ascii_art, description)  
    prompt = "|> "

    def do_build(self, arg):
        pass

    def do_list(self, arg):
        doc_dir = document_dir()
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
        pprint(git_diff())

    def do_edit(self, arg):
        config: Config = load_config()
        editor: str = config["editor"]
        command: List[str] = register_command(editor, arg)
        subprocess.run(command)

    def do_clear(self, arg):
        subprocess.run(["clear"])
        print(self.intro)

    def do_exit(self, arg):
        return True