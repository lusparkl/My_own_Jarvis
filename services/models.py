from faster_whisper import WhisperModel
from openwakeword.model import Model
from config import (WAKE_WORD_MODEL_PATH, WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE)

def build_wake_model() -> Model:
    return Model(wakeword_models=[WAKE_WORD_MODEL_PATH])

def build_transcriber() -> WhisperModel:
    return WhisperModel(
        WHISPER_MODEL, WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE
    )