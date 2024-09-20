"""Path utilities."""
from pathlib import Path

def get_default_path():
    return Path(Path.home(), ".careamics", "ui").absolute()
