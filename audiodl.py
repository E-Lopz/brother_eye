# audiodl.py
import os
import yt_dlp

AUDIO_DIR = 'audio'
FIXED_FILENAME = 'cursong.mp3'

def download_audio(query: str) -> str:
    os.makedirs(AUDIO_DIR, exist_ok=True)
    output_path = os.path.join(AUDIO_DIR, 'cursong.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100'  # Sample rate (opcional pero recomendable)
        ],
        'prefer_ffmpeg': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])
        return os.path.join(AUDIO_DIR, FIXED_FILENAME)

