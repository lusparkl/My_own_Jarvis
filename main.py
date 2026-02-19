from services.transcribe import start_transcribing
from services.wake import wait_for_wake_word
from models.load_models import load_models
from config import LOG_LEVEL
import logging

def setup_logging():
    logging.basicConfig(level=LOG_LEVEL,
                        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                        datefmt="%H:%M:%S"
                        )
    logging.getLogger("faster_whisper").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def run_assistant():
    logger.info("Loading all models..")
    transcriber_model, wake_model, [tts_model, tts_gpt_cond_latent, tts_speaker_embedding] = load_models()
    logger.info("Assistant Started")
    wait_for_wake_word(wake_model) # Will end only when hear "Hey Jarvis"
    start_transcribing(transcriber_model)

if __name__ == "__main__":
    setup_logging()
    run_assistant()

