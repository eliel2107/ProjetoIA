from langchain_community.document_loaders import (WebBaseLoader,
                                                  YoutubeLoader,
                                                  CSVLoader,
                                                  TextLoader,
                                                  JSONLoader,
                                                  PyPDFLoader)

url = 'https://asimov.academy/'
def carrega_site(url):
    loader = WebBaseLoader(url)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

url = 'xQirA9nHQ00'
def carrega_youtube(video_id):
    loader = YoutubeLoader(video_id, add_video_info=False, language='pt')
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento



caminho = 'arquivos\knowledge_base.csv'
def carrega_csv(caminho):
    loader = CSVLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

caminho = 'arquivos\RoteiroViagemEgito.pdf'
def carrega_pdf(caminho):
    loader = PyPDFLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento


caminho = 'arquivos\knowledge_base.txt'
def carrega_txt(caminho):
    loader = TextLoader(caminho)
    lista_documentos = loader.load()
    documento = '\n\n'.join([doc.page_content for doc in lista_documentos])
    return documento

documento = carrega_csv(caminho)
print(documento)