from . import database

db = database()

db = db.privacy

async def enable_privacy(user_id: int):
  x = await db.find_one({"user_id": user_id})
  if not x:
    await db.insert_one({"user_id": user_id})

async def disable_privacy(user_id: int):
  x = await db.find_one({"user_id": user_id})
  if x:
    await db.delete_one({"user_id": user_id})

async def get_private_users() -> list:
  x =  db.find({"user_id": {"$gt": 0}})
  if not x:
    return []
  x = await x.to_list(length=1000000)
  lis = []
  for y in x:
    lis.append(y['user_id'])
  return lis
    
