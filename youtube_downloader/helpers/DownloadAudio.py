from pathlib import Path
from typing import Any
from urllib.error import URLError

from pytubefix import Stream, YouTube
from pytubefix.exceptions import PytubeFixError as PytubeError

from youtube_downloader.helpers.util import (
    _error,
    complete,
    download,
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
        stream = yt.streams.get_audio_only()
        defaultTitle = getDefaultTitle(
            yt, subtype=Path(stream.default_filename).suffix.removeprefix(".")
        )
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


def get_audio(url: str, save_dir: Path, **kwargs: Any) -> None:
    with progress, metadata:
        task_id = progress.custom_add_task(title=url, description="Downloading", start=False)
        stream, defaultTitle = initialize(url, **kwargs)
        progress.start_task(task_id)
        progress.update(task_id, description=defaultTitle, total=stream.filesize, completed=0)
        progress.update_mapping(stream.title, task_id)
        # print(f"Downloading {defaultTitle}")
        download(stream, save_dir, defaultTitle, **kwargs)


if __name__ == "__main__":
    pass
