#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import telebot
from products import find_products, prepare_products
from logger import log_user_msgs
from stats import get_top_10_requests

bot = telebot.TeleBot(appConfig['tg']['key'].get())


def generate_answer(event, user, message):
    out = []
    user_id = user.id

    if event == "chat":
        products = find_products(str(message))
        msg = []
        if products:
            products = prepare_products(products)

            for product in products:
                msg.append('Продукт: %s (%s). Калорийность: %s ККАЛ' % (product['description_ru'], product['description'], product['kk']))
        else:
            msg.append("Извини, я не могу найти продукт в базе. Попробуй ввести что-то еще. Не забывай, что пока я только знаю английский язык.")

        out.append('\n'.join(msg))

    else:
        if message == "top":
            msg = []
            top = get_top_10_requests()
            for item in top:
                msg.append("Запрос: %s. Кол-во: %s" % (item['request'], item['times']))

            out.append('\n'.join(msg))

    return out


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе узнать из чего состоит то, что ты ешь. Пока что я могу помочь тебе узнать только о количестве калорий в твоей еде. Напиши свой продукт на английском языке.')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '1. Напиши /start и я расскажу тебе о себе.\n'
                                      '2. Напиши /top и я покажу тебе топ запросов пользователей.\n'
                                      '3. Напиши название продукта и я попробую найти его калорийность.\n'
                                      'Пока что на русский переведено примерно 30% базы. Поэтому пробуй как английские, так и русские названия еды.\n'
                                      'Если есть что сказать/пожелать - пиши мне на webdevre@gmail.com или в ТГ: @UNREALre')


@bot.message_handler(commands=['top'])
def start_message(message):
    bot.send_message(message.chat.id, 'Топ 10 запросов пользователей за все время:')
    msgs = generate_answer("command", message.from_user, 'top')
    for msg in msgs:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=["text"])
def send_text(message):
    log_user_msgs(message.text, message.from_user)
    user_message = message.text.lower()
    msgs = generate_answer("chat", message.from_user, user_message)
    for msg in msgs:
        bot.send_message(message.chat.id, msg)


bot.polling()