import re
import os
from .core.configure import load_config
from .core.dir_ops import get_dir_path
from .core.shell import fixed_path_shell
from .core.custom_types import Config


def c_rename(arg):
    result_1 = list(re.findall("\'", arg))
    result_2 = list(re.findall('\"', arg))

    if len(result_1) == 4:
        result = result_1
    elif len(result_2) == 4:
        result = result_2
    else:
        result = None

    if not result:
        names = arg.split(" ")

    if not result and len(names) != 2:
        print("Invalid syntax. rename <rename_from> <rename_to>")
        return 
    else:
        config: Config = load_config()
        uuid = config["uuid"]
        if len(names) == 2:
            original_name = names[0]
            new_name = names[1]
        elif result:
            original_name = arg[result[0].end():result[1].start()]
            new_name = arg[result[2].end():result[3].start()]
        else:
            raise Exception("logical error")

        if re.match("todo\/", original_name):
            print("Move to a todo directory is not allowed.")
            return 

        doc_dir = get_dir_path("DOCUMENT", config)
        original_path = f"{doc_dir}/{original_name}"
        new_path = f"{doc_dir}/{new_name}"

        hist_dir = get_dir_path("HISTORY", config)
        original_hist_path = f"{hist_dir}/{original_name}"
        new_hist_path = f"{hist_dir}/{new_name}"

        if os.path.isfile(original_path):
            if os.path.isfile(new_path):
                print(f"{new_name} is already existing. Choose another name")
                return 
            else:
                doc_mv_command = f"mv {original_path} {new_path}"
                fixed_path_shell(file_mv_command)
                doc_rm_command = f"git rm .docs/{uuid}/{original_name}"
                fixed_path_shell(doc_rm_command)
                if os.path.isfile(original_hist_path):
                    hist_mv_command = f"mv {original_hist_path} {new_hist_path}"
                    fixed_path_shell(command)
                    hist_rm_command = f"git rm .histories/{uuid}/{original_name}"
                    fixed_path_shell(hist_rm_command)
                else:
                    print(f"History file not found: {original_hist_path}")
                    return
        else:
            print(f"No such a file: {original_name}")
            return