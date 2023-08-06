from . import database

db = database()

db = db.usersdb

async def add_served_user(user_id: int):
    x = await db.find_one({"user_id": user_id})
    if not x:
        return await db.insert_one({"user_id": user_id})

async def rmv_served_user(user_id: int):
    x = await db.find_one({"user_id": user_id})
    if x:
        return await db.delete_one({"user_id": user_id})

async def get_served_users():
    x = db.find({'user_id': {'$gt': 0}})
    if not x:
        return []
    x = await x.to_list(length=1000000)
    lis = []
    for y in x:
        lis.append(y['user_id'])
    return lis
