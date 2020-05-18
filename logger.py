#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import db
import datetime


def log_user_msgs(message, user):
    """
    Логирует все запросы пользователя к боту
    Получает сообщение от пользователя, пользователя и в какую коллекцию записывать
    user - {'id': 99760649, 'is_bot': False, 'first_name': 'ALex', 'username': 'Test',
    'last_name': 'P', 'language_code': 'ru'}
    """
    user_request_collection = db['user_request']
    user_request_collection.insert_one({
        "message": message,
        "user_id": user.id,
        "user_fname": user.first_name,
        "user_lname": user.last_name,
        "user_username": user.username,
        "user_lang_code": user.language_code,
        "time": datetime.datetime.now()
    })
