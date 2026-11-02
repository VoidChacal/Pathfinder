# interface/renderer.py
import pygame
from interface.scene import Scene
from interface.hud import HUD

class Renderer:
    def __init__(self, screen, state_manager, datastore):
        self.screen = screen
        self.scene = Scene(state_manager)
        self.hud = HUD(datastore, state_manager, screen.get_height())

    def render(self, dt: float):
        # 1. Fase Física (Updates)
        self.scene.update(dt)
        self.hud.update(dt)
        
        # 2. Fase de Limpeza
        self.screen.fill((0, 0, 0))
        
        # 3. Fase de Renderização Cascata (Z-Index Natural)
        self.scene.draw(self.screen) # Desenha estrelas, glows, orbits e o núcleo
        self.hud.draw(self.screen)   # Desenha o FPS e as informações textuais por cima
        
        # 4. Envio para o Hardware
        pygame.display.flip()