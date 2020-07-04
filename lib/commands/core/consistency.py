"""Consistency Utilities
"""
import os
import re
from typing import Set, List
from lib.commands.core.configure import load_config
from lib.commands.core.custom_types import Config
from lib.commands.core.dir_ops import get_dir_path


def doc_file_exists(file_name: str, config: Config) -> bool:
    """Check whether a document exists or not

    Args:
        file_name (str): A file name to be checked
        config (Config): Config data

    Returns:
        bool: True if a document exists
    """
    doc_dir = get_dir_path("DOCUMENT", config)
    doc_path = f"{doc_dir}/{file_name}"
    if os.path.isfile(doc_path):
        return True
    else:
        return False