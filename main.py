
from faster_whisper import WhisperModel
import numpy as np
import sounddevice as sd
from queue import Queue

FS = 16000
BLOCK_SEC=1
WINDOW_SEC=3
STEP_SEC = 3

model = WhisperModel("distil-large-v3", device="cuda", compute_type="int8_float16")
audio_q = Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_q.put(indata[:, 0].copy())


def main():
    block_samples = int(FS * BLOCK_SEC)
    window_samples = int(FS * WINDOW_SEC)
    step_samples = int(FS * STEP_SEC)

    rolling = np.zeros(0, dtype=np.float32)
    since_last_decode = 0
    last_printed = ""

    print("Listening...")
    with sd.InputStream(
        samplerate=FS,
        channels=1,
        dtype="float32",
        blocksize=block_samples,
        callback=audio_callback
    ):
        while True:
            block = audio_q.get()
            rolling = np.concatenate([rolling, block])

            if rolling.size > window_samples:
                rolling = rolling[-window_samples:]
            
            since_last_decode += block.size
            if since_last_decode < step_samples:
                continue
            since_last_decode = 0

            segments, info = model.transcribe(
                rolling,
                beam_size=1,
                vad_filter=True,
                condition_on_previous_text=False
            )

            text = " ".join(seg.text.strip() for seg in segments).strip()
            if text and text != last_printed:
                print(text)
                last_printed=text

main()
