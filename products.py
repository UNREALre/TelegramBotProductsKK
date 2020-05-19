#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db, appConfig

food_collection = db['food']
food_categories_collection = db['food_category']
food_nutrient_collection = db['food_nutrient']
nutrient_collection = db['nutrient']
per_page = int(str(appConfig['app']['perPage']))


def find_products(name, page=1):
    """
    Ищет все данные по продукту в базе
    Получает наименование продукта
    Возвращает список продуктов с полной информацией из базы
    """

    """
    max_len = len(name) + 10
    cursor = food_collection.find(
        # {
        #    '$or': [
        #        {'$where': 'this.description.length < ' + str(max_len)},
        #        {'$where': 'this.description_ru.length < ' + str(max_len)},
        #    ],
        #    '$text': {'$search': name}
        # },
        #{'$where': 'this.description.length < 35', '$text': {'$search': name}},
        {'$text': {'$search': name}},
        {'score': {'$meta': "textScore"}},
    ).limit(per_page)
    cursor.sort([('score', {'$meta': 'textScore'})])
    """
    cursor = food_collection.aggregate([
        {'$match': {'$text': {'$search': name}}},
        {'$project': {
            'fdc_id': 1,
            'description': 1,
            'field_length': {'$strLenCP': '$description'}
        }},
        {'$sort': {'field_length': 1}},
        {'$skip': (page-1) * per_page},
        {'$limit': per_page}
    ])
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


def count_matched_documents(name):
    """
    Получает запрос
    Возвращает количество документов, удовлетворяющих запросу
    """
    return food_collection.find(
        {'$text': {'$search': name}}
    ).count()


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
            # 'description_ru': cur_product['description_ru'],
            'kk': cur_product['nutrient']['amount']
        })

    return prepared_products

