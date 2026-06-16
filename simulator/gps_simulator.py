import json
import random
import time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from shared.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC

ROTAS = [
    {"placa": "ABC1D23", "lat": -23.6815, "lon": -46.6205},
    {"placa": "BRA2E26", "lat": -23.5505, "lon": -46.6333},
    {"placa": "LOG3I21", "lat": -23.9608, "lon": -46.3336},
]

def gerar_payload(veiculo):
    veiculo["lat"] += random.uniform(-0.0012, 0.0012)
    veiculo["lon"] += random.uniform(-0.0012, 0.0012)
    return {
        "placa": veiculo["placa"],
        "latitude": round(veiculo["lat"], 6),
        "longitude": round(veiculo["lon"], 6),
        "velocidade": round(random.uniform(45, 115), 1),
        "temperatura_carga": round(random.uniform(2, 11), 1),
        "combustivel": round(random.uniform(8, 95), 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    print(f"Simulador iniciado. Publicando em mqtt://{MQTT_HOST}:{MQTT_PORT}/{MQTT_TOPIC}")
    while True:
        for veiculo in ROTAS:
            payload = gerar_payload(veiculo)
            client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
            print("[SIMULADOR]", payload)
            time.sleep(2)

if __name__ == "__main__":
    main()
