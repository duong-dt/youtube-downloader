import io
from collections.abc import Callable
from pathlib import Path
from urllib.parse import urlparse

import click
import pyperclip
import questionary
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from rich.console import Console

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


# fmt: off
main_opts: dict[str, Callable[[str, Path], None]] = {
    "1. Download audio only "           : get_audio,
    "2. Download video "                : get_video,
    "3. Download video with caption "   : get_video_srt,
    "4. Download audios from playlist " : get_audios,
    "5. Download videos from playlist " : get_videos,
}
# fmt: on


url_hist_path = Path("~/.local/share/youtube-downloader-cli/url_history").expanduser()
url_hist = FileHistory(url_hist_path)
save_hist_path = Path("~/.local/share/youtube-downloader-cli/save_history").expanduser()
save_hist = FileHistory(save_hist_path)


USAGE_MARKUP = """
SAMPLE : Provide inputs as per steps below
    [white]STEP 1 : Please enter YouTube URL that you want to download from[/white]
      Ex: [bold]? Enter YouTube URL: [yellow]https://youtube.com/?v=example1[/yellow][/bold]

    [white]STEP 2 : Select action[/white]
      Ex: [bold]? What do you want to download ?
        [white]    1. Download audio only
        [yellow]  » 2. Download video[/yellow] 
        [white]    3. Download video with caption
        [white]    4. Download audios from playlist
        [white]    5. Download videos from playlist
        [/bold]

    Option 2 selected:
      Ex: [bold]? What do you want to download ? [yellow]2. Download video[/yellow][/bold]

    STEP 3 : Choose save location
      Ex: [bold]? Where do you want to save ? [yellow]~/Videos/[/yellow][/bold]

    STEP 4 : If option 3 is chosen in STEP 2, select captions to download here
      Ex: [bold]? Select captions to download (Use arrow keys to move, <space> to select, <a> to toggle, <i> to invert)
            [yellow]» ○ en ---- English[/yellow]
            [white]  ○ ja ---- Japanese[/white]
            [white]  ○ ko ---- Korean[/white]
            [/bold]

"""

CMD_HELP_MARKUP = "[italic green]Run without option to start the app[/italic green]"


class RichFormatter(click.HelpFormatter):
    def __init__(
        self,
        indent_increment: int = 2,
        width: int | None = None,
        max_width: int | None = None,
    ) -> None:
        super().__init__(indent_increment, width, max_width)
        self.buffer = io.StringIO()
        self.console = Console(file=self.buffer, force_terminal=True)

    def write(self, string: str) -> None:
        self.console.print(string, end="")

    def getvalue(self) -> str:
        return self.buffer.getvalue()

    def write_usage(self, prog: str, args: str = "", prefix: str | None = None) -> None:
        super().write_usage(prog, args, prefix=(prefix or "USAGE : "))


class RichHelpCmd(click.Command):
    def get_help(self, ctx: click.Context) -> str:
        formatter = RichFormatter(width=ctx.terminal_width, max_width=ctx.max_content_width)
        self.format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        formatter.write(
            "[bold]youtube-downloader-cli :penguin: CLI APP to download from YouTube[/bold]\n"
        )

        formatter.write_paragraph()
        self.format_usage(ctx, formatter)
        formatter.write(self.help)

        formatter.write_paragraph()
        self.format_options(ctx, formatter)

        formatter.write(self.epilog)


@click.command(cls=RichHelpCmd, help=CMD_HELP_MARKUP, epilog=USAGE_MARKUP)
@click.help_option("-h", "--help", is_flag=True, is_eager=True)
@click.option("-v", "--version", is_flag=True, is_eager=True, help="Show version and exit.")
def main(version: bool) -> None:
    print(f"youtube-downloader-cli v{__version__}")
    if version:
        return

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
    opt = answers.get("opt")

    main_opts.get(opt)(url, save_dir)


if __name__ == "__main__":
    main()
