import json
import threading
from datetime import datetime, timezone
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
from shared.config import MQTT_HOST, MQTT_PORT, MQTT_TOPIC
from shared.db import execute, fetch_all, fetch_one
from shared.security import require_auth

app = Flask(__name__)

class TelemetryFactory:
    """Factory Method: normaliza diferentes tipos de sensores em um payload único."""
    @staticmethod
    def create(payload: dict) -> dict:
        return {
            "placa": payload.get("placa", "SEMPLACA"),
            "latitude": float(payload.get("latitude", 0)),
            "longitude": float(payload.get("longitude", 0)),
            "velocidade": float(payload.get("velocidade", 0)),
            "temperatura_carga": float(payload.get("temperatura_carga", payload.get("temperatura", 0))),
            "combustivel": float(payload.get("combustivel", 0)),
            "timestamp_evento": payload.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }

class AlertObserver:
    """Observer: observa novas telemetrias e registra alertas automaticamente."""
    def notify(self, telemetria_id: int, data: dict):
        alertas = []
        if data["velocidade"] > 100:
            alertas.append(("VELOCIDADE", f"Veículo {data['placa']} acima do limite: {data['velocidade']} km/h"))
        if data["temperatura_carga"] > 8:
            alertas.append(("TEMPERATURA", f"Carga do veículo {data['placa']} acima de 8°C: {data['temperatura_carga']}°C"))
        if data["combustivel"] < 15:
            alertas.append(("COMBUSTIVEL", f"Veículo {data['placa']} com combustível abaixo de 15%"))
        for tipo, mensagem in alertas:
            execute(
                "INSERT INTO alertas(telemetria_id, tipo, mensagem, severidade) VALUES (%s, %s, %s, %s)",
                (telemetria_id, tipo, mensagem, "ALTA" if tipo in ["VELOCIDADE", "TEMPERATURA"] else "MEDIA"),
            )

observer = AlertObserver()

def salvar_telemetria(data: dict):
    veiculo = fetch_one("SELECT id FROM veiculos WHERE placa=%s", (data["placa"],))
    if not veiculo:
        veiculo_id = execute("INSERT INTO veiculos(placa, motorista, status) VALUES (%s, %s, %s)", (data["placa"], "Motorista não informado", "ATIVO"))
    else:
        veiculo_id = veiculo["id"]

    telemetria_id = execute(
        """
        INSERT INTO telemetrias(veiculo_id, latitude, longitude, velocidade, temperatura_carga, combustivel, timestamp_evento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (veiculo_id, data["latitude"], data["longitude"], data["velocidade"], data["temperatura_carga"], data["combustivel"], data["timestamp_evento"].replace("Z", "+00:00")),
    )
    observer.notify(telemetria_id, data)
    return telemetria_id

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[MQTT] conectado: {reason_code}; assinando {MQTT_TOPIC}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        data = TelemetryFactory.create(payload)
        telemetria_id = salvar_telemetria(data)
        print(f"[MQTT] telemetria salva id={telemetria_id} placa={data['placa']}")
    except Exception as exc:
        print(f"[ERRO MQTT] {exc}")

def iniciar_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    client.loop_forever()

@app.get("/health")
def health():
    return {"service": "tracking_service", "status": "online", "mqtt_topic": MQTT_TOPIC}

@app.post("/telemetrias")
@require_auth
def criar_telemetria_http():
    data = TelemetryFactory.create(request.get_json() or {})
    telemetria_id = salvar_telemetria(data)
    return jsonify({"id": telemetria_id, "mensagem": "telemetria salva"}), 201

@app.get("/telemetrias")
@require_auth
def listar_telemetrias():
    rows = fetch_all(
        """
        SELECT t.id, v.placa, t.latitude, t.longitude, t.velocidade, t.temperatura_carga, t.combustivel, t.criado_em
        FROM telemetrias t JOIN veiculos v ON v.id=t.veiculo_id
        ORDER BY t.id DESC LIMIT 50
        """
    )
    return jsonify(rows)

@app.get("/veiculos")
@require_auth
def listar_veiculos():
    return jsonify(fetch_all("SELECT * FROM veiculos ORDER BY placa"))

if __name__ == "__main__":
    t = threading.Thread(target=iniciar_mqtt, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5001, debug=True)
