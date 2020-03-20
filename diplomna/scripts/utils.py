import youtube_dl


def download_audio(audio_file, audio_url):
    """
    Download audio of youtube video
    """
    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'outtmpl': audio_file}) as ydl:
        ydl.download([audio_url])

    return audio_file
