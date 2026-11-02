# interface/animation.py
from interface.objects.stars import Stars
from interface.objects.core import Core

class AnimationController:
    def __init__(self):
        self.stars = Stars()
        self.core = Core()

    def update(self, dt: float, current_mode):
        """Calcula deslocamentos puros."""
        self.stars.update(dt)
        self.core.update(dt, current_mode)

    def draw(self, screen):
        """Delega a renderização das camadas de objetos."""
        self.stars.draw(screen)
        self.core.draw(screen)