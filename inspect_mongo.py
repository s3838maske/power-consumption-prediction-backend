from pymongo import MongoClient
from decouple import config

mongo_uri = config('MONGODB_URI', default=None)
db_name = config('MONGODB_NAME', default='power_consumption_db')

if mongo_uri:
    client = MongoClient(mongo_uri)
else:
    host = config('MONGODB_HOST', default='localhost')
    port = int(config('MONGODB_PORT', default=27017))
    client = MongoClient(host, port)

db = client[db_name]
collection = db['authentication_user']

for doc in collection.find({'email': 'admin@gmail.com'}):
    print(doc)
