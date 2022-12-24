import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["CIAN"]
col = db["Flat_Data"]
tdb = db["Telegram_Data"]

