import re
from typing import List
from lib.commands.core.color import CYANC, BLUEC, ENDC


def color_diff(diff_text: str) -> str:
    diff_lines = diff_text.split("\n")
    colored_text = ""

    for line in diff_lines:
        if re.match(r"\+", line):
            colored_text += f"{CYANC}{line}{ENDC}\n" 
        elif re.match(r"\-", line):
            colored_text += f"{BLUEC}{line}{ENDC}\n" 
        else:
            colored_text += f"{line}\n"

    return colored_text

