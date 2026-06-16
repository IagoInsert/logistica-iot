DROP DATABASE IF EXISTS logistica_iot;
CREATE DATABASE logistica_iot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE logistica_iot;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('admin','operador') NOT NULL DEFAULT 'operador',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    motorista VARCHAR(120) NOT NULL,
    status ENUM('ATIVO','MANUTENCAO','INATIVO') NOT NULL DEFAULT 'ATIVO',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telemetrias (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    veiculo_id INT NOT NULL,
    latitude DECIMAL(10,6) NOT NULL,
    longitude DECIMAL(10,6) NOT NULL,
    velocidade DECIMAL(6,2) NOT NULL,
    temperatura_carga DECIMAL(5,2) NOT NULL,
    combustivel DECIMAL(5,2) NOT NULL,
    timestamp_evento DATETIME NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_telemetria_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id),
    INDEX idx_telemetrias_veiculo_data (veiculo_id, criado_em),
    INDEX idx_telemetrias_criado_em (criado_em)
);

CREATE TABLE alertas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    telemetria_id BIGINT NOT NULL,
    tipo ENUM('VELOCIDADE','TEMPERATURA','COMBUSTIVEL') NOT NULL,
    mensagem VARCHAR(255) NOT NULL,
    severidade ENUM('BAIXA','MEDIA','ALTA') NOT NULL,
    resolvido BOOLEAN NOT NULL DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerta_telemetria FOREIGN KEY (telemetria_id) REFERENCES telemetrias(id),
    INDEX idx_alertas_resolvido (resolvido, criado_em)
);
