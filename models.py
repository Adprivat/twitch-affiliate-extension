# models.py
from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client['my_affiliate_db']         # Datenbankname: my_affiliate_db
affiliate_collection = db['affiliates'] # Collectionname: affiliates

def get_affiliate(streamer_id):
    """
    Retrieves the affiliate document for the given streamer_id.
    """
    return affiliate_collection.find_one({"streamer_id": streamer_id}, {"_id": 0})

def create_affiliate(data):
    """
    Creates a new affiliate document.
    Sets created_at and updated_at timestamps.
    Falls ein Fehler auftritt, wird dieser geloggt und weitergegeben.
    """
    try:
        data['created_at'] = datetime.datetime.utcnow()
        data['updated_at'] = datetime.datetime.utcnow()
        result = affiliate_collection.insert_one(data)
        return result.inserted_id
    except Exception as e:
        print("Error in create_affiliate:", e)
        raise

def update_affiliate(streamer_id, affiliate_url):
    """
    Updates the affiliate_url for the given streamer_id and sets updated_at.
    """
    result = affiliate_collection.update_one(
        {"streamer_id": streamer_id},
        {"$set": {"affiliate_url": affiliate_url, "updated_at": datetime.datetime.utcnow()}}
    )
    return result.modified_count

def delete_affiliate(streamer_id):
    """
    Deletes the affiliate document for the given streamer_id.
    """
    result = affiliate_collection.delete_one({"streamer_id": streamer_id})
    return result.deleted_count
