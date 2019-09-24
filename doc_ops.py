import os
from configure import load_config, Config


def document_dir() -> str:
    config: Config = load_config()
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    doc_dir = f"{root_path}/docs/{uuid}"
    return doc_dir


def make_doc_directory() -> None:
    doc_dir = document_dir()
    if not os.path.isdir(doc_dir):
        os.makedirs(doc_dir)


def history_dir() -> str:
    config: Config = load_config()
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    history_dir = f"{root_path}/histories/{uuid}"
    return history_dir


def make_history_directory() -> None:
    hist_dir = history_dir()
    if not os.path.isdir(hist_dir):
        os.makedirs(hist_dir)

