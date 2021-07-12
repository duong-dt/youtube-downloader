@echo off
color 09
mode con: cols=135 lines=30
set _python="C:\Users\Do Tung Duong\AppData\Local\Programs\Python\Python38\python.exe"
set _audio="D:\python\youtube_downloader\DownloadAudio.py"
set _video="D:\python\youtube_downloader\DownloadVideo.py"
set _video_caption="D:\python\youtube_downloader\DownloadVideoWithCaption.py"
set _bulk_audio="D:\python\youtube_downloader\BulkAudioDownload.py"
set _bulk_video="D:\python\youtube_downloader\BulkVideoDownload.py"
set _notify="D:\python\youtube_downloader\notify.py"
set _askURL="D:\python\youtube_downloader\askURL.py"

:mainapp:
    cls
    echo                                    =================================================================
    echo                                    ^|^|                 Choose application options                  ^|^|
    echo                                    =================================================================
    echo                                    ^|^|          [  0. Exit program                         ]       ^|^|
    echo                                    ^|^|          [  1. Download audio only (mp3)            ]       ^|^|
    echo                                    ^|^|          [  2. Download video and audio (mp4)       ]       ^|^|
    echo                                    ^|^|          [  3. Download video with caption (srt)    ]       ^|^|
    echo                                    ^|^|          [  4. Bulk download audios from playlist   ]       ^|^|
    echo                                    ^|^|          [  5. Bulk download videos from playlist   ]       ^|^|
    echo                                    =================================================================
    echo.

    choice /C 012345 /N /T 300 /D 0
    if %errorlevel% EQU 1 goto:stop
    if %errorlevel% EQU 2 goto:audio
    if %errorlevel% EQU 3 goto:video
    if %errorlevel% EQU 4 goto:video_caption
    if %errorlevel% EQU 5 goto:bulk_audio
    if %errorlevel% EQU 6 goto:bulk_video
    goto:stop

:get_url:
    %_python% %_askURL%
    set /p _url=""
    if %main_opt% leq 3 goto:get_opt
    if %main_opt% gtr 3 goto:download

:get_opt:
    echo                                    ==============================================
    echo                                                  Choose options
    echo                                    ==============================================
    echo                                    [          0. Cancel                         ]
    echo                                    [          1. Choose directory and filename  ]
    echo                                    [          2. Choose directory               ]
    echo                                    ==============================================
    goto:download

:get_code:
    set /p _code="Enter caption code:   "
    goto:get_url

:audio:
	cls
    echo                                        Download audio only & echo.
    set main_opt=1
    goto:get_url

:video:
	cls
    echo                                        Download video & echo.
    set main_opt=2
    goto:get_url

:video_caption:
	cls
    echo                                        Download video and caption & echo.
    set main_opt=3
    goto:get_code

:bulk_audio:
	cls
    echo                                        Download audios from playlist & echo.
    set main_opt=4
    goto:get_url

:bulk_video:
	cls
    echo                                        Download videos from playlist & echo.
    set main_opt=5
    goto:get_url

:download:
    if %main_opt% equ 4 %_python% %_bulk_audio% %_url% & goto:notify
    if %main_opt% equ 5 %_python% %_bulk_video% %_url% & goto:notify
    choice /c 012 /n
    if %errorlevel% equ 1 goto:continue_stop
    if %errorlevel% equ 2 (
        if %main_opt% equ 1 %_python% %_audio% %_url% 1 & goto:notify
        if %main_opt% equ 2 %_python% %_video% %_url% 1 & goto:notify
        if %main_opt% equ 3 %_python% %_video_caption% %_url% %_code% 1 & goto:notify
    )
    if %errorlevel% equ 3 (
        if %main_opt% equ 1 %_python% %_audio% %_url% 2 & goto:notify
        if %main_opt% equ 2 %_python% %_video% %_url% 2 & goto:notify
        if %main_opt% equ 3 %_python% %_video_caption% %_url% %_code% 2 & goto:notify
    )

:notify:
    %_python% %_notify% %_url%
    goto:continue_stop

:continue_stop:
    echo.
    choice /c 01 /n /m "Press 0 to exit, 1 to continue ...     "
    if %errorlevel% equ 1 exit
    if %errorlevel% equ 2 goto:mainapp

:stop:
    echo Press any key to exit ...
    pause >nul