DEBUG = False


def set_debug(value: bool):
    global DEBUG
    DEBUG = value


def debug(*args, **kwargs):
    if DEBUG:
        print("DEBUG:", *args, **kwargs)
