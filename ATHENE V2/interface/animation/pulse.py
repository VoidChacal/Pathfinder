# interface/animation/pulse.py
import math
from core.modes import Mode

class PulseAnimation:
    def calculate_radius(self, mode: Mode, t: float, base_radius: float) -> float:
        """Calcula o deslocamento do raio baseado na pulsação senoidal de cada modo."""
        if mode == Mode.SPEAKING:
            # Pulsação rápida e agressiva (efeito de onda de áudio)
            return base_radius + (math.sin(t * 3.0) * 3)
            
        elif mode == Mode.PROCESSING:
            # Oscilação frenética de cálculo
            return base_radius + (math.sin(t * 3.0) * 3)
            
        elif mode in [Mode.WARNING, Mode.ALERT]:
            # Batimento cardíaco simulando estado crítico
            return base_radius + abs(math.sin(t * 3.0) * 3)
            
        else:
            # Respiração suave em repouso (Idle / Server)
            return base_radius + (math.sin(t * 3.0) * 3)