# core/event_bus.py
from collections import defaultdict
# ADICIONE ESTA LINHA AQUI:
from core.topics import Topics 

class EventBus:
    def __init__(self):
        # Cria um dicionário que inicializa uma lista vazia para cada novo tópico
        self._listeners = defaultdict(list)

    def subscribe(self, topic: Topics, callback):
        """Inscreve uma função (callback) para ouvir um tópico específico."""
        self._listeners[topic].append(callback)

    def publish(self, topic: Topics, data=None):
        """Dispara um evento para todos os inscritos daquele tópico."""
        if topic in self._listeners:
            for callback in self._listeners[topic]:
                callback(data)