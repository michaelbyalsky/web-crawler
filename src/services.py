from pymongo import MongoClient
import os


def connect_to_mongodb():
    try:
        client = MongoClient(f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}")
        db = client.db
        collection = db["pastedb"]
        print('sucessfully connected to mongo')
    except Exception as e:
        print("exeption:", e)
    return collection
