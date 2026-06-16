import concurrent.futures
import statistics
import time
import requests

BASE_AUTH = "http://localhost:5000"
BASE_TRACKING = "http://localhost:5001"

payload_login = {"email": "iago@logistica.local", "senha": "123456"}
payload_tel = {
    "placa": "ABC1D23",
    "latitude": -23.6815,
    "longitude": -46.6205,
    "velocidade": 78.5,
    "temperatura_carga": 5.2,
    "combustivel": 60.0,
}

def login():
    r = requests.post(f"{BASE_AUTH}/login", json=payload_login, timeout=5)
    r.raise_for_status()
    return r.json()["token"]

def enviar(token):
    inicio = time.perf_counter()
    r = requests.post(f"{BASE_TRACKING}/telemetrias", json=payload_tel, headers={"Authorization": f"Bearer {token}"}, timeout=5)
    fim = time.perf_counter()
    return (fim - inicio) * 1000, r.status_code

def rodada(workers=4, requests_total=40):
    token = login()
    inicio = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        resultados = list(executor.map(lambda _: enviar(token), range(requests_total)))
    duracao = time.perf_counter() - inicio
    latencias = [r[0] for r in resultados]
    ok = sum(1 for _, status in resultados if status in (200, 201))
    print(f"Workers: {workers}")
    print(f"Requisições OK: {ok}/{requests_total}")
    print(f"Latência média: {statistics.mean(latencias):.2f} ms")
    print(f"Latência p95: {statistics.quantiles(latencias, n=20)[18]:.2f} ms")
    print(f"Throughput: {requests_total/duracao:.2f} req/s")

if __name__ == "__main__":
    for workers in [1, 2, 4, 8]:
        rodada(workers=workers, requests_total=40)
