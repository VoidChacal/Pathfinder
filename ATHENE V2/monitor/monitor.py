# monitor/monitor.py
import threading
import time
import requests
from config.settings import PROMETHEUS_URL, POLLING_INTERVAL
from core.telemetry import TelemetryData
from core.topics import Topics  # Importando os tópicos

class MonitorService:
    # Ajustado o construtor para receber de forma opcional o datastore e o event_bus
    def __init__(self, datastore=None, event_bus=None):
        self.telemetry = TelemetryData()
        self.datastore = datastore
        self.bus = event_bus
        self.is_running = False
        self._thread = None
        # Garante que o atributo esperado pelo HUDRenderer exista
        self.telemetry.cpu_temp = 0.0  

    def start(self):
        self.is_running = True
        self._thread = threading.Thread(target=self._main_loop, daemon=True)
        self._thread.start()
        # Notifica o barramento que o monitoramento real começou
        if self.bus:
            self.bus.publish(Topics.SYSTEM_LOG, "[SYSTEM]: Conexão ativa com o cluster Prometheus.")

    def stop(self):
        self.is_running = False

    def get_latest_telemetry(self) -> TelemetryData:
        return self.telemetry

    # monitor/monitor.py (Substitua apenas este método)

    def _main_loop(self):
        while self.is_running:
            self._fetch_prometheus()
            
            # 1. Alimenta o DataStore centralizado com chaves limpas para o Chatbot ler
            if self.datastore:
                self.datastore.update_metrics({
                    "cpu": round(self.telemetry.cpu_usage, 2),
                    "ram": round(self.telemetry.ram_usage, 2),
                    "temp": round(getattr(self.telemetry, 'cpu_temp', 0.0), 2),
                    "status": self.telemetry.system_status
                })
                self.datastore.update_network({
                    "total_devices": self.telemetry.total_devices,
                    "online_devices": self.telemetry.online_devices,
                    "unknown_devices": self.telemetry.unknown_devices
                })
                
            time.sleep(POLLING_INTERVAL)

    # monitor/monitor.py (Substitua a função _fetch_prometheus por esta)

    def _fetch_prometheus(self):
        try:
            queries = {
                'cpu': '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
                'ram': '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
                'temp': 'node_hwmon_temp_celsius{sensor="core 0"} or node_hwmon_temp_celsius or (node_thermal_zone_temp)',
                'total_devices': 'network_devices_total',
                'online_devices': 'network_devices_online',
                'unknown_devices': 'network_unknown_devices'
            }
            
            # 1. CPU
            r_cpu = requests.get(PROMETHEUS_URL, params={'query': queries['cpu']}, timeout=3).json()
            if r_cpu.get('data', {}).get('result'):
                self.telemetry.cpu_usage = float(r_cpu['data']['result'][0]['value'][1])
            else:
                print("[PROM DEBUG] CPU query retornou vazia:", r_cpu)

            # 2. RAM
            r_ram = requests.get(PROMETHEUS_URL, params={'query': queries['ram']}, timeout=3).json()
            if r_ram.get('data', {}).get('result'):
                self.telemetry.ram_usage = float(r_ram['data']['result'][0]['value'][1])
            else:
                print("[PROM DEBUG] RAM query retornou vazia:", r_ram)

            # 3. Dispositivos Totais
            r_total = requests.get(PROMETHEUS_URL, params={'query': queries['total_devices']}, timeout=3).json()
            if r_total.get('data', {}).get('result'):
                self.telemetry.total_devices = int(r_total['data']['result'][0]['value'][1])

            # 4. Dispositivos Online
            r_online = requests.get(PROMETHEUS_URL, params={'query': queries['online_devices']}, timeout=3).json()
            if r_online.get('data', {}).get('result'):
                self.telemetry.online_devices = int(r_online['data']['result'][0]['value'][1])

            # 5. Dispositivos Desconhecidos (Invasores)
            r_unknown = requests.get(PROMETHEUS_URL, params={'query': queries['unknown_devices']}, timeout=3).json()
            if r_unknown.get('data', {}).get('result'):
                self.telemetry.unknown_devices = int(r_unknown['data']['result'][0]['value'][1])

            # 6. Temperatura
            r_temp = requests.get(PROMETHEUS_URL, params={'query': queries['temp']}, timeout=3).json()
            if r_temp.get('data', {}).get('result'):
                self.telemetry.cpu_temp = float(r_temp['data']['result'][0]['value'][1])
            else:
                self.telemetry.cpu_temp = 42.0 # Valor padrão visual caso não exista sensor térmico no OS

            self.telemetry.system_status = "OK"

        except Exception as e:
            # MOSTRA O ERRO REAL NO TERMINAL
            print(f"[PROM ERROR] Falha na conexão/requisição com o Prometheus ({PROMETHEUS_URL}): {e}")
            self.telemetry.system_status = "PROM_OFFLINE"