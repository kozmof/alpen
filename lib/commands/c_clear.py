import subprocess
from .core.record import read_edited_file_record
from .core.todo import get_todo
from .core.gprint import grid_text


def change_log() -> str:
    return f"recently edited\n{read_edited_file_record()}" 


def c_clear(description):
    subprocess.run(["clear"])
    grid_0 = description
    grid_1 = change_log()
    grid_2 = get_todo()
    intro = grid_text(grid_0, grid_1, grid_2, margin=5)
    print(intro)