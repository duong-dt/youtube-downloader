import sys
from DownloadVideo import initialize as init_one
from DownloadVideo import download as download_one
import argparse
from pytube import Playlist
from pytube.exceptions import PytubeError
from tkinter import Tk
from DownloadVideo import choose_dir
from os.path import isfile, join as pjoin
from urllib.error import URLError

global _ATTEMP
_ATTEMP = 1

def initialize(url):
    global _ATTEMP
    try:
        playlist = Playlist(url)
        return playlist.video_urls
    except URLError:
        if _ATTEMP < 4:
            print('Connection Error !!! Trying again ... ')
            _ATTEMP += 1
            return initialize(url)
        else:
            sys.exit('Connection ERROR !!!')
    except PytubeError:
        sys.exit('Invalid URL')

def download(videos, dir):
    for video in videos:
        stream, defaultTitle = init_one(video)
        if isfile(pjoin(dir, defaultTitle)):
            print('\nSkip existing file')
        else:
            print(f'\nDownloading {defaultTitle}')
            download_one(stream, dir, defaultTitle)

def main():
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str,help='url of youtube video')

    args = parser.parse_args()
    videos = initialize(args.url)
    dir = choose_dir()
    download(videos, dir)

if __name__=='__main__':
    Tk().withdraw()
    main()