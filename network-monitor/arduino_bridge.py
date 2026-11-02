#!/usr/bin/env python3
import time
import os
import json
import serial
from datetime import datetime

# Configurações
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
DB_FILE = "devices_db.json"
EVENT_LOG = "device_events.log"

def conectar_arduino():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        time.sleep(2) # Aguarda o reset automático do Arduino ao abrir a porta
        print(f"Conectado ao Arduino na porta {SERIAL_PORT}")
        return ser
    except Exception as e:
        print(f"Erro ao conectar na serial: {e}")
        return None

def obter_dados_db():
    """Lê o devices_db.json para extrair contagens e status da rede"""
    total_dispositivos = 0
    total_alertas = 0
    status_rede = "ONLINE"

    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                db = json.load(f)
                total_dispositivos = len(db)
                # Conta quantos dispositivos estão com status desconhecido/alerta
                for mac, info in db.items():
                    if info.get("name") == "DESCONHECIDO" and info.get("online", False):
                        total_alertas += 1
        except Exception as e:
            print(f"Erro ao ler JSON: {e}")

    return total_dispositivos, total_alertas, status_rede

def processar_evento_recente(linha):
    """Traduz a linha do log para comandos de texto do LCD"""
    linha = linha.strip()
    if "[ALERTA_INVASAO]" in linha:
        return "MSG:!! WARNING !!;Unknown device\n"
    elif "[ENTROU]" in linha:
        return "MSG:NOVO DISPOSITIVO;Conectado na rede\n"
    elif "[REDE_DESCONECTADA]" in linha:
        return "MSG:MODE ALERT;Status: OFFLINE\n"
    elif "[REDE_ESTAVEL]" in linha:
        return "MSG:MODE MONITOR;Status: ONLINE\n"
    return None

def main():
    ser = conectar_arduino()

    # Prepara para ler o log a partir do final (apenas novos eventos)
    if os.path.exists(EVENT_LOG):
        log_file = open(EVENT_LOG, "r")
        log_file.seek(0, 2)
    else:
        log_file = None
        print(f"Aviso: {EVENT_LOG} ainda não existe. Aguardando...")

    print("Ponte do Arduino iniciada. Pressione Ctrl+C para sair.")

    ultimo_envio_dados = 0

    try:
        while True:
            # 1. Verifica se há novos eventos no log de rede
            if log_file:
                linha = log_file.readline()
                if linha and ser and ser.is_open:
                    cmd_lcd = processar_evento_recente(linha)
                    if cmd_lcd:
                        ser.write(cmd_lcd.encode('utf-8'))

            # 2. Verifica se o Arduino enviou algum comando (ex: Botão de Scan Manual)
            if ser and ser.is_open and ser.in_waiting > 0:
                try:
                    comando = ser.readline().decode('utf-8').strip()
                    if comando == "CMD:FORCED_SCAN":
                        print("[HARDWARE] Botão de Scan Manual pressionado no Arduino!")
                        ser.write(b"MSG:SCAN MANUAL;Executando nmap...\n")

                        # Executa o seu monitor.py original para varrer a rede
                        import subprocess
                        subprocess.run(["sudo", "python3", "monitor.py"])

                        ser.write(b"MSG:SCAN COMPLETE;Rede atualizada!\n")
                except Exception as e:
                    print(f"Erro ao ler comando da serial: {e}")

            # 3. Envia periodicamente os dados consolidados para o Display de 4 Dígitos (a cada 2 segundos)
            tempo_atual = time.time()
            if tempo_atual - ultimo_envio_dados >= 2.0:
                if ser and ser.is_open:
                    hora_atual = datetime.now().strftime("%H%M")
                    disp, alertas, _ = obter_dados_db()

                    # Formato esperado pelo Arduino: DAT:HHMM,Dispositivos,Alertas,Banda,Status
                    # (Colocando 0 provisório para largura de banda caso não venha de outro lugar)
                    payload = f"DAT:{hora_atual},{disp},{alertas},0,ONLINE\n"
                    ser.write(payload.encode('utf-8'))

                ultimo_envio_dados = tempo_atual

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nEncerrando bridge do Arduino...")
        if log_file:
            log_file.close()
        if ser and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()
