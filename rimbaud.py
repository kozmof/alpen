#!/usr/bin/python3
import os
from lib.rimbaud_lib import RimbaudShell
from lib.commands.core.configure import (init,
                                         save_root_path,
                                         save_uuid, config_editor,
                                         CONFIG_PATH,
                                         SHORTHAND_PATH)

if __name__ == "__main__":
    if (os.path.isfile(CONFIG_PATH) and
        os.path.isfile(SHORTHAND_PATH)):
        RimbaudShell.set_shorthand()
        RimbaudShell().cmdloop()
    else:
        print("Welcome!")
        init()
        save_root_path()
        save_uuid()
        config_editor(editor="code")
        print("Complete init")
 
