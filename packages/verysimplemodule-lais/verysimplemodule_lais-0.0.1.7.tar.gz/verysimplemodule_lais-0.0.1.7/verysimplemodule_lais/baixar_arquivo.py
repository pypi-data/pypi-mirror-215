import requests

def baixar_arquivo(url, endereco):
    resposta = requests.get(url)
    with open('test.pdf', 'wb') as novo_arquivo:
        novo_arquivo.write(resposta.content)

