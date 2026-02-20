from services.transcribe import start_transcribing
from services.llm import get_llm_responce
from services.memory import save_chat
from services.play_responce import dub_and_play_responce
import config
import logging

logger = logging.getLogger(__name__)

def run_new_chat(transcribing_model, tts):
    messages = [{"role":"system", "content":config.SYSTEM_PROMT}]
    logger.info("Started new chat")
    while True:
        transcribtion = start_transcribing(transcribing_model)
        
        if not transcribtion:
            break
        
        logger.info("Transcribed user promt, working on it")
        messages.append({"role": "user", "content": transcribtion})
        llm_responce = get_llm_responce(messages)

        logger.info("Got LLM responce, streaming it.")
        dub_and_play_responce(tts, llm_responce)

    if len(messages) > 1:
        logger.info("Succesfully ended and saved the chat")
        save_chat(messages)
