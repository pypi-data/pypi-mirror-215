from . import database
from ..SpoiledPlugins import _sort

db = database()

db = db.completed

async def incr_word(user_id: int, chat_id: int):
  chat_id = str(chat_id)
  x = await db.find_one({"user_id": user_id})
  if x:
    dic = x["dic"]
  else:
    dic = {}
  if chat_id in dic:
    dic[chat_id] += 1
  else:
    dic[chat_id] = 1
  await db.update_one({"user_id": user_id}, {"$set": {"dic": dic}}, upsert=True)

async def get_completed_words(user_id: int, chat_id: int = None):
  if chat_id:
    chat_id = str(chat_id)
  x = await db.find_one({"user_id": user_id})
  if x:
    dic = x['dic']
    if chat_id:
      if chat_id in dic:
        return dic[chat_id]
      return 0
    tot = 0
    for y in dic:
      tot += dic[y]
    return tot
  return 0

async def get_top_chat(user_id: int):
  x = await db.find_one({"user_id": user_id})
  if x:
    dic = x['dic']
    dic = _sort(dic)
    for y in dic:
      return y
  return None
