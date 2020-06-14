from lib.commands.core.configure import (init,
                                         save_root_path,
                                         save_uuid,
                                         config_editor,
                                         config_user,
                                         load_config,
                                         make_directory)
def initialize():
    print("Welcome!")
    init()
    save_root_path()
    save_uuid()
    print("set user name")
    config_user(user=input())
    print("set your editor. default is vi")
    editor = input() or "vi"
    config_editor(editor=editor)
    dirs = ["DOCUMENT", "HISTORY", "TODO", "MEMO", "METADATA", "TAG", "DOMAIN"]
    config  = load_config()
    for d in dirs:
        make_directory(d, config)
    print("Complete init")