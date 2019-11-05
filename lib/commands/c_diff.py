import re
from .core.git_stamp import combine_stamp
from .core.color import color
from .core.parser import color_diff
from .core.git_stamp import untracked_files
from .core.configure import load_config
from .core.custom_types import Config


def c_diff():
    config: Config = load_config()
    uuid = config["uuid"]
    for file_name, diff_text in combine_stamp(enable_time_stamp=False).items():
        if not re.match(f"\.docs\/{uuid}\/todo", file_name):
            print(color(file_name, color_type="green"))
            print(color_diff(diff_text))

    untracked_f = untracked_files()
    if untracked_f:
        print(color("Untracked files:", color_type="yellow"))
        for file_name in untracked_files():
            print(color("\t" + file_name, color_type="yellow"))