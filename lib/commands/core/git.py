import os
import re
import json
from pprint import pprint
from typing import List, Dict
from datetime import datetime, timezone
from lib.commands.core.shell import fpshell
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config
from lib.commands.core.custom_types import Datetime, Diffs, Stamps
from lib.commands.core.dir_ops import get_dir_path


ROOT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, *([".."] * 3))))
USER_UUID_PATH: str = ROOT_DIR + "/" + "user-uuid.json"


def load_user_uuid(): 
    uupath = USER_UUID_PATH
    if os.path.isfile(uupath):
        with open(uupath, "r") as f:
            return json.load(f)
    else:
        return {}


def dump_user_uuid(user_uuid):
    uupath = USER_UUID_PATH
    with open(uupath, "w") as f:
        json.dump(user_uuid, f)


def git_diff() -> Diffs:
    cmd1: str = "git diff --histogram"
    output: str = fpshell(cmd1)

    lines: List[str] = output.split("\n")
    separate_pattern: str = "diff --git "
    group: Diffs = {}
    file_name = ""
    for i, line in enumerate(lines):
        if re.match(separate_pattern, line):
            file_name: str = re.sub("a/", "", re.sub(separate_pattern, "", line).split(" ")[0])
            group[file_name] = []

        if file_name in group and i > 1:
            if len(line) >= 2 and line[:2] == "@@":
                continue
            elif len(line) >= 3 and (line[:3] == "+++" or line[:3] == "---"):
                continue
            group[file_name].append(line)

    return group


def untracked_file_gpaths() -> List[str]:
    cmd: str = "git status"
    output: str = fpshell(cmd)
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
    output: str = fpshell(cmd)

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


def has_branch(branch_name) -> bool:
    cmd = f"git show-branch --list"
    res = fpshell(cmd)
    branch_ls_raw = res.split("\n")
    recom = re.compile(r"\[.+\]")
    branch_ls = []
    for branch in branch_ls_raw:
        sobj = recom.search(branch)
        if sobj:
            branch_ls.append(branch[sobj.start() + 1:sobj.end() - 1])
    if branch_name in branch_ls:
        return True
    else:
        return False


def make_my_branch() -> None:
    config: Config = load_config()
    uuid = config["uuid"]
    if not has_branch(uuid):
        cmd = f"git branch {uuid}"
        fpshell(cmd)