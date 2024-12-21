from .DownloadVideo import initialize as init_one
from .util import download as download_one, _error
from pytubefix import Playlist
from pytubefix.exceptions import PytubeFixError as PytubeError
from pathlib import Path
from urllib.error import URLError
from typing import Iterable

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> Iterable[str]:
    global _ATTEMPTS
    try:
        playlist = Playlist(url)
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


def download(videos: Iterable[str], save_dir: Path):
    for video in videos:
        stream, defaultTitle = init_one(video)
        print(f"\nDownloading {defaultTitle} ")
        download_one(stream, save_dir, defaultTitle)


def get_videos(url: str, save_dir: Path):
    videos = initialize(url)
    download(videos, save_dir)


if __name__ == "__main__":
    pass
