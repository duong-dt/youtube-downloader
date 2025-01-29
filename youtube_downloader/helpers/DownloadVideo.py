from pathlib import Path
from typing import Any
from urllib.error import URLError

from pytubefix import Stream, StreamQuery, YouTube
from pytubefix.exceptions import PytubeFixError as PytubeError

from youtube_downloader.helpers.util import (
    _error,
    check_ffmpeg,
    complete,
    download,
    download_video_wffmpeg,
    getDefaultTitle,
    metadata,
    progress,
    progress_update,
)

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str, **kwargs: Any) -> tuple[Stream, str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            client="WEB",
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )
        stream = get_resolution_upto(yt.streams.filter(progressive=True), **kwargs)
        defaultTitle = getDefaultTitle(yt, subtype=stream.subtype)
        metadata.add_title(url, Path(defaultTitle).stem)

        return stream, defaultTitle
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def get_resolution_upto(streams: StreamQuery, max_res: int = 1080) -> Stream:
    return sorted(
        filter(
            lambda s: (int(s.resolution[:-1]) <= max_res) or (max_res < 0),
            streams.filter(only_video=True),
        ),
        key=lambda s: int(s.resolution[:-1]),
    )[-1]


def initialize_wffmpeg(url: str, **kwargs: Any) -> tuple[Stream, Stream, str]:
    """
    With ffmpeg available, get audio & stream separately.
    return AudioStream, VideoStream, DefaultTitle
    """
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            client="WEB",
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )

        audio_stream, video_stream, defaultTitle = _init_ffmpeg(yt, **kwargs)
        metadata.add_title(url, Path(defaultTitle).stem)

        return audio_stream, video_stream, defaultTitle
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize_wffmpeg(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def _init_ffmpeg(yt: YouTube, **kwargs: Any) -> tuple[Stream, Stream, str]:
    audio_stream = yt.streams.get_audio_only()
    video_stream = get_resolution_upto(yt.streams.filter(only_video=True), **kwargs)
    defaultTitle = getDefaultTitle(yt, video_stream.subtype)

    return audio_stream, video_stream, defaultTitle


def get_video(url: str, save_dir: Path, **kwargs: Any) -> None:
    with progress, metadata:
        task_id = progress.custom_add_task(
            title=url,
            description="Downloading",
            start=False,
            total=0,
            completed=0,
        )
        if not check_ffmpeg():
            stream, defaultTitle = initialize(url, **kwargs)
            if not save_dir.joinpath(defaultTitle).exists():
                print(f"Downloading resolution {stream.resolution} for {defaultTitle}")
                progress.start_task(task_id)
                progress.update(
                    task_id,
                    description=defaultTitle,
                    total=stream.filesize,
                    completed=0,
                )
                progress.update_mapping(stream.title, task_id)

                download(stream, save_dir, defaultTitle, **kwargs)
        else:
            audio_stream, video_stream, defaultTitle = initialize_wffmpeg(url, **kwargs)
            if not save_dir.joinpath(defaultTitle).exists():
                print(f"Downloading resolution {video_stream.resolution} for {defaultTitle}")
                progress.start_task(task_id)
                progress.update(
                    task_id,
                    description=defaultTitle,
                    total=audio_stream.filesize + video_stream.filesize,
                    completed=0,
                )
                progress.update_mapping(audio_stream.title, task_id)
                progress.update_mapping(video_stream.title, task_id)

                download_video_wffmpeg(
                    audio_stream, video_stream, save_dir, defaultTitle, **kwargs
                )
            else:
                progress.remove_task(task_id)


if __name__ == "__main__":
    pass
