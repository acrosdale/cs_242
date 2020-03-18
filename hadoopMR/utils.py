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
        fieldnames = ['_id', 'text']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for document in cursor:
            writer.writerow({
                "_id": str(document["_id"]),
                "text": document["text"].encode('ascii', 'ignore'),
                # "location": location
            })


getDataFromDB()