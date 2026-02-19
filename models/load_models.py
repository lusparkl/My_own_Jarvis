from models.transcriber import build_transcriber
from models.tts import build_tts
from models.wake import build_wake
import logging

logger = logging.getLogger(__name__)

def load_models() -> list:
    transcriber_model = build_transcriber()
    wake_model = build_wake()
    tts_model, tts_gpt_cond_latent, tts_speaker_embedding = build_tts()

    return [transcriber_model, wake_model, [tts_model, tts_gpt_cond_latent, tts_speaker_embedding]]
