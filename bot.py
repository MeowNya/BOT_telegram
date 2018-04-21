#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Maia'


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json
from config import API_TOKEN_DIALOG_FLOW, API_TOKEN_TELEGRAM


updater = Updater(token=API_TOKEN_TELEGRAM)  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello you!')


def text_message(bot, update):
    request = apiai.ApiAI(API_TOKEN_DIALOG_FLOW).text_request()
    request.lang = 'ru'
    request.session_id = 'PyChatBotLW'
    request.query = update.message.text
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Не понял!')


# Хендлеры
start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
