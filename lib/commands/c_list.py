import os
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path


def c_list():
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    for file_name in sorted(os.listdir(doc_dir)):
        print(file_name)