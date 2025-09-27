from .wake import Wake
from .funasr import FunASR, FunASRLocal
from .realtime import Realtime
from utils import Config
from utils.task import TaskManager

mode = Config.get("ASR", "").get("mode", "wake")
player_mode = Config.get("Player", "").get("mode", "local")


def ASR(socketio, tasks: TaskManager):
    funasr: FunASR
    if player_mode == "local":
        funasr = FunASRLocal()
    else:
        funasr = FunASR(socketio)
    
    if mode == "wake":
        return Wake(socketio, tasks, funasr)
    elif mode == "realtime":
        return Realtime(socketio, tasks, funasr)
    else:
        raise ValueError(f"Invalid ASR mode: {mode}")
