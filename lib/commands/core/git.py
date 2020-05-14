import os
import re
from pprint import pprint
from typing import List, Dict
from datetime import datetime, timezone
from lib.commands.core.shell import fixed_path_shell
from lib.commands.core.configure import load_config, Config
from lib.commands.core.custom_types import Datetime, Diffs, Stamps
from lib.commands.core.dir_ops import get_dir_path


def git_diff() -> Diffs:
    cmd1: str = "git diff --histogram"
    output: str = fixed_path_shell(cmd1)

    lines: List[str] = output.split("\n")
    separate_pattern: str = "diff --git "
    group: Diffs = {}
    file_name = ""

    for line in lines:
        if re.match(separate_pattern, line):
            file_name: str = re.sub("a/", "", re.sub(separate_pattern, "", line).split(" ")[0])
            group[file_name] = []

        if file_name in group:
            group[file_name].append(line)

    return group


def untraced_file_gpaths() -> List[str]:
    cmd: str = "git status"
    output: str = fixed_path_shell(cmd)
    lines: List[str] = output.split("\n")
    files: List[str] = []

    untrack_start_patern = "Untracked files:"
    untrack_file_patern = "\t"
    untrack_area_start = False

    for line in lines:
        if re.match(untrack_start_patern, line):
            untrack_area_start = True
        if untrack_area_start:
            if re.match(untrack_file_patern, line):
                files.append(line.strip())

    return files


def changed_file_gpaths() -> List[str]:
    cmd: str = "git status"
    output: str = fixed_path_shell(cmd)

    lines: List[str] = output.split("\n")
    files: List[str] = []
    pattern: str = "(\tmodified:|\tnew file:)"
    renamed_pattern: str = "\trenamed:"

    for line in lines:
        file_name = None
        is_renamed = re.match(renamed_pattern, line)

        if re.match(pattern, line):
            file_name: str = re.sub(pattern, "", line).strip()

            if file_name not in files:
                files.append(file_name)

        elif is_renamed:
            file_names: str = re.sub(renamed_pattern, "", line).strip()
            renamed_from, _ = file_names.split(" -> ")
            files.append(renamed_from)

    return files


def fullpath(files: List[str]) -> List[str]:
    config: Config = load_config()
    root_path: str = config["root_path"]
    return [f"{root_path}/{file_name}" for file_name in files]


def make_time_stamp() -> str:
    now: Datetime = datetime.now()
    time: str = str(now.replace(microsecond=0))
    tzname: str = str(now.astimezone().tzname())
    return time + " " + tzname


def make_diff_stamp(file_name: str, diffs: Diffs, separator: str = "") -> str:
    stamp_text: str = ""
    if file_name in diffs:
        stamp_text = "\n".join(
            [line for line in diffs[file_name] if line != r"\ No newline at end of file"]
            )
        if separator:
            stamp_text = f"{separator}\n{stamp_text}"

    return stamp_text


def make_stamp() -> Stamps:
    stamps = {}
    gpaths = changed_file_gpaths()
    diffs: Diffs = git_diff()

    for gpath in gpaths:
        stamps[gpath] = {}
        stamps[gpath]["timestamp"] = f"{make_time_stamp()}\n"
        stamps[gpath]["diff"] = make_diff_stamp(gpath, diffs)

    return stamps