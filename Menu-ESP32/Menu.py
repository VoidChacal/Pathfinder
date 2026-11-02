import serial

from visualizer import run_visualizer
from hardware import run_hardware

PORT = "COM4"
BAUD = 921600

HEADER_MODE = 253

MODE_VISUALIZER = 1
MODE_HARDWARE = 2


def clear():
    print("\n" * 50)


def main():

    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)

    except Exception as e:
        print(f"Erro ao abrir serial: {e}")
        return

    while True:

        clear()

        print("================================")
        print("       ESP32 DASHBOARD")
        print("================================")
        print()
        print("1 - Music Visualizer")
        print("2 - Hardware Monitor")
        print("3 - Server Status")
        print("4 - LUMI/TAU Log")
        print()
        print("0 - Sair")
        print()

        op = input("Escolha: ")

        if op == "1":

            ser.write(
                bytes([
                    HEADER_MODE,
                    MODE_VISUALIZER
                ])
            )

            run_visualizer(ser)

        elif op == "2":

            ser.write(
                bytes([
                    HEADER_MODE,
                    MODE_HARDWARE
                ])
            )

            run_hardware(ser)

        elif op == "0":
            break

    ser.close()


if __name__ == "__main__":
    main()