from alphagram import Alpha, idle
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from .config import *
import sys
import os
import requests

BIU = BACKGROUND_IMAGE_URL

def database():
  mongo = MongoClient(MONGO_DB_URI)
  db = mongo.SPL
  return db

def init_bg():
  g = requests.get(BIU)
  try:
    os.mkdir("Images")
  except:
    pass
  with open("Images/bg.jpg", "wb") as f:
    f.write(g.content)

try:
  if API_ID and API_HASH:
    alpha = Alpha("SpLFW", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=dict(root='Spoiled/SpoiledPlugins'))
  else:
    alpha = Alpha("SpLFW", bot_token=BOT_TOKEN, plugins=dict(root='Spoiled/SpoiledPlugins'))
except Exception as e:
  print(e)
  sys.exit()

def __initialize__():  
  try:
    database()
    print("SpL Database Initialised ✔️")
  except:
    print("Cannot connect to Database !")
    sys.exit()
    
  try:
    init_bg()
    try:
      os.mkdir("saved_images")
    except:
      pass
    print("Background Image Loaded ✔️")
  except:
    print("Background Image Load Failed !")
    sys.exit()
  
  try:
    alpha.start()
    print("Bot Started ✔️")
    idle()
  except Exception as e:
    print(e)
    sys.exit()
  
