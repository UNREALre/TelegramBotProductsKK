#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import telebot
from products import find_products, prepare_products
from logger import log_user_msgs

bot = telebot.TeleBot(appConfig['tg']['key'].get())


def generate_answer(event, user, message):
    out = []
    user_id = user.id

    products = find_products(str(message))
    msg = []
    if products:
        products = prepare_products(products)

        for product in products:
            msg.append('Продукт: %s (%s). Калорийность: %s' % (product['description_ru'], product['description'], product['kk']))
    else:
        msg.append("Извини, я не могу найти продукт в базе. Попробуй ввести что-то еще. Не забывай, что пока я только знаю английский язык.")

    out.append('\n'.join(msg))

    return out


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе узнать из чего состоит то, что ты ешь. Пока что я могу помочь тебе узнать только о количестве калорий в твоей еде. Напиши свой продукт на английском языке.')


@bot.message_handler(content_types=["text"])
def send_text(message):
    log_user_msgs(message.text, message.from_user)
    user_message = message.text.lower()
    msgs = generate_answer("chat", message.from_user, user_message)
    for msg in msgs:
        bot.send_message(message.chat.id, msg)


bot.polling()