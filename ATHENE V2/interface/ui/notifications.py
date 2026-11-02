# interface/ui/notifications.py

class NotificationItem:
    def __init__(
        self, 
        message: str, 
        notification_type: str = "info", 
        priority: str = "NORMAL", 
        duration: float = 3.0,
        fade_in: float = 0.3,
        fade_out: float = 0.5
    ):
        self.message = message
        self.type = notification_type
        self.priority = priority
        self.duration = duration
        self.fade_in = fade_in
        self.fade_out = fade_out
        
        # Dados físicos e temporais dinâmicos
        self.time_alive = 0.0
        self.alpha = 0
        self.is_dead = False

        # Tabela de pesos para ordenação (Maior número = Topo da fila)
        self.PRIORITY_WEIGHTS = {
            "LOW": 0,
            "NORMAL": 1,
            "HIGH": 2,
            "CRITICAL": 3
        }

    @property
    def weight(self) -> int:
        return self.PRIORITY_WEIGHTS.get(self.priority, 1)

import pygame
from interface.themes import THEMES
from core.modes import Mode

# interface/ui/notifications.py (Continuação)

class NotificationManager:
    def __init__(self, max_notifications: int = 3):
        self.collection = []
        self.max_notifications = max_notifications

    def push(self, message: str, notification_type: str = "info", priority: str = "NORMAL", duration: float = 3.0):
        """Insere uma notificação e reordena a fila instantaneamente por prioridade."""
        new_item = NotificationItem(message, notification_type, priority, duration)
        self.collection.append(new_item)
        
        # Ordena: maior prioridade primeiro (vai para o topo visual)
        self.collection.sort(key=lambda item: item.weight, reverse=True)
        
        # Remove o excedente de menor prioridade se estourar o limite da tela
        if len(self.collection) > self.max_notifications:
            self.collection.pop() # Remove o último da lista ordenada (menor peso)

    def update(self, dt: float):
        """Atualiza a física dos tempos e calcula as curvas de opacidade alpha."""
        for item in self.collection:
            item.time_alive += dt
            
            # Curva de Fade-In customizada do objeto
            if item.time_alive < item.fade_in:
                item.alpha = int((item.time_alive / item.fade_in) * 255)
            # Curva de Fade-Out customizada do objeto
            elif item.time_alive > (item.duration - item.fade_out):
                remaining = item.duration - item.time_alive
                item.alpha = int(max(0, (remaining / item.fade_out) * 255))
            else:
                item.alpha = 255

            if item.time_alive >= item.duration:
                item.is_dead = True

        # Limpa as entidades mortas
        self.collection = [n for n in self.collection if not n.is_dead]