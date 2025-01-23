from .DownloadAudio import initialize as init_one
from pytubefix import Playlist
from pytubefix.exceptions import PytubeFixError as PytubeError
from .util import download as download_one, _error, progress, wait
from pathlib import Path
from urllib.error import URLError
from typing import Iterable
from concurrent.futures import ThreadPoolExecutor

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> Iterable[str]:
    global _ATTEMPTS
    try:
        playlist = Playlist(url, client="WEB")
        return playlist.video_urls
    except URLError:
        if _ATTEMPTS < 4:
            print("Connection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def download(urls: Iterable[str], save_dir: Path):
    def run(url):
        id = progress.custom_add_task(
            title=url,
            description="Downloading ...",
            total=0,
            completed=0,
        )
        stream, defaultTitle = init_one(url)
        progress.update(id, description=stream.title, total=stream.filesize)
        progress.update_mapping(stream.title, id)
        download_one(stream, save_dir, defaultTitle)

    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url in urls:
                pool.submit(run, url)
                wait(0.5)


def get_audios(url: str, save_dir: Path):
    urls = initialize(url)
    download(urls, save_dir)


if __name__ == "__main__":
    pass
