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

print("Manually assigning integer IDs to users...")
i = 1
for doc in collection.find({'id': {'$exists': False}}):
    email = doc.get('email')
    collection.update_one({'_id': doc['_id']}, {'$set': {'id': i}})
    print(f"Assigned ID {i} to {email}")
    i += 1
print("Done.")
