from pymongo import MongoClient


def connect_to_mongodb(mongo_url):
    try:
        client = MongoClient(mongo_url)
        print('sucessfully connected to mongo')
    except Exception as e:
        print(e)
    db = client["scrawler"]
    collection = db["pastes"]
    return collection
