SAMPLE_RATE_HZ = 16000

#Wake Word
WAKE_BLOCK_SEC = 2
WAKE_WORD_MODEL_PATH = "D:/tech_stuff/coding/ai_models/openwakeword_models/hey_jarvis_v0.1.tflite"
WAKE_TRESHOLD = 0.5

#Transcribtion
BLOCK_SEC=1
WINDOW_SEC=3
STEP_SEC = 3
WHISPER_MODEL = "D:/tech_stuff/coding/ai_models/huggingface_cache/hub/models--Systran--faster-distil-whisper-large-v3/snapshots/c3058b475261292e64a0412df1d2681c06260fab"
WHISPER_COMPUTE_TYPE = "float16"
WHISPER_DEVICE = "cuda"

#Logging
LOG_LEVEL="INFO"