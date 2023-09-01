from transformers import WhisperProcessor, TFWhisperForConditionalGeneration

whisper_processor = WhisperProcessor.from_pretrained(
    "openai/whisper-medium.en")
whisper_model = TFWhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-medium.en")

whisper_processor.save_pretrained("./src/models/whisper-medium.en")
whisper_model.save_pretrained("./src/models/whisper-medium.en")
