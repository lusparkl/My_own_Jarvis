import numpy as np
import sounddevice as sd
from audio.input.audio_callbacks import t_audio_callback, t_audio_q
from audio.utils import capture_silence
from config import (SAMPLE_RATE_HZ, BLOCK_SEC, WINDOW_SEC, STEP_SEC)
from services.stabilize_transcription import stabilize_transcription
import logging


logger = logging.getLogger(__name__)

def start_transcribing(model):
    block_samples = int(SAMPLE_RATE_HZ * BLOCK_SEC)
    window_samples = int(SAMPLE_RATE_HZ * WINDOW_SEC)
    step_samples = int(SAMPLE_RATE_HZ * STEP_SEC)

    rolling = np.zeros(0, dtype=np.float32)
    since_last_decode = 0
    committed_text=""
    st_window=[]

    logger.info("Listening to transcribe...")
    with sd.InputStream(
        samplerate=SAMPLE_RATE_HZ,
        channels=1,
        dtype="float32",
        blocksize=block_samples,
        callback=t_audio_callback
    ):
        while True:
            block = t_audio_q.get()
            rolling = np.concatenate([rolling, block])

            if rolling.size > window_samples:
                rolling = rolling[-window_samples:]
            
            since_last_decode += block.size
            if since_last_decode < step_samples:
                continue
            since_last_decode = 0

            segments, _ = model.transcribe(
                rolling,
                beam_size=1,
                vad_filter=True,
                condition_on_previous_text=False
            )

            new_chunk, committed_text = stabilize_transcription(segments, committed_text, st_window)

            if  capture_silence(st_window):
                pass


