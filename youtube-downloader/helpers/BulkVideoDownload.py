import sys
from .DownloadVideo import initialize as init_one
from .util import download as download_one, choose_dir
import argparse
from pytube import Playlist
from pytube.exceptions import PytubeError
from os.path import isfile, join as pjoin
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
    except PytubeError:
        sys.exit('Invalid URL')


def download(videos, save_dir):
    for video in videos:
        stream, defaultTitle = init_one(video)
        if isfile(pjoin(save_dir, defaultTitle)):
            print('\nSkip existing file')
        else:
            print(f'\nDownloading {defaultTitle} ')
            download_one(stream, save_dir, defaultTitle)


def get_videos(url):
    videos = initialize(url)
    save_dir = choose_dir()
    download(videos, save_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str, help='url of youtube video')

    args = parser.parse_args()
    get_videos(args.url)
