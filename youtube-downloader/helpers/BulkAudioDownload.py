import sys
from .DownloadAudio import initialize as init_one
import argparse
from pytubefix import Playlist
from pytubefix.exceptions import PytubeFixError as PytubeError
from .util import choose_dir, download as download_one
from os.path import join as pjoin, isfile
from urllib.error import URLError

global _ATTEMPTS
_ATTEMPTS = 1


def initialize(url):
    global _ATTEMPTS
    try:
        playlist = Playlist(url)
        return playlist.video_urls
    except URLError:
        if _ATTEMPTS < 4:
            print('Connection Error !!! Trying again ... ')
            _ATTEMPTS += 1
            return initialize(url)
        else:
            sys.exit('Connection ERROR !!!')
    except PytubeError as err:
        _error(err)


def download(videos, save_dir):
    for video in videos:
        stream, defaultTitle = init_one(video)
        if isfile(pjoin(save_dir, defaultTitle)):
            print('\nSkip existing file ')
        else:
            print(f'\nDownloading {defaultTitle} ')
            download_one(stream, save_dir, defaultTitle)


def get_audios(url):
    videos = initialize(url)
    save_dir = choose_dir()
    download(videos, save_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str, help='url of youtube video')

    args = parser.parse_args()
    get_audios(args.url)
