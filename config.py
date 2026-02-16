SAMPLE_RATE_HZ = 16000

#Wake Word
WAKE_BLOCK_SEC = 2
WAKE_WORD_MODEL_PATH = "D:/tech_stuff/coding/ai_models/openwakeword_models/hey_jarvis_v0.1.tflite"
WAKE_TRESHOLD = 0.5

#Transcribtion
BLOCK_SEC=1
WINDOW_SEC=7
STEP_SEC = 0.5
ENDPOINT_SILENCE_MS=650
WHISPER_MODEL = "D:/tech_stuff/coding/ai_models/huggingface_cache/hub/models--Systran--faster-distil-whisper-large-v3/snapshots/c3058b475261292e64a0412df1d2681c06260fab"
WHISPER_COMPUTE_TYPE = "float16"
WHISPER_DEVICE = "cuda"
TRANSCRIBTION_STAB_WINDOW = 3

#Logging
LOG_LEVEL="INFO"

#LLM
LLM_MAX_TOKENS=96
LLM_TEMPERATURE=0.5
MIN_STABLE_CHARS_FOR_LLM=24
RESTART_SIMILARITY_THRESHOLD=0.88
RESTART_COOLDOWN_MS=450