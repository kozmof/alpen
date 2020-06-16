"""Git operations
"""
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
    r"""Modify default diff of Git

    Example:
        (1)
            -foo
            \ No newline at end of file
            +bar
            +baz
            +foo
            +foo
            +quux
            \ No newline at end of file

            ==>

            +bar
            +baz
             foo
            +foo
            +quux

        (2)
            -foo
            +foo
            +bar

            ==>

             foo
            +bar

    Returns:
        Diffs: Diff of specific files
    """
    cmd1: str = "git diff --histogram"
    output: str = fpshell(cmd1)

    separate_pattern: str = "diff --git "
    lines: List[str] = output.split("\n")

    _lines = []
    _chunk = []
    lchunk = []
    _lchunk = []
    modify_lines = []

    group: Diffs = {}
    gpath = ""

    skip_append  = False
    is_modified = False
    current_j = 0
    current_k = 0

    for line in lines:
        if len(line) > 10 and line[:11]:
            if separate_pattern == line[:11]:
                if _chunk:
                    lchunk.append(_chunk)
                _chunk = []
        _chunk.append(line)
    if _chunk:
        lchunk.append(_chunk)

    #-------------------------------------------------------------------
    # Process per a file then gather them
    for lines in lchunk:
        #---------------------------------------------------------------
        # extract pairs

        # A plus list which is actual minus len
        remove_lines1 = [
            line for line in 
                [
                    f"+{line[1:]}"
                    for line in lines
                    if len(line) > 0 and line[0] == "-" 
                ]
            if line in lines
            ]
        # A minus list which is actual plus len
        remove_lines2 = [f"-{line[1:]}" for line in lines if line in remove_lines1]

        # Align actual shorter len
        # No need to adjust a len
        if (len2 := len(remove_lines2)) == (len1 := len(remove_lines1)):
            pass
        # The case of actural plus len is lognger than actual minus len
        # Adjust minus list which is actual plus len to the actual minus len
        elif len2 > len1:
            remove_lines2 = [f"-{line[1:]}" for line in remove_lines1]
        # The case of actural minus len is lognger than actual plus len
        # Adjust plus list which is actual muinus len to the actual plus len
        else:
            remove_lines1 = [f"+{line[1:]}" for line in remove_lines2]

        assert len(remove_lines1) == len(remove_lines2)

        #---------------------------------------------------------------
        # parse and modify then extract
        for i, line in enumerate(lines):
            if modify_lines and current_j < len(modify_lines):
                for j, modify_line in enumerate(modify_lines[current_j:]):
                    if modify_line == line:
                        line = f" {line[1:]}"
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
                        remove_line1 = remove_lines1[current_k]
                        current_k = k + 1
                        modify_lines.append(remove_line1)
                    break

            if not skip_append:
                _lines.append(line)
            else:
                skip_append = False
        _lchunk.append(_lines)
        _lines = []

    #---------------------------------------------------------------
    # Gather them
    lines = [line for _lines in _lchunk for line in _lines]

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
    """Get git-style paths of untracked file

    Returns:
        List[str]: git-style paths of untracked files
    """
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
    """Get git-style paths of changed files

    Returns:
        List[str]: git-style paths of changed files
    """
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


def make_time_stamp() -> str:
    """Make a timestamp with timezone of a computer
    Example:
        2020-05-12 21:44:01 GMT

    Returns:
        str: Timestamp
    """
    now: Datetime = datetime.now()
    time: str = str(now.replace(microsecond=0))
    tzname: str = str(now.astimezone().tzname())
    return time + " " + tzname


def make_diff_stamp(gpath: str, diffs: Diffs) -> str:
    """Make a diff of a file

    Args:
        gpath (str): Git-style path
        diffs (Diffs): Diffs

    Returns:
        str: Diff of a file
    """
    stamp_text: str = ""
    if gpath in diffs:
        stamp_text = "\n".join(diffs[gpath])

    return stamp_text


def make_stamp() -> Stamps:
    """Combine stamps
    Structure:
        stamps:
            {
                [gpath: str]: {
                    "timestamp": str,
                    "diff": str
                }
            }

    Returns:
        Stamps: Stamp of files
    """
    stamps = {}
    gpaths = changed_file_gpaths()
    diffs: Diffs = git_diff()

    for gpath in gpaths:
        stamps[gpath] = {}
        stamps[gpath]["timestamp"] = f"{make_time_stamp()}\n"
        stamps[gpath]["diff"] = make_diff_stamp(gpath, diffs)

    return stamps


def has_branch(branch_name: str) -> bool:
    """Check an existence of a branch

    Args:
        branch_name (str): Branch name

    Returns:
        bool: True if branch exists
    """
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
    """Make an user specific branch
    """
    config: Config = load_config()
    uuid = config["uuid"]

    if not has_branch(uuid):
        cmd = f"git branch {uuid}"
        fpshell(cmd)