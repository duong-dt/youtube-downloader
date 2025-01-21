from pathlib import Path

with Path(__file__).parent.parent.joinpath("VERSION") as f:
    __version__ = f.read_text()

__all__ = ["__version__"]
