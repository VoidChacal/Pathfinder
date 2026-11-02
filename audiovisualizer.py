import soundcard as sc
import numpy as np
import serial
import time
import warnings

warnings.filterwarnings("ignore")

ser = serial.Serial('COM4', 115200)

mic = sc.get_microphone("CABLE Output (VB-Audio Virtual Cable)")

BARS = 12

with mic.recorder(samplerate=48000) as rec:
    print("🎵 Rodando liso...")

    while True:
        data = rec.record(numframes=4096)

        fft = np.abs(np.fft.rfft(data[:, 0]))

        # criar bandas logarítmicas
        freqs = np.logspace(1, np.log10(len(fft)), BARS+1, dtype=int)

        values = []
        for i in range(BARS):
            start = freqs[i]
            end = freqs[i+1]

            chunk = fft[start:end]

            if len(chunk) > 0:
                values.append(int(np.max(chunk)))
            else:
                values.append(0)

        GAIN = 6

        values = [v * GAIN for v in values]

        max_val = max(values) + 1
        values = [int((v / max_val) * 320) for v in values]

        time.sleep(0.02)