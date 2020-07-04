"""Domain Utilities
"""
import os
import json
from pprint import pprint
from typing import Optional, List
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.metadata import (
    manipulate_metadata,
    f2d
    )
from lib.commands.core.custom_types import Config

DOMAIN_FILE = "domains.json"


def load_domain_data(config: Config):
    """Load all domain data

    Structure:
        domain_data:
            {
                [domain_name: str]:  List # file names
            }

    Args:
        config (Config): Config data

    Returns:
        Dict: Domain data
    """
    domain_dir = get_dir_path("DOMAIN", config)
    domain_file_path = f"{domain_dir}/{DOMAIN_FILE}"

    if os.path.isfile(domain_file_path):
        with open(domain_file_path, "r") as f:
            domain_data = json.load(f)
            return domain_data


def dump_domain_json(domain_data, config: Config):
    """Dump domain data

    Args:
        domain_data (Dict): Domain data
        config (Config): Config data
    """
    domain_dir = get_dir_path("DOMAIN", config)
    domain_file_path = f"{domain_dir}/{DOMAIN_FILE}"

    if not os.path.isdir(domain_dir):
        os.makedirs(domain_dir)

    with open(domain_file_path, "w") as f:
        json.dump(domain_data, f, indent=4, sort_keys=True)


def manipulate_domain_data(action_type: str, config: Config,
                       file_name: Optional[str] = None, new_file_name: Optional[str] = None,
                       domain_name: Optional[str] = None, new_domain_name: Optional[str] = None):
    """Update domain file

        - ADD_DOMAIN: Add a new domain
        - REMOVE_DOMAIN: Remove a domain
        - RENAME_DOMAIN: Rename a domain
        - SEARCH_DOMAIN: Search a domain and print linked files
        - SHOW_ALL: Print all domain data
        - RENAME_FILE: Rename a file which links to domains

    Arg Patterns:
        - ADD_DOMAIN:      file_name, domain_name
        - REMOVE_DOMAIN:   file_name, domain_name
        - RENAME_DOMAIN:   domain_name, new_domain_name
        - SEARCH_DOMAIN:   domain_name
        - SHOW_ALL:     none
        - RENAME_FILE:  file_name, new_file_name

    Args:
        action_type (str):                          ADD_DOMAIN, REMOVE_DOMAIN, RENAME_DOMAIN, SEARCH_DOMAIN, SHOW_ALL, RENAME_FILE
        config (Config):                            Config file
        file_name (Optional[str], optional):        Use in ADD_DOMAIN, REMOVE_DOMAIN, RENAME_DOMAIN, RENAME_FILE. Defaults to None.
        new_file_name (Optional[str], optional):    Use in RENAME_FILE. Defaults to None.
        domain_name (Optional[str], optional):         Use in ADD_DOMAIN, REMOVE_DOMAIN, SEARCH_DOMAIN.  Defaults to None.
        new_domain_name (Optional[str], optional):     Use in RENAME_DOMAIN. Defaults to None.
    """
    # -------------------------------------------------------
    # ADD_DOMAIN 
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
    # -------------------------------------------------------
    # REMOVE_DOMAIN
    elif action_type == "REMOVE_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            if file_name in domain_data[domain_name]:
                domain_data[domain_name].remove(file_name)
                if not domain_data[domain_name]:
                    del domain_data[domain_name]
                dump_domain_json(domain_data, config)
    # -------------------------------------------------------
    # RENAME_DOMAIN
    elif action_type == "RENAME_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            domain_data[new_domain_name] = domain_data[domain_name]
            del domain_data[domain_name]
            dump_domain_json(domain_data, config)
    # -------------------------------------------------------
    # SEARCH_DOMAIN
    elif action_type == "SEARCH_DOMAIN":
        domain_data = load_domain_data(config)
        if domain_data and domain_name in domain_data:
            pprint(domain_data[domain_name])
    # -------------------------------------------------------
    # SHOW_ALL
    elif action_type == "SHOW_ALL":
        domain_data = load_domain_data(config)
        pprint(domain_data)
    # -------------------------------------------------------
    # RENAME_FILE
    elif action_type == "RENAME_FILE":
        domain_names = f2d(file_name, config)
        domain_data = load_domain_data(config)
        if domain_names and domain_data:
            for domain_name in domain_names:
                domain_data[domain_name].remove(file_name)
                domain_data[domain_name].append(new_file_name)

            dump_domain_json(domain_data, config)
    # -------------------------------------------------------
    else:
        raise Exception(f"No such action type: {action_type}")