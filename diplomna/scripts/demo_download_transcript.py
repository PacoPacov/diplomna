from youtube_transcript_api import YouTubeTranscriptApi
import json
import os


if __name__ == "__main__":
    transcript_list = YouTubeTranscriptApi.list_transcripts("855Am6ovK7s", 'en')

    auto_generated_trans = []

    for trans in transcript_list:
        print(trans.language, trans.is_generated)
        if trans.is_generated:
            auto_generated_trans.append(trans.fetch())

    if auto_generated_trans:
        output_path = os.path.join(os.path.dirname(__file__), '855Am6ovK7s_en_transcript.json')
        print(output_path)
        with open(output_path, 'w') as f:
            json.dump(auto_generated_trans[0], f, indent=4)
