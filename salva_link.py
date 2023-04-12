import gspread
import oauth2client
import requests
import datetime
import pytz
import os
import bs4

from bs4 import BeautifulSoup


from oauth2client.service_account import ServiceAccountCredentials


def puxa_listasuja(): 

  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
  TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1xR0Xy-m_UWpxofHRf66xX2O50keDnAlexIFdQTOBa2Q")
  sheet = planilha.worksheet("Página1")
  
  today = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  url = 'https://www.gov.br/trabalho-e-previdencia/pt-br/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo'
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  links = soup.find_all('a')

  xlsx_links = []
  for link in soup.find_all("a"):
      href = link.get("href")
      if href and href.endswith(".xlsx") and "cadastro_de_empregadores" in href:
          xlsx_links.append(href)

  if xlsx_links:
      for link in xlsx_links:
          print(link)
          lista_sujaatual = link
          sheet.append_row([lista_sujaatual, today])
          print('Informações adicionadas com sucesso.')
  else:
      print("Não foi encontrado nenhum arquivo .xlsx files contendo a expressão 'cadastro_de_empregadores'.")
