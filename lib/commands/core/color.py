GREENC = "\033[1;32m"
BLUEC = "\033[1;34m"
CYANC = "\033[1;36m"
YELLOWC = "\033[93m"
ENDC = "\033[0m"


def color(text: str, color_type: str) -> str:
    if color_type == "green":
        return f"{GREENC}{text}{ENDC}"
    elif color_type == "blue":
        return f"{BLUEC}{text}{ENDC}"
    elif color_type == "cyan":
        return f"{CYANC}{text}{ENDC}"
    elif color_type == "yellow":
        return f"{YELLOWC}{text}{ENDC}"
