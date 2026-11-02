#!/usr/bin/env python3

import subprocess
import re
import json
import os
from datetime import datetime
from tau_vii.audio_player import play

NETWORK = "192.168.100.0/24"

KNOWN_FILE = "known_devices.txt"
DB_FILE = "devices_db.json"
EVENT_LOG = "device_events.log"
ALERT_FILE = "alerts.json"

# ==========================================
# STATUS DA REDE
# ==========================================
def internet_ok():

    try:

        gateway = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "192.168.100.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        internet = subprocess.run(
            ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return (
            gateway.returncode == 0 and
            internet.returncode == 0
        )

    except:

        return False

# ==========================================
# ALERTAS
# ==========================================

def create_alert(msg, alert_type="info"):

    alerts = []

    if os.path.exists(ALERT_FILE):

        with open(ALERT_FILE, "r") as f:

            try:
                alerts = json.load(f)
            except:
                alerts = []

    alerts.append({

        "type": alert_type,
        "message": msg

    })

    alerts = alerts[-20:]

    with open(ALERT_FILE, "w") as f:

        json.dump(
            alerts,
            f,
            indent=4
        )

def human_time(delta):

    dias = delta.days

    horas, resto = divmod(
        delta.seconds,
        3600
    )

    minutos, _ = divmod(
        resto,
        60
    )

    return f"{dias}d {horas}h {minutos}m"


# ==========================================
# CARREGAR DISPOSITIVOS CONHECIDOS
# ==========================================

known_devices = {}

if os.path.exists(KNOWN_FILE):

    with open(KNOWN_FILE, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if "|" not in line:
                continue

            mac, name = line.split("|", 1)

            known_devices[
                mac.strip().upper()
            ] = name.strip()


# ==========================================
# CARREGAR BANCO DE DADOS
# ==========================================

if os.path.exists(DB_FILE):

    with open(DB_FILE, "r") as f:

        devices_db = json.load(f)

else:

    devices_db = {}


# ==========================================
# ESTADO ANTERIOR
# ==========================================

previous_online = set()

for mac, info in devices_db.items():

    if info.get("online", False):

        previous_online.add(mac)


# ==========================================
# EXECUTAR NMAP
# ==========================================

print(f"\nEscaneando rede {NETWORK}...\n")

result = subprocess.run(
    ["sudo", "nmap", "-sn", NETWORK],
    capture_output=True,
    text=True
)

output = result.stdout


# ==========================================
# PROCESSAR RESULTADO
# ==========================================

current_devices = set()
unknown_devices = []

current_ip = None

now = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
)

internet_status = internet_ok()

for line in output.splitlines():

    ip_match = re.search(
        r"Nmap scan report for (.+)",
        line
    )

    if ip_match:

        current_ip = ip_match.group(1)

    mac_match = re.search(
        r"MAC Address: ([0-9A-F:]+) \((.+)\)",
        line
    )

    if mac_match and current_ip:

        mac = mac_match.group(1).upper()
        vendor = mac_match.group(2)

        current_devices.add(mac)

        was_online = devices_db.get(
            mac,
            {}
        ).get(
            "online",
            False
        )

        if mac not in devices_db:

            devices_db[mac] = {

                "name":
                known_devices.get(
                    mac,
                    "DESCONHECIDO"
                ),

                "vendor":
                vendor,

                "ip":
                current_ip,

                "first_seen":
                now,

                "last_seen":
                now,

                "online":
                True,

                "online_since":
                now,

                "offline_since":
                None
            }

        else:

            if not was_online:

                devices_db[mac][
                    "online_since"
                ] = now
            if mac in known_devices:

                devices_db[mac]["name"] = known_devices[mac]

            devices_db[mac]["ip"] = current_ip
            devices_db[mac]["vendor"] = vendor
            devices_db[mac]["last_seen"] = now
            devices_db[mac]["online"] = True

        if mac in known_devices:

            print(
                f"[OK] "
                f"{known_devices[mac]} "
                f"({current_ip})"
            )

        else:

            unknown_devices.append(
                (
                    current_ip,
                    mac,
                    vendor
                )
            )

if len(unknown_devices) > 0:

    with open(EVENT_LOG, "a") as log:

        log.write(
            f"{now} [ALERTA_INVASAO] "
            f"{len(unknown_devices)} "
            f"desconhecidos\n"
        )


# ==========================================
# MARCAR OFFLINE
# ==========================================

for mac in devices_db:

    if mac not in current_devices:

        if devices_db[mac]["online"]:

            devices_db[mac]["offline_since"] = now
            devices_db[mac]["online"] = False

            subprocess.Popen([
                "aplay",
                "II_TAU-VII-1_II/audio/desconectado.wav"
            ])

# ==========================================
# EVENTOS
# ==========================================

new_devices = (
    current_devices
    - previous_online
)

gone_devices = (
    previous_online
    - current_devices
)

with open(EVENT_LOG, "a") as log:

    if any(
        devices_db[mac]["name"] == "DESCONHECIDO"
        for mac in new_devices
    ):

        subprocess.Popen([
            "aplay",
            "II_TAU-VII-1_II/audio/alerta.wav"
        ])

    elif new_devices:

        subprocess.Popen([
            "aplay",
            "II_TAU-VII-1_II/audio/conectado.wav"
        ])

    for mac in new_devices:

        nome = devices_db[mac]["name"]

        log.write(
            f"{now} "
            f"[ENTROU] "
            f"{nome} "
            f"({mac})\n"
        )

    for mac in gone_devices:

        nome = devices_db[mac]["name"]

        log.write(
            f"{now} "
            f"[SAIU] "
            f"{nome} "
            f"({mac})\n"
        )

    if internet_status:

        log.write(
            f"{now} [REDE_ESTAVEL]\n"
        )

    else:

        log.write(
            f"{now} [REDE_DESCONECTADA]\n"
        )


# ==========================================
# DESCONHECIDOS
# ==========================================

print("\n====================")
print("DESCONHECIDOS")
print("====================")

if not unknown_devices:

    print("Nenhum")

else:

    for ip, mac, vendor in unknown_devices:

        print(
            f"{ip} | "
            f"{mac} | "
            f"{vendor}"
        )


# ==========================================
# TABELA
# ==========================================

print("\n====================")
print("DISPOSITIVOS")
print("====================")

agora = datetime.now()

for mac, info in devices_db.items():

    nome = info["name"]

    if info["online"]:

        inicio = datetime.strptime(
            info["online_since"],
            "%Y-%m-%d %H:%M:%S"
        )

        tempo = human_time(
            agora - inicio
        )

        status = (
            f"ONLINE "
            f"({tempo})"
        )

    else:

        if info["offline_since"]:

            inicio = datetime.strptime(
                info["offline_since"],
                "%Y-%m-%d %H:%M:%S"
            )

            tempo = human_time(
                agora - inicio
            )

            status = (
                f"OFFLINE "
                f"({tempo})"
            )

        else:

            status = "OFFLINE"

    print(
        f"{nome:<25}"
        f"{info['ip']:<18}"
        f"{status}"
    )

# ==========================================
# PROMETHEUS EXPORTER
# ==========================================

PROM_FILE = "/var/lib/node_exporter/textfile_collector/network_devices.prom"

total_devices = len(devices_db)

online_devices = sum(
    1 for d in devices_db.values()
    if d["online"]
)

offline_devices = total_devices - online_devices

unknown_count = sum(
    1 for mac in current_devices
    if mac not in known_devices
)

with open(PROM_FILE, "w") as f:

    for mac, info in devices_db.items():

        nome = info["name"].replace(" ", "_")

        status = 1 if info["online"] else 0

        uptime = 0

        if info["online"]:

            inicio = datetime.strptime(
                info["online_since"],
                "%Y-%m-%d %H:%M:%S"
            )

            uptime = int(
                (datetime.now() - inicio)
                .total_seconds()
            )

        vendor = (
            info.get(
            "vendor",
            "Unknown"
            )
            .replace('"', '')
        )

        f.write(
            f'network_device_online{{'
            f'device="{nome}",'
            f'ip="{info["ip"]}",'
            f'mac="{mac}",'
            f'vendor="{vendor}"'
            f'}} {status}\n'
        )

        f.write(
             f'network_device_uptime_seconds{{device="{nome}",mac="{mac}"}} {uptime}\n'
        )


    f.write(
        f"network_devices_total {total_devices}\n"
    )

    f.write(
        f"network_devices_online {online_devices}\n"
    )

    f.write(
        f"network_devices_offline {offline_devices}\n"
    )

    f.write(
        f"network_unknown_devices {unknown_count}\n"
    )

print(
    f"\nArquivo Prometheus atualizado:"
    f" {PROM_FILE}"
)

# ==========================================
# SALVAR BANCO
# ==========================================

with open(DB_FILE, "w") as f:

    json.dump(
        devices_db,
        f,
        indent=4
    )

print("\nBanco atualizado.")

