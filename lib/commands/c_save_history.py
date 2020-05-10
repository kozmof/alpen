import re
import os
from lib.commands.core.git import changed_file_gpaths, untraced_file_gpaths, combine_stamp
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.shell import fixed_path_shell

yes_command = ["Y", "YES"]


def c_save_history(debug=True):
    gpaths = changed_file_gpaths()
    ut_gpaths = untraced_file_gpaths()
    stamp = combine_stamp()
    config: Config = load_config()
    uuid = config["uuid"]
    commit_header = config["commit_header"]

    doc_uuid = fr".docs/{uuid}"
    history_uuid = fr".histories/{uuid}"

    doc_gpaths = [gpath for gpath in gpaths if re.match(doc_uuid, gpath)]
    ut_gpaths = [ut_gpath for ut_gpath in ut_gpaths if re.match(doc_uuid, gpath)]

    history_commited_files = []

    for gpath in doc_gpaths + ut_gpaths:
        print(f"Save change history of {gpath}?")
        yes_or_no = input()
        if yes_or_no.upper() in yes_command:
            if re.match(fr"{doc_uuid}/", gpath):
                print("Put a commit message")
                user_message = input()
                history_gpath = re.sub(r".docs", ".histories", gpath)
                root_path = config["root_path"]
                save_path_body, save_path_file_type = os.path.splitext(
                    f"{root_path}/{history_gpath}"
                    )
                save_path = f"{save_path_body-save_path_file_type}.md"
                with open(save_path, "a") as f:
                    f.write(stamp[gpath])

                stage_and_commit_command = f"git add {gpath} && git commit -m '{commit_header} {user_message}'"
                if debug:
                    print(stage_and_commit_command)
                fixed_path_shell(stage_and_commit_command)

                history_commited_files.append(history_gpath)

    history_files = [gpath for gpath in gpaths if re.match(history_uuid, gpath)]
    ut_history_files = [gpath for gpath in ut_gpaths if re.match(history_uuid, gpath)]

    for gpath in history_files + ut_history_files:
        if gpath in history_commited_files:
            stage_and_commit_command = f"git add {gpath} && git commit -m '[Alpen-history-auto-save] {gpath}'"
            if debug:
                print(stage_and_commit_command)
            fixed_path_shell(stage_and_commit_command)