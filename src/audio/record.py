# https://realpython.com/playing-and-recording-sound-python/#recording-audio

import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 44100 samples per second
filename = "src/cache/record.wav"

seconds = 3

p = pyaudio.PyAudio()
stream = p.open(
    format=sample_format,
    channels=channels,
    rate=fs,
    frames_per_buffer=chunk,
    input=True
)

print("starting recording for {}s".format(seconds))

audioFrames = []

for i in range(int(fs / chunk * seconds)):
    data = stream.read(chunk)
    audioFrames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

print("finished recording")

wf = wave.open(filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(audioFrames))
wf.close()
