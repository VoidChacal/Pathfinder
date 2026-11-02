# config/settings.py
import os

# --- CONFIGURAÇÕES DA JANELA / GRÁFICOS ---
WIDTH = 400
HEIGHT = 400
FPS = 60
NUM_STARS = 50

# --- TELEMETRIA & INFRAESTRUTURA ---
PROMETHEUS_URL = "http://192.168.100.104:9091/api/v1/query"
POLLING_INTERVAL = 15  # Segundos entre checagens do Prometheus

# --- CAMADA DE INTELIGÊNCIA (LLM) ---
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

# --- PROTOCOLO DE LIMITES ---
MIN_MODE_DURATION = 1.5  # Tempo mínimo (segundos) para sustentar um estado visual