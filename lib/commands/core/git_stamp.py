import os
import re
from pprint import pprint
from typing import List, Dict
from datetime import datetime, timezone
from .shell import fixed_path_shell
from .configure import load_config, is_active_file, Config
from .custom_types import Datetime, Diffs, Stamps
from .dir_ops import history_dir


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


def untracked_files() -> List[str]:
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


def changed_files() -> List[str]:
    cmd: str = "git status"
    output: str = fixed_path_shell(cmd)

    lines: List[str] = output.split("\n")
    files: List[str] = []
    pattern: str = "(\tmodified:|\tnew file:|\tdeleted:)"
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
            renamed_from, renamed_to = file_names.split(" -> ")
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
        stamp_text = "\n".join(diffs[file_name])
        if separator:
            stamp_text = f"{separator}\n{stamp_text}"

    return stamp_text


def combine_stamp(enable_time_stamp: bool = True, separator: str = "=" * 8) -> Stamps:
    stamps = {}
    file_names = changed_files()
    diffs: Diffs = git_diff()

    
    for file_name in file_names:
        time_stamp = ""
        diff_stamp = ""
        if enable_time_stamp:
            if separator:
                time_stamp: str = f"{separator}\n{make_time_stamp()}\n"
            else:
                time_stamp: str = f"{make_time_stamp()}\n"

        if is_active_file(file_name):
            diff_stamp: str = make_diff_stamp(file_name, diffs, separator=separator) + "\n"

        if diff_stamp:
            stamp: str = f"{time_stamp}{diff_stamp}"
            stamps[file_name] = stamp

    return stamps


def save_history() -> None:
    config: Config = load_config()
    uuid: str = config["uuid"]
    root_path: str = config["root_path"]
    hist_dir: str = history_dir(config)
    stamps: Stamps = combine_stamp()
    for file_name, stamp in stamps.items():
        file_name = re.sub(f"docs/{uuid}/", "", file_name)
        file_name = re.sub("\..*", "", file_name)
        save_path = f"{hist_dir}/{file_name}.txt"
        with open(save_path, "a") as f:
            f.write(stamp)