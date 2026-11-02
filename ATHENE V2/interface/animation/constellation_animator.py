# interface/animation/constellation_animator.py
import math
from core.modes import Mode

class ConstellationAnimator:
    def __init__(self):
        self.angles = [i * (2 * math.pi / 5) for i in range(5)]
        self.current_positions = None

    def update(self, constellation, core, current_mode, dt: float):
        cx, cy = core.x, core.y
        
        if self.current_positions is None:
            self.current_positions = [[cx, cy] for _ in range(5)]
            
        target_pts = []
        base_radius = 145.0
        
        if current_mode == Mode.IDLE:
            # Em IDLE: Flutuação sutil padrão
            for i, angle in enumerate(self.angles):
                dynamic_radius = base_radius + 12.0 * math.cos(core.time_accumulator * 1.5 + i)
                dynamic_angle = angle + (core.time_accumulator * 0.08)
                tx = cx + dynamic_radius * math.cos(dynamic_angle)
                ty = cy + dynamic_radius * math.sin(dynamic_angle)
                target_pts.append((tx, ty))
        else:
            # EM MODO ATIVO: Aceleração orbital aplicada (0.12) para um giro mais dinâmico
            fixed_rotation = core.time_accumulator * 0.12
            for angle in self.angles:
                tx = cx + base_radius * math.cos(angle + fixed_rotation)
                ty = cy + base_radius * math.sin(angle + fixed_rotation)
                target_pts.append((tx, ty))
                
        # Interpolação elástica responsiva
        lerp_speed = 6.0 * dt
        for i in range(5):
            self.current_positions[i][0] += (target_pts[i][0] - self.current_positions[i][0]) * lerp_speed
            self.current_positions[i][1] += (target_pts[i][1] - self.current_positions[i][1]) * lerp_speed
            
        constellation.points = [(p[0], p[1]) for p in self.current_positions]