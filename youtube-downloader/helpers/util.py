from pathlib import Path
import sys
from pytubefix import Stream


# Print iterations progress
def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=1,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int) # noqa: E501
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total))
    )
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)


def progress_update(stream: Stream, chunk: int, bytes_remaining: int):
    printProgressBar(stream.filesize - bytes_remaining, stream.filesize)


def complete(stream: Stream, filepath: str):
    filename = Path(filepath).name
    print(f"\nSuccessfully downloaded {filename} ")


def download(stream: Stream, save_dir: Path, filename: str):
    stream.download(filename=filename, output_path=save_dir)


def _error(_exception: Exception):
    print(f"{type(_exception).__name__} : {_exception}")
    sys.exit(1)
