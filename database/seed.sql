USE logistica_iot;
-- senha do usuário: 123456
INSERT INTO usuarios(nome, email, senha_hash, perfil) VALUES
('Iago Neves Alves', 'iago@logistica.local', '$2b$12$ZQzLyZYgg6w7ZVGQqjkq..UVhN1hfTrSVq6jDINkFA49f8/XSkgqG', 'admin');

INSERT INTO veiculos(placa, motorista, status) VALUES
('ABC1D23', 'Carlos Souza', 'ATIVO'),
('BRA2E26', 'Mariana Lima', 'ATIVO'),
('LOG3I21', 'Rafael Santos', 'ATIVO');
