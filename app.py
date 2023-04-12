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

import bot_telegram
import salva_link

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

#__________________________________[site]____________________________________ 
app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/salva-link">Arquivo da Lista Suja</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
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

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  resposta = requests.post(f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage", data=mensagem)
  return f"Mensagem enviada. Resposta ({resposta.status_code}): {resposta.text}"

@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  update = request.json
  bot_telegram.bot_dotelegram(update)
  return "ok"

@app.route("/salva-link")
def repositorio_listasuja():
  salva_link.puxa_listasuja()
  return menu + "esse é o link de acesso ao repositório da lista suja do trabalho escravo: https://docs.google.com/spreadsheets/d/1xR0Xy-m_UWpxofHRf66xX2O50keDnAlexIFdQTOBa2Q/edit#gid=0"
