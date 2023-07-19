import yt_dlp
import os

def download_video(url):
    downloader_options = {
        "format": "best",
        "outtmpl": os.path.join("Downloads", "%(id)s.%(ext)s"),
    }
    downloader = yt_dlp.YoutubeDL(downloader_options)
    info = downloader.extract_info(url, download=False)
    downloader.download([url])
    video_file_path = os.path.join("Downloads", info["id"] + ".mp4")
    video_file = open(video_file_path, "rb")
    return video_file


def download_audio(url):
    downloader_options = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join("Downloads", "%(title)s.%(ext)s"),
    }
    downloader = yt_dlp.YoutubeDL(downloader_options)
    info = downloader.extract_info(url, download=False)
    downloader.download([url])
    audio_file_path = os.path.join("Downloads", info["title"] + ".webm")
    audio_file = open(audio_file_path, "rb")
    return audio_file

         
    
    