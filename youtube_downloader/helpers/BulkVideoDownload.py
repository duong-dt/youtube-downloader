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


def download(videos: Iterable[str], save_dir: Path):
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for video in videos:
                stream, defaultTitle = init_one(video)
                progress.custom_add_task(
                    title=stream.title,
                    description=defaultTitle,
                    total=stream.filesize,
                )

                pool.submit(download_one, stream, save_dir, defaultTitle)


def download_wffmpeg(videos: Iterable[str], save_dir: Path):
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for video in videos:
                audio_stream, video_stream, defaultTitle = init_one_ffmpeg(
                    video
                )
                id = progress.custom_add_task(
                    title=video,
                    description=defaultTitle,
                    total=audio_stream.filesize + video_stream.filesize,
                    completed=0,
                )
                progress.update_mapping(audio_stream.title, id)
                progress.update_mapping(video_stream.title, id)

                pool.submit(
                    download_one_ffmpeg,
                    audio_stream,
                    video_stream,
                    save_dir,
                    defaultTitle,
                )


def get_videos(url: str, save_dir: Path):
    videos = initialize(url)
    if not check_ffmpeg():
        download(videos, save_dir)
    else:
        download_wffmpeg(videos, save_dir)


if __name__ == "__main__":
    pass
