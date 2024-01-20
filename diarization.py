import whisper
import datetime
import os
import subprocess

import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding

from pyannote.audio import Audio
from pyannote.core import Segment

import wave
import contextlib

from sklearn.cluster import AgglomerativeClustering
import numpy as np

from audio_extract import extract_audio


# videoFile - переменная берется из video_analyse.py далее превращается в audio.wav и далее работа идет с этим файлом

# convert_video = os.VIDEO_PATH.join(VIDEO_PATH, videoFile.name)
def path_for_audio(path,video_file):
    convert_video = os.path.join(path, video_file)
    extract_audio(input_path=convert_video, output_path="./audio.wav", output_format='wav', overwrite=True)
    pass

def time(secs):
    return datetime.timedelta(seconds=round(secs))

def dz_result(audio_wav):

    num_speakers = 2 #@param {type:"integer"}

    language = 'any' #@param ['any', 'English']

    model_size = 'large' #@param ['tiny', 'base', 'small', 'medium', 'large']


    model_name = model_size
    if language == 'English' and model_size != 'large':
        model_name += '.en'

    embedding_model = PretrainedSpeakerEmbedding(
        "speechbrain/spkrec-ecapa-voxceleb",
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    
    # if path[-3:] != 'wav':
    #     subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
    path = 'audio.wav'

    model = whisper.load_model(model_size)

    result = model.transcribe(path)
    segments = result["segments"]

    with contextlib.closing(wave.open(path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

        def segment_embedding(segment):
            start = segment["start"]
            # Whisper overshoots the end timestamp in the last segment
            end = min(duration, segment["end"])
            clip = Segment(start, end)
            waveform, sample_rate = audio.crop(path, clip)
            return embedding_model(waveform[None])
    
    audio = Audio()

    embeddings = np.zeros(shape=(len(segments), 192))
    # for i, segment in enumerate(segments):
    #     embeddings[i] = segment_embedding(segment)
    #     embeddings = np.nan_to_num(embeddings)

    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
        segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

    f = open("transcript.txt", "w")

    for (i, segment) in enumerate(segments):
        if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
            f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
        f.write(segment["text"][1:] + ' ')
    f.close()