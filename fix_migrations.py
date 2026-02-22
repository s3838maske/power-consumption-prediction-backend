import os
import django
from django.conf import settings
from pymongo import MongoClient
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Get DB config
db_config = settings.DATABASES['default']
client_config = db_config.get('CLIENT', {})

print(f"Connecting to MongoDB...")
if 'host' in client_config and client_config['host'].startswith('mongodb+srv'):
    client = MongoClient(client_config['host'])
else:
    client = MongoClient(
        host=client_config.get('host', 'localhost'),
        port=client_config.get('port', 27017),
        username=client_config.get('username', ''),
        password=client_config.get('password', '')
    )

db = client[db_config['NAME']]
migrations_col = db['django_migrations']

# Check if authentication 0001_initial is missing
exists = migrations_col.find_one({"app": "authentication", "name": "0001_initial"})

if not exists:
    print("Record missing. Inserting 'authentication.0001_initial' into django_migrations...")
    migrations_col.insert_one({
        "app": "authentication",
        "name": "0001_initial",
        "applied": datetime.now()
    })
    print("Success!")
else:
    print("Record already exists.")

client.close()
