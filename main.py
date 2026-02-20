from services.wake import wait_for_wake_word
from services.run_chat import run_new_chat
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
    transcriber_model, wake_model, tts_model = load_models()
    logger.info("Assistant Started")
    while True:
        wait_for_wake_word(wake_model)
        run_new_chat(transcriber_model, tts_model)

if __name__ == "__main__":
    setup_logging()
    run_assistant()

