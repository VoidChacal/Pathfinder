# interface/objects/core.py
import pygame
import pygame.gfxdraw
import math
import random
from core.modes import Mode
from interface.themes import THEMES

# =====================================================================
# INTERFACES AUXILIARES CINÉTICAS (UNIFICADAS PARA EVITAR ERROS DE IMPORT)
# =====================================================================

class FloatingEffect:
    def __init__(self, amplitude=14, speed=0.0015):
        self.amplitude = amplitude
        self.speed = speed
    def get_offset(self):
        ticks = pygame.time.get_ticks()
        return math.sin(ticks * self.speed) * self.amplitude

class DataParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.alpha = 255
        self.fade_speed = random.uniform(2, 5)
        self.size = random.choice([1, 2])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.alpha -= self.fade_speed

    def draw(self, surf):
        if self.alpha > 0:
            p_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.rect(p_surf, (self.color[0], self.color[1], self.color[2], int(self.alpha)), (0, 0, self.size, self.size))
            surf.blit(p_surf, (int(self.x), int(self.y)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    def emit(self, x, y, color, amount=1):
        for _ in range(amount):
            self.particles.append(DataParticle(x, y, color))
    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.alpha <= 0:
                self.particles.remove(p)
    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)

class HaloDot:
    def __init__(self, core_x, core_y, radius):
        self.core_x = core_x
        self.core_y = core_y
        self.radius = radius
        self.angle = random.uniform(0, 2 * math.pi)
        self.idle_speed = random.uniform(0.005, 0.03)
        self.action_speed = 0.015
        self.x = core_x
        self.y = core_y

    def update(self, mode, index, total_dots):
        if mode == "idle":
            self.angle += self.idle_speed
        else:
            target_angle = (pygame.time.get_ticks() * 0.001 * self.action_speed) + (index * (2 * math.pi / total_dots))
            self.angle += (target_angle - self.angle) * 0.1
        self.x = self.core_x + self.radius * math.cos(self.angle)
        self.y = self.core_y + self.radius * math.sin(self.angle)

class OrbitalStar:
    def __init__(self, core_x, core_y):
        self.core_x = core_x
        self.core_y = core_y
        self.x = core_x
        self.y = core_y
        self.target_x = core_x
        self.target_y = core_y
        self.random_angle = random.uniform(0, 2 * math.pi)
        self.noise_speed = random.uniform(0.01, 0.03)

    def update(self, mode, index, total_stars, global_angle, orbit_radius):
        if mode != "idle" and orbit_radius > 5:
            star_angle = global_angle + (index * (2 * math.pi / total_stars))
            self.target_x = self.core_x + orbit_radius * math.cos(star_angle)
            self.target_y = self.core_y + orbit_radius * math.sin(star_angle)
        else:
            self.random_angle += self.noise_speed
            current_radius = orbit_radius + math.sin(self.random_angle * 2) * 15
            self.target_x = self.core_x + current_radius * math.cos(self.random_angle)
            self.target_y = self.core_y + current_radius * math.sin(self.random_angle)
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

# =====================================================================
# OBJETO CENTRAL - CORE DA ATHENE
# =====================================================================

class Core:
    def __init__(self, x=400.0, y=300.0, radius=16):
        self.center_x = float(x)
        self.center_y = float(y)
        self.x = float(x)
        self.y = float(y)
        
        self.target_x = float(x)
        self.target_y = float(y)
        self.idle_timer = 0
        
        self.radius = radius
        self.base_radius = radius  
        self.color = THEMES.get(Mode.IDLE, (0, 150, 255))
        
        self.visual_mode = "idle"
        self.floater = FloatingEffect(amplitude=16, speed=0.0015)
        
        # Elementos da interface antiga acoplados localmente
        self.particles = ParticleSystem()
        self.num_orbit_stars = 5
        self.orbit_stars = [OrbitalStar(self.x, self.y) for _ in range(self.num_orbit_stars)]
        self.halo1_dots = [HaloDot(self.x, self.y, 56) for _ in range(4)]
        self.halo2_dots = [HaloDot(self.x, self.y, 80) for _ in range(4)]
        
        self.transition_progress = 0.0

    def set_visual_mode(self, mode_name: str):
        self.visual_mode = mode_name.lower()

    def update(self, dt, current_mode_enum):
        ticks = pygame.time.get_ticks()
        self.color = THEMES.get(current_mode_enum, (0, 150, 255))

        if self.visual_mode not in ["idle"]:
            self.visual_mode = current_mode_enum.name.lower()

        # Determina o Zoom Tático baseado no Modo
        target_zoom = 0.0 if (self.visual_mode == "idle" or current_mode_enum == Mode.IDLE) else 1.0
        self.transition_progress += (target_zoom - self.transition_progress) * 0.08

        # Lógica de movimentação
        if target_zoom == 0.0:
            if ticks > self.idle_timer:
                self.target_x = self.center_x + random.randint(-130, 130)
                self.target_y = self.center_y + random.randint(-90, 90)
                self.idle_timer = ticks + random.randint(3000, 5500)
            self.x += (self.target_x - self.x) * 0.022
            self.y += (self.target_y - self.y) * 0.022
        else:
            self.target_x = self.center_x
            self.target_y = self.center_y
            self.x += (self.target_x - self.x) * 0.095
            self.y += (self.target_y - self.y) * 0.095

        # Atualização dos nós dinâmicos
        render_x, render_y = self.get_render_positions()
        global_angle = ticks * 0.0008
        
        for i, star in enumerate(self.orbit_stars):
            star.core_x = render_x
            star.core_y = render_y
            star.update(self.visual_mode, i, self.num_orbit_stars, global_angle, 110 * self.transition_progress)

        for dot in self.halo1_dots + self.halo2_dots:
            dot.core_x = render_x
            dot.core_y = render_y

        for i, dot in enumerate(self.halo1_dots): dot.update(self.visual_mode, i, 4)
        for i, dot in enumerate(self.halo2_dots): dot.update(self.visual_mode, i, 4)

        if self.transition_progress > 0.1 and ticks % 4 == 0:
            self.particles.emit(render_x, render_y, self.color, 1)
        self.particles.update()

    def get_render_positions(self):
        render_y = self.y + self.floater.get_offset()
        return int(self.x), int(render_y)