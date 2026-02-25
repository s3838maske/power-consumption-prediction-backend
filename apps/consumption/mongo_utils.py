import pymongo
from django.conf import settings

def get_mongo_collection(collection_name):
    """Get a raw pymongo collection, bypassing djongo's broken SQL translator."""
    db_config = settings.DATABASES['default']
    client_cfg = db_config.get('CLIENT', {})
    host = client_cfg.get('host', 'localhost')
    port = client_cfg.get('port', 27017)
    db_name = db_config.get('NAME', 'power_consumption_db')

    # If host is a full URI (mongodb://... or mongodb+srv://...), use it directly
    if isinstance(host, str) and host.startswith('mongodb'):
        client = pymongo.MongoClient(host)
    else:
        username = client_cfg.get('username', '')
        password = client_cfg.get('password', '')
        if username and password:
            client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        else:
            client = pymongo.MongoClient(host=host, port=port)

    return client[db_name][collection_name]
