# interface/animation/stars_animator.py
import pygame
import random
import math
import pygame.gfxdraw

class StarsAnimator:
    def __init__(self, width, height, num_stars=300):
        self.width = width
        self.height = height
        self.stars = []
        self.mouse_pos = (0, 0)
        self._initialize_stars(num_stars)

    def _initialize_stars(self, num_stars):
        # Gera estrelas com posições, tamanhos, velocidades de piscar e profundidades (z) aleatórias
        for _ in range(num_stars):
            self.stars.append({
                'pos': [random.randint(0, self.width), random.randint(0, self.height)],
                'z': random.uniform(0.2, 2.0), # Profundidade (paralaxe)
                'size': random.uniform(0.5, 1.8),
                'base_alpha': random.randint(50, 180),
                'twinkle_speed': random.uniform(0.02, 0.08),
                'twinkle_offset': random.uniform(0, 6.28)
            })

    def update(self, dt: float):
        # Atualiza a posição do mouse
        self.mouse_pos = pygame.mouse.get_pos()
        
        # Atualiza o brilho de cada estrela (efeito de piscar senoidal)
        current_time = pygame.time.get_ticks() / 1000.0
        for star in self.stars:
            alpha_wave = math.sin(current_time * star['twinkle_speed'] * 50 + star['twinkle_offset'])
            star['alpha'] = int(star['base_alpha'] * (0.6 + 0.4 * alpha_wave)) # Mantém um brilho mínimo

    def draw(self, surf, core_color):
        bg_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        mx, my = self.mouse_pos
        
        for star in self.stars:
            base_alpha = star['alpha']
            dx = star['pos'][0] - mx
            dy = star['pos'][1] - my
            dist = math.sqrt(dx*dx + dy*dy)
            
            target_x = star['pos'][0]
            target_y = star['pos'][1]
            
            # CORREÇÃO: Adiciona verificação "dist > 0" para evitar ZeroDivisionError
            if dist > 0 and dist < 150:
                force = (150 - dist) / 150.0
                # A divisão agora só ocorre se dist for maior que zero
                target_x += (dx / dist) * force * 15.0
                target_y += (dy / dist) * force * 15.0
                
                base_alpha = min(255, base_alpha + int(force * 100))

            color = (*core_color[:3], base_alpha)
            
            # Desenha a estrela usando as coordenadas possivelmente alteradas
            pygame.gfxdraw.pixel(bg_surf, int(target_x), int(target_y), color)
            if star['size'] > 1.0:
                pygame.gfxdraw.filled_circle(bg_surf, int(target_x), int(target_y), int(star['size']), color)

        surf.blit(bg_surf, (0, 0))