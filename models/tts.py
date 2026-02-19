import os
import torch
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
import config

def build_tts():
    print("Loading XTTS model...")
    config = XttsConfig()
    config.load_json(config.XTTS_CONFIG_JSON)

    model = Xtts.init_from_config(config)
    model.load_checkpoint(config, checkpoint_dir=config.CHECKPOINT_DIR, use_deepspeed=config.USE_DEEPSPEED)
    model.to(torch.device(config.XTTS_DEVICE))
    model.eval()

    if os.path.exists(config.LATENTS_CACHE):
        cache = torch.load(config.LATENTS_CACHE, map_location="cpu")
        gpt_cond_latent = cache["gpt_cond_latent"].to(model.device)
        speaker_embedding = cache["speaker_embedding"].to(model.device)
    else:
        gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=config.REFERENCE_WAVS)

        torch.save(
            {
                "gpt_cond_latent": gpt_cond_latent.detach().cpu(),
                "speaker_embedding": speaker_embedding.detach().cpu(),
            },
            config.LATENTS_CACHE,
        )
        print(f"Saved speaker cache to: {config.LATENTS_CACHE}")
    
    return [model, gpt_cond_latent, speaker_embedding]