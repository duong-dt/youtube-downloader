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
   * pytube
2. Apt packages (for Linux)
   * python3-tk
   * python3-venv

# Installation via CLI
1. Install dependencies (for Linux)
   ```commandline
   sudo apt-get install python3-venv python3-tk
   ```
   
2. Download repo or clone
    ```commandline
    git clone https://github.com/github-duongdt/youtube-downloader.git
    ```

3. Create & activate _**python virtual environment**_
   * In Window
    ```commandline
    cd youtube-downloader
    python -m venv venv
   .\venv\Scripts\activate
    ```
    * In Linux
    ```commandline
    cd youtube-downloader
    python3 -m venv venv
    source ./venv/bin/activate
    ```

4. Install PyPI dependencies
   * In Window
    ```commandline
    pip install -r requirements.txt
    ```
   
   * In Linux
   ```commandline
   pip3 install -r requirements.txt
   ```

5. Launch application
   * In Window
   ```commandline
   python app.py
   ```
   
   * In Linux
   ```commandline
   python3 app.py
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

## If PyTube failed to connect to YouTube, it may need to be upgraded to the newest version
   * In Window
   ```commandline
   pip install --upgrade pytube
   ```

   * In Linux
   ```commandline
   pip3 install --upgrade pytube
   ```
