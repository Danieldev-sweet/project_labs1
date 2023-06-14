import streamlit as st
import pandas as pd
import sqlite3
import Banco.banco_dados as Banco
import Page.cadastro as PageCadastro , Page.usuario as PageUsuario, Page.veterinario as PageVeterinario, Page.adm as PageAdm, Page.login as PageLogin
from sqlite3 import Error
st.set_page_config(page_title='BuscaVet', page_icon=':mag:')
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('./Banco/banco_programa.db')
        print(f"Conexão com o banco de dados estabelecida: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'login' not in st.session_state:
    st.session_state.login = False

def aprovar():
    st.session_state.login = True
    return st.session_state.login

def fechar():
    st.session_state.login = False

start_bar = st.sidebar.empty()
checkbox_placeholder = st.sidebar.empty()
titulo = st.empty()
texto = st.empty()
#Abaixo o contúdo da página incial

title = titulo.title('Tela principal')

Banco.create_veterinario()
especialidade = Banco.busca_especialidade_geral()
branco = []
especialidades = st.empty()
banco_lista = st.empty()
texto_inicio = st.empty()
mapa_st = st.empty()

especialidade_selecionada = especialidades.selectbox('Selecione a Especialidade: ' ,especialidade, key='232322')

if especialidade_selecionada:
    texto_inicio.text(f"Médicos disponíveis para a especialidade: {especialidade_selecionada}")
    medicos = Banco.busca_medicos_por_especialidade(especialidade_selecionada)
        
    lista_medicos = pd.DataFrame(medicos, columns=['Médico', 'Especialidade', 'Localidade', 'Telefone'])
    banco_lista.dataframe(lista_medicos)

    # Criar DataFrame com coordenadas de Aracaju
data = {'LAT': [-10.9472], 'LON': [-37.0731]}
df = pd.DataFrame(data)

# Exibir mapa no Streamlit
texto_inicio.title("Localização dos médicos disponíveis")
mapa_medicos = mapa_st.map(df)

    


login, cadastro = start_bar.tabs(["Login", "Cadastro"])

with cadastro:
    PageCadastro.Cadastro()
    
with login:
    retorno = PageLogin.login()
    nome = retorno[0]
    senha = retorno[1]
    situacao = retorno[2]
    marcado = checkbox_placeholder.button('Login')


    if marcado:
        aprovar()
        

if st.session_state.login:    
    # if input_senha_func == '1234':
    Banco.create_usertable()
    Banco.create_veterinario()
    Banco.criar_clinica()
    user = Banco.login_user(nome, senha)
    vet = Banco.login_veterinario(nome, senha, situacao)
    #clinica = Banco.login_clinica(nome, senha, situacao)
    

    if user:
        start_bar.empty()
        checkbox_placeholder.empty()
        titulo.empty()
        texto.empty()
        especialidades.empty()
        banco_lista.empty()
        texto_inicio.empty()
        mapa_st.empty()

        Page = PageUsuario.Usuario(nome)

        
    elif vet:
        
        start_bar.empty()
        checkbox_placeholder.empty()
        titulo.empty()
        texto.empty()
        especialidades.empty()
        banco_lista.empty()
        texto_inicio.empty()
        mapa_st.empty()

        PageVeterinario.Veterinario(nome)


    elif senha == '0987':
        titulo.empty()
        texto.empty()
        start_bar.empty()
        checkbox_placeholder.empty()
        especialidades.empty()
        banco_lista.empty()
        texto_inicio.empty()
        mapa_st.empty()

        PageAdm.Adm()               
        
    else:
        st.sidebar.warning("Usuário incorreto ou Inexistente")

