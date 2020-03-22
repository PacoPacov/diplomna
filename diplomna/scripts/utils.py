import csv
import json
import os
import subprocess

import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi


def download_audio(audio_url, audio_file):
    """
    Download audio of youtube video:
    :param audio_url: Video url.
    :param audio_file: Name and path where to save the audio of youtube video.

    Example:
    download_audio("https://www.youtube.com/watch?v=vJ6MrDO0kgY", "Democratic Presidential Debate - June 26.mp3")

    OUT: /path/to/mp3/Democratic Presidential Debate - June 26.mp3
    """
    os.makedirs(os.path.dirname(audio_file), exist_ok=True)

    with youtube_dl.YoutubeDL({'format': 'bestaudio', 'outtmpl': audio_file}) as ydl:
        ydl.download([audio_url])

    return os.path.abspath(audio_file)


def download_auto_generated_transcript(target_url, output_path):
    """
    Downloads the auto generated transcript that Google creates for YouTube.
    :param target_url: Video url
    :parma output_path: Name and path where to save the transcript in JSON format.

    Example:
    download_auto_generated_transcript("https://www.youtube.com/watch?v=vJ6MrDO0kgY", "Democratic Presidential Debate - June 26.json")
    OUT: /path/to/mp3/Democratic Presidential Debate - June 26.mp3
    """
    url = target_url.replace("https://www.youtube.com/watch?v=", '')
    transcript_list = YouTubeTranscriptApi.list_transcripts(url, 'en')

    auto_generated_transcript = None

    for transcript in transcript_list:
        if transcript.is_generated:
            auto_generated_transcript = transcript.fetch()

    if auto_generated_transcript:
        with open(output_path, 'w') as f:
            json.dump(auto_generated_transcript, f, indent=4)

        return os.path.abspath(output_path)
    else:
        print("Couldn't find english transcript")


def align_transcript(audio_file, transcript_file, output_path):
    """
    To use this method you need to install "Gentle Forced Aligner"
    Also it will be a good think to install ffmpeg!
    :param audio_file: Audio file
    :param transcript_file: Transcript text file
    :param output_path: Output filename. It will be in JSON format
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        subprocess.Popen(["python3", "gentle/align.py", "audiofile {}".format(audio_file),
                          "txtfile {}".format(transcript_file), "--output {}".format(output_path)],
                         stdout=subprocess.PIPE)
    except OSError as e:
        print("Raised OSError: {}".format(e))


def combine_claims_into_transcript(file_path, output_dir):
    input_data = []

    with open(file_path, 'r') as rf:
        csv_reader = csv.DictReader(rf)
        for row in csv_reader:
            input_data.append(row['claim'])

    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.basename(file_path).replace(".csv", ".txt")
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(" ".join(input_data))
