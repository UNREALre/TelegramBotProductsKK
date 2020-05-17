import os
import confuse
import urllib.parse
import pymongo

project_root = os.path.dirname(os.path.abspath("config.yaml"))
os.environ["PRODUCTSKKDIR"] = project_root
appConfig = confuse.Configuration('ProductsKK')

db_conn = dict()
db_conn['username'] = urllib.parse.quote_plus(str(appConfig['db']['user']))
db_conn['password'] = urllib.parse.quote_plus(str(appConfig['db']['pass']))
db_conn['host'] = str(appConfig['db']['host'])
db_conn['port'] = str(appConfig['db']['port'])
db_conn['name'] = str(appConfig['db']['name'])

client = pymongo.MongoClient(
    'mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1'
    %
    (db_conn['username'], db_conn['password'], db_conn['host'], db_conn['port'], db_conn['name'])
)

db = client[str(appConfig['db']['name'])]