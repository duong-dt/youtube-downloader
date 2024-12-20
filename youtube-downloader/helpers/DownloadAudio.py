from pytubefix import YouTube, Stream
from pytubefix.exceptions import PytubeFixError as PytubeError
from urllib.error import URLError
from pathlib import Path
from .util import _error, complete, progress_update, download, progress
import unicodedata

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> tuple[Stream, str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )
        stream = yt.streams.get_audio_only()
        defaultTitle = stream.title
        special_char = [
            x
            for x in defaultTitle
            if unicodedata.category(x)[0] not in "LN" and x not in "_-()[]! "
        ]
        for c in special_char:
            defaultTitle = defaultTitle.replace(c, "")
        return stream, defaultTitle + ".mp3"
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def get_audio(url: str, save_dir: Path):
    with progress:
        id = progress.custom_add_task(
            title=url, description="Downloading", start=False
        )
        stream, defaultTitle = initialize(url)
        progress.start_task(id)
        progress.update(
            id, description=defaultTitle, total=stream.filesize, completed=0
        )
        progress.update_mapping(stream.title, id)
        # print(f"Downloading {defaultTitle}")
        download(stream, save_dir, defaultTitle)


if __name__ == "__main__":
    pass
