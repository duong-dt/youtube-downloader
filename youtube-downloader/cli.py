import questionary
from pathlib import Path
from urllib.parse import urlparse
import pyperclip
from helpers import (
    get_audios,
    get_audio,
    get_video,
    get_videos,
    get_video_srt,
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


def main():
    if not pyperclip.is_available():
        txt = pyperclip.paste()
        if url_validate(txt) is not True:
            txt = ""
    else:
        txt = ""
    answers = questionary.form(
        url=questionary.text(
            message="Enter YouTube URL:", default=txt, validate=url_validate
        ),
        opt=questionary.select(
            message="What do you want to download ?", choices=main_opts
        ),
        loc=questionary.path(
            message="Where do you want to save ?",
            default=str(Path.cwd()),
            only_directories=True,
            validate=lambda p: (
                True
                if Path(p).is_dir()
                else "Please enter path to a directory"
            ),
        ),
    ).ask()

    if not answers:
        return

    save_dir = Path(answers.get("loc"))

    if answers.get("opt").startswith("1."):
        get_audio(answers.get("url"), save_dir)
    if answers.get("opt").startswith("2."):
        get_video(answers.get("url"), save_dir)
    if answers.get("opt").startswith("3."):
        get_video_srt(answers.get("url"), save_dir)
    if answers.get("opt").startswith("4."):
        get_audios(answers.get("url"), save_dir)
    if answers.get("opt").startswith("5."):
        get_videos(answers.get("url"), save_dir)


if __name__ == "__main__":
    main()
