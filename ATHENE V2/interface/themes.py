# interface/themes.py
import pygame
from core.modes import Mode

# Definição das cores RGB dos estados da Athene
THEMES = {
    Mode.IDLE: (0, 150, 255),       # Azul Elétrico
    Mode.SERVER: (0, 255, 150),     # Verde Ciberbunk
    Mode.PROCESSING: (180, 50, 255),# Roxo Neon
    Mode.SPEAKING: (255, 255, 255),  # Branco Puro
    Mode.WARNING: (255, 160, 0),    # Laranja Alerta
    Mode.ALERT: (255, 0, 50)        # Vermelho Crítico
}

def color_lerp(start_color, end_color, t):
    """Realiza a interpolação linear suave entre duas cores (t varia de 0.0 a 1.0)."""
    t = max(0.0, min(1.0, t)) # Garante que t não estoure os limites
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * t),
        int(start_color[1] + (end_color[1] - start_color[1]) * t),
        int(start_color[2] + (end_color[2] - start_color[2]) * t)
    )