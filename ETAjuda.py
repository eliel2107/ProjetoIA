import tempfile

import streamlit as st
from langchain.memory import ConversationBufferMemory

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate


from Loaders import *


API_KEY_DEFAULT =  "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"
TIPOS_ARQUIVOS_VALIDOS = ['Site','csv', 'txt', 'Youtube', 'PDF']

CONFIG_MODELOS = {'OpenAI':
                    {'modelos': ['gpt-4o-mini', 'gpt-4o', 'o1-preview', 'o1-mini'],
                     'chat': ChatOpenAI}}

def carrega_arquivos(tipo_arquivo, arquivo):
    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)
    
    if tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)

    if tipo_arquivo == 'PDF':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)

    if tipo_arquivo == 'csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_csv(nome_temp)

    if tipo_arquivo == 'txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_txt(nome_temp)
    return documento



MEMORIA = ConversationBufferMemory()
def carrega_modelo(provedor, modelo, api_key, tipo_arquivo, arquivo):

    documento = carrega_arquivos(tipo_arquivo, arquivo)

    system_message = '''Você é um assistente amigável chamado ET te Ajudo.
    Você possui acesso às seguintes informações vindas 
    de um documento {}: 

    ####
    {}
    ####

    Utilize as informações fornecidas para basear as suas respostas.

    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''.format(tipo_arquivo, documento)
    
    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    chat = CONFIG_MODELOS[provedor]['chat'](model=modelo, api_key=api_key)
    chain = template | chat

    st.session_state['chain'] = chain
   
    

def pagina_chat():
    st.header("👽 Bem-Vindo ao ET-Ajuda Chat", divider=True)

    chain = st.session_state.get("chain")

    if chain is None:
        st.error("Carregue o ET te ajuda!")
        st.stop()


    memoria = st.session_state.get("memoria", MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)


    input_usuario = st.chat_input("Fale com o com o ET te Ajuda")
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input' :input_usuario,
            'chat_history' : memoria.buffer_as_messages
            }))
        
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria
        



def sidebar():
    tabs = st.tabs(['Upload de Arquivos', 'Seleção de Modelos'])
    
    with tabs[0]:
        tipo_arquivo = st.selectbox('Selecionar Arquivo', TIPOS_ARQUIVOS_VALIDOS)
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite o endereço do site')
        elif tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite o endereço do Video')
        elif tipo_arquivo == 'PDF':
            arquivo = st.file_uploader('Faça o upload do PDF', type=['pdf'])
        elif tipo_arquivo == 'csv':
            arquivo = st.file_uploader('Faça o upload do CSV', type=['csv'])
        elif tipo_arquivo == 'txt':
            arquivo = st.file_uploader('Faça o upload do txt', type=['txt'])
    
    with tabs[1]:
        provedor = st.selectbox('Selecione o provedor', CONFIG_MODELOS.keys())
        modelo = st.selectbox('Selecione o modelo', CONFIG_MODELOS[provedor]['modelos'])
        
        # Define a chave da API diretamente no session_state
        st.session_state[f'api_key_{provedor}'] = API_KEY_DEFAULT

   

    if st.button('Pedir Ajuda ao ET te ajuda', use_container_width=True):
        carrega_modelo(provedor, modelo, API_KEY_DEFAULT, tipo_arquivo, arquivo)
    if st.button('Apagar Histórico', use_container_width=True):
        st.session_state['memoria'] = MEMORIA







def main():
    with st.sidebar:
        sidebar()
    pagina_chat()
    


if __name__ == "__main__":
    main()