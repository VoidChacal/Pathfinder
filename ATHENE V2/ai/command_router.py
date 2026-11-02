# ai/command_router.py
from core.topics import Topics

class CommandRouter:
    def __init__(self, event_bus):
        self.bus = event_bus
        # Se inscreve para capturar as intenções puras extraídas da IA
        self.bus.subscribe(Topics.COMMAND, self.execute)

    def execute(self, command: dict):
        intent = command.get("intent")
        action = command.get("action")

        if intent == "network_monitor":
            # Roteia especificamente para o controlador do monitor de infraestrutura
            self.bus.publish(Topics.MONITOR_CONTROL, action)
            
        elif intent == "theme":
            self.bus.publish(Topics.UI_THEME, action)
            
        elif intent == "shutdown":
            self.bus.publish(Topics.SYSTEM_SHUTDOWN)
            
        else:
            print(f"[COMMAND ROUTER] Intenção desconhecida recebida: {intent}")