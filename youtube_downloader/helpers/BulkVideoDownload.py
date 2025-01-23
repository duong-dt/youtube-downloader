from .DownloadVideo import (
    initialize as init_one,
    initialize_wffmpeg as init_one_ffmpeg,
)
from .util import (
    download as download_one,
    download_video_wffmpeg as download_one_ffmpeg,
    _error,
    progress,
    check_ffmpeg,
    wait,
)
from pytubefix import Playlist
from pytubefix.exceptions import PytubeFixError as PytubeError
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


def download_wffmpeg(videos: Iterable[str], save_dir: Path):
    def run(url):
        id = progress.custom_add_task(
            title=url,
            description="Downloading ...",
            total=0,
            completed=0,
        )
        audio_stream, video_stream, defaultTitle = init_one_ffmpeg(video)
        if not save_dir.joinpath(defaultTitle).exists():
            progress.update(
                id,
                description=defaultTitle,
                total=audio_stream.filesize + video_stream.filesize,
                completed=0,
            )
            progress.update_mapping(audio_stream.title, id)
            progress.update_mapping(video_stream.title, id)
            download_one_ffmpeg(
                audio_stream,
                video_stream,
                save_dir,
                defaultTitle,
            )

    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for video in videos:
                pool.submit(run, video)
                wait(0.5)


def get_videos(url: str, save_dir: Path):
    videos = initialize(url)
    if not check_ffmpeg():
        download(videos, save_dir)
    else:
        download_wffmpeg(videos, save_dir)


if __name__ == "__main__":
    pass
