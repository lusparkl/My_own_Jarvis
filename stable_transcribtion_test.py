import numpy as np
import sounddevice as sd
from services.models import build_transcriber
from audio.input.audio_callbacks import t_audio_callback, t_audio_q
from config import (SAMPLE_RATE_HZ, BLOCK_SEC, WINDOW_SEC, STEP_SEC)
import logging

logger = logging.getLogger(__name__)

def common_prefix_len(a, b, c) -> int:
    common_len = 0
    for w0, w1, w2 in zip(a, b, c):
        if w0 == w1 == w2:
            common_len += 1
        else: break
    return common_len

def transcribe():
    block_samples = int(SAMPLE_RATE_HZ * BLOCK_SEC)
    window_samples = int(SAMPLE_RATE_HZ * WINDOW_SEC)
    step_samples = int(SAMPLE_RATE_HZ * STEP_SEC)
    model = build_transcriber()

    rolling = np.zeros(0, dtype=np.float32)
    since_last_decode = 0
    commited_text = ""

    last_3_blocks = []

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
                condition_on_previous_text=False,
                word_timestamps=True
            )

            step_words = []

            for segment in segments:
                for word in segment.words:
                    step_words.append(word.word.strip().lower())
            
            last_3_blocks.append(step_words)
            if len(last_3_blocks) > 3:
                last_3_blocks = last_3_blocks[-3:]
            
            if len(last_3_blocks) < 3:
                continue

            common_len = common_prefix_len(last_3_blocks[0], last_3_blocks[1], last_3_blocks[2])
            stable_text = " ".join(last_3_blocks[0][:common_len]).strip()

            if not stable_text or stable_text == commited_text:
                continue

            if stable_text.startswith(commited_text):
                new_part = stable_text[len(commited_text):].strip()
                if new_part:
                    print(new_part)
                else:
                    print(stable_text)
                
                commited_text = stable_text
            else:
                print(stable_text)
                commited_text = stable_text                       

                
transcribe()