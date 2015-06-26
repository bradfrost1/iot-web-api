from motor import MotorClient
from pymongo.errors import CollectionInvalid


COLLECTION_SIZE = (30 * 1024 ** 2) # ~30Mb


client = MotorClient('mongodb://db:27017')
db = client['inteliotroadshow2015']

# Create a capped collection to Stream data
db.create_collection('stream', capped=True, size=COLLECTION_SIZE,
    callback=lambda x, y: (x, y))
