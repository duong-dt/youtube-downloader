from pathlib import Path

scriptDir = Path(__file__).parent
if (p := scriptDir.joinpath("VERSION")).exists():
    __version__ = p.read_text()
else:
    __version__ = scriptDir.parent.joinpath("VERSION").read_text()

__all__ = ["__version__"]
