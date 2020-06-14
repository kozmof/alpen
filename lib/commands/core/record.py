import os
from typing import Optional, List
from datetime import datetime 
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path


def record_edited_file(file_name):
    config: Config = load_config()
    root_path: str = config["root_path"]
    with open(f"{root_path}/.edited_file_record", "a") as f:
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{file_name} {time_stamp}\n")


def read_edited_file_record(active_sign="A", not_active_sign="N") -> Optional[str]:
    config: Config = load_config()
    root_path: str = config["root_path"]
    record_path = f"{root_path}/.edited_file_record"
    if os.path.isfile(record_path):
        with open(record_path) as f:
            result = ""
            records: List[str] = f.readlines()
            for record in reversed(records):
                file_name = "".join(record.split(" ")[:-2])
                full_path = f"{get_dir_path('DOCUMENT', config)}/{file_name}"
                if os.path.isfile(full_path):
                    result += f"[{active_sign}] {record}"
                else:
                    result += f"[{not_active_sign}] {record}"

            return result