# interface/renderers/hud_renderer.py
import pygame
import pygame.gfxdraw
import math

class HUDRenderer:
    def draw(self, screen, telemetry, mode_name, core_color):
        base_color = core_color[:3] if len(core_color) >= 3 else (0, 180, 255)
        surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        
        w, h = screen.get_width(), screen.get_height()
        pad = 25  # Margem interna do visor
        bracket_len = 30  # Tamanho dos cantos táticos
        
        # 1. MOLDURA PERIMETRAL / CANTOS HOLOGRÁFICOS (Corner Brackets)
        # Canto Superior Esquerdo
        pygame.draw.line(surf, (*base_color, 180), (pad, pad), (pad + bracket_len, pad), 2)
        pygame.draw.line(surf, (*base_color, 180), (pad, pad), (pad, pad + bracket_len), 2)
        # Canto Superior Direito
        pygame.draw.line(surf, (*base_color, 180), (w - pad, pad), (w - pad - bracket_len, pad), 2)
        pygame.draw.line(surf, (*base_color, 180), (w - pad, pad), (w - pad, pad + bracket_len), 2)
        # Canto Inferior Esquerdo
        pygame.draw.line(surf, (*base_color, 180), (pad, h - pad), (pad + bracket_len, h - pad), 2)
        pygame.draw.line(surf, (*base_color, 180), (pad, h - pad), (pad, h - pad - bracket_len), 2)
        # Canto Inferior Direito
        pygame.draw.line(surf, (*base_color, 180), (w - pad, h - pad), (w - pad - bracket_len, h - pad), 2)
        pygame.draw.line(surf, (*base_color, 180), (w - pad, h - pad), (w - pad, h - pad - bracket_len), 2)

        # 2. GRÁFICOS DE BARRAS ANALÓGICAS SEGMENTADAS (Monitores Laterais Estilo Matrix)
        # Desenha pequenos blocos retangulares empilhados representando carga/capacidade
        bar_x = pad + 15
        bar_y_start = pad + 50
        num_blocks = 12
        block_h = 6
        block_gap = 4
        
        # Simula oscilação com base na CPU real da telemetria ou tempo
        t = pygame.time.get_ticks() / 1000.0
        active_blocks_left = int(num_blocks * (telemetry.cpu_usage / 100.0)) if hasattr(telemetry, 'cpu_usage') else int(6 + 4 * math.sin(t))
        active_blocks_left = max(1, min(num_blocks, active_blocks_left))
        
        for i in range(num_blocks):
            # Inverte a ordem para preencher de baixo para cima
            idx = num_blocks - i
            by = bar_y_start + i * (block_h + block_gap)
            
            alpha = 230 if idx <= active_blocks_left else 40
            # Bloco da Esquerda
            pygame.draw.rect(surf, (*base_color, alpha), pygame.Rect(bar_x, by, 18, block_h))
            # Bloco Simétrico da Direita
            pygame.draw.rect(surf, (*base_color, alpha), pygame.Rect(w - bar_x - 18, by, 18, block_h))

        # 3. CALIBRADOR DE HORIZONTE ARTIFICIAL (Linhas de Escala Lateral)
        center_y = h // 2
        scale_x = pad + 40
        for offset in [-60, -30, 0, 30, 60]:
            ly = center_y + offset
            line_w = 12 if offset == 0 else 6
            alpha_line = 150 if offset == 0 else 80
            pygame.draw.line(surf, (*base_color, alpha_line), (scale_x, ly), (scale_x + line_w, ly), 1)
            pygame.draw.line(surf, (*base_color, alpha_line), (w - scale_x, ly), (w - scale_x - line_w, ly), 1)

        screen.blit(surf, (0, 0))