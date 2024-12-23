import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('banco_de_dados.db')
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS controle_mensal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cc TEXT NOT NULL,
    proximos_meses TEXT NOT NULL,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    valor REAL NOT NULL
)
""")


st.markdown(
    """
    <style>
    .stMarkdownContainer {
        display: flex;
        justify-content: right;
        margin: 20px 0; /* Margem acima e abaixo do botão */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #161a1d;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .st-emotion-cache-6qob1r.eczjsme11 {
        background-color: #e61e24;
        opacity: 1;
        background-image: linear-gradient(135deg, #ff0404 25%, transparent 25%), 
                          linear-gradient(225deg, #ff0404 25%, transparent 25%), 
                          linear-gradient(45deg, #ff0404 25%, transparent 25%), 
                          linear-gradient(315deg, #ff0404 25%, #e61e24 25%);
        background-position: 16px 0, 16px 0, 0 0, 0 0;
        background-size: 32px 32px;
        background-repeat: repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menu no sidebar
st.sidebar.markdown("<h1 style='text-align: center; font-size: 30px;'>Menu</h1>", unsafe_allow_html=True)
menu = st.sidebar.selectbox(
    "Escolha uma Opção",
    ["Home", "Controle Mensal",
     "Relatório Dinâmico"])  # ------------------------------------------------------------------------

# Página principal
if menu == "Home":
    #st.image('TrainingMS-Branca-vermelha.png')
    pass

elif menu == "Controle Mensal":
    Centro_de_Custo = st.sidebar.selectbox("Informe o Centro de Custo",
                                           ["OFFSHORE", "SÓCIO", "EAD E APOIO", "FINANCEIRO", "DESENVOLVIMENTO",
                                            "ONSHORE", "COMERCIAL"])
    data = st.sidebar.selectbox("É para o próximo mês?", ["Não", "Sim"])
    nome_colaborador = st.sidebar.text_input("Digite o nome do Colaborador")
    categoria = st.sidebar.selectbox("É para o próximo mês?", ["Saúde", "Dental"])
    valor = st.sidebar.text_input("Insira o valor")


    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        button1 = st.button("Enviar")

    with col2:
        button2 = st.button("Limpar")

    with col3:
        button3 = st.button("Verificar Banco de Dados")

    # Ações dos botões
    if button1:
        try:
            valor = float(valor)  # Converte para tipo float
            cursor.execute("""
                INSERT INTO controle_mensal (cc, proximos_meses, nome, categoria, valor)
                VALUES (?, ?, ?, ?, ?)
            """, (Centro_de_Custo, data, nome_colaborador, categoria, valor))
            conn.commit()  # Confirma a inserção
            st.success("Dados inseridos com sucesso!")
        except ValueError:
            st.error("Por favor, insira um valor válido para o campo 'Valor'.")

    if button3:
        p = cursor.execute("SELECT * FROM controle_mensal")
        rows = p.fetchall()  # Obtém os dados
        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Centro de Custo", "Próximos Meses", "Nome", "Categoria", "Valor"])
            st.dataframe(df)
        else:
            st.warning("Não há dados disponíveis no banco de dados.")
    st.sidebar.write("\n\n")
    selectbox2 = st.sidebar.selectbox("Validação", ["Excluir Linha"])
    if selectbox2 == "Excluir Linha":
        selectbox_delete_line = st.sidebar.text_input("Número da linha para ser excluída")
        button_excluir_linha =st.sidebar.button("Excluir Linha")
        st.sidebar.write(f"Linha {selectbox_delete_line} deletada com sucesso!")
        if button_excluir_linha:
            cursor.execute(f"DELETE FROM controle_mensal WHERE id = {selectbox_delete_line}")
            conn.commit()


elif menu == "Relatório Dinâmico":
    # Consultar os dados do banco
    query = "SELECT * FROM controle_mensal"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(rows, columns=["ID", "Centro de Custo", "Próximos Meses", "Nome", "Categoria", "Valor"])

        # Exibir o DataFrame
        st.write("Dados do Banco de Dados:")
        st.dataframe(df)


        st.subheader("Distribuição de Valores por Categoria")
        fig = px.bar(df, x="Categoria", y="Valor", color="Categoria", title="Total de Valores por Categoria",
                     labels={'Valor': 'Total de Valores'})
        st.plotly_chart(fig)


        st.subheader("Relação entre 'Valor' e 'Centro de Custo'")
        fig2 = px.scatter(df, x="Centro de Custo", y="Valor", color="Categoria", title="Valor por Centro de Custo",
                          labels={'Valor': 'Total de Valores'})
        st.plotly_chart(fig2)
    else:
        st.warning("Não há dados disponíveis para mostrar.")