import re
import os
from .core.configure import load_config
from .core.dir_ops import get_dir_path
from .core.shell import fixed_path_shell
from .core.custom_types import Config
from .core.rename import arg_to_names


def c_rename(arg):
    original_name, new_name = arg_to_names(arg)
    if original_name and new_name:
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