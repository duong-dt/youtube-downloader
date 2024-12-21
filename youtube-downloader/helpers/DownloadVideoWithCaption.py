import math
import time
from .util import (
    progress_update,
    download,
    complete,
    _error,
)
from pytubefix import YouTube, Stream, CaptionQuery
from pytubefix.exceptions import PytubeFixError as PytubeError
from urllib.error import URLError
from pathlib import Path
import unicodedata
import questionary
from html import unescape
from xml.etree import ElementTree

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url: str) -> tuple[Stream, CaptionQuery, str]:
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            on_complete_callback=complete,
            on_progress_callback=progress_update,
        )
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        defaultTitle = stream.title
        special_char = [
            x
            for x in defaultTitle
            if unicodedata.category(x)[0] not in "LN" and x not in "_-()[]! "
        ]
        for c in special_char:
            defaultTitle = defaultTitle.replace(c, "")
        captions = []
        if len(yt.captions) >= 2:
            caption_choices = questionary.checkbox(
                message="Select captions to download",
                choices=[
                    f"{code} ---- {yt.captions[code].name}"
                    for code in yt.captions.lang_code_index.keys()
                ],
            ).ask()
            for choice in caption_choices:
                code = choice.split("----", 1)[0].strip()
                captions.append(yt.captions.get(code))
        else:
            captions = yt.captions
        return stream, captions, defaultTitle + ".mp4"
    except URLError:
        if _ATTEMPTS < 4:
            print("\nConnection Error !!! Trying again ... ")
            _ATTEMPTS += 1
            return initialize(url)
        else:
            _error(Exception("Cannot connect to Youtube !!!"))
    except PytubeError as err:
        _error(err)


def float_to_srt_time_format(d: float) -> str:
    """Convert decimal durations into proper srt format.

    :rtype: str
    :returns:
        SubRip Subtitle (str) formatted time duration.

    float_to_srt_time_format(3.89) -> '00:00:03,890'
    """
    fraction, whole = math.modf(d)
    time_fmt = time.strftime("%H:%M:%S,", time.gmtime(whole))
    ms = f"{fraction:.3f}".replace("0.", "")
    return time_fmt + ms


def xml_to_srt(xml_captions: str) -> str:
    """Convert xml caption tracks to "SubRip Subtitle (srt)".

    :param str xml_captions:
    XML formatted caption tracks.
    """
    segments = []
    root = ElementTree.fromstring(xml_captions)
    i = 0
    for child in list(root.iter("body"))[0]:
        if child.tag == "p":
            caption = ""
            if len(list(child)) == 0:
                # instead of 'continue'
                caption = child.text
            for s in list(child):
                if s.tag == "s":
                    caption += " " + s.text
            caption = unescape(
                caption.replace("\n", " ").replace("  ", " "),
            )
            try:
                duration = float(child.attrib["d"]) / 1000.0
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"]) / 1000.0
            end = start + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=sequence_number,
                start=float_to_srt_time_format(start),
                end=float_to_srt_time_format(end),
                text=caption,
            )
            segments.append(line)
            i += 1
    return "\n".join(segments).strip()


def get_srt_name(fname: str, code: str) -> str:
    filename = Path(fname).stem
    return f"{filename} ({code}).srt"


def get_video_srt(url: str, save_dir: Path):
    stream, captions, defaultTitle = initialize(url)
    print(f"Downloading {defaultTitle} - {stream.resolution}")
    download(stream, save_dir, defaultTitle)
    for cap in captions:
        print(f"Downloading subtitle {cap.code} ")
        try:
            cap.generate_srt_captions()
        except Exception:
            with open(
                save_dir.joinpath(get_srt_name(defaultTitle, cap.code)), "w"
            ) as file_handle:
                file_handle.write(xml_to_srt(cap.xml_captions))
        else:
            cap.download(title=defaultTitle, output_path=save_dir)
        print(f"Successfully downloaded {cap.code} ")


if __name__ == "__main__":
    pass
