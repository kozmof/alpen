"""Command for domain operations
"""
from lib.commands.core.domain_ops import (
    add_domain,
    remove_domain,
    rename_domain,
    search_domain,
    show_all
    )

def c_domain(arg: str) -> None:
    """Command for domain oprerations

    Ops:
        - add: Add a domain to a file
        - remove Remove a domain to a file
        - rename Rename a domain
        - search Search a domain

    Args:
        arg (str): Arguments for domain
    """
    options = [option for option in arg.split(" ") if option]

    # -------------------------------------------------------
    # show all operation
    if not len(options):
        show_all()
    # -------------------------------------------------------
    # add operation
    elif options[0] == "add":
        if len(options) == 3:
            domain_name = options[1]
            file_name = options[2]
            add_domain(file_name, domain_name)
        else:
            print("Use domain add <domain_name> <file_name>")
    # -------------------------------------------------------
    # remove operation
    elif options[0] == "remove":
        if len(options) == 3:
            domain_name = options[1]
            file_name = options[2]
            remove_domain(file_name, domain_name)
        else:
            print("Use domain remove <domain_name> <file_name>")
    # -------------------------------------------------------
    # rename operatoin
    elif options[0] == "rename":
        if len(options) == 3:
            domain_name = options[1]
            new_domain_name = options[2]
            rename_domain(domain_name, new_domain_name)
        else:
            print("Use domain rename <domain_name> <new_domain_name>")
    # -------------------------------------------------------
    # search operation
    elif options[0] == "search":
        if len(options) == 2:
            domain_name = options[1]
            search_domain(domain_name)
        else:
            print("Use domain search <domain_name>")
    # -------------------------------------------------------