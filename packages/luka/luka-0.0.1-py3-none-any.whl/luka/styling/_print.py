from .constants import BLUE, BOLD, CYAN, GREEN, ITALIC, RED, UNDERLINE, YELLOW


def set_style(style):
    return lambda str_: f"{style}{str_}\033[00m"


def bold(str_: str):
    return set_style(BOLD)(str_)


def underline(str_: str):
    return set_style(UNDERLINE)(str_)


def italic(str_: str):
    return set_style(ITALIC)(str_)


def red(str_: str):
    return set_style(RED)(str_)


def green(str_: str):
    return set_style(GREEN)(str_)


def blue(str_: str):
    return set_style(BLUE)(str_)


def yellow(str_: str):
    return set_style(YELLOW)(str_)


def cyan(str_: str):
    return set_style(CYAN)(str_)
