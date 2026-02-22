import os
import django
from django.conf import settings
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
db = client[settings.DATABASES['default']['NAME']]
collections = db.list_collection_names()
print(f"Collections: {collections}")
client.close()
