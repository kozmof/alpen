import subprocess
from lib.commands.core.record import read_edited_file_record
from lib.commands.core.todo import get_todo
from lib.commands.core.memo import get_memo
from lib.commands.core.gprint import grid_text


def change_log() -> str:
    return f"recently edited\n{read_edited_file_record()}" 


def c_clear(show_grid=False):
    subprocess.run(["clear"])
    if show_grid:
        grid_0 = get_memo()
        grid_1 = change_log()
        grid_2 = get_todo()
        intro = grid_text(grid_0, grid_1, grid_2, margin=5)
        print(intro)