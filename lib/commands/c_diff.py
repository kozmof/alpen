from .core.git_stamp import combine_stamp
from .core.color import color
from .core.parser import color_diff
from .core.git_stamp import untracked_files


def c_diff():
    for file_name, diff_text in combine_stamp(enable_time_stamp=False).items():
        print(color(file_name, color_type="green"))
        print(color_diff(diff_text))

    untracked_f = untracked_files()
    if untracked_f:
        print(color("Untracked files:", color_type="yellow"))
        for file_name in untracked_files():
            print(color("\t" + file_name, color_type="yellow"))