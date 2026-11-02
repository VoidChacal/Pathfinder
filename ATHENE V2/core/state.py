# core/state.py
import time
from core.modes import Mode
from core.topics import Topics

class AtheneState:
    def __init__(self):
        self.current_mode = Mode.IDLE
        self.alert_lock = False
        self.network_monitor_active = True
        self.last_mode_change = time.time()

class AtheneStateManager:
    def __init__(self, event_bus):
        self.state = AtheneState()
        self.bus = event_bus

    @property
    def mode(self) -> Mode:
        return self.state.current_mode

    def set_mode(self, mode: Mode):
        if self.state.current_mode == mode:
            return
        self.state.current_mode = mode
        self.state.last_mode_change = time.time()
        self.bus.publish(Topics.STATE_CHANGED, mode)