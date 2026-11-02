# interface/objects/constellation.py
import math
import random

class ConstellationNode:
    def __init__(self, base_angle: float):
        self.base_angle = base_angle
        self.current_angle = base_angle
        
        # Variáveis exclusivas para o Modo Idle Caótico:
        # Cada estrela ganha uma velocidade de rotação única
        self.speed_factor = random.uniform(0.6, 2.2)
        # Deslocamento de tempo para desenhar órbitas dessincronizadas
        self.time_offset = random.uniform(0.0, 100.0)

class Constellation:
    def __init__(self):
        # Cria as 5 estrelas base
        self.nodes = [ConstellationNode(math.radians(i * 72)) for i in range(5)]