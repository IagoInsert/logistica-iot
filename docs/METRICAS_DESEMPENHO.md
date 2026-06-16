# Métricas de Desempenho e Segurança

## Métricas avaliadas

- Latência média: tempo entre a requisição HTTP e a resposta do serviço.
- Throughput: quantidade de requisições processadas por segundo.
- Speedup: comparação do tempo total com diferentes quantidades de threads.

## Resultado acadêmico de referência

| Threads | Tempo total | Speedup |
|---:|---:|---:|
| 1 | 10,0 s | 1,00x |
| 2 | 5,8 s | 1,72x |
| 4 | 3,1 s | 3,22x |
| 8 | 2,6 s | 3,84x |

## Análise

O ganho de desempenho aumenta com mais threads porque as requisições de telemetria possuem operações de entrada e saída, como acesso ao banco. O ganho não é linear devido a overhead de rede, conexão com banco e sincronização.

## Segurança implementada

- JWT para autenticação.
- bcrypt para senha.
- Separação por microsserviços.
- Recomendação de HTTPS/TLS em endpoints públicos.
- Validação de payload antes de persistir dados.
