import sqlite3

# -------------------------------
# Ranking de uma corrida específica
# -------------------------------
def ranking_corrida(corrida_id):
    conn = sqlite3.connect("data/kart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nome, r.posicao, r.pontos, r.melhor_volta
        FROM resultados r
        JOIN pilotos p ON r.piloto_id = p.piloto_id
        WHERE r.corrida_id = ?
        ORDER BY r.posicao ASC
    """, (corrida_id,))
    
    resultados = cursor.fetchall()
    
    print(f"\n🏁 Ranking da Corrida {corrida_id} 🏁")
    print("-" * 50)
    print(f"{'Pos':<5}{'Piloto':<25}{'Pts':<5}{'Melhor Volta (s)'}")
    print("-" * 50)
    
    for r in resultados:
        print(f"{r[1]:<5}{r[0]:<25}{r[2]:<5}{r[3]:.3f}")
    
    print("-" * 50)
    conn.close()

# -------------------------------
# Ranking geral acumulado
# -------------------------------
def ranking_geral():
    conn = sqlite3.connect("data/kart.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.nome, SUM(r.pontos) as total_pontos, MIN(r.melhor_volta) as melhor_volta
        FROM resultados r
        JOIN pilotos p ON r.piloto_id = p.piloto_id
        GROUP BY r.piloto_id
        ORDER BY total_pontos DESC, melhor_volta ASC
    """)
    
    resultados = cursor.fetchall()
    
    print(f"\n🏆 Ranking Geral do Campeonato 🏆")
    print("-" * 50)
    print(f"{'Pos':<5}{'Piloto':<25}{'Pts':<5}{'Melhor Volta (s)'}")
    print("-" * 50)
    
    for i, r in enumerate(resultados, start=1):
        print(f"{i:<5}{r[0]:<25}{r[1]:<5}{r[2]:.3f}")
    
    print("-" * 50)
    conn.close()

# -------------------------------
# Menu simples
# -------------------------------
def menu():
    while True:
        print("\n--- MENU DE RANKING ---")
        print("1. Ranking de corrida específica")
        print("2. Ranking geral acumulado")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            corrida_id = int(input("Informe o ID da corrida: "))
            ranking_corrida(corrida_id)
        elif escolha == "2":
            ranking_geral()
        elif escolha == "3":
            print("Saindo... 🏁")
            break
        else:
            print("Opção inválida! Tente novamente.")

# -------------------------------
# Executar menu
# -------------------------------
if __name__ == "__main__":
    menu()
