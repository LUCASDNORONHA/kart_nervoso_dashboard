# 🏎️ Kart Nervoso Dashboard

Um painel interativo e completo para o grupo **Kart Nervoso**. Visualize rankings, estatísticas e acompanhe o desempenho dos pilotos em detalhes.

Link: link: https://kartnervosodashboard-auw9gtvhrpb9jqzbdve4rc.streamlit.app/


---
## ⚡ Funcionalidades

* 📊 **Dashboard Interativo:** Visualize rankings gerais e por corrida com gráficos e tabelas dinâmicas.
* 📈 **Análise Detalhada:** Acesse estatísticas de cada corrida, como tempo, volta mais rápida e posições.
* ➕ **Gerenciamento de Dados:** Adicione novos pilotos e corridas facilmente através da interface.
* 💻 **Acessibilidade:** Uma interface simples e intuitiva, acessível diretamente no seu navegador.

---
## 🛠️ Tecnologias

Este projeto foi construído utilizando as seguintes tecnologias:

* **Python 3.10+:** Linguagem principal para a lógica do backend.
* **Streamlit:** Framework para criar a interface do dashboard de forma rápida e eficiente.
* **SQLite:** Banco de dados leve e integrado, perfeito para o gerenciamento local dos dados.
* **Pandas:** Essencial para a manipulação e análise de dados, otimizando o cálculo dos rankings.

---

## 📂 Estrutura do Projeto

kart_nervoso_dashboard/

├─ dashboard.py       # Ponto de entrada do painel interativo

├─ insert_data.py     # Script para adicionar dados ao banco

├─ ranking.py         # Módulo para cálculo e exibição do ranking

├─ setup_db.py        # Script de configuração inicial do banco de dados

├─ requirements.txt   # Lista de dependências do projeto

└─ README.md          # Documentação do projeto
