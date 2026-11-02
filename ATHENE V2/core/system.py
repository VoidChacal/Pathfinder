# core/system.py
from core.event_bus import EventBus
from core.state import AtheneStateManager
from core.datastore import AtheneDataStore
from core.brain import AtheneBrain
from monitor.monitor import MonitorController
from ai.chatbot import AtheneChatbot
from ai.command_router import CommandRouter

class AtheneSystem:
    def __init__(self):
        self.bus = None
        self.state_manager = None
        self.datastore = None
        self.monitor = None
        self.chatbot = None
        self.router = None
        self.brain = None

    def initialize(self):
        """Instancia os componentes e estabelece as amarras do EventBus."""
        self.bus = EventBus()
        self.state_manager = AtheneStateManager(self.bus)
        self.datastore = AtheneDataStore(self.bus)
        
        self.monitor = MonitorController(self.bus, self.datastore)
        self.chatbot = AtheneChatbot(self.bus, self.datastore)
        self.router = CommandRouter(self.bus)
        self.brain = AtheneBrain(self.bus, self.state_manager)
        print("[SYSTEM] Ciclo de Inicialização concluído.")

    def start(self):
        """Dispara a execução dos serviços de background."""
        if self.monitor:
            self.monitor.start()
        print("[SYSTEM] Todos os serviços secundários ativos.")

    def shutdown(self):
        """Garante o encerramento seguro e limpo de todas as threads."""
        if self.monitor:
            self.monitor.stop()
        print("[SYSTEM] Desligamento do ecossistema executado.")