import os
import re
from .core.configure import load_config
from .core.dir_ops import document_dir, history_dir
from .core.custom_types import Config
from typing import Set

def c_recover_history():
    config: Config = load_config()
    doc_dir = document_dir(config)
    hist_dir = history_dir(config)
    doc_file_bodies: Set =  {os.path.splitext(f)[0] for f in os.listdir(doc_dir) if os.path.isfile(os.path.join(doc_dir, f)) and not re.match("\.", f)}
    hist_file_bodies: Set =  {os.path.splitext(f)[0] for f in os.listdir(hist_dir) if os.path.isfile(os.path.join(hist_dir, f)) and not re.match("\.", f)}
    hist_rests: Set = hist_file_bodies - doc_file_bodies
    if hist_rests:
        print("Choose a number to recover")
        for num, rest in enumerate(hist_rests):
            print(num, rest)
    else:
        print("There are no files to recover.")