# main.py
import pygame
import sys
from config.settings import WIDTH, HEIGHT, FPS
from core.state import AtheneStateManager
from core.event_bus import EventBus
from core.datastore import AtheneDataStore
from core.brain import AtheneBrain  # <-- IMPORTADO O CÉREBRO
from interface.scene import Scene
from interface.window import Window  
from monitor.monitor import MonitorService
from ai.chatbot import AtheneChatbot
from interface.ui.chat_window import AtheneChatWindow

def main():
    window = Window(WIDTH, HEIGHT, "Athene HUD")
    clock = pygame.time.Clock()

    # Inicialização da infraestrutura central de dados e eventos
    event_bus = EventBus()
    state_manager = AtheneStateManager(event_bus)
    datastore = AtheneDataStore(event_bus)  
    scene = Scene(state_manager)

    # Inicialização dos serviços e IA background
    chatbot = AtheneChatbot(event_bus, datastore)
    chat_window = AtheneChatWindow(event_bus)
    chat_window.start()
    
    monitor = MonitorService(datastore=datastore, event_bus=event_bus)
    monitor.start()

    # Instancia o Cérebro passando o contexto necessário
    brain = AtheneBrain(event_bus, state_manager, scene)

    # Contexto mínimo limpo para o window.handle_events processar macros de teclas se necessário
    class DummySystem:
        def __init__(self, bus, scene):
            self.bus = bus
            self.renderer = scene
    system_context = DummySystem(event_bus, scene)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        if not window.handle_events(system_context):
            running = False
                
        telemetry_data = monitor.get_latest_telemetry()
        
        # DELEGADO: O cérebro processa o modo correto baseado na telemetria atual
        brain.resolve_system_mode(telemetry_data)
        
        # Atualização lógica da física e cinética dos objetos do Pygame
        scene.update(dt)
        
        # Renderização gráfica limpa
        window.screen.fill((0, 0, 0))
        scene.draw(window.screen)
        
        scene.hud_renderer.draw(
            window.screen, 
            telemetry_data, 
            state_manager.mode.name, 
            scene.core.color
        )

        pygame.display.flip()

    # Desligamento seguro
    window.close()
    monitor.stop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()