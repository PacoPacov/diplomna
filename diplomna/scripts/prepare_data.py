import csv
import os

from utils import combine_claims_into_transcript, download_audio, align_transcript
from youtube_dl.utils import DownloadError


if __name__ == "__main__":
    DATASET_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dataset')

    # load annotation file
    data = []
    with open(os.path.join(DATASET_FOLDER, 'annotation_file.txt')) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            data.append(row)

    print("Loaded data with size:", len(data))

    output_path = os.path.join(DATASET_FOLDER, 'aligned_files')
    for record in data:
        if 'youtube' in record['annotation_url'] and record['timestamp'] not in ['20160311', '20160303', '20150805']:
            print('Create transcript')
            record['transcript_file'] = combine_claims_into_transcript(os.path.join(DATASET_FOLDER,
                                                                                    'annotated_transcripts',
                                                                                    record['file_name']),
                                                                       os.path.join(DATASET_FOLDER, 'transcripts'))

            try:
                print('Download Audio')
                record['audio_file'] = download_audio(record['annotation_url'],
                                                      os.path.join(DATASET_FOLDER, 'audios',
                                                                   record['file_name'].replace('.csv', '.mp3')))
            except DownloadError as e:
                print("Download error", e)
            except RuntimeError as e:
                print("RuntimeError {}".format(e))

            print('Align transcript')
            align_transcript(record['audio_file'], record['transcript_file'], output_path)
