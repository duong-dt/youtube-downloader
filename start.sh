#!/bin/bash

source $(which virtualenvwrapper.sh)

workon youtube-downloader

python3 $(dirname $0)/youtube-downloader

deactivate

