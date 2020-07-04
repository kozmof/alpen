"""TO-DO utilities
"""
import re
import os
from typing import List
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path 

CHECK_SIGN: str = "- [x]"
UNCHECK_SIGN: str = "- [ ]"


def todo_dir_path() -> str:
    """Get an absolute path of TO-DO directory

    Returns:
        str: A path
    """
    return get_dir_path('TODO', load_config())


def get_todo() -> str:
    """Get TO-DO lists

    Returns:
        str: TO-DO texts
    """
    TODO_DIR_PATH = todo_dir_path()
    if not os.path.isdir(TODO_DIR_PATH):
        os.makedirs(TODO_DIR_PATH)

    if TODO_DIR_PATH:
        todo_file_path = f"{TODO_DIR_PATH}/todo.md"
    else:
        return ""
    if os.path.isfile(todo_file_path):
        with open(todo_file_path, "r") as f:
            lines: List[str] = f.readlines()
            result_todo = ""

            for num, line in enumerate(lines):
                if re.match(f"{re.escape(CHECK_SIGN)}|{re.escape(UNCHECK_SIGN)}", line):
                    result_todo +=  f"{num}.{line[1:]}"
                else:
                    result_todo += line

            return result_todo
    else:
        with open(todo_file_path, "w") as f:
            f.write("")

        return ""


def toggle_check(num: int) -> None:
    """Toggle check and uncheck

    Args:
        num (int): An index to toggle
    """
    TODO_DIR_PATH = todo_dir_path()
    new_todo: str = ""
    try:
        with open(f"{TODO_DIR_PATH}/todo.md", "r") as f:
            lines: List[str] = f.readlines()
            if re.match(re.escape(UNCHECK_SIGN), lines[num]):
                lines[num] = re.sub(re.escape(UNCHECK_SIGN), CHECK_SIGN, lines[num])
            elif re.match(re.escape(CHECK_SIGN), lines[num]):
                lines[num] = re.sub(re.escape(CHECK_SIGN), UNCHECK_SIGN, lines[num])
            new_todo = "".join(lines)

        if new_todo:
            with open(f"{TODO_DIR_PATH}/todo.md", "w") as f:
                f.write(new_todo)
    except IndexError:
        pass