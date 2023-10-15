from transformers import AutoProcessor, AutoModel
import soundfile as sf
from server.log_connection import log, LogTypes
from time import time as now_time
from audio.audio_recog import audio_recog

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = AutoModel.from_pretrained("suno/bark-small")

voice_preset="v2/en_speaker_6"

# TODO: Add logging and test function

async def audio_gen(text: str):
    overall_time = now_time()
    start_time = now_time()

    inputs = processor(
        text=[text],
        return_tensors="pt",
        voice_preset=voice_preset
    )

    await log(__file__, f"Took {now_time() - start_time}s to process the text input.")

    start_time = now_time()
    values = model.generate(**inputs, do_sample=True)

    await log(__file__, f"Took {now_time() - start_time}s to generate tokens.")

    start_time = now_time()
    sf.write("src/cache/model_gen.wav", values.cpu().numpy().squeeze(), model.generation_config.sample_rate)

    await log(__file__, f"Took {now_time() - start_time}s to write tokens to audio file.")

    await log(__file__, f"Finished audio gen. in {now_time() - overall_time}s.", LogTypes.success)

# TODO: fix this shit
audio_test_string = "Hello. I am an artificial intelligent model."
async def test_audio_gen() -> bool:
    overall_time = now_time()
    start_time = now_time()

    inputs = processor(
        text=[audio_test_string],
        return_tensors="pt",
        voice_preset=voice_preset
    )

    print("testing audio generation model")

    # await log(__file__, f"Took {now_time() - start_time}s to process the text input.")

    start_time = now_time()
    values = model.generate(**inputs, do_sample=True)

    print("generate input values")

    # await log(__file__, f"Took {now_time() - start_time}s to generate tokens.")

    start_time = now_time()
    sf.write("src/cache/record.wav", values.cpu().numpy().squeeze(), model.generation_config.sample_rate)

    print("wrote file")

    # await log(__file__, f"Took {now_time() - start_time}s to write tokens to audio file.")

    # recognition part
    start_time = now_time()

    recog_string = await audio_recog()

    print("finished recog")

    # await log(__file__, f"Took {now_time() - start_time}s to finish audio recognition. Recognized: '{recog_string}'")

    passed = str(recog_string).lower() in audio_test_string.lower()

    print(recog_string, passed)

    """
    if passed:
        await log(__file__, f"Finished audio gen. test in {now_time() - overall_time}s. Status: passed.", LogTypes.success)
    else:
        await log(__file__, f"Finished audio gen. test in {now_time() - overall_time}s. Status: failed.", LogTypes.warning)
    """
        
    print("finished testing audio generation model")

    return passed