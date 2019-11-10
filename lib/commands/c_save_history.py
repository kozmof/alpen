import re
import os
from .core.git_stamp import changed_files, untracked_files, combine_stamp
from .core.custom_types import Config
from .core.configure import load_config
from .core.consistency import check_history_consistecy
from .core.shell import fixed_path_shell

yes_command = ["Y", "YES"]


def c_save_history(debug=True):
    files = changed_files()
    ut_files = untracked_files()
    stamp = combine_stamp()
    config: Config = load_config()
    uuid = config["uuid"]
    commit_header = config["commit_header"]

    doc_pattern = f"\.docs/{uuid}"
    history_pattern = f"\.histories/{uuid}"

    doc_files = [file for file in files if re.match(doc_pattern, file)]
    ut_doc_files = [file for file in ut_files if re.match(doc_pattern, file)]

    history_commited_files = []
    check_result = check_history_consistecy()

    if not check_result:
        print("Are you sure to continue?")
        user_input = input()
        if user_input.upper() not in yes_command:
            return

    for file_name in doc_files + ut_doc_files:
        if not re.match(f"{doc_pattern}\/todo\/", file_name):
            print(f"Save change history of {file_name}?")
            yes_or_no = input()
            if yes_or_no.upper() in yes_command:
                if re.match(f"{doc_pattern}\/", file_name):
                    print("Put a commit message")
                    user_message = input()
                    history_path = re.sub("\.docs", ".histories", file_name)
                    root_path = config["root_path"]
                    save_path_body = os.path.splitext(f"{root_path}/{history_path}")[0]
                    save_path = f"{save_path_body}.md"
                    with open(save_path, "a") as f:
                        f.write(stamp[file_name])

                    stage_and_commit_command = f"git add {file_name} && git commit -m '{commit_header} {user_message}'"
                    if debug:
                        print(stage_and_commit_command)
                    fixed_path_shell(stage_and_commit_command)

                    history_commited_files.append(history_path)

    history_files = [file for file in files if re.match(history_pattern, file)]
    ut_history_files = [file for file in ut_files if re.match(history_pattern, file)]

    for file_name in history_files + ut_history_files:
        if file_name in history_commited_files:
            stage_and_commit_command = f"git add {file_name} && git commit -m '[DSK-history-auto-save] {file_name}'"
            if debug:
                print(stage_and_commit_command)
            fixed_path_shell(stage_and_commit_command)

    