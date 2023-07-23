#!/bin/bash

# Get current working directory
old_dir=$(pwd -P)

# Change to directory of script
cd $(dirname $0)

# Install dependencies
sudo -k apt install python3-tk python3-venv

# Create and activate python virtual environment
echo "Creating python environment"
python3 -m venv venv
source ./venv/bin/activate

# Install python packages
python3 -m pip install -r requirements.txt

# Deactivate python virtual environment 
deactivate

# Change to old directory
cd $old_dir