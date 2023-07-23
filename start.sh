#!/bin/bash

# Get current working directory
old_dir=$(pwd -P)

# Change to directory of script
cd $(dirname $0)

# Activate Python Virtual Environment
source ./venv/bin/activate

# Run the application
python3 youtube-downloader

# Deactivate Python Virtual Environment
deactivate

# Change to old directory
cd $old_dir