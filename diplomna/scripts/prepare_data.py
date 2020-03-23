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
            annotated_file = os.path.join(DATASET_FOLDER, 'annotated_transcripts', record['file_name'])
            transcript_file = os.path.join(DATASET_FOLDER, 'transcripts')
            print('********** Create transcript **********')
            record['transcript_file'] = combine_claims_into_transcript(annotated_file, transcript_file)

            try:
                audio_file = os.path.join(DATASET_FOLDER, 'audios', record['file_name'].replace('.csv', '.wav'))
                print('********** Download Audio **********')
                record['audio_file'] = download_audio(record['annotation_url'], audio_file)
            except DownloadError as e:
                print("********** Download error: ", e)
            except RuntimeError as e:
                print("********** Runtime error: {}".format(e))

            if record.get('audio_file') and record.get('transcript_file'):
                aligned_transcript = os.path.join(output_path, record['file_name'].replace('.csv', '.json'))
                print('********** Align transcript **********')
                align_transcript(record['audio_file'], record['transcript_file'], aligned_transcript)
