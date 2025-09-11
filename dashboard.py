import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Conexão com o banco SQLite
# -----------------------------
conn = sqlite3.connect("data/kart.db")

# -----------------------------
# Configuração do Streamlit
# -----------------------------
st.set_page_config(page_title="Placar de Líderes Kart Nervoso", layout="wide")

# Logo + Título
col1, col2 = st.columns([1,5])
col1.image("assets/logo_kart_nervoso.png", width=120)
col2.markdown("<h1 style='color:white;'>🏁 Kart Nervoso</h1>", unsafe_allow_html=True)

# Custom CSS para tabela e fundo escuro
st.markdown("""
    <style>
    .main {background-color: #1e1e2f; color: white;}
    .stDataFrame tbody tr th {color: white;}
    .stDataFrame tbody tr td {color: white;}
    .leaderboard th {background-color: #333; color: white; text-align:center;}
    .leaderboard td {text-align:center;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Ranking Histórico Geral
# -----------------------------
st.header("🏆 Ranking Histórico")

ranking_query = """
SELECT p.nome AS Piloto,
       p.falta AS Falta,
       SUM(r.pontos) AS Pontos, 
       MIN(r.posicao) AS Melhor_Posicao, 
       MIN(r.melhor_volta) AS Melhor_Volta
FROM resultados r
JOIN pilotos p ON r.piloto_id = p.piloto_id
GROUP BY p.piloto_id
ORDER BY Pontos DESC, Melhor_Volta ASC
"""
ranking_df = pd.read_sql_query(ranking_query, conn)

# Formatar melhor volta
ranking_df['Melhor_Volta'] = ranking_df['Melhor_Volta'].apply(lambda x: f"{int(x//60):02d}:{x%60:06.3f}")
ranking_df['Piloto'] = ranking_df['Piloto'].apply(lambda x: f"🏎️ {x}")

# Função para destacar líder
def highlight_leader(row):
    return ['background-color: gold; color:black;' if row.name == 0 else '' for _ in row]

# Mostrar tabela
st.dataframe(
    ranking_df.style.apply(highlight_leader, axis=1).set_properties(**{'text-align': 'center'}),
    use_container_width=True
)

# -----------------------------
# Filtro por piloto ou equipe
# -----------------------------
st.header("🔎 Filtrar Ranking")
pilotos = ranking_df['Piloto'].tolist()
equipes = ranking_df['Equipe'].unique().tolist()

selected_piloto = st.selectbox("Escolha um piloto (opcional):", ["Todos"] + pilotos)
selected_equipe = st.selectbox("Escolha uma equipe (opcional):", ["Todas"] + equipes)

filtered_df = ranking_df.copy()
if selected_piloto != "Todos":
    filtered_df = filtered_df[filtered_df['Piloto'] == selected_piloto]
if selected_equipe != "Todas":
    filtered_df = filtered_df[filtered_df['Equipe'] == selected_equipe]

st.dataframe(
    filtered_df.style.apply(highlight_leader, axis=1).set_properties(**{'text-align': 'center'}),
    use_container_width=True
)

# -----------------------------
# Próximas Corridas
# -----------------------------
st.header("📅 Próximas Corridas")
corridas_query = """
SELECT pista AS Pista, data AS Data, status AS Status
FROM corridas
WHERE status='planejada'
ORDER BY data
"""
corridas_df = pd.read_sql_query(corridas_query, conn)
st.table(corridas_df)

# -----------------------------
# Melhores Voltas
# -----------------------------
st.header("⏱️ Melhor Volta por Piloto")
melhor_volta_query = """
SELECT p.nome AS Piloto, p.equipe AS Equipe, MIN(r.melhor_volta) AS Melhor_Volta
FROM resultados r
JOIN pilotos p ON r.piloto_id = p.piloto_id
GROUP BY p.piloto_id
ORDER BY Melhor_Volta ASC
"""
melhor_volta_df = pd.read_sql_query(melhor_volta_query, conn)
melhor_volta_df['Melhor_Volta'] = melhor_volta_df['Melhor_Volta'].apply(lambda x: f"{int(x//60):02d}:{x%60:06.3f}")
melhor_volta_df['Piloto'] = melhor_volta_df['Piloto'].apply(lambda x: f"🏎️ {x}")
st.table(melhor_volta_df)

# -----------------------------
# Fechar conexão
# -----------------------------
conn.close()
