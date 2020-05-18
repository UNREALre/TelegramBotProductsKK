#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db

requests_collection = db['user_request']


def get_top_10_requests(n=10):
    """
    Возвращает топ n запросов пользователей за все время
    По умолчанию - 10
    """
    cursor = requests_collection.aggregate([
        # Group the documents and "count" via $sum on the values
        {'$group': {
            '_id': {
                'request': '$message',
            },
            'times': {'$sum': 1}
        }},
        {'$sort': {'times': -1}},
        {'$limit': n}
    ])

    top = []
    for data in cursor:
        top.append({
            'request': data['_id']['request'],
            'times': data['times']
        })

    return top


def test_top():
    top = get_top_10_requests()
    for item in top:
        print(item)

#test_top()