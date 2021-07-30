from DownloadVideo import progress_update, download, choose_dir
from pytube import YouTube
from pytube.exceptions import PytubeError
import sys
import argparse
from tkinter import Tk
from os.path import splitext, split
from tkinter.filedialog import asksaveasfilename
import unicodedata

def complete(stream, filepath):
    path, _ = splitext(filepath)
    dir, filename = split(path)
    if caption:
        caption.download(title=filename, output_path=dir)
    else:
        print('\nNo caption available')
    print('\nDownloaded successfully')

def choose_path(defaultTitle):
    print('Choose directory and file name')
    fullpath = asksaveasfilename(
        filetypes = [
            ('Video Format', '.mp4')
        ],
        defaultextension = '.*',
        initialfile = defaultTitle,
        confirmoverwrite = True
    )
    dir, filename = split(fullpath)
    if not filename:
        sys.exit('Cancelled')

    return dir, filename

def main():
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str,help='url of youtube video')
    parser.add_argument('code', type=str, help='caption code')
    parser.add_argument('opt', type=int, choices=[1, 2], help='1. Choose directory and filename\n2. Choose directory')

    args = parser.parse_args()

    try:
        yt = YouTube(
            url = args.url,
            on_complete_callback = complete,
            on_progress_callback = progress_update
        )
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
        global caption
        defaultTitle = stream.title
        special_char = [x for x in defaultTitle if unicodedata.category(x)[0] not in 'LN' and x not in '_-()[]! ']
        for c in special_char:
            defaultTitle = defaultTitle.replace(c, '')
        caption = yt.captions.get(args.code)
    except PytubeError:
        sys.exit('Invalid URL')

    if args.opt == 1:
        dir, filename = choose_path(defaultTitle)
        download(stream, dir, filename)
    if args.opt == 2:
        dir = choose_dir()
        download(stream, dir, defaultTitle+'.mp4')

if __name__=='__main__':
    Tk().withdraw()
    main()