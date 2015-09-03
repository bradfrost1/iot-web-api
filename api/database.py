import os

from motor import MotorClient
from pymongo.errors import CollectionInvalid


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://db:27017')
DEFAULT_COLLECTION_SIZE = (30 * 1024 ** 2) # ~30Mb


def get_db_conn(db_name='iot_simple_api'):
    conn = MotorClient(MONGODB_URI)
    db = conn[db_name]
    # Create a capped collection to Stream data
    db.create_collection('stream', capped=True, size=DEFAULT_COLLECTION_SIZE,
        callback=lambda x, y: (x, y))

    return db, conn
