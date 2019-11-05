import os
from .custom_types import Config


def document_dir(config: Config) -> str:
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    doc_dir = f"{root_path}/.docs/{uuid}"
    return doc_dir


def make_doc_directory(config: Config) -> None:
    doc_dir = document_dir(config)
    if not os.path.isdir(doc_dir):
        os.makedirs(doc_dir)


def history_dir(config: Config) -> str:
    root_path: str = config["root_path"]
    uuid: str = config["uuid"]
    history_dir = f"{root_path}/.histories/{uuid}"
    return history_dir


def make_history_directory(config: Config) -> None:
    hist_dir = history_dir(config)
    if not os.path.isdir(hist_dir):
        os.makedirs(hist_dir)