import os

from config import BAD_DIRS, WEIGHT_BAD_PATH


def is_bad_path(exe):
    if not exe:
        return False, 0, "bad_path"

    path = os.path.normcase(exe).lower()

    for bad_dir in BAD_DIRS:
        if bad_dir in path:
            return True, WEIGHT_BAD_PATH, "bad_path"

    return False, 0, "bad_path"


RULES = [is_bad_path]


