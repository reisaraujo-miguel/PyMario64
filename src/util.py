from pathlib import Path


def get_path(path: str) -> Path:
    """Get the absolute path of a path-like string and return a Path object."""
    if not Path(path).is_absolute():
        abs_path = Path(__file__).parent / path
    else:
        abs_path = Path(path)

    return abs_path
