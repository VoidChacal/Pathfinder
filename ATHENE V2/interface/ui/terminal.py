# interface/ui/terminal.py
import pygame
from interface.themes import THEMES
from core.topics import Topics

class TerminalUI:
    def __init__(self, event_bus, state_manager, x=15, y_bottom=570, width=450, max_lines=8):
        self.bus = event_bus
        self.state_manager = state_manager
        self.x = x
        self.y_bottom = y_bottom
        self.width = width
        self.max_lines = max_lines
        self.font = pygame.font.SysFont("Consolas", 12)
        
        # Buffer de mensagens da tela (Mistura logs e respostas da IA)
        self.history = ["[SYSTEM]: Interface de terminal ativa. Aguardando comandos..."]
        
        # Buffer de entrada de texto
        self.input_text = ""
        
        # Inscreve o terminal para capturar e exibir mensagens
        self.bus.subscribe(Topics.CHAT_AI_MESSAGE, lambda msg: self.append_line(f"[ATHENE]: {msg}"))
        self.bus.subscribe(Topics.SYSTEM_LOG, lambda log: self.append_line(log))

    def append_line(self, text: str):
        """Adiciona uma linha ao terminal e gerencia quebra simples e rolagem."""
        # Quebra básica caso a linha passe do tamanho estipulado do terminal
        max_chars = int(self.width / 7) # Aproximação baseada na fonte Consolas
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
        
        for chunk in chunks:
            self.history.append(chunk)
            
        # Mantém apenas as últimas linhas necessárias na tela
        if len(self.history) > self.max_lines:
            self.history = self.history[-self.max_lines:]

    def handle_keydown(self, event):
        """Processa a digitação vinda do window.py"""
        if event.key == pygame.K_RETURN:
            if self.input_text.strip():
                user_msg = self.input_text
                self.append_line(f"[USER]: {user_msg}")
                # Envia para o barramento processar
                self.bus.publish(Topics.CHAT_USER_MESSAGE, user_msg)
                self.input_text = ""  # Limpa o prompt
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            # Captura caracteres de texto padrão digitados
            if event.unicode and event.unicode.isprintable():
                self.input_text += event.unicode

    def draw(self, screen):
        current_mode = self.state_manager.mode
        text_color = THEMES.get(current_mode, (0, 255, 0)) # Cor base do tema ativo
        
        line_spacing = 16
        current_y = self.y_bottom
        
        # 1. Desenha a linha de input ativo (Prompt inferior)
        prompt_str = f"athene@core:> {self.input_text}"
        # Piscar o cursor opcional
        if pygame.time.get_ticks() % 1000 < 500:
            prompt_str += "_"
            
        lbl_prompt = self.font.render(prompt_str, True, text_color)
        screen.blit(lbl_prompt, (self.x, current_y))
        
        # Separador visual simples acima do prompt
        pygame.draw.line(screen, (40, 40, 40), (self.x, current_y - 6), (self.x + self.width, current_y - 6), 1)
        
        # 2. Desenha o histórico de baixo para cima
        current_y -= 12
        for line in reversed(self.history):
            current_y -= line_spacing
            # Se for uma mensagem da Athene ou erro, podemos destacar levemente a cor
            color = text_color
            if "[ATHENE]" in line:
                color = (255, 255, 255)  # Destaca as respostas da IA em branco claro
            elif "[ERROR]" in line:
                color = (255, 50, 50)
                
            rendered_line = self.font.render(line, True, color)
            screen.blit(rendered_line, (self.x, current_y))