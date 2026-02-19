# tts_stream_cached.py
import os
import time
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from config import (CHECKPOINT_DIR, REFERENCE_WAVS, LANGUAGE, USE_DEEPSPEED, XTTS_CONFIG_JSON, OUTPUT_WAV, LATENTS_CACHE, XTTS_DEVICE)



""" 
chunks = model.inference_stream(
    "hello world",
    LANGUAGE,
    gpt_cond_latent,
    speaker_embedding,
)

wav_chunks = []
for i, chunk in enumerate(chunks):
    wav_chunks.append(chunk) """
