import os
from .core.custom_types import Config
from .core.configure import load_config
from .core.dir_ops import get_dir_path


def c_list():
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    for file_name in sorted(os.listdir(doc_dir)):
        print(file_name)