import pymongo
from Default_values import *
client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["CIAN"]
col = db["Flat_Data"]
tdb = db["Telegram_Data"]


def user_init(user_id):
    if tdb.find_one({'_id': user_id}) is None:
        tdb.insert_one({"_id": user_id})
    tdb.update_one({'_id': user_id},
                   {'$set': {'low_price': MIN_PRICE,
                             'high_price': MAX_PRICE,
                             'low_area': MIN_AREA,
                             'high_area': MAX_AREA,
                             'type': " ",
                             "active_param": "NO"}
                    })
