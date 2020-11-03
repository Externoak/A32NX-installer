# Downloader & Installer for A32NX

[![GitHub latest release version](https://img.shields.io/github/v/release/Externoak/A32NX-installer.svg?style=plastic)](https://github.com/Externoak/A32NX-installer/releases/latest)
[![Github All Releases download count](https://img.shields.io/github/downloads/Externoak/A32NX-installer/total.svg?style=plastic)](https://github.com/Externoak/A32NX-installer/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Externoak/A32NX-installer/Build?style=plastic)](https://github.com/Externoak/A32NX-installer/actions)

## About

A simple installer made in Python with tkinter for the [A32NX](https://github.com/flybywiresim/a32nx) mod. 

This installer should automatically detect your MSFS Community folder, download and install the A32NX mod all with the click of a button. It will also check if the current version you have installed is up to date, either stable or development version.

## Download

Click here to download the latest stable version: [Download](https://github.com/Externoak/A32NX-installer/releases/latest/download/A32NX_Downloader.zip)

## FAQs

- Do I need to install this?
  
  No, this is only an executable no installation is necessary.
  
- I don't trust running unknown exe file.
  
  The source code of the Downloader is available for all to view. The exe file will always be automatically created in an isolated environment using Github workflows, 
  you are also free to scan the exe file using an antivirus or [Virustotal](https://www.virustotal.com/). 
  
- Do I need to find my Community folder?
  
  No, the Downloader should automatically detect your Community folder location, in some rare cases it will not be possible to detect it should then be manually selected .

- Why is my download speed so slow?
  
  Your download speed from GitHub may vary depending on your connection to their servers, the Downloader will always use all available bandwidth.
  
- Downloader warning: "Could not check for updates! Github API rate limit could be exceeded".
  
  It is most likely you overused the GitHub API wait for a few minutes or up to one hour and retry again. 
  
- Downloader error: "Folder could not be unzipped, failed reason: FileNotFound".
  
  It is most likely you have MSFS installed in a WpSystem file path, this directory is write-protected and cannot be written to. 
  The best solution is to select a temporary location for example your Desktop then download the A32NX folder there and move it manually to your Community folder.
  
- Still having issues?
  
  Join our discord and feel free to ask for help. 
  
  [![Discord](https://img.shields.io/discord/738864299392630914.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/UjzuHMU)
   
  

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
