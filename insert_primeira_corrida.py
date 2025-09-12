import sqlite3

# Função para converter MM:SS.mmm em segundos (float)
def tempo_para_segundos(tempo_str):
    minutos, segundos = tempo_str.split(":")
    return int(minutos) * 60 + float(segundos)

# Conexão com o banco
conn = sqlite3.connect("data/kart.db")
cursor = conn.cursor()

# --- Corrida ---
local = "Kart Point"
data_corrida = "2025-09-07"
status = "concluída"

# Verifica se a corrida já existe
cursor.execute("SELECT corrida_id FROM corridas WHERE pista = ? AND data = ?", (local, data_corrida))
res = cursor.fetchone()
if res:
    corrida_id = res[0]
else:
    cursor.execute("INSERT INTO corridas (local, data, status) VALUES (?, ?, ?)", 
                   (local, data_corrida, status))
    corrida_id = cursor.lastrowid

# --- Pilotos e resultados ---
resultados = [
    ("David Maion", 1, 25, "00:52.321"),
    ("Marcos Silva", 2, 18, "00:53.732"),
    ("Daniel Francisco", 15, 16, "00:53.374"),
    ("Aldenir Nunes", 4, 12, "00:55.225"),
    ("Nicolas Alves", 5, 10, "00:56.595"),
    ("Lucas Dias Noronha", 8, 15, "00:57.063"),
    ("Rick Lira", 7, 6, "00:56.012")
]

# Função para inserir piloto se não existir
def get_or_create_piloto(nome):
    cursor.execute("SELECT piloto_id FROM pilotos WHERE nome = ?", (nome,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute("INSERT INTO pilotos (nome) VALUES (?)", (nome,))
    return cursor.lastrowid

# Inserir resultados
for r in resultados:
    piloto_id = get_or_create_piloto(r[0])
    posicao = r[1]
    pontos = max(0, 25 - (posicao - 1) * 2)  # Pontuação exemplo: 25, 23, 21...
    melhor_volta = tempo_para_segundos(r[3])
    
    # Verifica se resultado já existe (mesmo piloto e corrida)
    cursor.execute("""
        SELECT resultado_id FROM resultados 
        WHERE corrida_id = ? AND piloto_id = ?
    """, (corrida_id, piloto_id))
    
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO resultados (corrida_id, piloto_id, posicao, pontos, melhor_volta)
            VALUES (?, ?, ?, ?, ?)
        """, (corrida_id, piloto_id, posicao, pontos, melhor_volta))

# Commit e fechar
conn.commit()
conn.close()

print("Primeira corrida inserida com sucesso! ✅")