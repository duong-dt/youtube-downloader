from easygui import *
from helpers import *

main_opts = [
    '1. Download audio only (mp3)',
    '2. Download video and audio (mp4)',
    '3. Download video with caption (srt)',
    '4. Bulk download audios from playlist',
    '5. Bulk download videos from playlist',
]


def main():
    while True:
        choice = choicebox(
            title='Youtube Downloader',
            msg='Choose application options',
            choices=main_opts,
            preselect=1
        )
        if choice is None:
            break
        choice = main_opts.index(choice) + 1

        url = askURL()
        if choice == 1:
            get_audio(url, None)
        elif choice == 2:
            get_video(url, None)
        elif choice == 3:
            get_video_srt(url, None)
        elif choice == 4:
            get_audios(url)
        elif choice == 5:
            get_videos(url)

        if not ccbox(msg='Do you want to continue ?'):
            break


if __name__ == '__main__':
    main()
