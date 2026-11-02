# core/telemetry.py

class TelemetryData:
    def __init__(self):
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        self.disk_usage = 0.0
        self.total_devices = 0
        self.online_devices = 0
        self.unknown_devices = 0  # ADICIONADO: Contador de invasores/desconhecidos
        self.system_status = "OK"