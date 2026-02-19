import logging
import numpy as np
import sounddevice as sd
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from services.models import build_transcriber
from services.stabilize_transcription import stabilize_transcription
from audio.input.audio_callbacks import t_audio_callback, t_audio_q
from config import SAMPLE_RATE_HZ, BLOCK_SEC, WINDOW_SEC, STEP_SEC, LOG_LEVEL

logger = logging.getLogger(__name__)


def run_showcase():
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.getLogger("faster_whisper").setLevel(logging.WARNING)

    block_samples = int(SAMPLE_RATE_HZ * BLOCK_SEC)
    window_samples = int(SAMPLE_RATE_HZ * WINDOW_SEC)
    step_samples = int(SAMPLE_RATE_HZ * STEP_SEC)

    model = build_transcriber()
    rolling = np.zeros(0, dtype=np.float32)
    since_last_decode = 0
    committed_text = ""
    st_window = []
    shown_text = ""

    logger.info("Showcase started")

    panel = Panel(Text("Listening..."), title="Jarvis Showcase", border_style="cyan")
    with Live(panel, refresh_per_second=10) as live:
        with sd.InputStream(
            samplerate=SAMPLE_RATE_HZ,
            channels=1,
            dtype="float32",
            blocksize=block_samples,
            callback=t_audio_callback,
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
                    word_timestamps=True,
                )

                new_chunk, committed_text = stabilize_transcription(
                    segments,
                    committed_text,
                    st_window,
                )

                if not new_chunk:
                    continue

                shown_text = f"{shown_text} {new_chunk}".strip()
                body = Text()
                body.append(shown_text, style="bold white")
                live.update(Panel(body, title="You", border_style="green"))


if __name__ == "__main__":
    run_showcase()