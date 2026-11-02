# interface/effects/glow.py
import pygame

class GlowEffect:
    def __init__(self, num_layers=4, intensity=12):
        self.num_layers = num_layers
        self.intensity = intensity

    def draw(self, screen, x: int, y: int, radius: float, color: tuple):
        """Desenha anéis concêntricos com opacidade decrescente para simular o brilho."""
        glow_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        
        for i in range(self.num_layers, 0, -1):
            alpha = int(40 / i)
            layer_radius = int(radius + (i * self.intensity))
            pygame.draw.circle(glow_surface, (*color, alpha), (x, y), layer_radius)
            
        screen.blit(glow_surface, (0, 0))