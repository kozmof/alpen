import os
import json
from pprint import pprint
from typing import Optional, List
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.metadata import (update_metadata_file,
                      f2t)
from lib.commands.core.custom_types import Config

DOMAIN_FILE = "domains.json"


def load_domain_data(config: Config):
    domain_dir = get_dir_path("DOMAIN", config)
    domain_file_path = f"{domain_dir}/{DOMAIN_FILE}"

    if os.path.isfile(domain_file_path):
        with open(domain_file_path, "r") as fpt:
            domain_data = json.load(fpt)
            return domain_data


def dump_domain_json(domain_data, config: Config):
    domain_dir = get_dir_path("DOMAIN", config)
    domain_file_path = f"{domain_dir}/{DOMAIN_FILE}"

    if not os.path.isdir(domain_dir):
        os.makedirs(domain_dir)

    with open(domain_file_path, "w") as fpt:
        json.dump(domain_data, fpt, indent=4, sort_keys=True)


def update_domain_file(action_type: str, config: Config,
                       file_name: Optional[str] = None, new_file_name: Optional[str] = None,
                       domain_name: Optional[str] = None, new_domain_name: Optional[str] = None):

    if action_type == "ADD_DOMAIN":
        domain_data = load_domain_data(config)

        if domain_data:
            if domain_name in domain_data:
                if file_name not in domain_data[domain_name]:
                    domain_data[domain_name].append(file_name)
            else:
                domain_data[domain_name] = [file_name]

        else:
            domain_data = {}
            domain_data[domain_name] = [file_name]

        dump_domain_json(domain_data, config)

    elif action_type == "REMOVE_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            if file_name in domain_data[domain_name]:
                domain_data[domain_name].remove(file_name)
                if not domain_data[domain_name]:
                    del domain_data[domain_name]
                dump_domain_json(domain_data, config)

    elif action_type == "RENAME_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            domain_data[new_domain_name] = domain_data[domain_name]
            del domain_data[domain_name]
            dump_domain_json(domain_data, config)

    elif action_type == "SEARCH_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            pprint(domain_data[domain_name])

    elif action_type == "SHOW_ALL":
        domain_data = load_domain_data(config)
        pprint(domain_data)

    elif action_type == "RENAME_FILE":
        domain_names = f2t(file_name, config)
        domain_data = load_domain_data(config)
        if domain_names and domain_data:
            for domain_name in domain_names:
                domain_data[domain_name].remove(file_name)
                domain_data[domain_name].append(new_file_name)

            dump_domain_json(domain_data, config)
    else:
        raise Exception("No such action type: {action_type}")