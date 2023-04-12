import os 
import pandas as pd
import altair as alt
import json
import requests
import gspread
import openpyxl

from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
GOOGLE_SHEETS_KEY = os.environ["GOOGLE_SHEETS_KEY"]
TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key(f'{GOOGLE_SHEETS_KEY}')
sheet = planilha.worksheet("Página1")

def bot_dotelegram(update): 
   
#__________________________[Análise de dados]__________________

   lista_suja = 'https://www.gov.br/trabalho-e-previdencia/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/cadastro_de_empregadores.xlsx' 
   df = pd.read_excel(lista_suja, skiprows=5)


#excluir colunas vazias
   df.drop(df.iloc[:, 10:96], inplace=True, axis=1)


#excluir linhas as quais não contém dados
   df2=df.dropna()


   Soma_Trabalhadores = df2['Trabalhadores envolvidos'].sum()
   

   Trabalhadores_UF = df2.groupby('UF')['Trabalhadores envolvidos'].sum().sort_values(ascending=False)


   Trabalhadores_UF = Trabalhadores_UF.reset_index()


   a = df2['CNAE'].value_counts()


   a=a.reset_index()



   repeticoesCNAE = df2.pivot_table(index = ['CNAE'], aggfunc ='size')


   Ranking_CNAE = repeticoesCNAE.sort_values(ascending=False)

   Ranking_CNAE = Ranking_CNAE.reset_index()


   Ranking_CNAE['CNAE'] = Ranking_CNAE['CNAE'].astype(str)

   CNAES = {'0134-2/00': 'Cultivo de Café','0151-2/01': 'Criação de bovinos', '0210-1/08' : 'Produção de Carvão Vegetal', '9700-5/00' : 'Trabalho doméstico' }

   b = Ranking_CNAE.replace(CNAES)

#________________________[Fim da análise de dados]_____________________________

   update_id = update['update_id']
   first_name = update['message']['from']['first_name']
   last_name = update['message']['from']['last_name']
   sender_id = update['message']['from']['id']
   date = datetime.fromtimestamp(update['message']['date']).date()
   time = datetime.fromtimestamp(update['message']['date']).time()
   chat_id = update['message']['chat']['id']

   try:
      message = update['message']['text']
   except KeyError:
      print("received unhandled message type")
      message=''

   if message == "oi":
      texto_resposta = f"Olá. 🤖\n\nSou a Antonieta, uma robô que analisa e registra a lista suja do trabalho escravo.\n\nO que você deseja saber em relação à lista suja mais atual?\n\nDigite 1️⃣ para descobrir o número total de trabalhadores que constam na lista suja do trabalho escravo.\nDigite 2️⃣ para saber em quais atividades econômicas o trabalho análogo à escravidão é mais frequente.\nDigite 3️⃣ para descobrir qual foi o estado em que mais pessoas foram resgatadas.\nDigite 4️⃣ para denunciar casos de trabalho análogo à escravidão.\nDigite 5️⃣ para maiores informações sobre trabalho escravo e outras dúvidas.\nDigite 6️⃣ se você quer saber por que eu me chamo Antonieta. \n\n📊🔍Os dados analisados aqui são fornecidos pelo Ministério do Trabalho e Previdência do Brasil por meio do Cadastro de Empregadores que tenham submetido trabalhadores a condições análogas à de escravo (Lista Suja do Trabalho Escravo)."
   elif message == "1":
      texto_resposta = f"Infelizmente o trabalho análogo ao de escravo ainda é uma realidade no Brasil.\n\nNa lista suja mais atual, {int(Soma_Trabalhadores)} trabalhadores foram resgatados em condições análogas à escravidão."
   elif message == "2":
      texto_resposta = f"As atividades econômicas com maior frequência de trabalho escravo na lista suja mais atual são, respectivamente:\n\n{b['CNAE'].loc[0]}, \n{b['CNAE'].loc[1]}, \ne { b['CNAE'].loc[2]}."
   elif message == "3":
      texto_resposta = f"O estado com o maior número de trabalhadores em situação análoga a escravidão é {Trabalhadores_UF['UF'].loc[0]}, com um total de {int(Trabalhadores_UF['Trabalhadores envolvidos'].loc[0])} trabalhadores resgatados. \n\nEsse valor é referente à lista suja mais atual."
   elif message == "4":
      texto_resposta = f"O Ministério do Trabalho usa a plataforma IPÊ para coletar denúncias 🚨 de trabalho análogo à escravidão. O sigilo da denúncia é garantido e você pode realizá-la clicando no link a seguir. https://ipe.sit.trabalho.gov.br/#!/"
   elif message == "5":
      texto_resposta = f"A maioria dos trabalhadores que formam a mão de obra escrava é migrante, de baixa renda, oriunda de regiões marcadas pela fome e pobreza, onde há pouca oportunidade de sustento. \n\nLonge das estruturas de proteção social, eles são facilmente envolvidos por relações de trabalho violentas e têm sua força de trabalho extraída ao máximo. \n\nMuitos acabam sendo explorados e expostos a condições de trabalho degradantes, sem acesso à água potável, banheiro, comida de qualidade, sem um teto digno, vivendo sob ameaças e sem pagamento.\n\n⚖️ O Art. 149. do CP afirma ser crime reduzir alguém a condição análoga à de escravo quando há:  \n\n- Trabalho forçado; \n- Condições degradantes de trabalho; \n- Restrição de locomoção; \n- Servidão por dívida.  \n\nConsidera-se trabalho escravo quando alguma das situações é observada.\n\n📂 Para acessar a Lista Suja do Trabalho Escravo, acesse o link abaixo. www.gov.br/trabalho-e-previdencia/pt-br/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo\n\n\n🤖 O robô do trabalho escravo foi desenvolvido por Manoela Bonaldo (📩 bonaldomanoela@gmail.com) para a disciplina de Algoritmos de Automação, dos professores Álvaro Justen e Guilherme Felitti, no Master em Jornalismo de Dados, Automação e Datastorytelling, no Insper.\n\n"
   elif message == "6":
      texto_resposta = f"Meu nome é uma homenagem à incrível Antonieta de Barros, a primeira mulher negra eleita para um cargo político no Brasil.👩🏿\n\nIsso se deu nas eleições de 1934, primeiro pleito em quem mulheres puderam votar e serem votadas no país.\n\nAntonieta nasceu 13 anos após a escravidão ser abolida no Brasil.\n\nPioneira no combate à discriminação de gênero e raça, ela foi jornalista e professora e, inclusive, a educação era sua principal bandeira, que para ela se traduzia numa das principais fontes de força e libertação humana.\n\nAntonieta nasceu em Desterro, cidade que hoje se chama Florianópolis. Floripa também é a cidade natal de quem me programou e foi lá que meus primeiros códigos em Python começaram a ser escritos.💻\n\nAinda que eu seja apenas uma robô, sei da importância de lembrarmos do nosso passado e de quem contribuiu para os avanços na história.\n\nAntonieta era filha de Catarina de Barros, uma ex-escrava. Como mostrei alguns dados para você anteriormente, a escravidão contemporânea ainda persiste no país. Meu objetivo é analisar as nuances desse problema tão grave e disseminar informações detalhadas para que vocês, humanos, consigam colocar de vez um ponto final na escravidão no Brasil. ✊"
   else:
      texto_resposta = f"Olá. 🤖\n\nSou a Antonieta, uma robô que analisa e registra a lista suja do trabalho escravo.\n\nO que você deseja saber em relação à lista suja mais atual?\n\nDigite 1️⃣ para descobrir o número total de trabalhadores que constam na lista suja do trabalho escravo.\nDigite 2️⃣ para saber em quais atividades econômicas o trabalho análogo à escravidão é mais frequente.\nDigite 3️⃣ para descobrir qual foi o estado em que mais pessoas foram resgatadas.\nDigite 4️⃣ para denunciar casos de trabalho análogo à escravidão.\nDigite 5️⃣ para maiores informações sobre trabalho escravo e outras dúvidas.\nDigite 6️⃣ se você quer saber por que eu me chamo Antonieta. \n\n📊🔍Os dados analisados aqui são fornecidos pelo Ministério do Trabalho e Previdência do Brasil por meio do Cadastro de Empregadores que tenham submetido trabalhadores a condições análogas à de escravo (Lista Suja do Trabalho Escravo)."

   nova_mensagem = {"chat_id": chat_id, "text": texto_resposta}
   resposta = requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data = nova_mensagem)
    # Atualiza planilha do sheets com último update processado
   sheet.append_row([first_name, last_name, sender_id, message])

   return "ok"
