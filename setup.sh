#!/bin/bash

# Get current working directory
#old_dir=$(pwd -P)

# Change to directory of script
#cd $(dirname $0)

# Install dependencies
sudo -k apt install python3-venv
pip3 install virtualenvwrapper
source $(which virtualenvwrapper.sh)

# Create python virtual environment and install dependencies
echo "Creating python environment"
mkvirtualenv --clear -r $(dirname $(realpath "$0"))/requirements.txt youtube-downloader

# Create youtube-downloader script in ~/.local/bin/
echo $'#!/bin/bash\nsource $(which virtualenvwrapper.sh)\nworkon youtube-downloader' > $HOME/.local/bin/youtube-downloader
echo "python3 $(dirname $(realpath "$0"))/youtube-downloader" >> $HOME/.local/bin/youtube-downloader
echo 'deactivate' >> $HOME/.local/bin/youtube-downloader
chmod +x $HOME/.local/bin/youtube-downloader


# Change to old directory
#cd $old_dirt
