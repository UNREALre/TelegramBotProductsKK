#! /usr/bin/env python
# -*- coding: utf-8 -*-

from generator import generate_answer


def test_search(name):
    msgs = generate_answer("chat", {}, name)
    for msg in msgs:
        print(msg)


test_search("сыр")
print("===================")
test_search("Mars")
print("===================")
test_search("Snickers")
print("===================")

#food_collection.create_index([('description', 'text'), ('description_ru', 'text')])