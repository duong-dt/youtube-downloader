import sys
from pytube import YouTube
from pytube.exceptions import PytubeError
from progressBar import *
from tkinter.filedialog import asksaveasfilename, askdirectory
import tkinter
from os.path import split, splitext, join as pjoin
import subprocess
from urllib.request import urlopen

tkinter.Tk().wm_withdraw()

def download_and_convert_parallely(stream, filename):
    response = urlopen(stream.url)

    command = ["ffmpeg", "-y", "-i", "-", filename]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)

    while True:
        chunk = response.read(16 * 1024)
        if not chunk:
            break
        process.stdin.write(chunk)

    process.stdin.close()
    process.wait()

def download_audio():
    option = input('Choose option:\n1. Directory and file name\n2. Directory (default title name and file type)\n')
    if option == '1':
        print('Choose directory and file name')
        fullpath = asksaveasfilename(
            filetypes = [
                ('Video Format', '.mp4'),
                ('Audio Format', '.mp3')
            ],
            defaultextension = '.*',
            initialfile = defaultTitle,
            confirmoverwrite = True
        )
        global extenstion
        path, extenstion = splitext(fullpath)
        dir, filename = split(path)

        if not filename:
            print('Cancelled operation')
            return

        if extenstion == '.mp4':
            audiostream.download(filename=filename, output_path=dir)
        if extenstion == '.mp3':
            # download_and_convert_parallely(stream, fullpath)
            audiostream.download(filename=filename, output_path=dir)
            command = ' '.join((
                'ffmpeg.exe -loglevel verbose -hide_banner', 
                '-y -i',
                f'"{path}.mp4"',
                f'"{fullpath}"'
            ))
            print('Converting to mp3')
            subprocess.run(command, shell=True).check_returncode()
            if input('\nDelete mp4 file? [y/n]\n') == 'y':
                subprocess.run('del /F ' + f'"{path}.mp4"'.replace('/', '\\'), shell=True).check_returncode()
            print('Done')
    else:
        if option == '2':
            print('Choose directory')
            path = askdirectory()
            if not path:
                print('Cancelled operation')
                return
            audiostream.download(output_path=path)

def download_video():
    caption_code = input('Caption code:')
    option = input('Choose option:\n1. Directory and file name\n2. Directory (default title name)\n')
    if option == '1':
        print('Choose directory and file name')
        fullpath = asksaveasfilename(
            filetypes = [
                ('MP4', '.mp4')
            ],
            initialfile = defaultTitle,
            confirmoverwrite = True
        )
        path, filename = split(fullpath)
        if not filename:
            print('Cancelled operation')
            return
        videostream.download(filename=filename, output_path=path)
        if captions[caption_code]:
            captions[caption_code].download(title=filename, output_path=path)
        else:
            print('Caption not exist')
    else:
        if option == '2':
            print('Choose directory')
            path = askdirectory()
            if not path:
                print('Cancelled operation')
                return
            videostream.download(output_path=path)
            if captions[caption_code]:
                captions[caption_code].download(title=defaultTitle, output_path=path)
            else:
                print('Caption not exist')

def progress_update(stream, chunk, bytes_remaining):
    printProgressBar(stream.filesize - bytes_remaining, stream.filesize)

def complete(stream, filepath):
    print('\nDownloaded successfully')


url = input('URL:')
try:
    yt = YouTube(
        url,
        on_complete_callback = complete,
        on_progress_callback = progress_update
    )
    defaultTitle = yt.title
except PytubeError:
    sys.exit('Invalid URL')

type = input('Type:')

if type == 'audio':
    audiostream = yt.streams.get_audio_only()
    download_audio()
else:
    if type == 'video':
        videostream = yt.streams.filter(progressive=True).get_highest_resolution()
        captions = yt.captions
        download_video()

