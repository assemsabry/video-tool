import os
import sys
import tkinter as tk
from tkinter import filedialog
from yt_dlp import YoutubeDL

def get_download_path():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select download folder")
    return folder_selected

def is_youtube_link(url):
    return "youtube.com" in url or "youtu.be" in url

def get_video_info(url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info

def show_formats(formats):
    filtered = [f for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
    filtered.sort(key=lambda x: int(x.get('height', 0)), reverse=True)
    print("\nAvailable formats:")
    for idx, f in enumerate(filtered):
        resolution = f.get('resolution') or f"{f.get('height', 'N/A')}p"
        size = round(f['filesize'] / (1024 * 1024), 2) if f.get('filesize') else '?'
        print(f"{idx + 1}. {f['format']} - {f['ext']} - {resolution} - {size} MB")
    return filtered

def download_video(url, download_path, format_id=None):
    ydl_opts = {
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
    }
    if format_id:
        ydl_opts['format'] = format_id

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    url = input("Enter the video URL: ").strip()
    download_path = get_download_path()

    if not url or not download_path:
        print("Missing URL or download path.")
        sys.exit()

    if is_youtube_link(url):
        info = get_video_info(url)
        print(f"\nTitle: {info['title']}")
        formats = show_formats(info['formats'])

        choice = input("\nEnter the number of the quality to download: ").strip()
        try:
            selected_format = formats[int(choice) - 1]
            format_id = selected_format['format_id']
            download_video(url, download_path, format_id)
        except:
            print("Invalid choice.")
    else:
        print("Downloading from a non-YouTube source...")
        download_video(url, download_path)

if __name__ == "__main__":
    main()
