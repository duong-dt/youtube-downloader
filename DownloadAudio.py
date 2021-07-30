from pytube import YouTube
from pytube.exceptions import PytubeError
import sys
from os.path import split, splitext
from progressBar import *
from tkinter.filedialog import askdirectory, asksaveasfilename
from tkinter import Tk
import subprocess
import argparse
import unicodedata

def progress_update(stream, chunk, bytes_remaining):
    printProgressBar(stream.filesize - bytes_remaining, stream.filesize)

def complete(stream, filepath):
    print('\nDownloaded successfully')
    fullpath, _ = splitext(filepath)
    command = ' '.join((
        'ffmpeg.exe -loglevel verbose -hide_banner', 
        '-y -i',
        f'"{fullpath}.mp4"',
        f'"{fullpath}.mp3"'
    ))
    print('Converting to mp3')
    subprocess.run(command, shell=True).check_returncode()
    subprocess.run('del /F ' + f'"{fullpath}.mp4"'.replace('/', '\\'), shell=True).check_returncode()
    print('Done')

def download(stream, dir, filename):
    stream.download(filename=filename, output_path=dir)

def choose_path(defaultTitle):
    print('Choose directory and file name')
    fullpath = asksaveasfilename(
        filetypes = [
            ('Audio Format', '.mp3')
        ],
        defaultextension = '.*',
        initialfile = defaultTitle,
        confirmoverwrite = True
    )
    path, extenstion = splitext(fullpath)
    dir, filename = split(path)
    if not filename:
        sys.exit('Cancelled')

    return dir, filename+'.mp4'

def choose_dir():
    print('Choose directory')
    path = askdirectory()
    if not path:
        sys.exit('Cancelled')
    return path

def initialize(url):
    try:
        yt = YouTube(
            url = url,
            on_complete_callback = complete,
            on_progress_callback = progress_update
        )
        stream = yt.streams.get_audio_only()
        defaultTitle = stream.title
        special_char = [x for x in defaultTitle if unicodedata.category(x)[0] not in 'LN' and x not in '_-()[]! ']
        for c in special_char:
            defaultTitle = defaultTitle.replace(c, '')
        return stream, defaultTitle
    except PytubeError:
        sys.exit('Invalid URL')

def main():
    parser = argparse.ArgumentParser(prog='Youtube Audio Downloader')
    parser.add_argument('url', type=str,help='url of youtube video')
    parser.add_argument('opt', type=int, choices=[1, 2], help='1. Choose directory and filename\n2. Choose directory')

    args = parser.parse_args()
    stream, defaultTitle = initialize(args.url)
    if args.opt == 1:
        dir, filename = choose_path(defaultTitle)
        download(stream, dir, filename)
    if args.opt == 2:
        dir = choose_dir()
        download(stream, dir, defaultTitle+'.mp4')

if __name__=='__main__':
    Tk().withdraw()
    main()