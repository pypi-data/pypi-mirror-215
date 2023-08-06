from . import database

db = database()

db = db.record

async def update_record(user_id: int, time: float):
  x = await db.find_one({"_": "_"})
  if x:
    prev = x['time']
    if time < prev:
      prev = time
  else:
    prev = time
  await db.update_one({"_": "_"}, {"$set": {"time": prev}}, upsert=True)  

async def get_record(user_id: int):
  x = await db.find_one({"_": "_"})
  if x:
    prev = x['time']
    return prev
  return None
