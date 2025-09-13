import sqlite3

# Conexão com o banco de dados (cria o arquivo se não existir)
conn = sqlite3.connect("data/kart.db")
cursor = conn.cursor()

# -------------------------------
# Criar tabela de pilotos
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS pilotos (
    piloto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);
""")

# -------------------------------
# Criar tabela de corridas
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS corridas (
    corrida_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pista TEXT NOT NULL,
    data_corrida DATE NOT NULL,
    duracao TEXT NOT NULL,
    clima TEXT NOT NULL
);
""")

# -------------------------------
# Criar tabela de resultados
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    resultado_id INTEGER PRIMARY KEY AUTOINCREMENT,
    corrida_id INTEGER NOT NULL,
    piloto_id INTEGER NOT NULL,
    posicao INTEGER NOT NULL,
    pontos INTEGER NOT NULL,
    melhor_volta REAL NOT NULL,
    FOREIGN KEY(corrida_id) REFERENCES corridas(corrida_id),
    FOREIGN KEY(piloto_id) REFERENCES pilotos(piloto_id)
);
""")

# Salvar alterações e fechar conexão
conn.commit()
conn.close()

print("-----------------------------------------------")
print("Banco de dados e tabelas criados com sucesso! ✅")
print("-----------------------------------------------")