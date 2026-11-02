# test_prometheus.py
import requests
from config.settings import PROMETHEUS_URL

print(f"=== TESTANDO CONEXÃO COM: {PROMETHEUS_URL} ===")

queries = {
    'cpu': '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
    'ram': '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    'total_devices': 'network_devices_total',
    'online_devices': 'network_devices_online',
    'unknown_devices': 'network_unknown_devices'
}

for name, q in queries.items():
    try:
        url = f"{PROMETHEUS_URL}/api/v1/query" if not PROMETHEUS_URL.endswith('/api/v1/query') else PROMETHEUS_URL
        r = requests.get(url, params={'query': q}, timeout=3)
        data = r.json()
        results = data.get('data', {}).get('result', [])
        
        if results:
            val = results[0]['value'][1]
            print(f"[SUCESSO] {name} = {val}")
        else:
            print(f"[AVISO] Métrica '{name}' respondeu mas com RESULTADO VAZIO. Dicionário retornado: {data}")
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao consultar '{name}': {e}")