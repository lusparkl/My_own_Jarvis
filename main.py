from services.transcribe import start_transcribing
from services.wake import wait_for_wake_word
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
    logger.info("Assistant Started")
    wait_for_wake_word() # Will end only when hear "Hey Jarvis"
    start_transcribing()

if __name__ == "__main__":
    setup_logging()
    run_assistant()

