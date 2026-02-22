import os
import django
from pymongo import MongoClient
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.authentication.models import User

# Get MongoDB details from config
mongo_uri = config('MONGODB_URI', default=None)
db_name = config('MONGODB_NAME', default='power_consumption_db')

if mongo_uri:
    client = MongoClient(mongo_uri)
else:
    host = config('MONGODB_HOST', default='localhost')
    port = int(config('MONGODB_PORT', default=27017))
    user = config('MONGODB_USER', default='')
    password = config('MONGODB_PASSWORD', default='')
    if user and password:
        client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/{db_name}")
    else:
        client = MongoClient(host, port)

db = client[db_name]
collection = db['authentication_user']

print(f"Direct MongoDB access to collection 'authentication_user'")

# Delete ALL users with email 'admin@gmail.com' to start fresh
result = collection.delete_many({'email': 'admin@gmail.com'})
print(f"Deleted {result.deleted_count} documents from MongoDB with email admin@gmail.com")

# Delete any users with null ID or non-integer ID if possible, though 'id' in djongo is usually mapped
# In djongo, the '_id' field is used. Let's look for documents with email admin@gmail.com specifically.

# Ensure we create ONE fresh admin
try:
    User.objects.create_superuser(
        email='admin@gmail.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("Re-created clean admin@gmail.com with password: admin123")
except Exception as e:
    print(f"Error creating superuser: {e}")

# Verify current users
print("\nCurrent Users in DB:")
for user in User.objects.all():
    print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")
