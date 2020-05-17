#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import telebot
from pymongo import MongoClient

bot = telebot.TeleBot(appConfig['tg']['key'].get())

def generate_answer(event, user, message):
    out = []
    user_id = user.id

    out.append("Привет!")

    return out


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(content_types=["text"])
def send_text(message):
    user_message = message.text.lower().encode("utf-8")
    msgs = generate_answer("chat", message.from_user, user_message)
    for msg in msgs:
        bot.send_message(message.chat.id, msg)


bot.polling()