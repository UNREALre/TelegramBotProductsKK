#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db, appConfig
import pymongo
from os import listdir
from os.path import isfile, join
import csv

csv_path = str(appConfig['resources']['csv'])


def get_file(mask):
    """Получает маску имени файла
    Возвращает массив с именами файлов найденных, соответствующих переданной маске
    """
    all_files = [cur_file for cur_file in listdir(csv_path) if isfile(join(csv_path, cur_file))]
    required_files = []
    mask = mask.lower()
    for current_file in all_files:
        current_file = current_file.lower()
        if current_file == mask:
            required_files.append(current_file)

    return required_files


def create_index(collection, field, text=False):
    """Создает индекс в коллекции
    Принимает коллекцию и поле, которое должно быть индексом
    """
    if text:
        collection.create_index([(field, 'text')])
    else:
        collection.create_index([(field, pymongo.ASCENDING)], unique=True)


def fill_collection(source_file, source_collection, source_collection_index):
    """Обновляет коллекцию - либо добавляет, либо обновляет документ
    Получает наименование файла с данными и коллекцию.
    Возвращает словарь с двумя ключами: updated и created, в которых указывается
    количество обновленных и созданных документов соответственно"""
    updated, created = 0, 0

    cur_file = open(join(csv_path, source_file))
    csv_reader = csv.DictReader(cur_file)
    for row in csv_reader:
        # if source_file == 'food.csv':
        #    if row['data_type'] != "sr_legacy_food":  # выбираем только данный тип
        #        continue

        # if source_file == 'food_nutrient.csv':
        #    if not food_collection.find_one({"fdc_id": row["fdc_id"]}):
        #        continue

        document = source_collection.find_one({source_collection_index: row[source_collection_index]})
        if not document:
            source_collection.insert_one(row)
            created += 1
        # else:
        #    source_collection.update_one({
        #        '_id': document['_id']
        #    }, {
        #        '$set': row
        #    })
        #    updated += 1

    return {'updated': updated, 'created': created}


food_categories_collection = db['food_category']  # получили коллекцию
food_collection = db['food']
food_nutrient_collection = db['food_nutrient']
nutrient_collection = db['nutrient']

file_to_collection = {
    'food.csv': {
        'collection': food_collection,
        'index': 'fdc_id'
    },
    'food_category.csv': {
        'collection': food_categories_collection,
        'index': 'id'
    },
    'nutrient.csv': {
        'collection': nutrient_collection,
        'index': 'id'
    },
    'food_nutrient.csv': {
        'collection': food_nutrient_collection,
        'index': 'id'
    }
}

fill_results = dict()
for file_mask, collection_info in file_to_collection.items():

    collection_of_file = collection_info['collection']
    collection_index = collection_info['index']

    create_index(collection_of_file, collection_index)
    if file_mask == 'food.csv':
        food_collection.create_index([('description', 'text'), ('description_ru', 'text')])
    if file_mask == 'food_nutrient.csv':
        food_nutrient_collection.create_index('fdc_id')

    files = get_file(file_mask)
    fill_results[file_mask] = []
    if files:
        for file in files:
            fill_results[file_mask].append(fill_collection(file, collection_of_file, collection_index))

for file_name, fill_result in fill_results.items():
    print("Обработан файл: " + file_name)
    for result in fill_result:
        print("Создано: " + str(result['created']) + " шт.")
        print("Обновлено: " + str(result['updated']) + " шт.")
    print("===============================================")