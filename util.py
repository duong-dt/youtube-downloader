# from tkinter.filedialog import askdirectory, asksaveasfilename
# from tkinter import Tk
from easygui import *
from os.path import split
import sys


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)


def progress_update(stream, chunk, bytes_remaining):
    printProgressBar(stream.filesize - bytes_remaining, stream.filesize)


def complete(stream, filepath):
    filename = split(filepath)[-1]
    print(f'\nSuccessfully downloaded {filename} ')


def download(stream, save_dir, filename):
    stream.download(filename=filename, output_path=save_dir)


def choose_path(defaultTitle):
    print('Choose directory and file name')
    # fullpath = asksaveasfilename(
    #     filetypes=[
    #         ('Video Format', '.mp4')
    #     ],
    #     defaultextension='.*',
    #     initialfile=defaultTitle,
    #     confirmoverwrite=True
    # )
    fullpath = filesavebox(
        msg='Select file location',
        title='Save as',
        filetypes=['*.mp4', '*.mp3'],
        default=defaultTitle
    )

    if not fullpath:
        sys.exit('Cancelled')
    else:
        save_dir, filename = split(fullpath)
        if not filename:
            sys.exit('Cancelled')
        return save_dir, filename


def choose_dir():
    print('Choose directory')
    # path = askdirectory()
    path = diropenbox(
        title='Save in',
        msg='Select save location'
    )
    if not path:
        sys.exit('Cancelled')
    return path


def askLoc_or_Path():
    opt = choicebox(
        msg='Select save option',
        choices=[
            '1. Select file location and name',
            '2. Select file location'
        ]
    )
    if opt is None:
        sys.exit('Cancelled')
    opt = int(opt[0])
    return opt

