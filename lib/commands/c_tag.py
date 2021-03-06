from lib.commands.core.tag_ops import (add_tag,
                                       remove_tag,
                                       rename_tag,
                                       search_tag,
                                       show_all)

def c_tag(arg):
    options = [option for option in arg.split(" ") if option]

    if not len(options):
        show_all()

    elif options[0] == "add":
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

    elif options[0] == "rename":
        if len(options) == 3:
            tag_name = options[1]
            new_tag_name = options[2]
            rename_tag(tag_name, new_tag_name)
        else:
            print("Use tag rename <tag_name> <new_tag_name>")

    elif options[0] == "search":
        if len(options) == 2:
            tag_name = options[1]
            search_tag(tag_name)
        else:
            print("Use tag search <tag_name>")