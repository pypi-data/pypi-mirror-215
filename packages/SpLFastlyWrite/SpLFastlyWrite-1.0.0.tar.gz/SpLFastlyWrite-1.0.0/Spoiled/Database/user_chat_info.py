from . import database

db = database()

udb = db.user_info

async def update_user_info(user_id: int, info):
    await udb.update_one({"user_id": user_id}, {"$set": {"info": info}}, upsert=True)

async def get_user_info(user_id: int):
    x = await udb.find_one({"user_id": user_id})
    if not x:
        return {}
    return x["info"]

cdb = db.chat_info

async def update_chat_info(chat_id: int, info):
    await cdb.update_one({"chat_id": chat_id}, {"$set": {"info": info}}, upsert=True)

async def get_chat_info(chat_id: int):
    x = await cdb.find_one({"chat_id": chat_id})
    if not x:
        return {}
    return x["info"]
