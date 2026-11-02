# interface/animation/core_animator.py
import pygame
import math
from core.modes import Mode
from config.settings import WIDTH, HEIGHT

class CoreAnimator:
    def update(self, core, current_mode, dt: float):
        # Se estiver em MODO IDLE: Mantém livre
        if current_mode == Mode.IDLE:
            if hasattr(core, 'time_accumulator'):
                core.time_accumulator += dt
            return

        # =========================================================================
        # MODOS ATIVOS (Server, Warning, Alert, etc.):
        # =========================================================================
        target_x = WIDTH // 2
        base_y = HEIGHT // 2
        
        # Animação de flutuação suave vertical
        t = pygame.time.get_ticks() / 1000.0
        floating_offset = math.sin(t * 1.8) * 10.0 + math.cos(t * 3.6) * 3.0 
        target_y = base_y + floating_offset

        # Interpolação fluida para o centro
        lerp_speed = 6.0 * dt
        core.x += (target_x - core.x) * lerp_speed
        core.y += (target_y - core.y) * lerp_speed
        
        if hasattr(core, 'time_accumulator'):
            core.time_accumulator += dt