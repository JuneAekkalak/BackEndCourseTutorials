from pymongo import MongoClient
import ssl
from core import config

ssl._create_default_https_context = ssl._create_unverified_context


client = MongoClient("mongodb+srv://"+config.settings.user_name+":"+config.settings.pass_word+"@"+config.settings.host+"/test", ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

db = client.course

collection_name = db["course"]