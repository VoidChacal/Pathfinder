# interface/ui/fps.py
import pygame

class FPSCounter:
    def __init__(self, x=15, y=15, font_size=16):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("Consolas", font_size)
        self.color = (100, 100, 100)
        self.current_fps = 0
        self.min_fps = 999
        self.max_fps = 0

    def update(self, dt: float):
        """Calcula e armazena os picos de performance de forma autônoma."""
        if dt <= 0:
            return
        
        self.current_fps = int(1.0 / dt)
        
        # Ignora os frames iniciais de carregamento para não distorcer o mínimo
        if self.current_fps > 5:
            self.min_fps = min(self.min_fps, self.current_fps)
            self.max_fps = max(self.max_fps, self.current_fps)

    def draw(self, screen):
        # Exibe apenas o FPS atual (mas o objeto já guarda as métricas completas internamente)
        fps_text = self.font.render(f"FPS: {self.current_fps} (MIN: {self.min_fps})", True, self.color)
        screen.blit(fps_text, (self.x, self.y))