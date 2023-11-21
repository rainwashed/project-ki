# https://realpython.com/playing-and-recording-sound-python/#recording-audio

import pyaudio
import wave
from time import sleep
from pynput import keyboard

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 44100 samples per second
filename = "src/cache/record.wav"

seconds = 3

def start_recording(seconds: int = 3):
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

    for _ in range(int(fs / chunk * seconds)):
        data = stream.read(chunk)
        audioFrames.append(data)

    stream.stop_stream()
    stream.close()

    p.terminate()

    print("finished recording; writing files")

    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(audioFrames))
    wf.close()

    print("wrote file")


def open_record_loop(callback):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
        start=False
    )
    audioFrames = []

    print("[!] - Ready to start recording")

    def onPress(key):
        global spaceIsDown
        global recordedSomething

        if key == keyboard.Key.space:
            print("[*] - Space is pressed down, beginning to capture audio.", end="\r")
            stream.start_stream()
            data = stream.read(chunk)
            audioFrames.append(data)


    def onRelease(key):
        print("{} should have been released".format(key))
        if key == keyboard.Key.space:
            print("[*] - Space is released, stop capturing audio and write to file.", end="\r")
            stream.stop_stream()
            stream.close()
            p.terminate()

            print("[*] - Writing data to a file")
            wf = wave.open(filename, "wb")
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(audioFrames))
            wf.close()

            listener.stop()
            callback()
            return False

    with keyboard.Listener(
        on_press=onPress,
        on_release=onRelease
    ) as listener:
        listener.join()