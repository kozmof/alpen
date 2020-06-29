"""Shell command utilities
"""
import os
import subprocess
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config


def fpshell(cmd: str) -> str:
    """Execute a shell command at a fixed point

    Args:
        cmd (str): A shell command

    Returns:
        str: A result of a command
    """
    config: Config = load_config()
    root_path = config["root_path"]
    cwd = os.getcwd()
    os.chdir(root_path)
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    os.chdir(cwd)
    return output