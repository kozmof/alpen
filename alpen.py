#!/usr/bin/python3
import os
from lib.alpen_lib import AlpenShell
from lib.commands.core.configure import (init,
                                         save_root_path,
                                         save_uuid, config_editor,
                                         CONFIG_PATH,
                                         load_config,
                                         SHORTHAND_PATH)
from lib.commands.core.dir_ops import make_directory

if __name__ == "__main__":
    if (os.path.isfile(CONFIG_PATH) and
        os.path.isfile(SHORTHAND_PATH)):
        AlpenShell.set_shorthand()
        AlpenShell().cmdloop()
    else:
        print("Welcome!")
        init()
        save_root_path()
        save_uuid()
        config_editor(editor="code")
        dirs = ["DOCUMENT", "HISTORY", "TODO", "METADATA", "TAG"]
        config  = load_config()
        for d in dirs:
            make_directory(d, config)
        print("Complete init")
 
