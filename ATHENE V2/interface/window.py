# interface/window.py
import pygame
import sys
import win32gui
import win32api
import win32con
import keyboard
from core.topics import Topics
from core.modes import Mode

class Window:
    def __init__(self, width: int, height: int, title: str = "ATHENE - OS CORE INTERFACE"):
        pygame.init()
        self.width = width
        self.height = height
        
        # 1. Cria a janela sem bordas (NOFRAME)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
        pygame.display.set_caption(title)
        
        # 2. Captura o HWND do Windows e define como TOPMOST (Sempre no topo)
        self.hwnd = win32gui.FindWindow(None, title)
        if self.hwnd:
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW
            )
            
        # 3. Estado de arraste da janela
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # 4. Registra o atalho global F9
        keyboard.add_hotkey("f9", self.bring_to_front)

    def bring_to_front(self):
        """Traz a janela para o topo quando F9 é pressionado."""
        if self.hwnd:
            win32gui.ShowWindow(self.hwnd, win32con.SW_SHOWNORMAL)
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE |
                win32con.SWP_NOSIZE |
                win32con.SWP_NOACTIVATE
            )

    def handle_events(self, system) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # SE TIVER COMPATÍVEL COM O SISTEMA, ENVIAMOS PARA O TERMINAL DE CHAT
                # Evita disparar atalhos de teste se o usuário estiver digitando no terminal
                if hasattr(system, 'terminal'):
                    # O atalho de retorno (Enter/Backspace/Letras) é absorvido aqui
                    system.terminal.handle_keydown(event)
                    
                    # Permite ignorar as teclas de teste 1 a 6 caso o usuário esteja digitando números no prompt
                    if system.terminal.input_text != "":
                         continue
                
                # SIMULAÇÃO DE INPUTS VIA TECLADO PARA TESTAR A ENGINE:
                elif event.key == pygame.K_1:
                    system.bus.publish(Topics.AI_INTENT, {"type": "done"})
                    system.renderer.hud.notifications.push("AI: Estado alterado para IDLE", "ai", priority=1)
                    
                elif event.key == pygame.K_2:
                    system.bus.publish(Topics.AI_INTENT, {"type": "thinking"})
                    system.renderer.hud.notifications.push("AI: Processando requisição...", "ai", priority=1)
                    
                elif event.key == pygame.K_3:
                    system.bus.publish(Topics.AI_INTENT, {"type": "speaking"})
                    system.renderer.hud.notifications.push("AI: Sintetizando resposta por voz", "ai", priority=1)
                
                elif event.key == pygame.K_5:
                    system.bus.publish(Topics.MONITOR_STATE_EMITTED, Mode.WARNING)
                    system.renderer.hud.notifications.push("MONITOR: Anomalia de rede detectada!", "warning", priority=2)
                    
                elif event.key == pygame.K_6:
                    system.bus.publish(Topics.MONITOR_STATE_EMITTED, Mode.ALERT)
                    system.renderer.hud.notifications.push("SISTEMA: CPU CRÍTICA EM 98°C!!", "alert", priority=3)

            # INTERAÇÃO DE ARRASTO DA JANELA (Botão esquerdo do mouse)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.hwnd:
                    self.dragging = True
                    mouse_x, mouse_y = win32api.GetCursorPos()
                    rect = win32gui.GetWindowRect(self.hwnd)
                    self.drag_offset_x = mouse_x - rect[0]
                    self.drag_offset_y = mouse_y - rect[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False

        # Aplica a movimentação se o usuário estiver arrastando a janela
        if self.dragging and self.hwnd:
            mouse_x, mouse_y = win32api.GetCursorPos()
            win32gui.MoveWindow(
                self.hwnd,
                mouse_x - self.drag_offset_x,
                mouse_y - self.drag_offset_y,
                self.width,
                self.height,
                True
            )

        return True

    def close(self):
        """Limpa ganchos globais ao fechar a janela."""
        keyboard.unhook_all()