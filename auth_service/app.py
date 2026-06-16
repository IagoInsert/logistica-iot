from flask import Flask, request, jsonify
from shared.db import fetch_one, execute
from shared.security import verify_password, create_token, hash_password

app = Flask(__name__)

@app.get("/health")
def health():
    return {"service": "auth_service", "status": "online"}

@app.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    senha = data.get("senha")
    if not email or not senha:
        return jsonify({"erro": "email e senha são obrigatórios"}), 400

    usuario = fetch_one("SELECT * FROM usuarios WHERE email=%s", (email,))
    if not usuario or not verify_password(senha, usuario["senha_hash"]):
        return jsonify({"erro": "credenciais inválidas"}), 401

    token = create_token(usuario["id"], usuario["nome"], usuario["perfil"])
    return jsonify({"token": token, "usuario": {"id": usuario["id"], "nome": usuario["nome"], "perfil": usuario["perfil"]}})

@app.post("/usuarios")
def criar_usuario():
    data = request.get_json() or {}
    campos = ["nome", "email", "senha"]
    if any(c not in data for c in campos):
        return jsonify({"erro": "nome, email e senha são obrigatórios"}), 400

    perfil = data.get("perfil", "operador")
    senha_hash = hash_password(data["senha"])
    user_id = execute(
        "INSERT INTO usuarios(nome, email, senha_hash, perfil) VALUES (%s, %s, %s, %s)",
        (data["nome"], data["email"], senha_hash, perfil),
    )
    return jsonify({"id": user_id, "mensagem": "usuário criado"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
