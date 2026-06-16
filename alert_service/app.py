from flask import Flask, jsonify
from shared.db import fetch_all, execute
from shared.security import require_auth

app = Flask(__name__)

@app.get("/health")
def health():
    return {"service": "alert_service", "status": "online"}

@app.get("/alertas")
@require_auth
def listar_alertas():
    rows = fetch_all(
        """
        SELECT a.id, a.tipo, a.mensagem, a.severidade, a.criado_em, v.placa
        FROM alertas a
        JOIN telemetrias t ON t.id = a.telemetria_id
        JOIN veiculos v ON v.id = t.veiculo_id
        ORDER BY a.id DESC LIMIT 100
        """
    )
    return jsonify(rows)

@app.post("/alertas/<int:alerta_id>/resolver")
@require_auth
def resolver_alerta(alerta_id):
    execute("UPDATE alertas SET resolvido=1 WHERE id=%s", (alerta_id,))
    return jsonify({"mensagem": "alerta resolvido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
