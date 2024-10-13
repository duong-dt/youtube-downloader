# YouTube Downloader

1. YouTube Video download
   * Single video or All videos from a playlist
   * Download caption option available
   * Highest .mp4 resolution

2. YouTube Audio download
   * Single video or All videos from a playlist
   * Download audio only track to .mp3 file

# Dependencies
1. PyPI packages
   * easygui
   * pyperclip
   * pytubefix
2. Apt packages (for Linux)
   * python3-tk
   * python3-venv

# Installation via CLI
1. Download repo or clone
    ```commandline
    git clone https://github.com/duong-dt/youtube-downloader.git
    ```

2. Setup environment
   ```commandline
   setup.sh
   ```

3. Run application
   ```commandline
   start.sh
   ```

# CLI Application

## Step 1. Choose options

### Available options:

1. Download audio only (mp3)
2. Download video and audio (mp4)
3. Download video with caption (srt)
4. Bulk download audios from playlist
5. Bulk download videos from playlist

## Step 2. Enter YouTube video URL (auto-detect from clipboard)

## Step 3. Choose directory or full path (directory + filename)

Note: If PyTubeFix failed to connect to YouTube, it may need to be upgraded to the newest version (re-run setup.sh)
