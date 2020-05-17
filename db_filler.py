#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db
import pymongo
from pymongo import MongoClient

food_categories = db['food_category']  # получили коллекцию

# создаем индекс
food_categories.create_index([('id', pymongo.ASCENDING)], unique=True)


def fill_product_categories(food_category_data):
    updated, created, deleted = 0, 0, 0
    for food_category in food_category_data:
        existed_category = food_categories.find_one({'id': 1})
        if not existed_category:
            food_categories.insert_one(food_category)
            created += 1
        else:
            food_categories.update_one({
                '_id': existed_category['_id']
            }, {
                '$set': food_category
            })
            updated += 1

    return {'updated': updated, 'created': created, 'deleted': deleted}


data = [{
    "id": 1,
    "code": "0100",
    "description": "Dairy and Egg Products"
}]
result = fill_product_categories(data)

print("Категорий создано: " + str(result['created']) + " шт.")
print("Категорий обновлено: " + str(result['updated']) + " шт.")
print("Категорий удалено: " + str(result['deleted']) + " шт.")
