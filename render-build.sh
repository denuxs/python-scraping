#!/usr/bin/env bash
# exit on error
set -o errexit

STORAGE_DIR=/opt/render/project
mkdir -p $STORAGE_DIR/chrome
cd $STORAGE_DIR/chrome

echo "...Downloading Chrome"
wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
rm ./google-chrome-stable_current_amd64.deb
cd ..

# add your own build commands...
pip install -r requirements.txt