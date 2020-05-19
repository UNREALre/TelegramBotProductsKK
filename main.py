#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import telebot
from logger import log_user_msgs
from generator import generate_answer


bot = telebot.TeleBot(appConfig['tg']['key'].get())


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! \n'
                                      'Я беру данные по продуктам с самой большой и достоверной базы продуктов USDA - Министерство сельского хозяйства США.\n'
                                      'Я помогу тебе узнать из чего состоит то, что ты ешь.\n'
                                      'Пока что я могу помочь тебе узнать только о количестве калорий в твоей еде. \n'
                                      'Напиши свой продукт на английском(!) языке.\n'
                                      'Если есть что сказать/пожелать - пиши мне на webdevre@gmail.com или в ТГ: @UNREALre')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, '1. Напиши /start и я расскажу тебе о себе.\n'
                                      '2. Напиши /top и я покажу тебе топ запросов пользователей.\n'
                                      '3. Напиши /news и я покажу тебе новости по моей разработке.\n'
                                      '4. Напиши название продукта и я попробую найти его калорийность.\n')


@bot.message_handler(commands=['news'])
def start_message(message):
    bot.send_message(message.chat.id, '1. 18.05.2020 Выпущена 1 версия бота.\n')


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