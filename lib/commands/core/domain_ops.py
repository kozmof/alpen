from lib.commands.core.configure import load_config
from lib.commands.core.domain import update_domain_file
from lib.commands.core.metadata import update_metadata_file
from lib.commands.core.consistency import doc_file_exists
from lib.commands.core.custom_types import Config


def add_domain(file_name, domain_name):
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        update_domain_file("ADD_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        update_metadata_file("ADD_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        print(f"{domain_name} added to {file_name}")


def remove_domain(file_name, domain_name):
    config: Config = load_config()
    if not doc_file_exists(file_name, config):
        print(f"{file_name} does not exist.")
        return
    else:
        update_domain_file("REMOVE_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        update_metadata_file("REMOVE_DOMAIN", config, file_name=file_name, domain_name=domain_name)
        print(f"{domain_name} removed from {file_name}")


def rename_domain(domain_name, new_domain_name):
    config: Config = load_config()
    update_domain_file("RENAME_DOMAIN", config, domain_name=domain_name, new_domain_name=new_domain_name)
    update_metadata_file("RENAME_DOMAIN", config, domain_name=domain_name, new_domain_name=new_domain_name)
    print(f"{domain_name} renamed to {new_domain_name}")


def search_domain(domain_name):
    config: Config = load_config()
    update_domain_file("SEARCH_DOMAIN", config, domain_name=domain_name)


def show_all():
    config: Config = load_config()
    update_domain_file("SHOW_ALL", config)

    