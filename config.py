from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv(override=True)


TOKEN = os.getenv("CR_TOKEN")
#DB_NAME = os.getenv("DB_NAME")
#COLLECTION_NAME = os.getenv("COLLECTION_NAME")
CLUSTER = os.getenv("CLUSTER")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")



class Config:
    MONGO_ATLAS_URI = f'mongodb+srv://{USER_NAME}:{PASSWORD}@{CLUSTER}.puef2.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}'
    CR_MONGODB_URI = MongoClient("mongodb://localhost:27017/clash")
    CR_API_URL = 'https://developer.clashroyale.com/v1/'
    API_TOKEN = TOKEN



client = MongoClient(Config.MONGO_ATLAS_URI)



db = client["clashdb"]
collectionPlayers = db['cr_players']
collectionBattles = db['cr_battles']
