import soundcard as sc
import numpy as np
import serial
import time
import warnings

warnings.filterwarnings("ignore")

# 🔌 Serial ESP32
ser = serial.Serial('COM4', 115200)

# 🎤 Microfone (VB Cable)
mic = sc.get_microphone("CABLE Output (VB-Audio Virtual Cable)")

# 🎚️ número de barras do equalizador
BARS = 12

# 🔥 sensibilidade geral (ajuste aqui)
GAIN = 6

# ⚡ suavização (evita tremedeira)
SMOOTHING = 0.6
prev_values = np.zeros(BARS)

with mic.recorder(samplerate=48000) as rec:
    print("🎵 Visualizador rodando...")

    while True:
        # 📥 captura áudio
        data = rec.record(numframes=4096)
        audio = data[:, 0]

        # 🔥 ganho + janela (essencial)
        audio = audio * GAIN
        audio = audio * np.hanning(len(audio))

        # 📊 FFT
        fft = np.abs(np.fft.rfft(audio))

        # 🎯 bandas logarítmicas corretas
        freqs = np.logspace(np.log10(1), np.log10(len(fft)), BARS + 1).astype(int)

        values = []

        for i in range(BARS):
            chunk = fft[freqs[i]:freqs[i + 1]]

            if len(chunk) > 0:
                # 🔥 energia real (RMS)
                rms = np.sqrt(np.mean(chunk ** 2))
                values.append(rms)
            else:
                values.append(0)

        values = np.array(values)

        # 🔥 compressão estilo áudio (evita 1 barra dominar tudo)
        values = np.log1p(values) * 10

        # 🔥 limite fixo de sensibilidade
        values = np.clip(values, 0, 60)

        # 📏 escala pra 0–255 (ILI9488 / ESP32)
        values = (values / 60) * 255

        # 🔥 suavização (visual mais bonito)
        values = (SMOOTHING * prev_values) + ((1 - SMOOTHING) * values)
        prev_values = values

        values = values.astype(int)

        # 📡 envia pro ESP32
        msg = ",".join(map(str, values)) + "\n"
        ser.write(msg.encode())

        time.sleep(0.01)