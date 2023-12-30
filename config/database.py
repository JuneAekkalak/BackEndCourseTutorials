from pymongo import MongoClient
from core.config import settings

def get_mongo_connection():
    user_name = settings.user_name
    pass_word = settings.pass_word
    host = settings.host

    uri = f"mongodb+srv://{user_name}:{pass_word}@{host}/test"

    try:
        client = MongoClient(uri, ssl=True)
        
        client.list_database_names()
        
        return client

    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")

try:
    client = get_mongo_connection()
    
    db = client.course
    course_collection = db["course"]

except ConnectionError as ce:
    print(ce)
    
