# core/datastore.py

class AtheneDataStore:
    def __init__(self, event_bus):
        self._metrics = {}
        self._network = {}
        self._monitor_running = False

    def update_metrics(self, data: dict): self._metrics.update(data)
    def update_network(self, data: dict): self._network.update(data)
    def set_monitor_running(self, state: bool): self._monitor_running = state

    # Métodos Públicos Seguros
    def get_metrics(self) -> dict: return self._metrics.copy()
    def get_network(self) -> dict: return self._network.copy()
    def is_monitor_running(self) -> bool: return self._monitor_running
    def get_snapshot(self) -> dict:
        return {"metrics": self.get_metrics(), "network": self.get_network()}