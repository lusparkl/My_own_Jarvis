import queue
from typing import Iterable
import numpy as np

def tts_stream_audio_chunks(
    tts,
    text_chunks: Iterable[str],
    out_q: queue.Queue,
    speaker: str = "Jarvis",
    language: str = "en",
) -> None:
    # Producer: text chunks -> audio chunks
    for chunk in text_chunks:
        wav = tts.tts(text=chunk, speaker=speaker, language=language)
        wav = np.asarray(wav, dtype=np.float32)
        out_q.put(wav)

    out_q.put(None)
    




