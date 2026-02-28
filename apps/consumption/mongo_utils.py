import pymongo
from django.conf import settings

# Single MongoClient per process — avoids connection storm (Djongo production best practice)
_cached_client = None
_cached_db_name = None


def _get_client():
    global _cached_client, _cached_db_name
    if _cached_client is not None:
        return _cached_client, _cached_db_name
    db_config = settings.DATABASES['default']
    client_cfg = db_config.get('CLIENT', {})
    host = client_cfg.get('host', 'localhost')
    port = client_cfg.get('port', 27017)
    db_name = db_config.get('NAME', 'power_consumption_db')

    if isinstance(host, str) and host.startswith('mongodb'):
        _cached_client = pymongo.MongoClient(host)
    else:
        username = client_cfg.get('username', '')
        password = client_cfg.get('password', '')
        if username and password:
            _cached_client = pymongo.MongoClient(host=host, port=port, username=username, password=password)
        else:
            _cached_client = pymongo.MongoClient(host=host, port=port)
    _cached_db_name = db_name
    return _cached_client, _cached_db_name


def get_mongo_collection(collection_name):
    """Get a raw pymongo collection; uses a single cached MongoClient per process."""
    client, db_name = _get_client()
    return client[db_name][collection_name]
