# YouTube Downloader

1. YouTube Video download
   * Single video or All videos from a playlist
   * Download caption option available
   * Highest .mp4 resolution

2. YouTube Audio download
   * Single video or All videos from a playlist
   * Download audio only track to .mp3 file

# Installation
1. Using `pip`
   ```commandline
   pip install youtube-downloader-cli
   ```

2. Using `uv`
   ```commandline
   uv tool install youtube-downloader-cli
   ```

# CLI Application

## Step 1. Enter YouTube video URL (auto-detect from clipboard)

## Step 2. Choose options

### Available options:

1. Download audio only 
2. Download video 
3. Download video with caption 
4. Download audios from playlist
5. Download videos from playlist

## Step 3. Choose a directory to save file(s)

Note: If PyTubeFix failed to connect to YouTube, it may need to be upgraded to the newest version.
Using `pip`: `pip install --upgrade pytubefix`. Or using `uv`: `uv install youtube-downloader-cli --upgrade --reinstall`. 

# Dependencies
1. For CLI Application
   * pyperclip
   * pytubefix
   * questionary
   * rich

2. Of `pytubefix`
   
   NodeJS is used for POTOKEN generation by `pytubefix`. If NodeJS is not available, POTOKEN will be skipped, may result in YouTube denying `pytubefix`'s requests.

3. FFMPEG
   
   Progressive stream (both audio & video in one file) in YouTube has lower resolution. If `ffmpeg` is available, high resolution video & audio will be downloaded separately, then merges using `ffmpeg`.

   If `ffmpeg` is not available in $PATH, progressive stream will be downloaded.
