from pathlib import Path
import sys
from pytubefix import Stream
from rich.progress import (
    Progress,
    TaskID,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TotalFileSizeColumn,
    FileSizeColumn,
    SpinnerColumn,
)
from rich.table import Column
from typing import Any
import unicodedata
from tempfile import TemporaryDirectory


class CustomProgress(Progress):
    def __init__(
        self,
        *columns,
        console=None,
        auto_refresh=True,
        refresh_per_second=10,
        speed_estimate_period=30,
        transient=False,
        redirect_stdout=True,
        redirect_stderr=True,
        get_time=None,
        disable=False,
        expand=False,
    ):
        super().__init__(
            *columns,
            console=console,
            auto_refresh=auto_refresh,
            refresh_per_second=refresh_per_second,
            speed_estimate_period=speed_estimate_period,
            transient=transient,
            redirect_stdout=redirect_stdout,
            redirect_stderr=redirect_stderr,
            get_time=get_time,
            disable=disable,
            expand=expand,
        )
        self.task_ids_mapping: dict[str, int] = dict()

    def custom_add_task(
        self,
        title: str,
        description: str,
        start: bool = True,
        total: float | None = 100,
        completed: int = 0,
        visible: bool = True,
        **fields: Any,
    ) -> TaskID:
        id = self.add_task(
            description, start, total, completed, visible, **fields
        )
        self.task_ids_mapping[title] = id
        return id

    def update_mapping(self, title: str, id: int):
        self.task_ids_mapping[title] = id


progress: CustomProgress = CustomProgress(
    SpinnerColumn(),
    TextColumn(
        "[progress.description]{task.description}",
        table_column=Column(width=30, overflow="ellipsis", no_wrap=True),
    ),
    BarColumn(bar_width=50, style="red", complete_style="green"),
    TextColumn(" - ", style="bar.back"),
    TaskProgressColumn(),
    TextColumn(" - ", style="bar.back"),
    FileSizeColumn(),
    TextColumn("/", style="green"),
    TotalFileSizeColumn(),
    transient=True,
    refresh_per_second=100,
)

progress2: Progress = Progress(
    SpinnerColumn(),
    TextColumn(
        "[progress.description]{task.description}",
        table_column=Column(width=30, overflow="ellipsis", no_wrap=True),
    ),
    BarColumn(bar_width=50, style="red", complete_style="green"),
    TaskProgressColumn(),
    transient=True,
    refresh_per_second=100,
)


def progress_update(stream: Stream, chunk: bytes, bytes_remaining: int):
    global progress
    # on_progress(stream, chunk, bytes_remaining)
    id = progress.task_ids_mapping.get(stream.title)
    progress.update(id, advance=len(chunk))


def complete(stream: Stream, filepath: str):
    file = Path(filepath)
    id = progress.task_ids_mapping.get(stream.title)

    with progress._lock:
        if progress._tasks[id].finished:
            if file.stem not in ["ain", "vin"]:
                print(f"Successfully downloaded {file.name} ")
            progress.remove_task(id)


def download(stream: Stream, save_dir: Path, filename: str):
    stream.download(filename=filename, output_path=save_dir)


def _error(_exception: Exception):
    print(f"{type(_exception).__name__} : {_exception}")
    sys.exit(1)


def getDefaultTitle(stream: Stream) -> str:
    """
    Create safe file name by removing special character
    from YouTube video title
    """

    title = stream.default_filename

    special_char = [
        x
        for x in title
        if unicodedata.category(x)[0] not in "LN" and x not in "_-()[]! "
    ]
    for c in special_char:
        title.replace(c, "")

    return title


def check_ffmpeg() -> bool:
    """
    Check if ffmpeg is available.
    return True if ffmpeg is present, False otherwise
    """

    import subprocess

    try:
        subprocess.check_call(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ffmpeg is not available", file=sys.stderr)
        return False


def ffmpeg_merge(audio: Path, video: Path, out: Path) -> bool:
    import subprocess

    try:
        subprocess.check_call(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio.resolve()),
                "-i",
                str(video.resolve()),
                "-c",
                "copy",
                "-loglevel",
                "warning",
                str(out.resolve()),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        print(f"ffmpeg convert failed for {out.name}", file=sys.stderr)
        return False


def download_video_wffmpeg(
    audio_stream: Stream, video_stream: Stream, save_dir: Path, filename: str
):
    with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
        audio_file = Path(tmpdir) / f"ain.{audio_stream.subtype}"
        video_file = Path(tmpdir) / f"vin.{video_stream.subtype}"

        download(audio_stream, Path(tmpdir), audio_file.name)
        download(video_stream, Path(tmpdir), video_file.name)

        if ffmpeg_merge(audio_file, video_file, save_dir / filename):
            print(f"Successfully downloaded {filename}")

