#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import appConfig
import csv
import json
from os import listdir
from os.path import isfile, join

csv_path = str(appConfig['resources']['csv'])
json_path = str(appConfig['resources']['json'])
csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f))]

files_converted = []
for csv_file in csv_files:
    data = []

    cur_file = open(join(csv_path, csv_file))
    csv_reader = csv.DictReader(cur_file)

    json_file = open(join(json_path, csv_file.split('.')[0]+'.json'), 'w+')

    for row in csv_reader:
        data.append(row)

    json_file.write(json.dumps(data, indent=4))

    files_converted.append(join(csv_path, csv_file) + " => " + join(json_path, csv_file.split('.')[0]+'.json'))

print('\n'.join(files_converted))