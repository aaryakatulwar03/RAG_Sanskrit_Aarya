from pathlib import Path


def ensure_folder_exists(folder_path):
    """
    Create the folder if it does not already exist.
    """
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def print_separator():
    """
    Print a separator line in terminal output.
    """
    print("\n" + "-" * 50 + "\n")