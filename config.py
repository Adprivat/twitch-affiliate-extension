# config.py
import os

# MongoDB-Verbindungszeichenfolge.
# Achte darauf, dass hier keine zusätzlichen Leerzeichen oder Zeilenumbrüche enthalten sind.
MONGO_URI = os.environ.get(
    'MONGO_URI',
    "mongodb+srv://Testbenutzer:Kira2018%3F%3F%3F@testcluster1.6xbqa.mongodb.net/my_affiliate_db?retryWrites=true&w=majority"
).strip()
