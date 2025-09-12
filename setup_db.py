import sqlite3

# Conexão com o banco
conn = sqlite3.connect("data/kart.db")
cursor = conn.cursor()

# Criar tabelas
cursor.execute("""
CREATE TABLE IF NOT EXISTS pilotos (
    piloto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    falta TEXT NOT NULL,
    presença TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS corridas (
    corrida_id INTEGER PRIMARY KEY AUTOINCREMENT,
    local TEXT NOT NULL,
    data DATE NOT NULL,
    status TEXT CHECK(status IN ('planejada', 'concluída')) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    resultado_id INTEGER PRIMARY KEY AUTOINCREMENT,
    corrida_id INTEGER,
    piloto_id INTEGER,
    posicao INTEGER,
    pontos INTEGER,
    melhor_volta REAL,
    FOREIGN KEY(corrida_id) REFERENCES corridas(corrida_id),
    FOREIGN KEY(piloto_id) REFERENCES pilotos(piloto_id)
);
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
