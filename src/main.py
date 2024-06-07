import os
from pathlib import Path
BASE_DIR = str(Path(os.path.dirname(__file__)).parent)# Diretorio Base do programa
from dotenv import load_dotenv #instalar o pacote python-dotenv
load_dotenv()# Para ler as variaveis do arquivo .env
# Importe a biblioteca Pandas
import pandas as pd 
# Importar as funções contidas no meuPacotes
from meuPacote.bookToScrape import getPrice
from meuPacote.email import enviar_email
def main():
    #arquivo com os 12 romances desejados com suas respectivas metas de preço   
    file = BASE_DIR + '/data/livros_classics.xlsx'
    # leia esse file e grave em uma variavel df no formato pd.DataFrame
    df = pd.read_excel(file)

    # Pegue os preços atuais do livro usando a função getPrice()
    listaPrecos = []
    listaNomes = df['titulo'].tolist()
    for numero in listaNomes:
        preco = getPrice(numero)
        listaPrecos.append(preco)
    print(listaPrecos)
    # Verifique os paramentros da função atraves do help(getPrice)

    #Crie uma coluna nova no df com o nome "preco_atual" e insira os preços atuais de cada livro
    df['preco_atual'] = listaPrecos
    print(df)

    # Grave esse novo df em uma planilha excel com o nome "preco_atual.xlsx"
    df.to_excel (BASE_DIR + '/data/Precos_atual.xlsx')


    # Crie o arquivo .env e insira o seu usuario e senha do yahoo
    usuario = os.environ.get("YAHOO_USER") #pega o usuario do arquivo .env
    senha = os.environ.get("YAHOO_PASSWORD") #pega a senha do arquivo .env

    # Verifique quais os livros estão com os preços abaixo da meta e envie os nomes desses livros para o seu email, colocando-os nos nomes dos livros na mensagem.
    # Use a funcao enviar_email
    # verifique os parametros de entrada dessa funcao atraves do help(enviar_email)
    df2 =df.query("meta>preco_atual")
    promocao =  df2  ['titulo'].values
    destinatario = "lupixajello@gmail.com"
    assunto = "Livros em promoção!"
    mensagem = f"segue os livros em promoção :{promocao} "
    enviar_email(usuario,senha,destinatario,assunto,mensagem)
    print(f'Email enviado com sucesso!')

if __name__ == '__main__':
    main()

