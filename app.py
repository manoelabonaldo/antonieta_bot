import os

import gspread
import requests
import altair as alt
import pandas as pd
import openpyxl

from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
from datetime import datetime



TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]

with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1Sw8CTJRvdJQIC6YasjpDv5ofZEE0GeB_182Hr0E01Zg")
sheet = planilha.worksheet("Página1")

app = Flask(__name__)

#_________________________[análise dos dados]_________________________


  
#acessar a página do Ministério do Trabalho e analisar a Lista Suja, disponibilizada em .xls
lista_suja = 'https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/cadastro_de_empregadores.xlsx' 
df = pd.read_excel(lista_suja, skiprows=5)
df

#excluir colunas vazias
df.drop(df.iloc[:, 10:96], inplace=True, axis=1)
df

#excluir linhas as quais não contém dados
df2=df.dropna()
df2

Soma_Trabalhadores = df2['Trabalhadores envolvidos'].sum()
print(Soma_Trabalhadores)

Trabalhadores_UF = df2.groupby('UF')['Trabalhadores envolvidos'].sum().sort_values(ascending=False)
Trabalhadores_UF

Trabalhadores_UF = Trabalhadores_UF.reset_index()
Trabalhadores_UF

a = df2['CNAE'].value_counts()
print(a)

a=a.reset_index()

a.info()

repeticoesCNAE = df2.pivot_table(index = ['CNAE'], aggfunc ='size')

Ranking_CNAE = repeticoesCNAE.sort_values(ascending=False)

Ranking_CNAE = Ranking_CNAE.reset_index()
Ranking_CNAE

Ranking_CNAE['CNAE'] = Ranking_CNAE['CNAE'].astype(str)

CNAES = {'0134-2/00': 'Cultivo de Café','0151-2/01': 'Criação de bovinos', '0210-1/08' : 'Produção de Carvão Vegetal', '9700-5/00' : 'Trabalho doméstico' }

b = Ranking_CNAE.replace(CNAES)


#_________________________[fim da análise dos dados]_________________________

#__________________________________[site]____________________________________ 

menu = """
<a href="/">Página inicial</a> | <a href="/arquivolistasuja">Arquivo da Lista Suja</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, este é o site do robô do trabalho escravo."

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato"

@app.route("/arquivolistasuja")
def arquivolistasuja():
  return menu + "Aqui vai o conteúdo de arquivo da lista suja"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Manoela", "Bonaldo", "a partir do Flask"])
  return "Planilha escrita!"

 #______________________________[fim do site]_________________________________ 
 
  
 #__________________________________[bot]_____________________________________
 
@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  mensagens = []

  update = request.json
  
  if request.method == 'POST':
     update = request.get_json()
    
  update_id = update['update_id']
  first_name = update['message']['from']['first_name']
  last_name = update['message']['from']['last_name']
  user_name = update['message']['from']['username']
  sender_id = update['message']['from']['id']
  date = datetime.fromtimestamp(update['message']['date']).date()
  time = datetime.fromtimestamp(update['message']['date']).time()
  chat_id = update['message']['chat']['id']
  
  try:
      message = update['message']['text']
  except KeyError:
      print("received unhandled message type")
      message=''
  #return chat_id, texto
  
  if "username" in update["message"]["from"]:
    username = f' @{update["message"]["from"]["username"]}'
  else:
    username = ""

  
  if message == "oi":
     texto_resposta = f"Olá. 🤖\n\nSou a Antonieta, uma robô que analisa e registra a lista suja do trabalho escravo.\n\nO que você deseja saber em relação à lista suja mais atual?\n\nDigite 1️⃣ para descobrir o número total de trabalhadores que constam na lista suja do trabalho escravo.\nDigite 2️⃣ para saber em quais atividades econômicas o trabalho análogo à escravidão é mais frequente.\nDigite 3️⃣ para descobrir qual foi o estado em que mais pessoas foram resgatadas.\nDigite 4️⃣ para denunciar casos de trabalho análogo à escravidão.\nDigite 5️⃣ para maiores informações sobre trabalho escravo e outras dúvidas. \n\n📊🔍Os dados analisados aqui são fornecidos pelo Ministério do Trabalho e Previdência do Brasil por meio do Cadastro de Empregadores que tenham submetido trabalhadores a condições análogas à de escravo (Lista Suja do Trabalho Escravo)."
  elif message == "1":
     texto_resposta = f"Infelizmente o trabalho análogo ao de escravo ainda é uma realidade no Brasil.\n\nNa lista suja mais atual, {int(Soma_Trabalhadores)} trabalhadores foram resgatados em condições análogas à escravidão."
  elif message == "2":
     texto_resposta = f"As atividades econômicas com maior frequência de trabalho escravo na lista suja mais atual são, respectivamente:\n\n{b['CNAE'].loc[0]}, \n{b['CNAE'].loc[1]}, \ne { b['CNAE'].loc[2]}."
  elif message == "3":
     texto_resposta = f"O estado com o maior número de trabalhadores em situação análoga a escravidão é {Trabalhadores_UF['UF'].loc[0]}, com um total de {int(Trabalhadores_UF['Trabalhadores envolvidos'].loc[0])} trabalhadores resgatados. \n\nEsse valor é referente à lista suja mais atual."
  elif message == "4":
     texto_resposta = f"O Ministério do Trabalho usa a plataforma IPÊ para coletar denúncias 🚨 de trabalho análogo à escravidão. O sigilo da denúncia é garantido e você pode realizá-la clicando no link a seguir. https://ipe.sit.trabalho.gov.br/#!/"
  elif message == "5":
     texto_resposta = f"A maioria dos trabalhadores que formam a mão de obra escrava é migrante, de baixa renda, oriunda de regiões marcadas pela fome e pobreza, onde há pouca oportunidade de sustento. \n\nLonge das estruturas de proteção social, eles são facilmente envolvidos por relações de trabalho violentas e têm sua força de trabalho extraída ao máximo. \n\nMuitos acabam sendo explorados e expostos a condições de trabalho degradantes, sem acesso à água potável, banheiro, comida de qualidade, sem um teto digno, vivendo sob ameaças e sem pagamento.\n\n⚖️ O Art. 149. do CP afirma ser crime reduzir alguém a condição análoga à de escravo quando há:  \n\n- Trabalho forçado; \n- Condições degradantes de trabalho; \n- Restrição de locomoção; \n- Servidão por dívida.  \n\nConsidera-se trabalho escravo quando alguma das situações é observada.\n\n📂 Para acessar a Lista Suja do Trabalho Escravo, acesse o link abaixo. www.gov.br/trabalho-e-previdencia/pt-br/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo\n\n\n🤖 A Antonieta, robô que analisa a lista suja trabalho escravo, foi desenvolvida por Manoela Bonaldo (📩 bonaldomanoela@gmail.com) para a disciplina de Algoritmos de Automação, dos professores Álvaro Justen e Guilherme Felitti, no Master em Jornalismo de Dados, Automação e Datastorytelling, no Insper. Um agradecimento também a Bernardo Vianna, Eduardo Cuducos e Pedro Burgos :)\n\n"
  else:
     texto_resposta = f"Olá. 🤖\n\nSou a Antonieta, uma robô que analisa e registra a lista suja do trabalho escravo.\n\nO que você deseja saber em relação à lista suja mais atual?\n\nDigite 1️⃣ para descobrir o número total de trabalhadores que constam na lista suja do trabalho escravo.\nDigite 2️⃣ para saber em quais atividades econômicas o trabalho análogo à escravidão é mais frequente.\nDigite 3️⃣ para descobrir qual foi o estado em que mais pessoas foram resgatadas.\nDigite 4️⃣ para denunciar casos de trabalho análogo à escravidão.\nDigite 5️⃣ para maiores informações sobre trabalho escravo e outras dúvidas. \n\n📊🔍Os dados analisados aqui são fornecidos pelo Ministério do Trabalho e Previdência do Brasil por meio do Cadastro de Empregadores que tenham submetido trabalhadores a condições análogas à de escravo (Lista Suja do Trabalho Escravo)."

  nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
  resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data = nova_mensagem)
  return "ok"

  
  #___________________________________[fim do bot]______________________________________
