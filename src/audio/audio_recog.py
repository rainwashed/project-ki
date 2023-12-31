from os import remove as fileRemove
from time import time as now_time
from pathlib import Path
from server.log_connection import LogTypes, log
from audio.audio_functions import convert_sample_rate, load_file
from transformers import WhisperProcessor, WhisperForConditionalGeneration

saveFileName = "record.wav"

async def audio_recog() -> str:
    overall_time = now_time()
    start_time = now_time()

    filePath = f"src/cache/{saveFileName}"
    audioFileExists = Path(filePath).is_file()

    if not audioFileExists:
        raise Exception(f"src/cache/{saveFileName} is not present in the cache folder. Did nothing record?")
    
    processor = WhisperProcessor.from_pretrained("src/models/whisper-base.en-processor")
    model = WhisperForConditionalGeneration.from_pretrained("src/models/whisper-base.en-model")

    await log(__file__, f"Took {now_time() - start_time}s to load processor and model.")

    start_time = now_time()
    data = convert_sample_rate((load_file(filePath)), sr=16000)

    await log(__file__, f"Took {now_time() - start_time}s to load and downsample the audio file.")

    start_time = now_time()
    features = processor(data, sampling_rate=16000, return_tensors="pt").input_features
    tokens = model.generate(features)

    await log(__file__, f"Took {now_time() - start_time}s to process and generate the tokens for the audio file.")

    output = processor.batch_decode(tokens, skip_special_tokens=True)
    stringifiedOutput = str(output[0]).strip()

    await log(__file__, f"Finished audio recog. in {now_time() - overall_time}s. Recognized: '{stringifiedOutput}'", LogTypes.success)

    fileRemove(filePath)

    return stringifiedOutput


# bool = status of ai (true means that test passed)
# int = ms of time it took to generate
async def test_audio_recog() -> (bool, int):
    overall_time = now_time()
    start_time = now_time()

    processor = WhisperProcessor.from_pretrained("src/models/whisper-base.en-processor")
    model = WhisperForConditionalGeneration.from_pretrained("src/models/whisper-base.en-model")

    await log(__file__, f"Took {now_time() - start_time}s to load processor and model.")

    start_time = now_time()
    data = convert_sample_rate((load_file("src/audio/model_test.wav")), 16000)

    await log(__file__, f"Took {now_time() - start_time}s to load and downsample the audio file.")

    start_time = now_time()
    features = processor(data, sampling_rate=16000, return_tensors="pt").input_features
    tokens = model.generate(features)

    await log(__file__, f"Took {now_time() - start_time}s to process and generate the tokens for the audio file.")

    output = processor.batch_decode(tokens, skip_special_tokens=True)
    stringified_output = (str(output[0]).strip()).lower()

    passed: bool = stringified_output == "hello, this is my audio message to be tested with the openai whisper large version 2 model."
    
    await log(__file__, f"Finished audio recog. test in {now_time() - overall_time}s. Status: {passed}", LogTypes.success)

    return (passed, now_time() - overall_time)