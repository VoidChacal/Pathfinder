# core/brain.py
from core.topics import Topics
from core.modes import Mode
import time

class AtheneBrain:
    def __init__(self, event_bus, state_manager, scene):
        self.bus = event_bus
        self.state_manager = state_manager
        self.scene = scene
        
        self.is_forced = False
        self.forced_enum = None
        self._last_mode = None

        self.bus.subscribe(Topics.COMMAND_MODE_OVERRIDE, self._on_manual_state_change)

    def _on_manual_state_change(self, payload: dict):
        if payload.get("reset", False):
            self.is_forced = False
            self.forced_enum = None
            return

        self.is_forced = payload.get("forced", False)
        self.forced_enum = payload.get("mode", None)
        
        if self.forced_enum:
            self.state_manager.set_mode(self.forced_enum)
            if hasattr(self.scene, 'core'):
                self.scene.core.transition_progress = 0.0
            
        if hasattr(self.scene, 'core') and hasattr(self.scene.core, 'set_visual_mode'):
            if "forced_name" in payload:
                self.scene.core.set_visual_mode(payload["forced_name"])

    def resolve_system_mode(self, telemetry_data):
        if self.is_forced:
            if self.forced_enum:
                self.state_manager.set_mode(self.forced_enum)
            return

        # =========================================================================
        # AVALIAÇÃO AUTOMÁTICA DA TELEMETRIA
        # =========================================================================
        if telemetry_data.system_status == "CRITICAL":
            new_mode = Mode.ALERT
        elif telemetry_data.unknown_devices > 0 or telemetry_data.system_status == "WARNING":
            new_mode = Mode.WARNING
        else:
            # Ciclo padrão de teste automático (ex: alternando para server ou idle)
            uptime_seconds = time.time() % 240
            new_mode = Mode.SERVER if uptime_seconds < 60 else Mode.IDLE

        # Sincroniza a mudança de modo de forma limpa e força o reator a animar a entrada
        current_active_mode = self.state_manager.mode
        if new_mode != current_active_mode:
            self.state_manager.set_mode(new_mode)
            if hasattr(self.scene, 'core'):
                # Zera o progresso para que o núcleo execute a animação de centralização e libere as órbitas
                self.scene.core.transition_progress = 0.0