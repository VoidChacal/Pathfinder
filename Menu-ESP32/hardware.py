import psutil
import keyboard
import time
import requests

HEADER_MODE = 253
HEADER_HW = 254

def procurar_temp_cpu(node):

    if isinstance(node, dict):

        if (
            node.get("Type") == "Temperature"
            and node.get("Text") == "Core (Tctl/Tdie)"
        ):
            return node.get("Value")

        for value in node.values():

            resultado = procurar_temp_cpu(value)

            if resultado:
                return resultado

    elif isinstance(node, list):

        for item in node:

            resultado = procurar_temp_cpu(item)

            if resultado:
                return resultado

    return None


def get_cpu_temp():

    data = requests.get(
        "http://localhost:8085/data.json"
    ).json()

    temp = procurar_temp_cpu(data)

    if temp:

        temp = (
            temp.replace("°C", "")
                .replace(",", ".")
                .strip()
        )

        return int(float(temp))

    return 0


def run_hardware(ser):

    ser.write(bytes([HEADER_MODE, 2]))

    print("\nHardware Monitor iniciado")
    print("ESC para voltar\n")

    old_recv = psutil.net_io_counters().bytes_recv

    while True:

        if keyboard.is_pressed("esc"):
            print("Voltando...")
            time.sleep(0.3)
            return

        cpu = int(psutil.cpu_percent())

        ram = int(
            psutil.virtual_memory().percent
        )

        new_recv = psutil.net_io_counters().bytes_recv

        net_speed = (new_recv - old_recv)

        old_recv = new_recv

        net_percent = min(
            int(net_speed / 100000),
            100
        )

        
        temp = get_cpu_temp()
        

        packet = bytes([
            HEADER_HW,
            cpu,
            ram,
            net_percent,
            temp
        ])

        ser.write(packet)

        time.sleep(1)