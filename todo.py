import re
import os
from typing import List
from configure import load_config
from dir_ops import document_dir


TODO_DIR_PATH = f"{document_dir(load_config())}/todo"

CHECK_SIGN: str = "- [x]"
UNCHECK_SIGN: str = "- [ ]"


def get_todo() -> str:
    todo_file_path = f"{TODO_DIR_PATH}/todo.md"
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


def toggle_check(num: int) -> None:
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
