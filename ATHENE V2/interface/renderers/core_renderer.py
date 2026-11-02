# interface/renderers/core_renderer.py
import pygame
import pygame.gfxdraw

class CoreRenderer:
    def draw(self, screen, core):
        x, y = int(core.x), int(core.y)
        base_color = core.color[:3] if len(core.color) >= 3 else (0, 200, 100)
        
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        
        # Super brilho gradiente limpo (sem traços)
        glow_max_r = 55
        for r in range(glow_max_r, 0, -2):
            alpha_factor = (1.0 - (r / glow_max_r)) ** 1.3
            pygame.gfxdraw.filled_circle(surf, x, y, r + 4, (*base_color, int(70 * alpha_factor)))
            pygame.gfxdraw.filled_circle(surf, x, y, r, (255, 255, 255, int(180 * alpha_factor)))
            
        # Ponto centralizado fixo de alta definição
        pygame.gfxdraw.filled_circle(surf, x, y, 10, (255, 255, 255, 255))
        pygame.gfxdraw.aacircle(surf, x, y, 14, (*base_color, 255))
            
        screen.blit(surf, (0, 0))