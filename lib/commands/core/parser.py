import re
from typing import List
from .color import CYANC, BLUEC, ENDC


def color_diff(diff_text: str) -> str:
    diff_lines = diff_text.split("\n")
    colored_text = ""

    for line in diff_lines:
        if re.match("\+", line):
            colored_text += f"{CYANC}{line}{ENDC}\n" 
        elif re.match("\-", line):
            colored_text += f"{BLUEC}{line}{ENDC}\n" 
        else:
            colored_text += f"{line}\n"

    return colored_text

