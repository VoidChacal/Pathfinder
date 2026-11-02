# interface/objects/stars.py
from config.settings import WIDTH, HEIGHT
from .star import Star 

class Stars:
    def __init__(self, num_stars=150):
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        self.collection = [Star() for _ in range(num_stars)]


# interface/renderers/background_renderer.py
import pygame
import random
import math
from core.modes import Mode

class BackgroundRenderer:
    def __init__(self, width=600, height=600, num_stars=60):
        self.width = width
        self.height = height
        self.stars = []
        
        # Inicializa estrelas com posições, velocidades bidimensionais lentas e offsets de brilho
        for _ in range(num_stars):
            self.stars.append({
                'x': random.uniform(0, width),
                'y': random.uniform(0, height),
                'speed_x': random.uniform(-8.0, 8.0), # Movimento lateral lento
                'speed_y': random.uniform(-8.0, 8.0), # Movimento vertical lento
                'size': random.choice([1, 2, 2, 3]),
                'twinkle_speed': random.uniform(2.0, 5.0),
                'phase': random.uniform(0, 2 * math.pi)
            })

    def draw(self, screen, current_mode, dt):
        # O fundo escuro padrão se mantém intacto
        screen.fill((0, 5, 2, 255)) 
        
        t = pygame.time.get_ticks() / 1000.0
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        
        for star in self.stars:
            if current_mode == Mode.IDLE:
                # Se estiver em Idle, você pode manter a aproximação original ou a flutuação.
                # Para isolar o pedido, mantemos o comportamento livre apenas fora do Idle:
                star['x'] += star['speed_x'] * 0.2 * dt
                star['y'] += star['speed_y'] * 0.2 * dt
            else:
                # FORA DO IDLE: Movimento lento, livre e tridimensional cancelado
                star['x'] += star['speed_x'] * dt
                star['y'] += star['speed_y'] * dt
            
            # Reposiciona as estrelas caso saiam das bordas da tela
            if star['x'] < 0: star['x'] = self.width
            if star['x'] > self.width: star['x'] = 0
            if star['y'] < 0: star['y'] = self.height
            if star['y'] > self.height: star['y'] = 0
            
            # Cálculo de Cintilação (Efeito de piscar baseado no tempo e fase individual)
            alpha_multiplier = (math.sin(t * star['twinkle_speed'] + star['phase']) + 1.0) / 2.0
            # Variação de brilho mantendo a cor verde esmeralda digital característica do HUD
            alpha = int(100 + (155 * alpha_multiplier)) 
            
            color = (0, 220, 100, alpha) if star['size'] > 1 else (0, 150, 70, alpha)
            
            # Desenha a estrela como pequenos nós brilhantes na tela
            pos_x, pos_y = int(star['x']), int(star['y'])
            if star['size'] == 1:
                surf.set_at((pos_x, pos_y), color)
            else:
                pygame.draw.circle(surf, color, (pos_x, pos_y), star['size'] - 1)
                
        screen.blit(surf, (0, 0))