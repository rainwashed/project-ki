from transformers import WhisperProcessor, WhisperForConditionalGeneration
from time import time
from audio_functions import convert_sample_rate, load_file
from pathlib import Path

start_time = time()

processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

print(f"Took {time() - start_time} to load model and processor.")

start_time = time()

data = convert_sample_rate(load_file("src/audio/model_test.wav"), 16000)
features = processor(data, sampling_rate=16000, return_tensors="pt").input_features
tokens = model.generate(features)

output = processor.batch_decode(tokens, skip_special_tokens=True)

print(f"Took {time() - start_time} to complete generation.")
print(output)
print(type(output))
print(str(output[0]).strip())