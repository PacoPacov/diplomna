import os

import youtube_dl


def download_audio(audio_file, audio_url):
    """
    Download audio of youtube video:
    :param audio_file: Name and path where to save the audio of youtube video
    :param audio_url: Video url.

    Example:
    download_audio("Democratic Presidential Debate - June 26.mp3", "https://www.youtube.com/watch?v=vJ6MrDO0kgY")

    OUT: /path/to/mp3/Democratic Presidential Debate - June 26.mp3
    """
    os.makedirs(os.path.dirname(audio_file), exist_ok=True)

    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'outtmpl': audio_file}) as ydl:
        ydl.download([audio_url])

    return audio_file
