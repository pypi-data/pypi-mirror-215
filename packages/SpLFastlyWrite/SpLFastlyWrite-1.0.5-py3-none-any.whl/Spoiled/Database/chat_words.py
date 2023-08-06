from . import database
from ..SpoiledPlugins import _sort

db = database()

db = db.chat_words

async def incr_chat_word(chat_id: int, user_id: int):
  user_id = str(user_id)
  x = await db.find_one({"chat_id": chat_id})
  if x:
    dic = x['dic']
  else:
    dic = {}
  if user_id in dic:
    dic[user_id] += 1
  else:
    dic[user_id] = 1
  await db.update_one({"chat_id": chat_id}, {"$set": {"dic": dic}}, upsert=True)
  
async def get_chat_words(chat_id: int):
  x = await db.find_one({"chat_id": chat_id})
  if x:
    dic = x['dic']
    tot = 0
    for y in dic:
      tot += dic[y]
    return tot
  return 0

async def get_top_chat_users(chat_id: int) -> dict:
  x = await db.find_one({"chat_id": chat_id})
  if x:
    dic = x['dic']
    dic = _sort(dic)
    return dic
  return {}
