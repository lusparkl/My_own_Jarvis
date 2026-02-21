from openwakeword.model import Model
import config

def build_wake() -> Model:
    return Model(wakeword_models=[config.WAKE_WORD_MODEL_PATH])