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


def doc_file_exists(file_name, config):
    doc_dir = get_dir_path("DOCUMENT", config)
    doc_path = f"{doc_dir}/{file_name}"
    if os.path.isfile(doc_path):
        return True
    else:
        return False


def is_active_file(file_name: str) -> bool:
    config: Config = load_config()
    stops: List[str] = config["stops"]
    masks: List[str] = config["masks"]
    targets: List[str] = config["targets"]

    if file_name in stops:
        return False
    elif file_name in targets:
        return True
    else:
        for mask in masks:
            if re.match(f".*\.{mask}$", file_name):
                return True
        return False