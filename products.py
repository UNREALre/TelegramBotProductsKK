#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db
import re
import pymongo

food_collection = db['food']
food_categories_collection = db['food_category']
food_nutrient_collection = db['food_nutrient']
nutrient_collection = db['nutrient']


def find_products(name):
    """
    Ищет все данные по продукту в базе
    Получает наименование продукта
    Возвращает список продуктов с полной информацией из базы
    """
    print(name)
    max_len = len(name) + 10
    cursor = food_collection.find(
        {'$where': 'this.description.length < ' + str(max_len), '$text': {'$search': name}},
        {'score': {'$meta': "textScore"}},
    ).limit(20)
    cursor.sort([('score', {'$meta': 'textScore'})])
    cur_products = []
    for cur_product in cursor:
        nutrients = food_nutrient_collection.find(
            {'fdc_id': cur_product['fdc_id'], 'nutrient_id': '1008'},
            {'amount': 1}
        )
        for nutrient in nutrients:
            cur_product['nutrient'] = nutrient
        cur_products.append(cur_product)

    return cur_products


def prepare_products(db_products):
    """Подготавливает для передачи пользователю данные.
    Получает список продуктов из базы.
    Возвращает форматированный массив словарей с необходимыми пользователю данными"""
    prepared_products = []
    for cur_product in db_products:
        prepared_products.append({
            '_id': cur_product['_id'],
            'fdc_id': cur_product['fdc_id'],
            'description': cur_product['description'],
            'kk': cur_product['nutrient']['amount']
        })

    return prepared_products
