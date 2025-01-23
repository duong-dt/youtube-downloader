from pathlib import Path
from urllib.parse import urlparse

import pyperclip
import questionary
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

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
    "1. Download audio only ",
    "2. Download video ",
    "3. Download video with caption ",
    "4. Download audios from playlist ",
    "5. Download videos from playlist ",
]


url_hist_path = Path("~/.local/share/youtube-downloader-cli/url_history").expanduser()
url_hist = FileHistory(url_hist_path)
save_hist_path = Path("~/.local/share/youtube-downloader-cli/save_history").expanduser()
save_hist = FileHistory(save_hist_path)


def main() -> None:
    print(f"youtube-downloader version {__version__}")

    if not url_hist_path.parent.exists():
        url_hist_path.parent.mkdir(parents=True)
    url_hist_path.touch()
    save_hist_path.touch()

    # Get URL from clipboard if available
    if not pyperclip.is_available():
        txt = pyperclip.paste()
        if url_validate(txt) is not True:
            txt = ""
    else:
        txt = ""

    # Get user inputs (URL, action, save location)
    answers = questionary.form(
        url=questionary.text(
            message="Enter YouTube URL:",
            default=txt,
            validate=url_validate,
            enable_history_search=True,
            history=url_hist,
            auto_suggest=AutoSuggestFromHistory(),
        ),
        opt=questionary.select(message="What do you want to download ?", choices=main_opts),
        loc=questionary.path(
            message="Where do you want to save ?",
            default=str(Path.cwd()),
            only_directories=True,
            validate=lambda p: (
                True if Path(p).expanduser().is_dir() else "Please enter path to a directory"
            ),
            enable_history_search=False,
            history=save_hist,
            auto_suggest=AutoSuggestFromHistory(),
        ),
    ).ask()

    # If user cancelled, stop executing
    if not answers:
        return

    save_dir = Path(answers.get("loc")).expanduser().resolve()
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
