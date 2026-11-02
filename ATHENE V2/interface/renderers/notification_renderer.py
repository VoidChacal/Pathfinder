# interface/renderers/notification_renderer.py
import pygame

class NotificationRenderer:
    def __init__(self, font_size=14, line_spacing=35):
        self.font = pygame.font.SysFont("Consolas", font_size, bold=True)
        self.line_spacing = line_spacing
        
        # Paleta de cores semânticas e independentes do estado da Athene
        self.COLORS = {
            "info": (0, 180, 255),       # Azul Tecnológico
            "success": (0, 255, 120),    # Verde Operacional
            "warning": (255, 180, 0),    # Laranja de Atenção
            "alert": (255, 50, 50),      # Vermelho de Erro
            "system": (150, 150, 150),   # Cinza de Log Estrutural
            "ai": (180, 50, 255)         # Roxo de Pensamento Neural
        }

    def draw(self, screen, manager):
        """Consome o manager de notificações e renderiza a pilha na tela."""
        start_x = screen.get_width() - 320
        start_y = 20

        for i, item in enumerate(manager.collection):
            # Captura a cor do tipo específico da notificação
            accent_color = self.COLORS.get(item.type, (255, 255, 255))
            
            # Canvas transparente para o banner
            surface = pygame.Surface((300, 28), pygame.SRCALPHA)
            
            # Fundo fumê semi-transparente do box
            pygame.draw.rect(surface, (10, 10, 10, int(item.alpha * 0.85)), (0, 0, 300, 28), border_radius=4)
            # Tag/Barra lateral colorida baseada no TIPO da notificação
            pygame.draw.rect(surface, (*accent_color, item.alpha), (0, 0, 4, 28), border_radius=4)

            # Renderização da tipografia
            text_surface = self.font.render(item.message, True, (230, 230, 230))
            text_surface.set_alpha(item.alpha)
            
            surface.blit(text_surface, (12, 6))
            
            # Desenha na tela principal aplicando o empilhamento vertical
            screen.blit(surface, (start_x, start_y + (i * self.line_spacing)))