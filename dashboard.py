import sqlite3
import streamlit as st
import pandas as pd

# -----------------------------
# Conexão com o banco
# -----------------------------
conn = sqlite3.connect("data/kart.db")

# -----------------------------
# Configuração Streamlit
# -----------------------------
st.set_page_config(page_title="Kart Nervoso - Dashboard", layout="wide")

# -----------------------------
# Logo grande centralizado + título
# -----------------------------
st.markdown("""
<div style="text-align:center; margin-bottom:20px;">
    <h1 style="color:#d62828; margin-top:10px;">Kart Nervoso</h1>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Card de descrição do grupo
# -----------------------------
st.markdown(f"""
<div class='card' style='background-color:#ffe5e5; max-width:800px; margin-left:auto; margin-right:auto;'>
    <h4 style='text-align:center;'>Sobre o Kart Nervoso</h4>
    <p style='text-align:center; font-size:16px; line-height:1.5; color:#111;'>
        O Kart Nervoso é um grupo apaixonado por velocidade, adrenalina e competição saudável.<br>
        Nosso objetivo é reunir pilotos talentosos e proporcionar corridas emocionantes, 
        com espírito esportivo e muita diversão.<br>
        Aqui você encontra rankings, melhores voltas, histórico de corridas e eventos especiais do grupo.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# CSS customizado - tema esportivo claro
# -----------------------------
st.markdown("""
<style>
body {background-color: #f5f5f5; color: #111; font-family: 'Roboto', sans-serif;}
h1, h2, h3 {font-family: 'Orbitron', sans-serif; color: #d62828; text-shadow: 1px 1px 2px #aaa;}

/* Tabelas */
table {border-collapse: collapse; width: 100%; margin-bottom: 20px;}
th, td {padding: 10px; text-align: center; border: 1px solid #ccc; color:#111;}
thead th {background-color: #d62828; color: white; font-weight: bold;}
tbody tr:nth-child(odd) {background-color: #fff;}
tbody tr:nth-child(even) {background-color: #f2f2f2;}
tbody tr:hover {background-color: #ffe5e5; transition: 0.3s;}

/* Pódio */
.pos-1 {background-color: gold; font-weight:bold;}
.pos-2 {background-color: silver; font-weight:bold;}
.pos-3 {background-color: #cd7f32; font-weight:bold;}

/* Barras de pontos */
.bar-container {background-color: #eee; width: 100%; height: 12px; border-radius: 5px;}
.bar-fill {background-color: #d62828; height: 12px; border-radius: 5px;}

/* Cards de corrida */
.card {background-color: #fff0f0; padding: 15px; margin: 10px auto; border-radius: 10px; box-shadow: 2px 2px 8px #ccc; width: 250px;}
.card h4 {margin: 0; font-weight: bold; color:#d62828; text-align:center;}
.card p {margin: 2px 0; color:#555; text-align:center; font-size:14px;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Função para exibir tabela HTML com barras de pontos
# -----------------------------
def mostrar_tabela_html(df, mostrar_barras=True):
    html = "<table><thead><tr>"
    cols = df.columns.tolist()
    if 'Posição' in cols:
        cols.remove('Posição')
        cols = ['Posição', 'Piloto'] + [c for c in cols if c not in ['Posição','Piloto']]
    for col in cols:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    
    max_pontos = df['Pontos'].max() if mostrar_barras and 'Pontos' in df.columns else 0
    
    for _, row in df.iterrows():
        classe = f"pos-{row['Posição']}" if row['Posição'] <= 3 else ""
        html += f"<tr class='{classe}'>"
        for col in cols:
            valor = row[col]
            if col == "Pontos" and mostrar_barras:
                fill_percent = int((valor / max_pontos) * 100)
                valor = f"""
                {valor} 
                <div class='bar-container'>
                    <div class='bar-fill' style='width:{fill_percent}%;'></div>
                </div>
                """
            if col == "Melhor_Volta":
                valor = f"<strong style='color:#d62828;'>{valor}</strong>"
            html += f"<td>{valor}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

# -----------------------------
# 1️⃣ Ranking Histórico Geral
# -----------------------------
st.header("Ranking Histórico Geral")
ranking_query = """
SELECT p.nome AS Piloto,
       SUM(r.pontos) AS Pontos,
       MIN(r.melhor_volta) AS Melhor_Volta,
       RANK() OVER(ORDER BY SUM(r.pontos) DESC, MIN(r.melhor_volta)) AS Posição
FROM resultados r
JOIN pilotos p ON r.piloto_id = p.piloto_id
GROUP BY p.piloto_id
"""
ranking_df = pd.read_sql_query(ranking_query, conn)
ranking_df['Melhor_Volta'] = ranking_df['Melhor_Volta'].apply(lambda x: f"{int(x//60):02d}:{x%60:06.3f}")
mostrar_tabela_html(ranking_df)

# -----------------------------
# 2️⃣ Ranking por Corrida
# -----------------------------
st.header("Ranking por Corrida")
corridas_df = pd.read_sql_query("SELECT corrida_id, pista, data_corrida FROM corridas ORDER BY data_corrida", conn)
corrida_labels = [f"{row['data_corrida']} - {row['pista']}" for _, row in corridas_df.iterrows()]

selected_label = st.selectbox("Escolha uma corrida:", corrida_labels)
corrida_id = corridas_df[corridas_df.apply(lambda row: f"{row['data_corrida']} - {row['pista']}", axis=1) == selected_label]["corrida_id"].values[0]

query_corrida = """
SELECT r.posicao AS Posição, p.nome AS Piloto, r.pontos AS Pontos, r.melhor_volta AS Melhor_Volta
FROM resultados r
JOIN pilotos p ON r.piloto_id = p.piloto_id
WHERE r.corrida_id = ?
ORDER BY r.posicao ASC
"""
corrida_df = pd.read_sql_query(query_corrida, conn, params=(corrida_id,))
corrida_df['Melhor_Volta'] = corrida_df['Melhor_Volta'].apply(lambda x: f"{int(x//60):02d}:{x%60:06.3f}")
mostrar_tabela_html(corrida_df)

# -----------------------------
# 3️⃣ Melhor Volta por Piloto
# -----------------------------
st.header("Melhor Volta por Piloto")
melhor_volta_query = """
SELECT p.nome AS Piloto, MIN(r.melhor_volta) AS Melhor_Volta,
       RANK() OVER(ORDER BY MIN(r.melhor_volta)) AS Posição
FROM resultados r
JOIN pilotos p ON r.piloto_id = p.piloto_id
GROUP BY p.piloto_id
"""
melhor_volta_df = pd.read_sql_query(melhor_volta_query, conn)
melhor_volta_df['Melhor_Volta'] = melhor_volta_df['Melhor_Volta'].apply(lambda x: f"{int(x//60):02d}:{x%60:06.3f}")
mostrar_tabela_html(melhor_volta_df, mostrar_barras=False)

# -----------------------------
# Cards das Corridas
# -----------------------------
st.header("Eventos")
for _, row in corridas_df.iterrows():
    st.markdown(f"""
    <div class='card'>
        <h4>{row['pista']}</h4>
        <p>Data: {row['data_corrida']}</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Fechar conexão
# -----------------------------
conn.close()
