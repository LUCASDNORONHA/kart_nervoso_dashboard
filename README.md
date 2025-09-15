# 🏎️ Kart Nervoso Dashboard

Um painel interativo e completo para o grupo **Kart Nervoso**. Visualize rankings, estatísticas e acompanhe o desempenho dos pilotos em detalhes.

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
## 🚀 Como Rodar

Siga os passos abaixo para iniciar o projeto localmente.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/LUCASDNORONHA/kart_nervoso_dashboard.git](https://github.com/LUCASDNORONHA/kart_nervoso_dashboard.git)
    cd kart_nervoso_dashboard
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o banco de dados:**
    ```bash
    python setup_db.py
    ```

5.  **Inicie o painel:**
    ```bash
    streamlit run dashboard.py
    ```

6.  **Acesse o dashboard** no seu navegador: `http://localhost:8501`.

---
## 📂 Estrutura do Projeto

kart_nervoso_dashboard/

├─ dashboard.py       # Ponto de entrada do painel interativo

├─ insert_data.py     # Script para adicionar dados ao banco

├─ ranking.py         # Módulo para cálculo e exibição do ranking

├─ setup_db.py        # Script de configuração inicial do banco de dados

├─ requirements.txt   # Lista de dependências do projeto

└─ README.md          # Documentação do projeto


---
## 🙌 Contribuições

Contribuições são sempre bem-vindas! Se você tiver alguma ideia ou encontrar um bug, siga os passos abaixo:

1.  **Faça um fork** do projeto.
2.  Crie uma nova branch para a sua feature: `git checkout -b sua-feature`.
3.  **Faça suas alterações** e commit: `git commit -m 'Adicionando uma nova feature'`.
4.  **Envie** para a sua branch: `git push origin sua-feature`.
5.  Abra um **Pull Request** detalhado.

---
## 📸 O que vem por aí?

* Adicionar **gráficos e visualizações** mais detalhadas.
* Implementar um sistema de **autenticação** para administradores.
* Melhorar o design com **cores e logos** personalizados do "Kart Nervoso".

---
## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
