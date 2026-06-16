# Logística IoT - Rastreamento Inteligente de Frotas

**Aluno:** Iago Neves Alves  
**RA:** 12524147860  
**Disciplina:** Sistemas Distribuídos e Mobile - A3 2026/1  

## 1. Visão Geral

Este projeto implementa uma solução distribuída para monitoramento de frota logística em tempo real. Caminhões enviam dados simulados de GPS, velocidade, temperatura da carga e combustível via MQTT. Os dados são processados por microsserviços em Python, armazenados em MySQL e consultados por APIs REST protegidas com JWT.

## 2. Arquitetura

Fluxo principal:

```text
Simulador GPS IoT -> MQTT Broker -> Tracking Service -> MySQL
                                      |
                                      +-> Alert Observer -> Tabela de Alertas
Usuário -> Auth Service -> Token JWT -> APIs protegidas
```

## 3. Tecnologias

- Python 3.12
- Flask
- MySQL
- MQTT com Mosquitto/HiveMQ
- JWT
- bcrypt
- Docker Compose

## 4. Microsserviços

| Serviço | Porta | Responsabilidade |
|---|---:|---|
| Auth Service | 5000 | Login, criação de usuários e geração de JWT |
| Tracking Service | 5001 | Receber telemetrias por HTTP/MQTT e salvar no MySQL |
| Alert Service | 5002 | Consultar e resolver alertas operacionais |
| Simulador GPS | - | Publicar dados IoT no tópico MQTT `frota/telemetria` |

## 5. Como executar

### 5.1 Subir MySQL e MQTT

```bash
docker compose up -d
```

### 5.2 Criar ambiente Python

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 5.3 Rodar serviços

Abra 4 terminais diferentes:

```bash
python auth_service/app.py
python tracking_service/app.py
python alert_service/app.py
python simulator/gps_simulator.py
```

### 5.4 Testar login

```bash
curl -X POST http://localhost:5000/login ^
  -H "Content-Type: application/json" ^
  -d "{"email":"iago@logistica.local","senha":"123456"}"
```

## 6. Segurança

- Autenticação por JWT.
- Senhas armazenadas com hash bcrypt.
- Separação de responsabilidades por microsserviço.
- Recomendação de HTTPS/TLS no deploy em nuvem.

## 7. Padrões de Projeto

- **Factory Method:** normaliza sensores diferentes no `TelemetryFactory`.
- **Observer:** `AlertObserver` reage automaticamente a novas telemetrias.

## 8. Métricas de Desempenho

O script `scripts/performance_test.py` mede latência, throughput e comparação entre execuções com diferentes quantidades de threads.

Resultados esperados em ambiente local de teste:

| Threads | Tempo médio total | Speedup estimado |
|---:|---:|---:|
| 1 | 10,0 s | 1,00x |
| 2 | 5,8 s | 1,72x |
| 4 | 3,1 s | 3,22x |
| 8 | 2,6 s | 3,84x |

## 9. Entregáveis

- Código-fonte dos microsserviços.
- Scripts SQL do banco.
- Documentação técnica em `docs/`.
- Diagramas C4 e UML em `diagrams/`.
- Slides de apresentação em `slides/`.
