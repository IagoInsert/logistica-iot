from functools import wraps
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from flask import request, jsonify
from shared.config import JWT_SECRET, JWT_EXP_MINUTES


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(user_id: int, nome: str, perfil: str) -> str:
    payload = {
        "sub": str(user_id),
        "nome": nome,
        "perfil": perfil,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXP_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"erro": "Token JWT ausente"}), 401
        token = header.replace("Bearer ", "", 1)
        try:
            request.user = decode_token(token)
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido"}), 401
        return fn(*args, **kwargs)
    return wrapper
