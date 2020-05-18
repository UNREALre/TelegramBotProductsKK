#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db, appConfig
from yandex_translate import YandexTranslate
import json
from os.path import join

translate = YandexTranslate([appConfig['yandex']['trans_key']])

trans_path = str(appConfig['resources']['trans'])


def translate_food():
    translated = 0
    food_collection = db["food"]
    foods = food_collection.aggregate([
        {'$project': {
            'description': 1,
            'description_ru': 1,
            'description_length': {'$strLenCP': '$description'},
        }},
        {'$match': {
                'description_ru': {
                    '$exists': False,
                }
            }
        },
        {'$sort': {'description_length': 1}},
        #{'$limit': 10}
    ])
    for food in foods:
        description = food['description']
        print(description)
        trans = translate.translate(description, 'en-ru')
        description_ru = trans['text'][0]
        print(trans)
        print(description_ru)

        if description_ru:
            food_collection.update_one({
                '_id': food['_id']
            }, {
                '$set': {
                    "description_ru": description_ru
                }
            })
            translated += 1

    return translated


def get_translated():
    """
    Возвращает список документов уже переведенных
    """
    food_collection = db['food']
    cursor = food_collection.find({
        'description_ru': {'$exists': True}
    }, {
       'fdc_id': 1,
       'description_ru': 1
    })
    foods = []
    for food in cursor:
        cur_food = {
            'fdc_id': food['fdc_id'],
            'description_ru': food['description_ru']
        }
        foods.append(cur_food)

    return foods


def save_translated(foods):
    """
    Сохраняет то, что уже переведено яндексом в файл для последующего занесения в БД на проде
    Получает список переведенных документов
    """
    json_file = open(join(str(appConfig['resources']['trans']), 'trans.json'), 'w+', encoding="utf-8")
    json_file.write(json.dumps(foods, indent=4, ensure_ascii=False))


def update_translated():
    """
    Функция используется на проде, бежит по файлику с переводами и присвает ID-шникам переведенные значения
    Подразумевается, что на проде переводов нет
    """
    with open(join(str(appConfig['resources']['trans']), 'trans.json'), encoding='utf-8') as food:
        data = json.load(food)

    food_collection = db['food']
    for food in data:
        food_collection.update_one({
            'fdc_id': food['fdc_id']
        }, {
            '$set': {
                "description_ru": food['description_ru']
            }
        })


#food_trans_counter = translate_food()
#print("Переведено продуктов %s шт." % food_trans_counter)


#trans_foods = get_translated()
#save_translated(trans_foods)
update_translated()