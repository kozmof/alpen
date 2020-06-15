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


def git_diff() -> Diffs:
    """Normalize default diff of git

    Exapmple:
        -foo
        \ No newline at end of file
        +bar
        +baz
        +foo
        +foo
        +quux
        \ No newline at end of file

        =>

        +bar
        +baz
        foo
        +foo
        +quux

    Returns:
        Diffs: Diff of specific files
    """
    cmd1: str = "git diff --histogram"
    output: str = fpshell(cmd1)

    lines: List[str] = output.split("\n")
    separate_pattern: str = "diff --git "
    group: Diffs = {}
    gpath = ""
    _lines = []
    modify_lines = []

    continue_again = False
    skip_append  = False
    is_modified = False
    current_j = 0
    current_k = 0

    #---------------------------------------------------------------
    # extract pairs
    remove_lines1 = [
        line for line in 
            [
                f"+{line[1:]}"
                for line in lines
                if len(line) > 0 and line[0] == "-" 
            ]
        if line in lines
        ]
    remove_lines2 = [f"-{line[1:]}" for line in lines if line in remove_lines1]
    remove_lines1 = [f"+{line[1:]}" for line in remove_lines2]
    assert len(remove_lines1) == len(remove_lines2)

    #---------------------------------------------------------------
    # parse and modify then extract
    for i, line in enumerate(lines):
        if continue_again:
            continue_again = False
            continue

        if modify_lines and current_j < len(modify_lines):
            for j, modify_line in enumerate(modify_lines[current_j:]):
                if modify_line == line:
                    line = line[1:]
                    current_j = j + 1
                    _lines.append(line)
                    is_modified = True
                    break
            if is_modified:
                is_modified = False
                continue

        if len(lines) > i + 1 and current_k < len(remove_lines1):
            for k, remove_line2 in enumerate(remove_lines2[current_k:]):
                if line == remove_line2:
                    skip_append = True
                    for remove_line1 in remove_lines1[current_k:]:
                        if line[i + 1] == remove_line1:
                            continue_again = True
                            current_k = k + 1
                        else:
                            modify_lines.append(remove_line1)
                            current_k = k + 1
                        break
                    break

        if not skip_append:
            _lines.append(line)
        else:
            skip_append = False
    lines = _lines

    #---------------------------------------------------------------
    # match and extract
    for i, line in enumerate(lines):
        if re.match(separate_pattern, line):
            gpath: str = re.sub("a/", "", re.sub(separate_pattern, "", line).split(" ")[0])
            group[gpath] = []

        if gpath in group and i > 1:
            if len(line) >= 2 and line[:2] == "@@":
                continue
            elif len(line) >= 3 and (line[:3] == "+++" or line[:3] == "---"):
                continue
            elif line == r"\ No newline at end of file":
                continue
            group[gpath].append(line)

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


def make_diff_stamp(gpath: str, diffs: Diffs, separator: str = "") -> str:
    stamp_text: str = ""
    if gpath in diffs:
        stamp_text = "\n".join(diffs[gpath])
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