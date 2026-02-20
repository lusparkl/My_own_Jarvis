from models.transcriber import build_transcriber
from models.tts import build_tts
from models.wake import build_wake
import ollama
import config
import logging

logger = logging.getLogger(__name__)

def load_models() -> list:
    logger.info("Loading models, might take some time")
    transcriber_model = build_transcriber()
    wake_model = build_wake()
    tts_model = build_tts()
    ollama.generate(model=config.GPT_MODEL, prompt="responce with just '1'", keep_alive=-1) # Starting ollama server, that will run till turn pc off(keep_alive=-1)

    return [transcriber_model, wake_model, tts_model]
