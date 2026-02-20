from TTS.api import TTS
import config

def build_tts():
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(config.XTTS_DEVICE)