# Downloader & Installer for A32NX

[![GitHub latest release version](https://img.shields.io/github/v/release/Externoak/A32NX-installer.svg?style=plastic)](https://github.com/Externoak/A32NX-installer/releases/latest)
[![Github All Releases download count](https://img.shields.io/github/downloads/Externoak/A32NX-installer/total.svg?style=plastic)](https://github.com/Externoak/A32NX-installer/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Externoak/A32NX-installer/Build?style=plastic)](https://github.com/Externoak/A32NX-installer/actions)

## About

A simple installer made in Python with tkinter for the [A32NX](https://github.com/flybywiresim/a32nx) mod. 

This installer should automatically detect your MSFS Community folder, download and install the A32NX mod all with the click of a button. It will also check if the current version you have installed is up to date, either stable or development version.

## Download

Click here to download the latest stable version: [Download](https://github.com/Externoak/A32NX-installer/releases/latest/download/A32NX_Downloader.zip)

## Requirements (Only to regenerate the exe file)

Python 3.8.x (3.8.2 - version used by [@Externoak](https://github.com/Externoak))

Python 3.9 not supported!

Must have 64-bit version of python installed!

Pyinstaller 4.0

`pip install pyinstaller`

However, it is better to install PyInstaller from source after [building the bootloader yourself](https://pyinstaller.readthedocs.io/en/stable/bootloader-building.html). This prevents false positives as the bootloader provided by default is probably flagged by some antivirus software.

To do this first clone the PyInstaller repo, generate the bootloader and install PyInstaller manually:

```sh
git clone git@github.com:pyinstaller/pyinstaller.git
cd pyinstaller
cd bootloader
python ./waf all
cd ..
python setup.py install
```



## Install dependencies

`python -m pip install --upgrade Pillow`

`python -m pip install --upgrade hurry.filesize`

`python -m pip install --upgrade requests`

`python -m pip install --upgrade tqdm`

Or use the `requirements.txt` file to install everything at once

`python -m pip install --upgrade -r requirements.txt`

## How to generate exe file

`pyinstaller Downloader.spec`
