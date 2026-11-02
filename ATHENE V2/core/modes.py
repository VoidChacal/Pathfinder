# core/modes.py
from enum import Enum

class Mode(Enum):
    IDLE = "idle"
    SERVER = "server"
    PROCESSING = "processing"
    WARNING = "warning"
    ALERT = "alert"
    SPEAKING = "speaking"