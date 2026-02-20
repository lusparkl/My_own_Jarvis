import queue
import numpy as np
import sounddevice as sd

def play_streamed_audio_chunks_outputstream(
    in_q: queue.Queue,
    sample_rate: int = 24000,
) -> None:
    with sd.OutputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        latency="low",
    ) as stream:
        while True:

            item = in_q.get()

            if item is None:
                break

            audio = np.asarray(item, dtype=np.float32)

            if audio.ndim == 1:
                audio = audio[:, None]
            elif audio.ndim == 2 and audio.shape[1] != 1:
                audio = audio.mean(axis=1, keepdims=True)

            stream.write(audio)
