from lib.commands.core.configure import load_shorthand, Shorthand


def c_tutorial():
    shorthand: Shorthand = load_shorthand()
    description = "commands\n"\
                  " build ({build_short}): build texts\n"\
                  " list ({list_short}): list all documents\n"\
                  " edit ({edit_short}): edit documents\n"\
                  " tag ({tag_short}): tag documents\n"\
                  " rename ({rename_short}): raname a document\n"\
                  " save_history ({save_history_short}): save diffs\n"\
                  " todo ({todo_short}): edit todo list\n"\
                  " diff ({diff_short}): show diff (before stage)\n"\
                  " clear ({clear_short}): clear\n"\
                  " tutorial ({tutorial}): show tutorial\n"\
                  " quit ({quit_short}): quit".format(build_short=shorthand["build"],
                                                      list_short=shorthand["list"],
                                                      edit_short=shorthand["edit"],
                                                      tag_short=shorthand["tag"],
                                                      rename_short=shorthand["rename"],
                                                      save_history_short=shorthand["save_history"],
                                                      todo_short=shorthand["todo"],
                                                      diff_short=shorthand["diff"],
                                                      clear_short=shorthand["clear"],
                                                      tutorial=shorthand["tutorial"],
                                                      quit_short=shorthand["quit"])

    print(description)