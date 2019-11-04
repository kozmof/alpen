import os
from .core.custom_types import Config
from .core.configure import load_config
from .core.dir_ops import document_dir


def c_list():
    config: Config = load_config()
    doc_dir = document_dir(config)
    for file_name in sorted(os.listdir(doc_dir)):
        print(file_name)