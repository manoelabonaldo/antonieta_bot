import beautifulsoup4
import gspread
import oauth2client
import requests

from oauth2client.service_account import ServiceAccountCredentials

GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")



# Definir URL do site a ser verificado
url = 'https://www.gov.br/trabalho-e-previdencia/pt-br/pt-br/composicao/orgaos-especificos/secretaria-de-trabalho/inspecao/areas-de-atuacao/combate-ao-trabalho-escravo-e-analogo-ao-de-escravo'

# Fazer requisição HTTP para o site e obter seu conteúdo HTML
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Analisar o conteúdo HTML com BeautifulSoup e encontrar todos os links
soup = BeautifulSoup(response.content, 'html.parser')
links = soup.find_all('a')

xlsx_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".xlsx") and "cadastro_de_empregadores" in href:
        xlsx_links.append(href)

if xlsx_links:
    for link in xlsx_links:
        print(link)
else:
    print("Não foi encontrado nenhum arquivo .xlsx files contendo a expressão 'cadastro_de_empregadores'.")
    
lista_sujaatual = link
sheet.append_row([lista_sujaatual])
