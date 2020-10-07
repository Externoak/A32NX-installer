from datetime import datetime, timezone
import math
import os
from pathlib import Path
import re
import threading
import tkinter
from PIL.ImageTk import PhotoImage
from hurry.filesize import size
from tkinter.ttk import *
from tkinter import filedialog, ttk
import requests
import tqdm
import zipfile
import sys
import json

master_prerelease_url = 'https://api.github.com/repos/flybywiresim/a32nx/releases/tags/vmaster'
latest_release_url = 'https://api.github.com/repos/flybywiresim/a32nx/releases/latest'
asset_json_name = 'asset.json'


class Request:

    cancel_check = False

    @staticmethod
    def get(url: str):
        response = requests.get(url)
        return response

    @staticmethod
    def download_file(url: str, file_name: str, progress_bar: Progressbar, response_status: ttk.Label, stable: bool):
        Request.cancel_check = False
        if stable:
            download_message = f"Downloading stable version..."
        else:
            download_message = f"Downloading development version..."
        chunk_size = 16384
        req = requests.get(url, stream=True, allow_redirects=False, headers={'Accept-Encoding': None})
        if req.status_code == 200:
            try:
                progress_bar.pack(side="top", pady=(40, 0))
                progress_bar['value'] = 0
                file_size = int(req.headers['Content-Length'])
                num_bars = int(file_size / chunk_size)
                pbar_percentage = tqdm.tqdm(total=int(file_size), bar_format='{percentage}')
                with open(f'{sys.prefix}/{file_name}', 'wb') as fp:
                    response_status['text'] = download_message
                    for chunk in tqdm.tqdm(req.iter_content(chunk_size=chunk_size), total=num_bars, unit='B', desc=f'{sys.prefix}/{file_name}', disable=True):
                        fp.write(chunk)
                        pbar_percentage.update(len(chunk))
                        current_percentage = math.ceil(float(str(pbar_percentage)))
                        progress_bar['value'] = current_percentage
                        style.configure('text.Horizontal.TProgressbar', text=f'{current_percentage} %')
                        progress_bar.update()
                        if Request.cancel_check:
                            fp.close()
                            break
                progress_bar.pack_forget()
            except KeyError:
                progress_bar.pack_forget()
                total_chunk_downloaded = 0
                with open(f'{sys.prefix}/{file_name}', 'wb') as fp:
                    for chunk in req.iter_content(chunk_size=chunk_size):
                        total_chunk_downloaded = total_chunk_downloaded + chunk_size
                        response_status['text'] = f"{download_message} {size(total_chunk_downloaded)}b!"
                        fp.write(chunk)
                        progress_bar.update()
                        if Request.cancel_check:
                            fp.close()
                            break
                response_status['text'] = ""
        elif req.status_code == 302:
            Request.download_file(url=req.headers['location'], file_name=file_name, progress_bar=progress_bar, response_status=response_status, stable=stable)
        else:
            response_status['text'] = f"Error when downloading, response code:{req.status_code}"
            response_status['background'] = "red"
        response_status['text'] = ""
        progress_bar.pack_forget()

    @staticmethod
    def update_cancel():
        Request.cancel_check = True


class Application(ttk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.change_folder = True
        self.original_background = ""
        self.Artwork = ttk.Label(image="", borderwidth=0)
        self.photo = PhotoImage(file=f"{sys.prefix}/Image.pbm")
        self.Artwork['image'] = self.photo
        self.Artwork.photo = self.photo
        self.Artwork.pack()
        self.response_status = ttk.Label(text="Welcome to A32NX Mod Downloader & Installer!", wraplength=400, background="#1B1B1B", foreground="white")
        self.response_status.pack(side="top", fill=tkinter.X)
        self.filler_label = ttk.Label(text="", background="#1B1B1B")
        self.filler_label.pack(side="top", fill=tkinter.X)
        self.destination_folder_msg = ttk.Label(text="", background="#1B1B1B", wraplength=400)
        self.destination_folder_msg.pack(side="top", fill=tkinter.X)
        self.progress_bar = ttk.Progressbar(self, style='text.Horizontal.TProgressbar', orient="horizontal", length=200, mode="determinate")
        self.download_dev_btn = ttk.Button(self, text="Development version", width=20, style='W1.TButton', command=self.download_dev)
        self.download_stable_btn = ttk.Button(self, width=20, text="Stable version", style='W2.TButton', command=self.download_stable)
        self.browse_button = ttk.Button(self, text="", width=30, style='W3.TButton', command=self.browse_search)
        self.exit = ttk.Button(self, text="Exit", style='W4.TButton', command=self.master.destroy)
        self.exit.pack(side="bottom", pady=(30, 0), padx=(184, 184))
        self.filler_label2 = ttk.Label(text="", background="#1B1B1B")
        self.filler_label2.pack(side="bottom", fill=tkinter.X)
        self.cancel = ttk.Button(self, text="Cancel", style='W5.TButton', command=Request.update_cancel)
        root.bind_class("TButton", "<Enter>", self.on_enter)
        root.bind_class("TButton", "<Leave>", self.on_leave)
        try:
            user_cfg_path = None
            try:
                for path in Path(Path(os.environ['APPDATA']).parent).rglob('UserCfg.opt'):
                    if "Flight" in str(path) and str(path).endswith('UserCfg.opt'):
                        user_cfg_path = path
                        break
            except FileNotFoundError:
                pass
            if not user_cfg_path:
                raise IOError
            file_data = open(user_cfg_path, 'r')
            for row in file_data:
                if "InstalledPackagesPath" in row:
                    found_installation_path = row.split('InstalledPackagesPath')[1].lstrip().rstrip().strip('"')
                    self.destination_folder = f'{found_installation_path}\\Community'
                    self.destination_folder_msg['text'] = found_installation_path
            self.browse_button['text'] = "Change destination folder"
            self.browse_button.pack(side="top", pady=(20, 0))
            self.browse_search()
            file_data.close()
        except IOError:
            self.destination_folder = ""
            self.response_status['text'] = "Welcome to A32NX Mod Downloader & Installer. Could not automatically detect Community folder, please select it manually!"
            self.browse_button['text'] = "Select Community folder"
            self.browse_button.pack(side="top", pady=(20, 0))
        self.final_file_path = ""
        self.master = master
        master.title('FlyByWire Downloader')
        self.pack(after=self.exit.pack(side="bottom", pady=(20, 0), padx=(184, 184)))

    def get_asset_json_path(self):
        return Path(f'{self.destination_folder}\\A32NX\\{asset_json_name}')

    def browse_search(self):
        self.response_status['background'] = ""
        self.response_status.pack(side="top", fill=tkinter.X)
        if not self.change_folder or not self.destination_folder:
            self.destination_folder = filedialog.askdirectory()
        if self.destination_folder:
            self.check_if_update_available()
            self.download_dev_btn.pack(side="left", pady=(20, 0), padx=(20, 0))
            self.download_stable_btn.pack(side="right", pady=(20, 0), padx=(0, 20))
            msg = f'Destination folder: {self.destination_folder}'
            self.browse_button['text'] = "Change destination folder"
            self.browse_button.pack(side="top", pady=(20, 0))
            self.change_folder = False
        else:
            self.filler_label['text'] = ""
            self.filler_label['background'] = "#1B1B1B"
            self.download_dev_btn.pack_forget()
            self.download_stable_btn.pack_forget()
            msg = 'Please select an installation folder.'
            self.browse_button['text'] = "Select Community folder"
            self.change_folder = True
            self.browse_button.pack(side="top", pady=(20, 0))
        self.destination_folder_msg['text'] = msg
        self.destination_folder_msg.pack(side="top", fill=tkinter.X)
        ttk.Label(root, text="name")

    def download_zip(self, specific_url: str, stable: bool = True):
        if self.destination_folder:
            response = Request.get(specific_url)
            if response.status_code == 200:
                self.filler_label['text'] = ""
                self.filler_label['background'] = "#1B1B1B"
                self.browse_button.pack_forget()
                self.download_dev_btn.pack_forget()
                self.download_stable_btn.pack_forget()
                self.cancel.pack(side="bottom", pady=(20, 0), padx=(184, 184))
                self.exit.pack_forget()
                download_url = response.json()["assets"][0]["browser_download_url"]
                file_name = download_url.split("/")[-1]
                threading.Thread(target=Request.download_file(url=download_url, file_name=file_name, progress_bar=self.progress_bar, response_status=self.response_status, stable=stable)).start()
                if not self.response_status['text'] and not Request.cancel_check:
                    self.response_status['text'] = "Unzipping file..."
                    threading.Thread(target=self.unzip_file(file_name=file_name)).start()
                elif Request.cancel_check:
                    self.response_status['text'] = f"Download cancelled!"
                    self.exit.pack(side="bottom", pady=(20, 0), padx=(184, 184))
                    self.cancel.pack_forget()
                    self.browse_button.pack(side="top", pady=(20, 0))
                    self.download_dev_btn.pack(side="left", pady=(20, 0), padx=(20, 0))
                    self.download_stable_btn.pack(side="right", pady=(20, 0), padx=(0, 20))
            else:
                self.response_status['text'] = f"Error when downloading, response code: {response.status_code}"
                self.response_status['background'] = "red"

    def download_stable(self):
        self.download_zip(specific_url=latest_release_url)

    def download_dev(self):
        self.download_zip(specific_url=master_prerelease_url, stable=False)

    def check_if_update_available(self):
        try:
            layout_path = Path(f'{self.destination_folder}\\A32NX\\layout.json')
            if layout_path.is_file():
                layout_data = open(layout_path, 'r').read()
                clean_data_length = len(re.sub('\\s\\n', '\\n', layout_data))
                current_data_timestamp = Application.convert_from(int(re.search('"date":\\s(\\d+)', layout_data).group(1)))
                latest_release_version = Request.get(latest_release_url).json()
                tag_name = latest_release_version['tag_name']
                stable_published_at = latest_release_version['published_at']
                stable_len = int(Request.get(f'https://api.github.com/repos/flybywiresim/a32nx/contents/A32NX/layout.json?ref={tag_name}').json()['size'])
                if stable_len == clean_data_length:
                    self.filler_label['text'] = "Stable version is up to date!"
                    self.filler_label['background'] = "green"
                    return
                elif current_data_timestamp < stable_published_at:
                    self.filler_label['text'] = "Stable version is out of date, please consider updating!"
                    self.filler_label['background'] = "orange"
                elif current_data_timestamp > stable_published_at:
                    if self.get_asset_json_path().is_file():
                        with open(self.get_asset_json_path()) as file:
                            asset_data = json.load(file)
                            local_asset_id = asset_data['id']
                            latest_master_asset_id = Request.get(master_prerelease_url).json()['assets'][0]['id']
                            if local_asset_id == latest_master_asset_id:
                                self.filler_label['text'] = "Dev version is up to date!"
                                self.filler_label['background'] = "green"
                            else:
                                self.filler_label['text'] = "Dev version is out of date, please consider updating!"
                                self.filler_label['background'] = "orange"
                    else:
                        self.filler_label['text'] = "Dev version is out of date, please consider updating!"
                        self.filler_label['background'] = "orange"

        except KeyError:
            self.filler_label['text'] = "Could not check for updates! Github API rate limit could be exceeded."
            self.filler_label['background'] = "orange"
        except AttributeError:
            self.filler_label['text'] = "Could not check for updates! layout.json could have a wrong structure."
            self.filler_label['background'] = "orange"

    @staticmethod
    def convert_from(windows_timestamp: int) -> str:
        unix_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        epoch_delta = unix_epoch - windows_epoch
        windows_timestamp_in_seconds = windows_timestamp / 10_000_000
        unix_timestamp = windows_timestamp_in_seconds - epoch_delta.total_seconds()
        return datetime.utcfromtimestamp(unix_timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')

    def unzip_file(self, file_name: str):
        try:
            archive = zipfile.ZipFile(f'{sys.prefix}/{file_name}')
            for file in archive.namelist():
                if not os.path.isdir(file):
                    archive.extract(file, path=self.destination_folder)
            archive.close()
            latest_master_asset = Request.get(master_prerelease_url).json()['assets'][0]
            with open(self.get_asset_json_path(), 'w', encoding='utf-8') as f:
                # Store asset.json in A32NX folder so we can check it later to see if it is still up to date
                json.dump(latest_master_asset, f, ensure_ascii=False, indent=4)
            self.response_status['background'] = "green"
            self.response_status['text'] = "A32NX correctly installed, everything should be good to go!"
        except (zipfile.BadZipfile, OSError, KeyError):
            self.response_status['background'] = "red"
            self.response_status['text'] = "Folder could not be unzipped, failed!"
        self.exit.pack(side="bottom", pady=(20, 0), padx=(184, 184))
        self.cancel.pack_forget()
        self.pack()

    def on_enter(self, e):
        self.original_background = ttk.Style().configure(e.widget['style'])['background']
        ttk.Style().configure(e.widget['style'], background="#506164")

    def on_leave(self, e):
        ttk.Style().configure(e.widget['style'], background=self.original_background)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.resizable(False, False)
    root.iconbitmap(default=f"{sys.prefix}/icon.ico")
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(root, background='#1B1B1B')
    style.configure(root, foreground='white')
    ttk.Style().configure('W1.TButton', background="#6399AE")
    ttk.Style().configure('W2.TButton', background="#00C2CB")
    ttk.Style().configure('W3.TButton', background="#545454")
    ttk.Style().configure('W4.TButton', background="#545454")
    ttk.Style().configure('W5.TButton', background="#545454")
    style.layout('text.Horizontal.TProgressbar',
                 [('Horizontal.Progressbar.trough',
                   {'children': [('Horizontal.Progressbar.pbar',
                                  {'side': 'left', 'sticky': 'ns'})],
                    'sticky': 'nswe'}),
                  ('Horizontal.Progressbar.label', {'sticky': ''})])
    style.configure('text.Horizontal.TProgressbar', text='0 %')
    style.configure('text.Horizontal.TProgressbar', background='green')
    app = Application(master=root)
    app.mainloop()
