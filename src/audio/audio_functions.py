import soundfile
import librosa
import numpy as np

def load_file(path: str) -> soundfile.SoundFile:
    return soundfile.SoundFile(path)

def convert_sample_rate(audio: soundfile.SoundFile, sr: int) -> np.ndarray:
    data, sr = librosa.load(audio, sr=16000)
    return data

def write_file(audio: np.ndarray, sr: int, path: str):
    soundfile.write(path, audio, sr)
