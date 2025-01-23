from collections.abc import Iterable
from pathlib import Path
from urllib.error import URLError

import questionary
from pytubefix import Caption, CaptionQuery, Stream, YouTube
from pytubefix.exceptions import PytubeFixError as PytubeError

from youtube_downloader.helpers.DownloadVideo import get_resolution_upto
from youtube_downloader.helpers.util import (
    _error,
    check_ffmpeg,
    complete,
    download,
    download_video_wffmpeg,
    getDefaultTitle,
    progress,
    progress2,
    progress_update,
)

global _ATTEMPTS
_ATTEMPTS = 1


def select_captions(captions: CaptionQuery) -> Iterable[Caption]:
    selected_captions = []
    if len(captions) == 0:
        print("No caption available")
    elif len(captions) > 1:
        caption_choices = questionary.checkbox(
            message="Select captions to download",
            choices=[
                f"{code} ---- {captions[code].name}" for code in captions.lang_code_index.keys()
            ],
        ).ask()
        for choice in caption_choices:
            code = choice.split("----", 1)[0].strip()
            selected_captions.append(captions.get(code))
    else:
        selected_captions = captions
    return selected_captions


def initialize(url: str) -> tuple[Stream, Iterable[Caption], str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            client="WEB",
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        defaultTitle = getDefaultTitle(stream)
        captions = select_captions(yt.captions)

        return stream, captions, defaultTitle
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def initialize_wffmpeg(
    url: str,
) -> tuple[Stream, Stream, Iterable[Caption], str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            client="WEB",
            on_progress_callback=progress_update,
        )
        audio_stream = yt.streams.get_audio_only()
        video_stream = get_resolution_upto(yt.streams.filter(only_video=True, subtype="mp4"))
        defaultTitle = getDefaultTitle(video_stream)
        captions = select_captions(yt.captions)

        return audio_stream, video_stream, captions, defaultTitle
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def get_srt_name(fname: str, code: str) -> str:
    filename = Path(fname).stem
    return f"{filename} ({code}).srt"


def get_video_srt(url: str, save_dir: Path) -> None:
    ffmpeg_available = check_ffmpeg()
    if not ffmpeg_available:
        stream, captions, defaultTitle = initialize(url)
    else:
        audio_stream, video_stream, captions, defaultTitle = initialize_wffmpeg(url)
    with progress:
        if not ffmpeg_available:
            progress.custom_add_task(
                title=stream.title,
                description=defaultTitle,
                total=stream.filesize,
            )

            download(stream, save_dir, defaultTitle)
        else:
            task_id = progress.custom_add_task(
                title=url,
                description=defaultTitle,
                total=audio_stream.filesize + video_stream.filesize,
                completed=0,
            )

            progress.update_mapping(audio_stream.title, task_id)
            progress.update_mapping(video_stream.title, task_id)

            download_video_wffmpeg(audio_stream, video_stream, save_dir, defaultTitle)

    with progress2:
        task_id = progress2.add_task("Downloading captions ... ", total=len(captions))
        for cap in captions:
            with save_dir.joinpath(get_srt_name(defaultTitle, cap.code)).open("w") as file_handle:
                file_handle.write(cap.generate_srt_captions())
            progress2.update(task_id, advance=1)
            print(f"Successfully downloaded {cap.name} caption")


if __name__ == "__main__":
    pass
