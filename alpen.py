#!/usr/bin/python3
import os
from lib.alpen_lib import AlpenShell
from lib.commands.core.configure import (CONFIG_PATH,
                                         SHORTHAND_PATH)
from lib.commands.core.dir_ops import make_directory
from lib.commands.core.initialize import initialize

if __name__ == "__main__":
    if (os.path.isfile(CONFIG_PATH) and
        os.path.isfile(SHORTHAND_PATH)):
        AlpenShell.set_shorthand()
        AlpenShell().cmdloop()
    else:
        initialize()