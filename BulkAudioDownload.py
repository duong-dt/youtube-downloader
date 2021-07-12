import sys
from DownloadAudio import initialize as init_one
from DownloadAudio import download as download_one
import argparse
from pytube import Playlist
from pytube.exceptions import PytubeError
from tkinter import Tk
from DownloadAudio import choose_dir

def initialize(url):
    try:
        playlist = Playlist(url)
        return playlist.video_urls
    except PytubeError:
        sys.exit('Invalid URL')

def download(videos, dir):
    for video in videos:
        stream, defaultTitle = init_one(video)
        print(f'Downloading {defaultTitle}')
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