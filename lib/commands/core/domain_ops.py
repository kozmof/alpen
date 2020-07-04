"""Domain Operations
"""
from lib.commands.core.configure import load_config
from lib.commands.core.domain import manipulate_domain_data
from lib.commands.core.metadata import manipulate_metadata
from lib.commands.core.consistency import doc_file_exists
from lib.commands.core.custom_types import Config


def add_domain(file_name: str, domain_name: str) -> None:
    """Add a domain

    Args:
        file_name (str): A file name to add a domain
        domain_name (str): A domain name
    """
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        manipulate_domain_data("ADD_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        manipulate_metadata("ADD_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        print(f"{domain_name} added to {file_name}")


def remove_domain(file_name: str, domain_name: str) -> None:
    """Remove a domain

    Args:
        file_name (str): A file to remove a domain
        domain_name (str): A domain name
    """
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        manipulate_domain_data("REMOVE_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        manipulate_metadata("REMOVE_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        print(f"{domain_name} removed from {file_name}")


def rename_domain(domain_name: str, new_domain_name: str) -> None:
    """Rename a domain

    Args:
        domain_name (str): A domain name to be renamed
        new_domain_name (str): A new domain name
    """
    config: Config = load_config()
    manipulate_domain_data("RENAME_DOMAIN", config, domain_name=domain_name, new_domain_name=new_domain_name)
    manipulate_metadata("RENAME_DOMAIN", config, domain_name=domain_name, new_domain_name=new_domain_name)
    print(f"{domain_name} renamed to {new_domain_name}")


def search_domain(domain_name: str):
    """Search a domain name and print related file names

    Args:
        domain_name (str): A domain to search
    """
    config: Config = load_config()
    manipulate_domain_data("SEARCH_DOMAIN", config, domain_name=domain_name)


def show_all():
    """Show all domain data
    """
    config: Config = load_config()
    manipulate_domain_data("SHOW_ALL", config)