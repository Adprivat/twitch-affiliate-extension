# models.py
from pymongo import MongoClient
from config import MONGO_URI
import datetime

# Establish connection to MongoDB
client = MongoClient(MONGO_URI)
db = client['twitch_affiliate_db']
affiliate_collection = db['affiliates']

def get_affiliate(streamer_id):
    """
    Retrieve affiliate data for a given streamer_id.
    """
    return affiliate_collection.find_one({"streamer_id": streamer_id}, {"_id": 0})

def create_affiliate(data):
    """
    Create a new affiliate entry.
    The 'data' dictionary should include 'streamer_id' and 'affiliate_url'.
    """
    data['created_at'] = datetime.datetime.utcnow()
    data['updated_at'] = datetime.datetime.utcnow()
    result = affiliate_collection.insert_one(data)
    return result.inserted_id

def update_affiliate(streamer_id, affiliate_url):
    """
    Update the affiliate_url for a given streamer_id.
    """
    result = affiliate_collection.update_one(
        {"streamer_id": streamer_id},
        {"$set": {"affiliate_url": affiliate_url, "updated_at": datetime.datetime.utcnow()}}
    )
    return result.modified_count

def delete_affiliate(streamer_id):
    """
    Delete an affiliate entry by streamer_id.
    """
    result = affiliate_collection.delete_one({"streamer_id": streamer_id})
    return result.deleted_count
