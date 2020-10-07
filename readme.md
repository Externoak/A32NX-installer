# Downloader & Installer for A32NX

## About

A simple installer made in Python with tkinter for the [A32NX](https://github.com/flybywiresim/a32nx) mod. 

## Requirements (Only to regenerate the exe file)

Python 3.8.x (3.8.2 - version used by [@Externoak](https://github.com/Externoak))

Python 3.9 not supported!

Must have 64-bit version of python installed!

Pyinstaller 4.0

`pip install pyinstaller`

## Install dependencies

`python -m pip install --upgrade Pillow`

`python -m pip install --upgrade hurry.filesize`

`python -m pip install --upgrade requests`

`python -m pip install --upgrade tqdm`

## How to generate exe file

`pyinstaller Downloader.spec`
