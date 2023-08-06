# AI Link Embedder #
## Introduction ##
This abomination of a code was created to solve my fiancé issue with migrating Adobe Illustrator files to different machine. It comes with absolutely no guarantee, but it seems to work. Good luck.

## Requirements ##
Running this script requires:
- Windows OS (macOS is not supported for now)
- Adobe Illustrator installed
## Setup ##
To install necessary dependency you need to run:
```shell
pip install -r requirement.txt
```
## Run ##
Usage:
```
usage: AI Link Embedder [-h] [-r] [-o] [-d DEST] [-p PREFIX] [-s SUFFIX]
                        dictionary

This script takes .ai files and save them with linked files embedded

positional arguments:
  dictionary            Directory with input .ai files

options:
  -h, --help            show this help message and exit
  -r, --recursive       Scan for .ai files recursively
  -o, --override        Override resulting .ai is it exists
  -d DEST, --dest DEST  Directory where resulting .ai files will be saved to
  -p PREFIX, --prefix PREFIX
  -s SUFFIX, --suffix SUFFIX
```
Example:
```shell
python3 main.py -o -d C:\Users\Username\Documents\ai_embedded -r C:\Users\Username\Documents\
```