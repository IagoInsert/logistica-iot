import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "logistica123"),
    "database": os.getenv("MYSQL_DATABASE", "logistica_iot"),
}

JWT_SECRET = os.getenv("JWT_SECRET", "troque_este_segredo_em_producao")
JWT_EXP_MINUTES = int(os.getenv("JWT_EXP_MINUTES", "120"))

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "frota/telemetria")
