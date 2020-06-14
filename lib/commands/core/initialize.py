from lib.commands.core.configure import (init,
                                         save_root_path,
                                         save_uuid,
                                         config_editor,
                                         config_editor_file_pos,
                                         config_deploy_path,
                                         config_user,
                                         load_config,
                                         make_directory)
def initialize():
    print("Welcome!")
    init()
    save_root_path()
    save_uuid()
    print("set user name")
    user = input()
    config_user(user=user)
    print("set your editor. default is vi")
    editor = input() or "vi"
    config_editor(editor=editor)
    if editor != "vi":
        print("Configure your editor's file pos as opening")
        print("eg. vi <file_name> -> type 0")
        print(f"{editor}" " <0> <1> <2>...")
        is_valid_input = False
        while is_valid_input:
            pos = input()
            try:
                pos = int(pos)
                is_valid_input = True
            except:
                pass
    else:
        pos = 0
    config_editor_file_pos(pos=pos)
    print("set your content deploy path")
    config_deploy_path(path=input())
    dirs = ["DOCUMENT", "HISTORY", "TODO", "MEMO", "METADATA", "TAG", "DOMAIN"]
    config  = load_config()
    for d in dirs:
        make_directory(d, config)
    print("Complete init")