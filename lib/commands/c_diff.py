import re
from lib.commands.core.git import make_stamp, untracked_file_gpaths
from lib.commands.core.color import color
from lib.commands.core.parser import color_diff
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config


def c_diff():
    config: Config = load_config()
    uuid = config["uuid"]
    for file_name, stamp in make_stamp().items():
        if not re.match(fr".docs/{uuid}/todo", file_name):
            if re.match(fr".docs/{uuid}", file_name):
                print(color(file_name, color_type="green"))
                print(color_diff(stamp["diff"]))

    ut_gpaths = untracked_file_gpaths()
    if ut_gpaths:
        print(color("Untracked files:", color_type="yellow"))
        for ut_gpath in ut_gpaths:
            print(color("\t" + ut_gpath, color_type="yellow"))