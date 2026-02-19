import sounddevice as sd
from audio.input.audio_callbacks import w_audio_callback, w_audio_q
from config import SAMPLE_RATE_HZ, WAKE_TRESHOLD, WAKE_BLOCK_SEC
import logging

logger = logging.getLogger(__name__)

def wait_for_wake_word(model):
    block_samples = int(SAMPLE_RATE_HZ * WAKE_BLOCK_SEC)

    logger.info("Listening to wake word...")
    with sd.InputStream(
        samplerate=SAMPLE_RATE_HZ,
        channels=1,
        dtype="int16",
        blocksize=block_samples,
        callback=w_audio_callback
    ):
        while True:
            block = w_audio_q.get()
            prediction = model.predict(block)

            if prediction["hey_jarvis_v0.1"] > WAKE_TRESHOLD:
                print("Hooray! You called me!")
                break
            
            logger.debug(prediction)