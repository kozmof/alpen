from .core.tag_ops import (add_tag,
                           remove_tag)

def c_tag(arg):
    options = [option for option in arg.split(" ") if option]
    if options[0] == "add":
        if len(options) == 3:
            tag_name = options[1]
            file_name = options[2]
            add_tag(file_name, tag_name)
        else:
            print("Use tag add <tag_name> <file_name>")

    elif options[0] == "remove":
        if len(options) == 3:
            tag_name = options[1]
            file_name = options[2]
            remove_tag(file_name, tag_name)
        else:
            print("Use tag remove <tag_name> <file_name>")

    elif options[0] == "search":
        print("DEBUG SEARCH")