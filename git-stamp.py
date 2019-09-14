import re
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, NewType
from configure import load_config, Config
from pprint import pprint
Datetime = NewType("Datetime", datetime)
Diffs = NewType("Diffs", Dict[str, List[str]])


def git_diff() -> Diffs:
    cmd: str = "git diff --staged --histogram"
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    lines: List[str] = output.split("\n")
    separate_pattern: str = "diff --git "
    group: Diffs = {}

    for line in lines:
        if re.match(separate_pattern, line):
            file_name: str = re.sub("a/", "", re.sub(separate_pattern, "", line).split(" ")[0])
            group[file_name] = []

        group[file_name].append(line)

    return group


def changed_files() -> List[str]:
    cmd: str = "git status"
    output: str = subprocess.check_output(cmd, shell=True).decode("utf-8")
    lines: List[str] = output.split("\n")
    files: List[str] = []
    pattern: str = "(\tmodified:|\tnew file:)"
    break_pattern: str = "Changes not staged for commit:"

    for line in lines:
        if re.match(break_pattern, line):
            break
        elif re.match(pattern, line):
            file_name: str = re.sub(pattern, "", line).strip()
            if file_name not in files:
                files.append(file_name)

    return files


def fullpath(files: List[str]) -> List[str]:
    config: Config = load_config()
    root_path: str = config["root_path"]
    return ["{}/{}".format(root_path, file_name) for file_name in files]


def time_stamp() -> str:
    now: Datetime = datetime.now()
    time: str = str(now.replace(microsecond=0))
    tzname: str = str(now.astimezone().tzname())
    return time + " " + tzname


def make_stamp(file_name: str, diffs: Diffs, separator: str = "=" * 8) -> str:
    stamp_text: str = "{}\n{}".format(time_stamp(), "\n".join(diffs[file_name]))
    if separator:
        stamp_text: str = "{}\n{}".format(separator, stamp_text)
    return stamp_text


if __name__ == "__main__":
    pprint(git_diff())
    print(make_stamp("test/test2.txt", git_diff()))