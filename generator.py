#! /usr/bin/env python
# -*- coding: utf-8 -*-

from products import find_products, prepare_products
from stats import get_top_10_requests


def generate_answer(event, user, message, page=1):
    out = []
    #user_id = user.id

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
