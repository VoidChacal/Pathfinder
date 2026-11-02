from rtlsdr import RtlSdr
import numpy as np
import matplotlib.pyplot as plt
import time

sdr = RtlSdr()

# Config
sdr.sample_rate = 2.4e6
sdr.gain = 25

START_FREQ = 88e6
END_FREQ = 108e6
STEP = 200e3

freqs = []
power = []

print("Iniciando varredura RF...")

f = START_FREQ
while f <= END_FREQ:
    sdr.center_freq = f
    samples = sdr.read_samples(256*1024)
    psd = np.abs(np.fft.fft(samples))**2
    pwr = 10 * np.log10(np.mean(psd))

    freqs.append(f / 1e6)
    power.append(pwr)

    print(f"{f/1e6:.2f} MHz → {pwr:.1f} dB")
    f += STEP
    time.sleep(0.1)

sdr.close()

# Plot
plt.plot(freqs, power)
plt.xlabel("Frequência (MHz)")
plt.ylabel("Potência (dB)")
plt.title("Radar RF Passivo - Mapa de Energia")
plt.show()
