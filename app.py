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

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]

#__________________________________[site]____________________________________ 

app = Flask(__name__)

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

@app.route("/telegram-bot", methods=['POST'])
def telegram_bot():
  update = request.json
  bot_telegram.bot_dotelegram(update)
  return "ok"

@app.route("/salva-lista")
def arquivolistasuja():
  return menu + "Aqui vai o conteúdo de arquivo da lista suja"

