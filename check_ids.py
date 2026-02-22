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

print("Checking documents for 'id' field...")
for doc in collection.find().limit(10):
    print(f"Email: {doc.get('email')}, id field exists: {'id' in doc}, id value: {doc.get('id')}")
