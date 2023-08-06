import requests

def baixar_arquivo(url, endereco):
    resposta = requests.get(url)
    with open('test.pdf', 'wb') as novo_arquivo:
        novo_arquivo.write(resposta.content)

if __name__ == "__main__":
    baixar_arquivo()