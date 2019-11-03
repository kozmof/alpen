from typing import List
from unicodedata import east_asian_width


def count_wide_char(line):
    count = 0
    for char in line:
        if east_asian_width(char) in ["W", "F", "A"]:
            count += 1
    return count

TR_ST = "\033[?7l"
TR_ED = "\033[?7h"

def grid_text(*texts, margin: int = 3) -> str:
    whole_max_len: List[int] = []
    max_height: int = 0

    for text in texts:
        lines = text.split("\n")
        height = len(lines)
        max_len = max([len(line) + count_wide_char(line) for line in lines])
        whole_max_len.append(max_len)
        if max_height < height:
            max_height = height

    result_lines = ["" for _ in range(max_height)]

    last_col_pos = len(texts) - 1

    for col_pos, text in enumerate(texts):
        lines = text.split("\n")
        for line_pos, line in enumerate(lines):
            if col_pos == last_col_pos:
                padding = " " * (whole_max_len[col_pos] - len(line) - count_wide_char(line))
            else:
                padding = " " * (whole_max_len[col_pos] - len(line) - count_wide_char(line)) + " " * margin
            result_lines[line_pos] += f"{line}{padding}"

        if len(lines) < max_height:
            line_padding = max_height - len(lines)
            for n in range(line_padding):
                rest_line_pos = n + len(lines)
                if col_pos == last_col_pos:
                    result_lines[rest_line_pos] += " " * whole_max_len[col_pos] 
                else:
                    result_lines[rest_line_pos] += " " * whole_max_len[col_pos] + " " * margin

    result = "\n".join([f"{TR_ST}{result_line}{TR_ED}" for result_line in result_lines])
    return result


def gprint(*texts, margin: int = 3) -> None:
    result = grid_text(*texts, margin=margin)
    print(result)