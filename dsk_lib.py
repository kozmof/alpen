import os
import cmd
from pprint import pprint
from git_stamp import git_diff
from configure import load_config


class DSKShell(cmd.Cmd):
    ascii_art = " _____     ______     __  __ \n/\  __-.  /\  ___\   /\ \/ / \n\ \ \/\ \ \ \___  \  \ \  _\"-. \n \ \____-  \/\_____\  \ \_\ \_\ \n  \/____/   \/_____/   \/_/\/_/"
    description = "commands\n build: build texts\n list: list all documents\n exit: exit"

    intro = "{}\n{}".format(ascii_art, description)  
    prompt = "> "

    def do_build(self, arg):
        pass

    def do_list(self, arg):
        config = load_config()
        root_path = config["root_path"]
        md_path = "{}/md".format(root_path)
        for file_name in sorted(os.listdir(md_path)):
            print(file_name)

    def do_diff(self, arg):
        pprint(git_diff())

    def do_exit(self, arg):
        return True