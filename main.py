#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import confuse
import telebot

projectRoot = os.path.dirname(os.path.abspath("config.yaml"))
os.environ["PRODUCTSKKDIR"] = projectRoot

config = confuse.Configuration('ProductsKK')

bot = telebot.TeleBot(config['tg']['key'].get())

@bot.message_handler(commands=['start'])
def startMessage(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')

@bot.message_handler(content_types=['text'])
def sendText(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif message.text.lower() == 'мяу':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAINHV65UcH0-Qf80HIztYDHafoxf6F6AAJ1AAPZvGoaxRDGAz1iuPEZBA')
    else:
        bot.send_message(message.chat.id, 'Что-что ?')

bot.polling()