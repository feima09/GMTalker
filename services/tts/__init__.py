from .gptsovits import GPTSoVits
from utils import Config


def TTS():
    mode = Config.get("TTS", "").get("mode", "gptsovits")
    
    if mode == "gptsovits":
        return GPTSoVits()
    else:
        raise ValueError(f"Invalid TTS type: {mode}")
