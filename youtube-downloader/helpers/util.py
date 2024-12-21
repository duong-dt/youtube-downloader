from pathlib import Path
import sys
from pytubefix import Stream
from pytubefix.cli import on_progress


def progress_update(stream: Stream, chunk: bytes, bytes_remaining: int):
    on_progress(stream, chunk, bytes_remaining)


def complete(stream: Stream, filepath: str):
    filename = Path(filepath).name
    print(f"\nSuccessfully downloaded {filename} ")


def download(stream: Stream, save_dir: Path, filename: str):
    stream.download(filename=filename, output_path=save_dir)


def _error(_exception: Exception):
    print(f"{type(_exception).__name__} : {_exception}")
    sys.exit(1)
