# Roteiro do vídeo de demonstração - máximo 8 minutos

## 0:00 - 0:40 | Apresentação
Olá, meu nome é Iago Neves Alves, RA 12524147860. Este é o projeto Logística IoT, um sistema distribuído para rastreamento inteligente de frotas.

## 0:40 - 1:40 | Problema
O problema escolhido é o monitoramento em tempo real de caminhões. A empresa precisa acompanhar localização, velocidade, temperatura da carga e combustível para reduzir atrasos, riscos e perdas.

## 1:40 - 2:50 | Arquitetura
Mostrar o diagrama C4. Explicar que o simulador representa sensores IoT, o MQTT funciona como broker de mensagens, os microsserviços processam os dados e o MySQL armazena as informações.

## 2:50 - 4:20 | Código e execução
Mostrar os serviços em Python: Auth Service, Tracking Service, Alert Service e o simulador GPS. Explicar que o Tracking Service recebe dados MQTT e também possui endpoint HTTP protegido.

## 4:20 - 5:20 | Banco de dados
Mostrar o script SQL com as tabelas: usuários, veículos, telemetrias e alertas.

## 5:20 - 6:20 | Segurança
Demonstrar o login retornando um token JWT. Explicar bcrypt, token e controle de acesso.

## 6:20 - 7:20 | Desempenho
Mostrar o script de teste de desempenho e explicar latência, throughput e speedup.

## 7:20 - 8:00 | Conclusão
Concluir dizendo que o projeto atende conceitos de IoT, microsserviços, banco de dados, segurança e sistemas distribuídos.
