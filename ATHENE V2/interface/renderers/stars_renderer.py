# interface/renderers/stars_renderer.py
import pygame
import pygame.gfxdraw
import math
from core.modes import Mode

class StarsRenderer:
    def __init__(self):
        self.active_fade = 0.0  

    def draw(self, screen, stars_data, core_color, t: float, current_mode=None):
        rgb_color = core_color[:3] if len(core_color) >= 3 else (0, 200, 100)
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        fov = 250.0
        
        dt_fade = 0.016  
        if current_mode is not None and current_mode != Mode.IDLE:
            self.active_fade = min(1.0, self.active_fade + 0.35 * dt_fade) 
        else:
            # Reseta de forma limpa ao voltar para o IDLE
            self.active_fade = max(0.0, self.active_fade - 1.0 * dt_fade)

        # 1. ESTRELAS IDLE (3D Túnel)
        alpha_3d_multiplier = max(0.0, 1.0 - (self.active_fade * 1.3))
        if alpha_3d_multiplier > 0.01:
            for star in stars_data.collection:
                if star.z <= 0: continue
                proj_x = int((star.x * fov) / star.z) + stars_data.center_x
                proj_y = int((star.y * fov) / star.z) + stars_data.center_y
                
                if 0 <= proj_x < screen.get_width() and 0 <= proj_y < screen.get_height():
                    distance_factor = (1.0 - (star.z / 800.0))
                    sine_wave = math.sin((t * star.twinkle_speed * 0.6) + star.time_offset)
                    
                    alpha = int((195 + 125 * sine_wave) * distance_factor * alpha_3d_multiplier)
                    alpha = max(0, min(255, alpha))
                    
                    if alpha > 5:
                        pygame.gfxdraw.filled_circle(surf, proj_x, proj_y, 1, (*rgb_color, alpha))

        # 2. ESTRELAS LIVRES (2D)
        delayed_fade = max(0.0, (self.active_fade - 0.2) / 0.8) 
        if delayed_fade > 0.01:
            for star in stars_data.collection:
                if hasattr(star, 'pos_x'):
                    sx = int(star.pos_x)
                    sy = int(star.pos_y)
                    
                    if 0 <= sx < screen.get_width() and 0 <= sy < screen.get_height():
                        sine_wave = math.sin((t * star.twinkle_speed * 0.8) + star.time_offset)
                        alpha = int((140 + 115 * sine_wave) * delayed_fade)
                        alpha = max(0, min(255, alpha))
                        
                        if alpha > 5:
                            pygame.gfxdraw.filled_circle(surf, sx, sy, 1, (*rgb_color, alpha))
            
        screen.blit(surf, (0, 0))