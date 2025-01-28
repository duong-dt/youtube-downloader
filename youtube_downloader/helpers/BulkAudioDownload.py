from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from urllib.error import URLError

from pytubefix import Playlist
from pytubefix.exceptions import PytubeFixError as PytubeError

from youtube_downloader.helpers.DownloadAudio import initialize as init_one
from youtube_downloader.helpers.util import _error, getDefaultTitle, metadata, progress, wait
from youtube_downloader.helpers.util import download as download_one

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> Iterable[str]:
    global _ATTEMPTS
    try:
        playlist = Playlist(url, client="WEB")
        metadata.add_title(url, Path(getDefaultTitle(playlist)).stem)
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


def download(urls: Iterable[str], save_dir: Path, **kwargs: Any) -> None:
    def run(url: str, **kwargs: Any) -> None:
        task_id = progress.custom_add_task(
            title=url,
            description="Downloading ...",
            total=0,
            completed=0,
        )
        stream, defaultTitle = init_one(url, **kwargs)
        progress.update(task_id, description=stream.title, total=stream.filesize)
        progress.update_mapping(stream.title, task_id)
        download_one(stream, save_dir, defaultTitle, **kwargs)

    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url in urls:
                pool.submit(run, url, **kwargs)
                wait(0.5)


def get_audios(url: str, save_dir: Path, **kwargs: Any) -> None:
    with metadata:
        urls = initialize(url)
        download(urls, save_dir, **kwargs)


if __name__ == "__main__":
    pass
