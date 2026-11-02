# interface/effects/orbit.py
import pygame
import math

class OrbitEffect:
    def __init__(self, width_factor=2.4, height_factor=0.6):
        self.w_factor = width_factor
        self.h_factor = height_factor

    def draw(self, screen, x: int, y: int, radius: float, color: tuple, time_accumulator: float):
        """Calcula a distorção em elipse e desenha o anel rotacionando no espaço."""
        ring_w = int(radius * self.w_factor)
        ring_h = int(radius * self.h_factor)
        
        # Cria a superfície transparente para desenhar o anel
        ring_surface = pygame.Surface((ring_w * 2, ring_h * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(ring_surface, (*color, 120), (ring_w // 2, ring_h // 2, ring_w, ring_h), 2)
        
        # Aplica uma leve inclinação dinâmica baseada no tempo
        angle_tilt = math.degrees(math.sin(time_accumulator) * 0.2)
        rotated_ring = pygame.transform.rotate(ring_surface, angle_tilt)
        
        rect = rotated_ring.get_rect(center=(x, y))
        screen.blit(rotated_ring, rect.topleft)