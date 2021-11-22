# Youtube Downloader

1. Youtube Video download
  * Single video or All videos from a playlist
  * Download caption option available
  * Highest .mp4 resolution

2. Youtube Audio download
  * Single video or All videos from a playlist
  * Download .mp4, then convert to .mp3 file (using ffmpeg)
  
# Installation via CLI

1. Download repo or clone
```
git clone https://github.com/github-duongdt/youtube-downloader.git
```

2. Create .venv folder
```
cd youtube-downloader
python -m venv .venv
```

3. Activate venv
```
.venv\Scripts\activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Launch app.cmd 

# Dependencies

* python>=3.8.4
* pytube=11.0.1
* pywin32=302
* win10toast=0.9

# CLI Application

## Step 1. Choose options

### Available options:

1. Download audio only (mp3)
2. Download video and audio (mp4)
3. Download video with caption (srt)
4. Bulk download audios from playlist
5. Bulk download videos from playlist

## Step 2. Enter Youtube video URL (now auto paste from clipboard)

## Step 3. Choose directory or full path (directory + filename)
