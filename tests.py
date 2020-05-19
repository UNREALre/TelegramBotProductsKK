#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db
from products import find_products


def test_search(name):
    products = find_products(name)
    for product in products:
        print(product['fdc_id'], product['description'], sep='; ')


test_search("сыр")
print("===================")
test_search("Mars")
print("===================")
test_search("Snickers")
print("===================")

#food_collection.create_index([('description', 'text'), ('description_ru', 'text')])