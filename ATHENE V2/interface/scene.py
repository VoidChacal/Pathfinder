# interface/scene.py
import pygame
from config.settings import WIDTH, HEIGHT
from interface.objects.stars import Stars
from interface.objects.core import Core
from interface.objects.constellation import Constellation
from interface.animation.core_animator import CoreAnimator
from interface.animation.stars_animator import StarsAnimator
from interface.animation.constellation_animator import ConstellationAnimator
from interface.renderers.stars_renderer import StarsRenderer
from interface.renderers.core_renderer import CoreRenderer
from interface.renderers.constellation_renderer import ConstellationRenderer
from interface.renderers.hud_renderer import HUDRenderer

class Scene:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        
        centro_x = WIDTH // 2 if 'WIDTH' in globals() else 400
        centro_y = HEIGHT // 2 if 'HEIGHT' in globals() else 300
        
        # Modelos de Dados Puros
        self.stars = Stars()
        self.core = Core(x=centro_x, y=centro_y, radius=16)
        self.constellation = Constellation()
        
        # Inicializadores de atributos estendidos necessários pelos animadores herdados
        self.core.time_accumulator = 0.0
        self.core.transition_speed = 5.0
        
        # Sistemas de Animação (Mantém apenas a chamada correta com WIDTH e HEIGHT)
        self.stars_animator = StarsAnimator(WIDTH, HEIGHT)
        self.core_animator = CoreAnimator()
        self.constellation_animator = ConstellationAnimator()
        
        # Renderizadores Especialistas
        self.stars_renderer = StarsRenderer()
        self.core_renderer = CoreRenderer()
        self.constellation_renderer = ConstellationRenderer()
        self.hud_renderer = HUDRenderer()

    def update(self, dt):
        current_mode = self.state_manager.mode
        self.core.update(dt, current_mode)
        self.core_animator.update(self.core, current_mode, dt)
        
        # Atualiza a poeira estelar dinâmica de fundo
        self.stars_animator.update(dt)
        
        self.constellation_animator.update(self.constellation, self.core, current_mode, dt)

    def draw(self, screen):
        ticks_seconds = pygame.time.get_ticks() / 1000.0
        current_mode = self.state_manager.mode
        
        # Desenha o fundo com fade inteligente
        self.stars_renderer.draw(screen, self.stars, self.core.color, ticks_seconds, current_mode)
        
        # Desenha a poeira estelar dinâmica viva do StarsAnimator
        self.stars_animator.draw(screen, self.core.color)
        
        # Passa o current_mode para a constelação controlar o surgimento gradativo
        self.constellation_renderer.draw(screen, self.constellation, self.core, current_mode)
        
        self.core_renderer.draw(screen, self.core)