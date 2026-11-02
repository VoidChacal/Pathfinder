# interface/objects/star.py
import random
from config.settings import WIDTH, HEIGHT

class Star:
    def __init__(self):
        self.reset()
        # Inicializa o Z em posições aleatórias para evitar o efeito de "parede" no primeiro frame
        self.z = random.uniform(10, 800)
        self.time_offset = random.uniform(0.0, 100.0)
        self.twinkle_speed = random.uniform(2.0, 5.0)

    def reset(self):
        """Gera uma nova estrela no horizonte distante."""
        self.x = random.randint(-WIDTH // 2, WIDTH // 2)
        self.y = random.randint(-HEIGHT // 2, HEIGHT // 2)
        self.z = 800.0  # Fundo da tela