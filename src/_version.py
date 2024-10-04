from pathlib import Path


def get_version() -> str:
    """Get the version from the VERSION file."""
    filepath = Path("src/VERSION")
    return filepath.read_text().strip() if filepath.exists() else "0.1.0alpha"


__version__ = get_version()
