import os
import subprocess
from configure import load_config, Config


def fixed_shell(cmd: str) -> str:
    config: Config = load_config()
    root_path = config["root_path"]
    cwd = os.getcwd()
    os.chdir(root_path)
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    os.chdir(cwd)
    return output
