import re
import os
import json
from lib.commands.core.git import changed_file_gpaths, untracked_file_gpaths, make_stamp
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.shell import fpshell

yes_command = ["Y", "YES"]


def c_save_history(commit=True, debug=True):
    gpaths = changed_file_gpaths()
    ut_gpaths = untracked_file_gpaths()
    stamp = make_stamp()
    config: Config = load_config()
    uuid = config["uuid"]
    commit_header = config["commit_header"]

    doc_uuid = fr".docs/{uuid}"

    doc_gpaths = [gpath for gpath in gpaths if re.match(doc_uuid, gpath)]
    ut_gpaths = [ut_gpath for ut_gpath in ut_gpaths if re.match(doc_uuid, ut_gpath)]

    for gpath in doc_gpaths + ut_gpaths:
        print(f"Save change history of {gpath}? [y/N]")
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
                if save_path_body and commit:
                    save_path = f"{save_path_body}-{save_path_file_type}.json"
                    if os.path.isfile(save_path):
                        with open(save_path, "r") as f:
                            history_data = json.load(f)
                        with open(save_path, "w") as f:
                            diff_log = stamp.get(gpath)
                            if diff_log:
                                history_data.append(diff_log)
                                json.dump(history_data, f)
                    else:
                        with open(save_path, "w") as f:
                            diff_log = stamp.get(gpath)
                            if diff_log:
                                json.dump([diff_log], f)

                stage_and_commit_command = f"git add {gpath} && git commit -m '{commit_header} {user_message}'"
                if debug:
                    print(stage_and_commit_command)
                if commit:
                    fpshell(stage_and_commit_command)