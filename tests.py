#! /usr/bin/env python
# -*- coding: utf-8 -*-

from generator import generate_answer


def test_search(name):
    msgs = generate_answer("chat", {}, name)
    for msg in msgs:
        print(msg)


name = input()
while name != "0":
    test_search(name)
    print("===================")
    name = input()

#food_collection.create_index([('description', 'text'), ('description_ru', 'text')])