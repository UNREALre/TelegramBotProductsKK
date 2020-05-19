#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
from products import find_products, prepare_products
from stats import get_top_10_requests

per_page = int(str(appConfig['app']['perPage']))


def generate_answer(event, message, page=1):
    out = []

    if event == "chat":
        msg = []
        products = find_products(str(message), page)
        if products:
            products = prepare_products(products)

            for product in products:
                msg.append('%s. Калорийность: %s кк.\n' % (product['description'], product['kk']))
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