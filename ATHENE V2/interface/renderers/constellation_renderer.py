# interface/renderers/constellation_renderer.py
import pygame
import pygame.gfxdraw
import math
from core.modes import Mode

class ConstellationRenderer:
    def __init__(self):
        self.map_opacity = 0.0
        # Configuração das 5 estrelas livres com órbitas excêntricas e fases diferentes
        self.idle_stars_config = [
            {"radius": 75, "speed": 0.3, "phase": 0.0},
            {"radius": 110, "speed": -0.25, "phase": 1.25},
            {"radius": 135, "speed": 0.4, "phase": 2.5},
            {"radius": 90, "speed": -0.35, "phase": 3.75},
            {"radius": 120, "speed": 0.2, "phase": 5.0}
        ]

    def draw(self, screen, constellation, core, current_mode=None):
        base_color = core.color[:3] if len(core.color) >= 3 else (0, 200, 100)
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        cx, cy = int(core.x), int(core.y)
        t = pygame.time.get_ticks() / 1000.0
        
        dt_fade = 0.016
        is_idle = (current_mode == Mode.IDLE)

        if not is_idle:
            self.map_opacity = min(1.0, self.map_opacity + 0.8 * dt_fade) 
        else:
            self.map_opacity = max(0.0, self.map_opacity - 1.5 * dt_fade) 

        mo = self.map_opacity

        # =========================================================================
        # 1. MODO IDLE: Pentágono bagunçado (com conexões), Estrelas fixas, Rastro fantasmagórico
        # =========================================================================
        if is_idle:
            current_idle_points = []
            for data in self.idle_stars_config:
                dynamic_radius = data["radius"] + math.sin(t * 1.2 + data["phase"]) * 18.0
                angle = (t * data["speed"]) + data["phase"]
                px = cx + int(dynamic_radius * math.cos(angle))
                py = cy + int(dynamic_radius * math.sin(angle))
                current_idle_points.append((px, py))

            # Linhas de conexão do pentágono orgânico (conectadas ao núcleo e entre si)
            num_points = len(current_idle_points)
            for i in range(num_points):
                p_atual = current_idle_points[i]
                p_proxima = current_idle_points[(i + 1) % num_points]
                pygame.draw.aaline(surf, (*base_color, 75), p_atual, p_proxima)
                pygame.draw.aaline(surf, (*base_color, 40), (cx, cy), p_atual)

            # Desenha as estrelas livres (pontos fixos, sem piscar)
            for px, py in current_idle_points:
                star_alpha = 210 # Opacidade fixa
                pygame.draw.line(surf, (255, 255, 255, star_alpha), (px - 4, py), (px + 4, py), 1)
                pygame.draw.line(surf, (255, 255, 255, star_alpha), (px, py - 4), (px, py + 4), 1)
                pygame.gfxdraw.filled_circle(surf, px, py, 3, (255, 255, 255, star_alpha))
                pygame.gfxdraw.aacircle(surf, px, py, 8, (*base_color, int(star_alpha * 0.5)))
            
            # 2. ANEL DE TELEMETRIA OCULTO (Fantasmagórico)
            # O arco mais externo aparece apenas como um rastro tracejado e muito fraco no IDLE
            r_telemetry = 145
            telemetry_alpha = int(50 + 30 * math.sin(t * 0.8)) # Pulso fantasma lento
            pygame.gfxdraw.arc(surf, cx, cy, r_telemetry, 0, 360, (*base_color, telemetry_alpha))
            # Adiciona uns tracinhos extras para o efeito fantasma
            for ang_off in range(0, 360, 20):
                ang_rad = math.radians((t * 15) + ang_off) # Gira super devagar
                x1 = cx + int((r_telemetry - 8) * math.cos(ang_rad))
                y1 = cy + int((r_telemetry - 8) * math.sin(ang_rad))
                x2 = cx + int((r_telemetry + 8) * math.cos(ang_rad))
                y2 = cy + int((r_telemetry + 8) * math.sin(ang_rad))
                pygame.draw.aaline(surf, (*base_color, int(telemetry_alpha * 0.6)), (x1, y1), (x2, y2))


        # =========================================================================
        # 2. MODOS ATIVOS: Constelação estruturada e Arcos Órbita sólidos
        # =========================================================================
        else:
            if hasattr(constellation, 'points') and constellation.points:
                poly_points = [(int(p[0]), int(p[1])) for p in constellation.points]
                
                if mo > 0.01:
                    r_arco1, r_arco2, r_arco3, r_arco4 = 30, 65, 105, 145
                    
                    pygame.gfxdraw.aacircle(surf, cx, cy, r_arco1, (255, 255, 255, int(240 * mo)))

                    # Arco 2
                    pygame.gfxdraw.aacircle(surf, cx, cy, r_arco2, (*base_color, int(200 * mo)))
                    for i in range(4):
                        ang = (t * 0.4) + (i * (math.pi / 2))
                        sx = cx + int(r_arco2 * math.cos(ang))
                        sy = cy + int(r_arco2 * math.sin(ang))
                        pygame.gfxdraw.filled_circle(surf, sx, sy, 4, (255, 255, 255, int(255 * mo)))
                        pygame.gfxdraw.aacircle(surf, sx, sy, 6, (*base_color, int(220 * mo)))

                    # Arco 3
                    pygame.gfxdraw.aacircle(surf, cx, cy, r_arco3, (*base_color, int(180 * mo)))
                    for i in range(4):
                        ang = (-t * 0.25) + (i * (math.pi / 2))
                        sx = cx + int(r_arco3 * math.cos(ang))
                        sy = cy + int(r_arco3 * math.sin(ang))
                        pygame.gfxdraw.filled_circle(surf, sx, sy, 4, (255, 255, 255, int(255 * mo)))
                        pygame.gfxdraw.aacircle(surf, sx, sy, 6, (*base_color, int(200 * mo)))

                    # Arco 4 (Sólido e girando no modo ativo)
                    pygame.gfxdraw.aacircle(surf, cx, cy, r_arco4, (*base_color, int(220 * mo)))

                    # Linhas vetoriais oficiais
                    if len(poly_points) > 1:
                        for i in range(len(poly_points)):
                            p1 = poly_points[i]
                            p2 = poly_points[(i + 1) % len(poly_points)]
                            pygame.draw.aaline(surf, (*base_color, int(220 * mo)), p1, p2)
                            pygame.draw.aaline(surf, (*base_color, int(75 * mo)), (cx, cy), p1)

                # As 5 estrelas oficiais ativas
                for px, py in poly_points:
                    star_mo = max(mo, 0.1)
                    pygame.draw.line(surf, (255, 255, 255, int(240 * star_mo)), (px - 5, py), (px + 5, py), 1)
                    pygame.draw.line(surf, (255, 255, 255, int(240 * star_mo)), (px, py - 5), (px, py + 5), 1)
                    pygame.gfxdraw.filled_circle(surf, px, py, 4, (255, 255, 255, int(255 * star_mo)))
                    pygame.gfxdraw.aacircle(surf, px, py, 11, (*base_color, int(230 * star_mo)))

        screen.blit(surf, (0, 0))