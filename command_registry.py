import re
from typing import List
from custom_types import Config
from configure import load_config
from doc_ops import document_dir

def register_edit_command(editor: str, user_input: str) -> List[str]:
    config: Config = load_config()
    elements = list(filter(lambda x:x, user_input.split(" ")))
    doc_dir = document_dir(config)
    command = [editor] + list(map(lambda x: doc_dir + "/" + x if not re.match("\+|\-", x) else x, elements))
    return command