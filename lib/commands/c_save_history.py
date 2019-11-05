import re
from .core.git_stamp import changed_files, combine_stamp
from .core.custom_types import Config
from .core.configure import load_config


# TODO if untracked files exist, ask whether add or not
def c_save_history():
    files = changed_files()
    stamp = combine_stamp()
    config: Config = load_config()

    doc_pattern = "docs/{uuid}".format(uuid=config["uuid"])
    doc_files = [file for file in files if re.match(doc_pattern, file)]
    for file_name in doc_files:
        history_path = re.sub("docs", "histories", file_name)
        root_path = config["root_path"]
        save_path = f"{root_path}/{history_path}"
        with open(save_path, "a") as f:
            f.write(stamp[file_name])
    