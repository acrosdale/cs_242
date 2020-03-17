from pymongo import MongoClient
import csv


def getDataFromDB():
    client = MongoClient(
        'mongodb://root:pleaseUseAStr0ngPassword@mongod:27017/admin')
    collection_name = 'django'
    db = client['%s' % collection_name]
    collection = db['twit_tweet']
    cursor = collection.find({})
    with open('collection.csv', 'w', newline='') as file:
        fieldnames = ['id', 'text']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # writer.writeheader()
        for document in cursor:
            del document["_id"]
            del document["created_at"]
            writer.writerow({
                "id": document["id"],
                "text": document["text"].encode('ascii', 'ignore')
            })


getDataFromDB()