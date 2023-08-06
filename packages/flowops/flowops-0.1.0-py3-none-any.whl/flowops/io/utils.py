from pathlib import Path

from .typings import PathType


def get_ext(path: PathType) -> str:
    """
    Get the extension of a path.
    """

    if isinstance(path, Path):
        return path.suffix
    else:
        split = "." + path.split(".")
        if len(split) < 2:
            raise ValueError("Path has no extension!")
        return split[-1]
