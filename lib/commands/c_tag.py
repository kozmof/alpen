from .core.tag_ops import add_tag

def c_tag(arg):
    options = arg.split(" ")
    if options[0] == "add":
        if len(options) == 3:
            tag_name = options[1]
            file_name = options[2]
            add_tag(file_name, tag_name)
        else:
            print("Use add <tag_name> <file_name>")

    elif options[0] == "delete":
        print("DEBUG DELETE")
    elif options[0] == "search":
        print("DEBUG SEARCH")