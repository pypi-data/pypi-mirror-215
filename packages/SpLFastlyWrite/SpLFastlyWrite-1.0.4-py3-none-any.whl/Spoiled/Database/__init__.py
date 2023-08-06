from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Spoiled.Shannu.config import MONGO_DB_URI

def database():
  mongo = MongoClient(MONGO_DB_URI)
  db = mongo.SPL
  return db
