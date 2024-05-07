from pathlib import Path


# returns the absolute path of a path like string as an instance of Path()
def get_path(path: str) -> Path:
    if not Path(path).is_absolute():
        abs_path = Path(__file__).parent / path
    else:
        abs_path = Path(path)

    return abs_path
