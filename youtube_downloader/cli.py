from pathlib import Path
from urllib.parse import urlparse

import pyperclip
import questionary

from youtube_downloader import __version__
from youtube_downloader.helpers import (
    get_audio,
    get_audios,
    get_video,
    get_video_srt,
    get_videos,
)


def url_validate(url: str) -> bool | str:
    if urlparse(url).netloc.endswith("youtube.com") or (len(url) == 0):
        return True
    else:
        return "Please enter a YouTube URL"


main_opts = [
    "1. Download audio only (mp3)",
    "2. Download video and audio (mp4)",
    "3. Download video with caption (srt)",
    "4. Bulk download audios from playlist",
    "5. Bulk download videos from playlist",
]


def main() -> None:
    print(f"youtube-downloader version {__version__}")

    # Get URL from clipboard if available
    if not pyperclip.is_available():
        txt = pyperclip.paste()
        if url_validate(txt) is not True:
            txt = ""
    else:
        txt = ""

    # Get user inputs (URL, action, save location)
    answers = questionary.form(
        url=questionary.text(message="Enter YouTube URL:", default=txt, validate=url_validate),
        opt=questionary.select(message="What do you want to download ?", choices=main_opts),
        loc=questionary.path(
            message="Where do you want to save ?",
            default=str(Path.cwd()),
            only_directories=True,
            validate=lambda p: (True if Path(p).is_dir() else "Please enter path to a directory"),
        ),
    ).ask()

    # If user cancelled, stop executing
    if not answers:
        return

    save_dir = Path(answers.get("loc"))
    url = answers.get("url")

    if answers.get("opt").startswith("1."):  # Download audio only
        get_audio(url, save_dir)
    if answers.get("opt").startswith("2."):  # Donwload video
        get_video(url, save_dir)
    if answers.get("opt").startswith("3."):  # Download video with subtitle
        get_video_srt(url, save_dir)
    if answers.get("opt").startswith("4."):  # Download audios from playlist
        get_audios(url, save_dir)
    if answers.get("opt").startswith("5."):  # Download videos from playlist
        get_videos(url, save_dir)


if __name__ == "__main__":
    main()
