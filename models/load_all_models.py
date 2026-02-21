from models.load_transcribtion_model import build_transcriber
from models.load_tts_model import build_tts
from models.load_wakeword_model import build_wake
from models.load_ollama_model import start_ollama_model
import logging

logger = logging.getLogger(__name__)

def load_models() -> list:
    logger.info("Loading models, might take some time")
    transcriber_model = build_transcriber()
    wake_model = build_wake()
    tts_model = build_tts()
    start_ollama_model()
    
    return [transcriber_model, wake_model, tts_model]
