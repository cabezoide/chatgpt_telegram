#!/usr/bin/env python3
import telebot
import sys
import openai
import json
import requests


# API KEY reemplazar con las tuyas
API_KEY_TELEGRAM="TU_API_KEY_TELEGRAM"
API_KEY_OPENAI ="TU_API_KEY_OPENAI"


# Crear bot de Telegram
bot = telebot.TeleBot(API_KEY_TELEGRAM, parse_mode=None)
# Credenciales de API ChatGPT
openai.api_key = API_KEY_OPENAI


# Manejador de mensajes de Telegram
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Bot ChatGPT")
@bot.message_handler()
def handle_message(message):
    # Obtener texto del mensaje
    text = message.text

    # Crear solicitud a la API de ChatGPT
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {openai.api_key}"}
    data = json.dumps({
        "prompt": text, 
        "model": "text-davinci-003",
        "temperature":0,
        "max_tokens":500,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0,
        })
    try:
        response = requests.post("https://api.openai.com/v1/completions", headers=headers, data=data)
        # Procesar respuesta de la API de ChatGPT
        response_json = response.json()
        reply_text = response_json["choices"][0]["text"]
        # Enviar respuesta a Telegram
        bot.reply_to(message, reply_text)
    except:
        pass

bot.polling()
