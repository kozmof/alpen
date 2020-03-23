#!/usr/bin/python3
import os
from lib.rimbaud_lib import RimbaudShell
from lib.commands.core.configure import CONFIG_PATH, SHORTHAND_PATH

if __name__ == "__main__":
    if (os.path.isfile(CONFIG_PATH) and
        os.path.isfile(SHORTHAND_PATH)):
        RimbaudShell.set_shorthand()
        RimbaudShell().cmdloop()
    else:
        print("Welcome!")
 
