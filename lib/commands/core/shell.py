import os
import subprocess
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config


def fpshell(cmd: str) -> str:
    config: Config = load_config()
    root_path = config["root_path"]
    cwd = os.getcwd()
    os.chdir(root_path)
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    os.chdir(cwd)
    return output
