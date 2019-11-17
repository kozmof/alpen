import os
import re
from .configure import load_config
from .custom_types import Config
from .dir_ops import get_dir_path


def check_history_consistecy() -> bool:
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    hist_dir = get_dir_path("HISTORY", config)
    doc_file_bodies: Set =  {os.path.splitext(file)[0] for file in os.listdir(doc_dir) if os.path.isfile(os.path.join(doc_dir, file)) and not re.match("\.", file)}
    hist_file_bodies: Set =  {os.path.splitext(file)[0] for file in os.listdir(hist_dir) if os.path.isfile(os.path.join(hist_dir, file)) and not re.match("\.", file)}
    rest_hists = [f"{file_body}.md" for file_body in hist_file_bodies - doc_file_bodies]
    if rest_hists:
        print("These history files don't have main files")
        for history_file in rest_hists:
            print(history_file)
        return False
    else:
        return True

