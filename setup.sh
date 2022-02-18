#!/usr/local/bin/bash

pip3 install --user -r requirements.txt

./test.py

# Debugging server & reloader.
# ~/server-tools/watcher.py main.py,test.py "./test.py"
