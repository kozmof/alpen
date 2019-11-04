import re
from .core.git_stamp import changed_files
from .core.custom_types import Config
from .core.configure import load_config


def c_save_history():
    files = changed_files()
    config: Config = load_config()
    doc_pattern = "docs/{uuid}".format(uuid=config["uuid"])
    doc_files = [file for file in files if re.match(doc_pattern, file)]
    # TODO git command