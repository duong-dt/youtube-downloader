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
    progress.update(id, completed=stream.filesize - bytes_remaining)


def complete(stream: Stream, filepath: str):
    filename = Path(filepath).name
    print(f"Successfully downloaded {filename} ")
    progress.remove_task(progress.task_ids_mapping.get(stream.title))


def download(stream: Stream, save_dir: Path, filename: str):
    stream.download(filename=filename, output_path=save_dir)


def _error(_exception: Exception):
    print(f"{type(_exception).__name__} : {_exception}")
    sys.exit(1)


def getDefaultTitle(title: str) -> str:
    """
    Create safe file name by removing special character
    from YouTube video title
    """

    special_char = [
        x
        for x in title
        if unicodedata.category(x)[0] not in "LN" and x not in "_-()[]! "
    ]
    for c in special_char:
        title.replace(c, "")

    return title
