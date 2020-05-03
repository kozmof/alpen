import re
from lib.commands.core.git import combine_stamp, untraced_file_gpaths
from lib.commands.core.color import color
from lib.commands.core.parser import color_diff
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config


def c_diff():
    config: Config = load_config()
    uuid = config["uuid"]
    for file_name, diff_text in combine_stamp(enable_time_stamp=False).items():
        if not re.match(fr".docs/{uuid}/todo", file_name):
            if re.match(fr".docs/{uuid}", file_name):
                print(color(file_name, color_type="green"))
                print(color_diff(diff_text))

    untracked_f = untraced_file_gpaths()
    if untracked_f:
        print(color("Untracked files:", color_type="yellow"))
        for file_name in untraced_file_gpaths():
            print(color("\t" + file_name, color_type="yellow"))