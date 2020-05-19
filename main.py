#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logger import log_user_msgs
from generator import generate_answer
from products import count_matched_documents
import math
from telegram_bot_pagination import InlineKeyboardPaginator

bot = telebot.TeleBot(appConfig['tg']['key'].get())
per_page = int(str(appConfig['app']['perPage']))


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
    bot.send_message(message.chat.id, '1. 18.05.2020 Выпущена 1 версия бота.\n'
                                      '2. 19.05.2020 Отказ от локализации русской. Бот понимает только EN. Добавлено поле 200 тысяч брендированных товаров. Оптимизирован поиск.')


@bot.message_handler(commands=['top'])
def start_message(message):
    bot.send_message(message.chat.id, 'Топ 10 запросов пользователей за все время:')
    msgs = generate_answer("command", message.from_user, 'top')
    for msg in msgs:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=["text"])
def send_text(message, page=1, for_paging=False):
    if not for_paging:
        log_user_msgs(message.text, message.from_user)
        user_message = message.text.lower()
        chat_id = message.chat.id
    else:
        user_message, chat_id = message.split("~")

    msgs = generate_answer("chat", user_message, page)

    total = count_matched_documents(user_message)

    # markup = generate_pages(total, page, user_message)
    # bot.send_message(
    #    message.chat.id,
    #    msgs,
    #    reply_markup=markup
    # )

    if total > per_page:
        paginator = InlineKeyboardPaginator(
            math.ceil(total / per_page),
            current_page=page,
            data_pattern=user_message+'~'+str(chat_id)+'#{page}'
        )

    bot.send_message(
        chat_id,
        msgs,
        reply_markup=paginator.markup if total > per_page else [],
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    call_data = call.data.split("#")
    user_message = call_data[0]
    page = int(call_data[1])

    send_text(user_message, page, True)


def generate_pages(total, page, message):
    """
    НЕ ИСПОЛЬЗУЕТСЯ
    Получает количество документов запроса и текущую активную страницу
    Возвращает разметку для кнопок пагинаций
    """
    total = math.ceil(total / per_page)
    total = 10

    markup = InlineKeyboardMarkup()
    markup.row_width = 10
    for i in range(1, total):
        markup.add(InlineKeyboardButton(i, callback_data=("%s#%s" % (message, i))))

    return markup


bot.polling()
