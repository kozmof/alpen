import os
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.build import make_build_config_file


def c_build():
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    make_build_config_file(os.listdir(doc_dir))