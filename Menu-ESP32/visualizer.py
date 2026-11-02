import soundcard as sc
import numpy as np
import keyboard
import time

HEADER_MODE = 253
HEADER_VIS = 255

BARS = 12
GAIN = 7
SMOOTHING = 0.5

def run_visualizer(ser):

    ser.write(bytes([HEADER_MODE, 1]))

    prev_values = np.zeros(BARS)

    mic = sc.get_microphone(
        "CABLE Output (VB-Audio Virtual Cable)"
    )

    print("\nVisualizer iniciado")
    print("ESC para voltar\n")

    with mic.recorder(samplerate=48000) as rec:

        while True:

            if keyboard.is_pressed("esc"):
                print("Voltando...")
                time.sleep(0.3)
                return

            data = rec.record(numframes=2048)

            audio = data[:,0]

            audio *= GAIN
            audio *= np.hanning(len(audio))

            fft = np.abs(np.fft.rfft(audio))

            freqs = np.logspace(
                np.log10(1),
                np.log10(len(fft)),
                BARS + 1
            ).astype(int)

            values = []

            for i in range(BARS):

                chunk = fft[freqs[i]:freqs[i+1]]

                if len(chunk):
                    rms = np.sqrt(np.mean(chunk**2))
                    values.append(rms)
                else:
                    values.append(0)

            values = np.array(values)

            values = np.log1p(values) * 10
            values = np.clip(values,0,60)
            values = (values/60)*255

            values = (
                SMOOTHING * prev_values
                +
                (1-SMOOTHING)*values
            )

            prev_values = values

            values = values.astype(np.uint8)

            packet = bytes([HEADER_VIS]) + values.tobytes()

            ser.write(packet)

            time.sleep(0.005)

            if tecla_ESC:
                return