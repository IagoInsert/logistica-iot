# Como atualizar o GitHub com esta versão completa

1. Baixe e extraia o arquivo ZIP.
2. Copie todo o conteúdo extraído para a pasta do projeto que você abriu no VS Code.
3. Quando o Windows perguntar, escolha substituir os arquivos existentes.
4. No terminal do VS Code, rode:

```bash
git add .
git commit -m "Versao completa do projeto Logistica IoT"
git push
```

# O que entregar no AVA

- Link do repositório GitHub: https://github.com/IagoInsert/logistica-iot
- docs/Relatorio_Tecnico_Logistica_IoT.pdf
- slides/Apresentacao_Logistica_IoT.pptx
- docs/ROTEIRO_VIDEO.md, caso o professor peça roteiro do vídeo.

# Arquivos principais

- README.md: explicação do projeto e execução.
- database/schema.sql: criação do banco MySQL.
- database/seed.sql: dados iniciais.
- auth_service/app.py: autenticação JWT.
- tracking_service/app.py: ingestão MQTT/HTTP e persistência.
- alert_service/app.py: consulta e resolução de alertas.
- simulator/gps_simulator.py: simula caminhões e sensores IoT.
- diagrams/: diagramas C4 e UML.
- docs/: relatório, métricas e roteiro.
- slides/: apresentação final.
