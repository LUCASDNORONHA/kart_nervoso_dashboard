import sqlite3

# -------------------------------
# Funções auxiliares
# -------------------------------

def tempo_para_segundos(tempo_str):
    """Converte MM:SS.mmm em segundos (float)."""
    minutos, segundos = tempo_str.split(":")
    return int(minutos) * 60 + float(segundos)

def get_or_create_piloto(cursor, nome):
    """Verifica se o piloto existe, se não existir cria."""
    cursor.execute("SELECT piloto_id FROM pilotos WHERE nome = ?", (nome,))
    res = cursor.fetchone()
    if res:
        return res[0]
    cursor.execute("INSERT INTO pilotos (nome) VALUES (?)", (nome,))
    return cursor.lastrowid

# -------------------------------
# Função principal para inserir corrida
# -------------------------------

def inserir_corrida(pista, data_corrida, duracao, clima, resultados):
    """
    Insere uma corrida e os resultados no banco.

    resultados: lista de tuplas (posicao, nome_piloto, melhor_volta)
    """
    conn = sqlite3.connect("data/kart.db")
    cursor = conn.cursor()

    # Verifica se corrida já existe
    cursor.execute("SELECT corrida_id FROM corridas WHERE pista = ? AND data_corrida = ?", (pista, data_corrida))
    res = cursor.fetchone()
    if res:
        print(f"⚠️ Corrida '{pista}' em {data_corrida} já existe no banco!")
        corrida_id = res[0]
    else:
        cursor.execute(
            "INSERT INTO corridas (pista, data_corrida, duracao, clima) VALUES (?, ?, ?, ?)",
            (pista, data_corrida, duracao, clima)
        )
        corrida_id = cursor.lastrowid
        print(f"✅ Corrida '{pista}' em {data_corrida} inserida com sucesso!")

    # Inserir pilotos e resultados
    for r in resultados:
        posicao, nome, melhor_volta_str = r
        melhor_volta = tempo_para_segundos(melhor_volta_str)
        pontos = max(0, 25 - (posicao - 1) * 2)  # Exemplo de pontuação: 25, 23, 21...

        piloto_id = get_or_create_piloto(cursor, nome)

        # Evita duplicar resultados
        cursor.execute("""
            SELECT resultado_id FROM resultados
            WHERE corrida_id = ? AND piloto_id = ?
        """, (corrida_id, piloto_id))

        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO resultados (corrida_id, piloto_id, posicao, pontos, melhor_volta)
                VALUES (?, ?, ?, ?, ?)
            """, (corrida_id, piloto_id, posicao, pontos, melhor_volta))

    conn.commit()
    conn.close()
    print("-----------------------------------------------")
    print("Resultados inseridos com sucesso! ✅")
    print("-----------------------------------------------")

# -------------------------------
# Exemplo de uso
# -------------------------------

if __name__ == "__main__":
    # Exemplo: primeira corrida
    resultados = [
        (1, "David Maion", "00:52.321"),
        (2, "Marcos Silva", "00:53.732"),
        (3, "Daniel Francisco", "00:53.374"),
        (4, "Aldenir Nunes", "00:55.225"),
        (5, "Nicolas Alves", "00:56.595"),
        (6, "Lucas Dias Noronha", "00:57.063"),
        (7, "Rick Lira", "00:56.012")
    ]

    inserir_corrida(
        pista="Kart Point",
        data_corrida="2025-09-07",
        duracao="00:45:00",
        clima="Ensolarado",
        resultados=resultados
    )
