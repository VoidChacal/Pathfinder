# interface/renderers/hud_renderer.py
import pygame

class HUDRenderer:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 11, bold=True)

    def draw(self, screen, telemetry_data, mode_name, core_color):
        # =====================================================================
        # BLOCO INFERIOR (Status, Temperatura e Anomalias)
        # =====================================================================
        
        # 1. Status do Sistema
        status_text = f">> SYSTEM MODE: {mode_name.upper()}"
        lbl_status = self.font.render(status_text, True, core_color)
        screen.blit(lbl_status, (15, screen.get_height() - 64))

        # 2. Temperatura da CPU (Busca cpu_temp injetado pelo Monitor)
        temp = getattr(telemetry_data, 'cpu_temp', 0.0)
        cpu_text = f">> CPU TEMP: {temp:.1f} °C"
        lbl_cpu = self.font.render(cpu_text, True, core_color)
        screen.blit(lbl_cpu, (15, screen.get_height() - 47))

        # 3. Anomalias da Rede
        anomalies_count = getattr(telemetry_data, 'unknown_devices', 0)
        anomalies_text = f">> NET ANOMALIES: {anomalies_count} detected"
        cor_anomalia = core_color if anomalies_count == 0 else (255, 50, 50)
        lbl_anomalies = self.font.render(anomalies_text, True, cor_anomalia)
        screen.blit(lbl_anomalies, (15, screen.get_height() - 30))

        # =====================================================================
        # BLOCO SUPERIOR (Canto Esquerdo)
        # =====================================================================
        
        cpu_val = getattr(telemetry_data, 'cpu_usage', 0.0)
        ram_val = getattr(telemetry_data, 'ram_usage', 0.0)
        online_dev = getattr(telemetry_data, 'online_devices', 0)
        total_dev = getattr(telemetry_data, 'total_devices', 0)
        sys_status = getattr(telemetry_data, 'system_status', "OK")

        metrics_cpu_ram = f"CPU: {cpu_val:.1f}%  |  RAM: {ram_val:.1f}%"
        devices_info = f"DISPOSITIVOS: {online_dev}/{total_dev} ONLINE"
        network_state = "REDE: ONLINE" if sys_status != "PROM_OFFLINE" else "REDE: DESCONECTADA"
        
        lbl_hardware = self.font.render(metrics_cpu_ram, True, core_color)
        lbl_devices = self.font.render(devices_info, True, core_color)
        lbl_net_status = self.font.render(network_state, True, core_color if network_state == "REDE: ONLINE" else (255, 50, 50))
        
        screen.blit(lbl_hardware, (15, 15))
        screen.blit(lbl_devices, (15, 32))
        screen.blit(lbl_net_status, (15, 49))