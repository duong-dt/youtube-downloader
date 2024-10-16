from pytubefix import YouTube
from pytubefix.exceptions import PytubeFixError as PytubeError
from urllib.error import URLError
from os.path import split, isfile, join as pjoin
from .util import *
import argparse
import unicodedata

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url):
    global _ATTEMPTS
    try:
        yt = YouTube(
            url=url,
            on_complete_callback=complete,
            on_progress_callback=progress_update
        )
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        defaultTitle = stream.title
        special_char = [x for x in defaultTitle if unicodedata.category(x)[0] not in 'LN' and x not in '_-()[]! ']
        for c in special_char:
            defaultTitle = defaultTitle.replace(c, '')
        return stream, defaultTitle + '.mp4'
    except URLError:
        if _ATTEMPTS < 4:
            print('\nConnection Error !!! Trying again ... ')
            _ATTEMPTS += 1
            return initialize(url)
        else:
            sys.exit('Cannot connect to Youtube !!!')
    except PytubeError as err:
        _error(err)


def get_video(url, opt=None):
    stream, defaultTitle = initialize(url)
    if opt is None:
        opt = askLoc_or_Path()
    if opt == 1:
        save_dir, filename = choose_path(defaultTitle)
        print(f'Downloading {defaultTitle} - {stream.resolution} ')
        download(stream, save_dir, filename)
    if opt == 2:
        save_dir = choose_dir()
        if isfile(pjoin(save_dir, defaultTitle)):
            print('Skip existing file')
            return
        print(f'Downloading {defaultTitle} - {stream.resolution} ')
        download(stream, save_dir, defaultTitle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str, help='url of youtube video')
    parser.add_argument('opt', type=int, choices=[1, 2], help='1. Choose directory and filename\n2. Choose directory')

    args = parser.parse_args()
    get_video(args.url, args.opt)
