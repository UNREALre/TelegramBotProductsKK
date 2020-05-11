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
    userMessage = message.text.lower().encode('utf-8')
    if userMessage == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif userMessage == 'мяу':
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAINHV65UcH0-Qf80HIztYDHafoxf6F6AAJ1AAPZvGoaxRDGAz1iuPEZBA')
    else:
        bot.send_message(message.chat.id, 'Зачем ты мне написал мне - ' + userMessage + ' ?')


bot.polling()
