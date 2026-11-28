CREATE DATABASE IF NOT EXISTS monitoramento_processos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE monitoramento_processos;

CREATE TABLE
    IF NOT EXISTS processos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        tipo VARCHAR(255) NOT NULL,
        setor VARCHAR(255) NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

INSERT INTO
    processos (nome, tipo, setor)
VALUES
    ('Gestão de stakeholders', 'Desempenho', 'Gestão de Projetos');