from easygui import *

main_opts = [
    '1. Download audio only (mp3)',
    '2. Download video and audio (mp4)',
    '3. Download video with caption (srt)',
    '4. Bulk download audios from playlist',
    '5. Bulk download videos from playlist',
]

if __name__ == '__main__':
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

        from askURL import askURL
        url = askURL()
        if choice == 1:
            from DownloadAudio import get_audio
            get_audio(url, None)
        elif choice == 2:
            from DownloadVideo import get_video
            get_video(url, None)
        elif choice == 3:
            from DownloadVideoWithCaption import get_video_srt
            get_video_srt(url, None)
        elif choice == 4:
            from BulkAudioDownload import get_audios
            get_audios(url)
        elif choice == 5:
            from BulkVideoDownload import get_videos
            get_videos(url)

        if not ccbox(msg='Do you want to continue ?'):
            break
