from tracking_service.app import TelemetryFactory

def test_factory_normaliza_campos():
    payload = {"placa": "ABC1234", "latitude": "-23.5", "longitude": "-46.6", "velocidade": "70", "temperatura": "5", "combustivel": "30"}
    data = TelemetryFactory.create(payload)
    assert data["placa"] == "ABC1234"
    assert data["velocidade"] == 70.0
    assert data["temperatura_carga"] == 5.0
