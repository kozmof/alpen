import re
from typing import List, Dict

def register_command(editor: str, user_input: str) -> List[str]:
  elements = list(filter(lambda x:x, user_input.split(" ")))
  return [editor] + elements