from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import deque

# ================= CONFIG =================
START_FREQ = 88e6
END_FREQ   = 108e6
STEP       = 200e3

SAMPLE_RATE = 2.4e6
GAIN = 25

HISTORY_LENGTH = 60   # quantas varreduras ficam no mapa (tempo)
SAMPLES = 256 * 1024

# ================= SETUP =================
sdr = RtlSdr()
sdr.sample_rate = SAMPLE_RATE
sdr.gain = GAIN

freq_list = np.arange(START_FREQ, END_FREQ + STEP, STEP) / 1e6
history = deque(maxlen=HISTORY_LENGTH)

plt.ion()
fig, ax = plt.subplots()
heatmap = None

print("Radar RF Passivo - Mapa de Calor Iniciado")
print("CTRL+C para sair\n")

# ================= LOOP =================
try:
    while True:
        row = []

        for f_mhz in freq_list:
            f_hz = f_mhz * 1e6
            sdr.center_freq = f_hz

            samples = sdr.read_samples(SAMPLES)
            psd = np.abs(np.fft.fft(samples))**2
            pwr = 10 * np.log10(np.mean(psd))

            row.append(pwr)
            print(f"{f_mhz:.2f} MHz → {pwr:.1f} dB")

            time.sleep(0.05)

        history.append(row)

        data = np.array(history)

        ax.clear()
        heatmap = ax.imshow(
            data,
            aspect='auto',
            origin='lower',
            cmap='inferno'
        )

        ax.set_title("Radar RF Passivo - Mapa de Calor")
        ax.set_xlabel("Frequência (MHz)")
        ax.set_ylabel("Tempo (Varreduras)")

        ax.set_xticks(np.arange(0, len(freq_list), max(1, len(freq_list)//10)))
        ax.set_xticklabels(
            [f"{freq_list[i]:.1f}" for i in ax.get_xticks().astype(int)]
        )

        plt.pause(0.01)

except KeyboardInterrupt:
    print("\nEncerrando...")

finally:
    sdr.close()
