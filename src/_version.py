from pathlib import Path


def get_version() -> str:
    """Get the version from the VERSION file."""
    filepath = Path("src/VERSION")

    if not filepath.exists():
        return "0.1.0alpha"

    return filepath.read_text().strip()


__version__ = get_version()
